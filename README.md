# PurpleWatch

PurpleWatch est un laboratoire Purple Team privé qui valide la détection de comportements MITRE ATT&CK autorisés. Caldera orchestre les scénarios contrôlés, Sandcat les exécute sur les endpoints, Sysmon ou auditd produisent la télémétrie, puis Wazuh la centralise et applique les règles de détection.

Le cycle validé est : `émulation contrôlée → télémétrie → collecte → détection → analyse du GAP → ajustement → retest`.

## État du projet

Le laboratoire est opérationnel et les six scénarios de couverture ci-dessous ont été validés avec une preuve Caldera et une alerte Wazuh associée. Les détails, résultats et limites sont disponibles dans le [dossier de livraison](docs/portfolio/final-delivery.md) et dans les [preuves](docs/evidence/PW-402-final-validation.md).

| Endpoint | Technique | Commande contrôlée | Règle Wazuh | Résultat |
| --- | --- | --- | --- | --- |
| Windows | T1082 | `systeminfo.exe` | `100100` | PASS |
| Windows | T1057 | `tasklist.exe` | `100101` | PASS |
| Windows | T1087.001 | `net user` | `100102` | PASS |
| Windows | T1016 | `ipconfig /all` | `100103` | PASS |
| Linux | T1082 | `uname -a` | `100104` | PASS |
| Linux | T1057 | `ps -ef` et Atomic `ps` | `100105` | PASS |

## Architecture

- **PW-CALDERA-01** : orchestration Caldera.
- **PW-WIN11-01** : Sandcat, Sysmon et agent Wazuh.
- **PW-LINUX-01** : Sandcat, auditd et agent Wazuh.
- **PW-WAZUH-01** : manager, indexer et Threat Hunting.
- **Tailscale** : connectivité privée chiffrée entre les composants distribués.

Voir l'[architecture du laboratoire](docs/architecture/lab-topology.md) et la [méthode E2E](docs/runbooks/e2e-telemetry-validation.md).

## Principes de sécurité

- Lab contrôlé, techniques non destructrices et explicitement autorisées.
- Aucune exécution arbitraire de commandes à distance par PurpleWatch.
- Aucun secret, credential, log réel, donnée personnelle, VM, dump, base ou malware dans Git.
- Les fixtures sont petites, synthétiques, anonymisées et transversales.

Consulter le [Project Charter](docs/architecture/project-charter.md), le [périmètre MVP](docs/architecture/mvp-scope.md), l'[architecture v1](docs/architecture/system-architecture.md), les [ADR](docs/architecture/adr/) et le [threat model](docs/security/threat-model-stride.md).

## Contribution

Voir [CONTRIBUTING.md](CONTRIBUTING.md) et [SECURITY.md](SECURITY.md). Aucun commit, push ou changement de laboratoire ne doit être fait sans le processus de revue défini.
