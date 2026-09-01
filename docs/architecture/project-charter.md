# PW-001 — Project Charter

## Mission

PurpleWatch est une plateforme Purple Team de laboratoire qui répond de façon traçable à la question : « cette technique MITRE ATT&CK a-t-elle été testée et détectée ? » Elle corrèle les essais contrôlés, la télémétrie, les détections, la couverture, les gaps et les retests.

## Objectifs

- Fournir une référence professionnelle démontrant les pratiques cybersécurité, DevSecOps, détection et Purple Team.
- Mesurer la couverture de détection de techniques ATT&CK autorisées et non destructrices.
- Produire des preuves reproductibles, sûres, anonymisées et exploitables dans un portfolio.

## Utilisateurs et parties prenantes

Analyste SOC, Detection Engineer, Purple Teamer, mainteneur du laboratoire et évaluateur du portfolio.

## Critères de succès du MVP

- Cinq techniques ATT&CK de laboratoire, non destructrices et explicitement autorisées.
- Pour chaque test : une preuve de télémétrie, détection ou gap, liée à la technique.
- Couverture et gaps calculables ; amélioration puis retest traçables.
- API, base PostgreSQL, interface web et documentation cohérentes avec les ADR.

## Contraintes non négociables

Laboratoire isolé ; aucune exécution arbitraire de commandes à distance ; aucun secret, PII, log réel, malware ou artefact dangereux dans Git. PurpleWatch ne remplace pas Wazuh ni un SIEM.

## Gouvernance

Les identifiants `PW-xxx` sont des identifiants projet, indépendants des numéros GitHub. Les changements significatifs sont reliés à une issue, revus par PR et validés par CI avant intégration dans `main`.
