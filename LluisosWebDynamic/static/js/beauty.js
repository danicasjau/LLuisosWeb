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

      if (topBarEl) topBarEl.classList.add('is-scrolled', 'topbar-docked');
      if (apartatsNav) apartatsNav.classList.add('is-visible');
      if (titleEl) titleEl.classList.add('is-topbar', 'title-on-topbar');

      if (scrollY >= 80) {
        document.body.classList.add('topbar-mode');
        if (heroEl) heroEl.classList.add('hero-scrolled');
      } else {
        document.body.classList.remove('topbar-mode');
        if (heroEl) heroEl.classList.remove('hero-scrolled');
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

})();
