"""Build the bilingual institutional website. Run from any directory with Python 3."""
from pathlib import Path
import json, html, hashlib, re
ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'images/web/manifest.json').read_text())
LOCALES = {lang: json.loads((ROOT / 'locales' / (lang + '.json')).read_text()) for lang in ('fr', 'en')}
def t(lang, key):
    return LOCALES[lang][key]

SLUGS = {lang: data['slugs'] for lang, data in LOCALES.items()}
LABELS = {lang: data['navigation'] for lang, data in LOCALES.items()}
INTRO = {lang: data['intro'] for lang, data in LOCALES.items()}
DOMAINS = {lang: data['domains'] for lang, data in LOCALES.items()}
SWA = {lang: data['smart_women_academy'] for lang, data in LOCALES.items()}

def asset(path):
    version = hashlib.sha256((ROOT / path.lstrip('/')).read_bytes()).hexdigest()[:10]
    return path + '?v=' + version

def esc(s):
    return html.escape(s, quote=True)

def link(lang, n):
    return f'/' + lang + '/' + SLUGS[lang][n] + '.html'

def photo(n, lang, eager=False, sizes="(max-width: 850px) 92vw, 900px"):
    e = manifest[n]
    v = e['variants']
    last = v[-1]
    alt = t(lang, 'image_alt').get(str(n), 'Activité de Smart YIRIBA' if lang == 'fr' else 'Smart YIRIBA activity')
    return f'''<img class="activity-photo" style="--photo-width:{last['width']}px" src="/{last['path']}" srcset="''' + ', '.join((f"/{x['path']} {x['width']}w" for x in v)) + f'''" sizes="{sizes}" width="{last['width']}" height="{last['height']}" alt="{esc(alt)}" ''' + ('fetchpriority="high"' if eager else 'loading="lazy"') + ' decoding="async">'

def section(title, body):
    return f'<section class="content-section"><h2>{title}</h2>{body}</section>'

def values_list(lang):
    drawings = [
        '<path d="M16 3 5 7v8c0 7 11 14 11 14s11-7 11-14V7L16 3Z"/><path d="m10 15 4 4 8-8"/>',
        '<circle cx="16" cy="8" r="3"/><circle cx="6" cy="14" r="3"/><circle cx="26" cy="14" r="3"/><path d="M10 18v-1a6 6 0 0 1 12 0v1M1 27v-4a5 5 0 0 1 10 0v4m10 0v-4a5 5 0 0 1 10 0v4"/>',
        '<path d="M11 22c0-3-5-5-5-10a10 10 0 0 1 20 0c0 5-5 7-5 10M11 22h10m-9 4h8m-7 3h6m-3-7v-9m-4-3 4 3 4-3"/>',
        '<rect x="6" y="6" width="20" height="23" rx="2"/><rect x="11" y="3" width="10" height="6" rx="2"/><path d="m11 18 3 3 7-7"/>',
        '<path d="m2 15 7-7 7 3 7-3 7 7-7 8-4 3-6-2-6-6m9-7-5 5 4 3 4-4 5 5M2 15l5 3m23-3-6 5m-11 4 3-3m3 5 3-3"/>',
        '<circle cx="15" cy="17" r="11"/><circle cx="15" cy="17" r="6"/><path d="m15 17 13-13m-5 0h5v5"/>',
    ]
    return '<ul class="values-grid">' + ''.join('<li><span class="domain-icon"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + icon + '</svg></span><span>' + esc(label) + '</span></li>' for label, icon in zip(t(lang, 'integrite'), drawings)) + '</ul>'

def ul(items):
    return '<ul>' + ''.join((f'<li>{i}</li>' for i in items)) + '</ul>'

def table(lang):
    rows = t(lang, 'legal_rows')
    return '<table><caption>' + t(lang, 'identite_institutionnelle') + '</caption><tbody>' + ''.join('<tr><th scope="row">' + esc(k) + '</th><td>' + esc(v) + '</td></tr>' for k, v in rows) + '</tbody></table>'

def institutional_status(lang):
    data = t(lang, 'institutional')
    return section(esc(data['title']), ul([esc(item) for item in data['items']]) + '<p class="article-ref">' + esc(data['reference']) + '</p>')

def statutory_mission(lang):
    data = t(lang, 'statutory_mission')
    return section(esc(data['title']), '<p>' + esc(data['intro']) + '</p>' + ul([esc(item) for item in data['items']]))


def home_slider(lang):
    data = t(lang, 'slider')
    slides = []
    for i, slide in enumerate(data['slides']):
        image = photo(slide['image'], lang, i == 0, '(max-width: 950px) 92vw, 640px')
        import re
        image = re.sub(r'alt="[^"]*"', 'alt="' + esc(slide['alt']) + '"', image)
        slides.append('<figure class="group-slide" role="group" aria-roledescription="' + esc(data['slide_role']) + '" aria-label="' + str(i + 1) + ' / ' + str(len(data['slides'])) + '"' + (' hidden' if i else '') + '>' + image + '<figcaption>' + esc(slide['caption']) + '</figcaption></figure>')
    dots = ''.join('<button type="button" class="slider-dot" aria-label="' + esc(data['go_to']) + ' ' + str(i + 1) + '" aria-pressed="' + ('true' if i == 0 else 'false') + '" data-slide="' + str(i) + '"></button>' for i in range(len(slides)))
    return '<section class="group-slider" role="region" aria-roledescription="' + esc(data['role']) + '" aria-label="' + esc(data['label']) + '" data-pause-label="' + esc(data['pause']) + '" data-play-label="' + esc(data['play']) + '"><p class="slider-eyebrow">' + esc(data['eyebrow']) + '<span class="slider-counter" aria-hidden="true">01 / 03</span></p><div class="slider-viewport">' + ''.join(slides) + '</div><div class="slider-controls" hidden><button type="button" data-previous aria-label="' + esc(data['previous']) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M19 12H5m7-7-7 7 7 7"/></svg></button><div class="slider-dots">' + dots + '</div><button type="button" data-next aria-label="' + esc(data['next']) + '"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M5 12h14m-7-7 7 7-7 7"/></svg></button><button type="button" data-play aria-label="' + esc(data['pause']) + '"><span aria-hidden="true">Ⅱ</span></button></div><span class="sr-only slider-status" aria-live="polite" aria-atomic="true"></span></section>'

def photo_gallery(lang, key):
    data = t(lang, 'photo_galleries')[key]
    figures = []
    items = data['photos']
    if key == 'home':
        items = sorted(items, key=lambda item: manifest[item['image']]['variants'][-1]['width'] / manifest[item['image']]['variants'][-1]['height'], reverse=True)
    for item in items:
        image = photo(item['image'], lang, sizes='(max-width: 650px) 92vw, (max-width: 950px) 44vw, 400px')
        figures.append('<figure class="gallery-photo">' + image + '<figcaption>' + esc(item['caption']) + '</figcaption></figure>')
    layout = ''.join(figures)
    if key == 'home':
        landscape, portrait = [], []
        for item, figure in zip(items, figures):
            variant = manifest[item['image']]['variants'][-1]
            (landscape if variant['width'] >= variant['height'] else portrait).append(figure)
        layout = '<div class="gallery-format gallery-landscape">' + ''.join(landscape) + '</div><div class="gallery-format gallery-portrait">' + ''.join(portrait) + '</div>'
    return '<section class="photo-gallery" aria-labelledby="gallery-' + key + '"><h2 id="gallery-' + key + '">' + esc(data['title']) + '</h2><p class="gallery-intro">' + esc(data['intro']) + '</p><div class="photo-gallery-grid" data-count="' + str(len(figures)) + '">' + layout + '</div></section>'

def domain_icon(index):
    drawings = [
        '<rect x="4" y="5" width="24" height="17" rx="2"/><path d="M12 27h8m-4-5v5m-8-15 3 3-3 3m7 0h5"/>',
        '<path d="M16 8c-4-3-8-3-12-2v19c4-1 8-1 12 2 4-3 8-3 12-2V6c-4-1-8-1-12 2Zm0 0v19M8 11h4m-4 5h4m8-5h4m-4 5h4"/>',
        '<rect x="4" y="11" width="24" height="16" rx="2"/><path d="M11 11V7a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v4M4 17c8 4 16 4 24 0m-12 1v4"/>',
        '<circle cx="12" cy="9" r="4"/><path d="M4 26v-4a8 8 0 0 1 16 0v4m3-10V5m-4 4 4-4 4 4m-7 12h8m-4-4v8"/>',
        '<path d="M11 22c0-3-5-5-5-10a10 10 0 0 1 20 0c0 5-5 7-5 10M11 22h10m-9 4h8m-7 3h6m-3-7v-9m-4-3 4 3 4-3"/>',
        '<circle cx="16" cy="8" r="3"/><circle cx="6" cy="14" r="3"/><circle cx="26" cy="14" r="3"/><path d="M10 18v-1a6 6 0 0 1 12 0v1M1 26v-3a5 5 0 0 1 10 0v3m10 0v-3a5 5 0 0 1 10 0v3M11 27h10"/>',
    ]
    return '<span class="domain-icon"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + drawings[index] + '</svg></span>'

def home(lang):
    fr = lang == 'fr'
    cards = ''.join((f'<article class="card domain-card"><div class="domain-card-heading">{domain_icon(i)}<span class="number" aria-hidden="true">0{i + 1}</span></div><h3>{t}</h3><p>{d}</p></article>' for i, (t, d) in enumerate(DOMAINS[lang])))
    buttons = [(t(lang, 'decouvrir_smart_yiriba'), 1), (t(lang, 'nos_programmes'), 3), (t(lang, 'nous_contacter'), 6)]
    p = home_slider(lang)
    return f"""<section class="hero"><div class="wrap hero-grid"><div><p class="eyebrow">{t(lang, 'numerique_competences_developpement')}</p><h1><span class="hero-identity">Association</span> Smart YIRIBA</h1><p class="lead">{INTRO[lang]}</p><div class="buttons">{''.join((f'''<a class="button {('secondary' if i else '')}" href="{link(lang, n)}">{t}</a>''' for i, (t, n) in enumerate(buttons)))}</div><div class="legal-note"><strong>{t(lang, 'association_enregistree_au_mali')}</strong><br>{t(lang, 'reference_denregistrement')} : N° 181/P.C-T-2018</div></div><div class="hero-gallery">{p}</div></div></section>\n+<section class="section"><div class="wrap"><div class="section-head"><div><p class="eyebrow">{t(lang, 'notre_mission')}</p><h2>{t(lang, 'des_competences_pour_br_ouvrir_des_perspectives')}</h2></div><p>{t(lang, 'promouvoir_les_tic_lemploi_des_jeunes_et_des_femmes_la_')}</p></div><h3>{t(lang, 'nos_domaines_dintervention')}</h3><div class="grid">{cards}</div></div></section>\n+<section class="section soft"><div class="wrap split"><div>{photo(49, lang)}</div><div><span class="tag">{t(lang, 'programme_en_vedette')}</span><h2>Smart Women<br>Academy</h2><p class="lead">{SWA[lang]}</p><a class="button" href=\"{link(lang, 3)}#smart-women-academy">{t(lang, 'decouvrir_le_programme')} →</a></div></div></section>\n+<section class="section"><div class="wrap">{photo_gallery(lang, 'home')}</div></section>\n+<section class="band"><div class="wrap"><h2>{t(lang, 'un_ancrage_local_une_ambition_collective')}</h2><div class="facts"><div><strong>Tombouctou</strong><span>{t(lang, 'lieu_de_creation_et_siege_declare')}</span></div><div><strong>Bamako</strong><span>{t(lang, 'centre_de_plusieurs_activites_operationnelles')}</span></div><div><strong>Mali</strong><span>{t(lang, 'zone_dintervention_de_lassociation')}</span></div></div></div></section>\n+<section class="section"><div class="wrap split"><div><p class="eyebrow">{t(lang, 'transparence')}</p><h2>{t(lang, 'une_identite_claire_br_un_engagement_durable')}</h2><p>{t(lang, 'association_smart_yiriba_connue_sous_le_nom_smart_yirib')}</p><a href=\"{link(lang, 5)}">{t(lang, 'consulter_les_informations_legales')} →</a></div><div class="card"><h3>{t(lang, 'construisons_des_opportunites_ensemble')}</h3><p>{t(lang, 'pour_echanger_sur_nos_programmes_une_collaboration_ou_l')}</p><div class="buttons"><a class="button" href=\"{link(lang, 6)}">{t(lang, 'nous_contacter')} →</a></div></div></div></section>""".replace('\n+', '\n')

def documented_activities(lang):
    data = t(lang, 'documented_activities')
    cards = ''.join('<article class="card"><p class="eyebrow"><time datetime="' + esc(item['date']) + '">' + esc(item['date_label']) + '</time></p><h3>' + esc(item['title']) + '</h3><p>' + esc(item['text']) + '</p><p><a href="' + esc(item['source']) + '" target="_blank" rel="noopener noreferrer">' + esc(item['source_label']) + ' ↗</a></p></article>' for item in data['items'])
    return section(esc(data['title']), cards)

def governance_structure(lang):
    g = t(lang, 'governance')
    parts = ['<div class="governance-intro"><p class="lead">' + esc(g['intro']) + '</p><p class="source-note">' + esc(g['source_note']) + '</p></div>']
    parts.append('<section aria-labelledby="organs-title"><h2 id="organs-title">' + esc(g['organs_title']) + '</h2><div class="organs-grid">')
    for i, organ in enumerate(g['organs']):
        parts.append('<article class="card organ-card"><span class="number">0' + str(i + 1) + ' · ' + esc(organ['tag']) + '</span><h3>' + esc(organ['title']) + '</h3><p>' + esc(organ['text']) + '</p>' + ul([esc(item) for item in organ['items']]) + '<p class="article-ref">' + esc(organ['reference']) + '</p></article>')
    parts.append('</div></section>')
    parts.append(section(esc(g['roles_title']), '<p>' + esc(g['roles_intro']) + '</p><div class="roles-grid">' + ''.join('<article class="card"><h3>' + esc(role[0]) + '</h3><p>' + esc(role[1]) + '</p></article>' for role in g['roles']) + '</div>'))
    parts.append(section(esc(g['principles_title']), '<div class="principles-grid">' + ''.join('<article class="card"><h3>' + esc(item['title']) + '</h3><p>' + esc(item['text']) + '</p><p class="article-ref">' + esc(item['reference']) + '</p></article>' for item in g['principles']) + '</div>'))
    parts.append(section(esc(g['founders_title']), '<p>' + esc(g['founders_note']) + '</p>' + ul([esc(name) for name in g['founders']])) )
    return ''.join(parts)

def body(lang, n):
    fr = lang == 'fr'
    if n == 1:
        return section(t(lang, 'qui_sommes_nous'), '<p>' + esc(t(lang, 'about_identity')) + '</p>') + institutional_status(lang) + section(t(lang, 'notre_histoire'), ul(t(lang, '2018_creation_et_declaration_de_lassociation'))) + photo(29, lang) + section(t(lang, 'notre_presence'), '<h3>Tombouctou</h3><p>' + t(lang, 'lieu_de_creation_et_siege_declare_lors_de_lenregistreme') + '</p><h3>Bamako</h3><p>' + t(lang, 'principal_centre_actuel_de_plusieurs_activites_operatio') + '</p>') + photo_gallery(lang, 'about')
    if n == 2:
        text = t(lang, 'la_mission_de_lassociation_smart_yiriba_est_de_contribu')
        return section(t(lang, 'mission_institutionnelle'), f'<p class="lead">{text}</p>') + statutory_mission(lang) + section(t(lang, 'nos_valeurs'), values_list(lang)) + photo_gallery(lang, 'mission')
    if n == 3:
        groups = t(lang, 'tic_inclusion_numerique_formation_numerique_utilisation')
        activities = t(lang, 'formation_en_entrepreneuriat')
        return section(esc(t(lang, 'programs_scope_title')), '<p>' + esc(t(lang, 'programs_scope')) + '</p>') + documented_activities(lang) + photo(10, lang) + ''.join((section(t, ul(items)) for t, items in groups)) + photo_gallery(lang, 'programs') + f'<section id="smart-women-academy"><h2>Smart Women Academy</h2><p>{SWA[lang]}</p><p>' + t(lang, 'le_programme_soutient_laccompagnement_professionnel_et_') + '</p>' + photo(49, lang) + '<h3>' + esc(t(lang, 'swa_topics_label')) + '</h3>' + ul(activities) + '<p><strong>' + esc(t(lang, 'swa_contact_label')) + '</strong><br><a href="mailto:swa@smartyiriba.org">swa@smartyiriba.org</a></p>' + photo_gallery(lang, 'women') + '</section>'
    if n == 4:
        g = t(lang, 'governance')
        representative = '<div class="portrait-note"><p class="eyebrow">' + t(lang, 'association_presidency') + '</p><h3>Aboul Hassane CISSE</h3><p><strong>' + t(lang, 'executive_president') + '</strong><br>' + t(lang, 'representation_civil_matters') + '</p><p>' + t(lang, 'entrepreneur_social_specialiste_des_technologies_numeri') + '</p></div>'
        portrait = '<figure class="profile-photo"><img src="/images/web/Abou-hassane-cisse-640w.webp" width="640" height="853" alt="Aboul Hassane CISSE, ' + t(lang, 'fondateur_de_smart_yiriba') + '" decoding="async"><figcaption>Aboul Hassane CISSE</figcaption></figure>'
        book = '<section class="book-section" aria-labelledby="book-title"><p class="eyebrow">' + t(lang, 'publication_du_fondateur') + '</p><div class="book-grid"><figure><img src="/images/web/publication-couverture-23-640w.webp" width="640" height="1138" alt="' + t(lang, 'couverture_du_livre_vers_une_education_innovante_au_mal') + '" loading="lazy" decoding="async"><figcaption>' + t(lang, 'photographie_de_la_couverture') + '</figcaption></figure><div><h2 id="book-title">Vers une éducation innovante au Mali</h2><p class="lead">Vision et stratégie</p><dl><dt>' + t(lang, 'auteur') + '</dt><dd>Aboul Hassane CISSE</dd><dt>' + t(lang, 'editeur') + '</dt><dd>L’Harmattan Mali</dd><dt>' + t(lang, 'preface') + '</dt><dd>Moussa MARA</dd><dt>' + t(lang, 'postface') + '</dt><dd>Oussouby SACKO</dd></dl></div></div></section>'
        source = '<aside class="source-card"><h2>' + esc(g['source_title']) + '</h2><p>' + esc(g['source_details']) + '</p><a href="/documents/statut-Smart-YIRIBA-2018.pdf">' + esc(g['source_label']) + ' ↗</a></aside>'
        finance = g['finance']
        funding = section(esc(finance['title']), '<p>' + esc(finance['intro']) + '</p>' + ul([esc(item) for item in finance['items']]) + '<p>' + esc(finance['note']) + '</p>')
        return governance_structure(lang) + section(esc(g['representative_title']), '<div class="profile-grid">' + portrait + representative + '</div>') + funding + book + source
    if n == 5:
        return table(lang)
    return '<div class="contact-cards"><div class="card"><h3>' + t(lang, 'notre_presence') + '</h3><p>Association Smart YIRIBA<br>Tombouctou & Bamako<br>Mali</p></div><div class="card"><h3>' + t(lang, 'telephone') + '</h3><a href="tel:+22377010808">+223 77 01 08 08</a></div></div>' + email_contacts(lang) + section(t(lang, 'reseaux_sociaux'), social())

def email_contacts(lang):
    data = t(lang, 'email_contacts')
    cards = ''.join('<article class="card"><h3>' + esc(item['label']) + '</h3><a href="mailto:' + esc(item['email']) + '">' + esc(item['email']) + '</a></article>' for item in data['items'])
    return section(esc(data['title']), '<div class="email-cards">' + cards + '</div>')

def social():
    return '<div class="social"><a href="https://www.facebook.com/smartyiriba/" target="_blank" rel="noopener noreferrer">Facebook · Smart YIRIBA ↗</a><a href="https://www.facebook.com/smartwomenacademy" target="_blank" rel="noopener noreferrer">Facebook · Smart Women Academy ↗</a></div>'

def menu_social(lang):
    icons = [
        ('X (Twitter)', 'https://x.com/smartyiriba', '<path d="M4 4h4l12 16h-4L4 4Zm16 0L4 20"/>'),
        ('Facebook', 'https://www.facebook.com/smartyiriba/', '<path d="M14 21v-8h3l.5-4H14V7c0-1 .5-2 2-2h2V2h-3c-3 0-5 2-5 5v2H7v4h3v8"/>'),
        ('TikTok', 'https://www.tiktok.com/@smartyiriba', '<path d="M14 3v13a4 4 0 1 1-4-4M14 3c0 4 3 6 7 6"/>'),
    ]
    label = 'Réseaux sociaux' if lang == 'fr' else 'Social media'
    return '<div class="menu-social" role="group" aria-label="' + label + '">' + ''.join('<a href="' + url + '" target="_blank" rel="noopener noreferrer" aria-label="' + name + ' · @smartyiriba" title="' + name + ' · @smartyiriba"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + icon + '</svg></a>' for name, url, icon in icons) + '</div>'

def navigation_icon(index):
    drawings = [
        '<path d="m3 10 9-7 9 7M5 9v12h5v-7h4v7h5V9"/>',
        '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.01"/>',
        '<circle cx="11" cy="13" r="8"/><circle cx="11" cy="13" r="4"/><path d="m11 13 10-10m-4 0h4v4"/>',
        '<rect x="3" y="7" width="18" height="14" rx="2"/><path d="M8 7V3h8v4M3 12c6 3 12 3 18 0m-9 1v4"/>',
        '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M12 7v5m-7 5v-5h14v5"/>',
        '<path d="M6 3h9l4 4v14H6V3Zm9 0v5h4M9 12h7m-7 4h7"/>',
        '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
    ]
    return '<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + drawings[index] + '</svg>'

def render(lang, n):
    fr = lang == 'fr'
    title = t(lang, 'association_smart_yiriba_organisation_a_but_non_lucrati') if n == 0 else LABELS[lang][n] + ' | Association Smart YIRIBA'
    url = 'https://smartyiriba.org' + link(lang, n)
    desc = INTRO[lang] if n == 0 else LABELS[lang][n] + ' — ' + t(lang, 'decouvrez_lassociation_smart_yiriba_association_a_but_n')
    nav = ''.join((f'<a href="{link(lang, i)}"' + (' aria-current="page"' if i == n else '') + f'>{navigation_icon(i)}<span>{esc(v)}</span></a>' for i, v in enumerate(LABELS[lang])))
    langs = '<div class="languages">' + ''.join('<a href="' + link(code, n) + '" lang="' + code + '" hreflang="' + code + '" aria-label="' + esc(t(lang, 'languages')[code]) + '" title="' + esc(t(lang, 'languages')[code]) + '"' + (' aria-current="true"' if code == lang else '') + '><span aria-hidden="true">' + flag + '</span></a>' for code, flag in [('fr', '🇫🇷'), ('en', '🇬🇧')]) + '</div>'
    brand = f'<a class="brand" href="{link(lang, 0)}"><img src="/images/web/logo-smart-yiriba.webp" width="50" height="50" alt=""><span>Smart YIRIBA<small>ASSOCIATION · MALI</small></span></a>'
    banner = photo(5, lang, eager=True, sizes="100vw").replace('class="activity-photo"', 'class="page-hero-image" aria-hidden="true"')
    banner = re.sub(r'alt="[^\"]*"', 'alt=""', banner)
    content = home(lang) if n == 0 else f'<section class="page-hero">{banner}<div class="wrap"><nav class="breadcrumbs" aria-label="{esc(t(lang, 'breadcrumb_label'))}"><a href="{link(lang, 0)}">{esc(LABELS[lang][0])}</a><span aria-hidden="true">/</span><span aria-current="page">{esc(LABELS[lang][n])}</span></nav><p class="eyebrow">Association Smart YIRIBA · Mali</p><h1>{LABELS[lang][n]}</h1><p class="page-intro">{esc(t(lang, 'page_intros')[n])}</p></div></section><section class="section"><div class="wrap content{' governance-content' if n == 4 else ''}">{body(lang, n)}</div></section>'
    schema = {'@context': 'https://schema.org', '@type': 'NGO', 'name': 'Association Smart YIRIBA', 'alternateName': 'Smart YIRIBA', 'legalName': 'Association SMART/YIRIBA', 'url': 'https://smartyiriba.org', 'email': 'contact@smartyiriba.org', 'telephone': '+22377010808', 'areaServed': 'Mali'}
    return f'''<!doctype html>\n<html lang="{lang}" data-locale-url="/locales/{lang}.json"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="fr" href="https://smartyiriba.org{link('fr', n)}"><link rel="alternate" hreflang="en" href="https://smartyiriba.org{link('en', n)}"><link rel="alternate" hreflang="x-default" href="https://smartyiriba.org{link('fr', n)}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:type" content="website"><meta property="og:image" content="https://smartyiriba.org/{manifest[14]['variants'][-1]['path']}"><link rel="icon" type="image/webp" href="/images/web/logo-smart-yiriba.webp"><link rel="stylesheet" href="{asset('/css/site.css')}"><script src="{asset('/js/site.js')}" defer></script><script src="{asset('/js/carousel.js')}" defer></script><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script></head><body><div class="institutional-bar"><div class="wrap"><span>{esc(t(lang, 'institutional_bar'))}</span><span>N° 181/P.C-T-2018</span></div></div><a class="skip" href="#main">{t(lang, 'aller_au_contenu')}</a><header><div class="wrap header-row">{brand}<button class="menu-toggle" aria-expanded="false" aria-controls="navigation" data-close-label="{esc(t(lang, 'ui')['menu_close'])}" aria-label="{esc(t(lang, 'ui')['menu_open'])}">Menu</button><nav class="nav" id="navigation" aria-label="{t(lang, 'navigation_principale')}">{nav}{menu_social(lang)}</nav>{langs}</div></header><div class="reading-progress" aria-hidden="true"><span></span></div><main id="main" tabindex="-1">{content}</main><footer><div class="wrap"><div class="footer-grid"><div>{brand}<p>{t(lang, 'organisation_a_but_non_lucratif_enregistree_au_mali')}</p>{social()}</div><div><h3>Navigation</h3><nav class="footer-links" aria-label="{t(lang, 'navigation_du_pied_de_page')}">{''.join((f'<a href="{link(lang, i)}">{LABELS[lang][i]}</a>' for i in range(1, 7)))}</nav></div><div><h3>{t(lang, 'informations')}</h3><p>{t(lang, 'footer_registration')} : N° 181/P.C-T-2018<br>Tombouctou & Bamako · Mali</p><a href="mailto:contact@smartyiriba.org">contact@smartyiriba.org</a><br><a href="tel:+22377010808">+223 77 01 08 08</a></div></div><div class="footer-bottom"><span>© 2026 Association Smart YIRIBA. {t(lang, 'tous_droits_reserves')}</span>{langs}</div></div></footer><button class="back-to-top" hidden aria-label="{esc(t(lang, 'ui')['back_to_top'])}" title="{esc(t(lang, 'ui')['back_to_top'])}">↑</button></body></html>'''

def main():
    for lang in SLUGS:
        (ROOT / lang).mkdir(exist_ok=True)
        for n, slug in enumerate(SLUGS[lang]):
            (ROOT / lang / (slug + '.html')).write_text(render(lang, n))
    (ROOT / 'index.html').write_text(render('fr', 0))
    urls = ['https://smartyiriba.org/'] + ['https://smartyiriba.org' + link(l, n) for l in SLUGS for n in range(7)]
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(('<url><loc>' + u + '</loc></url>' for u in urls)) + '</urlset>\n')
    (ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /docs/\nDisallow: /scripts/\nSitemap: https://smartyiriba.org/sitemap.xml\n')
    print('Built 14 bilingual pages and French root home.')
if __name__ == '__main__':
    main()
