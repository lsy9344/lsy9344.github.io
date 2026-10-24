/**
 * theme.js - 초경량 다크/라이트 테마 제어 스크립트
 * 
 * 💡 초보 개발자를 위한 학습 포인트:
 * 1. IIFE (즉시 실행 함수 식): 전역 스코프 오염 방지
 * 2. matchMedia: 사용자의 OS 시스템 테마 설정 감지
 * 3. localStorage: 새로고침하거나 나중에 다시 방문해도 테마 유지
 * 4. dataset: <html data-theme="dark"> 속성을 조작하여 CSS 변수 전환
 * 5. 접근성(A11y): aria-pressed와 aria-label을 갱신해 스크린 리더 지원
 */

(() => {
  const root = document.documentElement;
  let systemPrefersLight;
  let userChoice;

  // 1. 기존에 사용자가 수동으로 저장한 테마가 있는지 확인
  try {
    const saved = localStorage.getItem('theme');
    if (saved === 'light' || saved === 'dark') {
      userChoice = saved;
    }
  } catch (e) {
    console.warn('localStorage 접근 실패:', e);
  }

  // 2. OS의 라이트모드 선호 여부 감지 미디어 쿼리
  try {
    systemPrefersLight = window.matchMedia('(prefers-color-scheme: light)');
  } catch (e) {
    console.warn('matchMedia 지원되지 않음:', e);
  }

  // 3. 현재 상태에 맞춰 <html> 태그와 버튼 아이콘 업데이트
  function applyTheme() {
    // 사용자가 선택한 값이 있으면 그 값을 우선, 없으면 시스템 설정에 따름
    const isDark = userChoice ? userChoice === 'dark' : !systemPrefersLight?.matches;

    root.dataset.theme = isDark ? 'dark' : 'light';

    const button = document.querySelector('[data-theme-toggle]');
    if (!button) return;

    button.setAttribute('aria-pressed', String(isDark));
    button.title = `Switch to ${isDark ? 'light' : 'dark'} mode`;

    const iconSpan = button.querySelector('[data-theme-icon]');
    if (iconSpan) {
      // 다크 모드일 땐 라이트로 전환할 수 있게 '해(☀︎)', 라이트 모드일 땐 '달(☾)' 표시
      iconSpan.textContent = isDark ? '☀︎' : '☾';
    }
  }

  // 초기 실행 (렌더링 깜빡임 최소화)
  applyTheme();

  // 4. DOM이 로드된 후 토글 버튼 클릭 이벤트 등록
  document.addEventListener('DOMContentLoaded', () => {
    applyTheme();

    const button = document.querySelector('[data-theme-toggle]');
    if (button) {
      button.addEventListener('click', () => {
        const currentTheme = root.dataset.theme;
        userChoice = currentTheme === 'dark' ? 'light' : 'dark';

        try {
          localStorage.setItem('theme', userChoice);
        } catch (e) {}

        applyTheme();
      });
    }
  });

  // 5. 사용자가 컴퓨터/휴대폰의 OS 설정을 바꿨을 때 실시간 반응
  const handleSystemChange = () => {
    if (!userChoice) {
      applyTheme();
    }
  };

  if (systemPrefersLight?.addEventListener) {
    systemPrefersLight.addEventListener('change', handleSystemChange);
  } else if (systemPrefersLight?.addListener) {
    systemPrefersLight.addListener(handleSystemChange);
  }
})();
