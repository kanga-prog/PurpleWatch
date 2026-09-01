# ADR-002 — Backend Python + FastAPI

**Statut : accepté**

## Contexte

Le backend devra exposer des contrats API et orchestrer les données de couverture.

## Décision

Adopter Python avec FastAPI lorsque le développement applicatif sera autorisé.

## Conséquences

Documentation OpenAPI et validation typée ; SAST Python et audit de dépendances obligatoires.

## Alternatives

Flask/Django ou Node backend : non retenus pour garder une API légère et typée au MVP.
