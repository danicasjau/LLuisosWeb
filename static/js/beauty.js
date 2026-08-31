/**
 * AE LLUÏSOS DE GRÀCIA - BEAUTY ENGINE (beauty.js)
 * Tracks scroll amount, manages 3D Parallax hero title docking to top bar at 200px scroll,
 * controls the 5 Top Bar Index Apartats, and provides smooth interactive navigation.
 */

(function () {
  'use strict';

  const SCROLL_THRESHOLD = 1000;
  let ticking = false;

  document.addEventListener('DOMContentLoaded', () => {
    console.log("⛰️ Beauty Engine Initialized - Scroll tracker & parallax title manager active");

    initScrollTracker();
    initTopBarApartats();
    initEquipCapsScroll();
  });

  /**
   * Tracks window scroll amount.
   * If scroll amount >= 200px:
   *  - Adds '.is-topbar' and '.topbar-mode' classes to title, header and body
   * If scroll amount < 200px:
   *  - Reverts title to centered static hero state
   */
  function initScrollTracker() {
    const titleEl = document.querySelector('.poster-title-fill');
    const topBarEl = document.getElementById('main-top-bar');
    const heroEl = document.querySelector('.hero-poster-container');
    const apartatsNav = document.getElementById('topbar-apartats');

    function updateScrollState() {
      const scrollY = window.pageYOffset || document.documentElement.scrollTop || 0;

      if (scrollY >= SCROLL_THRESHOLD) {
        document.body.classList.add('topbar-mode');
        if (titleEl) titleEl.classList.add('is-topbar', 'title-on-topbar');
        if (topBarEl) topBarEl.classList.add('is-scrolled', 'topbar-docked');
        if (heroEl) heroEl.classList.add('hero-scrolled');
        if (apartatsNav) apartatsNav.classList.add('is-visible');
      } else {
        document.body.classList.remove('topbar-mode');
        if (titleEl) titleEl.classList.remove('is-topbar', 'title-on-topbar');
        if (topBarEl) topBarEl.classList.remove('is-scrolled', 'topbar-docked');
        if (heroEl) heroEl.classList.remove('hero-scrolled');
        if (apartatsNav) apartatsNav.classList.remove('is-visible');
      }

      ticking = false;
    }

    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateScrollState);
        ticking = true;
      }
    }, { passive: true });

    // Initial check on load
    updateScrollState();
  }

  /**
   * 5 Index Apartats Interactivity & Active Section Spy
   */
  function initTopBarApartats() {
    const navLinks = document.querySelectorAll('.topbar-apartat-link');
    const sections = ['qui-som', 'novetats', 'caps'];

    function checkActiveSection() {
      const scrollPos = window.scrollY + 250;

      sections.forEach(id => {
        const el = document.getElementById(id);
        if (!el) return;
        const top = el.offsetTop;
        const height = el.offsetHeight;

        if (scrollPos >= top && scrollPos < top + height) {
          navLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}` || link.getAttribute('href') === `/#${id}`) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }

    window.addEventListener('scroll', checkActiveSection, { passive: true });
  }

  /**
   * Equip de Caps Horizontal Scroll Carousel Controller
   * Adds mouse drag-to-scroll and arrow navigation buttons
   */
  function initEquipCapsScroll() {
    const track = document.getElementById('caps-scroll-track');
    const prevBtn = document.getElementById('caps-scroll-prev');
    const nextBtn = document.getElementById('caps-scroll-next');

    if (!track) return;

    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        track.scrollBy({ left: -340, behavior: 'smooth' });
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        track.scrollBy({ left: 340, behavior: 'smooth' });
      });
    }

    // Drag to scroll functionality
    let isDown = false;
    let startX;
    let scrollLeft;

    track.addEventListener('mousedown', (e) => {
      isDown = true;
      track.classList.add('is-dragging');
      startX = e.pageX - track.offsetLeft;
      scrollLeft = track.scrollLeft;
    });

    track.addEventListener('mouseleave', () => {
      isDown = false;
      track.classList.remove('is-dragging');
    });

    track.addEventListener('mouseup', () => {
      isDown = false;
      track.classList.remove('is-dragging');
    });

    track.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 1.5;
      track.scrollLeft = scrollLeft - walk;
    });
  }

})();
