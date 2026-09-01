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

## Politique des fixtures

Les fixtures sous `tests/fixtures/` sont transversales, petites, synthétiques, anonymisées et non exécutables. Elles ne contiennent ni événement réel, ni PII, ni credential, ni payload offensif dangereux.
