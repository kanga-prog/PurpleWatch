# PW-206 — End-to-end telemetry validation runbook

## Objective

Validate:

`Windows → Sysmon → Wazuh Agent → Wazuh Manager`

## Preconditions

- `PurpleWatch-Wazuh` running
- `PurpleWatch-Windows` running
- Sysmon service running
- Wazuh Agent running
- Agent `PW-WIN11-01` reported `Active`

## Controlled test

Generate a benign marker:

`cmd.exe /c echo PW206-E2E-ARCHIVE-VALIDATION`

Confirm locally that Sysmon records Event ID `1`.

Expected fields:

- Image: `C:\Windows\System32\cmd.exe`
- Channel: `Microsoft-Windows-Sysmon/Operational`
- Command line contains the PW-206 marker

## Wazuh validation

The generic Sysmon Event ID 1 rule `61603` is level `0`.

If the controlled event does not appear in alerts, temporarily enable:

`<logall_json>yes</logall_json>`

Restart `wazuh-manager`, generate a fresh marker and search:

`/var/ossec/logs/archives/archives.json`

Confirm:

- agent ID `001`
- agent name `PW-WIN11-01`
- Sysmon Event ID `1`
- command line contains the marker

## Restore configuration

Immediately restore:

`<logall_json>no</logall_json>`

Restart the Manager and verify:

- `wazuh-manager` is active
- agent `001 / PW-WIN11-01` is `Active`

## Security

- Do not commit raw archive files.
- Do not expose credentials.
- Do not display or commit `client.keys`.
- Keep Wazuh services private to the Cyber Lab.
- Disable full JSON archiving after the test.

## Success criterion

The test succeeds when the same controlled process marker is confirmed from the Windows endpoint through Sysmon and the Wazuh Manager.
