# PW-103 — SAST/SCA baseline

## Purpose

PurpleWatch applies layered security analysis before application development begins. This baseline defines when each control applies, how findings are handled, and which controls are deliberately deferred until genuine source code or dependencies exist.

## SAST and SCA

Software composition analysis (SCA) evaluates third-party dependencies and their supply-chain risk. Static application security testing (SAST) evaluates code written by PurpleWatch for potentially insecure patterns. Neither replaces threat modelling, review, runtime testing, or detection-engineering validation.

## Active now

- Repository-policy validates Markdown, YAML, file policy, ShellCheck, Actionlint, and Gitleaks.
- CodeQL detects whether genuine Python or JavaScript/TypeScript application source exists. Its `CodeQL gate` succeeds when no source exists and fails when an applicable analysis fails.
- La configuration Dependabot de cette branche cible uniquement les dépendances GitHub Actions ; elle devient active après revue et merge.

## Activates when real code or dependencies exist

### Python

- Ruff provides fast linting and selected security-pattern rules. It does not perform deep dataflow analysis or dependency vulnerability analysis.
- Bandit identifies Python AST patterns such as unsafe APIs and weak security practices. It does not establish runtime exploitability or dependency CVEs.
- CodeQL provides semantic and dataflow analysis when Python source exists.
- `pip-audit` runs only after a real resolved dependency lock is available. It audits known dependency vulnerabilities; it does not analyse PurpleWatch source code.

### JavaScript and TypeScript

- ESLint provides quality, unsafe-idiom and selected security-rule checks. It does not provide dependency CVE analysis or complete dataflow analysis.
- CodeQL provides semantic analysis when real JavaScript or TypeScript source exists.
- `npm audit` runs only when a genuine `package-lock.json` exists. It evaluates dependency advisories, not application source.

## Deferred tools

Semgrep is deferred until a curated PurpleWatch rule set provides distinct value beyond Ruff, Bandit, ESLint, and CodeQL. It may begin as advisory-only because generic rules can create maintenance overhead and false positives.

Trivy is deferred until Dockerfiles, images, or infrastructure definitions exist. It will then scan images, filesystems and infrastructure configuration; it does not replace application SAST or dependency remediation.

## Source-aware and dependency-aware activation

No scanner is activated by fabricated source, manifests, lockfiles, or dependencies. Language SAST jobs activate from real application source under `apps/api` or `apps/web`. Python SCA activates from the approved Python lock strategy; npm SCA activates from `package-lock.json`. Each activation must be added with the first genuine component it protects.

## Severity policy

| Severity | Pull Request policy | Follow-up |
|---|---|---|
| CRITICAL | Block. | Immediate remediation; emergency exception only. |
| HIGH | Block when introduced or reachable. | Remediate before merge unless a temporary exception is approved. |
| MEDIUM | Block when reachable in an exposed or security-sensitive path. | Otherwise create a remediation issue with an owner and target date. |
| LOW | Informational. | Track when material and review periodically. |

For SAST findings without CVSS, impact and confidence determine the equivalent severity. High-confidence injection, authentication bypass, secret exposure, or unsafe command execution are treated as HIGH or CRITICAL.

## Temporary security exceptions

Exceptions are never permanent or blanket suppressions. Each requires a technical justification, named owner, linked `PW-xxx` issue, compensating control, explicit expiry date, and review before expiry. Suggested maximum durations are 7 days for CRITICAL, 14 days for HIGH, and 30 days for MEDIUM findings.

## Local developer flow

```text
Developer → repository validation → applicable SAST/SCA → Gitleaks → push → Pull Request
```

When their genuine scope exists, developers run Ruff/Bandit or ESLint and the corresponding dependency audit locally. CodeQL and dependency review remain CI controls.

## CI security flow

```text
Pull Request → repository-policy → source/dependency detection → applicable SAST/SCA → CodeQL → security gate → review → merge
```

## Definition of Done

A change introducing source, dependencies, a lockfile, a GitHub Action, or a container definition must activate the corresponding controls, resolve blocking findings, document time-bounded exceptions, and attach validation evidence to its PR.
