/**
 * AE Lluïsos de Gràcia - Automatic Horizontal Looping Carousel for Equip de Caps
 * Smoothly moves cards horizontally in an infinite loop with pause-on-hover and drag support.
 */

(function () {
  'use strict';

  function initCapsCarousel() {
    const track = document.getElementById('caps-scroll-track');
    if (!track) return;

    // Duplicate children to ensure seamless infinite looping
    const originalCards = Array.from(track.children);
    if (originalCards.length === 0) return;

    originalCards.forEach(card => {
      const clone = card.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    });

    let isHovered = false;
    let isDragging = false;
    let startX = 0;
    let scrollStart = 0;
    let animationFrameId = null;
    const scrollSpeed = 0.85; // Pixels per frame for a smooth continuous glide

    function getHalfScrollWidth() {
      return track.scrollWidth / 2;
    }

    function step() {
      if (!isHovered && !isDragging) {
        track.scrollLeft += scrollSpeed;
        const halfWidth = getHalfScrollWidth();
        if (track.scrollLeft >= halfWidth) {
          track.scrollLeft -= halfWidth;
        }
      }
      animationFrameId = requestAnimationFrame(step);
    }

    // Start auto-scroll
    animationFrameId = requestAnimationFrame(step);

    // Pause on hover / touch
    track.addEventListener('mouseenter', () => {
      isHovered = true;
    });

    track.addEventListener('mouseleave', () => {
      isHovered = false;
      isDragging = false;
      track.classList.remove('is-dragging');
    });

    // Touch support
    track.addEventListener('touchstart', () => {
      isHovered = true;
    }, { passive: true });

    track.addEventListener('touchend', () => {
      setTimeout(() => {
        isHovered = false;
      }, 1200);
    }, { passive: true });

    // Drag to scroll functionality
    track.addEventListener('mousedown', (e) => {
      isDragging = true;
      track.classList.add('is-dragging');
      startX = e.pageX - track.offsetLeft;
      scrollStart = track.scrollLeft;
    });

    window.addEventListener('mouseup', () => {
      if (isDragging) {
        isDragging = false;
        track.classList.remove('is-dragging');
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDragging) return;
      e.preventDefault();
      const x = e.pageX - track.offsetLeft;
      const walk = (x - startX) * 1.5;
      track.scrollLeft = scrollStart - walk;

      const halfWidth = getHalfScrollWidth();
      if (track.scrollLeft >= halfWidth) {
        track.scrollLeft -= halfWidth;
        scrollStart -= halfWidth;
      } else if (track.scrollLeft <= 0) {
        track.scrollLeft += halfWidth;
        scrollStart += halfWidth;
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCapsCarousel);
  } else {
    initCapsCarousel();
  }
})();
