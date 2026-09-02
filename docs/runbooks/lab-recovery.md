# PW-201 — Cyber Lab Recovery Runbook

## Objectif

Ce runbook décrit comment revenir à un état connu du Cyber Lab après une erreur de configuration, un test inattendu ou une corruption d'une machine virtuelle.

## Principe

Une reconstruction reproductible est préférable à une réparation manuelle non documentée.

Les snapshots du laboratoire sont des points de restauration pratiques. Ils ne remplacent pas une sauvegarde des données importantes.

## États de référence

Lorsque les composants correspondants seront déployés, le laboratoire devra disposer des états logiques suivants :

```text
Windows-Clean
    Windows installé et mis à jour

Windows-Instrumented
    Windows + Sysmon + Wazuh Agent configurés

Wazuh-Clean
    Wazuh all-in-one fonctionnel avant expérimentation
```

Les noms exacts des snapshots dépendront de l'hyperviseur retenu.

## Avant un test

Avant une validation Purple Team :

1. vérifier que les VM attendues sont démarrées ;
2. vérifier que le réseau du lab est isolé ;
3. vérifier la disponibilité de Wazuh ;
4. confirmer que l'endpoint appartient au lab ;
5. vérifier ou créer le point de restauration requis ;
6. noter l'identifiant du test à exécuter.

## Comportement inattendu

Arrêter immédiatement le test.

Ne pas poursuivre avec d'autres techniques tant que l'état du laboratoire n'est pas compris.

Si nécessaire :

```text
Endpoint Windows
      ↓
arrêt
      ↓
restauration d'un snapshot connu
      ↓
redémarrage
      ↓
validation Sysmon
      ↓
validation Wazuh Agent
      ↓
validation télémétrie
```

## Récupération Wazuh

Si Wazuh devient instable :

```text
arrêter les tests
      ↓
conserver uniquement les preuves nécessaires
      ↓
arrêter proprement la VM
      ↓
restaurer Wazuh-Clean
      ↓
redémarrer
      ↓
vérifier la santé des composants
      ↓
revalider la réception de télémétrie
```

Les commandes spécifiques seront ajoutées dans PW-202 après le choix et le déploiement effectif de l'environnement Wazuh.

## Validation après restauration

Une restauration n'est considérée réussie que si les composants déjà déployés retrouvent leur état attendu.

À terme, la validation complète couvrira :

```text
endpoint accessible dans le réseau privé
+
Sysmon opérationnel
+
Wazuh Agent opérationnel
+
Wazuh central opérationnel
+
nouvel événement de test visible
```

Les composants non encore installés sont ignorés jusqu'à leur issue de déploiement respective.

## Gestion des ressources

Sur la machine hôte actuelle, les VM ne doivent pas rester démarrées sans besoin.

En mode développement, les VM du Cyber Lab restent arrêtées.

En mode validation, les applications hôte non nécessaires sont réduites au minimum avant de démarrer simultanément Wazuh et l'endpoint Windows.

Un manque de ressources doit provoquer l'arrêt contrôlé du test et une réévaluation des allocations, pas la suppression des contrôles de sécurité.

## Preuves

Les preuves de récupération peuvent inclure :

- l'état des VM ;
- l'état des agents ;
- la capture d'un événement Wazuh ;
- l'horodatage du test ;
- le résultat du contrôle de télémétrie.

Les preuves ne doivent contenir ni secret ni donnée personnelle inutile.

## Limites de PW-201

PW-201 documente uniquement la stratégie de récupération.

Les commandes propres à l'hyperviseur, Wazuh, Sysmon et Wazuh Agent seront ajoutées dans leurs issues de déploiement respectives.
