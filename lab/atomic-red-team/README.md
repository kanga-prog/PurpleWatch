# Atomic Red Team Lab Integration

This directory documents the controlled Atomic Red Team integration used by PurpleWatch.

## Role

Atomic Red Team reproduces reviewed MITRE ATT&CK behaviors on the Windows lab endpoint so PurpleWatch can validate whether those behaviors are observed, detected, and correctly mapped.

MITRE ATT&CK is the technique taxonomy; Atomic Red Team is the controlled test framework.

## Endpoint

- Windows VM: `PW-WIN11-01`
- Sysmon: process telemetry
- Wazuh Agent: telemetry forwarding
- Wazuh Manager: detection and ATT&CK mapping
- PurpleWatch: correlation, coverage measurement, gap tracking, and retest status

## P0 techniques

- T1082
- T1057
- T1087.001
- T1016
- T1059.001

## Repository boundary

Do not commit:

- downloaded Atomic Red Team content
- Atomic payloads
- PowerShell modules
- raw Sysmon or Wazuh logs
- credentials or secrets
- malware or dangerous binaries

Only configuration, runbooks, sanitized evidence, and PurpleWatch-owned detection/test metadata belong in Git.

## Recovery

Validated snapshot:

`PW-301-AtomicRedTeam-Validated`

UUID:

`03576529-fe5a-4d09-ac4b-da1a5b45577c`
