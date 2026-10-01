(() => {
  'use strict';
  document.documentElement.classList.add('js-enabled');
  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const backToTop = document.querySelector('.back-to-top');
  const progress = document.querySelector('.reading-progress span');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  let ui = {
    menu_open: toggle?.getAttribute('aria-label'),
    menu_close: toggle?.dataset.closeLabel,
    back_to_top: backToTop?.getAttribute('aria-label'),
  };

  // Content is rendered from these same JSON dictionaries during the build.
  // Loading localized UI enhances the page; a failed request never hides content.
  const localeUrl = document.documentElement.dataset.localeUrl;
  if (localeUrl) {
    fetch(localeUrl)
      .then(response => {
        if (!response.ok) throw new Error(`Locale HTTP ${response.status}`);
        return response.json();
      })
      .then(dictionary => {
        if (!dictionary.ui) return;
        ui = { ...ui, ...dictionary.ui };
        if (toggle) toggle.setAttribute('aria-label', ui[toggle.getAttribute('aria-expanded') === 'true' ? 'menu_close' : 'menu_open']);
        if (backToTop) {
          backToTop.setAttribute('aria-label', ui.back_to_top);
          backToTop.title = ui.back_to_top;
        }
      })
      .catch(() => { /* The pre-rendered, localized HTML remains fully usable. */ });
  }

  function setMenu(open) {
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', ui[open ? 'menu_close' : 'menu_open']);
    navigation.classList.toggle('open', open);
  }
  if (toggle && navigation) {
    toggle.addEventListener('click', () => setMenu(toggle.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setMenu(false);
        toggle.focus();
      }
    });
    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) setMenu(false);
    });
    window.matchMedia('(min-width: 851px)').addEventListener('change', event => {
      if (event.matches) setMenu(false);
    });
  }

  // Small, one-time reveals use the native animation API. No content is hidden
  // by CSS or made dependent on JavaScript, JSON loading or observer support.
  let observer;
  if ('IntersectionObserver' in window && typeof Element.prototype.animate === 'function' && !reducedMotion.matches) {
    observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        if (reducedMotion.matches) continue;
        const animation = entry.target.animate(
          [{ opacity: 0, transform: 'translateY(14px)' }, { opacity: 1, transform: 'translateY(0)' }],
          { duration: 480, easing: 'cubic-bezier(.2,.65,.3,1)', delay: Number(entry.target.dataset.revealDelay || 0) },
        );
        animations.add(animation);
        animation.finished.catch(() => {}).finally(() => animations.delete(animation));
      }
    }, { threshold: 0.08 });
    document.querySelectorAll('.hero-grid > div, .section-head, .card, .profile-grid, .book-grid, .source-card').forEach(element => {
      if (element.classList.contains('card')) {
        const siblings = [...element.parentElement.children];
        element.dataset.revealDelay = String((siblings.indexOf(element) % 3) * 60);
      }
      observer.observe(element);
    });
  }
  reducedMotion.addEventListener('change', event => {
    if (event.matches) {
      observer?.disconnect();
      for (const animation of animations) animation.cancel();
    }
  });

  let framePending = false;
  function updateScroll() {
    framePending = false;
    const maximum = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = maximum > 0 ? Math.min(1, Math.max(0, window.scrollY / maximum)) : 0;
    if (progress) progress.style.transform = `scaleX(${ratio})`;
    if (backToTop) backToTop.hidden = window.scrollY < 500;
    document.querySelector('header')?.classList.toggle('scrolled', window.scrollY > 16);
  }
  function scheduleScroll() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(updateScroll);
  }
  window.addEventListener('scroll', scheduleScroll, { passive: true });
  window.addEventListener('resize', scheduleScroll, { passive: true });
  window.addEventListener('load', scheduleScroll, { once: true });
  if ('ResizeObserver' in window) new ResizeObserver(scheduleScroll).observe(document.body);
  backToTop?.addEventListener('click', () => {
    document.querySelector('#main')?.focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: reducedMotion.matches ? 'instant' : 'smooth' });
  });
  updateScroll();
})();
