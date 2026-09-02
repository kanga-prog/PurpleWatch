# PW-201 — Cyber Lab Isolation

## Objectif

Cette politique limite les expériences PurpleWatch à un environnement de laboratoire explicitement contrôlé.

Le laboratoire ne doit jamais cibler un système de production, un système tiers ou une machine ne faisant pas partie du périmètre autorisé.

## Principe d'isolation

Les composants du Cyber Lab utilisent un réseau virtuel privé dédié.

La communication nécessaire entre l'endpoint Windows et Wazuh est autorisée uniquement dans le périmètre du laboratoire.

Aucun service du laboratoire ne doit être rendu directement accessible depuis Internet.

## Exposition interdite

Les éléments suivants ne doivent pas être exposés publiquement :

```text
RDP de l'endpoint Windows
Wazuh Dashboard
Wazuh API
ports d'enrôlement des agents
services internes PurpleWatch
services de test du laboratoire
```

Aucune redirection de port du routeur domestique vers le Cyber Lab n'est requise ou autorisée par défaut.

## Accès sortant

Un accès sortant à Internet peut être temporairement autorisé pour :

- les mises à jour du système ;
- le téléchargement de composants officiels ;
- l'installation de dépendances approuvées ;
- les flux CTI publics approuvés dans les étapes ultérieures.

L'accès sortant n'autorise jamais l'exécution de tests sur des systèmes externes.

## Endpoint Windows

L'endpoint Windows est une cible de laboratoire.

Sysmon et Wazuh Agent doivent être configurés uniquement pour produire et transmettre la télémétrie nécessaire au projet.

Aucune donnée personnelle réelle ou donnée de production ne doit être introduite volontairement dans la machine de test.

## Tests Purple Team

Les techniques ATT&CK futures doivent être :

```text
connues
+
documentées
+
limitées au laboratoire
+
reproductibles
+
observables
```

PurpleWatch ne fournit aucune console PowerShell, SSH ou autre mécanisme générique d'exécution distante arbitraire.

## Secrets

Les mots de passe, jetons, clés privées et autres secrets du laboratoire :

- ne sont jamais commités dans Git ;
- ne sont jamais inclus dans les captures destinées au dépôt ;
- ne sont jamais enregistrés dans les preuves publiques ;
- utilisent des valeurs spécifiques au laboratoire.

## Données et journaux

Les événements doivent être limités au besoin de validation de détection.

Les captures, exports et journaux susceptibles de contenir des données sensibles doivent rester hors du dépôt Git public.

## Arrêt de sécurité

Si un test produit un comportement inattendu :

```text
STOP test
    ↓
isoler l'endpoint
    ↓
conserver les preuves nécessaires
    ↓
restaurer un état propre
    ↓
analyser avant nouveau test
```

La procédure détaillée de restauration est définie dans `docs/runbooks/lab-recovery.md`.
