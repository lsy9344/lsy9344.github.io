# 🌿 Karri Saarinen 스타일 미니멀 포트폴리오 & 인라인 CMS

Linear의 공동 창업자이자 CEO인 **Karri Saarinen**의 개인 웹사이트([karrisaarinen.com](https://karrisaarinen.com/))와 **Arlan Marat**([arlan.me](https://arlan.me/))의 인터랙션을 융합하여 제작한 초경량 개인 포트폴리오 웹사이트입니다.

화려한 효과나 무거운 자바스크립트 프레임워크(React/Vue 빌드 환경 등) 없이, **순수 HTML5, CSS3, 바닐라 JavaScript, 초경량 Python 서버**로만 구축되어 빠르고 단단하며 유지보수가 쉽습니다.

---

## 📂 파일 구조

```text
ws_noah/
├── DESIGN.md           # 상세 디자인 철학 및 타이포그래피/그리드 시스템 가이드
├── README.md           # 프로젝트 안내 및 커스터마이징 가이드
├── index.html          # 메인 홈 페이지 (소개, 원칙, 프로젝트, 글 목록)
├── style.css           # Karri Saarinen & Arlan.me 융합 디자인 시스템 CSS
├── theme.js            # 시스템 연동 및 다크/라이트 테마 제어 스크립트
├── admin.js            # [NEW] 히든 비밀번호 인증 및 인라인 실시간 편집 CMS 스크립트
├── server.py           # [NEW] 정적 파일 서빙 + /api/save 디스크 자동 저장 파이썬 서버
├── images/             # 69장의 실제 앱 고해상도 구동 스크린샷 에셋 (총 86.91 MB)
└── projects/           # 14개의 독립된 심층 케이스 스터디 상세 페이지
```

---

## 🔐 히든 관리자 모드 (인라인 CMS) 사용법

Karri Saarinen 사이트의 상단 헤더에 있는 **`RSS`** 메뉴 자리에 **비밀번호 관리자 게이트**가 숨겨져 있습니다!

1. **관리자 모드 진입**:
   * 상단 헤더의 **`RSS`** 버튼을 클릭하거나, 키보드 단축키 **`Cmd + Shift + E`** (Windows: `Ctrl + Shift + E`)를 누릅니다.
2. **비밀번호 입력**:
   * 비밀번호 팝업이 뜨면 기본 비밀번호 **`1234`**를 입력하고 Enter를 누릅니다.
3. **실시간 인라인 편집 (WYSIWYG)**:
   * 상단에 `Edit Mode` 플로팅 바가 나타납니다.
   * `About me` 소개글, `Notes on building` 원칙 목록, 프로젝트 제목 등을 **메모장처럼 화면에서 마우스로 클릭하고 바로 타이핑하여 수정**할 수 있습니다!
   * 상단 바의 **`+ 새 원칙 추가`** 버튼을 누르면 새로운 점자(`⡢`) 불릿 항목이 즉시 생성됩니다.
4. **영구 저장 (Save)**:
   * 상단 우측의 **`[저장하기 (Save)]`** 버튼(또는 `Cmd + S`)을 누르면:
     1. 브라우저 `localStorage`에 즉각 저장되고,
     2. 파이썬 백엔드(`/api/save`)로 전송되어 **실제 `index.html` 파일 자체를 디스크에 영구 백업 및 갱신**합니다!
     3. 수정 전 원본 파일은 자동으로 `.backups/` 폴더에 타임스탬프와 함께 자동 백업됩니다.

---

## 🛠️ 비밀번호 변경 방법

`server.py` 파일의 상단을 열어 원하는 비밀번호로 변경할 수 있습니다:
```python
# server.py (Line 18)
ADMIN_PASSCODE_HASH = hashlib.sha256("원하는비밀번호".encode('utf-8')).hexdigest()
```

---

## 🚀 로컬 서버 실행

```bash
# 디스크 자동 저장을 지원하는 파이썬 CMS 서버 실행
python3 server.py
```
브라우저에서 [http://localhost:3000](http://localhost:3000) 접속.
