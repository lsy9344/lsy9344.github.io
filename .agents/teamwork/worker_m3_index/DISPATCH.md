## 2026-10-21T19:32:19Z
당신은 메인 페이지(index.html)와 14개 프로젝트의 네비게이션 및 포커스 딤(Focus Dim) 효과를 통합하는 Index Integration Worker (M3)입니다.
- 작업 디렉토리: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/worker_m3_index/
- 원본 사용자 요청 파일: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/ORIGINAL_REQUEST.md
- 프로젝트 명세: /Users/sooyeol/Desktop/Code/ws_noah/PROJECT.md
- 디자인 가이드: /Users/sooyeol/Desktop/Code/ws_noah/DESIGN.md
- 단독 파일 소유권: index.html (다른 파일은 수정하지 마십시오)

[필수 구현 지침]
1. `index.html` 내의 `<section class="home-projects" id="project">` 섹션을 열람하십시오.
2. 기존에 외부 노션 링크(`https://notion.so/...`)로 설정되어 있던 13개 프로젝트의 `href` 속성을 로컬 상대 경로 `./projects/<project_slug>.html`로 교체하십시오:
   - 01: `./projects/beauty-brand-crm.html` (기존 유지)
   - 02: `./projects/beauty-review-platform.html`
   - 03: `./projects/beauty-band-automation.html`
   - 04: `./projects/beauty-erp-inventory.html`
   - 05: `./projects/boothy-photo-booth.html`
   - 06: `./projects/multi-branch-studio-erp.html`
   - 07: `./projects/sms-automation-review.html`
   - 08: `./projects/cuteditor-photo-tool.html`
   - 09: `./projects/vietnam-aesthetic-erp.html`
   - 10: `./projects/seafood-distribution-erp.html`
   - 11: `./projects/military-meal-management.html`
   - 12: `./projects/multimarket-crawler.html`
   - 13: `./projects/kakaotalk-unread-excel.html`
   - 14: `./projects/tactrun-delivery-landing.html`
3. 로컬 페이지로 이동하므로 `target="_blank"` 및 `rel="noopener noreferrer"` 속성은 제거하여 동일 창 내 자연스러운 네비게이션이 되도록 하십시오 (첫 번째 crm 링크와 일치).
4. `index.html`의 2열 그리드와 포커스 딤(Focus Dim) CSS 인터랙션이 14개 항목 전체에서 매끄럽게 유지되는지 확인하십시오.
5. 변경 후 반드시 `python3 scripts/verify_portfolio.py --all`을 직접 실행하여 Tier 1 ~ Tier 4 전체 검사가 100% PASS 되는지 확인하십시오!
6. 작업 완료 후 handoff.md를 작성하고 send_message로 완료 보고를 하십시오.
