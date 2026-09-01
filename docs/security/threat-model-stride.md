# PW-004 — Threat Model STRIDE v1

## Actifs et frontières

Actifs : définitions de tests, règles de détection, résultats, preuves, contrats, configurations, données CTI et secrets d'intégration. Frontières : navigateur/API, API/base, PurpleWatch/Wazuh, ingestion CTI et lab Windows.

| STRIDE | Menace | Exemple | Contrôles initiaux |
|---|---|---|---|
| Spoofing | Usurpation d'identité | Faux agent, faux feed, appel API non autorisé | Authentification future, TLS, validation de provenance, secrets hors Git |
| Tampering | Altération | Règle, résultat ou preuve modifiés | PR, branches protégées, audit trail, hachage de preuves |
| Repudiation | Action non attribuable | Retest ou changement de règle sans auteur | IDs de test, lien issue/PR/preuve, journalisation future |
| Information disclosure | Fuite d'information | Token, log Windows ou PII dans Git | `.gitignore`, Gitleaks, fixtures synthétiques, minimisation et rétention |
| Denial of service | Épuisement de ressources | Feed ou import massif | Limites de taille, timeouts, parsing défensif, quotas futurs |
| Elevation of privilege | Privilège indu | API exécutant une commande endpoint | ADR-011, pas d'exécution arbitraire distante, moindre privilège |

## Risques prioritaires

Les entrées CTI et les intégrations Wazuh sont non fiables jusqu'à validation. Les règles de détection sont des actifs de sécurité : elles exigent revue, tests et provenance. Tout secret introduit dans Git est traité comme compromis.

## Évolution

Ce modèle sera révisé avant chaque frontière nouvelle : authentification API, import Wazuh, exécution de tests de lab, persistance et exposition de l'interface.
