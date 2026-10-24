/**
 * stealth-admin.js - 완전 은밀한(Stealth) 인라인 글 수정기
 * 
 * 💡 비밀번호 입력 숨김 트리거:
 * 1. 키보드로 화면 어디서든 '1234' 타이핑
 * 2. 상단 헤더 이름 'Noah' 더블클릭
 * 3. 하단 푸터 끝 마침표(.) 클릭
 * 
 * 💡 비밀번호 인증 후:
 * - 화면의 모든 텍스트(제목, About me, Notes on building, 블로그 글 등)를 직접 클릭해 수정
 * - 우측 하단 미니멀 [저장] 칩 클릭 또는 Cmd+S로 실제 html 파일에 영구 저장
 */

(() => {
  const DEFAULT_PASSCODE = '1234';
  let isEditing = false;
  let activePasscode = '';
  let typedBuffer = '';

  // 1. 히든 패스코드 모달 및 미니멀 저장 칩 주입
  function initStealthUI() {
    // 패스코드 모달
    const modal = document.createElement('div');
    modal.id = 'stealth-modal';
    modal.className = 'stealth-modal-overlay';
    modal.hidden = true;
    modal.style.display = 'none';
    modal.innerHTML = `
      <div class="stealth-modal-box">
        <div class="stealth-modal-title">Passcode</div>
        <form id="stealth-pass-form">
          <input type="password" id="stealth-pass-input" class="stealth-pass-input" placeholder="••••" autocomplete="off" />
          <div class="stealth-modal-buttons">
            <button type="button" id="stealth-cancel-btn" class="stealth-btn stealth-btn-subtle">취소</button>
            <button type="submit" class="stealth-btn stealth-btn-accent">확인</button>
          </div>
          <div id="stealth-err-msg" class="stealth-err-msg" style="display:none;">비밀번호 불일치</div>
        </form>
      </div>
    `;
    document.body.appendChild(modal);

    // 우측 하단 미니멀 플로팅 저장 칩
    const chip = document.createElement('div');
    chip.id = 'stealth-chip';
    chip.className = 'stealth-chip';
    chip.hidden = true;
    chip.style.display = 'none';
    chip.innerHTML = `
      <span class="stealth-chip-dot"></span>
      <span class="stealth-chip-label">Editing</span>
      <button type="button" id="stealth-add-bullet-btn" class="stealth-chip-btn" title="새 원칙 추가">+ 원칙</button>
      <button type="button" id="stealth-save-btn" class="stealth-chip-btn stealth-chip-save" title="저장 (Cmd+S)">저장</button>
      <button type="button" id="stealth-exit-btn" class="stealth-chip-btn" title="종료 (ESC)">&times;</button>
    `;
    document.body.appendChild(chip);

    // 토스트 알림
    const toast = document.createElement('div');
    toast.id = 'stealth-toast';
    toast.className = 'stealth-toast';
    toast.hidden = true;
    toast.style.display = 'none';
    document.body.appendChild(toast);

    bindEvents();
  }

  function showToast(msg) {
    const toast = document.getElementById('stealth-toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.hidden = false;
    toast.style.display = 'block';
    toast.classList.add('is-visible');
    setTimeout(() => {
      toast.classList.remove('is-visible');
      setTimeout(() => {
        toast.hidden = true;
        toast.style.display = 'none';
      }, 200);
    }, 2200);
  }

  // 모달 제어
  function showPassModal() {
    if (isEditing) {
      showToast('이미 수정 모드입니다. 우측 하단 [저장]을 누르세요.');
      return;
    }
    const modal = document.getElementById('stealth-modal');
    const input = document.getElementById('stealth-pass-input');
    const err = document.getElementById('stealth-err-msg');
    if (modal) {
      typedBuffer = '';
      modal.hidden = false;
      modal.style.display = 'flex';
      modal.classList.add('is-open');
      if (err) err.style.display = 'none';
      if (input) {
        input.value = '';
        setTimeout(() => input.focus(), 60);
      }
    }
  }

  function hidePassModal() {
    const modal = document.getElementById('stealth-modal');
    if (modal) {
      typedBuffer = '';
      modal.hidden = true;
      modal.style.display = 'none';
      modal.classList.remove('is-open');
    }
  }

  // 편집 모드 토글
  function toggleEditing(enable, passcode = '') {
    isEditing = enable;
    if (passcode) activePasscode = passcode;

    const chip = document.getElementById('stealth-chip');
    if (chip) {
      chip.hidden = !enable;
      chip.style.display = enable ? 'flex' : 'none';
      chip.classList.toggle('is-active', enable);
    }

    document.body.classList.toggle('stealth-editing-active', enable);

    // 수정 가능한 요소 선택자
    const editableSelectors = [
      '[data-content-body] p',
      '[data-content-body] li',
      '[data-content-body] h2',
      '.section-heading h2',
      '.project-title',
      '.project-desc',
      '.project-meta',
      '.archive-row .title',
      '.article-header h1',
      '.article-header .date',
      '.article blockquote',
      '.article h2',
      '.article p',
      '.article ul li',
      '.article figcaption'
    ];

    const editableElements = document.querySelectorAll(editableSelectors.join(', '));
    editableElements.forEach(el => {
      el.contentEditable = enable ? 'true' : 'false';
      el.spellcheck = false;
    });

    if (enable) {
      showToast('✏️ 수정 모드 켜짐! 글자를 직접 클릭해 타이핑하세요');
    }
  }

  // 현재 페이지의 파일 경로 계산
  function getCurrentTargetFile() {
    const pathname = window.location.pathname;
    if (pathname.includes('/projects/')) {
      const parts = pathname.split('/').filter(Boolean);
      return 'projects/' + parts[parts.length - 1];
    }
    return 'index.html';
  }

  // 실제 HTML 파일에 영구 저장
  async function saveToDisk() {
    const saveBtn = document.getElementById('stealth-save-btn');
    if (saveBtn) saveBtn.textContent = '저장 중...';

    // 1) 편집 모드 일시 해제하여 순수 DOM 캡처
    toggleEditing(false);

    // 2) 주입된 요소 제거한 클론 생성
    const clone = document.documentElement.cloneNode(true);
    const injected = clone.querySelectorAll('#stealth-modal, #stealth-chip, #stealth-toast');
    injected.forEach(el => el.remove());

    clone.querySelectorAll('[contenteditable]').forEach(el => {
      el.removeAttribute('contenteditable');
      el.removeAttribute('spellcheck');
    });
    clone.body.classList.remove('stealth-editing-active');

    const cleanHtml = '<!doctype html>\n' + clone.outerHTML;
    const targetFile = getCurrentTargetFile();

    // 3) 백엔드 server.py에 저장 요청
    try {
      const resp = await fetch('/api/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          passcode: activePasscode || DEFAULT_PASSCODE,
          html: cleanHtml,
          file: targetFile
        })
      });
      const data = await resp.json();
      if (data.success) {
        showToast('✨ 파일에 영구 저장되었습니다!');
      } else {
        showToast('저장 실패: ' + (data.message || '오류'));
      }
    } catch (e) {
      // 오프라인 fallback
      localStorage.setItem('portfolio_saved_' + targetFile, cleanHtml);
      showToast('브라우저에 저장되었습니다 (오프라인 모드)');
    }

    // 편집 모드 복원
    toggleEditing(true, activePasscode);
    if (saveBtn) saveBtn.textContent = '저장';
  }

  // 새 원칙 추가
  function addBullet() {
    const ul = document.querySelector('[data-content-body] > ul, .article ul');
    if (!ul) return;
    const li = document.createElement('li');
    li.textContent = '새로운 원칙 또는 항목을 입력하세요.';
    li.contentEditable = 'true';
    ul.appendChild(li);
    li.focus();

    const range = document.createRange();
    range.selectNodeContents(li);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }

  // 이벤트 연결
  function bindEvents() {
    // 1. 비밀번호 제출
    const form = document.getElementById('stealth-pass-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const input = document.getElementById('stealth-pass-input');
        const err = document.getElementById('stealth-err-msg');
        const code = input ? input.value.trim() : '';

        let ok = false;
        if (code === DEFAULT_PASSCODE) {
          ok = true;
        } else {
          try {
            const res = await fetch('/api/verify', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ passcode: code })
            });
            const resData = await res.json();
            if (resData.success) ok = true;
          } catch {
            ok = (code === DEFAULT_PASSCODE);
          }
        }

        if (ok) {
          hidePassModal();
          toggleEditing(true, code);
        } else {
          if (err) err.style.display = 'block';
          if (input) {
            input.focus();
            input.select();
          }
        }
      });
    }

    // 모달 닫기 버튼들
    document.getElementById('stealth-cancel-btn')?.addEventListener('click', (e) => {
      e.preventDefault();
      hidePassModal();
    });

    document.getElementById('stealth-modal')?.addEventListener('click', (e) => {
      if (e.target.id === 'stealth-modal') {
        hidePassModal();
      }
    });

    // 2. 플로팅 칩 버튼들
    document.getElementById('stealth-save-btn')?.addEventListener('click', saveToDisk);
    document.getElementById('stealth-add-bullet-btn')?.addEventListener('click', addBullet);
    document.getElementById('stealth-exit-btn')?.addEventListener('click', () => {
      toggleEditing(false);
      showToast('수정 모드 종료');
    });

    // 3. 단축키 & 이스터에그 키스트로크
    window.addEventListener('keydown', (e) => {
      // ESC로 닫기
      if (e.key === 'Escape') {
        hidePassModal();
        if (isEditing) toggleEditing(false);
        return;
      }

      // Cmd+S 또는 Ctrl+S로 저장
      if (isEditing && (e.metaKey || e.ctrlKey) && (e.key === 's' || e.key === 'S')) {
        e.preventDefault();
        saveToDisk();
        return;
      }

      // 모달이 열려있거나 편집 중일 때는 이스터에그 버퍼 수집 건너뜀 (중복 루프 방지)
      const modal = document.getElementById('stealth-modal');
      const isModalOpen = modal && (!modal.hidden && modal.style.display !== 'none');
      if (isEditing || isModalOpen) {
        return;
      }

      // 인풋 필드 밖에서 키보드로 '1234' 타이핑 시 모달 자동 오픈!
      const activeTag = document.activeElement ? document.activeElement.tagName : '';
      if (!['INPUT', 'TEXTAREA'].includes(activeTag)) {
        typedBuffer += e.key;
        if (typedBuffer.length > 8) typedBuffer = typedBuffer.slice(-8);
        if (typedBuffer.includes('1234') || typedBuffer.includes('admin')) {
          typedBuffer = '';
          showPassModal();
        }
      }
    });

    // 4. 히든 클릭 트리거 1: 헤더 이름 'Noah' 더블클릭!
    const nameEl = document.querySelector('.site-header .name');
    if (nameEl) {
      nameEl.addEventListener('dblclick', (e) => {
        e.preventDefault();
        showPassModal();
      });
    }

    // 5. 히든 클릭 트리거 2: 하단 푸터 끝 마침표(.) 클릭!
    const footerSpan = document.querySelector('.site-footer span');
    if (footerSpan) {
      footerSpan.addEventListener('click', (e) => {
        const rect = footerSpan.getBoundingClientRect();
        if (e.clientX > rect.right - 25) {
          showPassModal();
        }
      });
      footerSpan.style.cursor = 'default';
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStealthUI);
  } else {
    initStealthUI();
  }
})();
