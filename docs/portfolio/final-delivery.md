# PurpleWatch — Dossier de livraison final

## Description

PurpleWatch est un laboratoire Purple Team qui vérifie qu'un comportement MITRE ATT&CK autorisé peut être émulé, observé et détecté. Le projet relie Caldera et Sandcat à la télémétrie Sysmon ou auditd, puis à Wazuh.

## Architecture et technologies

| Composant | Rôle |
| --- | --- |
| Caldera | Orchestration des abilities, adversaries et opérations |
| Sandcat | Agent qui récupère une instruction, l'exécute et renvoie le résultat |
| Sysmon | Télémétrie de création de processus Windows |
| auditd | Télémétrie d'exécution Linux |
| Wazuh | Collecte, règles locales, alertes et Threat Hunting |
| Atomic Red Team | Test complémentaire reproductible sur Linux |
| Tailscale | Réseau privé chiffré entre les composants distribués |

## Méthode de validation

1. Caldera lance une ability associée à une technique MITRE ATT&CK.
2. Sandcat exécute la commande sur Windows ou Linux.
3. Sysmon ou auditd produit un événement local.
4. L'agent Wazuh transmet l'événement au manager.
5. Une règle PurpleWatch crée une alerte liée à la technique.
6. En cas de GAP, le scénario est diagnostiqué, corrigé puis relancé.

Les résultats détaillés sont disponibles dans [PW-402](../evidence/PW-402-final-validation.md).
Le rapport prêt à partager est disponible en [PDF](PurpleWatch_Rapport_Final.pdf).

## Démonstration de soutenance

La démonstration live doit durer moins de trois minutes : vérifier l'agent, lancer T1057 Windows dans Caldera, afficher le succès, puis filtrer Wazuh sur la règle `100101`. Le scénario Linux T1057 avec la règle `100105` constitue le plan de secours plus stable.

## Apprentissages

- Différencier une exécution réussie d'une détection réellement validée.
- Utiliser MITRE ATT&CK comme langage commun entre émulation et détection.
- Ajuster une règle à partir des champs réels de la télémétrie.
- Documenter les limites et confirmer chaque correction par retest.

## Prochaines étapes

- Étendre la couverture à d'autres tactiques MITRE ATT&CK.
- Enrichir les règles pour mieux distinguer les usages légitimes des usages suspects.
- Fiabiliser la persistance Windows avant de la déclarer validée.
- Automatiser la production d'une matrice de couverture à partir des preuves.

## Éléments de présentation

Le support de soutenance est disponible dans [`presentation/`](../../presentation/). Ne pas intégrer de secrets, journaux bruts ni identifiants d'infrastructure.

## Évolution vérifiée au 24 septembre 2026

Les essais récents ont validé T1016 et T1087.001 sur Linux ainsi que T1059.004 (Execution) sur Linux. Voir [progression et journal normalisé](progression-2026-09-24/README.md). Ce jalon enrichit le dépôt historique ; le PDF et la présentation datés d'avant ce jalon demandent une mise à jour éditoriale avant d'être présentés comme état courant. Les métriques P50 et P95 ne sont pas encore établies.
