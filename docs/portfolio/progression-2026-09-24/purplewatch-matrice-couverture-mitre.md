# PurpleWatch — Matrice de couverture MITRE ATT&CK

**Date de mise à jour :** 24 septembre 2026
**Périmètre :** laboratoire PurpleWatch autorisé uniquement.

## Objectif

Cette matrice relie chaque émulation ATT&CK à sa télémétrie, à la règle Wazuh, au résultat et à la preuve utilisable pendant la soutenance.

| Technique MITRE | Endpoint | Émulation Caldera | Télémétrie attendue | Détection Wazuh | Résultat | Preuve principale |
|---|---|---|---|---|---|---|
| T1082 — System Information Discovery | `PW-WIN11-01` | `systeminfo.exe` | Sysmon Event ID 1 ; image `C:\Windows\System32\systeminfo.exe` | Règle `100100`, niveau 6 | PASS de détection ; fiabilisation Caldera à conserver comme suivi | Sysmon : `systeminfo.exe` ; Wazuh : `PurpleWatch: System Information Discovery via systeminfo.exe` |
| T1057 — Process Discovery | `PW-WIN11-01` | `tasklist.exe` ; opération `PW-OP-007-WIN11-T1057-BASELINE` | Sysmon Event ID 1 ; `tasklist.exe` ; parent PowerShell | Règle `100101`, niveau 6 | PASS | Caldera `success` à 13:32:26 ; Wazuh `100101` à 13:32:41 |
| T1087.001 — Account Discovery: Local Account | `PW-WIN11-01` | `net user; exit 0` ; opération `PW-OP-009-WIN11-T1087.001-POST-TUNING-RETEST` | Sysmon Event ID 1 ; `net.exe` / `net1.exe` ; commande `net user` | Règle `100102`, niveau 6 | PASS après tuning Caldera | Caldera `success` à 14:33:04 ; Wazuh `100102` à 14:34:06 |
| T1016 — System Network Configuration Discovery | `PW-WIN11-01` | `ipconfig /all` ; opération `PW-OP-010-WIN11-T1016-LIVE-WAZUH` | Sysmon Event ID 1 ; `ipconfig.exe` ; argument `/all` | Règle `100103`, niveau 6 | PASS | Caldera `success` à 14:41:07 ; Wazuh `100103` à 14:41:28 |
| T1082 — System Information Discovery | `PW-LINUX-01` | `uname -a` via `PW-T1082-Linux-OSInfo` | auditd `EXECVE` ; `exe=/usr/bin/uname` ; clé `purplewatch_execve` | Règle `100104`, niveau 6 | PASS après tuning Wazuh | Caldera `success` ; auditd PID `2936`, PPID Caldera `2935` ; Wazuh `100104` à 11:06:47 |
| T1057 — Process Discovery | `PW-LINUX-01` | Ability PurpleWatch `ps -ef` ; retest `PW-OP-012-LINUX-T1057-POST-TUNING-RETEST` ; Atomic `Process Discovery - ps`, opération `PW-OP-013-LINUX-ATOMIC-T1057` ; post-reboot `PW-OP-014-LINUX-T1057-REBOOT-E2E` | auditd `EXECVE` ; `exe=/usr/bin/ps` ; `proctitle=ps -ef` ou `ps aux` ; clé `purplewatch_execve` | Règle locale `100105`, niveau 6 ; règle native `92604` pour le test Atomic | PASS après ajout de la règle Wazuh ; Atomic et persistance post-redémarrage validés | Retest : Caldera `success` à 18:19:56 ; Wazuh `100105` à 18:20:26. Atomic : `success` à 19:29:11 ; Wazuh `100105` et `92604` à 19:29:19 ; nettoyage confirmé. Post-reboot : `PW-OP-014` `success` à 12:33:09 ; Wazuh `100105` à 12:33:35 |
| T1016 — System Network Configuration Discovery | `PW-LINUX-01` | `/usr/sbin/ip addr show` ; ability `PW-T1016-Linux-NetworkConfig`, ID `d174545d-d59e-4363-87bc-578c7c19f832` | Premier essai : auditd `4444`, `exe=/usr/bin/ip`, `ppid=4388` (PID Caldera), clé `purplewatch_execve` ; télémétrie du retest à archiver | Règle `100106`, niveau 6, MITRE T1016 ; `wazuh-logtest` validé sur le SYSCALL brut | PASS de détection au retest ; corrélation PID du retest à compléter | 24/09 UTC+2 : Caldera `success` 00:43:44, PID affiché `5215` ; alerte Wazuh `100106` 00:43:47.794 ; écart affiché 3,794 s |
| T1087.001 — Account Discovery: Local Account | `PW-LINUX-01` | `/usr/bin/getent passwd` ; ability `PW-T1087.001-Linux-LocalAccountDiscovery`, ID `1a85d811-8cfd-4d1c-a83e-b496214e7857` | Baseline auditd `1790205916.904:5388`, PID `5412`, PPID `5411` ; retest `1790207059.331:5466`, PID `5477`, PPID `5476` (Caldera), `exe=/usr/bin/getent`, clé `purplewatch_execve` | Règle `100107`, niveau 6, MITRE T1087.001 ; `wazuh-logtest` validé sur SYSCALL brut | PASS E2E ; ID d'alerte à archiver | 24/09 UTC+2 : Caldera retest `success` 01:44:17, PID `5476` ; auditd 01:44:19.331 ; alerte Wazuh `100107` 01:44:20.223 ; écart affiché 3,223 s, latence E2E non normalisée |
| T1059.004 — Command and Scripting Interpreter: Unix Shell | `PW-LINUX-01` | `/bin/sh -c 'printf PW-T1059-EXECUTION-OK'` ; ability `PW-T1059.004-Linux-UnixShell` | auditd regroupe SYSCALL+EXECVE ; `/usr/bin/dash`, `purplewatch_execve`, marqueur `a2` hexadécimal | `100108`, niveau 6 | **PASS E2E — Execution** | Caldera `success` 24/09 02:42:37 UTC+2, PID `5807` ; Wazuh `100108` 02:42:49.269 UTC+2 ; écart affiché 12,269 s, latence exacte à confirmer |

## GAP et améliorations démontrés

| Technique | Constat initial | Amélioration | Retest |
|---|---|---|---|
| Linux T1082 | auditd était décodé par la règle générique `80700`, niveau 0 ; aucune alerte visible | Règle locale `100104` ciblant `/usr/bin/uname` et la clé `purplewatch_execve` | Alerte Wazuh T1082 niveau 6 : PASS |
| Windows T1087.001 | `net user` listait les comptes mais Caldera retournait `failed` à cause d’un code de retour non nul | Ability Caldera normalisée en `net user; exit 0` ; limite documentée dans l’AAR | Caldera `success` + Wazuh `100102` : PASS |
| Windows T1057 | Baseline exécuté lorsque le Manager Wazuh était indisponible : télémétrie Sysmon prouvée, remontée centrale non prouvée | Retest court avec Windows et Wazuh actifs | Caldera `success` + Wazuh `100101` : PASS |
| Linux T1057 | `ps -ef` était enregistré par auditd avec la clé `purplewatch_execve`, mais aucune règle locale PurpleWatch ne l’élevait en alerte dédiée | Ajout de la règle `100105` ciblant `audit.exe=/usr/bin/ps` et la clé `purplewatch_execve` ; libellé généralisé en « via ps » | Caldera `success` + Wazuh `100105` : PASS ; ability Atomic standardisée validée avec la règle Wazuh native `92604` |
| Linux T1087.001 | Baseline `getent passwd` exécuté par Caldera et lié à auditd par PID/PPID, sans alerte dédiée | Règle `100107` sur `/usr/bin/getent` et la clé `purplewatch_execve` ; syntaxe et `wazuh-logtest` validés | Nouvelle alerte `100107` au retest Caldera : PASS de détection ; auditd du retest à archiver |

## Lecture pour la soutenance

Une ligne `PASS` signifie que la technique a été exécutée dans le laboratoire, qu’une télémétrie pertinente a été produite, et que Wazuh a généré l’alerte précise associée. Les améliorations ci-dessus constituent les éléments de résolution de problèmes et de tuning demandés par le projet.

## Addendum de fiabilité — 19 septembre 2026

Après reprise de `WazuhSvc` sur `PW-WIN11-01`, deux retests E2E Windows ont confirmé une remontée rapide vers le manager :

| Technique | Opération / ability | Heure Caldera | Heure Wazuh | Latence | Verdict |
|---|---|---:|---:|---:|---|
| T1082 | `PW-T1082-Windows-SystemInfo` | 19:03:08 | 19:03:44.817, règle `100100` | 36,817 s | PASS |
| T1057 | `PW-T1057-Windows-ProcessDiscovery` | 19:09:31 | 19:09:47.526, règle `100101` | 16,526 s | PASS |

Ces délais comprennent l'exécution Caldera, l'événement Sysmon, la transmission par l'agent Wazuh et l'analyse par le manager. Ils constituent la référence de démonstration, en remplacement de la mesure anormalement longue observée avant reprise de l'agent Wazuh.
