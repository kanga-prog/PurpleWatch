# ADR-009 — Detection-as-Code Sigma + Wazuh

**Statut : accepté**

## Contexte

Les détections doivent être revues, testées et améliorées de manière traçable.

## Décision

Versionner les règles Sigma et Wazuh, leurs métadonnées et fixtures sûres.

## Conséquences

Toute règle nécessite revue, mapping ATT&CK, test et preuve de retest.

## Alternatives

Règles modifiées manuellement dans l'outil : rejetées car non auditables dans Git.
