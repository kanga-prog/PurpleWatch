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

## SAST, SCA et dépendances

SAST analyse le code PurpleWatch ; SCA analyse les dépendances tierces. Exécuter les contrôles applicables au composant modifié, sans contourner une security gate. Toute nouvelle dépendance exige revue de provenance, lockfile versionné et validation de vulnérabilités. Les exceptions temporaires exigent une issue `PW-xxx`, un propriétaire, une justification et une date d'expiration.

Les détails sont définis dans le [baseline SAST/SCA](docs/security/sast-sca-baseline.md) et la [politique supply-chain](docs/security/supply-chain-security-policy.md).

## Secret scanning

Avant commit et push, exécuter `gitleaks dir . --redact`, `bash scripts/validate-repository.sh` et `git diff --check`. `.gitignore` réduit les erreurs, mais n'est pas une frontière de sécurité : un fichier ignoré peut être ajouté explicitement à Git. Ne contournez jamais un finding sans investigation. Tout secret authentique poussé doit être révoqué et remplacé, même s'il est ensuite supprimé du fichier.

Voir le [baseline secret scanning](docs/security/secret-scanning-baseline.md) et le [runbook sécurité](docs/runbooks/repository-security.md).

## Revue

`main` est destinée à être protégée : PR obligatoire, contrôles CI requis, revue humaine et squash merge. Aucun push direct vers `main`.
