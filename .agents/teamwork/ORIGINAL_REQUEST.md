# Original User Request

## 2026-10-21T18:51:56Z

Use a very large team of agents. 노션 포트폴리오(Page ID: `3f90c30e2dc0811c879cc02e554b63e4`)에 수록된 14개 실전 프로젝트 전체에 대해 `temp_portfolio-craft` 스킬 명세에 맞춰 실제 앱 스크린샷 에셋을 추출 및 다운로드하고, Karri Saarinen × Arlan Marat 융합 스타일의 정갈한 전용 케이스 스터디 상세 페이지(`projects/*.html`)를 병렬로 제작하여 메인 페이지(`index.html`)와 완벽하게 연결합니다.

Working directory: /Users/sooyeol/Desktop/Code/ws_noah
Integrity mode: development

## Requirements

### R1. 14개 프로젝트 전체에 대한 노션 데이터 및 실제 앱 스크린샷 에셋 추출
- 노션 서브페이지 14개 전체에서 텍스트(하는 일, 해결한 문제, 시스템 구성, 처리 흐름, 구현 기능)와 실제 앱 첨부 이미지(`attachment:...`)의 서명된 URL을 Notion API(`getSignedFileUrls`)로 조회하여 로컬 `images/<project_slug>/` 디렉토리에 고해상도로 다운로드 저장합니다.

### R2. `temp_portfolio-craft` 스킬 기반 개별 케이스 스터디 페이지 제작
- 각 프로젝트별로 `projects/<project_slug>.html` 페이지를 생성합니다 (총 14개 페이지).
- Karri Saarinen의 480px 단일 컬럼 가독성, `<figure>` 및 `<figcaption>` 시맨틱 이미지 프레임, 인용구(`<blockquote>`), 브라유 점자(`⡢`) 불릿을 적용합니다.
- Arlan Marat 스타일의 기술 태그 칩과 정돈된 날짜/역할 메타데이터를 배치합니다.
- 다크/라이트 모드 테마 전환(`theme.js`) 및 모바일 반응형 스타일(`style.css`)이 완벽히 작동해야 합니다.

### R3. 메인 페이지(`index.html`) 및 네비게이션 연결 갱신
- 메인 페이지의 `Project` 섹션에서 14개 항목 모두가 각각 생성된 로컬 상세 페이지(`projects/<project_slug>.html`)로 자연스럽게 연결되도록 링크를 업데이트합니다.
- `arlan.me`의 2열 그리드와 시그니처 포커스 딤(Focus Dim) 효과가 14개 항목 전체에서 매끄럽게 유지되도록 보장합니다.

## Verification Resources

- 자동 검증 스크립트 실행: Python 스크립트로 `projects/` 폴더 내 14개 HTML 파일의 존재 여부, 내부 이미지 태그의 로컬 파일 실재 여부(404 에러 방지), HTTP 로컬 서버(`http://localhost:3000`)의 정상 응답(200 OK)을 자동 확인합니다.

## Acceptance Criteria

### Content Completeness
- [ ] 14개 프로젝트 모두 독립된 `projects/*.html` 상세 페이지가 존재할 것
- [ ] 노션 원본에 포함된 실제 앱 스크린샷 이미지들이 각 프로젝트 페이지에 누락 없이 `<figure>` 형태로 렌더링될 것
- [ ] 깨진 이미지 링크(404)나 빈 텍스트 영역이 없을 것

### Design & Interaction Integrity
- [ ] `temp_portfolio-craft` 및 `DESIGN.md` 명세를 100% 준수할 것 (480px 컨테이너, Paper/Ink 톤, 점자 불릿)
- [ ] 모든 페이지에서 다크/라이트 테마 토글이 깜빡임 없이 즉각 반응할 것
- [ ] 메인 화면의 포커스 딤(Focus Dim) 효과가 깨짐 없이 작동할 것
