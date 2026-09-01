# ADR-006 — Sysmon pour la télémétrie Windows

**Statut : accepté**

## Contexte

Les techniques MVP visent une cible Windows de laboratoire.

## Décision

Utiliser Sysmon comme source de télémétrie Windows détaillée.

## Conséquences

Le paramétrage doit être versionné, limité au lab et accompagné de règles de rétention.

## Alternatives

Événements Windows seuls : rejeté car moins adaptés à la couverture de détection ciblée.
