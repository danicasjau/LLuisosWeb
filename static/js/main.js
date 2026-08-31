/**
 * AE LLUÏSOS DE GRÀCIA - RETRO POSTER INTERACTIVITY & ENGINE
 */

document.addEventListener('DOMContentLoaded', () => {
  console.log("AE Lluïsos de Gràcia Web Engine Initialized");

  initNavHideToggle();
  //initNavAutoHide();
  initBarcode();
  initModalSystem();
  initCalendarViewer();
  initShopCart();

  setTimeout(handleHashExpansion, 300);
});

window.addEventListener('hashchange', handleHashExpansion);

/* ==========================================================================
   STATIC NAVIGATION MENU HIDE / SHOW TOGGLE
   ========================================================================== */
function initNavHideToggle() {
  const toggleBtn = document.getElementById('nav-hide-toggle');
  const navMenu = document.getElementById('main-nav');

  if (!toggleBtn || !navMenu) return;

  toggleBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    navMenu.classList.toggle('is-hidden');
    toggleBtn.classList.toggle('is-hidden-active');
  });
}

/* ==========================================================================
   AUTO-HIDE MENU ON INACTIVITY (5 SECONDS NO SCROLL)
   ========================================================================== */
function initNavAutoHide() {
  const navMenu = document.getElementById('main-nav');
  if (!navMenu) return;

  let scrollTimer = null;
  const HIDE_DELAY = 2000; // 5 seconds of inactivity

  function hideNav() {
    navMenu.classList.add('is-autohidden');
  }

  function showNav() {
    navMenu.classList.remove('is-autohidden');
  }

  function resetTimer() {
    showNav();
    if (scrollTimer) {
      clearTimeout(scrollTimer);
    }
    scrollTimer = setTimeout(hideNav, HIDE_DELAY);
  }

  // Listen to window scroll events to reveal menu and reset the 5-second timer
  window.addEventListener('scroll', resetTimer, { passive: true });

  // Pause auto-hide timer when user hovers over the navigation menu
  navMenu.addEventListener('mouseenter', () => {
    if (scrollTimer) clearTimeout(scrollTimer);
    showNav();
  });

  // Resume auto-hide timer when mouse leaves navigation menu
  navMenu.addEventListener('mouseleave', () => {
    resetTimer();
  });

  // Start initial 5-second timer on page load
  resetTimer();
}

/* ==========================================================================
   RETRO BARCODE GENERATOR
   ========================================================================== */
function initBarcode() {
  const barcodeContainer = document.getElementById('barcode-lines-container');
  if (!barcodeContainer) return;

  const pattern = [2, 1, 3, 1, 4, 1, 2, 2, 1, 3, 1, 1, 4, 2, 1, 3, 2, 1, 4, 1, 2, 1, 3, 1, 2, 4, 1, 2];
  barcodeContainer.innerHTML = '';

  pattern.forEach(width => {
    const bar = document.createElement('div');
    bar.className = 'barcode-bar';
    bar.style.width = `${width}px`;
    barcodeContainer.appendChild(bar);
  });
}

/* ==========================================================================
   MODAL POPUP SYSTEM
   ========================================================================== */
function initModalSystem() {
  const modalBackdrop = document.getElementById('retro-modal');
  const closeBtn = document.getElementById('modal-close-btn');

  if (!modalBackdrop) return;

  const closeModal = () => {
    modalBackdrop.classList.remove('active');
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });
}

function openModal(title, badge, dateLoc, content, imageSrc = null) {
  const modalBackdrop = document.getElementById('retro-modal');
  const titleEl = document.getElementById('modal-title');
  const badgeEl = document.getElementById('modal-badge');
  const metaEl = document.getElementById('modal-meta');
  const bodyEl = document.getElementById('modal-body');
  const imgEl = document.getElementById('modal-img');

  if (!modalBackdrop) return;

  titleEl.textContent = title;
  badgeEl.textContent = badge;
  metaEl.textContent = dateLoc;
  bodyEl.innerHTML = content;

  if (imageSrc && imgEl) {
    imgEl.src = imageSrc;
    imgEl.style.display = 'block';
  } else if (imgEl) {
    imgEl.style.display = 'none';
  }

  modalBackdrop.classList.add('active');
}

/* ==========================================================================
   CALENDAR EVENT TAP INTERACTIVITY
   ========================================================================== */
function initCalendarViewer() {
  const cells = document.querySelectorAll('.calendar-cell[data-event]');
  cells.forEach(cell => {
    cell.addEventListener('click', () => {
      const title = cell.getAttribute('data-title');
      const unit = cell.getAttribute('data-unit');
      const timeLoc = cell.getAttribute('data-timeloc');
      const desc = cell.getAttribute('data-desc');

      openModal(title, unit, timeLoc, `<p>${desc}</p>`);
    });
  });
}

/* ==========================================================================
   SHOPPING CART SYSTEM FOR BOTIGA
   ========================================================================== */
let cart = [];

function initShopCart() {
  const cartButtons = document.querySelectorAll('.btn-add-cart');
  const cartCounter = document.getElementById('cart-counter');

  cartButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = btn.getAttribute('data-id');
      const name = btn.getAttribute('data-name');
      const price = parseFloat(btn.getAttribute('data-price'));

      cart.push({ id, name, price });
      if (cartCounter) cartCounter.textContent = cart.length;

      showCartToast(`Afegit a la cesta: ${name}`);
    });
  });
}

function showCartToast(msg) {
  let toast = document.getElementById('cart-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'cart-toast';
    toast.style.cssText = `
      position: fixed;
      bottom: 25px;
      right: 25px;
      background: #FF5722;
      color: white;
      padding: 12px 20px;
      border: 1px solid rgba(18, 18, 18, 0.2);
      border-radius: 12px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      font-family: 'Space Grotesk', sans-serif;
      font-weight: 700;
      z-index: 2000;
      transition: all 0.3s ease;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';

  setTimeout(() => {
    toast.style.opacity = '0';
  }, 2500);
}

/* ==========================================================================
   HASH SHORTCUT AUTO-SCROLL (e.g. /#distinction-qui-som, /#qui-som)
   ========================================================================== */
function handleHashExpansion() {
  const hash = window.location.hash;
  if (!hash) return;

  const targetEl = document.querySelector(hash);
  if (targetEl) {
    targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

