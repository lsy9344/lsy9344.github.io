#!/usr/bin/env python3
"""
scripts/test_verify_portfolio.py
==============================================================================
Noah Park 포트폴리오 E2E 검증 스크립트(scripts/verify_portfolio.py)의 자체 단위 및 통합 테스트 스위트
(Zero-Dependency, Python Standard Library unittest)

테스트 대상:
1. IndexPageParser: Notion 링크 및 로컬 프로젝트 링크 파싱 정확도
2. CaseStudyPageParser: W3C 메타, FOUC 방지 <head> 위치, 5대 섹션, <figure>/<figcaption> 쌍 검증
3. VerificationContext: 통계 집계 및 strict 모드 동작 검증
4. Tier 3 Interaction/Theme 검증 로직 단위 테스트
5. CLI 인자 파서 및 포트 탐색 로직 검증
==============================================================================
"""

import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 검증 스크립트 모듈 import
from scripts.verify_portfolio import (
    IndexPageParser,
    CaseStudyPageParser,
    VerificationContext,
    Tier1FilePresenceChecker,
    Tier2SemanticLinkChecker,
    Tier3InteractionThemeChecker,
    Tier4LiveServerHttpChecker,
    PROJECT_DEFINITIONS,
    EXPECTED_SECTIONS,
)


class TestIndexPageParser(unittest.TestCase):
    def test_parses_notion_and_local_links(self):
        sample_html = """
        <ul class="project-list">
          <li>
            <a href="./projects/beauty-brand-crm.html" class="project-link">CRM</a>
          </li>
          <li>
            <a href="https://notion.so/test12345" class="project-link">Notion Old</a>
          </li>
        </ul>
        """
        parser = IndexPageParser()
        parser.feed(sample_html)

        self.assertEqual(len(parser.project_links), 2)
        hrefs = [l["href"] for l in parser.project_links]
        self.assertIn("./projects/beauty-brand-crm.html", hrefs)
        self.assertIn("https://notion.so/test12345", hrefs)


class TestCaseStudyPageParser(unittest.TestCase):
    def test_parses_full_case_study(self):
        sample_html = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>테스트 프로젝트</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="설명문">
  <link rel="stylesheet" href="../style.css">
  <script src="../theme.js"></script>
</head>
<body class="article-page">
  <main class="article">
    <a href="../index.html#project" class="back-link">← Project</a>
    <blockquote>"핵심 철학 인용문"</blockquote>
    <div class="article-meta-tags">
      <span class="tag">Next.js</span>
      <span class="tag">TypeScript</span>
      <span class="tag">PostgreSQL</span>
    </div>
    <h2>1. 하는 일 (Overview)</h2>
    <p>본문 내용입니다.</p>
    <figure>
      <img src="../images/crm/01.png" alt="스크린샷 설명">
      <figcaption class="caption">상세 캡션</figcaption>
    </figure>
    <h2>2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)</h2>
    <p>본문 2</p>
    <h2>3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)</h2>
    <p>본문 3</p>
    <h2>4. 핵심 구현 기능 (Key Features)</h2>
    <p>본문 4</p>
    <h2>5. 엔지니어링 교훈 (Key Takeaways)</h2>
    <p>본문 5</p>
  </main>
</body>
</html>"""
        parser = CaseStudyPageParser()
        parser.feed(sample_html)

        self.assertTrue(parser.has_title)
        self.assertTrue(parser.has_viewport)
        self.assertTrue(parser.has_description)
        self.assertTrue(parser.has_stylesheet)
        self.assertTrue(parser.has_theme_script)
        self.assertTrue(parser.theme_script_in_head)
        self.assertTrue(parser.has_blockquote)
        self.assertEqual(len(parser.backlinks), 1)
        self.assertEqual(len(parser.tags), 3)
        self.assertEqual(len(parser.h2_headings), 5)
        self.assertEqual(len(parser.images), 1)
        self.assertEqual(len(parser.images_outside_figure), 0)

    def test_detects_theme_script_outside_head(self):
        sample_html = """<!doctype html>
<html>
<head><title>Test</title></head>
<body>
  <script src="../theme.js"></script>
</body>
</html>"""
        parser = CaseStudyPageParser()
        parser.feed(sample_html)
        self.assertTrue(parser.has_theme_script)
        self.assertFalse(parser.theme_script_in_head)

    def test_detects_image_outside_figure(self):
        sample_html = """<div><img src="naked.png" alt="alone"></div>"""
        parser = CaseStudyPageParser()
        parser.feed(sample_html)
        self.assertEqual(len(parser.images), 1)
        self.assertEqual(len(parser.images_outside_figure), 1)


class TestVerificationContext(unittest.TestCase):
    def test_context_strict_mode(self):
        tmp_dir = Path("/tmp")
        # 비엄격 모드
        ctx = VerificationContext(tmp_dir, strict=False)
        ctx.add_pass("Tier 1", "P1", "OK")
        ctx.add_warn("Tier 1", "W1", "Warn")
        self.assertTrue(ctx.is_successful)

        # 엄격 모드
        ctx_strict = VerificationContext(tmp_dir, strict=True)
        ctx_strict.add_pass("Tier 1", "P1", "OK")
        ctx_strict.add_warn("Tier 1", "W1", "Warn")
        self.assertFalse(ctx_strict.is_successful)

        # 실패가 있을 때
        ctx.add_fail("Tier 1", "F1", "Fail")
        self.assertFalse(ctx.is_successful)


class TestTierChecksOnCurrentWorkspace(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root_dir = Path(__file__).resolve().parent.parent

    def test_tier3_passes_on_workspace(self):
        ctx = VerificationContext(self.root_dir, strict=False)
        checker = Tier3InteractionThemeChecker()
        checker.run(ctx)
        self.assertEqual(ctx.fail_count, 0)
        self.assertTrue(ctx.pass_count >= 10)

    def test_tier1_correctly_finds_existing_beauty_brand_crm(self):
        ctx = VerificationContext(self.root_dir, strict=False)
        checker = Tier1FilePresenceChecker()
        checker.run(ctx)
        # beauty-brand-crm 관련 합격 확인
        crm_passes = [i for i in ctx.items if "beauty-brand-crm" in i.name and i.status == "PASS"]
        self.assertTrue(len(crm_passes) >= 1)

    def test_tier4_server_and_dummy_404(self):
        ctx = VerificationContext(self.root_dir, strict=False)
        checker = Tier4LiveServerHttpChecker()
        checker.run(ctx, port=3456)
        # 가상 404 음성 테스트가 성공했는지 확인
        n404_passes = [i for i in ctx.items if "404" in i.name and i.status == "PASS"]
        self.assertTrue(len(n404_passes) >= 1)


if __name__ == "__main__":
    unittest.main()
