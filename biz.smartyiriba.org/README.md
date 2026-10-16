# Smart YIRIBA Business

Application Django indépendante du site institutionnel. Lots 1 à 3 : comptes, catalogue administrable, demandes de devis, commandes, factures HTML/PDF, paiements manuels, annulations sans encaissement et remboursements contrôlés.

## Démarrage local

Python 3.12 ou plus récent recommandé.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export DJANGO_DEBUG=true
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

Pour préparer le catalogue initial :

```sh
DJANGO_DEBUG=true .venv/bin/python manage.py seed_showcase
```

Cette commande ajoute 12 offres de base sur devis et conserve les contenus déjà modifiés. Les offres sont modifiables dans `/admin/`. Aucun prix, client ou projet fictif n'est préchargé.

Les variables de `.env.example` doivent être exportées dans le shell. SQLite est réservé au développement. Hors développement, un secret et les paramètres PostgreSQL sont obligatoires. Les emails locaux sont écrits sur la console.

## Vérification

```sh
DJANGO_DEBUG=true .venv/bin/python manage.py check
DJANGO_DEBUG=true .venv/bin/python manage.py test
```

## Périmètre restant

Ce lot ne constitue pas encore le MVP prêt pour la production. Vérification email, récupération de mot de passe, limitation des requêtes, audit, traductions, fichiers joints, finalisation comptable des factures et avoirs, organisations multi-membres et autres modules restent à réaliser. Le CSS initial est autonome ; l'intégration Tailwind reste à faire. DRF est installé avec accès administrateur par défaut ; aucune API métier n'est encore exposée.

Avant production : terminer les contrôles de sécurité, configurer un service email, les sauvegardes, les médias privés, la supervision et le proxy HTTPS. Ne pas utiliser le serveur de développement en production.

Voir `docs/CHECKLIST.md` pour le plan complet.

## Commandes et règlements

Voir [la procédure du lot 2](docs/COMMANDES_FACTURES_PAIEMENTS.md) pour convertir un devis, préparer une commande, émettre une facture et confirmer des paiements. Les limites avant production y sont précisées.

## Priorité actuelle : site vitrine

La navigation publique privilégie les services, formations, solutions, réalisations, présentation et contact. Les modules de gestion restent accessibles depuis le pied de page et l'administration.

Le contact est enregistré en base et traité dans l'administration ; aucun email n'est envoyé automatiquement. Configurer les coordonnées `BUSINESS_CONTACT_*` et `BUSINESS_WHATSAPP` dans l'environnement. Adresse confirmée : Sotuba, Bamako, Mali. Horaire : 09 h à 18 h, jours restant à préciser. Email, téléphone et WhatsApp restent à fournir.

Dans l'administration, publier les sessions de formation et les contenus vitrine autorisés (réalisations, clients commerciaux, équipe, opportunités, documents). Les demandes d'inscription et de réservation sont des prises de contact, sans confirmation automatique. Le calendrier masque les sessions passées. Capacités, prix, photos des salles, noms de l'équipe et références doivent être renseignés avec les données réelles.

Le formulaire contact comprend un consentement, un champ anti-robot et un délai entre envois par adresse IP. En production multi-processus, configurer un cache partagé pour cette limitation. Les pièces jointes au devis, la traduction anglaise, les pages contractuelles finalisées et la notification email restent à réaliser. La mise en page responsive est implémentée. Le nouveau design a été contrôlé visuellement sur ordinateur dans Chrome ; la recette aux dimensions mobiles reste à effectuer.

## Identité et textes de la vitrine

Positionnement : **Smart YIRIBA Business est une entreprise informatique et de formation à Bamako.** La vitrine utilise une palette vert du logo, bleu pétrole, noir et blanc, des photographies fournies par Smart YIRIBA et deux axes de présentation : services informatiques et formation professionnelle. Les textes de l'accueil, de la présentation, des services, des formations, des solutions et du contact ont été réécrits. Les réalisations ne sont mises en avant sur l'accueil que lorsqu'un contenu autorisé est publié.

## Images et logos

Les originaux fournis sont conservés dans `docs/`. La sélection utilisée est copiée dans `static/images/` : les deux logos JPEG et les variantes WebP 640/1280 des photos d'atelier, de formation, de présentation et des espaces. Les proportions des logos sont conservées. Les photos utilisent `srcset`, des dimensions explicites et le chargement différé, sauf l'image principale prioritaire. L'intégration de l'accueil a été vérifiée dans Chrome.

La refonte des couleurs s'appuie sur le vert `#7bb43d`, le bleu pétrole `#174d50`, le noir et le blanc. Les composants communs (navigation, boutons, cartes, formulaires et pied de page) utilisent cette palette. Le contraste des principales associations de texte et de fond a été vérifié ; l'accueil a été contrôlé dans Chrome sur ordinateur.

La composition de la vitrine a également été revue : accueil vert profond, pictogrammes de services, cartes de catalogue avec zone tarifaire, présentation en deux colonnes et encadré de devis sur les fiches de prestation. Les formulaires et la FAQ reprennent les composants communs.

Les compétences présentées dans la vitrine sont regroupées par domaine : développement et bases de données, IA et analyse de données, exploitation web, formation, gestion de projet et recherche/prototypage. Les textes commerciaux ne reprennent ni identité personnelle, ni coordonnées privées, ni références académiques individuelles. Les sujets de recherche sont distingués des prestations opérationnelles.

## Relecture et cohérence éditoriale

Les pages publiques, formulaires et 12 offres initiales ont été relus. Le nom public est Smart YIRIBA. La location reste proposée ; la logistique est retirée. Le conseil porte sur l’analyse et les recommandations, le déploiement sur les outils et les utilisateurs, l’automatisation sur les processus, et le prototypage IA sur l’étude et l’évaluation de modèles. Les informations de contact partagées proviennent de la même configuration.

Pour synchroniser explicitement les textes initiaux en conservant les prix et les statuts :

```sh
DJANGO_DEBUG=true .venv/bin/python manage.py seed_showcase --update-texts
```

Sans cette option, la commande conserve les contenus existants. Restent à fournir : téléphone, WhatsApp, jours d’ouverture, documents commerciaux validés, sessions datées et références autorisées. Aucun de ces éléments n’est inventé dans les textes publics.
