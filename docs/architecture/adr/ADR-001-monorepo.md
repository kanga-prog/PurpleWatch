# ADR-001 — Monorepo

**Statut : accepté**

## Contexte

PurpleWatch rassemble application, intégrations, détections, laboratoire, contrats et documentation.

## Décision

Utiliser un monorepo avec frontières de répertoires explicites.

## Conséquences

Les changements corrélés sont versionnés et revus ensemble ; la CI doit filtrer les chemins pour rester rapide.

## Alternatives

Polyrepo : rejeté pour le MVP car il fragmente les contrats, les preuves et la gouvernance.
