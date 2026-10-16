const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#main-nav');
if (toggle && nav) {
  toggle.hidden = false;
  document.documentElement.classList.add('js');
  const close = () => { toggle.setAttribute('aria-expanded', 'false'); nav.classList.remove('is-open'); };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open)); nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('keydown', event => { if (event.key === 'Escape') { close(); toggle.focus(); } });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', close));
}
