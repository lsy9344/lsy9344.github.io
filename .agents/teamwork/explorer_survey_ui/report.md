# 🎨 UI 디자인 시스템 정밀 조사 보고서 및 14개 프로젝트 표준 HTML 템플릿 명세서

> **작성자**: Teamwork Explorer (UI Survey & Design System Specialist)  
> **대상자**: 초보 소프트웨어 엔지니어 & 프로젝트 빌더 에이전트  
> **기준 레퍼런스**: Karri Saarinen (Linear CEO) × Arlan Marat (Design Engineer)  
> **참조 문서**: `DESIGN.md`, `temp_portfolio-craft/SKILL.md`, `projects/beauty-brand-crm.html`, `index.html`, `style.css`, `theme.js`

---

## 1. 서론 및 핵심 디자인 철학 (Core Philosophy)

### 1.1 "Less, but Better" — 타이포그래피와 여백 중심의 웹
웹 개발을 처음 배울 때 흔히 저지르는 실수는 3D 캔버스, 화려한 그라디언트, 무거운 컴포넌트 라이브러리(Bootstrap, MUI 등)를 과도하게 끌어다 쓰는 것입니다. 그러나 Linear의 창업자이자 디자이너인 **Karri Saarinen**과 디자인 엔지니어 **Arlan Marat**의 웹사이트는 군더더기를 극도로 덜어내고 **타이포그래피의 계층, 줄바꿈의 호흡, 섬세한 여백, 그리고 부드러운 마이크로 인터랙션**만으로 압도적인 완성도를 증명합니다.

### 1.2 480px 단일 컬럼 그리드와 가독성 (CPL 최적화)
* **원리**: 일반적인 웹사이트처럼 `1200px` 전체를 텍스트로 채우면 한 줄이 너무 길어져 왼쪽에서 오른쪽으로 시선을 이동하다가 다음 줄을 놓치게 됩니다(독서 피로도 급증).
* **CPL (Characters Per Line)**: 인지과학과 타이포그래피 연구에 따르면 인간이 한눈에 인지하고 편안하게 읽을 수 있는 한 줄당 글자 수는 **45~65자(영문)**, **30~45자(한글)**입니다.
* **480px의 힘**: `max-width: 480px` 컨테이너는 책 한 페이지를 손에 쥐고 읽는 듯한 최적의 CPL을 강제하여, 독자가 긴 기술 문서나 포트폴리오를 읽어도 지치지 않게 만듭니다.

### 1.3 Paper & Ink 팔레트 — 눈부심 없는 아날로그 질감
* 순수한 검정(`#000000`) 배경에 순수한 흰색(`#ffffff`) 텍스트는 명도 대비가 21:1에 달해 눈의 망막을 자극하고 잔상을 유발합니다(Halation 현상).
* 본 디자인 시스템은 아날로그 종이(Paper)와 먹물(Ink)의 질감을 차용하여:
  * **다크 모드**: 차콜 톤 배경(`--paper: #121213`) 위에 부드러운 오프화이트(`--ink: #deddd8`)를 얹어 눈의 피로를 최소화합니다.
  * **라이트 모드**: 새하얀 A4 용지 대신 따뜻한 미색 종이(`--paper: #fdfdfc`) 위에 깊은 먹색(`--ink: #292824`)을 사용합니다.

---

## 2. 기존 케이스 스터디 (`projects/beauty-brand-crm.html`) 정밀 해부

기존에 단독 완성되어 있는 `beauty-brand-crm.html`은 향후 제작될 13개 상세 페이지의 **골든 마스터(Golden Master)**입니다. 이 파일의 모든 DOM 요소와 CSS 속성은 명확한 설계 의도를 가지고 있습니다.

### 2.1 문서 기본 골격 및 헤더 (`<head>` & `<header>`)

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>뷰티 브랜드 고객 관리·캠페인 준비 CRM — Noah Park</title>
  <meta name="description" content="실측 구매 기록과 AI 재구매 예측을 분리하고, 5단계 안전 관문으로 발송을 제어하는 고객 관리 SaaS 개발기.">
  <!-- 상위 폴더(루트)의 스타일시트와 테마 스크립트를 참조하므로 반드시 '../' 상대 경로 유지 -->
  <link rel="stylesheet" href="../style.css">
  <script src="../theme.js"></script>
</head>

<body class="article-page">
  <!-- 상단 사이트 헤더: 메인 홈의 헤더와 통일된 네비게이션 제공 -->
  <header class="site-header">
    <h1>
      <a class="name" href="../index.html">Noah Park</a>
    </h1>
    <nav aria-label="Main navigation">
      <a href="../index.html#project">Project</a>
      <a href="../index.html#writing">Writing</a>
      <a class="social-link" href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Dark mode toggle" aria-pressed="false">
        <span data-theme-icon aria-hidden="true">☾</span>
      </button>
    </nav>
  </header>
```

💡 **학습 포인트**:
1. `projects/` 하위 디렉토리에 위치하므로 모든 CSS/JS 및 홈 링크는 `../`로 시작해야 합니다.
2. `<body>`에 `class="article-page"`를 부여하여 페이지 단위의 스타일 확장을 지원합니다.
3. 테마 토글 버튼(`[data-theme-toggle]`)은 자바스크립트 접근성 표준(`aria-label`, `aria-pressed`)을 준수합니다.

---

### 2.2 백링크 (`.back-link`)와 아티클 헤더 (`.article-header`)

```html
<main class="article">
  <!-- 1. 본문 최상단 백링크: 홈의 #project 섹션으로 즉시 회귀 -->
  <a href="../index.html#project" class="back-link">← Project</a>

  <!-- 2. 제목, 작업 기간/역할, 기술 태그 칩 -->
  <header class="article-header">
    <h1>뷰티 브랜드 고객 관리·캠페인 준비 CRM</h1>
    <span class="date">2026.08 — 2026.10 &middot; Product Design & Full-stack Engineering</span>
    
    <div class="article-meta-tags">
      <span class="tag">Next.js</span>
      <span class="tag">TypeScript</span>
      <span class="tag">PostgreSQL</span>
      <span class="tag">Prisma</span>
      <span class="tag">CRM SaaS</span>
    </div>
  </header>
```

* **`.back-link`의 인터랙션**:
  * 마진: `margin-bottom: 36px;`로 본문 헤더와 확실한 공간적 거리를 둡니다.
  * 색상: 평소에는 차분한 `--muted` 컬러이다가 호버 시 선명한 `--ink`로 전환되며 밑줄이 생기지 않아 깔끔함을 유지합니다.
* **`.article-header h1`**:
  * 글자 크기 `21px`, `font-weight: 600`, `letter-spacing: -0.3px` (자간을 미세하게 조여 제목의 밀도감을 높임).
* **`.article-meta-tags .tag` (Arlan Marat 스타일 칩)**:
  * 폰트: 시스템 모노스페이스(`ui-monospace, SFMono-Regular, Menlo, Monaco, monospace`).
  * 스타일: `font-size: 11px`, `padding: 2px 7px`, `border-radius: 3px`, `background: var(--image-frame)`, `border: 1px solid var(--rule)`.
  * 목적: 사용된 핵심 기술 스택을 직관적이면서도 과하지 않은 칩 형태로 한눈에 보여줍니다.

---

### 2.3 핵심 인용구 (`<blockquote>`)

```html
<blockquote>
  "기록(Actual Fact)과 예상값(Predicted Value)을 분리하지 않으면, 계산으로 나온 관심 상품이 실제 구매처럼 보이고 실적은 왜곡된다."
</blockquote>
```

* **디자인 의도**: 프로젝트 전체를 관통하는 가장 핵심적인 **아키텍처 철학 또는 엔지니어링 문제의식**을 이탤릭체로 강조합니다.
* **CSS 구현 (`style.css:396-402`)**:
  ```css
  .article blockquote {
    margin: 28px 0;
    padding: 0 0 0 18px;
    border-left: 2px solid var(--quote-rule);
    color: var(--quote-ink);
    font-style: italic;
  }
  ```
  * 왼쪽에 2px 두께의 은은한 라인(`--quote-rule`)을 부여하여 본문 텍스트와 시각적으로 명확히 구분됩니다.

---

### 2.4 `<figure>`와 `<figcaption>` 시맨틱 이미지 프레임

```html
<!-- 실제 앱 사용 이미지: 커버 및 오토메이션 화면 -->
<figure>
  <img src="../images/crm/01_automation_cover.png" alt="고객 인사이트와 시각적 자동화 화면" />
  <figcaption class="caption">고객 인사이트와 시각적 자동화, 담당자 지정과 후속 업무가 한 초안으로 이어지는 메인 작업 화면</figcaption>
</figure>
```

* **시맨틱 웹 표준**: 단순 `<div>`나 `<img>`만 던져놓는 것이 아니라, HTML5의 시맨틱 태그인 `<figure>`와 설명문 `<figcaption>`을 사용합니다.
* **액자 프레임 CSS (`style.css:408-425`)**:
  ```css
  .article figure img {
    display: block;
    width: 100%;
    height: auto;
    border-radius: 6px;
    border: 1px solid var(--rule);
    background: var(--image-frame);
    transition: transform 0.2s ease;
  }
  .article figcaption,
  .article .caption {
    font-size: 11px;
    color: var(--muted);
    margin-top: 8px;
    line-height: 1.5;
    text-align: center;
  }
  ```
  💡 **왜 이미지에 테두리(`border`)와 배경색(`background`)을 주는가?**  
  다크 모드에서 스크린샷의 배경이 흰색이거나 반대로 어두운 화면일 때, 웹사이트 배경과 스크린샷 경계가 뭉개질 수 있습니다. `border: 1px solid var(--rule)`을 주면 얇은 액자(Frame) 효과가 생겨 어떤 색상의 앱 캡처든 단정하고 또렷하게 분리됩니다.

---

### 2.5 Karri Saarinen식 점자 불릿 (`⡢`) 가상 요소

`projects/beauty-brand-crm.html`의 2장(해결한 문제)과 5장(엔지니어링 교훈)을 보면 리스트(`<ul>`)가 있습니다.

```html
<ul>
  <li><strong>Fact vs Prediction:</strong> 머신러닝이나 통계 알고리즘이 뽑아낸 지표는 '추정'일 뿐입니다.</li>
  <li><strong>실제 화면이 주는 신뢰:</strong> 복잡한 비즈니스 로직일수록 직관적인 시각화가 중요합니다.</li>
  <li><strong>방어적 안전장치:</strong> 자동화 도구에서 가장 중요한 것은 Guardrails입니다.</li>
</ul>
```

* **놀라운 점**: HTML 코드 안에는 어디에도 점자 기호(`⡢`)를 적지 않았습니다!
* **CSS 구현 비밀 (`style.css:427-445`)**:
  ```css
  .article ul {
    list-style: none; /* 브라우저 기본 까만 점(•) 제거 */
    padding-left: 20px;
    margin: 14px 0 24px;
  }
  .article ul li {
    position: relative;
    margin: 7px 0;
    line-height: 1.6;
  }
  .article ul li::before {
    content: '⡢'; /* 브라유 점자 유니코드 U+2862 */
    position: absolute;
    left: -20px;
    top: -0.25em;
    color: var(--muted);
  }
  ```
  💡 **초보 개발자가 배워야 할 점**:
  * 콘텐츠(HTML)와 표현(CSS)을 철저히 분리했습니다.
  * 스크린 리더 등 보조 기기가 읽을 때 의미 없는 특수문자가 음성으로 낭독되지 않도록 시맨틱 순수 태그(`<ul><li>`)를 유지하고, 시각적 장식만 CSS `::before`로 처리한 것입니다.

---

### 2.6 케이스 스터디의 5대 표준 섹션 구성 (Structure)

`beauty-brand-crm.html`은 기승전결이 완벽한 5개 장으로 조직되어 있습니다. 14개 프로젝트 전체가 이 표준 5단 구성을 따라야 합니다:

| 번호 | 섹션 명칭 | 주요 내용 및 포함 요소 |
| :---: | :--- | :--- |
| **1** | **하는 일 (Overview)** | 서비스의 배경, 기존 작업 방식의 비효율, 본인의 역할 및 개발 기간. 대표 커버 스크린샷 1개(`<figure>`). |
| **2** | **해결한 문제 & 데이터 정합성 (Problem & Integrity)** | 단순 기능 나열이 아닌, 데이터 오류/버그/운영 사고를 막은 엔지니어링 문제 해결. 불릿 리스트(`<ul><li>`). 2번째 스크린샷(`<figure>`). |
| **3** | **시스템 아키텍처 및 처리 흐름 (Architecture & Flow)** | DB 및 프레임워크 스택, 데이터 동기화 주기. 핵심 안전 관문 코드 스니펫(`<pre><code>`). 파이프라인/흐름도 스크린샷(`<figure>`). |
| **4** | **핵심 구현 기능 (Key Features)** | 2~3개의 세부 기능 소제목(`<h3>`), 설명 문단(`<p>`), 해당 화면의 고화질 스크린샷(`<figure>`). |
| **5** | **엔지니어링 교훈 (Key Takeaways)** | 프로젝트를 통해 얻은 3가지 아키텍처/엔지니어링 인사이트를 담은 불릿 리스트 (`<ul><li><strong>키워드:</strong> 설명</li></ul>`). |

---

## 3. 메인 페이지 2열 그리드 & Focus Dim(포커스 딤) 원리

### 3.1 2열 고밀도 그리드 구조 (`index.html`)

```html
<ul class="project-list">
  <li>
    <a href="./projects/beauty-brand-crm.html" class="project-link">
      <span class="project-title">뷰티 브랜드 고객 관리·캠페인 준비 CRM</span>
      <span class="project-year">2026</span>
    </a>
  </li>
  <!-- ... 다른 프로젝트 항목들 ... -->
</ul>
```

* `.project-link`:
  ```css
  .project-link {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: baseline;
    gap: 16px;
    padding: 4px 0;
    text-decoration: none;
    cursor: pointer;
    transition: opacity 0.15s cubic-bezier(0.16, 1, 0.3, 1);
  }
  ```
  * `minmax(0, 1fr)`: 좌측 프로젝트 제목이 공간을 최대한 차지하되, 좁은 화면에서 텍스트가 넘칠 때 그리드가 터지지 않도록 `minmax(0, ...)`을 사용합니다.
  * `.project-title`: `white-space: nowrap; overflow: hidden; text-overflow: ellipsis;` 속성을 통해 긴 한글 제목도 우측 연도를 밀어내지 않고 단정하게 말줄임표(`...`) 처리됩니다.
  * `auto` & `.project-year`: `font-variant-numeric: tabular-nums;`로 2026 숫자의 자릿수 폭을 균일하게 맞춰 세로 열 정렬이 칼같이 일치합니다.

---

### 3.2 순수 CSS 5줄로 만드는 초고성능 포커스 딤 (Focus Dim)

```css
/* 1. 사용자가 프로젝트 목록(.project-list) 전체 영역에 마우스를 올리면, 목록 안의 모든 링크를 0.35로 흐리게 만듭니다 */
.project-list:hover .project-link {
  opacity: 0.35;
}

/* 2. 하지만 사용자의 마우스 포인터가 직접 올라간 '그 하나의 링크'만 100% 선명하게 덮어씁니다! */
.project-list .project-link:hover {
  opacity: 1 !important;
  text-decoration: none;
}
```

💡 **초보 개발자를 위한 CS/브라우저 렌더링 팁**:
1. 자바스크립트로 구현하면 `mousemove` 이벤트마다 DOM을 탐색하고 스타일을 변경해야 하므로 브라우저 메인 스레드에 부담을 줍니다.
2. 하지만 CSS의 `opacity` 속성은 **합성(Composite) 단계**에서 브라우저 GPU 가속을 받기 때문에 초당 60~120fps로 극도로 부드럽게 동작합니다.
3. CSS 선택자의 특이성(Specificity)과 부모 호버 계층을 이용한 이 기법은 모던 웹 디자인의 정수입니다.

---

## 4. 다크/라이트 테마 시스템 & 반응형 레이아웃 원리

### 4.1 테마 변수 매핑 테이블 (`style.css`)

| CSS 변수명 | 역할 | 다크 모드 (`dark`) | 라이트 모드 (`light`) | 비고 |
| :--- | :--- | :---: | :---: | :--- |
| `--paper` | 배경 캔버스 | `#121213` | `#fdfdfc` | 눈부심 없는 차콜 / 미색 종이 |
| `--ink` | 기본 본문 텍스트 | `#deddd8` | `#292824` | 배경과의 적정 명도 대비 유지 |
| `--link` | 링크 및 대제목 강조 | `#ffffff` | `#080808` | 선명한 흑백 대비 |
| `--muted` | 연도, 메타정보, 캡션 | `#9d9b96` | `#77746d` | 중간 계층 보조 텍스트 |
| `--rule` | 구분선 및 프레임 테두리 | `#303030` | `#e5e2db` | 섬세한 1px 라인 |
| `--quote-rule` | 인용문 좌측 세로선 | `#45433e` | `#d5d2ca` | `blockquote` 전용 |
| `--quote-ink` | 인용문 텍스트 | `#b6b3aa` | `#59564d` | 이탤릭 본문 톤 |
| `--code-paper` | 코드 블록 배경 | `#1d1d1c` | `#f2f0e9` | `pre`, `code` 배경음영 |
| `--image-frame` | 이미지/태그 칩 배경 | `#202021` | `#f1f0ea` | 액자 프레임 및 태그 칩 |

### 4.2 `theme.js`와 FOUC(화면 깜빡임) 방지 메커니즘
웹사이트를 새로고침할 때 다크 모드 사용자의 화면이 0.1초 동안 하얗게 번쩍였다가 다시 검게 변하는 현상을 **FOUC(Flash of Unstyled Content)**라고 합니다.
`theme.js`는 이 문제를 완전히 해결했습니다:
1. `<script src="../theme.js"></script>`를 `<body>`가 아닌 `<head>`의 맨 아래에 배치합니다.
2. 브라우저가 화면을 그리기 전에 즉시 실행 함수(IIFE)가 실행되어 `localStorage` 또는 `matchMedia('(prefers-color-scheme: light)')`를 검사합니다.
3. 즉시 `<html data-theme="dark|light">` 속성을 DOM 트리에 주입합니다.
4. CSS 엔진이 HTML 본문을 처음 파싱하여 화면에 그리는 순간 이미 해당 테마의 CSS 변수가 적용되어 있으므로 깜빡임이 0%입니다.

### 4.3 480px 컨테이너 및 모바일 반응형 미디어 쿼리
```css
body {
  max-width: 480px;
  margin: 0 auto;
  padding: 72px 24px 60px;
}

@media (max-width: 560px) {
  body {
    padding: 36px 20px 48px;
  }
  .site-header {
    margin-bottom: 34px;
  }
}
```
* 화면 너비가 560px 이하인 모바일 기기에서는 패딩을 위아래 `36px/48px`, 좌우 `20px`로 좁혀 작은 화면에서도 글자가 너무 일찍 줄바꿈되지 않도록 여백을 최적화합니다.

---

## 5. 14개 프로젝트 전체 매핑 현황

`index.html`의 4대 카테고리에 정의된 14개 프로젝트의 상세 정보 및 권장 파일명/이미지 디렉토리 명세입니다:

| No | 카테고리 (Category) | 프로젝트 공식 명칭 | 추천 HTML 파일명 (`projects/*.html`) | 추천 이미지 디렉토리 (`images/*/`) | 노션 Page ID |
|:--:| :--- | :--- | :--- | :--- | :--- |
| **1** | Commerce & SaaS | 뷰티 브랜드 고객 관리·캠페인 준비 CRM | `beauty-brand-crm.html` *(완료)* | `images/crm/` *(6장 보유)* | `3f90c30e...` |
| **2** | Commerce & SaaS | 뷰티 브랜드 다국어 상품 후기 플랫폼 | `beauty-reviews-platform.html` | `images/reviews/` | `a420c30e2dc083f58df0815ac6aefeb4` |
| **3** | Commerce & SaaS | 뷰티 브랜드 BAND 콘텐츠 운영 자동화 | `beauty-band-automation.html` | `images/band-auto/` | `5300c30e2dc083b3b46601a6db18cf3e` |
| **4** | Commerce & SaaS | 뷰티 브랜드 사내 ERP·재고·매출 관리 | `beauty-inventory-erp.html` | `images/beauty-erp/` | `39d0c30e2dc082f9bf1801bd61e8ae54` |
| **5** | Media & Photo Booth | Boothy · 무인 사진관 촬영·프리셋·운영 제어 | `boothy-photo-booth.html` | `images/boothy/` | `4590c30e2dc082deac2301c38029ea55` |
| **6** | Media & Photo Booth | 다지점 사진관 운영·급여·주차·보정 ERP | `photo-studio-erp.html` | `images/studio-erp/` | `cda0c30e2dc083aa81e781f872730906` |
| **7** | Media & Photo Booth | 다지점 예약 안내·리뷰 요청 문자 자동화 | `studio-sms-automation.html` | `images/studio-sms/` | `24d0c30e2dc0825593fe810da40499e4` |
| **8** | Media & Photo Booth | CutEditor 브라우저 사진 편집·PNG 저장 도구 | `cuteditor-photo-tool.html` | `images/cuteditor/` | `1320c30e2dc0824fb6d101a77e8fc48a` |
| **9** | Specialized Industry ERP | 베트남 에스테틱 접수·객실·정산 ERP | `vietnam-aesthetic-erp.html` | `images/aesthetic-erp/` | `fa80c30e2dc08283b17701bab4aea61f` |
| **10** | Specialized Industry ERP | 수산물 유통 본사·지점 통합 ERP | `seafood-distribution-erp.html` | `images/seafood-erp/` | `82f0c30e2dc082579edb81f3ff79e03b` |
| **11** | Specialized Industry ERP | 군부대 식사 신청·식권·급여 공제 관리 | `military-meal-management.html` | `images/military-meal/` | `2630c30e2dc082869e7781b35b22ad1e` |
| **12** | Automation & Tools | 멀티마켓 상품·판매자 공개정보 수집기 | `multimarket-scraper.html` | `images/market-scraper/` | `a890c30e2dc082039891011dd4d456ff` |
| **13** | Automation & Tools | 카카오톡 미열람 1:1 대화방 엑셀 정리 도구 | `kakaotalk-unread-cleaner.html` | `images/kakaotalk-tool/` | `4010c30e2dc082d3bd280198dfeb3e3d` |
| **14** | Automation & Tools | 배달센터 실적 자동화 서비스 소개 웹 (TactRun) | `tactrun-delivery-web.html` | `images/tactrun/` | `b280c30e2dc0822483c9812ea88fd5ec` |

---

## 6. 14개 프로젝트 표준 HTML 템플릿 명세서 (Template Specification)

모든 프로젝트 상세 페이지 빌더 에이전트 및 개발자는 **반드시 아래 표준 템플릿 스니펫을 기반으로** 페이지를 작성해야 합니다.

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{PROJECT_TITLE}} — Noah Park</title>
  <meta name="description" content="{{PROJECT_SUMMARY_META}}">
  <link rel="stylesheet" href="../style.css">
  <script src="../theme.js"></script>
</head>

<body class="article-page">
  <!-- 상단 사이트 헤더 -->
  <header class="site-header">
    <h1>
      <a class="name" href="../index.html">Noah Park</a>
    </h1>

    <nav aria-label="Main navigation">
      <a href="../index.html#project">Project</a>
      <a href="../index.html#writing">Writing</a>
      <a class="social-link" href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
      <button class="theme-toggle" type="button" data-theme-toggle aria-label="Dark mode toggle" aria-pressed="false">
        <span data-theme-icon aria-hidden="true">☾</span>
      </button>
    </nav>
  </header>

  <!-- 본문 컨테이너 -->
  <main class="article">
    <a href="../index.html#project" class="back-link">← Project</a>

    <header class="article-header">
      <h1>{{PROJECT_TITLE}}</h1>
      <span class="date">{{DATE_RANGE}} &middot; {{ROLE_DESCRIPTION}}</span>
      
      <div class="article-meta-tags">
        <!-- 3~6개의 주요 기술 및 도메인 태그 -->
        {{#each TECH_TAGS}}
        <span class="tag">{{this}}</span>
        {{/each}}
      </div>
    </header>

    <blockquote>
      "{{KEY_QUOTE_OR_CORE_PHILOSOPHY}}"
    </blockquote>

    <h2>1. 하는 일 (Overview)</h2>
    <p>
      {{OVERVIEW_PARAGRAPH_1}}
    </p>
    <p>
      {{OVERVIEW_PARAGRAPH_2}}
    </p>

    <!-- [스크린샷 1]: 메인 화면 / 커버 -->
    <figure>
      <img src="../images/{{PROJECT_SLUG}}/{{IMAGE_1_NAME}}" alt="{{IMAGE_1_ALT}}" />
      <figcaption class="caption">{{IMAGE_1_CAPTION}}</figcaption>
    </figure>

    <h2>2. 해결한 문제 & 데이터 정합성 (Problem & Integrity)</h2>
    <p>
      {{PROBLEM_PARAGRAPH_1}}
    </p>
    <p>
      {{PROBLEM_PARAGRAPH_2}}
    </p>

    <ul>
      {{#each PROBLEM_SOLUTIONS}}
      <li><strong>{{this.title}}:</strong> {{this.description}}</li>
      {{/each}}
    </ul>

    <!-- [스크린샷 2]: 데이터 처리 / 규칙 / 검증 화면 -->
    <figure>
      <img src="../images/{{PROJECT_SLUG}}/{{IMAGE_2_NAME}}" alt="{{IMAGE_2_ALT}}" />
      <figcaption class="caption">{{IMAGE_2_CAPTION}}</figcaption>
    </figure>

    <h2>3. 시스템 아키텍처 및 처리 흐름 (Architecture & Flow)</h2>
    <p>
      {{ARCHITECTURE_PARAGRAPH}}
    </p>

    <pre><code>{{CORE_CODE_SNIPPET}}</code></pre>

    <!-- [스크린샷 3]: 시스템 구조 / 파이프라인 / 다이어그램 (있는 경우) -->
    <figure>
      <img src="../images/{{PROJECT_SLUG}}/{{IMAGE_3_NAME}}" alt="{{IMAGE_3_ALT}}" />
      <figcaption class="caption">{{IMAGE_3_CAPTION}}</figcaption>
    </figure>

    <h2>4. 핵심 구현 기능 (Key Features)</h2>

    <h3>{{FEATURE_1_TITLE}}</h3>
    <p>
      {{FEATURE_1_DESCRIPTION}}
    </p>

    <!-- [스크린샷 4]: 기능 세부 화면 1 -->
    <figure>
      <img src="../images/{{PROJECT_SLUG}}/{{IMAGE_4_NAME}}" alt="{{IMAGE_4_ALT}}" />
      <figcaption class="caption">{{IMAGE_4_CAPTION}}</figcaption>
    </figure>

    <h3>{{FEATURE_2_TITLE}}</h3>
    <p>
      {{FEATURE_2_DESCRIPTION}}
    </p>

    <h3>{{FEATURE_3_TITLE}}</h3>
    <p>
      {{FEATURE_3_DESCRIPTION}}
    </p>

    <!-- [스크린샷 5]: 기능 세부 화면 2 또는 전체 조감도 -->
    <figure>
      <img src="../images/{{PROJECT_SLUG}}/{{IMAGE_5_NAME}}" alt="{{IMAGE_5_ALT}}" />
      <figcaption class="caption">{{IMAGE_5_CAPTION}}</figcaption>
    </figure>

    <h2>5. 엔지니어링 교훈 (Key Takeaways)</h2>
    <ul>
      {{#each TAKEAWAYS}}
      <li><strong>{{this.keyword}}:</strong> {{this.insight}}</li>
      {{/each}}
    </ul>

    <hr>
    <a href="../index.html#project" class="back-link">← Back to Project</a>
  </main>

  <!-- 푸터 -->
  <footer class="site-footer">
    <span>© 2026 Noah Park. Crafted with care.</span>
    <span><a href="mailto:noah.park.dev@example.com">Contact</a></span>
  </footer>
</body>
</html>
```

---

## 7. 제작 가이드 및 체크리스트 (Do's & Don'ts)

### 7.1 반드시 준수해야 할 필수 원칙 (Do's)
1. **상대 경로 검증**: `projects/*.html` 내부에서 상위 에셋을 참조할 때 `../style.css`, `../theme.js`, `../images/<slug>/...`, `../index.html`처럼 반드시 `../`가 포함되어야 합니다.
2. **시맨틱 태그 준수**:
   - 이미지는 반드시 `<figure>`로 감싸고 하단에 `<figcaption class="caption">`을 병기합니다.
   - 불릿 리스트는 순수 `<ul><li>`만 작성하며, 점자 기호(`⡢`)를 HTML 문자열로 직접 넣지 않습니다(CSS `::before` 자동 처리).
   - 인용구는 `<blockquote>` 태그를 사용합니다.
3. **이미지 실제 존재 확인**: `images/<project_slug>/` 디렉토리에 실제 다운로드된 고해상도 이미지가 있을 때만 `src`에 명시하며, 404가 발생하지 않도록 파일명을 일치시킵니다.
4. **Takeaways 3가지 포함**: 5장 엔지니어링 교훈에는 단순 소감이 아닌, **아키텍처/데이터 무결성 관점의 교훈 3가지**를 굵은 글씨(`<strong>`) 키워드와 함께 배치합니다.
5. **메인 페이지 링크 전환**: `index.html`의 14개 항목 모두 기존 노션 외부 링크 대신 생성된 로컬 파일(`./projects/<slug>.html`)로 교체되어야 합니다.

### 7.2 피해야 할 안티패턴 (Don'ts)
1. ❌ 인라인 스타일(`style="..."`)의 남용을 금지합니다. 모든 타이포그래피와 여백은 `style.css` 클래스를 활용합니다.
2. ❌ 모달 팝업이나 아코디언 드롭다운으로 콘텐츠를 가리지 않습니다. Karri Saarinen과 Arlan Marat의 철학에 따라 사용자가 한 번의 스크롤로 모든 깊이 있는 정보를 자연스럽게 읽을 수 있어야 합니다.
3. ❌ 캡션 없는 날것의 이미지 배치를 금지합니다. 스크린샷이 무엇을 나타내는지 모르는 방문자에게 `figcaption`은 맥락을 전달하는 결정적인 역할을 합니다.
4. ❌ 본문에 순수한 검정(`#000`)이나 순백(`#fff`)을 하드코딩하지 않습니다. 모든 색상은 CSS 변수(`var(--ink)`, `var(--muted)` 등)를 통해 다크/라이트 테마에 반응해야 합니다.
