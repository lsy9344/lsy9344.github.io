# Reviewer 2 검토 보고서: 시스템 아키텍처 및 테마/링크 정합성 검증

**검토자**: Reviewer 2 (Roles: reviewer, critic)  
**일시**: 2026-10-21T19:43:00Z  
**최종 판정**: **APPROVE (승인)**  

---

## 1. 관찰 결과 (Observation)

직접 확인하고 검증한 사실과 명령어 실행 결과는 다음과 같습니다:

### ① 4-Tier E2E 종합 검증 및 단위 테스트 실행 결과
- **명령어**: `python3 scripts/verify_portfolio.py --all --strict`
  - **결과**: `최종 판정: PASSED (합격) | 합격: 270개 | 실패: 0개 | 경고: 0개 (소요 시간: 0.91초)`
  - Tier 1 (파일 실재성 & 0-byte 방지): 31 PASS
  - Tier 2 (시맨틱 구조 & 링크 무결성): 140 PASS
  - Tier 3 (클라이언트 인터랙션 & 테마 무결성): 13 PASS
  - Tier 4 (실서버 환경 E2E 크롤링): 86 PASS
- **명령어**: `python3 -m unittest scripts/test_verify_portfolio.py`
  - **결과**: `Ran 8 tests in 0.893s | OK`

### ② 4대 핵심 아키텍처 패턴 반영 실측 관찰
1. **원장과 예상값의 엄격한 분리 (Fact vs Prediction)**
   - 파일: `projects/beauty-brand-crm.html` (라인 46-48, 66-82, 114-124)
   - 인용: `"기록(Actual Fact)과 예상값(Predicted Value)을 분리하지 않으면, 계산으로 나온 관심 상품이 실제 구매처럼 보이고 실적은 왜곡된다."`
   - 실제 구현: 결제/주문 사실(Fact)과 AI 재구매 예측(Prediction)을 스키마 및 화면에서 물리적으로 격리. 조회 실패 건을 '미주문'으로 오인하지 않는 상태 격리 및 5단계 발송 안전 관문(Guardrails) 파이프라인 수록.
2. **스냅샷 패턴 (Snapshot Pattern)**
   - 파일: `projects/multi-branch-studio-erp.html` (라인 47-49, 78-83, 98-122), `projects/military-meal-management.html` (라인 47-49, 77-82, 97-123)
   - 인용: `"시급이나 단가가 바뀌더라도 과거 제출된 근무 기록과 보정 접수 원장은 제출 시점의 스냅샷 금액으로 영구 고정되어야 회계가 틀어지지 않는다."`
   - 실제 구현: `appliedHourlyRate`, `totalWage`를 제출 시점의 불변 스냅샷으로 원장에 복제/박제하여 이후 마스터 테이블의 시급이 인상되어도 과거 급여 장부가 변하지 않도록 보장하는 `prisma.$transaction` 코드 수록.
   - 군부대 ERP: 식권 신청 당시의 단가 스냅샷 영구 보존 및 식권 양도 시 사용권만 이전하고 원래 결제 대상자(`payer_id`)를 보존하는 회계 모델 반영.
3. **멱등성(Idempotency)과 폭주 방지 (Catch-up Storm Prevention)**
   - 파일: `projects/beauty-band-automation.html` (라인 47-49, 78-82, 97-123), `projects/sms-automation-review.html` (라인 46-48, 78-83, 98-120)
   - 인용: `"발송 요청 성공과 고객 수신은 다르며, 예약 식별자별 독립적인 멱등성 플래그가 없으면 네트워크 재시도는 즉시 고객 불만 폭탄으로 돌아온다."`
   - 실제 구현: BAND 자동화에서 PC 절전 모드 복구 시 10분 초과 작업 자동 만료/폐기(`TimeSpan.FromMinutes(10)` 초과 검사), SMS 자동화에서 3대 독립 상태 플래그(`is_confirmed_sent`, `is_remind_2h_sent`, `is_review_req_sent`)를 통한 중복 발송 원천 방지 및 실패 시 안전 재평가 로직 구현.
4. **프라이버시 바이 디자인 (Privacy by Design)**
   - 파일: `projects/kakaotalk-unread-excel.html` (라인 47-49, 78-83, 98-116, 126-130)
   - 인용: `"개인정보 보호의 가장 확실한 방법은 민감 데이터를 암호화해 보관하는 것이 아니라, 애초에 수집하지 않고 메모리 밖으로 내보내지 않는 '프라이버시 바이 디자인'이다."`
   - 실제 구현: 대화방 원본 DB를 직접 건드리지 않는 SQLite 로컬 읽기 전용 복사본(Shadow Snapshot) 생성. 대화 본문, 사용자 식별자, 채팅방 키, 로컬 프로필 경로를 일절 수집하지 않고 검증된 1:1 대화방 표시 이름과 수정 여부만 엑셀로 추출하는 설계 수록.

### ③ 백링크 및 네비게이션 정합성 관찰
- 14개 프로젝트 HTML 파일 전수 검사 결과:
  - 헤더 nav 링크: `<a href="../index.html#project">Project</a>` (14/14 파일 일치)
  - 상단 백링크: `<a href="../index.html#project" class="back-link">← Project</a>` (14/14 파일 일치)
  - 하단 백링크: `<a href="../index.html#project" class="back-link">← Back to Project</a>` (14/14 파일 일치)
- 메인 `index.html` 내 앵커:
  - 라인 66: `<section class="home-projects" id="project" aria-labelledby="project-title">` 존재 확인. 상세 페이지에서 클릭 시 메인 페이지의 `#project` 섹션으로 정확히 이동함.
  - 라인 75, 81, 87, 93 등: 14개 프로젝트 항목 전체가 `./projects/<project_slug>.html`로 로컬 연결되어 잔존 Notion 링크 0건.

### ④ `theme.js` 테마 전환 및 FOUC(깜빡임) 방지 관찰
- `theme.js`:
  - `(() => { ... })();` 즉시 실행 함수(IIFE)로 전역 오염 방지.
  - 라인 39: `root.dataset.theme = isDark ? 'dark' : 'light';`로 `<html>` 태그의 `data-theme`을 즉시 동기 설정.
  - 라인 18-25: `localStorage.getItem`을 try-catch로 감싸 시크릿 모드 예외 완벽 방어.
  - 라인 29: `window.matchMedia('(prefers-color-scheme: light)')` 지원 및 리스너 등록.
- 14개 프로젝트 및 `index.html`:
  - 모든 파일의 `<head>` 내부 상단(라인 9 및 라인 20)에 동기 스크립트 `<script src="../theme.js"></script>`로 로드됨.
  - `<body>`가 파싱되기 전에 `data-theme`이 세팅되므로 브라우저가 첫 페인트(Paint)부터 올바른 CSS 변수를 적용하여 깜빡임(FOUC)이 전혀 없음.

---

## 2. 논리적 추론 체계 (Logic Chain)

1. **테스트 도구의 무결성 (Integrity of Test Suite)**:
   - 관찰 ①에서 `verify_portfolio.py`가 270개 항목을 0.91초만에 통과시켰습니다.
   - 소스코드 감사 결과: 이 스크립트는 가짜 PASS나 하드코딩된 결과를 반환하는 것이 아니라, `html.parser.HTMLParser`를 상속한 실제 파서로 HTML DOM을 파싱하고, `ThreadingHTTPServer`를 백그라운드 스레드로 기동하여 86개의 실서버 HTTP GET 200 OK 및 가상 404 음성 테스트를 실측 수행하고 있습니다.
   - 따라서 이 테스트 결과는 완전히 신뢰할 수 있는 실측 증빙입니다.

2. **아키텍처 및 도메인 지식의 깊이 (Architectural Depth)**:
   - 관찰 ②에서 4대 아키텍처 패턴이 단순한 키워드 나열이 아니라, 각 프로젝트의 비즈니스 문제, 레거시 시스템의 결함, 이를 해결하기 위한 데이터 정합성 규칙, 그리고 실제 언어(Prisma/TypeScript, C#/.NET, Python, Rust)로 작성된 트랜잭션 코드 블록으로 구체화되어 있음을 확인했습니다.
   - 또한 14개 프로젝트 전체에 5대 표준 섹션(Overview, Problem & Integrity, Architecture & Flow, Key Features, Key Takeaways)과 노션에서 추출된 63개의 실제 고해상도 앱 스크린샷이 `<figure>`와 `<figcaption>` 시맨틱 태그로 완벽하게 렌더링되어 있습니다.

3. **사용자 경험 및 네비게이션 연속성 (UX Continuity)**:
   - 관찰 ③에서 상단과 하단의 모든 백링크가 `../index.html#project`를 가리키고, 메인 페이지에 정확히 `id="project"` 섹션이 매핑되어 있어 사용자가 프로젝트를 탐색하다가 언제든 메인 리스트의 원래 위치로 자연스럽게 복귀할 수 있습니다.

4. **성능 및 테마 신뢰성 (FOUC-Free Performance)**:
   - 관찰 ④에서 `theme.js`가 IIFE로 `<head>` 최상단에서 실행되도록 배치되어 브라우저 렌더링 파이프라인 상 DOM 구성 이전에 테마 속성이 확정됩니다. 이로써 새로고침이나 페이지 이동 시 흰색 화면이 번쩍이는 FOUC 현상이 원천 차단되었습니다.

---

## 3. 한계 및 고려사항 (Caveats)

- **초고해상도 다중 모니터 환경**: CSS 상 `max-width: 500px`로 Karri Saarinen의 단일 컬럼 가독성을 충실히 구현하였으므로, 4K 이상의 광폭 모니터에서도 정중앙에 편안한 독서 영역이 유지됩니다.
- **자바스크립트 비활성화 환경**: 클라이언트 브라우저에서 JS가 꺼져 있더라도, `style.css` 내부에 `@media (prefers-color-scheme: light)` fallback 룰이 정의되어 있어 시스템 설정에 맞는 미색 종이 테마가 정상 표현됩니다.
- 그 외 아키텍처, 링크, 테마, 테스트 무결성에 대한 결함은 없습니다 (No critical caveats).

---

## 4. 최종 결론 (Conclusion)

- **최종 판정**: **APPROVE (승인)**
- **평가 요약**:
  1. 14개 프로젝트의 4대 아키텍처 패턴(원장과 예상값 분리, 스냅샷 패턴, 멱등성, 프라이버시 바이 디자인) 및 도메인 모델링이 매우 깊이 있고 충실하게 구현되었습니다.
  2. 상단 및 하단 백링크가 `../index.html#project`로 100% 일치하며 메인 페이지의 `#project` 앵커와 완벽히 맞물립니다.
  3. `theme.js`가 `<head>` 상단에서 IIFE로 실행되어 FOUC 없이 다크/라이트 테마가 즉각 전환됩니다.
  4. 4-Tier 종합 검증(270/270 PASS)과 단위 테스트(8/8 PASS)가 무결하게 통과되었으며 어떠한 속임수나 하드코딩도 없습니다.

---

## 5. 독립적 검증 방법 (Verification Method)

다음 명령어로 누구든지 동일한 검증 결과를 즉시 재현할 수 있습니다:

```bash
# 1. 4-Tier 종합 E2E 무결성 검증 (엄격 모드)
python3 scripts/verify_portfolio.py --all --strict

# 2. 자체 단위 테스트 스위트 실행
python3 -m unittest scripts/test_verify_portfolio.py

# 3. 14개 프로젝트의 백링크 일치 여부 정규식 전수 확인
grep -n "href=\"\.\./index\.html#project\"" projects/*.html

# 4. theme.js 로드 위치 전수 확인
grep -n "theme\.js" projects/*.html index.html
```
