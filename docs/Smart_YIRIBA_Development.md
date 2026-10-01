# Développement de la V1 Smart YIRIBA

## Réalisé

- Site statique HTML/CSS/JavaScript sans dépendance de framework ni service tiers de police.
- Sept pages en français et sept équivalents anglais, plus l’accueil français à la racine.
- Header sticky, navigation mobile, sélecteur de langue vers la page équivalente, footer commun.
- Contenus institutionnels provenant du cahier des charges, informations légales et gouvernance sans membres inventés.
- Métadonnées SEO, URL canoniques, hreflang, données structurées NGO, sitemap et robots.txt.
- Logo extrait de la page initialement fournie.
- 58 photos sources conservées, 57 images uniques, 120 versions WebP adaptées aux différentes tailles d’écran. Variantes jusqu’à 640, 1280 et 1920 pixels, sans agrandissement des originaux.
- Orientation corrigée et métadonnées des photos exclues des exports web.
- Inventaire des sources et des copies : [Smart_YIRIBA_Image_Inventory.md](Smart_YIRIBA_Image_Inventory.md).
- Ancienne page conservée dans `docs/archive/index-original.html`.

Les noms des images décrivent leur contenu visible. Ils ne certifient pas l’identité des personnes, les dates ou les lieux des prises de vue. Les photos retenues sur le site illustrent les activités ; aucun participant n’est identifié nominativement, à l’exception d’Aboul Hassane CISSE dont la photo a été identifiée par l’utilisateur.

## Modifier et reconstruire

Les traductions et contenus multilingues sont dans `locales/fr.json` et `locales/en.json`. Les composants communs sont dans `scripts/build_site.py`, les styles dans `css/site.css`, les comportements et animations dans `js/site.js`. Modifier les mêmes clés dans les deux dictionnaires puis reconstruire les pages.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --test tests/*.test.cjs
```

Pour refaire les conversions (Pillow et ImageMagick nécessaires) :

```sh
python3 scripts/optimize_images.py
```

Le script d’images attend l’inventaire actuel. Lors de l’ajout de nouvelles photos, mettre à jour les noms descriptifs avant de le relancer.

## Prévisualisation locale

Depuis la racine du projet :

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Ouvrir `http://127.0.0.1:8000`. Utiliser un serveur local, car les chemins des pages et des fichiers partent de la racine du site.

## Vérifications réalisées

Le validateur vérifie les quinze pages HTML : destinations internes, ancres, images, variantes srcset, dimensions, langues, présence des métadonnées SEO et fichiers de l’inventaire.

Le contrôle visuel des photos a été effectué à partir d’une planche contact. Le contrôle visuel du site dans un navigateur reste à effectuer : le navigateur natif a été identifié, mais sa capture a échoué avec une erreur du service de contrôle. Le comportement responsive et le menu mobile sont implémentés mais restent à vérifier visuellement et au clavier dans un navigateur.

## À confirmer avant publication

- Réception effective des emails : les trois adresses demandées par l’utilisateur sont publiées, avec des liens `mailto:` vérifiés ; aucun message de test n’a été envoyé.
- Disponibilité et activité actuelles des deux pages Facebook : les URL proviennent de l’ancienne page, sans vérification de leur disponibilité externe.
- Validation par l’association des traductions, données institutionnelles et choix des photos.
- Texte de la Vision : mentionné dans l’architecture recommandée, mais absent du cahier des charges ; il n’a pas été inventé.
- Contrôle visuel sur mobile et ordinateur, navigation au clavier.
- Hébergement, HTTPS et certificat SSL valide après mise en ligne.

Aucun formulaire n’est présent : les coordonnées sont directement accessibles. Les pages supplémentaires recommandées ne font pas partie de cette V1.

## Fichiers à publier

Publier `index.html`, `fr/`, `en/`, `css/`, `js/`, `locales/`, `documents/statut-Smart-YIRIBA-2018.pdf`, `images/web/` (les fichiers WebP), `robots.txt` et `sitemap.xml` à la racine de l’hébergement. Ne pas publier les photos originales, `docs/`, `scripts/` ni le manifeste de travail. Aucun déploiement n’a été effectué dans cette session.

## Mise à jour du représentant légal

Le portrait fourni sous `images/web/Abou-hassane-cisse-640w.webp` est utilisé sur les pages Gouvernance FR et EN. Une rubrique présente son livre *Vers une éducation innovante au Mali — Vision et stratégie*, avec la photographie de couverture, L’Harmattan Mali comme éditeur, la préface de Moussa MARA et la postface d’Oussouby SACKO. Les informations proviennent des photographies du livre et de l’identification fournie par l’utilisateur.

## Architecture multilingue JSON

Les fichiers JSON sont la source des traductions françaises et anglaises. Ils contiennent notamment la navigation, les chemins des pages, les textes, les listes de programmes, les libellés d’interface et une rubrique `governance` structurée en organes, rôles, principes et fondateurs. Le générateur Python produit les pages HTML à partir de ces données. Les contenus et métadonnées restent ainsi disponibles sans JavaScript et sans attente réseau.

JavaScript charge le dictionnaire de la langue déclarée dans le HTML pour les libellés interactifs. Le sélecteur FR/EN mène à la page équivalente. Une erreur de chargement JSON laisse le contenu et les libellés HTML fonctionnels.

## Gouvernance fondée sur les statuts

Source lue : `documents/statut-Smart-YIRIBA-2018.pdf`, statuts établis à Tombouctou le 15 mai 2018.

- Article 8 : cinq membres fondateurs, présentés comme une liste historique.
- Articles 11 à 15 : Assemblée générale, Bureau exécutif, Comité consultatif, bénévolat, gestion opérationnelle et contrôle annuel.
- Articles 16 à 18 : élections et six fonctions statutaires du bureau.
- Articles 10 et 13 : ressources et approbation des comptes.
- Articles 19 et 21 : modification des statuts et règlement intérieur.

Les noms des titulaires actuels des six fonctions du bureau ne sont pas établis par cette source et ne sont pas inventés. Aboul Hassane CISSE est présenté comme Président Exécutif et représentant de l’Association dans les actes de la vie civile, selon l’article 14 et la dernière page des statuts, conformément à la correction fournie par l’utilisateur. Le portrait et le livre restent présents après l’organisation institutionnelle. Un lien permet de consulter le PDF des statuts.

## Animations et contrôles

Apparitions légères au défilement via IntersectionObserver et l’API native d’animation, retours visuels au survol et au focus, progression de lecture, retour en haut et ombre discrète du header. Les animations se désactivent avec `prefers-reduced-motion`. Aucun contenu n’est masqué en attendant une animation. La navigation mobile reste visible sans JavaScript.

Les tests Node vérifient le menu avec échec du chargement JSON, les libellés JSON, la progression de lecture, le retour en haut, l’animation unique par élément et la réduction des mouvements. Le validateur Python vérifie la parité des dictionnaires ainsi que les organes, les rôles, les fondateurs et les fichiers de référence présents dans les deux pages Gouvernance. Le contrôle visuel dans le navigateur reste à réaliser en raison de l’erreur de capture rencontrée.

## Slider d’accueil et sélecteur à drapeaux

Le hero des accueils FR, EN et racine contient un slider de trois photos de groupe : participants devant la bannière Smart YIRIBA, groupe dans les locaux et participantes présentant leurs attestations. Les légendes, textes alternatifs et contrôles sont définis dans la clé `slider` des JSON. Les images utilisent les variantes WebP existantes et restent entières avec `object-fit: contain`.

`js/carousel.js` gère une rotation toutes les six secondes, les flèches, les points de sélection et lecture/pause. Le survol, le focus, une page masquée et la réduction des mouvements interrompent la rotation. Une navigation manuelle arrête la lecture automatique jusqu’à un appui explicite sur Lecture. Sans JavaScript, la première photo reste affichée.

Le sélecteur de langue utilise les drapeaux français et britannique avec les noms accessibles « Français » et « English », des infobulles et une bordure indiquant la langue active. Les liens vers les pages équivalentes sont conservés. Ces modifications sont couvertes par la validation des fichiers et trois tests du slider ; leur contrôle visuel reste à effectuer.

## Corrections institutionnelles

La présentation d’Aboul Hassane CISSE privilégie désormais sa fonction de Président Exécutif et la représentation dans les actes de la vie civile. Sa qualité de membre fondateur est conservée. Les informations légales et l’histoire distinguent le 2 mai 2018 (déclaration mentionnée sur le récépissé), le 15 mai 2018 (statuts signés) et le 28 décembre 2018 (délivrance du récépissé). Les deux dates du récépissé restent issues du cahier des charges et des précisions de l’utilisateur ; le fichier fourni dans `documents/` est celui des statuts.

La page Mission présente les objets de l’article 5 ; À propos et Informations légales précisent le caractère apolitique, non confessionnel, à but non lucratif, la durée illimitée et le territoire d’intervention national. La page Gouvernance dispose d’une rubrique Transparence et financement avec les ressources statutaires, sans montants ou financement actuel inventés. Le cahier des charges et la checklist ont été alignés sur ces corrections.

## Relecture et reprise visuelle

Les textes français et anglais ont été relus et les formulations identifiées comme maladroites ont été corrigées. Les intitulés sont harmonisés, la référence d’enregistrement du footer est traduite et les textes anglais utilisent les conventions britanniques. Les descriptions alternatives des photos sont rédigées dans les deux langues.

La feuille de styles a été consolidée. Les photos d’activités utilisent leur ratio naturel, les portraits et le livre ont une largeur adaptée, et les variantes WebP demandées correspondent à leur largeur prévue. Le slider conserve les photos de groupe entières ; sa légende n’est plus dans un bandeau vert et ses commandes sont plus discrètes. L’accueil utilise un titre moins dominant et des colonnes mieux équilibrées.

Le générateur ajoute une empreinte du contenu aux URL des styles et scripts pour renouveler le cache lors d’une modification. Cette correction a été nécessaire : Safari affichait le nouveau HTML avec les anciens styles lors du premier contrôle.

Le nouvel accueil a été contrôlé visuellement sur ordinateur dans Safari, et la sélection manuelle d’une photo a été vérifiée dans l’interface. Le contrôle visuel de toutes les autres pages et de la version mobile reste à effectuer. Les tests automatisés du menu et du slider ainsi que les validations des pages et des dictionnaires passent.

## Design institutionnel global

La présentation commune aux pages françaises et anglaises utilise une palette vert profond et tons neutres, des titres en Georgia et un corps de texte sans empattement. Le bandeau institutionnel affiche le statut associatif et la référence d’enregistrement. Les pages intérieures disposent d’un en-tête vert, d’un fil d’Ariane accessible et d’une introduction définie dans les JSON. Les sections, cartes, tableaux, contacts et le footer ont été harmonisés ; les photos conservent leurs proportions.

Le contrôle automatisé des 15 pages et les sept tests JavaScript passent. L’accueil et le bas de la page Gouvernance ont été contrôlés visuellement sur ordinateur dans Safari. Le contrôle visuel complet sur mobile et des autres pages reste à effectuer. Cette refonte concerne la version locale ; elle ne constitue pas un déploiement public.

## Adresses institutionnelles

Les pages Contact FR/EN présentent `contact@smartyiriba.org` (contact général), `rejoindre@smartyiriba.org` (rejoindre l’association) et `aboulhassane@smartyiriba.org` (Président exécutif). Le footer commun et les données structurées NGO utilisent l’adresse générale. Les intitulés sont définis dans `email_contacts` des JSON. Les liens sont contrôlés sans envoi de message.

## Galeries de photos des activités

Douze photos supplémentaires sont réparties entre cinq galeries sur Accueil, À propos, Mission et Programmes, dont une galerie consacrée à la formation et à la participation des femmes. Les scènes choisies montrent le travail sur ordinateur, les échanges collectifs, les présentations, les participantes aux événements et la remise d’attestations.

La clé `photo_galleries` des JSON définit la sélection et les légendes ; `image_alt` définit les descriptions alternatives. Les photos sont issues des fichiers fournis, sans attribution de date, de lieu précis ou d’identité non confirmés. La fonction `photo_gallery` génère des figures sémantiques avec légendes. La grille passe à une colonne sur petit écran et conserve les proportions naturelles des images. Les versions WebP existantes sont utilisées avec `srcset` et chargement différé.
