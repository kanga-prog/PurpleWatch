# PW-201 — Cyber Lab Topology

## Objectif

Le Cyber Lab PurpleWatch fournit un environnement contrôlé pour produire de la télémétrie Windows, la collecter avec Wazuh et mesurer la couverture de détection sans exposer de système de production.

PurpleWatch n'est pas un SIEM. Wazuh reste responsable de la collecte et de la détection ; PurpleWatch orchestre, corrèle, mesure et visualise les résultats.

## Topologie cible

```text
HP EliteBook x360 / Windows 11
│
├── WSL2
│   └── environnement de développement PurpleWatch
│
├── VM Linux
│   └── Wazuh all-in-one
│
└── VM Windows de laboratoire
    ├── Sysmon
    └── Wazuh Agent
```

## Flux de télémétrie cible

```text
Windows Event
    ↓
Sysmon
    ↓
Wazuh Agent
    ↓
Wazuh central
    ↓
événement visible et vérifiable
```

Les tests MITRE ATT&CK et Atomic Red Team seront introduits après validation de cette chaîne de télémétrie.

## Réseau et frontières de confiance

Le laboratoire utilise un réseau virtuel privé. Aucun service du lab ne doit être exposé directement à Internet.

Sont notamment interdits par défaut :
- la redirection de port depuis le routeur Internet ;
- l'exposition publique de RDP ;
- l'exposition publique du dashboard Wazuh ;
- l'exposition publique de l'API Wazuh ;
- l'exposition publique des ports d'enrôlement Wazuh.

PurpleWatch ne fournit aucune primitive générique d'exécution distante arbitraire.

## Contraintes de ressources

La machine hôte dispose d'environ 8 Go de mémoire physique. Cette contrainte ne modifie pas l'architecture cible ; elle impose un mode d'exploitation contrôlé.

### Mode développement

```text
WSL2                ON
éditeur / Codex     ON
Wazuh VM            OFF
Windows VM          OFF
```

### Mode validation laboratoire

```text
WSL2                minimal ou arrêté si inutile
Wazuh VM            ON
Windows VM          ON
applications hôte   réduites au minimum
```

Les allocations CPU, RAM et disque des VM seront validées empiriquement lors des étapes de déploiement.

## Périmètre PW-201

PW-201 documente :
- la topologie ;
- les frontières de confiance ;
- l'isolation réseau ;
- les contraintes de ressources ;
- la stratégie de récupération.

PW-201 n'installe pas Wazuh, Sysmon, Wazuh Agent ou Atomic Red Team.

## Jalons suivants

- PW-202 : déploiement Wazuh all-in-one ;
- PW-203 : préparation de l'endpoint Windows ;
- PW-204 : configuration Sysmon ;
- PW-205 : enrôlement du Wazuh Agent ;
- PW-206 : validation de la télémétrie de bout en bout.

## Critères d'acceptation

PW-201 est terminé lorsque :
- la topologie physique et logique est documentée ;
- les frontières de confiance sont identifiées ;
- l'isolation réseau est documentée ;
- les contraintes de ressources sont documentées sans changer l'architecture cible ;
- une procédure de récupération existe ;
- aucun composant offensif ou service Wazuh n'est déployé par cette issue.
