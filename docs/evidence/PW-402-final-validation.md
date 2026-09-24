# PW-402 — Validation finale PurpleWatch

## Objectif

Consolider les preuves de la chaîne PurpleWatch : une technique MITRE ATT&CK autorisée est exécutée par Caldera, observée sur l'endpoint, transmise à Wazuh, puis détectée par une règle précise.

## Périmètre et sécurité

- Laboratoire privé uniquement.
- Techniques de découverte non destructrices.
- Aucun secret, payload, dump ou log brut n'est stocké dans ce dépôt.
- Les adresses publiques et les identifiants d'accès ne font pas partie des preuves.

## Couverture validée

| Endpoint | Technique | Commande | Télémétrie | Règle | Résultat |
| --- | --- | --- | --- | --- | --- |
| Windows | T1082 | `systeminfo.exe` | Sysmon Event ID 1 | `100100` | PASS |
| Windows | T1057 | `tasklist.exe` | Sysmon Event ID 1 | `100101` | PASS |
| Windows | T1087.001 | `net user` | Sysmon Event ID 1 | `100102` | PASS |
| Windows | T1016 | `ipconfig /all` | Sysmon Event ID 1 | `100103` | PASS |
| Linux | T1082 | `uname -a` | auditd `execve` | `100104` | PASS |
| Linux | T1057 | `ps -ef` | auditd `execve` | `100105` | PASS |

## Windows : retest E2E

Après reprise contrôlée du service Wazuh Agent Windows, les deux retests suivants ont confirmé la remontée de télémétrie jusqu'au manager :

| Technique | Opération Caldera | Alerte Wazuh | Délai observé | Résultat |
| --- | --- | --- | ---: | --- |
| T1082 | `PW-T1082-Windows-SystemInfo` à 19:03:08 | règle `100100` à 19:03:44.817 | 36,817 s | PASS |
| T1057 | `PW-T1057-Windows-ProcessDiscovery` à 19:09:31 | règle `100101` à 19:09:47.526 | 16,526 s | PASS |

Un succès Caldera confirme l'exécution. L'alerte Wazuh associée confirme la détection. Les deux éléments sont requis pour déclarer un scénario PASS.

## Linux : extension et Atomic Red Team

auditd enregistrait les exécutions de `uname` et `ps` avec la clé `purplewatch_execve`. Les règles locales `100104` et `100105` ont été ajoutées pour élever ces traces en alertes PurpleWatch liées à MITRE.

L'ability Atomic Linux de découverte des processus a exécuté `ps` et `ps aux`, puis a supprimé le fichier temporaire `/tmp/loot.txt`. Wazuh a généré la règle PurpleWatch `100105` et la règle native `92604`. Le nettoyage a été vérifié.

La persistance Linux a également été validée après un redémarrage contrôlé : `purplewatch-sandcat.service` est revenu actif, Sandcat a repris ses beacons et l'opération `PW-OP-014-LINUX-T1057-REBOOT-E2E` a obtenu `success`.

## GAP, correction et retest

| GAP observé | Diagnostic et correction | Preuve de retest |
| --- | --- | --- |
| `ps -ef` enregistré par auditd sans alerte PurpleWatch dédiée | Ajout de la règle `100105` ciblant `/usr/bin/ps` et `purplewatch_execve` | Alerte `100105` et test Atomic validés |
| Opération Windows réussie sans alerte récente | Vérification Sysmon, connectivité et agent Wazuh, puis reprise de `WazuhSvc` | T1082 et T1057 détectées en moins d'une minute |

## Limites connues

- La tâche planifiée Windows `PurpleWatch-Sandcat` a retourné `0x8007042B`. Elle n'est donc pas retenue comme preuve de persistance.
- La procédure de soutenance utilise le script manuel `Start-PurpleWatch-Sandcat.cmd` pour démarrer Sandcat Windows.
- La machine hôte limitée en mémoire impose des démonstrations courtes et séquentielles.

## Conclusion

PW-402 démontre une boucle Purple Team mesurée : émulation, télémétrie, détection, correction et retest. Les écarts sont documentés au lieu d'être masqués, et chaque PASS repose sur une preuve d'exécution et une preuve de détection.
