# PurpleWatch — suivi du 24 septembre 2026

Ce dossier fige les livrables actualisés et les observations assainies du lab. La source de vérité et le journal JSONL documentent les exécutions réelles ; les heures Caldera affichées ne constituent pas des `started_at` exacts.

## Validations ajoutées

| Technique | Tactique | Endpoint | Règle | Statut |
| --- | --- | --- | --- | --- |
| T1016 | Discovery | PW-LINUX-01 | 100106 | PASS de détection |
| T1087.001 | Discovery | PW-LINUX-01 | 100107 | PASS de détection |
| T1059.004 | Execution | PW-LINUX-01 | 100108 | PASS de bout en bout le 24/09/2026 |

Pour T1059.004, Wazuh regroupe les lignes auditd SYSCALL et EXECVE : la règle du dépôt vise ce format de production. Les autres tactiques proposées (Collection, Defense Evasion, Credential Access) restent à implémenter et à valider. P50 et P95 restent à mesurer avec répétitions et horodatages comparables.
