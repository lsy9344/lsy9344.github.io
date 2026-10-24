# 📋 E2E 검증 및 테스트 아키텍처 설계 명세서 (report.md)

- **작성일**: 2026-10-22
- **작성자**: E2E Verification Architect & Spec Miner (`explorer_survey_test`)
- **대상 프로젝트**: Noah 미니멀 포트폴리오 웹사이트 (14개 실전 프로젝트 케이스 스터디)
- **참조 명세**: `ORIGINAL_REQUEST.md`, `DESIGN.md`, `temp_portfolio-craft` 스킬

---

## 1. 개요 및 목적 (Executive Summary)

본 보고서는 노션 포트폴리오(Page ID: `3f90c30e2dc0811c879cc02e554b63e4`)에 수록된 **14개 실전 프로젝트 전체**가 로컬 케이스 스터디 페이지(`projects/*.html`)로 제작되고 메인 페이지(`index.html`)와 완벽하게 연결될 때, 단 하나의 링크 깨짐(404)이나 레이아웃 왜곡, 테마 오작동 없이 무결성을 보장하기 위한 **E2E(End-to-End) 테스트 아키텍처 및 종합 자동 검증 체계**를 수립합니다.

초보 개발자도 테스트의 필요성과 검증 원리를 쉽게 이해하고 운영할 수 있도록, 순수 Python 기반의 **4-Tier 계층형 테스트 방법론**과 자동 검증 스크립트(`scripts/verify_portfolio.py`)의 구현 명세를 정의합니다.

---

## 2. Features Discovered (발견된 검증 기능 명세)

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|---|---|---|---|---|---|---|
| 1 | File Integrity | 14개 프로젝트 파일 실재성 검사 | `projects/` 폴더 내 14개의 `.html` 파일이 물리적으로 존재하는지 확인 | `projects/*.html` 경로 목록 | Boolean (14개 일치 여부) | 누락된 파일명 목록 및 [FAIL] 리포트 | `ORIGINAL_REQUEST.md` R1, R2 |
| 2 | File Integrity | 에셋 이미지 파일 실재성 검사 | `images/<project_slug>/` 내 실제 앱 스크린샷 파일들이 존재하는지 확인 | `images/*/*` 파일 경로 | 이미지 개수 및 유효 파일 목록 | 이미지 폴더 누락 또는 0개일 시 [FAIL] | `ORIGINAL_REQUEST.md` R1 |
| 3 | File Integrity | 무효/빈 파일 방지 (0 Byte Guard) | HTML 및 이미지 파일의 크기가 0 바이트이거나 비정상적으로 작은지 검사 | 파일 stat (st_size) | 파일 크기(bytes) | 파일 크기 < 기준치일 시 [FAIL] | 현장 엔지니어링 표준 |
| 4 | Link Boundary | 메인 화면 링크 로컬 직행성 검사 | `index.html` 내 14개 프로젝트 링크가 외부 Notion 링크가 아닌 로컬 `projects/*.html`로 매핑되었는지 검사 | `index.html` DOM | 14개 로컬 링크 목록 | Notion URL 잔존 또는 잘못된 경로 시 [FAIL] | `ORIGINAL_REQUEST.md` R3 |
| 5 | Link Boundary | 케이스 스터디 이미지 404 방지 검사 | 각 HTML 내 모든 `<img src="...">` 상대 경로가 실제 존재하는 로컬 파일을 가리키는지 역추적 검사 | HTML 파일 및 상대 경로 | 대상 파일 절대 경로 매핑 결과 | 404 Not Found 대상 파일 보고 및 [FAIL] | `ORIGINAL_REQUEST.md` Verification |
| 6 | Link Boundary | 상/하단 백링크 네비게이션 검사 | 상세 페이지의 `← Project` 백링크가 `../index.html#project`를 가리키는지 확인 | HTML `<a>` 태그 href | 백링크 유효성 Boolean | 오타 또는 누락 시 [WARN] 또는 [FAIL] | `temp_portfolio-craft` Step 6 |
| 7 | Semantic HTML | Karri Saarinen 5대 섹션 헤딩 검사 | 상세 페이지가 5대 표준 섹션(`h2`)을 순서대로 보유하는지 검사 | HTML `<h2>` 텍스트 목록 | 5개 섹션 매칭 리스트 | 누락된 섹션 헤딩 보고 및 [FAIL] | `projects/beauty-brand-crm.html` |
| 8 | Semantic HTML | `<figure>` & `<figcaption>` 시맨틱 검사 | 모든 스크린샷 이미지가 `<figure>` 및 설명 `<figcaption>`으로 감싸여 있는지 검사 | HTML DOM 트리 | figure-figcaption 쌍 매칭 | 날것의 `<img>` 단독 존재 시 [FAIL] | `DESIGN.md` & `SKILL.md` |
| 9 | Semantic HTML | 기술 태그 칩 메타데이터 검사 | `.article-meta-tags > .tag` 요소가 프로젝트당 최소 3개 이상 존재하는지 검사 | HTML `.tag` 요소 목록 | 태그 수 및 텍스트 목록 | 태그 < 3개 시 [WARN] | `DESIGN.md` §1 |
| 10 | Interaction | Arlan Marat 순수 CSS 포커스 딤 검사 | `style.css` 내 hover 시 0.35 딤 처리 및 마우스 오버 항목 1.0 선명도 복원 CSS 규칙 존재 확인 | `style.css` 텍스트 | CSS 선택자 및 선언 일치 | 선택자 누락 또는 transition 부재 시 [FAIL] | `DESIGN.md` §2.1 |
| 11 | Interaction | 깜빡임 방지 테마 시스템 검사 | `theme.js`가 `<head>` 상단에서 IIFE로 실행되고 `data-theme` 속성을 제어하는지 검사 | HTML `<head>` 및 `theme.js` | 스크립트 로드 위치 및 버튼 | `<head>` 외부에 있거나 버튼 속성 불일치 시 [FAIL] | `DESIGN.md` §2.3 |
| 12 | Live Server | 로컬 웹서버 HTTP 200 OK 검사 | Python 내장 서버를 띄워 모든 페이지와 이미지에 HTTP GET 요청을 보내 200 응답 확인 | HTTP `GET http://localhost:3000/...` | HTTP 상태 코드, Content-Type | 404, 500 등 비정상 응답 시 [FAIL] | `ORIGINAL_REQUEST.md` Verification |
| 13 | Live Server | 비정상 URL 404 핸들링 검사 | 존재하지 않는 가상 경로 요청 시 웹서버가 정확히 404 Not Found를 반환하는지 확인 | HTTP `GET .../not-found.html` | HTTP 상태 코드 404 | 200 OK 등 오작동 반환 시 [FAIL] | HTTP 표준 검증 |

---

## 3. Edge Cases (경계값 및 예외 시나리오)

| # | Feature | Input (경계 조건) | Observed / Expected Behavior | 대응 방어 전략 |
|---|---|---|---|---|
| 1 | Image Relative Path | `../images/crm/01.png` vs `./images/crm/01.png` | `projects/` 폴더 내 상세 페이지에서는 반드시 한 단계 상위(`../`)로 올라가야 하므로, `./` 사용 시 404 발생 | 상대 경로 해석 시 부모 디렉토리 기준 절대 경로 변환 알고리즘 적용 |
| 2 | Special Characters in URL | URL 인코딩된 파일명 (공백 `%20`, 한글 등) | 파일시스템에서는 디코딩된 파일명이 필요하며, URL 요청 시에는 인코딩 필요 | `urllib.parse.unquote`를 통해 파일 경로 역참조 검증 |
| 3 | Empty / Stub Content | HTML 파일은 생성되었으나 내용이 비어있거나 "TODO"만 있는 경우 | 파일 크기는 0이 아니지만 실질적 콘텐츠 부재로 사용자 경험 훼손 | 최소 파일 크기 2,000 바이트 + 본문 `<p>` 태그 텍스트 길이 합산(최소 500자) 검증 |
| 4 | Broken Image Asset | 이미지 파일 헤더가 손상되었거나 0 바이트인 더미 이미지 | 브라우저에서 깨진 이미지 엑스박스 아이콘 표시 | 이미지 파일 크기 최소 1,000 바이트 이상 검증 및 확장자 화이트리스트 검사 |
| 5 | Web Server Port Conflict | 지정한 포트(예: 3000)를 다른 프로세스가 이미 사용 중인 경우 | `OSError: [Errno 48] Address already in use` 예외 발생 | 동적 포트 탐색(3000 -> 3001 -> 3002 ...) 또는 `SO_REUSEADDR` 소켓 옵션 적용 |
| 6 | Theme Persistence | `localStorage`가 비활성화된 시크릿 창 또는 브라우저 보안 환경 | 스크립트 실행 중 `localStorage` 접근 시 `SecurityError` 발생 | `theme.js` 내 `try-catch` 블록 보호 및 폴백 동작 검증 |
| 7 | Focus Dim Mobile Touch | 터치 스크린 디바이스에서 hover 시 전체 항목이 흐려진 채 고착되는 현상 | 모바일에서 `:hover`가 stick 되는 브라우저 버그 가능성 | CSS 미디어 쿼리 `@media (hover: hover)` 지원 여부 검증 권고 |

---

## 4. E2E 테스트 4-Tier 계층형 검증 아키텍처

초보 개발자 친화적인 4단계 검증 피라미드는 **가장 가볍고 빠른 검증부터 시작하여 가장 포괄적인 실서버 통합 검증**으로 나아갑니다.

```
       ▲
      / \     Tier 4: 실서버 환경 E2E 시나리오 (HTTP 200, MIME Type, Live Crawl)
     /   \
    /     \   Tier 3: 클라이언트 인터랙션 & 테마 (CSS Focus-Dim, theme.js IIFE, FOUC 방지)
   /       \
  /         \ Tier 2: HTML 시맨틱 & 링크 무결성 (W3C 표준, <figure>/<figcaption>, 404 방지)
 /           \
/_____________\ Tier 1: 정적 파일 실재성 (14개 HTML, 이미지 디렉토리, 0 Byte 방지)
```

### 4.1 Tier 1: 파일 시스템 정적 검증 (Static File & Asset Presence)
* **목적**: 디스크 상에 필요한 모든 파일이 실재하며, 비어있지 않은지 0.01초 만에 확인.
* **검증 매트릭스**:
  1. `projects/*.html` 14개 파일 물리적 존재 검사.
  2. 각 프로젝트별 `images/<slug>/` 디렉토리 및 최소 1개 이상의 스크린샷 이미지 실재 검사.
  3. 공통 에셋: `index.html`, `style.css`, `theme.js` 존재 검사.
  4. 파일 크기 하한선:
     - HTML 파일: 최소 2,000 바이트 이상 (스켈레톤/더미 방지)
     - 이미지 파일: 최소 1,000 바이트 이상 (빈 파일 방지)

### 4.2 Tier 2: 시맨틱 구조 및 링크 404 경계값 검증 (HTML Semantic & Link Integrity)
* **목적**: HTML 표준 준수, 시맨틱 태그 구조 및 모든 내부 링크의 상호 참조 정합성 검증.
* **검증 매트릭스**:
  1. `index.html` 프로젝트 링크 파싱:
     - 14개 프로젝트의 `href`가 `./projects/<slug>.html` 형태로 정확히 교체되었는가?
     - `https://notion.so/...` 외부 링크가 프로젝트 섹션에 1개라도 남아있는가? (발견 시 FAIL)
     - 링크된 각 파일이 실제 `projects/` 폴더에 존재하는가?
  2. 14개 `projects/*.html` 상세 파싱:
     - W3C 헤더 메타데이터: `<title>`, `<meta name="description">`, `<meta name="viewport">`
     - 공통 리소스 링크: `<link rel="stylesheet" href="../style.css">`, `<script src="../theme.js"></script>`
     - 네비게이션 & 백링크: 상단/하단 `← Project` 링크의 `href="../index.html#project"`
     - 인용구: `<blockquote>` 존재 여부
     - 5대 표준 섹션 헤딩:
       1. `1. 하는 일 (Overview)`
       2. `2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)`
       3. `3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)`
       4. `4. 핵심 구현 기능 (Key Features)`
       5. `5. 엔지니어링 교훈 (Key Takeaways)`
     - `<figure>` 및 `<figcaption class="caption">`:
       - 모든 `<img>` 태그가 `<figure>` 내부에 위치하는가?
       - `<img>`의 `src`가 실제 존재하는 로컬 파일을 가리키는가? (404 방지)
       - `alt` 속성이 비어있지 않은가?
       - `<figcaption>` 텍스트가 의미 있는 설명을 담고 있는가?
     - 브라유 점자 불릿: Takeaways 및 목록에 `<ul><li>` 리스트 적용 여부.

### 4.3 Tier 3: DOM 인터랙션 및 테마 시스템 정합성 (Interaction & Styling)
* **목적**: CSS 인터랙션과 JavaScript 테마 토글이 규격대로 작동하도록 마크업 및 스타일 규칙 검증.
* **검증 매트릭스**:
  1. **포커스 딤(Focus Dim) CSS 검증 (`style.css`)**:
     - `.project-list:hover .project-link`에 `opacity: 0.35` 정의 확인
     - `.project-list .project-link:hover`에 `opacity: 1 !important` 정의 확인
     - `.project-link`에 `transition` (부드러운 전환 효과) 정의 확인
     - 2열 그리드 레이아웃: `grid-template-columns: minmax(0, 1fr) auto` 정의 확인
  2. **테마 시스템(Theme System) 검증 (`theme.js` & HTML)**:
     - `<head>` 내부 즉시 실행 함수(IIFE) 형태로 `theme.js`가 임베드되어 깜빡임(FOUC) 방지
     - `document.documentElement.dataset.theme` 속성 전환 로직
     - 토글 버튼: `button[data-theme-toggle]` 존재, `aria-pressed`, `data-theme-icon` 접근성 속성
     - CSS 변수: 다크/라이트 모드별 `--paper`, `--ink`, `--link`, `--muted`, `--rule`, `--image-frame` 완전 정의

### 4.4 Tier 4: 실서버 환경 E2E 시나리오 (Live Server HTTP & E2E Integration)
* **목적**: 실제 HTTP 프로토콜 상에서 모든 리소스가 정상 전달되는지 종합 크롤링 검증.
* **검증 매트릭스**:
  1. Python 내장 `http.server` 백그라운드 스레드 기동 (포트 3000 기본).
  2. `GET /index.html` 요청 -> HTTP 200 OK, MIME Type `text/html`.
  3. 메인 페이지 내 14개 프로젝트 링크 파싱 후 순차 HTTP GET 요청 -> 14개 전원 HTTP 200 OK.
  4. 각 프로젝트 페이지의 모든 종속 리소스(CSS, JS, PNG/JPG 이미지) HTTP GET 요청 -> 전원 HTTP 200 OK.
  5. 음성 테스트(Negative Test): `GET /projects/non-existent-sample.html` -> HTTP 404 확인.
  6. 서버 Graceful Shutdown 및 소켓 자원 반환.

---

## 5. 종합 자동 검증 스크립트 (`scripts/verify_portfolio.py`) 구현 명세

### 5.1 설계 원칙
1. **Zero External Dependencies**: `pip install` 없이 순수 Python 3 표준 라이브러리(`urllib`, `http.server`, `html.parser`, `threading`, `pathlib`)만 사용.
2. **초보 개발자를 위한 친절한 리포팅**: ANSI 터미널 색상과 함께 실패 원인, 문제 파일 경로 및 줄 번호, 해결 방법 가이드 제공.
3. **CI/CD 친화성**: 유닉스 종료 코드(`exit code 0`: 성공, `1`: 실패) 및 `--json` 출력 옵션 제공.

### 5.2 아키텍처 및 클래스 설계

```python
# scripts/verify_portfolio.py 주요 클래스 구조

class VerificationContext:
    """검증 실행 컨텍스트 및 결과 집계기"""
    def __init__(self, root_dir: Path, strict: bool = False):
        self.root_dir = root_dir
        self.strict = strict
        self.passed: List[str] = []
        self.failed: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []

class Tier1FilePresenceChecker:
    """Tier 1: 파일 시스템 실재성 및 크기 검사기"""
    def run(self, ctx: VerificationContext) -> bool: ...

class Tier2SemanticLinkChecker(HTMLParser):
    """Tier 2: HTML 파싱, W3C 시맨틱, 이미지 404 방지, 5개 섹션 검사기"""
    def run(self, ctx: VerificationContext) -> bool: ...

class Tier3InteractionThemeChecker:
    """Tier 3: CSS 포커스 딤 및 테마 JS/DOM 정합성 검사기"""
    def run(self, ctx: VerificationContext) -> bool: ...

class Tier4LiveServerHttpChecker:
    """Tier 4: 로컬 웹서버 기동 및 HTTP 200 E2E 크롤러"""
    def run(self, ctx: VerificationContext, port: int = 3000) -> bool: ...

class PortfolioVerifier:
    """종합 테스트 러너"""
    def run_all(self) -> int: ...
```

### 5.3 CLI 사용법 명세
```bash
# 전체 4-Tier 검증 실행
python3 scripts/verify_portfolio.py --all

# 특정 티어만 단독 실행 (개발 중 빠른 피드백)
python3 scripts/verify_portfolio.py --tier 1
python3 scripts/verify_portfolio.py --tier 2

# HTTP 테스트 포트 지정 및 엄격 모드(경고도 실패로 처리)
python3 scripts/verify_portfolio.py --all --port 8080 --strict

# CI/CD용 JSON 결과 출력
python3 scripts/verify_portfolio.py --all --json test_results.json
```

---

## 6. 결론 및 권고사항

1. **4-Tier 체계의 점진적 적용**: 개발 초기에는 Tier 1 & 2로 파일 및 마크업을 신속히 검증하고, 페이지 완성이 완료되면 Tier 3 & 4로 E2E 통합 품질을 검증합니다.
2. **이미지 404 방지**: 노션 이미지 다운로드 에이전트와 페이지 빌더 에이전트는 파일명 슬러그 규칙(소문자, 하이픈)을 통일하여 경로 불일치를 예방해야 합니다.
3. **무결성 게이트**: 오케스트레이터는 모든 에이전트 작업 완료 후 반드시 `scripts/verify_portfolio.py --all`을 최종 실행하여 무결성을 공인해야 합니다.
