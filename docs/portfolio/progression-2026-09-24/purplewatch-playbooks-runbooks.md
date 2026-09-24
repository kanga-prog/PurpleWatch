# PurpleWatch — Playbooks et runbooks d’exécution

**Périmètre :** environnement PurpleWatch autorisé uniquement. Toutes les techniques ci-dessous sont de découverte non destructive.

## Préconditions communes

1. `caldera.service` est `active` sur `PW-CALDERA-01`.
2. Le tunnel WSL `caldera-tunnel.service` est `active` ; le dashboard Caldera est ouvert sur `http://127.0.0.1:8888` depuis le PC hôte.
3. Sur l’endpoint Windows : `Sysmon64`, `WazuhSvc`, `Tailscale` et `splunkd.exe` sont actifs.
4. Sur Linux : `wazuh-agent`, `auditd`, `tailscaled` et `purplewatch-sandcat.service` sont actifs.
5. Pour un retest Windows avec preuve immédiate : Wazuh et Windows sont simultanément actifs seulement pendant la durée du test, puis Windows est arrêté proprement.

## Exécution Windows

| Technique | Profil Caldera | Commande | Règle Wazuh | Preuve attendue |
|---|---|---|---|---|
| T1082 | `PW-WIN11 — T1082 System Information Discovery` | `systeminfo.exe` | `100100` | Sysmon Event ID 1 + alerte T1082 |
| T1057 | `PW-WIN11 — T1057 Process Discovery` | `tasklist.exe` | `100101` | Sysmon Event ID 1 + alerte Process Discovery |
| T1087.001 | `PW-WIN11 — T1087.001 Local Account Discovery` | `net user; exit 0` | `100102` | Sortie des comptes + alerte Local Account Discovery |
| T1016 | `PW-WIN11 — T1016 Network Configuration Discovery` | `ipconfig /all` | `100103` | Sysmon Event ID 1 + alerte Network Configuration Discovery |

### Procédure Windows unique

1. Dans Caldera : **Operations → Start New Operation**.
2. Nommer l’opération `PW-OP-<num>-WIN11-<technique>-LIVE-WAZUH`.
3. Sélectionner le profil associé, `Fact Source: basic`, `Group: ALL`, `Planner: batch`, `Obfuscator: plain-text`, `Run immediately`.
4. Vérifier la ligne Caldera `success` sur `PW-WIN11-01`.
5. Dans Wazuh Threat Hunting : filtrer `agent.name = PW-WIN11-01`, puis le `rule.id` attendu ; confirmer l’alerte de niveau 6.
6. Archiver les horaires Caldera et Wazuh dans la matrice.

## Exécution Linux

| Technique | Profil Caldera | Commande | Règle Wazuh | Preuve attendue |
|---|---|---|---|---|
| T1082 | `PW-LINUX — T1082 OS Information` | `uname -a` et collecte OS | `100104` | auditd `EXECVE` + alerte T1082 |
| T1057 | `PW-LINUX — T1057 Process Discovery` | `ps -ef` | `100105` | auditd `EXECVE` + alerte Process Discovery |
| T1057 Atomic | `PW-LINUX — Atomic T1057 Process Discovery` | `ps >> /tmp/loot.txt; ps aux >> /tmp/loot.txt` | `100105` et `92604` | Caldera `success`, deux alertes de niveau 6 et fichier temporaire supprimé |
| T1016 | `PW-LINUX — T1016 Network Configuration Discovery` | `/usr/sbin/ip addr show` | `100106` | auditd `exe=/usr/bin/ip`, clé `purplewatch_execve` ; alerte T1016 niveau 6 |
| T1087.001 | `PW-LINUX — T1087.001 Local Account Discovery` | `/usr/bin/getent passwd` | `100107` | auditd `exe=/usr/bin/getent`, clé `purplewatch_execve` ; alerte T1087.001 niveau 6 |

### Procédure Linux

1. Vérifier : `sudo systemctl is-active wazuh-agent auditd tailscaled purplewatch-sandcat.service`.
2. Vérifier Sandcat : `pgrep -af '/opt/purplewatch/sandcat'`.
3. Dans Caldera, lancer le profil Linux avec `Group: red` et `Planner: batch`.
4. Vérifier `success` sur `PW-LINUX-01`.
5. Preuve locale : `sudo ausearch -k purplewatch_execve -ts recent -i` ; rechercher l’exécutable correspondant (`/usr/bin/uname`, `/usr/bin/ps`, `/usr/bin/ip` ou `/usr/bin/getent`). Pour T1016/T1087.001, vérifier `ppid` par rapport au PID Caldera et les arguments `addr show` ou `passwd`.
6. Dans Wazuh, filtrer `agent.name = PW-LINUX-01` et le `rule.id` attendu (`100104`, `100105`, `100106` ou `100107`) sur la plage du test.
7. Pour l’ability Atomic T1057, vérifier ensuite que `/tmp/loot.txt` est absent : `test ! -e /tmp/loot.txt`.

## Procédure de retour à l’état stable

- Arrêter la VM Windows après la campagne : `VBoxManage controlvm "PurpleWatch-Windows" acpipowerbutton`.
- Conserver le serveur Caldera actif via son service systemd.
- Ne jamais utiliser `caldera --fresh`.
- Ne modifier une règle Wazuh qu’après avoir documenté le GAP et validé la syntaxe avec `wazuh-analysisd -t` et `wazuh-logtest`.

## Runbook de reprise Windows pour la soutenance

### Pré-vol (2 minutes)

1. Vérifier `WazuhSvc` et `Sysmon64` sur `PW-WIN11-01` : `sc query WazuhSvc` puis `sc query Sysmon64` ; état attendu `RUNNING`.
2. Vérifier le port Wazuh : `powershell -NoProfile -Command "Test-NetConnection 192.168.56.105 -Port 1514"` ; attendu `TcpTestSucceeded : True`.
3. Lancer Sandcat manuellement : `C:\\Users\\Public\\Start-PurpleWatch-Sandcat.cmd`.
4. Vérifier que `splunkd.exe` apparaît et que Caldera présente l'agent Windows `alive, trusted`.

### Si aucune alerte Wazuh récente n'arrive

1. Ne pas relancer plusieurs opérations Caldera.
2. Vérifier les deux services et le test TCP ci-dessus.
3. Redémarrer uniquement l'agent : `net stop WazuhSvc` puis `net start WazuhSvc`.
4. Lancer un seul retest, puis filtrer la règle attendue.

### Preuves de référence

- T1082 : 36,817 s de Caldera à Wazuh après reprise.
- T1057 : 16,526 s de Caldera à Wazuh après reprise.
- La tâche `PurpleWatch-Sandcat` n'est pas utilisée pour la démo tant que son résultat `0x8007042B` n'est pas corrigé.

## Journal et mesures pour les nouveaux runs

Utiliser `purplewatch-journal-attaques.md` : un objet JSONL par exécution, y compris les échecs. Relever l'ID réel de l'opération et de l'ability, l'heure UTC de début du lien Caldera, le statut, l'identifiant et l'heure UTC de l'alerte Wazuh. Conserver l'événement local auditd ou Sysmon, puis marquer `detected`, `not_detected`, `execution_failed` ou `pending_evidence`. Ne calculer la latence qu'avec deux heures vérifiées et comparables. Le run T1016 du 24/09 attend encore son événement auditd et l'identifiant d'alerte propres au retest.

### Prochain scénario Linux : T1087.001

Ability et adversary dédiés créés. Baseline Caldera `success` le 24/09 à 01:24:57 UTC+2, PID 5411 ; auditd `1790205916.904:5388`, PID 5412, PPID 5411. Règle `100107` testée avec `wazuh-analysisd -t` et `wazuh-logtest`. Retest Caldera `success` à 01:44:17 UTC+2, PID 5476 ; Wazuh `100107` niveau 6 à 01:44:20.223 : PASS de détection. Archiver encore le SYSCALL du retest, son PID/PPID et l'ID de l'alerte. La sortie de `getent passwd` peut contenir des noms de comptes : éviter de la publier intégralement.

## T1059.004 Linux — shell contrôlé validé

- Ability `PW-T1059.004-Linux-UnixShell`, tactique Execution, commande `/bin/sh -c 'printf PW-T1059-EXECUTION-OK'`, hôte `PW-LINUX-01`.
- Règle Wazuh `100108` : événement auditd regroupé `SYSCALL+EXECVE`, exécutable `/usr/bin/dash`, clé `purplewatch_execve`, `a0=/bin/sh`, `a1=-c`, `a2` contenant le marqueur hexadécimal. Un `EXECVE` isolé dans `wazuh-logtest` ne représente pas le format de production.
- Référence : 24/09/2026 02:42:37 UTC+2, Caldera `success`, PID 5807 ; Wazuh 02:42:49.269 UTC+2, alerte `100108`, niveau 6. Capturer le `full_log`, l'ID d'alerte et l'heure d'exécution précise pour les métriques ultérieures.
