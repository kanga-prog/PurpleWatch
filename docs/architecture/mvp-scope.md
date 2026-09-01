# PW-002 — Scope & MVP

## In scope — MVP futur

- Un endpoint Windows de laboratoire avec Sysmon et agent Wazuh.
- Un moteur Wazuh all-in-one de laboratoire.
- Atomic Red Team limité à environ cinq techniques ATT&CK sûres et autorisées.
- Règles Sigma et Wazuh versionnées comme Detection-as-Code.
- Backend FastAPI, PostgreSQL, frontend React/Vite, contrats OpenAPI.
- Corrélation test, télémétrie, collecte, détection, couverture, gap, amélioration et retest.
- Enrichissement CTI minimal depuis des feeds publics normalisés.
- Documentation, fixtures synthétiques et preuves.

## Out of scope

- Remplacer un SIEM, EDR, SOAR ou Wazuh.
- Production, multi-tenancy, haute disponibilité, SSO ou exposition Internet.
- C2, persistence, élévation de privilèges, exfiltration, malware ou exécution arbitraire à distance.
- Données de production, PII, gros logs, images de VM, bases exportées ou dumps mémoire.
- Installation ou configuration de Wazuh, Sysmon, Atomic Red Team ou Caldera au Jour 1.

## Frontières MVP

Chaque technique admise est documentée avec son autorisation, son impact attendu, sa règle de détection, ses preuves attendues et son mécanisme de retest. Toute extension du périmètre nécessite une ADR et une validation sécurité.
