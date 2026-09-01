# PW-003 — Architecture v1

## Vue d'ensemble

```text
Opérateur → PurpleWatch Web → PurpleWatch API → PostgreSQL
                                      │
                                      ├── Résultats/corrélation Wazuh
                                      ├── Règles Sigma et Wazuh versionnées
                                      └── CTI public normalisé

Endpoint Windows de laboratoire → Sysmon → Wazuh Agent → Wazuh central
Atomic Red Team (contrôlé) ────────┘
```

PurpleWatch est la couche d'orchestration, corrélation, mesure et visualisation. Wazuh reste responsable de la collecte et de la détection. La plateforme ne doit pas disposer d'une primitive d'exécution arbitraire distante.

## Limites de confiance

- Navigateur vers API : authentification, autorisation et validation d'entrée futures.
- API vers PostgreSQL : compte à privilèges minimaux et secrets hors dépôt.
- PurpleWatch vers Wazuh : accès en lecture et contrats explicitement limités.
- Feeds CTI publics : contenu non fiable, validation de schéma, provenance, limite de taille et expiration.
- Endpoint de lab : environnement isolé, techniques autorisées seulement.

## Principes d'architecture

Monorepo, contrats versionnés, least privilege, données minimisées, Detection-as-Code, auditabilité et preuves reliées aux tests. Les composants applicatifs restent intentionnellement absents au Jour 1.
