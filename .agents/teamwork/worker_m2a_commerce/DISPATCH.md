## 2026-10-21T19:14:17Z
당신은 Commerce & SaaS 도메인의 3개 케이스 스터디 상세 HTML 페이지를 제작하는 UI Builder Worker (M2-A)입니다.
- 작업 디렉토리: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/worker_m2a_commerce/
- 원본 사용자 요청 파일: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/ORIGINAL_REQUEST.md
- 프로젝트 명세: /Users/sooyeol/Desktop/Code/ws_noah/PROJECT.md
- 디자인 가이드: /Users/sooyeol/Desktop/Code/ws_noah/DESIGN.md
- 골든 마스터 레퍼런스: /Users/sooyeol/Desktop/Code/ws_noah/projects/beauty-brand-crm.html
- UI 표준 템플릿 명세: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_ui/report.md
- 노션 분석 데이터 및 원시 JSON: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_notion/report.md, /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_notion/notion_survey_raw.json

[단독 파일 소유권]
당신이 생성 및 수정할 파일은 오직 다음 3개뿐입니다:
1. `projects/beauty-review-platform.html` (이미지: `../images/beauty-review-platform/` 5장)
2. `projects/beauty-band-automation.html` (이미지: `../images/beauty-band-automation/` 6장)
3. `projects/beauty-erp-inventory.html` (이미지: `../images/beauty-erp-inventory/` 5장)
다른 파일(index.html, style.css, images 등)은 절대 수정하지 마십시오.

[필수 구현 지침]
1. `projects/beauty-brand-crm.html`의 시맨틱 구조를 100% 따를 것:
   - `<head>`: `../style.css`, `../theme.js` 상대 경로
   - 상단/하단 백링크: `<a href="../index.html#project" class="back-link">← Project</a>`
   - 헤더: `<h1>` 제목, `<span class="date">` 날짜, `<div class="article-meta-tags">` 모노스페이스 태그 칩
   - 인용구: `<blockquote>`
   - 5대 표준 섹션 `<h2>`:
     `1. 하는 일 (Overview)`
     `2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)`
     `3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)`
     `4. 핵심 구현 기능 (Key Features)`
     `5. 엔지니어링 교훈 (Key Takeaways)`
2. 모든 스크린샷 이미지는 반드시 `<figure><img src="../images/<slug>/<filename>" alt="..." /><figcaption class="caption">...</figcaption></figure>` 형식으로 감쌀 것.
3. 주의: HTML 텍스트 내에 점자 기호(`⡢`)나 불릿(`•`)을 직접 타이핑하지 마십시오. CSS의 `.article ul li::before` 가상 요소가 자동으로 점자를 렌더링하므로 순수 `<ul><li>`만 작성하십시오.
4. 노션 원시 텍스트의 깊이 있는 엔지니어링 내용(원장 분리, 스냅샷, 멱등성 등)을 충실히 반영하십시오.
