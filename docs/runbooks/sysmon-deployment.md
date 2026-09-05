# PW-204 — Sysmon deployment

## Objective

Deploy and validate Microsoft Sysmon on the PurpleWatch Windows laboratory endpoint.

## Endpoint

- Hostname: `PW-WIN11-01`
- Platform: Windows 11 Enterprise Evaluation x64
- Sysmon binary: `Sysmon64.exe`
- Sysmon version: `15.21`
- Configuration schema: `4.91`

## Supply-chain validation

The Sysmon executable was downloaded from the official Microsoft Sysinternals source.

Authenticode validation:

- Status: `Valid`
- Signer: `Microsoft Windows Publisher`

SHA-256 of `Sysmon64.exe`:

`A60AA845457406383277AFDEAD35BD90C7804572B99901D239CC974841DF2528`

The Sysmon binary itself is not stored in this repository.

## Configuration

Repository-managed configuration:

`lab/endpoints/windows/sysmon/sysmonconfig.xml`

Configuration SHA-256:

`A89EEF27392308B3220B120A4730562D258D5AE7B8E5925A1720AEFD776484B9`

The active Sysmon configuration reported the same hash.

Enabled telemetry for the MVP baseline:

- Event ID 1 — Process Create
- Event ID 3 — Network Connect
- SHA-256 hashing for process images

## Event channel

Sysmon telemetry is written to:

`Microsoft-Windows-Sysmon/Operational`

This channel will be consumed by the Wazuh Agent during PW-205 and validated end-to-end during PW-206.

## Controlled validation

A benign process was generated:

`cmd.exe /c "echo PW204-SYSMON-VALIDATION"`

Sysmon produced Event ID 1 and recorded:

- image: `C:\Windows\System32\cmd.exe`
- parent image: `powershell.exe`
- command line
- user context
- process hash
- integrity level

No malicious payload was executed.

## Recovery

Validated snapshot:

`PW-204-Sysmon-Validated`

Snapshot UUID:

`7eb6bcd4-cc27-4521-81bd-e0cd921c10f6`

The snapshot was created before Wazuh Agent installation.

## Next

- PW-205 — Wazuh Agent
- PW-206 — End-to-end telemetry
