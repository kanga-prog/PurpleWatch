# PurpleWatch — Source de vérité

> Document vivant de référence. Toute modification d’architecture, d’accès, de règle de détection ou de procédure doit être ajoutée ici après validation.

**Version :** 1.0
**Dernière mise à jour :** 24 septembre 2026
**Périmètre :** laboratoire autorisé PurpleWatch uniquement.

## 1. Objectif du projet

PurpleWatch mesure si des techniques MITRE ATT&CK autorisées, exécutées dans un laboratoire isolé, sont correctement observées et détectées.

La boucle de travail obligatoire est :

```text
Technique ATT&CK → télémétrie → détection Wazuh → PASS ou GAP → amélioration → retest → preuve
```

Wazuh est le SIEM. Caldera orchestre les tests autorisés. Sysmon (Windows) et auditd (Linux) produisent la télémétrie.

## 2. Architecture validée

```text
PC hôte HP x360
├── Edge : dashboard Caldera via http://127.0.0.1:8888
├── Edge : dashboard Wazuh via https://192.168.56.105
├── WSL Ubuntu : tunnel SSH Caldera persistant
├── VirtualBox : PurpleWatch-Windows / PW-WIN11-01
└── VirtualBox : PurpleWatch-Wazuh / PW-WAZUH-01

Scaleway
├── PW-CALDERA-01 : Caldera
└── PW-LINUX-01 : endpoint Linux

Tailscale : réseau privé chiffré entre les composants du lab
```

## 3. Composants et accès

| Composant | Emplacement | Adresse / accès validé | Rôle |
|---|---|---|---|
| PC hôte | HP x360 | Edge | Poste de présentation et de pilotage |
| Wazuh | VM VirtualBox `PurpleWatch-Wazuh` | `https://192.168.56.105` depuis Edge hôte | SIEM, corrélation, dashboard |
| Windows | VM VirtualBox `PurpleWatch-Windows` / `PW-WIN11-01` | VirtualBox `192.168.56.106`, Tailscale `100.115.23.127` | Endpoint Windows surveillé |
| Caldera | Scaleway `PW-CALDERA-01` | Tailscale `100.103.199.63` | Orchestration des techniques ATT&CK |
| Linux | Scaleway `PW-LINUX-01` | Tailscale `100.127.134.63` | Endpoint Linux surveillé |

## 4. Caldera — fonctionnement de référence

### Service serveur Caldera

- Dossier : `/opt/caldera`
- Python : `/opt/caldera/.venv/bin/python`
- Service systemd : `caldera.service`
- Port dashboard HTTP : `8888`
- Port `2222` : FTP Caldera ; **ce n’est pas le dashboard**.

Commandes serveur :

```bash
sudo systemctl start caldera
sudo systemctl status caldera --no-pager
sudo ss -lntp | grep ':8888'
```

Le serveur Caldera doit rester lancé par systemd. Ne pas le lancer durablement dans une simple session SSH.

**Interdit :** ne jamais utiliser `--fresh` sauf décision explicite documentée. Cette option réinitialise l’état Caldera.

### Tunnel dashboard Caldera vers le PC hôte

- Environnement : WSL Ubuntu sur le PC hôte.
- Service systemd : `caldera-tunnel.service`.
- URL de présentation : `http://127.0.0.1:8888` dans Edge du **PC hôte**.

Commandes hôte PowerShell :

```powershell
wsl -d Ubuntu -- bash -lc "sudo systemctl start caldera-tunnel"
wsl -d Ubuntu -- bash -lc "systemctl is-active caldera-tunnel"
```

Résultat attendu : `active`.

**Règle critique :** ne pas exécuter `wsl --shutdown` avant une démonstration Caldera. Cette commande arrête le tunnel.

## 5. Windows — état de référence

- Sysmon : service `Sysmon64`, attendu `Running`.
- Agent Wazuh : service `WazuhSvc`, attendu `Running`.
- Tailscale : service `Tailscale`, attendu `Running` et `Automatic`.
- Sandcat Caldera : `C:\Users\Public\splunkd.exe`.
- Tâche de persistance Sandcat : `PurpleWatch-Sandcat`.

Vérification dans PowerShell de la VM Windows :

```powershell
Get-Service WazuhSvc,Sysmon64 | Select-Object Name,Status
Get-Service Tailscale | Select-Object Name,Status,StartType
Get-Process -Name splunkd -ErrorAction SilentlyContinue | Select-Object Name,Id,StartTime
schtasks /Query /TN "PurpleWatch-Sandcat" /FO LIST
```

Lors d’un démarrage manuel de Sandcat, utiliser le serveur Caldera Tailscale sur le port `8888` et le groupe `red`. Ne pas inscrire de secret dans ce document.

### Parcours de mise en marche — endpoint Windows

**But :** préparer `PW-WIN11-01` pour une campagne Windows, sans démarrer la VM Wazuh locale.
**Analogie :** Caldera est le chef d’orchestre, Sandcat est le musicien sur Windows, et Sysmon/Wazuh Agent sont les enregistreurs. On vérifie d’abord que chacun est prêt avant de jouer la technique.

#### 1. Vérifier Caldera sur PW-CALDERA-01

Dans le terminal SSH du serveur Scaleway :

```bash
sudo systemctl is-active caldera
```

Résultat attendu : `active`. Si ce n’est pas le cas, démarrer puis vérifier :

```bash
sudo systemctl start caldera
sudo systemctl is-active caldera
```

#### 2. Vérifier que Wazuh local est arrêté

Dans PowerShell du **PC hôte** :

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" list runningvms
```

`PurpleWatch-Wazuh` ne doit pas apparaître pendant cette phase afin de préserver la mémoire.

#### 3. Démarrer l’endpoint Windows

Toujours dans PowerShell du **PC hôte** :

```powershell
& "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" startvm "PurpleWatch-Windows" --type gui
```

Si la VM est déjà affichée dans `list runningvms`, ne pas relancer cette commande.

#### 4. Vérifier la télémétrie dans la VM Windows

Dans PowerShell de **PW-WIN11-01** (invite `PS C:\Users\purplewatch>`), attendre environ une minute après le démarrage, puis exécuter :

```powershell
Get-Service WazuhSvc,Sysmon64 | Select-Object Name,Status
```

Résultat attendu : `WazuhSvc` et `Sysmon64` sont `Running`.

#### 5. Vérifier le trajet Windows → Caldera

Toujours dans PowerShell de la VM Windows :

```powershell
Test-NetConnection 100.103.199.63 -Port 8888 | Select-Object ComputerName,RemotePort,TcpTestSucceeded
```

Résultat attendu : `TcpTestSucceeded : True`.

#### 6. Vérifier Sandcat et le démarrer seulement s’il est absent

```powershell
Get-Process -Name splunkd -ErrorAction SilentlyContinue | Select-Object Name,Id,StartTime
```

Si une ligne `splunkd` apparaît, Sandcat est déjà lancé : ne rien faire.
Si la sortie est vide, démarrer une seule fois :

```powershell
Start-Process "C:\Users\Public\splunkd.exe" -ArgumentList "-server http://100.103.199.63:8888 -group red" -WindowStyle Hidden
```

Puis re-vérifier avec la commande `Get-Process` ci-dessus. La tâche `PurpleWatch-Sandcat` lance normalement Sandcat automatiquement après le démarrage de Windows ; ce démarrage manuel est uniquement un secours.

#### Dépannage Tailscale Windows

Si le test vers `100.103.199.63:8888` échoue alors que Caldera est `active`, vérifier d’abord :

```powershell
Get-Service Tailscale | Select-Object Name,Status,StartType
```

Si le service est `Stopped`, le démarrer puis re-tester la connectivité :

```powershell
Start-Service Tailscale
Test-NetConnection 100.103.199.63 -Port 8888 | Select-Object TcpTestSucceeded
```

Le retour arrière est `Stop-Service Tailscale`, mais il coupe la connectivité privée du lab.

#### 7. Ouvrir Caldera pour piloter la campagne

Dans PowerShell du **PC hôte** :

```powershell
wsl -d Ubuntu -- bash -lc "sudo systemctl start caldera-tunnel"
wsl -d Ubuntu -- bash -lc "systemctl is-active caldera-tunnel"
```

Résultat attendu : `active`. Ouvrir ensuite Edge du **PC hôte** sur `http://127.0.0.1:8888`, puis contrôler dans Caldera que l’agent `PW-WIN11-01` du groupe `red` apparaît.

> Le tunnel sert à afficher le dashboard sur le PC hôte. Sandcat, lui, communique directement avec Caldera via Tailscale. Ne pas faire `wsl --shutdown`, car cela coupe le tunnel.

## 6. Linux — état de référence

- Endpoint : `PW-LINUX-01`.
- `wazuh-agent` : attendu `active`.
- `auditd` : attendu `active`.
- `tailscaled` : attendu `active`.
- Sandcat : géré par `purplewatch-sandcat.service`, attendu `active (running)` ; le service relance l’agent en cas d’arrêt.
- Règle audit générique : appels `execve`, clé `purplewatch_execve`.
- Fichier lu par l’agent Wazuh : `/var/log/audit/audit.log`.

Chaîne attendue :

```text
auditd → /var/log/audit/audit.log → agent Wazuh Linux → manager Wazuh → dashboard
```

## 7. État de validation technique au 24 septembre 2026

| Endpoint / technique | Émulation Caldera | Télémétrie locale | Wazuh | État à retenir |
|---|---|---|---|---|
| Windows T1082 | `systeminfo.exe` exécuté ; un essai Caldera a atteint `success`, un autre a atteint `timeout` | Sysmon Event ID 1 ; image `C:\Windows\System32\systeminfo.exe` | Règle `100100` déclenchée : `PurpleWatch: System Information Discovery via systeminfo.exe` | Détection PASS ; fiabilisation Caldera à retester avec un délai augmenté |
| Windows T1057 | Caldera `PW-OP-007-WIN11-T1057-BASELINE` : `success` à 12:16 ; retest réel : `success` à 13:32:26, agent `nekqel`, PID `8740` | Sysmon Event ID 1 : `C:\Windows\System32\tasklist.exe`; lors du baseline, parent PID `5936` = PID Caldera | Règle `100101`, niveau 6 : `PurpleWatch: Process Discovery via tasklist.exe`, alerte à 13:32:41 | **PASS de détection bout en bout** |
| Windows T1087.001 | Baseline Caldera : commande exécutée mais statut `failed` (retour Windows non nul) ; retest après tuning : `success` à 14:33:04, agent `nekqel`, PID `2664` | `net user` a listé les comptes locaux ; Wazuh a reçu les événements associés | Règle `100102`, niveau 6 : `PurpleWatch: Local Account Discovery via net user`, alertes fraîches à 14:34:06 | **PASS après tuning Caldera et retest** |
| Windows T1016 | Caldera `PW-OP-010-WIN11-T1016-LIVE-WAZUH` : `success` à 14:41:07, agent `nekqel`, PID `8784` | Exécution `ipconfig /all` par l’ability Windows | Règle `100103`, niveau 6 : `PurpleWatch: System Network Configuration Discovery`, alerte fraîche à 14:41:28 | **PASS de détection bout en bout** |
| Linux T1082 | Caldera `PW-T1082-Linux-OSInfo` exécuté avec `success` sur `PW-LINUX-01` (agent PID `2935`) | auditd : `uname -a`, `exe=/usr/bin/uname`, clé `purplewatch_execve`, PID `2936`, PPID `2935` | Règle locale `100104`, niveau 6, MITRE `T1082`, alerte visible à `10:55:20` puis retest post-tuning à `11:06:47` | **PASS de détection après tuning et retest** |
| Linux T1057 | `ps -ef` : retest `PW-OP-012-LINUX-T1057-POST-TUNING-RETEST`, `success` à 18:19:56 ; Atomic `PW-OP-013-LINUX-ATOMIC-T1057`, `success` à 19:29:11 ; post-redémarrage `PW-OP-014-LINUX-T1057-REBOOT-E2E`, `success` à 12:33:09 le 18/09 | auditd : `exe=/usr/bin/ps`, clé `purplewatch_execve`, `proctitle=ps -ef` ou `ps aux` | Règle locale `100105`, niveau 6, MITRE `T1057` ; test Atomic aussi vu par la règle native `92604` | **PASS de détection, validation Atomic et persistance confirmée après redémarrage** |
| Linux T1016 | Nouvelle ability `PW-T1016-Linux-NetworkConfig`, ID `d174545d-d59e-4363-87bc-578c7c19f832`, profil `PW-LINUX — T1016 Network Configuration Discovery` ; retest Caldera `success` le 24/09 à 00:43:44 UTC+2, PID affiché `5215` | Premier essai du 23/09 : auditd événement `4444` à 21:44:26.550 UTC, `EXECVE /usr/sbin/ip addr show`, `exe=/usr/bin/ip`, clé `purplewatch_execve`, PID `4389`, PPID Caldera `4388` | Règle Linux `100106`, niveau 6, MITRE `T1016` ; `wazuh-logtest` PASS sur l'événement `4444` ; nouvelle alerte à 00:43:47.794 UTC+2 le 24/09 | **PASS de détection au retest** ; vérifier encore le PID/PPID auditd de ce retest pour une corrélation forte et la latence exacte |
| Linux T1087.001 | Ability `PW-T1087.001-Linux-LocalAccountDiscovery`, ID `1a85d811-8cfd-4d1c-a83e-b496214e7857`, `/usr/bin/getent passwd` ; baseline Caldera `success` à 01:24:57 UTC+2, PID `5411` ; retest `success` à 01:44:17 UTC+2, PID `5476` | Baseline auditd `1790205916.904:5388`, PID `5412`, PPID `5411` ; retest auditd `1790207059.331:5466`, 23:44:19.331 UTC, `exe=/usr/bin/getent`, clé `purplewatch_execve`, PID `5477`, PPID Caldera `5476` | Règle Linux `100107`, niveau 6, MITRE T1087.001 ; `wazuh-logtest` validé ; alerte fraîche à 01:44:20.223 UTC+2 | **PASS E2E Caldera → auditd → Wazuh** ; ID d'alerte à archiver et heure de début exacte du lien à relever |

Profils Caldera actuellement disponibles :

- `PW-WIN11 — T1082 System Information Discovery`
- `PW-LINUX — T1082 OS Information`
- `PW-LINUX — T1057 Process Discovery`
- `PW-LINUX — Atomic T1057 Process Discovery`

### Détection Linux T1082 validée

La télémétrie auditd est correctement décodée par Wazuh (`auditd`). Avant tuning, elle atteignait seulement la règle générique `80700`, de niveau `0` : aucun événement n’était donc visible dans Threat Hunting.

La règle locale suivante a été ajoutée à `/var/ossec/etc/rules/purplewatch_p0_rules.xml` après sauvegarde du fichier :

```xml
<group name="purplewatch,linux,audit,">
  <rule id="100104" level="6">
    <if_sid>80700</if_sid>
    <field name="audit.exe" type="pcre2">^/usr/bin/uname$</field>
    <field name="audit.key">^purplewatch_execve$</field>
    <description>PurpleWatch: System Information Discovery via uname</description>
    <mitre><id>T1082</id></mitre>
    <group>purplewatch_p0,discovery,</group>
  </rule>
</group>
```

Validation avant mise en production : `wazuh-analysisd -t` sans erreur, puis `wazuh-logtest` a attribué la règle `100104`, le niveau `6` et la technique `T1082`. Le retest réel a ensuite généré une seconde alerte Wazuh, ce qui clôt la boucle de détection.

### Détection Linux T1057 validée et persistance Sandcat

L’ability `PW-T1057-Linux-ProcessDiscovery` exécute `ps -ef`. auditd enregistre l’appel `execve` avec `exe=/usr/bin/ps`, `proctitle=ps -ef` et la clé `purplewatch_execve`.

La règle locale `100105` cible cet exécutable et cette clé avec la technique MITRE `T1057`. Le retest `PW-OP-012-LINUX-T1057-POST-TUNING-RETEST` a obtenu `success` à 18:19:56, suivi de l’alerte Wazuh `100105`, niveau 6, à 18:20:26.

Le plugin Atomic Red Team a ensuite validé la même couverture avec l’ability `Process Discovery - ps` (`ps` puis `ps aux`). `PW-OP-013-LINUX-ATOMIC-T1057` a obtenu `success` à 19:29:11 ; Wazuh a généré à la fois l’alerte PurpleWatch `100105` et la règle native `92604` à 19:29:19. Le fichier temporaire `/tmp/loot.txt` était absent après exécution, ce qui confirme le nettoyage.

Sandcat Linux est maintenant rendu persistant par `/etc/systemd/system/purplewatch-sandcat.service`. Le service dépend du réseau et de Tailscale, redémarre automatiquement et autorise `AF_NETLINK`, nécessaire à la lecture des routes par Sandcat. Validation : `active (running)` et `Beacon (HTTP): ALIVE` vers Caldera.

Après redémarrage contrôlé de `PW-LINUX-01`, le service était encore `active`, Sandcat a repris ses beacons puis l’opération `PW-OP-014-LINUX-T1057-REBOOT-E2E` a obtenu `success` à 12:33:09 (18/09). auditd a enregistré `ps -ef` avec `tty=(none)`, `exe=/usr/bin/ps` et la clé `purplewatch_execve`; Wazuh a déclenché `100105`, niveau 6, à 12:33:35. La persistance et la boucle Caldera → auditd → Wazuh sont donc prouvées après reboot.

### Détection Windows T1057 validée

L’ability Caldera `PW-T1057-Windows-ProcessDiscovery` exécute `tasklist.exe` avec le profil `PW-WIN11 — T1057 Process Discovery`. Le baseline a établi la corrélation Caldera → Sysmon : PID Caldera `5936` = `ParentProcessId` Sysmon de `tasklist.exe`.

Le retest avec Wazuh actif a déclenché l’alerte `100101`, niveau `6`, à `13:32:41`, quinze secondes après l’opération Caldera réussie de `13:32:26`. Cette preuve valide la chaîne Caldera → Sysmon → Wazuh pour T1057.

### Détection Windows T1087.001 validée

L’ability `PW-T1087.001-Windows-LocalAccountDiscovery` utilise `net user`. Le baseline a bien listé les comptes locaux mais Caldera a signalé `failed` parce que Windows a retourné un code non nul avec le message « Des erreurs ont affecté l’exécution de la commande ».

Le tuning minimal a remplacé la commande par `net user; exit 0`. Il est documenté comme une normalisation du retour pour Caldera : le texte de sortie reste conservé et la limite est explicitement connue. Le retest `PW-OP-009-WIN11-T1087.001-POST-TUNING-RETEST` a obtenu `success` à `14:33:04`, puis Wazuh a généré la règle `100102`, niveau `6`, à `14:34:06`.

### Détection Windows T1016 validée

L’ability `PW-T1016-Windows-NetworkConfigurationDiscovery` et le profil `PW-WIN11 — T1016 Network Configuration Discovery` exécutent `ipconfig /all`, sans modifier la configuration réseau. L’opération `PW-OP-010-WIN11-T1016-LIVE-WAZUH` a obtenu `success` à `14:41:07`, puis Wazuh a déclenché la règle `100103`, niveau `6`, à `14:41:28`.

## 8. Contraintes de ressources et stratégie de démonstration

Le PC hôte possède environ 8 Go de RAM. Les deux VM locales ne doivent pas être utilisées simultanément pendant une démonstration.

| Phase | Éléments locaux actifs | Objectif |
|---|---|---|
| Campagne Windows | `PurpleWatch-Windows` ; Wazuh VM arrêté | Exécuter les techniques Windows, conserver Sysmon/Wazuh Agent |
| Exploitation Windows | `PurpleWatch-Wazuh` ; Windows VM arrêté | Consulter les événements et preuves Wazuh |
| Campagne Linux | `PurpleWatch-Wazuh` + serveurs Scaleway | auditd, Caldera, détection et retest Linux |

Ne pas démarrer Wazuh local et Windows local ensemble pendant la soutenance. Un retest technique simultané est toléré uniquement sur une courte durée, avec surveillance mémoire, puis retour au fonctionnement séquentiel.

## 9. Feuille de route de finalisation — objectif 17 septembre 2026

### Priorité de travail

La priorité n’est pas d’augmenter rapidement le nombre d’attaques. Chaque technique doit suivre la boucle complète : émulation, télémétrie, détection, classement PASS/GAP, amélioration et retest.

| Date cible | Objectif | Résultat concret attendu |
|---|---|---|
| 13–14 septembre | Terminer les retests T1082 Windows et Linux | Linux : **PASS** Caldera → auditd → règle `100104` → Wazuh. Windows : détection `100100` prouvée ; fiabilisation Caldera à terminer. |
| 14 septembre | Étendre la couverture Windows | Playbooks Caldera et preuves pour T1057, T1087.001 et T1016 ; valider les règles `100101` à `100103`. |
| 15 septembre | Consolider les livrables techniques | Matrice de couverture ATT&CK, playbooks, runbooks et After-Action Report (AAR) initial. |
| 16 septembre | Préparer la soutenance | Schéma d’architecture, support de 20 minutes, scénario de démonstration, captures de secours et répartition des prises de parole. |
| 17 septembre | Finaliser et répéter | Vérification finale, répétition chronométrée, corrections mineures et archivage des preuves. |

### Définition de terminé

PurpleWatch sera considéré prêt lorsque les éléments suivants seront archivés :

1. Deux démonstrations complètes et reproductibles : une Windows et une Linux.
2. Une matrice ATT&CK indiquant, pour chaque technique, l’endpoint, la commande, la télémétrie, la règle, le résultat et la preuve.
3. Les playbooks Caldera et runbooks associés.
4. Un AAR expliquant les GAP rencontrés, les corrections et les retests.
5. Un support et un scénario de soutenance de 20 minutes, avec preuves de secours.

### Tâche immédiate

Construire la matrice de couverture ATT&CK avec les quatre preuves disponibles : T1082 Windows, T1057 Windows, T1087.001 Windows, T1016 Windows, ainsi que T1082 Linux. Préparer ensuite les playbooks, runbooks et l’After-Action Report (AAR).

## 10. Procédure de démarrage soutenance

1. Démarrer `PW-CALDERA-01` sur Scaleway, puis vérifier `caldera.service`.
2. Sur le PC hôte, démarrer `caldera-tunnel.service` dans WSL.
3. Ouvrir Edge hôte : `http://127.0.0.1:8888`.
4. Démarrer uniquement les composants prévus pour la phase de démonstration.
5. Vérifier chaque service avant l’exécution d’une technique.

## 11. Journal des changements

| Date | Changement | Motif | Validation | Retour arrière |
|---|---|---|---|---|
| 13/09/2026 | Création de `caldera.service` sur PW-CALDERA-01 | Caldera s’arrêtait à la fermeture SSH | service `active`, Python écoute sur `:8888` | `sudo systemctl disable --now caldera` |
| 13/09/2026 | Restauration de `caldera-tunnel.service` WSL | Dashboard Caldera à nouveau accessible depuis Edge hôte | service `active`, dashboard `127.0.0.1:8888` affiché | `sudo systemctl stop caldera-tunnel` |
| 13/09/2026 | Création des profils Caldera Windows et Linux T1082 | Émulations séparées, reproductibles et pédagogiques | profils visibles et agents Windows/Linux `alive` | supprimer uniquement après archivage des playbooks |
| 13/09/2026 | Rétablissement de Tailscale sur PW-WIN11-01 | Service Tailscale arrêté malgré le démarrage automatique ; Caldera inaccessible depuis Windows | service `Running`, pair Caldera visible et TCP/8888 à `True` | `Stop-Service Tailscale` |
| 13/09/2026 | Ajout de la feuille de route au 17 septembre | Concentrer le travail sur les livrables P.1 et la soutenance | version 0.3 du document | restaurer la version précédente du document |
| 13/09/2026 | Création de ce document | Éviter les divergences d’architecture et conserver les décisions | à mettre à jour après chaque changement | n/a |
| 14/09/2026 | Ajout de la règle Linux `100105` et retest T1057 | Transformer la télémétrie auditd de `ps` en alerte ATT&CK visible | Caldera `success` + Wazuh `100105`, niveau 6 | restaurer le fichier de règles sauvegardé puis recharger Wazuh |
| 14/09/2026 | Création de `purplewatch-sandcat.service` | Éviter la relance manuelle de Sandcat Linux | service `active (running)` + beacon HTTP `ALIVE` | `sudo systemctl disable --now purplewatch-sandcat.service` |
| 14/09/2026 | Validation Atomic Red Team Linux T1057 | Vérifier une ability standardisée sans modification durable | Caldera `success`, Wazuh `100105` et `92604`, nettoyage confirmé | supprimer le profil/adversaire Atomic uniquement après archivage |
| 18/09/2026 | Libellé `100105` généralisé en « via ps » | Couvrir fidèlement `ps -ef`, `ps` et `ps aux` | `wazuh-analysisd -t`, redémarrage manager `active` | restaurer la sauvegarde `.before-100105-label` puis recharger Wazuh |
| 18/09/2026 | Test E2E Linux après redémarrage | Prouver la persistance opérationnelle de Sandcat et la détection sans intervention manuelle | `PW-OP-014-LINUX-T1057-REBOOT-E2E` : Caldera `success` à 12:33:09 ; Wazuh `100105` à 12:33:35 | `sudo systemctl disable --now purplewatch-sandcat.service` |
| 24/09/2026 | Ajout de la règle Linux `100106` pour T1016 | Élever la télémétrie `ip` auditd en alerte dédiée | sauvegarde `.bak-T1016` ; `wazuh-analysisd -t` ; `wazuh-logtest` règle `100106`/T1016 ; retest Caldera `success` et alerte Wazuh fraîche | restaurer `.bak-T1016` puis valider et redémarrer le manager |
| 24/09/2026 | Ajout de la règle Linux `100107` pour T1087.001 | Détecter `getent` instrumenté par auditd | sauvegarde `.bak-T1087-001` ; `wazuh-analysisd -t`, `wazuh-logtest` sur baseline `5388` ; retest Caldera `success`, alerte Wazuh fraîche `100107` | restaurer `.bak-T1087-001` puis valider et redémarrer le manager |

## 12. Règle de mise à jour

Avant toute modification : vérifier ce document.

Après toute modification validée : ajouter une ligne au journal avec le motif, le test de validation et le retour arrière.

## 13. Validation Windows de reprise — 19 septembre 2026

### État opérationnel retenu

- L'agent Sandcat Windows a été relancé avec le script manuel `C:\\Users\\Public\\Start-PurpleWatch-Sandcat.cmd` ; processus constaté : `splunkd.exe`, PID `5188`.
- L'agent Caldera actif `ezyrym` sur `PW-WIN11-01` est utilisé pour les retests ci-dessous.
- La tâche planifiée `PurpleWatch-Sandcat` reste configurée mais n'est pas retenue comme preuve de persistance : elle a retourné `0x8007042B` (processus terminé de manière inattendue). Le script manuel est la procédure de secours de soutenance.
- Un arrêt/reprise de `WazuhSvc` sur Windows a rétabli la collecte après une période sans nouveaux événements centralisés. Sysmon et la connectivité vers `192.168.56.105:1514` étaient actifs.

### Preuves E2E rapides

| Technique | Caldera | Wazuh | Délai Caldera → alerte | Résultat |
|---|---|---|---:|---|
| T1082 Windows | `PW-T1082-Windows-SystemInfo` `success` à 19:03:08 | règle `100100`, niveau 6 à 19:03:44.817 | 36,817 s | PASS |
| T1057 Windows | `PW-T1057-Windows-ProcessDiscovery` `success` à 19:09:31 | règle `100101`, niveau 6 à 19:09:47.526 | 16,526 s | PASS |

### Décision de démonstration

Le démonstrateur Windows est de nouveau viable : Sandcat manuel → Caldera → Sysmon → Wazuh est validé en moins d'une minute. Pour réduire le risque, garder les deux VMs Windows/Wazuh actives uniquement pendant la séquence de démonstration et conserver captures et vidéo de secours.

## 14. Validation Linux T1016 — 23–24 septembre 2026

L'ability dédiée `PW-T1016-Linux-NetworkConfig` (ID `d174545d-d59e-4363-87bc-578c7c19f832`, `linux`/`sh`) et son profil exécutent `/usr/sbin/ip addr show`. Ce chemin est un lien symbolique vers `/usr/bin/ip`. Le premier essai `success` du 23/09 à 23:43:54 UTC+2 n'a pas produit d'alerte PurpleWatch T1016. L'événement auditd `4444`, à 21:44:26.550 UTC, montre `pid=4389`, `ppid=4388` (PID Caldera du premier essai), `exe=/usr/bin/ip`, `EXECVE` avec `a1=addr`, `a2=show` et `key=purplewatch_execve`.

Une nouvelle règle Linux `100106` (niveau 6, `if_sid=80700`, `audit.exe=^/usr/bin/ip$`, `audit.key=^purplewatch_execve$`, MITRE `T1016`) a été ajoutée à `/var/ossec/etc/rules/purplewatch_p0_rules.xml` après sauvegarde `.bak-T1016`. La syntaxe `wazuh-analysisd -t` est valide ; le test du `SYSCALL` brut de l'événement `4444` par `wazuh-logtest` donne `audit.command=ip`, `audit.exe=/usr/bin/ip`, `audit.key=purplewatch_execve`, puis `100106`/niveau 6/T1016. Cette règle couvre toute exécution de `ip` avec cette clé, et pas seulement `addr show`.

Au retest du 24/09, Caldera affiche `success` à 00:43:44 UTC+2 sur `PW-LINUX-01` (PID affiché `5215`) et Wazuh affiche une nouvelle alerte `100106` à 00:43:47.794 UTC+2. L'écart entre ces horodatages affichés est de 3,794 s ; ce n'est pas encore une mesure de latence E2E normalisée fondée sur l'heure de début exacte du lien Caldera. Le document de l'alerte et l'événement auditd propres à ce retest restent à archiver pour vérifier le couple PID/PPID et l'identifiant d'alerte. La preuve du premier essai ne doit pas être présentée comme la télémétrie du retest.

## 15. Programme d'amélioration issu de la revue coach — état au 24 septembre 2026

Le schéma détaillé des zones, ports, réseaux et données est dans `purplewatch-schema-lab-hybride.md`. Le contrat commun de journal JSONL, son exemple T1016 incomplet et les définitions de métriques sont dans `purplewatch-journal-attaques.md`. Ces documents sont des livrables de référence ; la validation des flux exacts en conditions de soutenance reste une vérification de pré-vol.

| Ordre | Travail | État et critère de clôture |
| --- | --- | --- |
| 1 | Schéma hybride renforcé | Document produit ; vérifier adresses/ports au pré-vol. |
| 2 | Journal d'attaque normalisé | Contrat et exemple produits ; renseigner les identifiants et heures exacts des prochains runs. |
| 3 | T1016 et T1087.001 Linux | Alertes fraîches `100106` et `100107` après retests ; auditd T1087.001 corrélé par PPID. Pour T1016, archiver encore auditd du retest ; pour les deux, relever les ID d'alerte. |
| 4 | Adversaries dédiés et scénario combiné | Profils individuels existants ; scénario de séquence à créer et à exporter. |
| 5 | Latence, P50, P95 | Aucun percentile publié sans répétitions et heures comparables. |
| 6 | Corrélation même hôte T1082 + T1057 + T1016 en cinq minutes | Après vérification des trois détections unitaires et du format des événements ; tester les alertes positives et hors fenêtre. |
| 7 | Soutenance | Mettre à jour slides après collecte des preuves et des métriques, sans valeur fictive. |

La diversité tactique reste une exigence distincte : après les scénarios Discovery, concevoir un T1059 (Execution) strictement contrôlé et non destructif dans le laboratoire, puis seulement envisager T1119 (Collection) sur répertoire de test et T1036 (Defense Evasion) inoffensif. Valider chaque nouvelle technique sur la boucle Caldera → télémétrie → Wazuh avant de l'annoncer couverte.

## 16. Validation Linux T1087.001 — 24 septembre 2026

L'ability dédiée `PW-T1087.001-Linux-LocalAccountDiscovery` (ID `1a85d811-8cfd-4d1c-a83e-b496214e7857`) exécute `/usr/bin/getent passwd`. Caldera a réussi le baseline à 01:24:57 UTC+2, PID `5411`. Auditd confirme l'événement complet `1790205916.904:5388` à 23:25:16.904 UTC le 23/09 : `pid=5412`, `ppid=5411`, `exe=/usr/bin/getent`, `a1=passwd`, clé `purplewatch_execve`. Le numéro court `5388` seul n'identifie pas un événement sans son horodatage, car un autre événement `sed` portait ce même numéro dans les journaux consultés.

Après sauvegarde `.bak-T1087-001`, ajout de la règle Linux `100107` (niveau 6, parent `80700`, champs `audit.exe=^/usr/bin/getent$`, `audit.key=^purplewatch_execve$`, MITRE `T1087.001`). `wazuh-analysisd -t` n'a signalé aucune erreur et `wazuh-logtest` sur le SYSCALL brut de l'événement baseline a retourné `100107`, niveau 6, T1087.001. La règle cible toutes les exécutions de `getent` avec la clé du lab, pas seulement l'argument `passwd`.

Au retest du 24/09, Caldera indique `success` à 01:44:17 UTC+2 sur `PW-LINUX-01` avec PID affiché `5476`; auditd `1790207059.331:5466` à 23:44:19.331 UTC le 23/09 porte `pid=5477`, `ppid=5476`, `exe=/usr/bin/getent`, `a1=passwd`, clé `purplewatch_execve`. Wazuh montre l'alerte fraîche `100107`, niveau 6, à 01:44:20.223 UTC+2. La chaîne E2E est corrélée sur ce run. L'écart des heures Caldera et Wazuh affichées est 3,223 s ; il ne remplace pas la latence E2E calculée depuis le début exact du lien. L'ID d'alerte reste à archiver.

## 17. Enrichissement demandé par le coach : quatre autres tactiques

Les quatre techniques Discovery déjà présentes sur Windows et Linux ne satisfont pas à elles seules la demande de diversification. La cible de conception est **quatre tactiques supplémentaires**, avec une technique distincte chacune. Les lignes suivantes sont **planifiées, non validées** ; choisir les commandes définitives et la télémétrie avant de créer les abilities, puis exiger la boucle E2E et un test négatif pertinent. Les ID ci-dessous sont ceux de MITRE ATT&CK Enterprise.

| Tactique supplémentaire | Technique candidate | Émulation sûre dans le lab | Télémétrie et point de vigilance |
| --- | --- | --- | --- |
| Execution | [T1059.004 — Unix Shell](https://attack.mitre.org/techniques/T1059/004/) | Script `sh` contrôlé qui écrit un marqueur non sensible dans un espace de test. | auditd `execve`, arguments/parent et marqueur ; l'executor `sh` de Caldera crée déjà du bruit : ne pas assimiler chaque shell à ce scénario. |
| Collection | [T1119 — Automated Collection](https://attack.mitre.org/techniques/T1119/) | Collecte automatisée d'un petit jeu de fichiers factices dans un répertoire dédié, puis nettoyage. | `execve` de l'outil et journalisation des fichiers de test ; `execve` seul ne prouve pas quels fichiers ont été lus. |
| Defense Evasion | [T1036.005 — Match Legitimate Resource Name or Location](https://attack.mitre.org/techniques/T1036/005/) | Exécutable de test inoffensif placé sous un nom imitant un binaire courant dans un répertoire isolé, sans toucher aux binaires système. | Comparer chemin complet, hash et contexte au nom apparent ; autoriser uniquement le chemin de test. |
| Credential Access | [T1552.001 — Credentials In Files](https://attack.mitre.org/techniques/T1552/001/) | Accès à un fichier de leurre contenant seulement une fausse chaîne de test, dans un répertoire isolé. | Ajouter une télémétrie ciblée des accès au fichier et vérifier le contenu factice ; `execve` du lecteur ne prouve pas l'accès au fichier. |

Ordre conseillé : T1059.004 en premier pour démontrer une deuxième tactique, puis T1119 sur fichiers factices, T1036.005 et enfin T1552.001 avec leurre. Pour chacune : ability/adversary dédiés, une exécution baseline, règle Wazuh spécifique, test de règle, retest et journal JSONL. Ne pas annoncer quatre tactiques supplémentaires comme couvertes avant validation de chacune.

## 17. Execution Linux T1059.004 — validation du 24 septembre 2026

Ability Caldera `PW-T1059.004-Linux-UnixShell`, commande `/bin/sh -c 'printf PW-T1059-EXECUTION-OK'`, endpoint `PW-LINUX-01`. Premier lancement Caldera `success` à 02:03:49 UTC+2, PID 5553 ; auditd deuxième shell PID 5554, PPID 5553, événement `1790208256.770:5556`, `exe=/usr/bin/dash`, `a0=/bin/sh`, `a1=-c`, marqueur encodé dans `a2`. Aucun avertissement Wazuh à ce stade.

La première version de la règle `100108` ciblait `audit.type=EXECVE`. `wazuh-logtest` sur la ligne isolée a donné `100108` ; un `a2` différent est resté à `80700`. Pourtant le retest Caldera `success` à 02:21:06 UTC+2 (PID 5700, auditd `1790209300.114:5708`, PID 5701, PPID 5700) n'a généré aucune alerte. Le contrôle T1082 lancé à 02:34:12 UTC+2 a généré `100104` à 02:34:32.493, confirmant la chaîne de collecte. Son `full_log` prouve que Wazuh agrège les lignes SYSCALL et EXECVE sous `audit.type=SYSCALL`. La condition `EXECVE` de la règle initiale excluait ainsi les événements réels.

Correction appliquée par l'opérateur : règle `100108` de niveau 6, MITRE T1059.004, parent `80700`, `audit.type=SYSCALL`, `audit.exe=/usr/bin/dash`, `audit.key=purplewatch_execve`, `audit.execve.a0=/bin/sh`, `audit.execve.a1=-c` et correspondance PCRE2 du marqueur `a2=7072696E74662050572D54313035392D455845435554494F4E2D4F4B` dans le log regroupé. Après validation et redémarrage du manager, retest Caldera `success` à 02:42:37 UTC+2 (PID 5807) et alerte `100108` à 02:42:49.269 UTC+2 sur `PW-LINUX-01` : **PASS de détection de bout en bout et deuxième tactique validée (Execution)**. Écart des heures affichées : 12,269 s ; latence E2E normalisée `started_at` → `alerted_at` encore indéterminée ; événement auditd et identifiant précis de l'alerte du retest à archiver. Aucun P50/P95 calculable sur cette seule réussite.
