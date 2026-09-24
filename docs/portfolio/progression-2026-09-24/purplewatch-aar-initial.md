# PurpleWatch — After-Action Report (AAR) initial

**Période couverte :** 13–24 septembre 2026
**Périmètre :** laboratoire PurpleWatch autorisé.

## 1. Objectif

Valider de bout en bout les techniques ATT&CK émises par MITRE Caldera : exécution sur endpoint, télémétrie, analyse Wazuh, amélioration lorsque nécessaire, puis retest.

## 2. Architecture utilisée

- Caldera : `PW-CALDERA-01` sur Scaleway.
- Endpoint Windows : `PW-WIN11-01`, Sysmon + Wazuh Agent + Sandcat.
- Endpoint Linux : `PW-LINUX-01`, auditd + Wazuh Agent + Sandcat.
- SIEM : `PW-WAZUH-01` local, dashboard accessible depuis Edge hôte.
- Connectivité : Tailscale, réseau privé chiffré.

## 3. Résultats

| Technique | Endpoint | Résultat | Détection |
|---|---|---|---|
| T1082 | Windows | PASS de détection | `100100` |
| T1057 | Windows | PASS | `100101` |
| T1087.001 | Windows | PASS après tuning Caldera | `100102` |
| T1016 | Windows | PASS | `100103` |
| T1082 | Linux | PASS après tuning Wazuh | `100104` |
| T1057 | Linux | PASS après ajout de la règle Wazuh ; validation Atomic Red Team et redémarrage contrôlé | `100105` et `92604` |
| T1016 | Linux | PASS de détection après ajout de la règle ; événement auditd du retest à archiver | `100106` |
| T1087.001 | Linux | PASS de détection après ajout de la règle ; événement auditd du retest à archiver | `100107` |

## 4. Incidents, analyse et corrections

### Linux T1082 — détection silencieuse

**Constat :** auditd enregistrait bien `uname`, mais Wazuh appliquait seulement la règle générique `80700` de niveau 0.
**Cause :** aucune règle locale ne transformait l’exécution `uname` instrumentée en alerte ATT&CK.
**Correction :** ajout de la règle `100104`, ciblant `audit.exe=/usr/bin/uname` et `audit.key=purplewatch_execve`.
**Retest :** alerte T1082 niveau 6 visible dans Wazuh : PASS.

### Windows T1087.001 — retour Caldera non nul

**Constat :** `net user` listait les comptes locaux mais Caldera affichait `failed`.
**Cause :** Windows retournait un code non nul accompagné du message indiquant que des erreurs avaient affecté l’exécution.
**Correction :** commande d’ability normalisée en `net user; exit 0`.
**Limite :** ce réglage normalise le statut Caldera ; la sortie de commande reste l’élément de contrôle fonctionnel.
**Retest :** Caldera `success` et alerte Wazuh `100102` : PASS.

### Windows T1057 — preuve centralisée manquante au baseline

**Constat :** Sysmon avait prouvé `tasklist.exe`, mais le Manager Wazuh était arrêté lors du baseline.
**Correction :** retest court avec Windows et Wazuh simultanément actifs.
**Retest :** Caldera `success` à 13:32:26, Wazuh `100101` à 13:32:41 : PASS.

### Linux T1057 — détection de processus et test Atomic

**Constat :** auditd enregistrait déjà les appels `execve` de `ps` avec la clé `purplewatch_execve`, mais aucune règle PurpleWatch spécifique ne générait une alerte de découverte de processus.
**Correction :** ajout de la règle locale `100105`, ciblant `audit.exe=/usr/bin/ps` et `audit.key=purplewatch_execve`. Le libellé a été rendu générique : « PurpleWatch: Process Discovery via ps ».
**Retest PurpleWatch :** l’opération `PW-OP-012-LINUX-T1057-POST-TUNING-RETEST` a obtenu `success` à 18:19:56 ; Wazuh a généré la règle `100105`, niveau 6, à 18:20:26 : PASS.
**Validation Atomic :** l’ability Atomic `Process Discovery - ps` a exécuté `ps` et `ps aux`, puis le nettoyage `rm /tmp/loot.txt`. L’opération `PW-OP-013-LINUX-ATOMIC-T1057` a obtenu `success` à 19:29:11 ; Wazuh a déclenché `100105` et sa règle native `92604` à 19:29:19. Le fichier temporaire était absent après le test : PASS.

**Persistance vérifiée :** après un redémarrage contrôlé de `PW-LINUX-01`, `purplewatch-sandcat.service` est revenu `active` et Sandcat a repris ses beacons. L’opération `PW-OP-014-LINUX-T1057-REBOOT-E2E` a ensuite obtenu `success` à 12:33:09 le 18 septembre ; auditd a enregistré `ps -ef` et Wazuh a généré `100105`, niveau 6, à 12:33:35 : PASS complet post-redémarrage.

## 5. Limites et suites

- Le PC hôte, limité à environ 8 Go de RAM, impose des campagnes séquentielles ; les retests Windows/Wazuh simultanés doivent rester très courts.
- La persistance Sandcat Linux est assurée par `purplewatch-sandcat.service` avec redémarrage automatique et a été validée par un test E2E après redémarrage.
- Préparer une vidéo ou captures de secours pour la soutenance.
- Répéter un scénario Windows et un scénario Linux en respectant le plan de démonstration.

## 6. Conclusion

PurpleWatch démontre une démarche de validation défensive : les scénarios ATT&CK sont exécutés par Caldera, observés par Sysmon ou auditd, puis détectés par des règles Wazuh documentées. Les GAP constatés ont été corrigés et validés par retest.

## Addendum — reprise de collecte Windows du 19 septembre 2026

### Incident

Un test Windows a été exécuté avec succès dans Caldera, sans alerte Wazuh récente. Les services `WazuhSvc` et `Sysmon64` étaient pourtant `RUNNING`, et le port manager `192.168.56.105:1514` était accessible depuis Windows. La cause opérationnelle retenue est une session de collecte Wazuh bloquée ou vieillissante.

### Remédiation et retest

`WazuhSvc` a été redémarré sans toucher à Sysmon ni à Sandcat. Les retests suivants sont passés :

- T1082 : Caldera 19:03:08 ; Wazuh `100100` 19:03:44.817 ; 36,817 s.
- T1057 : Caldera 19:09:31 ; Wazuh `100101` 19:09:47.526 ; 16,526 s.

### Décision

Le scénario Windows est retenu pour une démonstration courte. Le script manuel `C:\\Users\\Public\\Start-PurpleWatch-Sandcat.cmd` est la procédure de reprise Sandcat ; la tâche planifiée demeure un point à corriger, car son dernier résultat connu est `0x8007042B`.

## Addendum — Linux T1016 du 23–24 septembre 2026

**GAP initial :** l'ability dédiée `PW-T1016-Linux-NetworkConfig` (ID `d174545d-d59e-4363-87bc-578c7c19f832`) a exécuté `/usr/sbin/ip addr show` avec `success`, mais aucune alerte T1016 n'était visible. L'événement auditd `4444` du premier essai montre `exe=/usr/bin/ip` (chemin réel du lien symbolique), `key=purplewatch_execve`, `pid=4389`, `ppid=4388` (PID Caldera). Un test témoin T1082 a produit une nouvelle alerte `100104`, confirmant la chaîne de collecte existante.

**Correction :** ajout de la règle Linux `100106` sur `audit.exe=/usr/bin/ip` et `audit.key=purplewatch_execve`, niveau 6, MITRE `T1016`. Sauvegarde préalable `.bak-T1016`, validation de syntaxe avec `wazuh-analysisd -t` puis `wazuh-logtest` sur le `SYSCALL` brut de l'événement `4444` : règle `100106` sélectionnée. La règle détecte `ip` en général avec la clé du laboratoire ; les arguments `addr show` ne font pas partie de son filtre.

**Retest :** le 24/09 à 00:43:44 UTC+2, Caldera indique `success` sur `PW-LINUX-01`, PID affiché `5215`. Wazuh affiche une nouvelle alerte `100106` de niveau 6 à 00:43:47.794 UTC+2 : PASS de détection. L'écart de 3,794 s entre les heures affichées ne représente pas une latence E2E normalisée. Reste à archiver le document d'alerte et la télémétrie auditd propres à ce retest pour vérifier le couple PID/PPID.

## Addendum — Linux T1087.001 du 24 septembre 2026

**Baseline :** l'ability `PW-T1087.001-Linux-LocalAccountDiscovery`, ID `1a85d811-8cfd-4d1c-a83e-b496214e7857`, a exécuté `/usr/bin/getent passwd` avec `success` à 01:24:57 UTC+2, PID Caldera `5411`. Auditd `1790205916.904:5388` à 23:25:16.904 UTC relève `pid=5412`, `ppid=5411`, `exe=/usr/bin/getent`, clé `purplewatch_execve` ; pas d'alerte dédiée à ce stade.

**Correction :** après sauvegarde `.bak-T1087-001`, la règle `100107`, niveau 6, MITRE T1087.001, cible `audit.exe=/usr/bin/getent` et `audit.key=purplewatch_execve`. `wazuh-analysisd -t` n'a signalé aucune erreur ; `wazuh-logtest` sur la ligne SYSCALL brute a sélectionné `100107`/T1087.001. Cette règle couvre toutes les exécutions `getent` avec la clé du lab, sans vérifier l'argument `passwd`.

**Retest :** Caldera `success` à 01:44:17 UTC+2 sur `PW-LINUX-01`, PID affiché `5476` ; Wazuh affiche une nouvelle alerte `100107` à 01:44:20.223 UTC+2. PASS de détection ; écart affiché 3,223 s, qui n'est pas une latence E2E normalisée. Le SYSCALL et l'ID de l'alerte propres au retest restent à archiver pour la corrélation forte.

## Addendum — T1059.004 Linux, 24 septembre 2026

Caldera a exécuté le shell contrôlé à 02:03:49 puis à 02:21:06 UTC+2 ; auditd a enregistré les deux exécutions, mais `100108` ne se déclenchait pas. Test sur `EXECVE` isolé positif et test de marqueur différent négatif. Cause : en production Wazuh regroupe `SYSCALL` et `EXECVE` en événement principal `SYSCALL`. Le contrôle `uname` T1082 à 02:34:12 a déclenché `100104` à 02:34:32.493 et montré la structure réelle de `full_log`. Correction `100108` sur l'événement `SYSCALL` regroupé, avec `exe=/usr/bin/dash`, clé audit, arguments shell et marqueur hexadécimal ; retest à 02:42:37, alerte `100108` à 02:42:49.269. **PASS Execution T1059.004.** Écart affiché 12,269 s, non utilisé comme latence E2E rigoureuse.
