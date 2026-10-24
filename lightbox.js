/**
 * lightbox.js - 초경량 무결점 미니멀 이미지 줌 & 라이트박스
 * - figure img 또는 .zoomable 클릭 시 전체 화면으로 고해상도 확대
 * - ESC 키 또는 배경 클릭 시 부드럽게 닫힘
 */

(() => {
  function initLightbox() {
    let overlay = document.getElementById('global-lightbox');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'global-lightbox';
      overlay.className = 'lightbox-overlay';
      overlay.setAttribute('role', 'dialog');
      overlay.setAttribute('aria-modal', 'true');
      overlay.setAttribute('aria-label', 'Image preview');
      overlay.innerHTML = `
        <button type="button" class="lightbox-close" aria-label="닫기">&times;</button>
        <img class="lightbox-img" src="" alt="" />
        <div class="lightbox-caption"></div>
      `;
      document.body.appendChild(overlay);

      const closeBtn = overlay.querySelector('.lightbox-close');
      const img = overlay.querySelector('.lightbox-img');
      const caption = overlay.querySelector('.lightbox-caption');

      function closeLightbox() {
        overlay.classList.remove('is-active');
        document.body.style.overflow = '';
      }

      overlay.addEventListener('click', (e) => {
        if (e.target !== img) {
          closeLightbox();
        }
      });

      closeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        closeLightbox();
      });

      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && overlay.classList.contains('is-active')) {
          closeLightbox();
        }
      });
    }

    const overlayEl = overlay;
    const lightboxImg = overlayEl.querySelector('.lightbox-img');
    const lightboxCaption = overlayEl.querySelector('.lightbox-caption');

    // 페이지 내의 모든 대상 이미지에 줌 커서 및 클릭 이벤트 바인딩
    const targets = document.querySelectorAll('.zoomable, figure img, .minimal-shot figure img, .zen-section figure img');
    targets.forEach((img) => {
      img.classList.add('zoomable');
      img.title = '클릭하면 확대됩니다';
      img.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt || '확대 이미지';
        const labelText = img.alt || img.closest('figure')?.querySelector('figcaption')?.textContent || '';
        if (labelText) {
          lightboxCaption.textContent = labelText;
          lightboxCaption.style.display = 'block';
        } else {
          lightboxCaption.style.display = 'none';
        }
        overlayEl.classList.add('is-active');
        document.body.style.overflow = 'hidden';
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLightbox);
  } else {
    initLightbox();
  }
})();
