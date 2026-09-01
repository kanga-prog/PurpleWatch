# Runbook — sécurité du dépôt

## Avant un commit

1. Vérifier les fichiers et le diff : `git status`, `git diff --check`, `git diff --stat`, `git diff`.
2. Confirmer qu'aucun secret, PII, log réel, VM, dump, base, malware, binaire ou archive non justifiée n'est présent.
3. Exécuter les contrôles disponibles : validation dépôt, ShellCheck, Actionlint, Gitleaks, SAST et SCA selon les composants modifiés.
4. Vérifier que les fichiers générés, caches, `.env` et credentials sont ignorés.
5. Relier le changement à un identifiant `PW-xxx` et documenter toute exception sécurité.

## Réponse à une exposition de secret

1. Arrêter la diffusion sans republier la valeur.
2. Révoquer/faire tourner immédiatement le secret : il est considéré compromis.
3. Prévenir le mainteneur par canal privé et ouvrir un suivi privé.
4. Évaluer l'historique Git et les systèmes touchés ; supprimer la valeur de la version courante sans présumer que l'historique est sain.
5. Documenter la cause et les contrôles préventifs ajoutés.

## Traitement des findings sécurité

Processus commun : **finding → classify → verify → remediate or create exception → validate → evidence → close**.

- **Finding SAST :** confirmer le contexte, l'impact et la confiance ; corriger le code ou créer une exception temporaire conforme au baseline SAST/SCA.
- **Vulnérabilité de dépendance :** identifier la dépendance directe ou transitive, évaluer atteignabilité/exposition, mettre à jour, remplacer ou appliquer un contrôle compensatoire temporaire.
- **Exposition de secret :** suivre immédiatement la procédure de révocation ci-dessus ; ne pas attendre la triage normale.
- **Mise à jour GitHub Actions :** vérifier l'origine, le SHA épinglé, le diff de version et les contrôles CI avant merge.

Chaque résolution ou exception conserve une preuve de validation et une issue `PW-xxx`. Aucune suppression globale et permanente d'un finding n'est admise.

## Politique des fixtures

Les fixtures sous `tests/fixtures/` sont transversales, petites, synthétiques, anonymisées et non exécutables. Elles ne contiennent ni événement réel, ni PII, ni credential, ni payload offensif dangereux.
