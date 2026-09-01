# PW-104 — Secret scanning baseline

## Purpose

PurpleWatch prevents, detects, and responds to accidental exposure of secrets without storing secret-shaped fixtures or weakening controls. A leaked secret is handled as an exposure incident, not as a formatting defect.

## Secret classification

Secrets include API and OAuth tokens, passwords, database credentials, private keys, certificates containing private material, Wazuh credentials, PostgreSQL credentials, future CTI-feed credentials, GitHub tokens, cloud credentials, webhook secrets, CI credentials, deployment keys, and service-account material.

## Prevention and detection

Prevention reduces the chance that a secret enters Git. Detection identifies suspected exposure that bypassed prevention. Neither layer revokes a secret; deletion from a file does **not** revoke the secret.

## Current controls

### Active now

- `.gitignore` excludes local environment files, common key material, credentials directories, logs, databases, VM artifacts, and dangerous binaries.
- `.env.example` contains empty placeholders only.
- Gitleaks scans local working trees when run by developers and scans Git history in blocking CI with redacted output.
- GitHub Secret Scanning and Push Protection are enabled.
- PR and issue templates prohibit public disclosure of secrets and sensitive evidence.

### Disabled or not configured

- GitHub Secret Scanning validity checks are disabled.
- GitHub non-provider patterns are disabled.
- No custom PurpleWatch secret patterns are configured.
- `pre-commit` is not installed; a lightweight pinned Gitleaks hook is a future improvement, not an active control.

## Gitleaks and GitHub roles

Gitleaks provides repository-controlled local and CI scanning. The pinned CI version `8.30.0` is the source of truth; local installations may be newer but must remain compatible. The CI scan uses `gitleaks git --redact --exit-code 1` with complete checkout history and blocks findings. GitHub Secret Scanning adds GitHub-managed detection and alerting. Push Protection can stop supported secrets before a push is accepted. These controls complement each other.

## Empty environment-file policy

`.env.example` documents variable names only. Local `.env` files remain ignored and may not be committed. `.gitignore` is not a security boundary: a deliberately staged ignored file can still enter Git.

## Local developer procedure

Before commit and push, run:

```text
gitleaks dir . --redact
bash scripts/validate-repository.sh
git diff --check
```

Investigate every finding. Do not bypass a suspected genuine secret. A pushed genuine secret requires revocation and rotation.

## CI procedure

CI checks out complete history, installs the pinned Gitleaks version, and runs the blocking redacted Git-history scan. A CI failure remains blocking until the finding is remediated or a narrowly scoped, reviewed temporary exception is approved.

## Exposure levels

| Level | Exposure | Immediate response |
|---|---|---|
| A | Working tree only | Stop use, remove safely, scan, assess whether the value was shared. |
| B | Staged Git content | Unstage/remove, scan, and rotate if any external system received the value. |
| C | Local commit, not pushed | Revoke/rotate when genuine; amend or rewrite before publication when safe. |
| D | Remote branch or Pull Request | Revoke/rotate first, remove active value, assess PR, cache and fork exposure. |
| E | `main` | Treat as broad exposure: revoke/rotate first, assess consumers and document incident. |
| F | Public history | Treat as compromised regardless of later deletion; revoke/rotate before evaluating history cleanup. |

## Revocation, rotation, and history

Core lifecycle: **stop use → revoke → rotate → assess exposure → identify consumers → replace safely → remove active value → scan → document non-secret evidence → close**.

History rewriting is a deliberate incident-response decision after revocation and exposure assessment. It may reduce accidental redistribution but cannot erase clones, forks, caches, logs, or external consumers. Deleting a file is never equivalent to revocation.

## Fixtures and exceptions

Fixtures are synthetic, small, and non-token-shaped. Do not create secret-looking values to test scanners. There is no global allowlist, repository-wide disable, `.gitleaksignore`, or `.gitleaks.toml` today.

Any future false-positive exception must be minimal in scope, justified, linked to a `PW-xxx` issue when material, reviewed, and time-bounded where relevant. Blanket or permanent suppressions are prohibited.

## Future secret management

Local secrets remain in ignored `.env` files. CI secrets use GitHub Secrets or Environments with least privilege. Production secrets use an appropriate secret manager with rotation. Secrets must not appear in Docker images, frontend bundles, logs, or evidence artifacts.

## Evidence and Definition of Done

Evidence contains command outcomes, affected components, revocation timestamps, replacement validation, and issue references—never the secret itself. A change is complete only when applicable scans pass, no real or secret-shaped test material was introduced, and any incident or exception has documented closure criteria.
