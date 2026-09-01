# Runbook — sécurité du dépôt

## Avant un commit

1. Vérifier les fichiers et le diff : `git status`, `git diff --check`, `git diff --stat`, `git diff`.
2. Confirmer qu'aucun secret, PII, log réel, VM, dump, base, malware, binaire ou archive non justifiée n'est présent.
3. Exécuter les contrôles disponibles : validation dépôt, ShellCheck, Actionlint, Gitleaks, SAST et SCA selon les composants modifiés.
4. Vérifier que les fichiers générés, caches, `.env` et credentials sont ignorés.
5. Relier le changement à un identifiant `PW-xxx` et documenter toute exception sécurité.

## Réponse à une exposition de secret

Cycle obligatoire : **stop use → revoke → rotate → assess exposure → identify consumers → replace safely → remove active value → scan → document non-secret evidence → close**.

| Niveau | Action immédiate | Git et exposition | Preuve, validation et clôture |
|---|---|---|---|
| A — working tree | Arrêter l'usage et retirer la valeur sans la recopier. | Vérifier si le secret a été partagé avec un processus, terminal, log ou outil externe. | Scanner ; clôturer si aucune exposition confirmée ou après rotation nécessaire. |
| B — staged | Retirer du stage et arrêter l'usage. | Vérifier index, diff et tout outil ayant reçu le contenu. | Scanner ; documenter la décision de révocation/rotation. |
| C — local commit | Considérer le secret sensible ; révoquer/rotate si authentique. | Amender ou réécrire localement avant publication lorsque c'est sûr. | Vérifier l'historique local et les consommateurs ; conserver une preuve non secrète. |
| D — remote branch / PR | Révoquer et rotate avant tout nettoyage. | Évaluer branche, PR, caches, clones, forks et logs de CI. | Supprimer la valeur active, scanner, documenter exposition et remplacements. |
| E — main | Révoquer et rotate immédiatement. | Évaluer releases, déploiements, clones, forks, caches et consommateurs. | Incident privé, validation de remédiation, décision documentée sur l'historique. |
| F — public history | Traiter comme compromis confirmé. | Révoquer/rotate avant d'évaluer réécriture, invalidation de caches ou avis aux consommateurs. | Conserver chronologie et preuves sans valeur secrète ; clôturer après validation. |

La suppression d'un fichier ne révoque pas un secret. La réécriture d'historique est une décision délibérée de réponse à incident, jamais un réflexe automatique : elle ne retire pas les copies, forks, caches ni journaux externes.

## Traitement des findings sécurité

Processus commun : **finding → classify → verify → remediate or create exception → validate → evidence → close**.

- **Finding SAST :** confirmer le contexte, l'impact et la confiance ; corriger le code ou créer une exception temporaire conforme au baseline SAST/SCA.
- **Vulnérabilité de dépendance :** identifier la dépendance directe ou transitive, évaluer atteignabilité/exposition, mettre à jour, remplacer ou appliquer un contrôle compensatoire temporaire.
- **Exposition de secret :** suivre immédiatement la procédure de révocation ci-dessus ; ne pas attendre la triage normale.
- **Mise à jour GitHub Actions :** vérifier l'origine, le SHA épinglé, le diff de version et les contrôles CI avant merge.

Chaque résolution ou exception conserve une preuve de validation et une issue `PW-xxx`. Aucune suppression globale et permanente d'un finding n'est admise.

## Politique des fixtures

Les fixtures sous `tests/fixtures/` sont transversales, petites, synthétiques, anonymisées et non exécutables. Elles ne contiennent ni événement réel, ni PII, ni credential, ni payload offensif dangereux.
