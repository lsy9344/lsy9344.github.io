#!/usr/bin/env python3
"""
scripts/verify_portfolio.py
==============================================================================
Noah Park 포트폴리오 웹사이트 E2E 4-Tier 종합 검증 스크립트
(Zero-Dependency, Pure Python Standard Library)

[검증 아키텍처: 4-Tier 검증 피라미드]
- Tier 1: 정적 파일 실재성 및 0-byte 방지 (HTML, 이미지 디렉토리, 용량)
- Tier 2: HTML 시맨틱 및 링크 무결성 (이미지 404 역추적, <figure>/<figcaption>, 5대 섹션)
- Tier 3: 클라이언트 인터랙션 & 테마 무결성 (CSS Focus-Dim 선택자, theme.js IIFE, CSS 변수)
- Tier 4: 실서버 환경 E2E 크롤링 (백그라운드 로컬 웹서버 기동, 전수 리소스 HTTP 200 OK, 404 음성 테스트)

초보 개발자도 쉽게 이해하고 문제를 수정할 수 있도록 친절한 디버깅 팁([Tip])을 제공합니다.
==============================================================================
"""

import sys
import os
import re
import json
import time
import socket
import argparse
import threading
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, unquote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from typing import List, Dict, Optional, Tuple, Any

# ----------------------------------------------------------------------------
# 1. 터미널 컬러 및 스타일 상수 (초보 개발자 친화적 UI)
# ----------------------------------------------------------------------------
class TerminalColors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GRAY = "\033[90m"

    @classmethod
    def pass_badge(cls) -> str:
        return f"{cls.BOLD}{cls.GREEN}[PASS]{cls.RESET}"

    @classmethod
    def fail_badge(cls) -> str:
        return f"{cls.BOLD}{cls.RED}[FAIL]{cls.RESET}"

    @classmethod
    def warn_badge(cls) -> str:
        return f"{cls.BOLD}{cls.YELLOW}[WARN]{cls.RESET}"

    @classmethod
    def info_badge(cls) -> str:
        return f"{cls.BOLD}{cls.CYAN}[INFO]{cls.RESET}"


# ----------------------------------------------------------------------------
# 2. 14개 프로젝트 기준 데이터 명세 (PROJECT.md & TEST_INFRA.md 기반)
# ----------------------------------------------------------------------------
PROJECT_DEFINITIONS = [
    {
        "slug": "beauty-brand-crm",
        "name": "뷰티 브랜드 고객 CRM",
        "html_path": "projects/beauty-brand-crm.html",
        "images_dir": "images/crm",
        "requires_images": True,
    },
    {
        "slug": "beauty-review-platform",
        "name": "뷰티 브랜드 상품 후기 플랫폼",
        "html_path": "projects/beauty-review-platform.html",
        "images_dir": "images/beauty-review-platform",
        "requires_images": True,
    },
    {
        "slug": "beauty-band-automation",
        "name": "뷰티 브랜드 BAND 운영 자동화",
        "html_path": "projects/beauty-band-automation.html",
        "images_dir": "images/beauty-band-automation",
        "requires_images": True,
    },
    {
        "slug": "beauty-erp-inventory",
        "name": "뷰티 브랜드 사내 ERP",
        "html_path": "projects/beauty-erp-inventory.html",
        "images_dir": "images/beauty-erp-inventory",
        "requires_images": True,
    },
    {
        "slug": "boothy-photo-booth",
        "name": "Boothy 무인 사진관 제어",
        "html_path": "projects/boothy-photo-booth.html",
        "images_dir": None,  # Text & Architecture only
        "requires_images": False,
    },
    {
        "slug": "multi-branch-studio-erp",
        "name": "다지점 사진관 운영 ERP",
        "html_path": "projects/multi-branch-studio-erp.html",
        "images_dir": "images/multi-branch-studio-erp",
        "requires_images": True,
    },
    {
        "slug": "sms-automation-review",
        "name": "다지점 문자 발송 자동화",
        "html_path": "projects/sms-automation-review.html",
        "images_dir": "images/sms-automation-review",
        "requires_images": True,
    },
    {
        "slug": "cuteditor-photo-tool",
        "name": "브라우저 사진 편집 도구",
        "html_path": "projects/cuteditor-photo-tool.html",
        "images_dir": "images/cuteditor-photo-tool",
        "requires_images": True,
    },
    {
        "slug": "vietnam-aesthetic-erp",
        "name": "베트남 에스테틱 ERP",
        "html_path": "projects/vietnam-aesthetic-erp.html",
        "images_dir": "images/vietnam-aesthetic-erp",
        "requires_images": True,
    },
    {
        "slug": "seafood-distribution-erp",
        "name": "수산물 유통 통합 ERP",
        "html_path": "projects/seafood-distribution-erp.html",
        "images_dir": "images/seafood-distribution-erp",
        "requires_images": True,
    },
    {
        "slug": "military-meal-management",
        "name": "군부대 식권·급여 공제 관리",
        "html_path": "projects/military-meal-management.html",
        "images_dir": "images/military-meal-management",
        "requires_images": True,
    },
    {
        "slug": "multimarket-crawler",
        "name": "멀티마켓 공개정보 수집",
        "html_path": "projects/multimarket-crawler.html",
        "images_dir": "images/multimarket-crawler",
        "requires_images": True,
    },
    {
        "slug": "kakaotalk-unread-excel",
        "name": "카카오톡 1:1 대화방 정리",
        "html_path": "projects/kakaotalk-unread-excel.html",
        "images_dir": "images/kakaotalk-unread-excel",
        "requires_images": True,
    },
    {
        "slug": "tactrun-delivery-landing",
        "name": "배달센터 실적 소개 웹 (TactRun)",
        "html_path": "projects/tactrun-delivery-landing.html",
        "images_dir": "images/tactrun-delivery-landing",
        "requires_images": True,
    },
]

REQUIRED_COMMON_FILES = [
    {"path": "index.html", "min_bytes": 2000, "desc": "메인 포트폴리오 인덱스 페이지"},
    {"path": "style.css", "min_bytes": 1000, "desc": "Karri & Arlan 융합 디자인 CSS"},
    {"path": "theme.js", "min_bytes": 500, "desc": "FOUC 방지 테마 제어 스크립트"},
]

EXPECTED_SECTIONS = [
    {"num": 1, "pattern": r"1\.\s*하는\s*일.*Overview", "title": "1. 하는 일 (Overview)"},
    {"num": 2, "pattern": r"2\.\s*해결한\s*문제.*Problem\s*&\s*Integrity", "title": "2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)"},
    {"num": 3, "pattern": r"3\.\s*시스템\s*아키텍처.*Architecture\s*&\s*Flow", "title": "3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)"},
    {"num": 4, "pattern": r"4\.\s*핵심\s*구현\s*기능.*Key\s*Features", "title": "4. 핵심 구현 기능 (Key Features)"},
    {"num": 5, "pattern": r"5\.\s*엔지니어링\s*교훈.*Key\s*Takeaways", "title": "5. 엔지니어링 교훈 (Key Takeaways)"},
]


# ----------------------------------------------------------------------------
# 3. 검증 결과 레코드 및 실행 컨텍스트
# ----------------------------------------------------------------------------
class CheckItem:
    def __init__(
        self,
        tier: str,
        name: str,
        status: str,  # "PASS", "FAIL", "WARN"
        message: str,
        tip: Optional[str] = None,
        file_path: Optional[str] = None,
        line_no: Optional[int] = None,
    ):
        self.tier = tier
        self.name = name
        self.status = status
        self.message = message
        self.tip = tip
        self.file_path = file_path
        self.line_no = line_no

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier": self.tier,
            "name": self.name,
            "status": self.status,
            "message": self.message,
            "tip": self.tip,
            "file_path": self.file_path,
            "line_no": self.line_no,
        }


class VerificationContext:
    def __init__(self, root_dir: Path, strict: bool = False):
        self.root_dir = root_dir.resolve()
        self.strict = strict
        self.items: List[CheckItem] = []

    def add_pass(self, tier: str, name: str, message: str, file_path: Optional[str] = None):
        self.items.append(CheckItem(tier, name, "PASS", message, file_path=file_path))

    def add_fail(
        self,
        tier: str,
        name: str,
        message: str,
        tip: Optional[str] = None,
        file_path: Optional[str] = None,
        line_no: Optional[int] = None,
    ):
        self.items.append(CheckItem(tier, name, "FAIL", message, tip, file_path, line_no))

    def add_warn(
        self,
        tier: str,
        name: str,
        message: str,
        tip: Optional[str] = None,
        file_path: Optional[str] = None,
        line_no: Optional[int] = None,
    ):
        self.items.append(CheckItem(tier, name, "WARN", message, tip, file_path, line_no))

    @property
    def pass_count(self) -> int:
        return sum(1 for i in self.items if i.status == "PASS")

    @property
    def fail_count(self) -> int:
        return sum(1 for i in self.items if i.status == "FAIL")

    @property
    def warn_count(self) -> int:
        return sum(1 for i in self.items if i.status == "WARN")

    @property
    def is_successful(self) -> bool:
        if self.strict:
            return self.fail_count == 0 and self.warn_count == 0
        return self.fail_count == 0


# ----------------------------------------------------------------------------
# 4. HTML 파서 및 구문 분석 도우미
# ----------------------------------------------------------------------------
class IndexPageParser(HTMLParser):
    """index.html 내 프로젝트 링크와 아카이브 링크를 분석하는 파서"""
    def __init__(self):
        super().__init__()
        self.in_project_list = False
        self.current_a_href = None
        self.project_links: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()

        if tag == "ul" and "project-list" in classes:
            self.in_project_list = True

        if tag == "a" and self.in_project_list:
            href = attr_dict.get("href", "")
            is_proj_link = "project-link" in classes
            line_no = self.getpos()[0]
            self.project_links.append({
                "href": href,
                "classes": classes,
                "is_project_link": is_proj_link,
                "line": line_no,
            })

    def handle_endtag(self, tag: str):
        if tag == "ul" and self.in_project_list:
            self.in_project_list = False


class CaseStudyPageParser(HTMLParser):
    """projects/*.html 케이스 스터디 상세 페이지의 W3C 시맨틱 및 이미지/링크 분석기"""
    def __init__(self):
        super().__init__()
        self.has_title = False
        self.has_viewport = False
        self.has_description = False
        self.has_stylesheet = False
        self.has_theme_script = False
        self.theme_script_in_head = False
        self.in_head = False
        self.in_blockquote = False
        self.has_blockquote = False

        self.backlinks: List[Dict[str, Any]] = []
        self.h2_headings: List[Dict[str, Any]] = []
        self.tags: List[str] = []

        self.in_figure = False
        self.figure_count = 0
        self.figcaption_count = 0
        self.images: List[Dict[str, Any]] = []
        self.images_outside_figure: List[Dict[str, Any]] = []

        self.current_tag = None
        self.text_buffer = []
        self.current_h2_text = []
        self.in_h2 = False
        self.in_tag_span = False
        self.current_tag_text = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]):
        attr_dict = dict(attrs)
        line_no = self.getpos()[0]

        if tag == "head":
            self.in_head = True
        elif tag == "title":
            self.has_title = True
        elif tag == "meta":
            if attr_dict.get("name") == "viewport":
                self.has_viewport = True
            elif attr_dict.get("name") == "description":
                self.has_description = True
        elif tag == "link":
            rel = attr_dict.get("rel", "")
            href = attr_dict.get("href", "")
            if rel == "stylesheet" and "style.css" in href:
                self.has_stylesheet = True
        elif tag == "script":
            src = attr_dict.get("src", "")
            if "theme.js" in src:
                self.has_theme_script = True
                if self.in_head:
                    self.theme_script_in_head = True
        elif tag == "blockquote":
            self.has_blockquote = True
            self.in_blockquote = True
        elif tag == "a":
            href = attr_dict.get("href", "")
            classes = attr_dict.get("class", "").split()
            if "back-link" in classes or "project" in href.lower():
                self.backlinks.append({"href": href, "classes": classes, "line": line_no})
        elif tag == "h2":
            self.in_h2 = True
            self.current_h2_text = []
        elif tag == "figure":
            self.in_figure = True
            self.figure_count += 1
        elif tag == "figcaption":
            self.figcaption_count += 1
        elif tag == "img":
            src = attr_dict.get("src", "")
            alt = attr_dict.get("alt", "")
            img_data = {
                "src": src,
                "alt": alt,
                "line": line_no,
                "in_figure": self.in_figure,
            }
            self.images.append(img_data)
            if not self.in_figure:
                self.images_outside_figure.append(img_data)
        elif tag == "span" and "tag" in attr_dict.get("class", "").split():
            self.in_tag_span = True
            self.current_tag_text = []

    def handle_endtag(self, tag: str):
        if tag == "head":
            self.in_head = False
        elif tag == "blockquote":
            self.in_blockquote = False
        elif tag == "figure":
            self.in_figure = False
        elif tag == "h2":
            self.in_h2 = False
            full_h2 = "".join(self.current_h2_text).strip()
            self.h2_headings.append({"text": full_h2, "line": self.getpos()[0]})
        elif tag == "span" and self.in_tag_span:
            self.in_tag_span = False
            tag_text = "".join(self.current_tag_text).strip()
            if tag_text:
                self.tags.append(tag_text)

    def handle_data(self, data: str):
        self.text_buffer.append(data)
        if self.in_h2:
            self.current_h2_text.append(data)
        if self.in_tag_span:
            self.current_tag_text.append(data)

    def get_full_text(self) -> str:
        return "".join(self.text_buffer)


# ----------------------------------------------------------------------------
# 5. Tier 1: 정적 파일 실재성 및 0-byte 방지 검사기
# ----------------------------------------------------------------------------
class Tier1FilePresenceChecker:
    TIER_NAME = "Tier 1: 파일 실재성 & 0-byte 방지"

    def run(self, ctx: VerificationContext):
        print(f"\n{TerminalColors.BOLD}{TerminalColors.CYAN}▶ [{self.TIER_NAME}] 실행 중...{TerminalColors.RESET}")

        # 1. 공통 필수 파일 확인
        for item in REQUIRED_COMMON_FILES:
            rel_path = item["path"]
            min_bytes = item["min_bytes"]
            desc = item["desc"]
            file_path = ctx.root_dir / rel_path

            if not file_path.exists():
                ctx.add_fail(
                    tier="Tier 1",
                    name=f"공통 파일 누락: {rel_path}",
                    message=f"필수 파일 '{rel_path}'({desc})이 루트 디렉토리에 존재하지 않습니다.",
                    tip=f"프로젝트 루트에 '{rel_path}' 파일이 생성되었는지 확인하십시오.",
                    file_path=rel_path,
                )
            else:
                size = file_path.stat().st_size
                if size < min_bytes:
                    ctx.add_fail(
                        tier="Tier 1",
                        name=f"파일 크기 미달: {rel_path}",
                        message=f"'{rel_path}' 크기({size} bytes)가 최소 기준({min_bytes} bytes)보다 작습니다. (스켈레톤 또는 빈 파일 의심)",
                        tip=f"파일 내용이 정상적으로 작성되었는지 확인하십시오.",
                        file_path=rel_path,
                    )
                else:
                    ctx.add_pass(
                        tier="Tier 1",
                        name=f"공통 파일 유효: {rel_path}",
                        message=f"정상 존재 확인 ({size:,} bytes)",
                        file_path=rel_path,
                    )

        # 2. 14개 프로젝트 HTML 파일 실재성 및 크기 검사
        for proj in PROJECT_DEFINITIONS:
            slug = proj["slug"]
            html_rel = proj["html_path"]
            file_path = ctx.root_dir / html_rel

            if not file_path.exists():
                ctx.add_fail(
                    tier="Tier 1",
                    name=f"케이스 스터디 누락: {slug}",
                    message=f"프로젝트 상세 페이지 '{html_rel}'가 존재하지 않습니다.",
                    tip=f"'projects/{slug}.html' 케이스 스터디 상세 페이지를 생성하십시오.",
                    file_path=html_rel,
                )
            else:
                size = file_path.stat().st_size
                if size < 2000:
                    ctx.add_fail(
                        tier="Tier 1",
                        name=f"케이스 스터디 용량 미달: {slug}",
                        message=f"'{html_rel}' 파일 크기({size} bytes)가 2,000 bytes 미만입니다.",
                        tip=f"케이스 스터디 상세 본문 내용이 충분히 채워졌는지 확인하십시오.",
                        file_path=html_rel,
                    )
                else:
                    ctx.add_pass(
                        tier="Tier 1",
                        name=f"케이스 스터디 파일 실재: {slug}",
                        message=f"'{html_rel}' 확인 ({size:,} bytes)",
                        file_path=html_rel,
                    )

        # 3. 이미지 디렉토리 및 에셋 실재성 검사
        for proj in PROJECT_DEFINITIONS:
            slug = proj["slug"]
            img_rel = proj["images_dir"]
            req_imgs = proj["requires_images"]

            if not req_imgs or not img_rel:
                ctx.add_pass(
                    tier="Tier 1",
                    name=f"이미지 제외 프로젝트: {slug}",
                    message="텍스트 및 아키텍처 전용 프로젝트 (이미지 디렉토리 불요)",
                )
                continue

            dir_path = ctx.root_dir / img_rel
            if not dir_path.exists() or not dir_path.is_dir():
                ctx.add_fail(
                    tier="Tier 1",
                    name=f"이미지 폴더 누락: {slug}",
                    message=f"에셋 디렉토리 '{img_rel}'가 존재하지 않습니다.",
                    tip=f"노션 첨부 이미지를 다운로드하여 '{img_rel}/' 디렉토리에 저장하십시오.",
                    file_path=img_rel,
                )
            else:
                # 내부 이미지 파일 개수 및 용량 검사
                valid_exts = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}
                images = [f for f in dir_path.iterdir() if f.is_file() and f.suffix.lower() in valid_exts]

                if len(images) == 0:
                    ctx.add_fail(
                        tier="Tier 1",
                        name=f"이미지 파일 없음: {slug}",
                        message=f"'{img_rel}' 폴더 내에 유효한 이미지 에셋이 0개입니다.",
                        tip=f"해당 프로젝트의 실제 앱 스크린샷 이미지를 다운로드하십시오.",
                        file_path=img_rel,
                    )
                else:
                    # 빈(0 byte) 이미지 검사
                    small_images = [f for f in images if f.stat().st_size < 1000]
                    if small_images:
                        ctx.add_fail(
                            tier="Tier 1",
                            name=f"손상된 이미지 감지: {slug}",
                            message=f"{len(small_images)}개 이미지가 1,000 bytes 미만입니다: {[f.name for f in small_images]}",
                            tip="다운로드 실패로 인한 0-byte 더미 이미지인지 확인하십시오.",
                            file_path=img_rel,
                        )
                    else:
                        ctx.add_pass(
                            tier="Tier 1",
                            name=f"이미지 에셋 유효: {slug}",
                            message=f"{len(images)}개 정상 이미지 확인 ({img_rel})",
                            file_path=img_rel,
                        )


# ----------------------------------------------------------------------------
# 6. Tier 2: HTML 시맨틱 및 링크 무결성 검사기
# ----------------------------------------------------------------------------
class Tier2SemanticLinkChecker:
    TIER_NAME = "Tier 2: 시맨틱 구조 & 링크 무결성"

    def run(self, ctx: VerificationContext):
        print(f"\n{TerminalColors.BOLD}{TerminalColors.CYAN}▶ [{self.TIER_NAME}] 실행 중...{TerminalColors.RESET}")

        # A. index.html 링크 검사
        index_file = ctx.root_dir / "index.html"
        if not index_file.exists():
            ctx.add_fail("Tier 2", "메인 인덱스 부재", "index.html 파일이 없어 링크 검사를 건너뜁니다.")
            return

        try:
            with open(index_file, "r", encoding="utf-8") as f:
                index_content = f.read()
        except Exception as e:
            ctx.add_fail("Tier 2", "index.html 읽기 실패", str(e), file_path="index.html")
            return

        index_parser = IndexPageParser()
        index_parser.feed(index_content)

        notion_links = [l for l in index_parser.project_links if "notion.so" in l["href"]]
        if notion_links:
            ctx.add_fail(
                tier="Tier 2",
                name="외부 노션 링크 잔존",
                message=f"index.html 내 프로젝트 목록에 {len(notion_links)}개의 외부 Notion 링크가 남아있습니다.",
                tip="모든 프로젝트 링크를 './projects/<slug>.html' 로컬 케이스 스터디 링크로 교체하십시오.",
                file_path="index.html",
                line_no=notion_links[0]["line"],
            )
        else:
            ctx.add_pass(
                tier="Tier 2",
                name="노션 외부 링크 전멸",
                message="index.html의 프로젝트 목록에 잔존 노션 링크가 0건입니다.",
                file_path="index.html",
            )

        # 14개 프로젝트가 index.html에서 모두 연결되어 있는지 확인
        linked_hrefs = {l["href"].split("?")[0].split("#")[0] for l in index_parser.project_links}
        for proj in PROJECT_DEFINITIONS:
            slug = proj["slug"]
            expected_href_local = f"./projects/{slug}.html"
            expected_href_direct = f"projects/{slug}.html"

            is_linked = (expected_href_local in linked_hrefs) or (expected_href_direct in linked_hrefs)
            if not is_linked:
                ctx.add_fail(
                    tier="Tier 2",
                    name=f"메인 인덱스 미연결: {slug}",
                    message=f"'{slug}' 프로젝트의 로컬 링크 ('{expected_href_local}')가 index.html에 없습니다.",
                    tip=f"index.html의 프로젝트 목록에 <a href=\"{expected_href_local}\" class=\"project-link\">를 연결하십시오.",
                    file_path="index.html",
                )
            else:
                ctx.add_pass(
                    tier="Tier 2",
                    name=f"메인 인덱스 연결 확인: {slug}",
                    message=f"index.html -> '{expected_href_local}' 정상 연결",
                    file_path="index.html",
                )

        # B. 각 projects/*.html 상세 페이지 파싱 검사
        for proj in PROJECT_DEFINITIONS:
            slug = proj["slug"]
            html_rel = proj["html_path"]
            file_path = ctx.root_dir / html_rel

            if not file_path.exists():
                continue  # 파일 부재는 Tier 1에서 이미 처리됨

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                ctx.add_fail("Tier 2", f"HTML 읽기 실패: {slug}", str(e), file_path=html_rel)
                continue

            parser = CaseStudyPageParser()
            try:
                parser.feed(content)
            except Exception as e:
                ctx.add_fail("Tier 2", f"HTML 파싱 에러: {slug}", str(e), file_path=html_rel)
                continue

            # 1. 헤더 메타데이터 검사
            if not parser.has_title:
                ctx.add_fail("Tier 2", f"<title> 태그 누락: {slug}", "<title> 태그가 정의되지 않았습니다.", file_path=html_rel)
            if not parser.has_viewport:
                ctx.add_fail("Tier 2", f"viewport 메타 누락: {slug}", "<meta name=\"viewport\">가 없습니다.", file_path=html_rel)
            if not parser.has_description:
                ctx.add_warn("Tier 2", f"description 메타 권장: {slug}", "<meta name=\"description\">이 없습니다.", file_path=html_rel)
            if not parser.has_stylesheet:
                ctx.add_fail("Tier 2", f"style.css 링크 누락: {slug}", "<link rel=\"stylesheet\" href=\"../style.css\">가 없습니다.", file_path=html_rel)

            # 2. theme.js 로드 위치 (FOUC 방지 위해 head 내부 위치 필수)
            if not parser.has_theme_script:
                ctx.add_fail("Tier 2", f"theme.js 누락: {slug}", "<script src=\"../theme.js\"></script>가 로드되지 않았습니다.", file_path=html_rel)
            elif not parser.theme_script_in_head:
                ctx.add_fail(
                    tier="Tier 2",
                    name=f"theme.js 위치 오류 (FOUC 유발): {slug}",
                    message="theme.js가 <head> 태그 내부에 위치하지 않아 페이지 로딩 시 깜빡임(FOUC)이 발생합니다.",
                    tip="<head> 내부 상단으로 <script src=\"../theme.js\"></script>를 이동하십시오.",
                    file_path=html_rel,
                )
            else:
                ctx.add_pass("Tier 2", f"테마 스크립트 위치 정상: {slug}", "theme.js가 <head> 내부에 위치함", file_path=html_rel)

            # 3. 백링크 네비게이션 검사
            backlink_valid = any(
                b["href"] in {"../index.html#project", "../index.html", "./index.html", "index.html#project"}
                for b in parser.backlinks
            )
            if not backlink_valid:
                ctx.add_fail(
                    tier="Tier 2",
                    name=f"백링크 오류: {slug}",
                    message="상단/하단 '← Project' 백링크가 올바른 '../index.html#project'를 가리키지 않습니다.",
                    tip="<a href=\"../index.html#project\" class=\"back-link\">← Project</a> 형태로 백링크를 추가하십시오.",
                    file_path=html_rel,
                )
            else:
                ctx.add_pass("Tier 2", f"백링크 유효: {slug}", "index.html로 정상 연결", file_path=html_rel)

            # 4. 5대 표준 섹션 헤딩 순서 및 존재 검사
            found_sections = []
            h2_texts = [h["text"] for h in parser.h2_headings]

            for sec in EXPECTED_SECTIONS:
                pattern = re.compile(sec["pattern"], re.IGNORECASE)
                matched = any(pattern.search(t) for t in h2_texts)
                if not matched:
                    ctx.add_fail(
                        tier="Tier 2",
                        name=f"5대 섹션 헤딩 누락: {slug}",
                        message=f"필수 섹션 '{sec['title']}'이 없습니다.",
                        tip=f"h2 태그로 '{sec['title']}' 헤딩을 추가하십시오.",
                        file_path=html_rel,
                    )
                else:
                    found_sections.append(sec["num"])

            if len(found_sections) == 5:
                ctx.add_pass("Tier 2", f"5대 섹션 헤딩 완비: {slug}", "5대 표준 섹션 100% 매칭", file_path=html_rel)

            # 5. figure / figcaption 및 이미지 404 역추적 검사
            if parser.images_outside_figure:
                ctx.add_fail(
                    tier="Tier 2",
                    name=f"<figure> 미적용 이미지 발견: {slug}",
                    message=f"{len(parser.images_outside_figure)}개의 <img> 태그가 <figure> 외부에서 단독 사용되었습니다.",
                    tip="모든 스크린샷 <img>는 <figure><img ... /><figcaption ...></figure> 형태로 감싸야 합니다.",
                    file_path=html_rel,
                    line_no=parser.images_outside_figure[0]["line"],
                )

            # 이미지 태그별 검사 (404 Not Found 방지 핵심 로직)
            for img in parser.images:
                src = img["src"]
                alt = img["alt"]
                line = img["line"]

                if not alt.strip():
                    ctx.add_warn(
                        tier="Tier 2",
                        name=f"alt 속성 부재: {slug}",
                        message=f"이미지({src})에 접근성을 위한 alt 속성이 비어있습니다.",
                        tip="스크린 리더와 SEO를 위해 구체적인 alt 설명을 기재하십시오.",
                        file_path=html_rel,
                        line_no=line,
                    )

                # 외부 웹 URL(http://, https://)이 아닌 로컬 상대 경로 역추적
                if not src.startswith("http://") and not src.startswith("https://") and not src.startswith("data:"):
                    # projects/ 내부 파일이므로 상대 경로를 해석
                    # 예: src="../images/crm/01.png" -> projects/../images/crm/01.png -> images/crm/01.png
                    clean_src = unquote(src.split("?")[0].split("#")[0])
                    target_file = (ctx.root_dir / "projects" / clean_src).resolve()

                    if not target_file.exists():
                        ctx.add_fail(
                            tier="Tier 2",
                            name=f"이미지 404 역추적 오류: {slug}",
                            message=f"<img> src='{src}' 파일이 디스크에 실재하지 않습니다 (404 Not Found). 대상: {target_file}",
                            tip=f"상대 경로를 확인하십시오. 상세 페이지에서는 '../images/{slug}/...' 형태여야 합니다.",
                            file_path=html_rel,
                            line_no=line,
                        )
                    else:
                        ctx.add_pass(
                            tier="Tier 2",
                            name=f"이미지 역추적 성공: {slug}",
                            message=f"'{clean_src}' 실재 확인 ({target_file.name})",
                            file_path=html_rel,
                        )

            # 6. 메타 태그 칩 개수 검사
            if len(parser.tags) < 3:
                ctx.add_warn(
                    tier="Tier 2",
                    name=f"기술 태그 부족: {slug}",
                    message=f"기술 태그가 {len(parser.tags)}개입니다 (최소 3개 권장).",
                    tip="<div class=\"article-meta-tags\"> 내에 <span class=\"tag\"> 태그를 3개 이상 추가하십시오.",
                    file_path=html_rel,
                )
            else:
                ctx.add_pass("Tier 2", f"기술 태그 충분: {slug}", f"{len(parser.tags)}개 태그 등록됨", file_path=html_rel)

            # 7. 본문 길이 및 스켈레톤 더미 검사
            full_text = parser.get_full_text()
            if len(full_text.strip()) < 500:
                ctx.add_fail(
                    tier="Tier 2",
                    name=f"본문 텍스트 부족: {slug}",
                    message=f"문서 전체 텍스트가 {len(full_text)}자에 불과하여 실질적인 케이스 스터디 내용이 결여되었습니다.",
                    tip="실제 해결한 문제와 아키텍처에 관한 상세 내용을 작성하십시오.",
                    file_path=html_rel,
                )


# ----------------------------------------------------------------------------
# 7. Tier 3: 클라이언트 인터랙션 & 테마 무결성 검사기
# ----------------------------------------------------------------------------
class Tier3InteractionThemeChecker:
    TIER_NAME = "Tier 3: 클라이언트 인터랙션 & 테마 무결성"

    def run(self, ctx: VerificationContext):
        print(f"\n{TerminalColors.BOLD}{TerminalColors.CYAN}▶ [{self.TIER_NAME}] 실행 중...{TerminalColors.RESET}")

        # A. style.css 포커스 딤 및 테마 변수 검증
        style_file = ctx.root_dir / "style.css"
        if not style_file.exists():
            ctx.add_fail("Tier 3", "style.css 부재", "style.css 파일이 없어 스타일 검사를 건너뜁니다.")
            return

        try:
            with open(style_file, "r", encoding="utf-8") as f:
                style_css = f.read()
        except Exception as e:
            ctx.add_fail("Tier 3", "style.css 읽기 실패", str(e))
            return

        # 1. 포커스 딤(Focus Dim) CSS 룰 검증
        # .project-list:hover .project-link { opacity: 0.35; }
        has_dim_rule = bool(re.search(r"\.project-list:hover\s+[^\{]*\.project-link\s*\{[^}]*opacity\s*:\s*0\.[2-4]", style_css))
        if not has_dim_rule:
            ctx.add_fail(
                tier="Tier 3",
                name="포커스 딤(Focus Dim) 규칙 누락",
                message="'.project-list:hover .project-link { opacity: 0.35; }' 스타일 규칙이 없습니다.",
                tip="마우스 오버 시 미선택 항목을 흐리게 하는 CSS 규칙을 style.css에 추가하십시오.",
                file_path="style.css",
            )
        else:
            ctx.add_pass("Tier 3", "포커스 딤 규칙 확인", ".project-list:hover 시 opacity 0.35 감쇄 확인", file_path="style.css")

        # .project-list .project-link:hover { opacity: 1 !important; }
        has_restore_rule = bool(re.search(r"\.project-list\s+\.project-link:hover\s*\{[^}]*opacity\s*:\s*1", style_css))
        if not has_restore_rule:
            ctx.add_fail(
                tier="Tier 3",
                name="포커스 대상 복원 규칙 누락",
                message="'.project-list .project-link:hover { opacity: 1 !important; }' 규칙이 없습니다.",
                tip="호버된 링크를 선명하게 100% 복원하는 CSS 규칙을 style.css에 추가하십시오.",
                file_path="style.css",
            )
        else:
            ctx.add_pass("Tier 3", "포커스 대상 1.0 복원 확인", "호버 항목 opacity 1 확인", file_path="style.css")

        # .project-link { transition: ...; }
        has_transition = bool(re.search(r"\.project-link\s*\{[^}]*transition\s*:[^}]+opacity", style_css))
        if not has_transition:
            ctx.add_warn(
                tier="Tier 3",
                name="포커스 딤 부드러운 전환 효과(transition) 부재",
                message=".project-link에 transition: opacity 속성이 명시되지 않아 전환이 끊겨 보일 수 있습니다.",
                tip=".project-link에 'transition: opacity 0.15s cubic-bezier(0.16, 1, 0.3, 1);'를 추가하십시오.",
                file_path="style.css",
            )
        else:
            ctx.add_pass("Tier 3", "부드러운 전환 효과 확인", ".project-link opacity transition 확인", file_path="style.css")

        # 2열 그리드 레이아웃: grid-template-columns: minmax(0, 1fr) auto
        has_grid = "grid-template-columns" in style_css and "minmax" in style_css
        if not has_grid:
            ctx.add_warn(
                tier="Tier 3",
                name="Arlan.me 2열 그리드 구조 권장",
                message=".project-link에 'grid-template-columns: minmax(0, 1fr) auto;' 레이아웃이 확인되지 않습니다.",
                file_path="style.css",
            )
        else:
            ctx.add_pass("Tier 3", "2열 그리드 레이아웃 확인", "project-link 그리드 정의 일치", file_path="style.css")

        # 2. 필수 CSS 변수 검증 (Dark / Light)
        required_vars = ["--paper", "--ink", "--link", "--muted", "--rule", "--image-frame"]
        for var in required_vars:
            if var not in style_css:
                ctx.add_fail(
                    tier="Tier 3",
                    name=f"CSS 테마 변수 누락: {var}",
                    message=f"style.css에 필수 디자인 토큰 '{var}'가 정의되어 있지 않습니다.",
                    tip=f":root 및 html[data-theme=\"light\"] 양쪽에 '{var}' 색상값을 정의하십시오.",
                    file_path="style.css",
                )
            else:
                ctx.add_pass("Tier 3", f"CSS 변수 정의 확인: {var}", f"'{var}' 변수 존재", file_path="style.css")

        # B. theme.js 스크립트 무결성 검증
        theme_file = ctx.root_dir / "theme.js"
        if not theme_file.exists():
            ctx.add_fail("Tier 3", "theme.js 부재", "theme.js 파일이 없습니다.")
            return

        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_js = f.read()
        except Exception as e:
            ctx.add_fail("Tier 3", "theme.js 읽기 실패", str(e))
            return

        # IIFE 구조 검사
        has_iife = ("(() =>" in theme_js) or ("(function" in theme_js)
        if not has_iife:
            ctx.add_fail(
                tier="Tier 3",
                name="theme.js IIFE 패턴 부재",
                message="theme.js가 즉시 실행 함수(IIFE)로 감싸져 있지 않아 전역 스코프가 오염될 수 있습니다.",
                tip="theme.js를 '(() => { ... })();' 형태로 래핑하십시오.",
                file_path="theme.js",
            )
        else:
            ctx.add_pass("Tier 3", "theme.js IIFE 래핑 확인", "전역 스코프 보호 구조 확인", file_path="theme.js")

        # data-theme 조작 로직
        if "data-theme" not in theme_js and "dataset.theme" not in theme_js:
            ctx.add_fail(
                tier="Tier 3",
                name="테마 변경 데이터 속성 부재",
                message="theme.js에서 document.documentElement.dataset.theme 제어 로직을 찾을 수 없습니다.",
                file_path="theme.js",
            )
        else:
            ctx.add_pass("Tier 3", "HTML data-theme 조작 확인", "dataset.theme 제어 로직 일치", file_path="theme.js")

        # localStorage 에러 핸들링
        if "try" not in theme_js or "localStorage" not in theme_js:
            ctx.add_warn(
                tier="Tier 3",
                name="localStorage 예외 방어 권장",
                message="시크릿 모드 등에서 localStorage 접근 시 발생할 수 있는 SecurityError를 방어하기 위한 try-catch 블록이 권장됩니다.",
                file_path="theme.js",
            )
        else:
            ctx.add_pass("Tier 3", "localStorage 방어 코드 확인", "try-catch 보호 확인", file_path="theme.js")


# ----------------------------------------------------------------------------
# 8. Tier 4: 실서버 환경 E2E 크롤링 검사기
# ----------------------------------------------------------------------------
class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    """서버 로그 및 클라이언트 연결 종료 예외가 터미널 출력을 어지럽히지 않도록 처리하는 핸들러"""
    def log_message(self, format, *args):
        pass

    def copyfile(self, source, outputfile):
        try:
            super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):
            pass


class Tier4LiveServerHttpChecker:
    TIER_NAME = "Tier 4: 실서버 환경 E2E 크롤링"

    def _find_available_port(self, preferred_port: int) -> int:
        port = preferred_port
        for _ in range(50):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    port += 1
        raise RuntimeError(f"사용 가능한 포트를 찾을 수 없습니다 (시도: {preferred_port}~{port})")

    def run(self, ctx: VerificationContext, port: int = 3000):
        print(f"\n{TerminalColors.BOLD}{TerminalColors.CYAN}▶ [{self.TIER_NAME}] 실행 중...{TerminalColors.RESET}")

        actual_port = self._find_available_port(port)
        if actual_port != port:
            print(f"  {TerminalColors.YELLOW}포트 {port}가 점유되어 있어 포트 {actual_port}에서 서버를 시작합니다.{TerminalColors.RESET}")

        # 백그라운드 웹서버 기동
        root_dir_str = str(ctx.root_dir)

        class CustomHandler(QuietHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=root_dir_str, **kwargs)

        httpd = None
        server_thread = None
        try:
            httpd = ThreadingHTTPServer(("127.0.0.1", actual_port), CustomHandler)
            server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
            server_thread.start()
            time.sleep(0.3)  # 서버 안착 대기

            base_url = f"http://127.0.0.1:{actual_port}"
            ctx.add_pass("Tier 4", "로컬 HTTP 서버 기동", f"서버 실행 성공 ({base_url})")

            # 1. index.html 요청
            index_url = f"{base_url}/index.html"
            try:
                req = Request(index_url, headers={"User-Agent": "Portfolio-E2E-Verifier"})
                with urlopen(req, timeout=5) as resp:
                    code = resp.getcode()
                    content_type = resp.headers.get("Content-Type", "")
                    _ = resp.read()
                    if code == 200:
                        ctx.add_pass("Tier 4", "메인 인덱스 HTTP 200", f"GET /index.html -> 200 OK ({content_type})")
                    else:
                        ctx.add_fail("Tier 4", "메인 인덱스 HTTP 에러", f"응답 코드: {code}")
            except Exception as e:
                ctx.add_fail("Tier 4", "메인 인덱스 접속 실패", str(e), tip="로컬 서버 응답 확인 필요")

            # 2. 존재하는 14개 프로젝트 페이지 전수 크롤링
            for proj in PROJECT_DEFINITIONS:
                slug = proj["slug"]
                html_rel = proj["html_path"]
                full_path = ctx.root_dir / html_rel

                if not full_path.exists():
                    continue

                proj_url = f"{base_url}/{html_rel}"
                try:
                    req = Request(proj_url, headers={"User-Agent": "Portfolio-E2E-Verifier"})
                    with urlopen(req, timeout=5) as resp:
                        code = resp.getcode()
                        _ = resp.read()
                        if code == 200:
                            ctx.add_pass("Tier 4", f"케이스 스터디 HTTP 200: {slug}", f"GET /{html_rel} -> 200 OK")
                        else:
                            ctx.add_fail("Tier 4", f"케이스 스터디 HTTP 비정상: {slug}", f"응답 코드: {code}")
                except Exception as e:
                    ctx.add_fail("Tier 4", f"케이스 스터디 요청 실패: {slug}", str(e), file_path=html_rel)

            # 3. 상세 페이지에 임베드된 리소스(이미지, CSS, JS) HTTP GET 200 OK 검증
            for proj in PROJECT_DEFINITIONS:
                slug = proj["slug"]
                html_rel = proj["html_path"]
                full_path = ctx.root_dir / html_rel
                if not full_path.exists():
                    continue

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        html_text = f.read()
                    parser = CaseStudyPageParser()
                    parser.feed(html_text)

                    # 각 이미지에 대한 실제 HTTP GET 검증
                    for img in parser.images:
                        src = img["src"]
                        if src.startswith("http://") or src.startswith("https://") or src.startswith("data:"):
                            continue
                        clean_src = unquote(src.split("?")[0].split("#")[0])
                        # projects/ 하위이므로 urljoin
                        img_http_url = urljoin(f"{base_url}/projects/", clean_src)
                        try:
                            with urlopen(Request(img_http_url, headers={"User-Agent": "Portfolio-E2E-Verifier"}), timeout=5) as img_resp:
                                _ = img_resp.read()
                                if img_resp.getcode() == 200:
                                    ctx.add_pass(
                                        "Tier 4",
                                        f"에셋 HTTP 200: {slug}",
                                        f"GET {clean_src} -> 200 OK",
                                        file_path=html_rel,
                                    )
                                else:
                                    ctx.add_fail(
                                        "Tier 4",
                                        f"에셋 HTTP 에러: {slug}",
                                        f"GET {clean_src} -> HTTP {img_resp.getcode()}",
                                        file_path=html_rel,
                                    )
                        except HTTPError as he:
                            ctx.add_fail(
                                "Tier 4",
                                f"에셋 HTTP 404/오류: {slug}",
                                f"GET {clean_src} -> HTTP {he.code} Not Found",
                                tip="실제 파일이 올바른 위치에 있는지, HTML 상대경로가 맞는지 확인하십시오.",
                                file_path=html_rel,
                                line_no=img["line"],
                            )
                        except Exception as ex:
                            ctx.add_fail("Tier 4", f"에셋 요청 실패: {slug}", str(ex), file_path=html_rel)

                except Exception as e:
                    ctx.add_fail("Tier 4", f"리소스 파싱 중 예외: {slug}", str(e))

            # 4. 음성 테스트 (Negative Test): 존재하지 않는 URL 404 확인
            dummy_404_url = f"{base_url}/projects/non-existent-sample-page-for-test-404.html"
            try:
                with urlopen(Request(dummy_404_url), timeout=5) as resp:
                    _ = resp.read()
                ctx.add_fail(
                    "Tier 4",
                    "가상 404 음성 테스트 실패",
                    "존재하지 않는 페이지가 200 OK를 반환했습니다 (서버 라우팅 오작동 의심).",
                )
            except HTTPError as e:
                if e.code == 404:
                    ctx.add_pass("Tier 4", "가상 404 음성 테스트 성공", "존재하지 않는 URL에 대해 정확히 HTTP 404 반환 확인")
                else:
                    ctx.add_fail("Tier 4", "가상 404 음성 테스트 비정상", f"기대 404 대신 {e.code} 반환됨")
            except Exception as e:
                ctx.add_fail("Tier 4", "가상 404 테스트 실패", str(e))

        finally:
            # 서버 종료 처리
            if httpd:
                httpd.shutdown()
                httpd.server_close()
            if server_thread and server_thread.is_alive():
                server_thread.join(timeout=1.0)


# ----------------------------------------------------------------------------
# 9. 결과 리포터 및 CLI 메인 함수
# ----------------------------------------------------------------------------
class PortfolioVerifier:
    """4-Tier E2E 종합 테스트 러너 및 결과 리포터"""
    def __init__(self, root_dir: Path, strict: bool = False, port: int = 3000):
        self.ctx = VerificationContext(root_dir, strict)
        self.port = port
        self.t1 = Tier1FilePresenceChecker()
        self.t2 = Tier2SemanticLinkChecker()
        self.t3 = Tier3InteractionThemeChecker()
        self.t4 = Tier4LiveServerHttpChecker()

    def run_tiers(self, tiers: List[int]) -> int:
        start_time = time.time()
        print(f"\n{TerminalColors.BOLD}{'=' * 75}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}🔍 Noah Park 포트폴리오 4-Tier E2E 무결성 검증 시작{TerminalColors.RESET}")
        print(f"   - 대상 디렉토리: {self.ctx.root_dir}")
        print(f"   - 엄격 모드 (Strict): {'켜짐 (Warning도 실패 처리)' if self.ctx.strict else '꺼짐'}")
        print(f"   - 실행 티어: {tiers}")
        print(f"{TerminalColors.BOLD}{'=' * 75}{TerminalColors.RESET}")

        if 1 in tiers:
            self.t1.run(self.ctx)
        if 2 in tiers:
            self.t2.run(self.ctx)
        if 3 in tiers:
            self.t3.run(self.ctx)
        if 4 in tiers:
            self.t4.run(self.ctx, port=self.port)

        elapsed = time.time() - start_time
        self.print_summary(elapsed)
        return 0 if self.ctx.is_successful else 1

    def print_summary(self, elapsed: float):
        print(f"\n{TerminalColors.BOLD}{'=' * 75}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}📊 검증 결과 세부 내역 및 실패/경고 리포트{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'=' * 75}{TerminalColors.RESET}")

        # 실패 및 경고 항목 상세 출력
        issues = [i for i in self.ctx.items if i.status in {"FAIL", "WARN"}]
        if not issues:
            print(f"\n  {TerminalColors.GREEN}✨ 모든 검사항목이 성공적으로 통과되었습니다!{TerminalColors.RESET}")
        else:
            for item in issues:
                badge = TerminalColors.fail_badge() if item.status == "FAIL" else TerminalColors.warn_badge()
                loc = f" [{item.file_path}" + (f":{item.line_no}]" if item.line_no else "]") if item.file_path else ""
                print(f"\n{badge} {TerminalColors.BOLD}{item.name}{TerminalColors.RESET}{TerminalColors.GRAY}{loc}{TerminalColors.RESET}")
                print(f"       {item.message}")
                if item.tip:
                    print(f"       {TerminalColors.CYAN}💡 [Tip] {item.tip}{TerminalColors.RESET}")

        # 통계 요약 표
        print(f"\n{TerminalColors.BOLD}{'-' * 75}{TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}종합 통계 요약 (소요 시간: {elapsed:.2f}초){TerminalColors.RESET}")
        print(f"{TerminalColors.BOLD}{'-' * 75}{TerminalColors.RESET}")

        tier_names = ["Tier 1", "Tier 2", "Tier 3", "Tier 4"]
        for t in tier_names:
            t_items = [i for i in self.ctx.items if i.tier.startswith(t)]
            p = sum(1 for i in t_items if i.status == "PASS")
            f = sum(1 for i in t_items if i.status == "FAIL")
            w = sum(1 for i in t_items if i.status == "WARN")
            if t_items:
                status_str = f"{TerminalColors.GREEN}P: {p}{TerminalColors.RESET} | {TerminalColors.RED}F: {f}{TerminalColors.RESET} | {TerminalColors.YELLOW}W: {w}{TerminalColors.RESET}"
                print(f"  • {t:<8}: {status_str}  (총 {len(t_items)}개 검사)")

        print(f"{TerminalColors.BOLD}{'-' * 75}{TerminalColors.RESET}")
        final_color = TerminalColors.GREEN if self.ctx.is_successful else TerminalColors.RED
        final_status = "PASSED (합격)" if self.ctx.is_successful else "FAILED (불합격)"
        print(f"  {TerminalColors.BOLD}최종 판정: {final_color}{final_status}{TerminalColors.RESET}")
        print(f"  합격: {self.ctx.pass_count}개 | 실패: {self.ctx.fail_count}개 | 경고: {self.ctx.warn_count}개")
        print(f"{TerminalColors.BOLD}{'=' * 75}{TerminalColors.RESET}\n")

    def export_json(self, json_path: str, elapsed: float):
        data = {
            "root_dir": str(self.ctx.root_dir),
            "strict": self.ctx.strict,
            "elapsed_seconds": round(elapsed, 3),
            "is_successful": self.ctx.is_successful,
            "summary": {
                "total": len(self.ctx.items),
                "pass": self.ctx.pass_count,
                "fail": self.ctx.fail_count,
                "warn": self.ctx.warn_count,
            },
            "results": [item.to_dict() for item in self.ctx.items],
        }
        target = Path(json_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"{TerminalColors.info_badge()} JSON 결과가 저장되었습니다: {target.resolve()}")


def main():
    parser = argparse.ArgumentParser(
        description="Noah Park 포트폴리오 웹사이트 E2E 4-Tier 종합 무결성 검증 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
[사용 예시]
  # 1. 전체 4-Tier 종합 검증 실행
  python3 scripts/verify_portfolio.py --all

  # 2. 특정 티어만 단독 실행
  python3 scripts/verify_portfolio.py --tier 1
  python3 scripts/verify_portfolio.py --tier 2
  python3 scripts/verify_portfolio.py --tier 3
  python3 scripts/verify_portfolio.py --tier 4

  # 3. 엄격 모드 (경고 사항도 실패로 엄격히 처리)
  python3 scripts/verify_portfolio.py --all --strict

  # 4. 검증 결과 JSON 파일 내보내기 (CI/CD 파이프라인 연동)
  python3 scripts/verify_portfolio.py --all --json results.json
        """,
    )

    parser.add_argument("--all", action="store_true", help="Tier 1~4 전체 종합 검증 실행")
    parser.add_argument(
        "--tier",
        type=int,
        nargs="+",
        choices=[1, 2, 3, 4],
        help="실행할 특정 Tier 선택 (1: 파일, 2: 시맨틱/링크, 3: 테마/인터랙션, 4: 실서버)",
    )
    parser.add_argument("--port", type=int, default=3000, help="Tier 4 테스트용 로컬 서버 포트 (기본값: 3000)")
    parser.add_argument("--strict", action="store_true", help="엄격 모드: 경고(Warning)도 실패로 처리하여 exit code 1 반환")
    parser.add_argument("--json", type=str, metavar="FILE", help="검증 결과를 JSON 파일로 저장")
    parser.add_argument("--root", type=str, help="프로젝트 루트 디렉토리 (기본값: 현재 스크립트 상위 디렉토리)")

    args = parser.parse_args()

    # 루트 디렉토리 산출
    if args.root:
        root_dir = Path(args.root)
    else:
        # scripts/ 상위 디렉토리를 기본 프로젝트 루트로 설정
        root_dir = Path(__file__).resolve().parent.parent

    # 실행할 티어 결정
    tiers = []
    if args.all or (not args.tier):
        tiers = [1, 2, 3, 4]
    else:
        tiers = sorted(list(set(args.tier)))

    start_time = time.time()
    verifier = PortfolioVerifier(root_dir=root_dir, strict=args.strict, port=args.port)
    exit_code = verifier.run_tiers(tiers)
    elapsed = time.time() - start_time

    if args.json:
        verifier.export_json(args.json, elapsed)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
