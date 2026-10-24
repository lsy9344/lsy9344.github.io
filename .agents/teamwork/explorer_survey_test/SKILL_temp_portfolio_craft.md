# 🌿 temp_portfolio-craft: 미니멀 장인정신 포트폴리오 구축 가이드

이 문서는 `.agents/skills/temp_portfolio-craft/SKILL.md`의 로컬 복사본입니다.

## 1. 디자인 철학의 융합 (Core Philosophy)
- Karri Saarinen: 480px 단일 컬럼, 아날로그 Paper/Ink 톤, 브라유 점자(`⡢`) 불릿, 타이포그래피 중심
- Arlan Marat: 2열 그리드 + 연도 메타데이터, 포커스 딤(Focus Dim) 순수 CSS 인터랙션, direct-link 직행성

## 2. 케이스 스터디 상세 페이지 (`projects/*.html`) 요구 규칙
- 상단 `← Project` 백링크 (`href="../index.html#project"`)
- `article-header`: 제목 `<h1>`, 날짜 및 역할 `.date`, 기술 태그 칩 `.article-meta-tags > .tag`
- 핵심 인용구 `<blockquote>`
- 5개 표준 아티클 섹션 구조:
  1. `<h2>1. 하는 일 (Overview)</h2>`
  2. `<h2>2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)</h2>`
  3. `<h2>3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)</h2>`
  4. `<h2>4. 핵심 구현 기능 (Key Features)</h2>`
  5. `<h2>5. 엔지니어링 교훈 (Key Takeaways)</h2>`
- 실제 앱 이미지 프레임:
  - `<figure>` 및 `<figcaption class="caption">`
  - 이미지 태그: `<img src="../images/<slug>/<filename>" alt="..." />`
  - `style.css`에서 `border: 1px solid var(--rule); border-radius: 6px;` 액자화
- 브라유 점자 불릿 리스트 (`<ul><li>...</li></ul>` with CSS `::before { content: '⡢'; }`)
- 하단 백링크 (`<a href="../index.html#project" class="back-link">← Back to Project</a>`)
- 다크/라이트 모드 지원 (`../style.css`, `../theme.js`)
