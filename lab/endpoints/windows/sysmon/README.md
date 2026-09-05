# PurpleWatch Sysmon baseline

This directory contains the version-controlled Sysmon configuration used by the PurpleWatch Windows laboratory endpoint.

## Configuration

File:

`sysmonconfig.xml`

Schema:

`4.91`

Initial telemetry scope:

- Event ID 1 — Process Create
- Event ID 3 — Network Connect
- SHA-256 image hashing

## Design

The initial PurpleWatch baseline intentionally focuses on telemetry required for the first controlled MITRE ATT&CK validation scenarios.

The configuration can be refined later as detection engineering introduces additional visibility requirements and noise reduction rules.

## Security

Only configuration is committed.

Sysmon executables, credentials, private keys and raw sensitive event logs must not be committed.

## Related documentation

- [PW-204 deployment runbook](../../../../docs/runbooks/sysmon-deployment.md)
- [PW-204 evidence](../../../../docs/evidence/PW-204.md)
