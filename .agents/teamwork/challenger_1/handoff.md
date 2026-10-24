# Handoff Report — Challenger 1 (에셋 및 404 링크 적대적 검증)

- **작성자**: Challenger 1 (적대적 검증 전문 에이전트)
- **작성일시**: 2026-10-21T19:43:00Z
- **수신자**: Orchestrator (`078608ad-aa6c-458a-875b-2187c76d3e60`)
- **최종 판정**: **APPROVE (조건부/권고사항 포함 승인)**

---

## 1. Observation (직접 관찰한 사실)

독립적인 검증 파이썬 스크립트를 작성하여 18개 전체 HTML 문서와 69개 로컬 이미지 에셋에 대해 적대적 전수 검사를 실행한 직접 관찰 결과는 다음과 같습니다.

### (1) 이미지 태그 및 물리 파일 실재성 100% 역추적 검사
- 대상: 전체 18개 HTML (`index.html`, `projects/*.html` 14개, `posts/*.html` 3개)
- HTML 파서(`html.parser.HTMLParser`) 및 정규식(`re.findall`) 병렬 추출 결과:
  - `index.html`: `<img>` 태그 **0개**
  - `posts/*.html` (3개): `<img>` 태그 **0개**
  - `projects/*.html` (14개): 총 **69개** `<img>` 태그 발견
    - `beauty-band-automation.html`: 6개
    - `beauty-brand-crm.html`: 6개
    - `beauty-erp-inventory.html`: 5개
    - `beauty-review-platform.html`: 5개
    - `boothy-photo-booth.html`: **0개** (의도된 텍스트/아키텍처 전용)
    - `cuteditor-photo-tool.html`: 5개
    - `kakaotalk-unread-excel.html`: 6개
    - `military-meal-management.html`: 5개
    - `multi-branch-studio-erp.html`: 5개
    - `multimarket-crawler.html`: 6개
    - `seafood-distribution-erp.html`: 5개
    - `sms-automation-review.html`: 5개
    - `tactrun-delivery-landing.html`: 5개
    - `vietnam-aesthetic-erp.html`: 5개
- **물리 파일 존재 여부**: 69개 상대 경로(`../images/<slug>/<file>.png`) 모두 파일시스템에 실재함 (누락/404 발생 **0건**).
- **고아 파일(Orphan Files) 검사**: `images/` 폴더 내 물리 파일 69개와 HTML 참조 69개가 1:1로 완벽히 일치 (사용되지 않는 방치 이미지 **0개**).

### (2) Linux 배포 대비 파일시스템 대소문자(Case-Sensitivity) 전수 검사
- macOS는 기본적으로 대소문자를 구분하지 않는(Case-insensitive, Case-preserving) 파일시스템(APFS/HFS+)을 사용하므로, `Path.exists()`만으로는 Linux(ext4) 서버 배포 시 발생하는 404 대소문자 오류를 발견할 수 없습니다.
- 각 디렉토리 경로에 대해 `os.listdir()`의 실제 디스크 엔트리와 문자열을 바이트 단위로 대조:
  - 검사 결과: **69개 이미지 경로 모두 디렉토리명 및 파일명의 대소문자가 디스크와 100% 정확히 일치함** (대소문자 불일치 **0건**).

### (3) 파일 크기 및 매직 바이트(Magic Bytes) 전수 검증
- `images/` 하위 69개 파일 전체 용량 검사:
  - 최소 크기: `247,538 바이트 (241.7 KB)` (`images/beauty-erp-inventory/jena-portfolio-overview.png`)
  - 최대 크기: `2,318,329 바이트 (2.21 MB)` (`images/beauty-review-platform/02_review_readiness_flow.png`)
  - 0바이트 빈 파일 또는 1KB 미만 스켈레톤 더미 파일: **0건**.
- **매직 바이트(Magic Bytes) 검사 결과**:
  - **56개 파일**: 표준 PNG 매직 바이트(`89 50 4E 47 0D 0A 1A 0A` / `\x89PNG\r\n\x1a\n`)와 올바른 `IHDR` 및 `IEND` 청크 보유.
  - **13개 파일 (`*-portfolio-overview.png`)**:
    - 파일 확장자는 `.png`이나, 실제 파일 헤더가 JPEG 매직 바이트(`FF D8 FF E0 00 10 4A 46` / JFIF) 및 JPEG 종료 바이트(`FF D9`)로 확인됨!
    - 해당 13개 파일 목록:
      1. `images/beauty-band-automation/jena_band-portfolio-overview.png`
      2. `images/beauty-erp-inventory/jena-portfolio-overview.png`
      3. `images/beauty-review-platform/jena_review-portfolio-overview.png`
      4. `images/crm/jena_crm_portfolio_overview.png`
      5. `images/cuteditor-photo-tool/cuteditor-portfolio-overview.png`
      6. `images/kakaotalk-unread-excel/sft_kakao_chat_detect-portfolio-overview.png`
      7. `images/military-meal-management/military_meal_sys-portfolio-overview.png`
      8. `images/multi-branch-studio-erp/erp_dabi-portfolio-overview.png`
      9. `images/multimarket-crawler/sft_gmarket-portfolio-overview.png`
      10. `images/seafood-distribution-erp/erp_fish-portfolio-overview.png`
      11. `images/sms-automation-review/n-smsauto-portfolio-overview.png`
      12. `images/tactrun-delivery-landing/ws_tactrun-portfolio-overview.png`
      13. `images/vietnam-aesthetic-erp/vietnam_massage-portfolio-overview.png`
- **PIL(Pillow) 디코딩 무결성 검증 (`Image.open().verify()`)**:
  - 69개 파일 전체 디코딩 성공, 이미지 손상(Corruption) **0건**.
  - 13개 overview 파일은 실제 JPEG 포맷으로 완벽히 렌더링 가능한 유효 이미지임이 검증됨.

### (4) Boothy 무인사진관 (`projects/boothy-photo-booth.html`) 검증
- `projects/boothy-photo-booth.html` 내 `<img>`, `<picture>`, `<svg>` 태그: **0개**.
- 깨진 이미지 링크나 빈 박스 없음.
- 이미지 대신 고품질 텍스트 아키텍처 다이어그램(`<pre><code>`)과 Rust 세션 상태 머신 코드가 배치되어 노션 원본(이미지 0개)의 명세를 정갈하게 충족함.

### (5) 시맨틱 마크업 및 접근성 (`<figure>`, `<figcaption>`, `alt`)
- 14개 프로젝트 내 69개 이미지 전량:
  - `<figure>` 태그 안에 정확히 1개의 `<img>`와 1개의 `<figcaption class="caption">`이 쌍을 이루고 있음.
  - 모든 `<img>` 태그에 빈 문자열이 아닌 구체적이고 설명적인 `alt` 속성이 100% 부여됨.

### (6) 내부 하이퍼링크 및 앵커(#id) 전수 검사
- `index.html` -> 14개 프로젝트 링크: 14개 전량 유효 (`./projects/<slug>.html`).
- 14개 프로젝트 -> `index.html` 백링크: 14개 페이지 모두 `../index.html#project`로 정확히 연결되며 `index.html` 내 `<section id="project">`가 실재함.
- **[발견 사항] 레거시 블로그 포스트(`posts/*.html`) 내 앵커 불일치 발견**:
  - `posts/building-a-lightweight-markdown-editor.html` (19번 줄): `<a href="../index.html#work">Work</a>` -> `index.html`에 `#work` ID 부재.
  - `posts/why-i-choose-simplicity.html` (19번 줄): `<a href="../index.html#work">Work</a>` -> `index.html`에 `#work` ID 부재.
  - `posts/why-craftsmanship-matters.html` (20번 줄): `<a href="../index.html#projects">Work</a>` -> `index.html`에 `#projects` ID 부재 (실제 ID는 단수형 `#project`).

---

## 2. Logic Chain (논리적 추론 체인)

1. **[관찰 1 & 2] 에셋 100% 실재성과 404 부재**:
   - 14개 프로젝트의 69개 이미지 경로가 상대 경로 해석 및 대소문자 검사를 모두 통과함.
   - 따라서 로컬 정적 사이트로서 어떠한 페이지에서도 깨진 이미지(엑스박스/404)가 렌더링되지 않음.
2. **[관찰 3] 확장자-매직 바이트 불일치(JPEG in PNG)에 대한 기술적 분석**:
   - **발생 원인**: 노션 S3 원본 저장소에서 조감도 이미지가 JPEG로 압축된 파일이었으나, 노션 다운로드 스크립트 또는 원본 파일명이 `.png`로 명명되어 로컬에 그대로 저장됨.
   - **실제 영향도 평가**:
     - *브라우저 환경*: 최신 웹 브라우저는 파일 확장자가 아닌 바이너리 앞부분(MIME Sniffing)을 읽어 포맷을 판단하므로, 사용자가 웹사이트를 볼 때는 아무런 문제 없이 고해상도로 렌더링됨.
     - *잠재적 리스크*: 엄격한 MIME 검증을 수행하는 프록시나 이미지 압축 CLI 툴에서는 경고를 발생시킬 수 있음.
   - **판단**: 현재 HTML 코드와 파일시스템의 파일명이 1:1로 일치하여 404가 발생하지 않으며, 이미지 자체도 손상되지 않은 정상 파일이므로 사이트 기능 동작을 차단(Block)할 수준의 치명적 결함은 아님.
3. **[관찰 4] Boothy 무인사진관 구현의 정합성**:
   - 원본 노션에 이미지가 전혀 없었던 제약 조건을 왜곡하지 않고, 불필요한 가짜 이미지를 넣지 않은 채 아키텍처 다이어그램으로 충실하게 대체하여 무결성 원칙을 준수함.
4. **[관찰 6] posts 폴더의 앵커 불일치**:
   - 금번 태스크의 핵심 범위는 14개 프로젝트 케이스 스터디 페이지(`projects/*.html`) 제작 및 `index.html` 연결임.
   - 14개 프로젝트 페이지의 백링크(`../index.html#project`)는 완벽히 작동하나, 기존에 존재하던 3개의 글(`posts/*.html`)에서 `index.html`의 프로젝트 섹션을 가리키는 앵커가 구버전 ID(`#work`, `#projects`)로 남아있음.
   - 이는 금번 14개 프로젝트 작업으로 인해 발생한 리그레션은 아니지만, 향후 유지보수를 위해 수정이 권장되는 발견 사항임.

---

## 3. Caveats (주의사항 및 한계)

1. **JPEG/PNG 확장자 통일 관련**:
   - 13개 `*-portfolio-overview.png`의 파일명을 `.jpg`로 임의 변경할 경우, 이미 작성된 13개 HTML의 `<img src="...">` 경로도 함께 일괄 수정되어야 합니다. 그렇지 않으면 즉시 404 에러가 발생합니다. (현재는 양쪽 모두 `.png`로 일치되어 404가 발생하지 않는 상태임).
2. **블로그 포스트 영역 스코프**:
   - `posts/*.html` 파일은 이번 14개 포트폴리오 프로젝트 생성 작업의 직접적 대상은 아니었으나, 사이트 전체의 링크 무결성 검증 차원에서 적대적으로 발굴하여 리포트하였습니다.

---

## 4. Conclusion (최종 판정 및 결론)

### 최종 판정: **APPROVE (조건부/권고사항 포함 승인)**

1. **요구사항 충족**:
   - 14개 프로젝트의 69개 에셋 전수 역추적 100% 성공 (누락 0건).
   - 0바이트 빈 파일 0건, 손상된 파일 0건.
   - Boothy 무인사진관 0-image 및 시맨틱 코드 다이어그램 완벽 충족.
   - 14개 프로젝트 <-> 메인 페이지 간 링크 및 백링크 100% 정상 작동.
2. **권고사항 (Advisory Recommendations)**:
   - **권고 1 (포맷 정돈)**: 향후 필요 시 13개 `*-portfolio-overview.png` 파일을 실제 PNG로 무손실 변환하거나, 파일명을 `.jpg`로 바꾸고 HTML의 `src`를 일괄 업데이트할 것을 권장.
   - **권고 2 (앵커 링크 수정)**: `posts/*.html` 3개 문서의 네비게이션 헤더에 있는 `#work` 및 `#projects` 링크를 `../index.html#project`로 통일 수정할 것을 권장.

---

## 5. Verification Method (독립적 재검증 방법)

초보 개발자도 터미널에서 즉시 실행하여 동일한 결과를 확인할 수 있는 독립 재검증 명령어입니다.

### (1) 이미지 파일 실재성, 대소문자 및 404 누락 전수 검증 스크립트
```bash
python3 -c "
import os
from pathlib import Path
from html.parser import HTMLParser

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs = []
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            self.imgs.append(dict(attrs))

total, errors = 0, []
for p in Path('projects').glob('*.html'):
    parser = ImgParser()
    parser.feed(p.read_text(encoding='utf-8'))
    for img in parser.imgs:
        total += 1
        src = img.get('src', '')
        resolved = (p.parent / src).resolve()
        # 대소문자 및 존재 확인
        parts = Path(src).parts
        curr = p.parent.resolve()
        for part in parts:
            if part == '..': curr = curr.parent; continue
            if part not in os.listdir(curr):
                errors.append(f'{p.name}: {src} (불일치: {part})')
            curr = curr / part

print(f'검사한 총 이미지: {total}개 (기대값: 69개)')
print(f'발견된 경로 오류: {len(errors)}건')
"
```

### (2) 매직 바이트 및 0바이트/손상 검증 스크립트
```bash
python3 -c "
from pathlib import Path
from PIL import Image

checked, jpeg_in_png = 0, 0
for p in Path('images').glob('**/*'):
    if p.is_file():
        checked += 1
        with open(p, 'rb') as f:
            header = f.read(8)
            img = Image.open(p)
            img.verify() # 손상 검증
            if header.startswith(b'\xff\xd8\xff') and p.suffix.lower() == '.png':
                jpeg_in_png += 1

print(f'검사한 이미지 파일: {checked}개 (기대값: 69개)')
print(f'PNG 확장자 내 JPEG 헤더 파일: {jpeg_in_png}개 (기대값: 13개)')
print('모든 이미지가 PIL 손상 검사를 100% 통과했습니다.')
"
```
