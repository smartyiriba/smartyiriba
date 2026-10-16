# Commandes, factures et paiements manuels — lot 2

## Parcours administratif

1. Dans l'administration, sélectionner une demande de devis acceptée et rattachée à un compte, puis utiliser « Convertir en commande brouillon ». Une nouvelle tentative retrouve la même commande.
2. Ouvrir la commande et saisir les lignes chiffrées convenues : description, quantité, prix unitaire, remise totale de ligne avant taxe, taux de taxe. La demande de devis initiale n'inclut pas d'offre chiffrée : aucun prix n'est copié automatiquement.
3. Vérifier le client, la devise et les montants, puis enregistrer. Les prix XOF et remises doivent être entiers ; EUR et USD utilisent deux décimales. Les taxes sont arrondies par ligne, puis les montants sont additionnés.
4. Sélectionner « Émettre la facture (paiement à réception) ». Cette action confirme la commande et fige ses lignes dans l'administration. La facture conserve les montants et coordonnées client à cette date. L'action répétée retrouve la même facture.
5. Après réception d'un règlement, créer un paiement avec la facture, une référence unique, le montant et la méthode. La devise est celle de la facture.
6. Après vérification du règlement, utiliser « Confirmer les paiements vérifiés ». La permission `commerce.confirm_payment` est indispensable. Un paiement supérieur au solde est refusé. Une confirmation répétée ne crée pas un deuxième encaissement.
7. Consulter les événements d'audit : conversion, émission et confirmation, avec acteur, date et changements d'état.

Les commandes peuvent également être créées directement en brouillon dans l'administration. Le client consulte ses commandes confirmées et ses factures depuis son espace ; aucun formulaire public ne permet de déclarer lui-même un paiement confirmé.

## Permissions

Attribuer explicitement aux groupes concernés les permissions Django nécessaires. Le commercial a besoin de `add_order` pour convertir ; la comptabilité a besoin de `add_invoice` pour émettre et `confirm_payment` pour confirmer, ainsi que des permissions de consultation correspondantes. Les groupes métier ne sont pas encore préconfigurés.

Factures, paiements confirmés et événements d'audit sont protégés contre l'édition directe dans l'administration. Les factures sont créées par le service d'émission. Les écritures directes via ORM/scripts doivent également passer par les services métier ; elles ne constituent pas une interface publique autorisée.

## Limites avant production

- Ce lot propose une consultation HTML : export PDF et identité légale de l'émetteur restent à ajouter avant utilisation comme facturation commerciale finale.
- La numérotation utilise un préfixe et un UUID unique ; une politique de numérotation comptable doit être validée avant exploitation.
- Échéance, statut « en retard », factures brouillon et avoirs restent à réaliser. Les annulations sans encaissement et les remboursements sur factures réglées sont disponibles. Les autres transitions métier des commandes restent à développer.
- L'offre chiffrée du devis, son acceptation client et la conservation des conditions acceptées restent à développer.
- La règle de taxes est saisie par l'administrateur : aucun taux fiscal n'est présumé.
- Les pièces justificatives de paiement et les notifications restent à ajouter.
- Les opérations utilisent des transactions et verrouillent les lignes avec PostgreSQL. Les tests locaux utilisent SQLite : les scénarios concurrents doivent encore être testés sur PostgreSQL.

## Lot 3 : PDF, annulations et remboursements

### Coordonnées et PDF

Exporter `BUSINESS_LEGAL_NAME`, `BUSINESS_ADDRESS`, `BUSINESS_REGISTRATION` et `BUSINESS_EMAIL` dans l'environnement avant émission. Les coordonnées sont figées dans la facture, comme celles du client. Le bouton « Télécharger le PDF » se trouve sur la facture client ; l'URL contrôle le propriétaire et interdit la mise en cache partagée. Le PDF conserve le document d'émission ; le statut courant, les paiements et les remboursements figurent dans le portail.

### Annulation sans encaissement

Dans la liste des commandes, saisir le motif dans le champ d'action, sélectionner les commandes et choisir « Annuler les commandes sans encaissement ». La permission `commerce.cancel_order` est nécessaire. Seuls les brouillons et commandes confirmées sans paiement confirmé peuvent être annulés. La facture associée et les paiements en attente sont annulés dans la même transaction. Une nouvelle tentative ne répète pas l'opération. Les paiements déjà encaissés exigent un traitement de remboursement.

### Remboursement manuel

Après avoir réellement effectué le remboursement, créer une entrée « Refund » dans l'administration : paiement d'origine confirmé, référence unique, montant et motif. Sélectionner ensuite « Confirmer les remboursements effectués ». La permission `commerce.confirm_refund` est nécessaire. Le logiciel enregistre un remboursement ; il n'effectue aucun transfert bancaire.

Dans ce lot, seules les factures intégralement réglées sont remboursables. Plusieurs remboursements partiels sont possibles jusqu'au montant du paiement d'origine ; les confirmations répétées sont sans double effet. La facture devient partiellement ou totalement remboursée ; une commande totalement remboursée reçoit le statut correspondant. Le paiement d'origine reste conservé, avec son statut confirmé.

Le solde de facture correspond au montant d'origine non réglé. Un remboursement ne réouvre pas une créance. Le portail affiche séparément montants encaissés, remboursés et encaissement net. Les avoirs comptables restent à développer avant finalisation de la chaîne comptable.

### Vérifications

22 tests couvrent les lots 1 à 3, dont PDF privé et contenu, arrondis, paiements, annulations, remboursements, permissions et administration. Un PDF de contrôle à descriptions longues a été rendu et inspecté sur deux pages. Les tests concurrents sur PostgreSQL restent à réaliser.
