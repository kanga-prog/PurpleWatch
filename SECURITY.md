# Politique de sécurité

## Signalement

Ne publiez jamais de vulnérabilité exploitable, secret, token, log réel ou donnée personnelle dans une issue publique. Utilisez le canal privé convenu avec le mainteneur ; si aucun canal n'est établi, demandez-en un sans partager de détail sensible.

Inclure un impact, des étapes minimales non destructrices, les versions concernées et une proposition de remédiation. Ne joignez ni credential ni artefact dangereux.

## Périmètre et règles

PurpleWatch est destiné à un laboratoire contrôlé. Sont interdits dans le dépôt : mots de passe, clés privées, tokens, credentials Wazuh, PII, logs réels, bases de données, images de VM, dumps mémoire, malware et binaires dangereux.

Les simulations et les données de test doivent être explicitement autorisées, non destructrices, minimales et documentées. La plateforme ne doit pas offrir d'exécution distante arbitraire.

## Réponse

Le mainteneur accuse réception, évalue le risque, coordonne la correction, puis documente la résolution sans exposer les éléments sensibles. Tout secret suspecté exposé est considéré compromis et doit être révoqué.
