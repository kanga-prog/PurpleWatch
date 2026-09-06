# Règles Wazuh

Ce répertoire contient les règles Wazuh PurpleWatch revues, versionnées et validées dans le laboratoire privé.

## PW-401 — P0 Detection Engineering Baseline

Fichier actif : `purplewatch_p0_rules.xml`

Mappings validés :

| Rule ID | MITRE ATT&CK |
| --- | --- |
| 100100 | T1082 — System Information Discovery |
| 100101 | T1057 — Process Discovery |
| 100102 | T1087.001 — Local Account Discovery |
| 100103 | T1016 — System Network Configuration Discovery |

La non-régression `T1059.001` reste couverte par la règle Wazuh native `92057`.

SHA-256 validé du fichier PW-401 :

`98f4679ec7707381a3aa8c5d3159181121237c57de71bda861500a2e9480a510`

## Règles de sécurité

- Ne jamais modifier directement `/var/ossec/ruleset/rules/`.
- Déployer les règles PurpleWatch uniquement comme règles locales de laboratoire.
- Valider avec `wazuh-analysisd -t` avant tout redémarrage du manager.
- Ne stocker aucun secret, credential, log brut, malware ou payload Atomic dans ce répertoire.
- Conserver les preuves détaillées et assainies dans `docs/evidence/`.
