# Règles Wazuh

Ce répertoire contient les règles Wazuh PurpleWatch revues, versionnées et validées dans le laboratoire privé.

## Couverture PurpleWatch validée

Fichier actif : `purplewatch_p0_rules.xml`

Mappings validés :

| Rule ID | MITRE ATT&CK |
| --- | --- |
| 100100 | T1082 — System Information Discovery |
| 100101 | T1057 — Process Discovery |
| 100102 | T1087.001 — Local Account Discovery |
| 100103 | T1016 — System Network Configuration Discovery |
| 100104 | T1082 — System Information Discovery via `uname` |
| 100105 | T1057 — Process Discovery via `ps` |

La non-régression `T1059.001` reste couverte par la règle Wazuh native `92057`.

Les règles Windows reposent sur la création de processus Sysmon. Les règles Linux reposent sur le décodage auditd `80700`, l'exécutable observé et la clé locale `purplewatch_execve`.

Consulter [PW-401](../../docs/evidence/PW-401.md) pour la baseline Windows et [PW-402](../../docs/evidence/PW-402-final-validation.md) pour la validation finale multi-endpoint.

## Règles de sécurité

- Ne jamais modifier directement `/var/ossec/ruleset/rules/`.
- Déployer les règles PurpleWatch uniquement comme règles locales de laboratoire.
- Valider avec `wazuh-analysisd -t` avant tout redémarrage du manager.
- Ne stocker aucun secret, credential, log brut, malware ou payload Atomic dans ce répertoire.
- Conserver les preuves détaillées et assainies dans `docs/evidence/`.
