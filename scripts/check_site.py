"""Validate generated pages and their local destinations without dependencies."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
ROOT=Path(__file__).resolve().parents[1]
class Page(HTMLParser):
 def __init__(self,path):super().__init__();self.path=path;self.refs=[];self.ids=set();self.tags=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id' in a:self.ids.add(a['id'])
  for k in ('href','src','data-locale-url'):
   if a.get(k,'').startswith(('/','#')):self.refs.append(a[k])
  if tag=='img':
   assert 'alt' in a and int(a['width'])>0 and int(a['height'])>0,self.path
   for variant in a.get('srcset','').split(','):
    if variant.strip():self.refs.append(variant.strip().split()[0])
files=[ROOT/'index.html',*sorted((ROOT/'fr').glob('*.html')),*sorted((ROOT/'en').glob('*.html'))]
pages={}
for p in files:
 page=Page(p);page.feed(p.read_text());pages[p]=page
for p,page in pages.items():
 for ref in page.refs:
  url=urlsplit(ref);target=ROOT/url.path.lstrip('/') if url.path else p
  assert target.is_file(),f'{p}: missing {ref}'
  if url.fragment:assert url.fragment in pages[target].ids,f'{p}: missing anchor {ref}'
 attrs=page.tags
 assert any(t=='html' and a.get('lang') in ('fr','en') for t,a in attrs)
 assert any(t=='meta' and a.get('name')=='description' for t,a in attrs)
 assert any(t=='link' and a.get('rel')=='canonical' for t,a in attrs)
 assert {a['hreflang'] for t,a in attrs if t=='link' and 'hreflang' in a}>={'fr','en'}
 assert '<title>' in p.read_text()
 assert 'mailto:contact@smartyiriba.org' in p.read_text(), f'{p}: missing institutional email'
for entry in json.loads((ROOT/'images/web/manifest.json').read_text()):
 for variant in entry['variants']:assert (ROOT/variant['path']).is_file()
print(f'OK: {len(files)} pages; links, anchors, srcset, images, language and SEO metadata; image manifest.')

# Both locale dictionaries must have the same topology and no empty translation.
locales = {lang: json.loads((ROOT / 'locales' / (lang + '.json')).read_text()) for lang in ('fr', 'en')}
def compare_locales(a, b, key='root'):
    assert type(a) == type(b), f'Locale type mismatch at {key}'
    if isinstance(a, dict):
        assert a.keys() == b.keys(), f'Locale keys differ at {key}'
        for name in a: compare_locales(a[name], b[name], key + '.' + name)
    elif isinstance(a, list):
        assert len(a) == len(b), f'Locale lengths differ at {key}'
        for i, pair in enumerate(zip(a, b)): compare_locales(*pair, key + '.' + str(i))
    elif isinstance(a, str):
        assert a.strip() and b.strip(), f'Empty translation at {key}'
compare_locales(locales['fr'], locales['en'])
for lang, slug in [('fr', 'gouvernance'), ('en', 'governance')]:
    content = (ROOT / lang / (slug + '.html')).read_text()
    governance = locales[lang]['governance']
    assert len(governance['organs']) == 3 and len(governance['roles']) == 6
    for item in governance['organs']: assert item['title'] in content
    for name in governance['founders']: assert name in content
    assert 'documents/statut-Smart-YIRIBA-2018.pdf' in content
    assert 'Abou-hassane-cisse-640w.webp' in content and 'publication-couverture-23-640w.webp' in content
    assert f'data-locale-url="/locales/{lang}.json"' in content
print('OK: locale parity; 3 statutory organs, 6 board roles, founders, source PDF, portrait and book in FR/EN.')

for lang in ('fr', 'en'):
    content = (ROOT / lang / 'contact.html').read_text()
    for email in ('contact@smartyiriba.org', 'rejoindre@smartyiriba.org', 'aboulhassane@smartyiriba.org', 'swa@smartyiriba.org'):
        assert 'href="mailto:' + email + '"' in content
print('OK: four requested email links on both Contact pages and institutional email in every footer.')

# The twelve home-gallery photos are exclusive to this section (shared FR/EN translations).
manifest = json.loads((ROOT / 'images/web/manifest.json').read_text())
for lang in ('fr', 'en'):
    selection = [item['image'] for item in locales[lang]['photo_galleries']['home']['photos']]
    assert len(selection) == len(set(selection)) == 12, 'Home gallery must contain twelve different photos'
    for index in selection:
        source = '/' + manifest[index]['variants'][-1]['path']
        for path, page in pages.items():
            uses = sum(tag == 'img' and attrs.get('src') == source for tag, attrs in page.tags)
            assert uses == (1 if path.name == 'index.html' else 0), f'{path}: gallery photo reused or missing: {source}'
print('OK: twelve distinct home-gallery photos, absent from other pages and home sections.')
