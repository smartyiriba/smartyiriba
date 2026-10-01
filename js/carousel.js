(() => {
  'use strict';
  document.querySelectorAll('.group-slider').forEach(slider => {
    const slides = [...slider.querySelectorAll('.group-slide')];
    const dots = [...slider.querySelectorAll('.slider-dot')];
    if (slides.length < 2) return;
    const controls = slider.querySelector('.slider-controls');
    const play = slider.querySelector('[data-play]');
    const status = slider.querySelector('.slider-status');
    const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    let current = 0, timer, animation;
    let playing = !motion.matches, hovered = false, focused = false;
    controls.hidden = false;

    function schedule() {
      clearTimeout(timer);
      if (playing && !hovered && !focused && !document.hidden) timer = setTimeout(() => { show(current + 1, false); }, 6000);
      play.setAttribute('aria-label', slider.dataset[playing ? 'pauseLabel' : 'playLabel']);
      play.setAttribute('data-playing', String(playing));
      play.querySelector('span').textContent = ''; 
    }
    function show(index, announce = true) {
      animation?.cancel();
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, i) => { slide.hidden = i !== current; });
      dots.forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === current)));
      if (!motion.matches && typeof slides[current].animate === 'function') {
        animation = slides[current].animate([{ opacity: .3 }, { opacity: 1 }], { duration: 350, easing: 'ease-out' });
      }
      const counter = slider.querySelector('.slider-counter');
      if (counter) counter.textContent = `${String(current + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
      if (announce) status.textContent = `${current + 1} / ${slides.length} — ${slides[current].querySelector('figcaption').textContent}`;
      schedule();
    }
    function manual(index) { playing = false; show(index); }
    slider.querySelector('[data-previous]').addEventListener('click', () => manual(current - 1));
    slider.querySelector('[data-next]').addEventListener('click', () => manual(current + 1));
    dots.forEach((dot, i) => dot.addEventListener('click', () => manual(i)));
    play.addEventListener('click', () => { playing = !playing; schedule(); });
    slider.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault(); manual(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    slider.addEventListener('pointerenter', () => { hovered = true; schedule(); });
    slider.addEventListener('pointerleave', () => { hovered = false; schedule(); });
    // Stop automatic changes when keyboard focus enters; resume only on Play.
    slider.addEventListener('focusin', () => { focused = true; playing = false; schedule(); });
    slider.addEventListener('focusout', event => {
      if (!slider.contains(event.relatedTarget)) { focused = false; schedule(); }
    });
    document.addEventListener('visibilitychange', schedule);
    motion.addEventListener('change', () => {
      if (motion.matches) { playing = false; animation?.cancel(); }
      schedule();
    });
    schedule();
  });
})();
