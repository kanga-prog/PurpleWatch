# Supply-chain security policy

## Sources and provenance

PurpleWatch uses official registries and verified upstream sources: PyPI for Python, npm for JavaScript/TypeScript, and reviewed GitHub Actions. New direct dependencies require a PR review covering maintainer activity, provenance, release cadence, known advisories, purpose, and alternatives.

## Dependencies and locking

Direct dependencies must use intentional version constraints and every dependency ecosystem must commit its resolved lockfile. Reviewers consider the full resolved graph, including transitive dependencies, rather than only the package named in a manifest.

Packages with unclear ownership, no meaningful maintenance, suspiciously similar names, unexpected install scripts, or unexplained transitive growth require additional review. Suspected typosquatting blocks introduction until provenance is confirmed.

## Vulnerabilities and licenses

Known vulnerabilities are handled under the severity policy in the SAST/SCA baseline. Direct and material transitive vulnerabilities require remediation, upgrade, replacement, or a time-bounded exception.

GPL, AGPL, SSPL, proprietary, no-license, dual-license, or otherwise ambiguous licenses trigger review before adoption. This is a governance and compatibility review trigger; it is not an automatic claim of illegality.

## Automation and updates

GitHub Actions are pinned to reviewed commit SHA. Dependabot est configuré pour surveiller GitHub Actions après merge et surveillera pip et npm seulement après l'arrivée de manifests réels. Dependency updates receive the same CI, review, and severity gates as feature changes.

## Containers and SBOMs

When containers are introduced, base images must be pinned by immutable digest and scanned with Trivy. The first release-capable application pipeline must generate a CycloneDX SBOM from resolved dependencies and retain it as a build artifact. Images, VM files, and large SBOM artifacts are not committed to Git.

## Vulnerability remediation

Finding → classify → verify → remediate or approve a temporary exception → validate → retain evidence → close. Security updates are prioritised by severity, reachability, exposure, and compensating controls.

## Temporary exceptions

Exceptions require justification, owner, linked `PW-xxx` issue, compensating controls, expiry date, and revalidation. Expired exceptions are treated as active findings. Permanent blanket suppressions are prohibited.
