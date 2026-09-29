/**
 * AE LLUÏSOS DE GRÀCIA - SCROLL ANIMATIONS ENGINE
 * Dedicated JavaScript module for scroll-triggered entrance animations,
 * staggered reveals, and visual section transitions.
 */

document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initStaggeredCards();
  initParallaxDecorations();
});

/**
 * Initializes IntersectionObserver to trigger 'is-visible' class
 * on elements marked with '.animate-on-scroll' when they flow into view.
 */
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');

  if (!animatedElements.length) return;

  if (!('IntersectionObserver' in window)) {
    // Fallback for browsers without IntersectionObserver support
    animatedElements.forEach(el => el.classList.add('is-visible'));
    return;
  }

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -90px 0px',
    threshold: 0.12
  };

  const scrollObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        
        // Trigger any child staggered animations
        const children = entry.target.querySelectorAll('.stagger-child');
        children.forEach((child, index) => {
          setTimeout(() => {
            child.classList.add('is-visible');
          }, index * 90);
        });

        // Unobserve after initial entrance animation
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  animatedElements.forEach(el => {
    scrollObserver.observe(el);
  });
}

/**
 * Automatically assigns staggered animation delays to grid items
 */
function initStaggeredCards() {
  const gridContainers = document.querySelectorAll('.stagger-grid');
  
  gridContainers.forEach(container => {
    const items = container.children;
    Array.from(items).forEach((item, idx) => {
      item.classList.add('stagger-child');
      item.style.transitionDelay = `${idx * 0.08}s`;
    });
  });
}

/**
 * Subtle parallax tilt effect on section dividers during scroll
 */
function initParallaxDecorations() {
  const dividers = document.querySelectorAll('.section-divider-graphic');
  if (!dividers.length) return;

  window.addEventListener('scroll', () => {
    const scrolled = window.scrollY;
    dividers.forEach(div => {
      const speed = 0.05;
      const rect = div.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        div.style.transform = `translateY(${(rect.top * speed).toFixed(2)}px)`;
      }
    });
  }, { passive: true });
}
