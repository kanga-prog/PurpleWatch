# PurpleWatch — contrat du journal d'attaque

**Version :** 1.0, 24 septembre 2026. Un objet JSON par exécution Caldera, enregistré comme une ligne dans un fichier JSONL UTF-8. Garder le run même en cas d'échec ; ne pas confondre exécution, télémétrie et détection.

**Runs enregistrés :** `purplewatch-runs-20260924.jsonl` contient le baseline et le retest T1087.001 Linux. Les heures `Time Ran` et l'alerte sont conservées en UTC, tandis que `started_at` et `latency_seconds` restent nuls jusqu'à obtention du début exact du lien Caldera. Les identifiants d'opération et d'alerte encore inconnus restent également nuls.

| Champ | Type | Règle |
| --- | --- | --- |
| `run_id` | chaîne | Identifiant unique, par exemple `PW-RUN-20260924-001`. |
| `scenario_id` | chaîne | Identifiant stable de la fiche de scénario. |
| `technique_id`, `tactic` | chaînes | Mapping ATT&CK de l'ability. |
| `platform`, `target` | chaînes | OS et nom de l'endpoint ciblé. |
| `caldera_operation`, `caldera_ability_id` | chaînes | Identifiants observés dans Caldera. |
| `command` | chaîne | Commande réellement enregistrée dans l'ability. |
| `expected_telemetry`, `expected_rule` | chaîne, liste de chaînes | Signal attendu et règles attendues ; préciser la portée d'une règle native optionnelle. |
| `started_at`, `alerted_at` | ISO 8601 UTC ou `null` | Début du lien Caldera et heure de l'alerte attendue. `Time Ran` n'est utilisé comme substitut qu'avec une mention explicite. |
| `latency_seconds` | nombre ou `null` | `alerted_at - started_at`, seulement si les deux heures sont comparables et établies. |
| `caldera_status` | `success` ou `failed` | Statut effectivement relevé. |
| `verdict` | `detected`, `not_detected`, `execution_failed`, `pending_evidence` | Verdict propre à ce run. |
| `observed_rule`, `alert_id`, `audit_event_id` | chaîne ou `null` | Identifiants de preuve, sans les inventer. |
| `evidence` | objet | Références aux captures/exports et état de la corrélation PID/PPID. |

Exemple **partiel réel** du retest T1016 (remplir les valeurs nulles après export ; `started_at` reste nul car seule l'heure `Time Ran` a été fournie) :

```json
{
  "run_id": "PW-RUN-20260924-001",
  "scenario_id": "PW-T1016-LINUX-IPADDR",
  "technique_id": "T1016",
  "tactic": "Discovery",
  "platform": "linux",
  "target": "PW-LINUX-01",
  "caldera_operation": null,
  "caldera_ability_id": "d174545d-d59e-4363-87bc-578c7c19f832",
  "command": "/usr/sbin/ip addr show",
  "expected_telemetry": "auditd execve, exe=/usr/bin/ip, key=purplewatch_execve",
  "expected_rule": ["100106"],
  "started_at": null,
  "caldera_time_ran": "2026-09-23T22:43:44Z",
  "alerted_at": "2026-09-23T22:43:47.794Z",
  "latency_seconds": null,
  "caldera_status": "success",
  "verdict": "pending_evidence",
  "observed_rule": "100106",
  "alert_id": null,
  "audit_event_id": null,
  "evidence": {
    "caldera_pid": 5215,
    "audit_ppid_matches_caldera": null,
    "note": "Alerte fraîche observée ; ID d'alerte et auditd de ce retest encore à archiver."
  }
}
```

Le nom exact de l'opération effectivement lancée n'a pas été fourni ; renseigner `caldera_operation` après vérification dans Caldera. Le `run_id` est un exemple à réserver uniquement si aucune entrée existante n'utilise déjà cet identifiant.

## Calculs et garde-fous

| Indicateur | Calcul |
| --- | --- |
| Taux d'exécution | Nombre de runs `success` / nombre de runs lancés. |
| Taux de détection | Nombre de runs `detected` / nombre de runs `success` avec règle attendue. |
| Latence E2E | Heure d'alerte Wazuh moins début exact du lien Caldera, en UTC. |
| P50 / P95 | Médiane / percentile 95 des seules latences valides ; publier `n`, la méthode de percentile et les échecs à part. |
| Faux positifs en lab | Alertes de la règle attendue hors fenêtres de runs sur le même endpoint ; vérifier les activités administratives. |
| Couverture ATT&CK | Techniques avec PASS étayé / techniques planifiées ; distinguer les plateformes. |

**Échantillonnage :** viser au moins 20 répétitions pour interpréter P95, sur configuration stable, en espaçant les runs et en gardant les échecs. Une valeur calculée sur un seul test ne s'appelle pas P95. Le simple écart entre `Time Ran` et Wazuh du 24/09 (3,794 s) est un indicateur exploratoire, pas une latence E2E normalisée.

## Exécutions T1059.004 du 24 septembre 2026

La trace normalisée des trois essais est enregistrée dans `purplewatch-runs-20260924.jsonl` : baseline et premier retest Caldera `success` sans alerte, puis retest après correction de l'analyse des événements auditd regroupés `SYSCALL+EXECVE`. À 02:42:37 UTC+2, Caldera `success` sur `PW-LINUX-01`, PID 5807 ; alerte Wazuh `100108` à 02:42:49.269 UTC+2. Verdict **detected**. `started_at`, l'identifiant Wazuh et le P50/P95 restent non renseignés tant que les preuves précises et les répétitions manquent.

## T1119 — Automated Collection, 24 septembre 2026

Quatre exécutions sont consignées dans `purplewatch-runs-20260924.jsonl` : deux erreurs de chemin liées à `PrivateTmp=yes`, une baseline réussie avec fichiers factices, puis un retest détecté par `100109`. Les identifiants Wazuh du retest et les horodatages `started_at` restent à relever avant toute statistique de latence.

## T1036.005 et T1552.001 — 24 septembre 2026

Les baselines et retests de Defense Evasion et Credential Access sont consignés dans `purplewatch-runs-20260924.jsonl`. Pour chaque retest, `started_at`, identifiant d'alerte et événement auditd complet restent à renseigner avant calcul de percentiles. Les quatre nouvelles tactiques demandées ont désormais une alerte dédiée visible après Caldera.

## Séquence T1082 → T1057 → T1016 — 24 septembre 2026

Trois entrées normalisées ajoutées au journal JSONL, avec IDs Wazuh `1790241865.609283`, `1790241905.611203`, `1790241958.613081`, agent `002`, fenêtre 92,053 s. Résultat de la corrélation script et alertes corrélées propres à mesurer séparément ; ne pas assimiler les écarts d'heures affichées à des latences E2E exactes.

## Mesures et adversary à plusieurs tactiques — 24 septembre 2026

Cinq séquences Caldera de reconnaissance réussies sur `PW-LINUX-01`, 15 alertes Wazuh attendues et observées. Latence auditd → alerte calculée sur les 15 paires `full_log`/`timestamp` : P50 **0,874 s**, P95 **1,178 s** (rang supérieur, n=15). Une corrélation manuelle des trois premières alertes a donné 92,053 s ; aucune alerte de corrélation autonome encore confirmée.

`PW-LINUX-MultiTactic-Sequence` : une opération unique, huit abilities `success`, huit alertes Wazuh sur agent `002`. Références horaires UTC+2 et couples technique/règle : T1059.004/100108 12:24:24.394 ; T1082/100104 12:25:16.391 ; T1057/100105 12:26:08.447 ; T1016/100106 12:26:46.408 ; T1087.001/100107 12:27:48.481 ; T1552.001/100111 12:28:52.454 ; T1119/100109 12:29:52.404 ; T1036.005/100110 12:30:48.464. Fichiers de test et leurre fictifs. Le tableau Caldera affiché couvre 12:24:00–12:29:55 UTC+2 ; heures arrondies impropres à une latence E2E précise.

### Retest automatisé et corrélation réelle, 13:03–13:09 UTC+2

Deuxième opération `PW-LINUX-MultiTactic-Sequence` : huit abilities Caldera réussies sur `PW-LINUX-01` (13:03:23 à 13:08:08). Huit règles individuelles Wazuh observées dans le même ordre : `100108` 13:03:59.002, `100104` 13:04:37.023, `100105` 13:05:30.690, `100106` 13:06:03.068, `100107` 13:06:43.075, `100111` 13:07:22.721, `100109` 13:08:06.731, `100110` 13:09:08.721. Service `purplewatch-recon.service` actif ; ligne JSON de corrélation sur le manager avec IDs sources `1790247877.701199`, `1790247930.704662`, `1790247963.706540`, agent source `002` et durée 86,045 s. Alerte Wazuh **100112**, niveau 10, horodatée 13:06:04.374 UTC+2, ID `1790247964.708527`, `agent.id=000`, `data.pw_source_agent_id=002`. **PASS corrélation automatique E2E**.
