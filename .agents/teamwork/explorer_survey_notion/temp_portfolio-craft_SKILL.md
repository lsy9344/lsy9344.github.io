---
name: temp_portfolio-craft
description: >-
  Karri Saarinen(Linear)의 미니멀 타이포그래피/장인정신 철학과 Arlan Marat의 포커스 딤(Focus Dim) 마이크로 인터랙션을 융합하여 고품질 개발자 소개 및 포트폴리오 웹사이트를 설계하고 제작하는 워크플로우 스킬입니다. 노션 포트폴리오 데이터 분석, 실측 앱 이미지 추출, 480px 단일 컬럼 그리드, CSS 변수 다크/라이트 테마, 케이스 스터디 작성 지침을 포함합니다.
---

# 🌿 temp_portfolio-craft: 미니멀 장인정신 포트폴리오 구축 가이드

이 스킬은 **Karri Saarinen**(Linear 공동 창업자 & CEO)의 극도로 정제된 타이포그래피와 **Arlan Marat**(디자인 엔지니어)의 세련된 포커스 딤 인터랙션을 결합하여, 군더더기 없이 단단한 개발자 포트폴리오 웹사이트를 처음부터 끝까지 구축하는 표준 워크플로우를 안내합니다.

---

## 1. 디자인 철학의 융합 (Core Philosophy)

### 1.1 "Less, but Better" (내용과 타이포그래피 중심)
* **화려한 그래픽보다 텍스트의 호흡**: 불필요한 3D, 화려한 그라디언트, 무거운 UI 라이브러리를 배제하고 폰트 자간, 행간, 여백으로 완성도를 극대화합니다.
* **480px 단일 컬럼 가독성**: 가로 폭을 480~500px로 제한하여 한 줄당 40~60자 내외가 들어가도록 설계합니다. 책 한 페이지를 읽는 듯한 눈의 피로 최소화와 높은 몰입감을 제공합니다.
* **아날로그 종이(Paper)와 먹물(Ink) 팔레트**: 완전한 블랙/화이트 대신 눈이 편안한 차콜(`#121213`)과 부드러운 오프화이트(`#fdfdfc`) 톤을 사용합니다.

### 1.2 두 레퍼런스 융합 매트릭스

| 영역 | 레퍼런스 원천 | 적용 패턴 |
| :--- | :--- | :--- |
| **전체 레이아웃 & 톤앤매너** | Karri Saarinen | `max-width: 480px`, 미니멀 헤더, 다크/라이트 테마 |
| **철학 및 원칙 리스트** | Karri Saarinen | `Notes on building`, 브라유 점자 불릿(`⡢`) |
| **프로젝트 목록 & 인터랙션** | Arlan Marat | 좌측 타이틀 + 우측 연도 2열 그리드, **포커스 딤(Focus Dim)** 효과 |
| **케이스 스터디 상세 페이지** | 융합 (Hybrid) | Karri식 아티클 레이아웃 + Arlan식 모던 태그 + 실제 앱 스크린샷 캡션 |

---

## 2. 작업 절차 (Step-by-Step Workflow)

### Step 1. 디자인 시스템 문서화 (`DESIGN.md`)
개발에 착수하기 전 반드시 `DESIGN.md`를 먼저 작성합니다:
* **레이아웃 명세**: 바디 패딩(`72px 24px 60px`), 모바일 반응형(`36px 20px 48px`).
* **CSS 변수 표**: `--paper`, `--ink`, `--link`, `--muted`, `--rule`, `--image-frame`.
* **타이포그래피 위계**:
  * `h1`: 18~21px (font-weight 500~600, letter-spacing -0.2px)
  * `h2`: 14px (font-weight 600)
  * `body`: 14px (line-height 1.7)
  * `meta / time`: 11~12px (`tabular-nums`)

### Step 2. 포트폴리오 소스 분석 (Notion 데이터 추출)
1. **재귀 순회 파싱**:
   * Notion API(`https://www.notion.so/api/v3/loadPageChunk`)를 사용하여 최상위 페이지와 하위 블록을 파싱합니다.
2. **실제 앱 이미지 추출**:
   * `https://www.notion.so/api/v3/getSignedFileUrls` 엔드포인트를 호출하여 노션 내부 `attachment:...` 파일의 서명된 AWS S3 URL을 가져옵니다.
   * 이미지를 로컬 `images/<project-slug>/` 폴더로 다운로드하여 외부 링크 만료에 구애받지 않는 영구 에셋으로 만듭니다.
3. **아키텍처 패턴 도출**:
   * 각 프로젝트에서 단순 기능 나열이 아닌, **해결한 문제**, **원장과 예상값의 분리(Fact vs Prediction)**, **스냅샷 패턴**, **멱등성(Idempotency)** 같은 엔지니어링 가치를 발굴합니다.

### Step 3. CSS 기반 포커스 딤(Focus Dim) 마이크로 인터랙션 구현
자바스크립트 이벤트 대신 **순수 CSS 5줄**로 브라우저 GPU 가속을 받는 초경량 인터랙션을 구현합니다:

```css
/* 목록 전체 호버 시 모든 항목을 딤(흐리게) 처리 */
.project-list:hover .project-link {
  opacity: 0.35;
}

/* 마우스가 직접 올라간 특정 항목만 100% 선명하게 복원 */
.project-list .project-link:hover {
  opacity: 1 !important;
  text-decoration: none;
}

.project-link {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  gap: 16px;
  padding: 4px 0;
  text-decoration: none;
  transition: opacity 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Step 4. 깜빡임 없는 테마 스크립트 (`theme.js`)
* HTML `<head>` 최상단에서 IIFE(즉시 실행 함수)로 동작하여 FOUC(화면 깜빡임)를 원천 차단합니다.
* OS 다크모드 선호(`window.matchMedia('(prefers-color-scheme: light)')`)와 사용자 수동 토글(`localStorage.getItem('theme')`)을 유기적으로 연동합니다.
* `<html>` 태그의 `data-theme="dark|light"` 속성을 조작하여 CSS 변수를 즉시 전환합니다.

### Step 5. 메인 페이지 구성 (`index.html`)
1. **Header**: 이름, 네비게이션(`Project`, `Writing`), GitHub 소셜 배지, 테마 토글 버튼(`☀︎ / ☾`).
2. **About me**: 2~3줄의 단단한 엔지니어링 지향점.
3. **Notes on building**: 브라유 점자(`⡢`) 불릿을 적용한 제품/개발 철학 목록.
4. **Project**: Arlan.me 스타일의 도메인별 2열 포커스 딤 목록.
   * 대표 프로젝트(첫 번째)는 자체 제작 상세 페이지(`projects/*.html`)로 연결.
   * 기타 프로젝트는 원본 노션 링크(`target="_blank" rel="noopener noreferrer"`)로 직행.
5. **Writing**: Karri Saarinen식 연도별 아카이브 그리드(`64px minmax(0, 1fr)`).

### Step 6. 심층 케이스 스터디 상세 페이지 구축 (`projects/*.html`)
* 상단 `← Project` 백링크와 Arlan식 기술 태그 칩 배치.
* 핵심 인용구(`<blockquote>`).
* **`<figure>`와 `<figcaption>` 시맨틱 태그**를 활용한 실제 고화질 앱 스크린샷 렌더링.
* 이미지에 미세 테두리(`border: 1px solid var(--rule); border-radius: 6px;`)를 부여하여 다크 모드에서도 스크린샷이 선명하게 돋보이도록 액자화.
* 엔지니어링 교훈(Takeaways)을 브라유 점자 불릿으로 정리.

---

## 3. 핵심 규칙 및 주의사항 (Do's & Don'ts)

* **Do**: 불필요한 번들러나 무거운 npm 패키지 없이 순수 웹 표준(Semantic HTML5, CSS Variables, Vanilla JS)을 지향할 것.
* **Do**: 반응형 디자인을 위해 모바일 미디어 쿼리(`@media (max-width: 560px)`)를 반드시 포함할 것.
* **Do**: 링크 클릭 시 불필요한 아코디언이나 모달로 가로막지 말고, 콘텐츠로 가장 빠르게 직행하도록 원칙을 준수할 것.
* **Don't**: 완전한 순흑(`#000000`)과 순백(`#ffffff`)을 배경과 본문에 직접 사용하지 말 것 (눈부심 유발 방지).
* **Don't**: 이미지에 캡션 없이 날것으로 방치하지 말 것. 항상 시각 자료의 맥락을 `<figcaption>`으로 설명할 것.
