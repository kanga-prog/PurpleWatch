# Contribuer à PurpleWatch

## Règles de contribution

- Une contribution significative est liée à un identifiant projet `PW-xxx`.
- Créer une branche depuis `main` : `docs/PW-001-description`, `feat/PW-501-description` ou `fix/PW-xxx-description`.
- Utiliser des commits conventionnels, par exemple `docs(PW-001): add project charter`.
- Une Pull Request doit décrire le périmètre, les contrôles exécutés, les impacts sécurité et les preuves associées.
- Ne jamais ajouter de secret, donnée réelle, fichier massif, VM, dump, base de données ou artefact dangereux.

## Qualité et sécurité

Avant proposition, exécuter les contrôles disponibles et vérifier `git diff --check`. Les exceptions de sécurité nécessitent une justification, une issue de suivi et une date d'expiration.

Les règles de détection, fixtures et scénarios de laboratoire doivent être sûrs, minimaux, anonymisés et revus. Aucune fonctionnalité permettant l'exécution distante arbitraire n'est acceptée.

## Revue

`main` est destinée à être protégée : PR obligatoire, contrôles CI requis, revue humaine et squash merge. Aucun push direct vers `main`.
