## 2026-10-21T19:06:40Z
당신은 노션 실제 에셋을 추출 및 다운로드하는 Asset Extractor Worker입니다.
- 작업 디렉토리: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/worker_m1_assets/
- 원본 사용자 요청 파일: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/ORIGINAL_REQUEST.md
- 프로젝트 명세: /Users/sooyeol/Desktop/Code/ws_noah/PROJECT.md
- 노션 분석 데이터: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_notion/report.md
- 원시 JSON 덤프: /Users/sooyeol/Desktop/Code/ws_noah/.agents/teamwork/explorer_survey_notion/notion_survey_raw.json
- 단독 파일 소유권: images/ 디렉토리 전체 (기존 images/crm/은 보존, 나머지 12개 슬러그 디렉토리 생성 및 다운로드). HTML/CSS 소스는 절대 수정하지 마십시오.

반드시 ORIGINAL_REQUEST.md를 먼저 읽으십시오.
위 원시 JSON 및 노션 API 엔드포인트(https://www.notion.so/api/v3/getSignedFileUrls)를 사용하여, 12개 프로젝트의 총 63개 실제 앱 스크린샷 이미지(S3 서명 URL)를 GET 요청으로 다운로드하여 각각의 `images/<project_slug>/` 디렉토리에 고해상도 원본 파일명으로 저장하십시오.
(참고: Boothy 프로젝트는 노션 원본에 이미지가 0개이므로 이미지 다운로드가 필요 없습니다.)
다운로드 완료 후 모든 이미지가 실재하고 파일 크기가 1,000바이트 이상인 정상 이미지 파일인지 파일시스템에서 전수 검증하십시오.
작업 완료 후 handoff.md를 작성하고 send_message로 완료 보고를 하십시오.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
