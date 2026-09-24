# Passation à Codex — PurpleWatch, 24 septembre 2026

Le vrai dépôt local est C:\Users\HP x360\Desktop\spe cybersecu holberton\portfolio sybrsecurite. La présente archive est une photographie sans métadonnées Git. Elle ne prouve ni la branche ni l'état actuel de GitHub.

1. Ouvrir le vrai dépôt dans Codex et consulter les éventuelles consignes AGENTS.md, puis git status, la branche et les remotes. Préserver tous les changements locaux et historiques plus récents.
2. Comparer les livrables joints dans docs/portfolio/progression-2026-09-24 et les règles proposées dans detections/wazuh/purplewatch_p0_rules.xml avec le dépôt réel. Intégrer uniquement les écarts manquants ; signaler les contradictions.
3. Vérifier les règles 100106 (T1016 Linux, ip), 100107 (T1087.001 Linux, getent) et 100108 (T1059.004 Linux, événement auditd SYSCALL+EXECVE regroupé). Comparer la règle proposée avec celle effectivement déployée sur PW-WAZUH-01 avant de déclarer une identité exacte.
4. Actualiser l'architecture hybride avec la topologie de référence : Caldera et Linux Scaleway, Wazuh et Windows VirtualBox, réseau Tailscale, agent TCP 1514, Caldera HTTP 8888 via tunnel SSH pour le navigateur. Ne pas réécrire les preuves historiques.
5. Conserver le statut vérifié : T1059.004 Caldera success à 02:42:37 GMT+2, PID 5807 ; Wazuh règle 100108 à 02:42:49.269 GMT+2. L'écart des heures affichées est 12,269 s ; latence E2E exacte, started_at, P50 et P95 restent inconnus. Collection, Defense Evasion et Credential Access restent à tester.
6. Vérifier XML, JSONL et contrôles du dépôt ; ne pas ajouter secrets, clés, journaux bruts ou payloads. Le test natif Wazuh de la future copie de dépôt doit être refait avant déploiement.
7. Montrer le diff. Si les accès GitHub sont disponibles, créer une branche dédiée, commit, push, ouvrir une PR et transmettre son lien. Aucun push forcé ni écrasement de la branche courante. Si l'accès manque, laisser une branche locale et les commandes exactes.

Suite de la feuille de route : scénarios T1119 sur fichiers factices, T1036.005 isolé, T1552.001 sur faux secrets uniquement ; automatisation, répétitions pour P50/P95, corrélation T1082+T1057+T1016 sur cinq minutes, mise à jour des slides. Aucun PASS sans retest et preuve.
