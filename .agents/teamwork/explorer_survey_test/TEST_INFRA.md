# 🧪 E2E 테스트 아키텍처 및 검증 인프라 명세서 (TEST_INFRA.md)

> 이 문서는 **Noah Park 포트폴리오 웹사이트**의 14개 실전 프로젝트 케이스 스터디 및 메인 페이지에 대한 **E2E(End-to-End) 검증 및 테스트 인프라 아키텍처**를 정의한 엔지니어링 가이드입니다.
> 
> 초보 개발자도 테스트 피라미드의 개념과 링크 무결성(404 에러 방지), 시맨틱 웹 표준 검증 원리를 쉽게 이해하고 실무에 적용할 수 있도록 단계별로 설명합니다.

---

## 1. 테스트 철학: 왜 정적 사이트에도 E2E 테스트가 필요한가?

초보 개발자는 흔히 *"HTML, CSS, JS로만 이루어진 정적 웹사이트인데 굳이 복잡한 E2E 테스트가 필요할까?"*라고 생각하기 쉽습니다.

하지만 프로젝트 규모가 커져 **14개의 상세 케이스 스터디 페이지**와 **수십 장의 고화질 앱 스크린샷 이미지**, **다크/라이트 테마**, **미세 인터랙션(포커스 딤)**이 얽히게 되면 다음과 같은 치명적인 휴먼 에러가 빈번하게 발생합니다:

1. **상대 경로 실수로 인한 이미지 404 (Broken Images)**:
   - 메인 페이지에서는 `./images/crm/...`이지만, `projects/` 하위 페이지에서는 `../images/crm/...`이어야 합니다.
   - 단 하나의 마침표(`.`) 실수로 인해 면접관이나 방문자에게 깨진 이미지 엑스박스 아이콘이 노출됩니다.
2. **누락되거나 잘못 연결된 링크 (Dead Links)**:
   - 14개 프로젝트 중 일부가 여전히 외부 노션 링크로 남아있거나, 오타로 인해 잘못된 페이지로 이동할 수 있습니다.
3. **시맨틱 구조 결여로 인한 검색엔진(SEO) 및 접근성 훼손**:
   - `<figure>`와 `<figcaption>` 없이 날것의 `<img>`만 방치되면 화면 판독기(Screen Reader)와 웹 크롤러가 이미지 맥락을 해석할 수 없습니다.
4. **FOUC(화면 깜빡임) 및 테마 오작동**:
   - 테마 스크립트가 잘못된 위치에서 실행되면 새로고침 시 화면이 하얗게 번쩍이는 깜빡임 현상이 발생합니다.

이러한 결함을 **배포 전 단 1초 만에 자동으로 검출하고 방어**하기 위해 **4-Tier 계층형 E2E 검증 인프라**를 구축합니다.

---

## 2. E2E 테스트 4-Tier 검증 매트릭스

테스트는 가볍고 빠른 순서대로 계층을 이루어 실행됩니다:

```
[Tier 4] 실서버 환경 E2E 크롤링 (HTTP 200, MIME Type, 404 음성 테스트)
   ▲
[Tier 3] 클라이언트 인터랙션 & 스타일 (CSS 포커스 딤, theme.js IIFE, FOUC 방지)
   ▲
[Tier 2] HTML 시맨틱 & 링크 무결성 (W3C 표준, <figure>/<figcaption>, 5대 섹션)
   ▲
[Tier 1] 정적 파일 & 에셋 실재성 (14개 HTML 존재, 이미지 디렉토리, 0 Byte 방지)
```

### 상세 검증 매트릭스

| Tier | 계층 이름 | 주요 검증 항목 | 합격 기준 (Pass Criteria) | 실패 시 위험도 |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1** | 정적 파일 실재성 | • 14개 `projects/*.html` 파일 실재<br>• `images/<slug>/` 디렉토리 및 이미지 실재<br>• `index.html`, `style.css`, `theme.js` 실재 | • 14개 파일 전원 존재<br>• 프로젝트당 1개 이상 이미지 존재<br>• 파일 크기 > 0 (HTML ≥ 2KB, 이미지 ≥ 1KB) | 🔴 치명적 (Critical): 콘텐츠 누락 |
| **Tier 2** | 시맨틱 & 링크 무결성 | • `index.html` 14개 프로젝트 링크 검사<br>• 모든 `<img src="...">` 로컬 경로 역추적<br>• `<figure>` & `<figcaption>` 1:1 매칭<br>• 5대 표준 섹션 헤딩 (`h2`) 검사<br>• `alt` 텍스트 및 백링크(`← Project`) 검사 | • 노션 외부 링크 0개 (모두 로컬 매핑)<br>• 이미지 404 에러 0건<br>• 모든 스크린샷이 `<figure>`로 액자화<br>• 5대 섹션 헤딩 완벽 일치 | 🔴 치명적: 링크 깨짐 및 디자인 훼손 |
| **Tier 3** | 인터랙션 & 테마 | • Arlan.me 순수 CSS 포커스 딤 규칙<br>• Karri Saarinen 테마 토글 스크립트<br>• FOUC(화면 깜빡임) 방지 IIFE 로드 위치<br>• CSS 변수(`--paper`, `--ink` 등) 정의 | • `.project-list:hover` 시 opacity 0.35 적용<br>• hover 대상 1.0 선명 복원<br>• `theme.js`가 `<head>` 상단 위치<br>• 토글 버튼 A11y 속성 완비 | 🟡 경고 (Warning): UX 저하 |
| **Tier 4** | 실서버 E2E 통합 | • 내장 로컬 HTTP 서버 기동<br>• 메인 페이지 HTTP GET -> 200 OK<br>• 14개 상세 페이지 HTTP GET -> 200 OK<br>• 모든 에셋(CSS, JS, PNG) HTTP GET -> 200 OK<br>• 가상 404 경로 음성 테스트 | • 전체 HTTP 요청 100% 200 OK<br>• 적합한 Content-Type 응답<br>• 존재하지 않는 경로는 정확히 404 반환 | 🔴 치명적: 웹서버 배포 장애 |

---

## 3. 검증 도구: `scripts/verify_portfolio.py`

본 프로젝트는 외부 무거운 프레임워크(Cypress, Playwright 등) 없이, **순수 Python 3 표준 라이브러리**만으로 작성된 초경량 종합 자동 검증 스크립트(`scripts/verify_portfolio.py`)를 제공합니다.

### 3.1 주요 기능 및 특징
1. **Zero-Dependency**: 별도의 `pip install` 없이 macOS, Linux, Windows 어디서나 즉시 실행.
2. **풍부한 컬러 터미널 출력**: 초보자도 한눈에 성공(`[PASS]`), 실패(`[FAIL]`), 경고(`[WARN]`)를 파악할 수 있는 시각적 UI.
3. **친절한 디버깅 가이드**: 실패 발생 시 *"어느 파일의 몇 번째 줄에서 왜 실패했는지"*, *"어떻게 고치면 되는지"* 해결 팁을 함께 출력.
4. **CI/CD 자동화 지원**: 성공 시 exit code 0, 실패 시 1을 반환하여 GitHub Actions 등에서 빌드 실패를 감지.

### 3.2 명령어 가이드

```bash
# 1. 전체 4-Tier 종합 검증 실행
python3 scripts/verify_portfolio.py --all

# 2. 특정 Tier만 단독 실행 (개발 중 빠른 확인)
python3 scripts/verify_portfolio.py --tier 1   # 파일 존재 여부만 빠르게 확인
python3 scripts/verify_portfolio.py --tier 2   # 이미지 404 및 시맨틱 태그 확인
python3 scripts/verify_portfolio.py --tier 3   # 테마 및 포커스 딤 스타일 확인
python3 scripts/verify_portfolio.py --tier 4   # 로컬 웹서버 200 OK 크롤링

# 3. 사용자 지정 포트로 실서버 테스트 실행
python3 scripts/verify_portfolio.py --tier 4 --port 8080

# 4. 엄격 모드 (경고 사항도 실패로 엄격히 처리)
python3 scripts/verify_portfolio.py --all --strict

# 5. 결과 파일 JSON 내보내기 (CI/CD 파이프라인 연동)
python3 scripts/verify_portfolio.py --all --json test_results.json
```

---

## 4. 케이스 스터디 상세 페이지 (`projects/*.html`) 시맨틱 체크리스트

모든 케이스 스터디 상세 페이지는 W3C 표준과 `DESIGN.md` 명세를 100% 준수해야 하며, 검증 스크립트는 다음 항목을 전수 검사합니다:

### 4.1 필수 구조
```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[프로젝트 명] — Noah Park</title>
  <meta name="description" content="[프로젝트 요약]">
  <link rel="stylesheet" href="../style.css">
  <script src="../theme.js"></script> <!-- 반드시 head 내부 위치 (FOUC 방지) -->
</head>
<body class="article-page">
  <header class="site-header"> ... </header>

  <main class="article">
    <a href="../index.html#project" class="back-link">← Project</a>

    <header class="article-header">
      <h1>[프로젝트 제목]</h1>
      <span class="date">[기간] &middot; [역할]</span>
      <div class="article-meta-tags">
        <span class="tag">Next.js</span>
        <span class="tag">TypeScript</span>
        <span class="tag">PostgreSQL</span>
      </div>
    </header>

    <blockquote>"[핵심 엔지니어링 철학 인용문]"</blockquote>

    <h2>1. 하는 일 (Overview)</h2>
    <p>...</p>
    <figure>
      <img src="../images/[slug]/[file].png" alt="[이미지 설명]" />
      <figcaption class="caption">[상세 설명 캡션]</figcaption>
    </figure>

    <h2>2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)</h2>
    <p>...</p>

    <h2>3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)</h2>
    <p>...</p>

    <h2>4. 핵심 구현 기능 (Key Features)</h2>
    <p>...</p>

    <h2>5. 엔지니어링 교훈 (Key Takeaways)</h2>
    <ul>
      <li><strong>[교훈 제목]:</strong> [설명]</li>
    </ul>

    <hr>
    <a href="../index.html#project" class="back-link">← Back to Project</a>
  </main>

  <footer class="site-footer"> ... </footer>
</body>
</html>
```

---

## 5. CI/CD 자동화 연동 가이드 (GitHub Actions 예시)

GitHub 저장소에 코드를 푸시할 때마다 깨진 이미지나 링크가 없는지 자동으로 검사하도록 워크플로우를 설정할 수 있습니다:

```yaml
# .github/workflows/verify.yml
name: Portfolio Quality Gate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Run 4-Tier Portfolio Verification
        run: |
          python3 scripts/verify_portfolio.py --all --strict
```

---

## 6. 트러블슈팅 및 자주 묻는 질문 (FAQ)

### Q1. "Image file not found (404)" 에러가 발생합니다.
* **원인**: HTML 문서 내 `<img src="...">` 경로와 실제 파일 저장 위치가 불일치합니다.
* **해결**: `projects/` 폴더 내의 HTML 파일에서는 한 단계 상위 디렉토리로 이동해야 하므로, 반드시 `../images/<slug>/파일명.png` 형태로 작성해야 합니다. (`./images/...`는 404가 발생합니다.)

### Q2. "External Notion URL detected" 에러가 발생합니다.
* **원인**: `index.html`의 프로젝트 목록에 아직 Notion 원본 링크(`https://notion.so/...`)가 남아있습니다.
* **해결**: 모든 14개 프로젝트의 `href`를 로컬 상세 페이지 `./projects/<slug>.html`로 교체하십시오.

### Q3. "Section heading missing" 에러가 발생합니다.
* **원인**: 케이스 스터디 상세 페이지의 5대 표준 섹션 중 일부가 누락되었거나 제목 번호/철자가 일치하지 않습니다.
* **해결**: `1. 하는 일 (Overview)`, `2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)`, `3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)`, `4. 핵심 구현 기능 (Key Features)`, `5. 엔지니어링 교훈 (Key Takeaways)`의 5개 제목을 정확히 기재하십시오.
