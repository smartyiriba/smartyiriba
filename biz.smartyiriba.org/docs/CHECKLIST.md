# Checklist — Smart YIRIBA Business

Source : [Cahier des charges — Smart YIRIBA Business](Cahier%20des%20charges%20%E2%80%94%20Smart%20YIRIBA%20Business.md), sections 1 à 75.

Date de préparation : 16 octobre 2026.

Cette checklist constitue le plan de réalisation. Les cases générales restent ouvertes lorsque seule une partie du périmètre est réalisée.

## Avancement — premier lot, 16 octobre 2026

- [x] Initialiser une application Django indépendante avec utilisateur personnalisé, catalogue et demandes de devis.
- [x] Créer et appliquer les migrations initiales en développement SQLite.
- [x] Configurer PostgreSQL pour les environnements hors développement (exécution PostgreSQL restant à vérifier).
- [x] Créer accueil, catalogue public, fiches service et formulaire de devis.
- [x] Ajouter inscription, connexion, déconnexion et espace client limité à ses propres devis.
- [x] Administrer comptes, catégories, services et demandes de devis.
- [x] Vérifier cinq tests : visibilité du catalogue, rattachement des devis, isolation client, refus des services inactifs et CSRF.
- [x] Documenter le démarrage et les limites du premier lot dans le README.

## Avancement — deuxième lot

- [x] Créer commandes et lignes avec quantités, prix, remises, taxes et calculs en décimal.
- [x] Convertir un devis accepté lié à un client en commande brouillon sans duplication.
- [x] Émettre une facture HTML avec instantané des lignes et coordonnées ; figer la commande dans le back-office.
- [x] Enregistrer les paiements manuels et confirmer sous permission dédiée.
- [x] Gérer les paiements partiels/complets, refuser les dépassements et éviter les doubles confirmations.
- [x] Afficher commandes et factures dans l'espace client avec isolation des données.
- [x] Journaliser conversion, émission et confirmation.
- [x] Appliquer les migrations et vérifier les calculs, permissions et parcours avec 16 tests au total, y compris le rendu des formulaires administratifs.

Voir `COMMANDES_FACTURES_PAIEMENTS.md` pour les procédures et limites. Les rubriques générales restent ouvertes : PDF, finalisation comptable, remboursements, transitions avancées et tests concurrents PostgreSQL restent notamment à réaliser.

## Avancement — troisième lot

- [x] Ajouter le téléchargement PDF des factures, réservé au propriétaire.
- [x] Conserver les coordonnées de l'émetteur à l'émission et proposer leur configuration par environnement.
- [x] Annuler les commandes sans encaissement avec motif, permission dédiée et audit.
- [x] Enregistrer et confirmer les remboursements manuels partiels/complets sur factures réglées.
- [x] Empêcher les doubles confirmations et remboursements supérieurs au montant disponible.
- [x] Afficher les remboursements et l'encaissement net dans le portail client.
- [x] Appliquer les migrations et valider 22 tests ; contrôler visuellement le PDF sur deux pages.

Restent pour la finalisation comptable : numérotation validée, avoirs, échéances et retards, ainsi que les coordonnées commerciales réelles. Aucun déploiement n'a été effectué.

## Priorité révisée — vitrine et services de base

La vitrine commerciale devient prioritaire avant la poursuite des outils de gestion.

- [x] Navigation publique en sept entrées et bouton distinct de devis.
- [x] Accueil avec proposition de valeur, expertises, publics et appels à l'action.
- [x] Catalogue initial de 11 prestations sur devis, éditables sans écrasement lors du chargement initial.
- [x] Inclure informatique, web/domaines/hébergement, développement, conseil, organisations, location et logistique.
- [x] Pages formations, programmes, calendrier et demandes de renseignements/inscription.
- [x] Pages solutions B2B/institutions, présentation, réalisations et références autorisées.
- [x] Rubriques administrables : équipe, opportunités et documents commerciaux.
- [x] FAQ et formulaire contact enregistré en base, avec consentement et protections élémentaires.
- [x] Adresse Sotuba, Bamako, Mali et horaire 09 h à 18 h.
- [ ] Renseigner email, téléphone, WhatsApp et jours d'ouverture confirmés.
- [ ] Ajouter capacités, équipements, photos et tarifs réels des salles.
- [ ] Publier les sessions datées, conditions d'inscription et références vérifiables.
- [ ] Ajouter les documents légaux et commerciaux validés.
- [ ] Compléter la version anglaise, les pièces jointes sécurisées et les notifications.
- [ ] Effectuer la recette visuelle mobile/ordinateur dans un navigateur puis préparer la publication.

## Refonte de la vitrine — informatique et formation

- [x] Affirmer le positionnement « entreprise informatique et de formation ».
- [x] Refaire la feuille de style commune : bleu nuit, blanc, orange, typographie et composants.
- [x] Recomposer l'accueil autour des deux métiers, des services et de l'accompagnement.
- [x] Réécrire les textes de présentation, services, formations, solutions, contact et devis.
- [x] Contrôler le rendu de l'accueil sur ordinateur dans Chrome.
- [x] Vérifier les 28 tests existants après refonte.
- [ ] Terminer la recette visuelle mobile et les coordonnées professionnelles manquantes.

## Intégration des images fournies

- [x] Remplacer le monogramme provisoire par le logo fourni dans l'en-tête.
- [x] Intégrer le logo complet dans le pied de page et le symbole comme favicon.
- [x] Illustrer accueil, formations, présentation, contact et location avec les photos fournies.
- [x] Utiliser les variantes WebP 640/1280, les dimensions et les textes alternatifs.
- [x] Vérifier les fichiers référencés et le rendu de l'accueil dans Chrome.

## Règles de réalisation

- Commencer par un monolithe Django modulaire, distinct du site institutionnel.
- Livrer le MVP avant les intégrations et automatisations avancées.
- Conserver les priorités du cahier des charges : P0 fondations, P1 modules métier, P2 automatisation, P3 évolutions.
- Le MVP inclut des éléments P0 et P1 : domaines, hébergement, formations, paiements manuels et support sont nécessaires à la V1.
- Une tâche cochée doit correspondre à un résultat vérifié ; les critères de recette figurent plus bas.

## 0. Cadrage préalable

Références : §§ 1–5, 21, 40–46, 53, 59–67, 71–75.

- [ ] Confirmer le périmètre exact du MVP et les offres effectivement vendues au lancement.
- [ ] Définir la séparation technique avec le site institutionnel : configuration, données, comptes, médias et déploiement.
- [ ] Définir la charte Business : logo, couleurs, typographie, ton et distinction avec l'association.
- [ ] Réunir les coordonnées commerciales, contacts officiels et informations de facturation de Smart YIRIBA.
- [ ] Valider prix, taxes applicables, remises, délais, conditions et politiques de renouvellement avec les responsables concernés.
- [ ] Confirmer le FCFA comme devise principale et son code XOF ; préciser la gestion EUR/USD et l'éventuel JPY, sans supposer une conversion automatique.
- [ ] Définir les moyens de paiement manuels proposés et la procédure de vérification des justificatifs.
- [ ] Choisir les fournisseurs initiaux de domaines, hébergement et emails, ainsi que leurs procédures manuelles.
- [ ] Définir les règles de numérotation, transitions de statut, annulation, remboursement et paiement partiel.
- [ ] Harmoniser les noms des modules proposés : `billing`/`invoices`, catalogue/services et contenus/CMS.
- [ ] Définir les règles d'accès client, organisation et équipe interne.
- [ ] Réunir les contenus français/anglais, offres, formations, FAQ et réalisations autorisées à publier.
- [ ] Décider du niveau d'accès des membres d'organisation en V1 ; planifier la gestion multi-membres complète.
- [ ] Valider l'ordre des lots et les critères de lancement ci-dessous.

## 1. Socle technique — P0

Références : §§ 29, 34, 38–41, 65–67, 73–74.

- [ ] Initialiser le projet Python/Django et ses dépendances.
- [ ] Organiser `config/`, `apps/`, `templates/`, `static/`, `media/`, `locale/`, `tests/`, `docker/` et `requirements/`.
- [ ] Configurer PostgreSQL et les migrations.
- [ ] Prévoir les modules comptes, organisations, clients, catalogue, devis, commandes, factures, paiements, domaines, hébergement, formations, support, notifications, portfolio, contenus et audit.
- [ ] Installer Django REST Framework et définir les premières API utiles, leurs permissions et leur documentation.
- [ ] Configurer Django Templates, Tailwind CSS et JavaScript.
- [ ] Séparer les configurations développement, staging et production.
- [ ] Externaliser les secrets et fournir un fichier d'exemple sans valeur sensible.
- [ ] Configurer les fichiers statiques, les médias privés/publics et les accès aux téléchargements.
- [ ] Préparer Docker, Gunicorn et Nginx.
- [ ] Préparer Git, les conventions de branches et les contrôles automatisés.
- [ ] Préparer l'internationalisation français/anglais et les champs éditoriaux traduisibles.
- [ ] Configurer l'administration Django avec recherche, filtres et actions métier contrôlées.

## 2. Identité, clients et permissions — P0

Références : §§ 22–24, 38–39, 71.

- [ ] Créer le modèle utilisateur avant les premières migrations métier.
- [ ] Ajouter inscription, connexion, déconnexion, vérification email, récupération et changement de mot de passe.
- [ ] Gérer les profils particulier, entreprise, ONG et institution.
- [ ] Gérer nom, prénom, organisation, email, téléphone, adresse, pays, langue et coordonnées de facturation.
- [ ] Créer les organisations et rattacher leurs représentants.
- [ ] Définir les rôles propriétaire, administrateur, finance, technique et utilisateur pour les organisations.
- [ ] Configurer les rôles internes Super Admin, Business, Commercial, Comptabilité, Technique, Formation et Support.
- [ ] Appliquer le minimum d'accès nécessaire dans les vues, API, fichiers et back-office.
- [ ] Vérifier qu'un client ne peut consulter ni modifier les données d'un autre client.

## 3. Catalogue et site commercial — P0 / V1

Références : §§ 3–7, 9–15, 26, 30, 32, 34–37, 53, 56–59.

- [ ] Modéliser catégories, produits et services actifs/inactifs.
- [ ] Gérer prix fixe, « à partir de », sur devis, ponctuel, mensuel et annuel, avec devise et conditions.
- [ ] Préparer les dix familles commerciales définies dans le cahier des charges.
- [ ] Créer les fiches service : description, cible, fonctionnalités, avantages, prix, délai, conditions, FAQ et boutons de commande/devis.
- [ ] Créer la navigation : Accueil, Services, Domaines, Hébergement, Développement, Formations, Solutions, Réalisations, Tarifs, À propos et Contact.
- [ ] Ajouter les accès permanents « Demander un devis » et « Espace client ».
- [ ] Réaliser l'accueil : hero, services, offres populaires, arguments, réalisations et appel à l'action.
- [ ] Préparer les packs Présence Web, Business Web, Organisation et E-commerce ; harmoniser les noms des packs mis en avant.
- [ ] Décrire les offres de sites web : fonctionnalités, pages, délais, maintenance, hébergement et révisions.
- [ ] Décrire développement logiciel, maintenance, email professionnel, collaboration, conseil et services aux organisations.
- [ ] Prévoir les prestations de maintenance par intervention, mois, trimestre et année.
- [ ] Publier les tarifs validés, sans inventer de montants ni de références clients.
- [ ] Créer le portfolio : client, type, année, technologies, description, images, lien et résultats.
- [ ] Créer la FAQ par domaine métier et la recherche services/formations/FAQ/documentation.
- [ ] Créer le formulaire de contact et les liens sociaux officiels ; ajouter WhatsApp si retenu.
- [ ] Traduire les interfaces et les contenus publiés en français et en anglais.
- [ ] Vérifier le responsive mobile, tablette et ordinateur.
- [ ] Vérifier clavier, focus, contrastes, textes alternatifs, sémantique et lisibilité.
- [ ] Ajouter titres SEO, descriptions, URL propres, sitemap, robots.txt, données structurées et Open Graph.
- [ ] Optimiser images, chargement différé, compression, cache et pagination.
- [ ] Reporter les témoignages jusqu'à disponibilité de témoignages vérifiables.

## 4. Devis — P0

Références : §§ 17, 63, 72.

- [ ] Créer la demande de devis avec identité, organisation, contacts, pays, type de client, service, budget, délai, besoin et pièces jointes.
- [ ] Valider les saisies et sécuriser les fichiers transmis.
- [ ] Gérer les statuts Nouveau, En analyse, Informations requises, Devis préparé, Envoyé, Accepté, Refusé, Expiré et Converti en commande.
- [ ] Permettre au commercial d'analyser la demande, préparer l'offre et suivre les échanges.
- [ ] Permettre au client de consulter et accepter/refuser son devis.
- [ ] Convertir un devis accepté en commande sans duplication accidentelle.
- [ ] Conserver l'historique et les conditions/prix acceptés.

## 5. Commandes, factures et paiements — P0 + P1 requis en V1

Références : §§ 18–21, 30, 47, 59, 63.

- [ ] Créer les commandes avec numéro unique, client, lignes, quantités, prix, taxes, remises, total, devise et mode de paiement.
- [ ] Gérer Brouillon, En attente, Confirmée, En préparation, Active, Terminée, Annulée et Remboursée.
- [ ] Conserver les prix commandés et l'historique des changements.
- [ ] Générer les factures avec numéro, date, coordonnées client, prestations, quantités, prix, taxes, devise, total et modalités.
- [ ] Gérer Brouillon, Émise, Payée, Partiellement payée, En retard et Annulée.
- [ ] Permettre l'export et le téléchargement sécurisé des factures PDF.
- [ ] Enregistrer les paiements manuels : mobile, virement, espèces et autres méthodes retenues.
- [ ] Gérer En attente, Confirmé, Échoué, Annulé et Remboursé, avec références et justificatifs.
- [ ] Réserver la confirmation des paiements aux rôles autorisés.
- [ ] Rapprocher paiements et factures ; gérer paiements partiels, solde restant et remboursements.
- [ ] Garantir la cohérence des montants et empêcher la double validation d'une opération.
- [ ] Tracer émission de facture, validation de paiement, annulation et changement de statut.

## 6. Domaines et hébergement manuels — P1 / V1

Références : §§ 8–10, 28, 42–44, 59, 63.

- [ ] Gérer les extensions proposées, prix de vente et prix de renouvellement.
- [ ] Ajouter la demande de domaine et sa vérification manuelle, avec résultat explicite pour le client.
- [ ] Relier demande, commande, facture et paiement à l'enregistrement manuel.
- [ ] Enregistrer domaine, client, extension, registrar, identifiant externe, dates, statut, renouvellement et prix d'achat/vente.
- [ ] Afficher au client ses domaines, dates d'expiration, statuts, mode de renouvellement et factures.
- [ ] Définir les offres Starter, Business, Pro et Custom selon les offres retenues.
- [ ] Gérer stockage, trafic, sites, bases, emails, SSL, sauvegardes, support, durée, prix et renouvellement par offre.
- [ ] Enregistrer les comptes d'hébergement : client, plan, domaine, serveur, identifiant externe, dates, statut et ressources.
- [ ] Permettre l'activation et le renouvellement manuels par l'équipe technique.
- [ ] Suivre les échéances et préparer les rappels manuels avant expiration.
- [ ] Prévoir une couche fournisseur pour éviter le couplage aux futurs prestataires, sans intégrer leurs API en V1.

## 7. Formations — P1 / V1

Références : §§ 15–16, 63.

- [ ] Créer les formations : titre, description, objectifs, public, prérequis, durée, programme, formateur, langue, lieu, format, prix, places, date et certification éventuelle.
- [ ] Gérer les formats individuel, groupe, entreprise, en ligne, présentiel, hybride et cohortes.
- [ ] Publier le catalogue, les fiches et les sessions.
- [ ] Relier compte client, inscription, commande et paiement.
- [ ] Contrôler les capacités et empêcher les inscriptions en double.
- [ ] Confirmer l'inscription après validation du paiement selon les conditions retenues.
- [ ] Afficher les inscriptions et documents téléchargeables dans l'espace client.
- [ ] Prévoir le suivi de participation et les certificats uniquement pour les formations concernées.

## 8. Espace client et support — P1 / V1

Références : §§ 22, 25–27, 57, 59.

- [ ] Créer le tableau de bord client : commandes, services, domaines, hébergements, factures, paiements, devis, formations, tickets et notifications.
- [ ] Ajouter les listes, détails, filtres utiles et téléchargements autorisés.
- [ ] Permettre la mise à jour du profil et des informations de facturation.
- [ ] Créer les tickets : domaine, hébergement, email, site, facturation, paiement, formation, technique et autre.
- [ ] Gérer les priorités faible, normale, haute et urgente.
- [ ] Gérer Nouveau, En cours, En attente client, Résolu et Fermé.
- [ ] Permettre les réponses du client et de l'équipe, avec historique et fichiers sécurisés.
- [ ] Ajouter les notifications dans l'interface et les confirmations essentielles.
- [ ] Préparer les événements commande, paiement, facture, expiration, ticket et formation ; reporter les scénarios email automatiques étendus en V2.

## 9. Administration et suivi opérationnel — P0 / P1

Références : §§ 29, 47, 54–55, 70–72.

- [ ] Administrer clients, utilisateurs, organisations, catalogue et contenus.
- [ ] Administrer devis, commandes, factures, paiements et remises.
- [ ] Administrer domaines, hébergements, formations, inscriptions et tickets.
- [ ] Administrer les notifications ; ajouter promotions et abonnements avec leurs lots respectifs.
- [ ] Mettre en place le journal d'audit : acteur, date, action, ancien état et nouvel état.
- [ ] Tracer les modifications sensibles de prix, statut, client, service et renouvellement.
- [ ] Afficher chiffre d'affaires par devise, commandes, paiements, impayés, devis et nouveaux clients.
- [ ] Afficher domaines actifs/expirants, hébergements actifs, formations et tickets.
- [ ] Définir le suivi prospect → devis → client → commande → paiement → exécution → livraison → support → renouvellement.

## 10. Sécurité, confidentialité et exploitation — requis avant lancement

Références : §§ 38, 47–52, 66, 68–70.

- [ ] Activer HTTPS et les paramètres de sécurité Django de production.
- [ ] Vérifier hashage des mots de passe, CSRF, XSS, injections SQL, sessions et authentification.
- [ ] Limiter les tentatives sur connexion, formulaires et API sensibles.
- [ ] Valider taille/type des fichiers et protéger les justificatifs, devis et documents privés.
- [ ] Contrôler les permissions de toutes les ressources métier et actions administratives.
- [ ] Éviter les secrets et données sensibles dans le dépôt et les journaux.
- [ ] Définir collecte minimale, consentement, conservation, modification et suppression selon les obligations applicables.
- [ ] Préparer et faire valider mentions légales, confidentialité, CGV et conditions d'utilisation.
- [ ] Préparer et faire valider remboursement, renouvellement, hébergement, domaines et formations.
- [ ] Sauvegarder PostgreSQL, fichiers, médias et configuration ; définir rotation quotidienne, hebdomadaire et mensuelle.
- [ ] Tester une restauration complète et documenter la procédure.
- [ ] Surveiller disponibilité, erreurs, CPU, RAM, disque, base, SSL et sauvegardes ; ajouter Celery lors de son introduction.
- [ ] Préparer staging, DNS du sous-domaine, certificats, stockage et configuration de production.
- [ ] Documenter déploiement, migrations et retour à une version précédente.

## 11. Recette et lancement du MVP

Références : §§ 59, 63–64, 68–70, 75.

- [ ] Tester les règles métier et API utiles : comptes, devis, commandes, factures, paiements, domaines et permissions.
- [ ] Vérifier calculs, arrondis, taxes, remises, paiements partiels, doublons et transitions interdites.
- [ ] Vérifier inscription, vérification email, connexion et récupération de mot de passe.
- [ ] Valider le parcours service → devis → acceptation → commande → facture → paiement manuel → livraison.
- [ ] Valider le parcours domaine → demande → vérification manuelle → commande → paiement → enregistrement → suivi d'expiration.
- [ ] Valider le parcours hébergement → plan → domaine → commande → paiement → activation manuelle → espace client.
- [ ] Valider le parcours formation → compte → inscription → paiement → confirmation → documents.
- [ ] Valider le parcours ticket → réponse → résolution et son cloisonnement par client.
- [ ] Vérifier les factures PDF, traductions, formulaires, liens et affichages mobiles.
- [ ] Vérifier l'accessibilité, le SEO et la performance sur les pages principales.
- [ ] Tester les sauvegardes, alertes et procédures d'exploitation sur staging.
- [ ] Rédiger README, installation, architecture, schéma de données et documentation API.
- [ ] Rédiger les procédures : client, facture, paiement, domaine, renouvellement, hébergement, ticket et formation.
- [ ] Charger les contenus et tarifs validés ; retirer les données de démonstration.
- [ ] Effectuer une recette métier avec les rôles commercial, comptabilité, technique, formation et support.
- [ ] Valider la mise en production et contrôler les parcours essentiels après déploiement.

## 12. V2 — automatisation progressive / P2

Références : §§ 8, 24, 27–28, 39, 42, 46, 60, 64.

- [ ] Installer/configurer Redis et Celery avec supervision et reprise des tâches.
- [ ] Développer les adaptateurs fournisseurs, leur gestion d'erreur et leurs tests.
- [ ] Ajouter la recherche de domaine en temps réel, disponibilité, prix et suggestions alternatives.
- [ ] Intégrer l'API registrar : enregistrement, renouvellement et synchronisation des statuts.
- [ ] Intégrer l'API d'hébergement et synchroniser les comptes.
- [ ] Intégrer les moyens de paiement en ligne retenus et sécuriser les callbacks/webhooks contre les doublons.
- [ ] Gérer les abonnements : client, produit, début, échéance, prix, statut et renouvellement automatique.
- [ ] Automatiser les renouvellements autorisés et gérer les échecs.
- [ ] Automatiser les emails de commande, paiement, facture, support et formation.
- [ ] Configurer les rappels d'expiration à J−60, J−30, J−15, J−7 et J−1.
- [ ] Étendre le portail client et finaliser la gestion multi-membres des organisations.
- [ ] Évaluer la 2FA, les connexions Google/Microsoft et les notifications SMS/WhatsApp.

## 13. V3 — services et exploitation avancés

Références : §§ 8, 31, 33, 42, 49–50, 55, 61, 64.

- [ ] Automatiser le provisioning et la suspension/réactivation des services selon les règles validées.
- [ ] Ajouter la gestion DNS client avec permissions et audit.
- [ ] Ajouter les offres VPS et reseller hosting.
- [ ] Ajouter monitoring client, statistiques et premiers services cloud.
- [ ] Étendre les automatisations et la supervision des intégrations.
- [ ] Ajouter coupons, promotions datées, nouveaux clients, groupes et bundles.
- [ ] Ajouter les analytics : visiteurs, conversions, devis, commandes, panier moyen, services populaires, renouvellements, taux de paiement et récurrence.
- [ ] Ajouter CDN et optimisations de performance selon les mesures.
- [ ] Évaluer la rubrique Marchés & contrats et le profil de société téléchargeable.

## 14. V4 — plateforme Cloud / Digital Services

Références : §§ 62, 64, 73.

- [ ] Cadrer les offres infrastructure, SaaS, email, cloud et stockage.
- [ ] Cadrer les offres cybersécurité, IA, automatisation et API.
- [ ] Évaluer les abonnements avancés et une éventuelle marketplace.
- [ ] Évaluer les applications mobiles selon les besoins réels.
- [ ] Réévaluer l'architecture selon les volumes d'utilisateurs et de transactions.

## Ordre conseillé

1. Cadrage et décisions commerciales.
2. Socle, comptes, permissions et catalogue.
3. Site public et devis.
4. Commandes, factures et paiements manuels.
5. Domaines, hébergement et formations.
6. Espace client, support et administration.
7. Sécurité, contenus, documentation et recette.
8. Lancement du MVP, puis V2, V3 et V4 selon les besoins constatés.

Les exigences transversales de sécurité, traduction, accessibilité et audit s'appliquent pendant chaque lot ; leur vérification finale ne remplace pas leur mise en place progressive. Les placements d'éléments non explicitement rattachés à une version dans le cahier des charges constituent des propositions de planification à valider au cadrage.

## Densité des pages

- [x] Réduire les espacements communs des sections, titres, cartes et formulaires.
- [x] Compacter l'en-tête, le pied de page et les blocs d'appel à l'action.
- [x] Réduire la hauteur des photos sur ordinateur et mobile.
- [x] Supprimer la hauteur minimale du contenu qui créait du vide sur les pages courtes.
- [ ] Recontrôler visuellement les pages après compactage (connexion au navigateur interrompue pendant cette étape).

## Identité visuelle — vert du logo

- [x] Remplacer la palette orange/bleu nuit par vert du logo, bleu pétrole, noir et blanc.
- [x] Revoir boutons, navigation active, cartes de service et cartes des deux métiers.
- [x] Harmoniser photos, formations, formulaires et pied de page.
- [x] Conserver la densité compacte et les adaptations mobiles.
- [x] Vérifier les contrastes principaux et contrôler l'accueil dans Chrome sur ordinateur.

## Refonte de composition

- [x] Accueil sur fond vert profond avec photographie et accès directs aux prestations.
- [x] Pictogrammes par famille de services et cartes de catalogue avec prix et lien regroupés.
- [x] Présentation À propos en deux colonnes texte/photo.
- [x] Fiches service avec encadré de demande de devis et informations essentielles.
- [x] Harmoniser les formulaires, FAQ, blocs de formation et pied de page.
- [x] Vérifier 28 tests et contrôler visuellement l'accueil dans Chrome.

## Compétences et confidentialité

- [x] Adapter les compétences transmises en présentation des domaines d'expertise.
- [x] Ajouter les bases de données, l'analyse de données et l'étude/prototypage IA au catalogue.
- [x] Enrichir les thématiques de formation : programmation, données et gestion de projet.
- [x] Distinguer recherche/prototypage des prestations opérationnelles.
- [x] Ne pas reprendre de nom, coordonnées privées ou références académiques personnelles dans les nouveaux textes.

## Relecture éditoriale et cohérence des offres

- [x] Relire les pages publiques, formulaires, messages et fiches des 12 services.
- [x] Harmoniser le nom Smart YIRIBA, les intitulés et les descriptions.
- [x] Clarifier Google Workspace, automatisation, étude/prototypage IA, conseil et déploiement.
- [x] Corriger le lien vers les formations en gestion de projet.
- [x] Préciser la demande de renseignements/inscription et l’absence de sessions datées.
- [x] Harmoniser adresse et horaires depuis la configuration commune.
- [x] Actualiser les textes du catalogue sans modifier les tarifs ni les statuts.
- [x] Vérifier 28 tests et le rendu de 31 pages, sans logistique ni identité personnelle.
- [ ] Compléter les coordonnées et documents commerciaux encore manquants.

## Nouvelle composition de l’accueil et correction des textes

- [x] Remplacer la composition précédente par un titre introductif et deux blocs photo/formation.
- [x] Recomposer les services, la formation, la méthode et le contact avec les styles propres à l’accueil.
- [x] Réécrire et relire les textes : orthographe, accents, ponctuation et formulations.
- [x] Conserver les couleurs validées, les photos fournies, le nom Smart YIRIBA et le retrait de la logistique.
- [x] Vérifier le rendu Django, les images et les 19 liens internes de l’accueil.
- [x] Contrôler visuellement le haut de page dans Chrome sur ordinateur.

## Compactage de l’accueil

- [x] Réduire les marges verticales, la taille des grands titres et les espacements des cartes.
- [x] Réduire les blocs photo/formation et la hauteur des images.
- [x] Supprimer les sauts de ligne décoratifs et rapprocher les sections sur ordinateur et mobile.
- [x] Contrôler visuellement le haut de l’accueil dans Chrome.
