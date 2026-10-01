const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {runInNewContext} = require('node:vm');
const script = readFileSync(require('node:path').join(__dirname, '../js/carousel.js'), 'utf8');
function setup(reduced = false) {
  const element = () => ({hidden:false, attrs:{}, events:{}, setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,fn){this.events[k]=fn;}});
  const slides = [0,1,2].map(i => ({...element(), hidden:i !== 0, querySelector:() => ({textContent:`Group ${i+1}`})}));
  const dots = slides.map(element), controls=element(),play=element(),previous=element(),next=element(),status=element(),icon={};
  play.querySelector=()=>icon;
  const slider = {...element(), dataset:{pauseLabel:'Pause',playLabel:'Play'}, contains:target=>target===play,
    querySelectorAll:selector=>selector==='.group-slide'?slides:dots,
    querySelector:selector=>({'.slider-controls':controls,'[data-play]':play,'.slider-status':status,'[data-previous]':previous,'[data-next]':next})[selector]};
  const motion={matches:reduced,addEventListener(k,fn){this.change=fn;}};
  const document={hidden:false,querySelectorAll:()=>[slider],events:{},addEventListener(k,fn){this.events[k]=fn;}};
  let pending;
  runInNewContext(script,{document,window:{matchMedia:()=>motion},setTimeout:fn=>{pending=fn;return 1;},clearTimeout:()=>{pending=undefined;}});
  return {slides,dots,play,previous,next,status,slider,motion,document,get pending(){return pending;}};
}
test('Automatic rotation wraps; manual controls stop rotation and announce the photo',()=>{
  const e=setup(); e.pending();assert.equal(e.slides[1].hidden,false);
  e.next.events.click();assert.equal(e.slides[2].hidden,false);assert.equal(e.pending,undefined);
  e.next.events.click();assert.equal(e.slides[0].hidden,false);assert.equal(e.dots[0].attrs['aria-pressed'],'true');
  assert.equal(e.status.textContent,'1 / 3 — Group 1');
  e.previous.events.click();assert.equal(e.slides[2].hidden,false);
});
test('Reduced motion, hover and a hidden page stop automatic rotation',()=>{
  const reduced=setup(true);assert.equal(reduced.pending,undefined);
  const e=setup();e.slider.events.pointerenter();assert.equal(e.pending,undefined);
  e.slider.events.pointerleave();assert.ok(e.pending);
  e.document.hidden=true;e.document.events.visibilitychange();assert.equal(e.pending,undefined);
  e.document.hidden=false;e.document.events.visibilitychange();assert.ok(e.pending);
  e.motion.matches=true;e.motion.change();assert.equal(e.pending,undefined);
});
test('Keyboard arrows navigate and focus pauses playback until explicitly resumed',()=>{
  const e=setup();e.slider.events.focusin();assert.equal(e.pending,undefined);
  let prevented=false;e.slider.events.keydown({key:'ArrowRight',preventDefault(){prevented=true;}});
  assert.equal(prevented,true);assert.equal(e.slides[1].hidden,false);
  e.slider.events.focusout({relatedTarget:null});assert.equal(e.pending,undefined);
  e.play.events.click();assert.ok(e.pending);assert.equal(e.play.attrs['aria-label'],'Pause');
});
