# Politique de sécurité

## Signalement

Ne publiez jamais de vulnérabilité exploitable, secret, token, log réel ou donnée personnelle dans une issue publique. Utilisez le canal privé convenu avec le mainteneur ; si aucun canal n'est établi, demandez-en un sans partager de détail sensible.

Inclure un impact, des étapes minimales non destructrices, les versions concernées et une proposition de remédiation. Ne joignez ni credential ni artefact dangereux.

## Périmètre et règles

PurpleWatch est destiné à un laboratoire contrôlé. Sont interdits dans le dépôt : mots de passe, clés privées, tokens, credentials Wazuh, PII, logs réels, bases de données, images de VM, dumps mémoire, malware et binaires dangereux.

Les simulations et les données de test doivent être explicitement autorisées, non destructrices, minimales et documentées. La plateforme ne doit pas offrir d'exécution distante arbitraire.

## Réponse

Le mainteneur accuse réception, évalue le risque, coordonne la correction, puis documente la résolution sans exposer les éléments sensibles. Tout secret suspecté exposé est considéré compromis et doit être révoqué.

## SAST, SCA et remédiation

Les contrôles et seuils sont décrits dans le [baseline SAST/SCA](docs/security/sast-sca-baseline.md) et la [politique supply-chain](docs/security/supply-chain-security-policy.md). Les vulnérabilités suivent le processus de remédiation documenté dans le runbook. Les exceptions temporaires exigent une justification, un propriétaire, une issue `PW-xxx`, des contrôles compensatoires et une date d'expiration.

Le signalement privé de vulnérabilités reste distinct des issues normales d'ingénierie et ne doit jamais inclure de secret ou de détail exploitable dans un espace public.

## Signalement et exposition de secrets

Les défauts d'ingénierie non sensibles utilisent les issues normales. Une vulnérabilité suspectée ou une exposition de secret ne doit jamais être publiée dans une issue. Le signalement privé GitHub n'est pas encore configuré pour ce dépôt ; l'établissement d'un canal privé est un suivi de gouvernance. En attendant, demandez un canal privé au mainteneur sans transmettre de détail sensible.

Consulter le [baseline secret scanning](docs/security/secret-scanning-baseline.md) et le [runbook sécurité](docs/runbooks/repository-security.md). Une exposition de secret suit immédiatement la révocation et la rotation, pas seulement la suppression du fichier.
