# smartyiriba

Site institutionnel bilingue de l’Association Smart YIRIBA, au Mali.

## Développement local

Depuis la racine du projet :

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --test tests/*.test.cjs
python3 -m http.server 8000
```

Ouvrir `http://127.0.0.1:8000/fr/index.html` ou `/en/index.html`.

## Structure

- `locales/` : textes français et anglais en JSON.
- `scripts/build_site.py` : génération des pages HTML.
- `css/` et `js/` : styles, navigation et animations.
- `images/web/` : images WebP optimisées et manifeste.
- `documents/` : statuts publiés sur le site.
- `docs/` : cahier des charges, checklist et audit du contenu.
- `tests/` : tests des interactions JavaScript.

Les images originales sont conservées dans `images/`. Leur conversion nécessite Pillow et s’effectue avec `scripts/optimize_images.py`.

## Publication

La version GitHub Pages est publiée à https://smartyiriba.github.io/ via le dépôt
`smartyiriba/smartyiriba.github.io`. Son workflow `pages.yml` récupère la branche
`main` de ce dépôt source, reconstruit les pages, exécute les validations et publie
les fichiers publics. Après un push du code source, déclencher la publication :

```sh
gh workflow run pages.yml --repo smartyiriba/smartyiriba.github.io
```

Le réglage Pages du dépôt de publication doit utiliser **GitHub Actions**, pour
éviter de publier son README à la place du site. Ce déploiement ne modifie pas
la configuration DNS de `smartyiriba.org`.

Déployer uniquement `index.html`, `fr/`, `en/`, `css/`, `js/`, `locales/`, `images/web/`, `documents/`, `robots.txt` et `sitemap.xml`. Exclure les fichiers de développement, les images originales et `docs/`, notamment l’ancienne page archivée. La publication sur GitHub ne déploie pas automatiquement le site sur `smartyiriba.org`.
