const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { runInNewContext } = require('node:vm');
const script = readFileSync(require('node:path').join(__dirname, '../js/site.js'), 'utf8');
function environment(reduce = false, failLocale = false) {
  function element(attrs = {}) {
    const classes = new Set();
    return {
      attrs, dataset: {}, style: {}, events: {}, hidden: true,
      getAttribute: key => attrs[key], setAttribute: (key, value) => { attrs[key] = value; },
      classList: { add: key => classes.add(key), contains: key => classes.has(key), toggle: (key, on) => on ? classes.add(key) : classes.delete(key) },
      addEventListener(type, callback) { this.events[type] = callback; },
      focus() { this.focused = true; },
      animate() { state.animationCount++; return { finished: Promise.resolve(), cancel() { state.cancelCount++; } }; },
    };
  }
  const state = { animationCount: 0, cancelCount: 0, observers: [], unobserved: [] };
  const toggle = element({ 'aria-expanded': 'false', 'aria-label': 'Open menu' });
  toggle.dataset.closeLabel = 'Close menu';
  const navigation = element(), top = element({ 'aria-label': 'Back to top' }), progress = element(), header = element(), main = element(), card = element();
  card.classList.add('card'); card.parentElement = { children: [card] };
  const elements = { '.menu-toggle': toggle, '#navigation': navigation, '.back-to-top': top, '.reading-progress span': progress, header, '#main': main };
  const root = element(); root.dataset.localeUrl = '/locales/en.json'; root.scrollHeight = 2000;
  const motion = { matches: reduce, addEventListener(type, fn) { this.listener = fn; } };
  const desktop = { matches: false, addEventListener(type, fn) { this.listener = fn; } };
  const window = { scrollY: 0, innerHeight: 1000, events: {}, matchMedia: query => query.includes('reduce') ? motion : desktop,
    addEventListener(type, fn) { this.events[type] = fn; }, scrollTo(options) { state.scroll = options; } };
  const document = { documentElement: root, body: {}, events: {}, querySelector: selector => elements[selector], querySelectorAll: () => [card], addEventListener(type, fn) { this.events[type] = fn; } };
  class Observer {
    constructor(fn) { this.callback = fn; state.observers.push(this); }
    observe() {} unobserve(target) { state.unobserved.push(target); } disconnect() { this.disconnected = true; }
  }
  const locale = { ui: { menu_open: 'Ouvrir', menu_close: 'Fermer', back_to_top: 'Retour' } };
  window.IntersectionObserver = Observer;
  runInNewContext(script, { window, document, Element: { prototype: { animate() {} } }, IntersectionObserver: Observer,
    fetch: () => failLocale ? Promise.reject(new Error('offline')) : Promise.resolve({ ok: true, json: () => Promise.resolve(locale) }),
    requestAnimationFrame: fn => fn(), Number, Set });
  return { state, toggle, navigation, top, progress, main, card, document, window, motion };
}
test('Menu and page remain usable when locale loading fails', async () => {
  const e = environment(false, true);
  await new Promise(resolve => setImmediate(resolve));
  e.toggle.events.click();
  assert.equal(e.toggle.attrs['aria-expanded'], 'true');
  assert.equal(e.toggle.attrs['aria-label'], 'Close menu');
  assert.equal(e.navigation.classList.contains('open'), true);
  e.document.events.keydown({ key: 'Escape' });
  assert.equal(e.toggle.attrs['aria-expanded'], 'false');
  assert.equal(e.toggle.focused, true);
});
test('JSON labels enhance UI and reading progress follows scrolling', async () => {
  const e = environment();
  await new Promise(resolve => setImmediate(resolve));
  e.toggle.events.click();
  assert.equal(e.toggle.attrs['aria-label'], 'Fermer');
  assert.equal(e.top.attrs['aria-label'], 'Retour');
  e.window.scrollY = 750; e.window.events.scroll();
  assert.equal(e.progress.style.transform, 'scaleX(0.75)');
  assert.equal(e.top.hidden, false);
  e.top.events.click();
  assert.equal(e.main.focused, true);
  assert.deepEqual({ ...e.state.scroll }, { top: 0, behavior: 'smooth' });
});
test('Reduced motion skips reveals and smooth scrolling', () => {
  const e = environment(true);
  assert.equal(e.state.observers.length, 0);
  assert.equal(e.state.animationCount, 0);
  e.top.events.click();
  assert.equal(e.state.scroll.behavior, 'instant');
});
test('Reveals run once and stop when reduced motion is enabled', () => {
  const e = environment();
  const observer = e.state.observers[0];
  observer.callback([{ isIntersecting: true, target: e.card }]);
  assert.equal(e.state.animationCount, 1);
  assert.equal(e.state.unobserved[0], e.card);
  e.motion.matches = true; e.motion.listener({ matches: true });
  assert.equal(observer.disconnected, true);
  assert.equal(e.state.cancelCount, 1);
});
