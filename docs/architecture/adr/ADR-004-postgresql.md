# ADR-004 — PostgreSQL

**Statut : accepté**

## Contexte

Tests, techniques, résultats, preuves et retests possèdent des relations traçables.

## Décision

Utiliser PostgreSQL comme base relationnelle du MVP.

## Conséquences

Schémas, migrations, moindre privilège et sauvegardes restent nécessaires ; aucune base ne sera versionnée.

## Alternatives

SQLite : rejeté pour la cible multi-composants et l'exploitation réaliste ; NoSQL : rejeté pour les relations centrales.
