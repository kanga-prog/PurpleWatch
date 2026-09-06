# PW-401 — Wazuh P0 Detection Engineering Runbook

## Purpose

This runbook describes how PurpleWatch develops, validates, deploys, and retests lab-owned Wazuh rules for the P0 ATT&CK validation set.

## Rule ownership

PurpleWatch custom rules live in `detections/wazuh/`.

Do not edit Wazuh upstream rules under `/var/ossec/ruleset/rules/`.

Lab deployment target: `/var/ossec/etc/rules/`.

## P0 mappings

| Rule | Technique | Detection intent |
| --- | --- | --- |
| 100100 | T1082 | detect `systeminfo.exe` process creation |
| 100101 | T1057 | detect `tasklist.exe` process creation |
| 100102 | T1087.001 | detect local-account enumeration through `net user` / `net1 user` |
| 100103 | T1016 | detect approved Windows network-configuration discovery commands |

Native Wazuh rule `92057` remains the regression reference for `T1059.001`.

## Development workflow

1. Change rules only on a dedicated Git branch.
2. Keep custom rule IDs in the PurpleWatch-owned local range.
3. Match Sysmon Event ID 1 process creation through the `sysmon_event1` group.
4. Prefer behavior-specific process and command-line conditions over broad shell-based mappings.
5. Validate XML locally.
6. Transfer the exact file into the private Wazuh lab.
7. Verify file integrity with SHA-256.
8. Run Wazuh native rule validation before restarting the manager.
9. Restart `wazuh-manager` only after validation succeeds.
10. Confirm Manager, Indexer, and endpoint agent health.
11. Retest the approved controlled behavior.
12. Correlate the alert with endpoint, UTC execution window, rule ID, and ATT&CK mapping.
13. Preserve only sanitized evidence in Git.

## Local XML validation

```bash
python3 -c 'import xml.etree.ElementTree as ET; ET.parse("detections/wazuh/purplewatch_p0_rules.xml"); print("XML OK")'
git diff --check
```

## Integrity verification

Validated PW-401 SHA-256:

`98f4679ec7707381a3aa8c5d3159181121237c57de71bda861500a2e9480a510`

## Wazuh native validation

```bash
sudo /var/ossec/bin/wazuh-analysisd -t
```

Do not restart the manager if validation fails.

Validated PW-401 result: `exit code 0`.

## Lab health checks

```bash
sudo systemctl is-active wazuh-manager
sudo systemctl is-active wazuh-indexer
sudo /var/ossec/bin/agent_control -l
systemctl --failed --no-legend
```

Expected validation state:
- `wazuh-manager`: active
- `wazuh-indexer`: active
- `PW-WIN11-01`: Active
- no failed services

## Controlled retest set

Approved P0 retests:
- T1082 Atomic #1
- T1057 Atomic #2
- T1016 Atomic #1
- T1059.001 Atomic #17 for non-regression
- T1087.001 safe primitive: `net user`

For T1087.001, do not execute the complete Atomic #8 in the P0 safe workflow because the installed test also contains `cmdkey.exe /list`.

## Time correlation

Capture start and end from the same PowerShell variables and convert them directly to UTC:

```powershell
Write-Host "START LOCAL:" $Start.ToString("yyyy-MM-ddTHH:mm:ssK")
Write-Host "END   LOCAL:" $End.ToString("yyyy-MM-ddTHH:mm:ssK")
Write-Host "START UTC  :" $Start.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
Write-Host "END   UTC  :" $End.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
```

Do not use a later `UtcNow` value as the converted end time.

## Evidence acceptance

Accept a PurpleWatch detection result only when these correlate:
- controlled test or approved safe primitive
- endpoint `PW-WIN11-01`
- Sysmon process telemetry
- execution window
- Wazuh alert
- rule ID
- expected ATT&CK technique

Do not classify unrelated Wazuh SCA activity as controlled-test evidence.

## Rollback

Validated recovery points:
- Wazuh: `PW-401-Detection-Baseline-Validated`
  - UUID `015434b0-0bb3-4ac3-8123-5e6e5eeabf5a`
- Windows: `PW-401-Detection-Baseline-Validated`
  - UUID `8f721988-3808-4a7a-a245-c92767e630ce`

## Repository boundary

Commit reviewed custom rules, runbooks, sanitized evidence, mappings, and hashes.

Do not commit credentials, `client.keys`, raw Wazuh logs, malware, destructive tests, Atomic payloads, or private keys.
