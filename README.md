# PurpleWatch

PurpleWatch est une plateforme Purple Team de laboratoire qui mesure si des techniques MITRE ATT&CK autorisées ont été testées, observées et détectées. Elle orchestre, corrèle et visualise les résultats autour de Wazuh ; elle n'est ni un SIEM ni un outil d'exécution distante.

Le cycle cible est : `TEST CONTROLLED → TELEMETRY → COLLECTION → DETECTION → CORRELATION → COVERAGE → DETECTION GAP → IMPROVEMENT → RETEST`.

## État du projet

Jour 1 : fondations documentaires et DevSecOps uniquement. Aucune application FastAPI/React, aucun laboratoire offensif, ni Wazuh, Sysmon, Atomic Red Team ou Caldera ne sont installés ou configurés.

## Principes de sécurité

- Lab contrôlé, techniques non destructrices et explicitement autorisées.
- Aucune exécution arbitraire de commandes à distance par PurpleWatch.
- Aucun secret, credential, log réel, donnée personnelle, VM, dump, base ou malware dans Git.
- Les fixtures sont petites, synthétiques, anonymisées et transversales.

Consulter le [Project Charter](docs/architecture/project-charter.md), le [périmètre MVP](docs/architecture/mvp-scope.md), l'[architecture v1](docs/architecture/system-architecture.md), les [ADR](docs/architecture/adr/) et le [threat model](docs/security/threat-model-stride.md).

## Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) et [SECURITY.md](SECURITY.md). Aucun commit, push ou changement de laboratoire ne doit être fait sans le processus de revue défini.
