# ADR-012 — DevSecOps dès le premier jour

**Statut : accepté**

## Contexte

Les contrôles ajoutés tardivement laissent s'installer dette, secrets et pratiques non auditables.

## Décision

Appliquer CI, scans secrets, SAST/SCA planifiés, revue et politiques de dépôt dès la fondation.

## Conséquences

Un coût initial de documentation et de contrôle est accepté pour améliorer la qualité et la traçabilité.

## Implémentation et preuves

Le [baseline SAST/SCA](../../security/sast-sca-baseline.md) et la [politique supply-chain](../../security/supply-chain-security-policy.md) définissent l'activation conditionnelle des scanners, les seuils, les exceptions et les contrôles de dépendances. Ils matérialisent cette décision sans en modifier le statut accepté.

## Alternatives

Ajouter les contrôles après le MVP : rejeté, incompatible avec Secure-by-Design.
