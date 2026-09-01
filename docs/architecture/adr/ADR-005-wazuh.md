# ADR-005 — Wazuh pour collecte et détection

**Statut : accepté**

## Contexte

Le projet doit collecter et détecter des télémétries de laboratoire sans devenir un SIEM.

## Décision

Wazuh fournit collecte et détection ; PurpleWatch consomme, corrèle et mesure.

## Conséquences

Les interfaces Wazuh sont une frontière de confiance ; accès minimal et contrats documentés requis.

## Alternatives

Construire une chaîne SIEM interne : rejeté, hors périmètre et redondant.
