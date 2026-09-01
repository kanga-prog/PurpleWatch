# ADR-011 — Aucune exécution arbitraire distante

**Statut : accepté**

## Contexte

Une plateforme Purple Team peut devenir un vecteur d'abus si elle exécute librement des commandes sur des endpoints.

## Décision

PurpleWatch ne fournit aucune exécution arbitraire de commandes à distance.

## Conséquences

Les tests sont contrôlés par le lab et approuvés ; l'API ne devient pas une console d'administration distante.

## Alternatives

Exécution générique PowerShell/SSH/agent : rejetée pour le risque de sécurité et de dérive de périmètre.
