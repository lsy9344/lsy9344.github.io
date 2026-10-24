## 2026-10-21T19:06:40Z
당신은 E2E 검증 테스트 스위트를 개발하는 Test Writer입니다.
- 작업 디렉토리: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/worker_m_test/
- 원본 사용자 요청 파일: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/ORIGINAL_REQUEST.md
- 프로젝트 명세: /Users/sooyeol/Desktop/Code/ws_noah/PROJECT.md
- 테스트 인프라 명세: /Users/sooyeol/Desktop/Code/ws_noah/TEST_INFRA.md
- 분석 리포트: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_test/report.md
- 단독 파일 소유권: scripts/verify_portfolio.py 및 scripts/ 디렉토리 (다른 HTML/CSS 소스는 수정하지 마십시오)

반드시 ORIGINAL_REQUEST.md를 먼저 읽으십시오.
TEST_INFRA.md 및 report.md의 4-tier 검증 아키텍처에 따라 표준 라이브러리(Zero-Dependency) 기반 Python 검증 스크립트 `scripts/verify_portfolio.py`를 구현하십시오:
- Tier 1: 정적 파일 실재성 및 0-byte 방지 (14개 HTML, 이미지 서브디렉토리)
- Tier 2: HTML 시맨틱 및 링크 무결성 (img src 404 역추적 검증, <figure>/<figcaption>, 5대 섹션, index.html 로컬 링크 확인)
- Tier 3: 클라이언트 인터랙션 & 테마 무결성 (CSS Focus-Dim 선택자, theme.js IIFE, CSS 변수 일치)
- Tier 4: 실서버 환경 E2E 크롤링 (백그라운드 로컬 웹서버 기동 또는 지정 포트 대상 전체 리소스 HTTP 200 OK 검증)
- CLI 옵션: `--all`, `--tier 1..4`, `--port <PORT>`, `--strict`, `--json`
구현 후 `python3 scripts/verify_portfolio.py --help` 및 실행 테스트를 직접 수행하고 결과를 확인하십시오.
작업 완료 후 handoff.md를 작성하고 send_message로 완료 보고를 하십시오.
