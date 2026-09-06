# Atomic Red Team Controlled Validation Runbook

## Purpose

This runbook defines the approved PurpleWatch workflow for installing and using Atomic Red Team inside the private Windows cyber lab.

Atomic Red Team is used only to reproduce reviewed MITRE ATT&CK behaviors for defensive validation.

It is not exposed as an arbitrary remote-command execution mechanism.

## Scope

Initial PurpleWatch P0 techniques:

- T1082 — System Information Discovery
- T1057 — Process Discovery
- T1087.001 — Local Account Discovery
- T1016 — System Network Configuration Discovery
- T1059.001 — PowerShell

## Safety boundaries

Allowed:

- private PurpleWatch lab only
- reviewed Atomic tests
- benign discovery commands
- controlled PowerShell execution
- Sysmon and Wazuh telemetry validation
- recovery through VirtualBox snapshots

Not allowed:

- credential theft
- persistence
- destructive actions
- lateral movement
- arbitrary user-supplied commands
- malware execution
- Mimikatz
- BloodHound collection
- uncontrolled downloads
- public exposure of the Windows endpoint or Wazuh services

## Lab endpoint

Windows endpoint:

`PW-WIN11-01`

Atomic working directory:

`C:\PurpleWatch\AtomicRedTeam`

Atomics folder:

`C:\PurpleWatch\AtomicRedTeam\content\atomics`

## Installed components

PowerShell modules:

- Invoke-AtomicRedTeam 2.3.0
- powershell-yaml 0.4.12

Pinned revisions:

- Invoke-AtomicRedTeam:
  `8af478bb9e4637df568ac1e596553b025b16cd1b`
- Atomic Red Team:
  `388942adbd9641f4dfdcf079d7efe9a75ec0ac43`

Atomic YAML content was installed with `-NoPayloads`.

Do not commit downloaded Atomic content, modules, payloads, raw telemetry, or secrets to this repository.

## PowerShell session preparation

Use a process-scoped execution policy only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
Import-Module powershell-yaml -Force
Import-Module Invoke-AtomicRedTeam -Force
$AtomicsPath = "C:\PurpleWatch\AtomicRedTeam\content\atomics"
```

Do not configure a persistent unrestricted or bypass execution policy.

## Approved P0 tests

- `T1082 #1` — System Information Discovery
- `T1057 #2` — Process Discovery (`tasklist`)
- `T1087.001 #10` — Enumerate logged-on users (`query user`)
- `T1016 #1` — System Network Configuration Discovery
- `T1059.001 #17` — benign Base64-encoded PowerShell execution

Always run `-CheckPrereqs` before executing an approved test.

## Validation workflow

For each test:

1. Record the execution start and end time.
2. Confirm the expected process in Sysmon Event ID 1.
3. Confirm the event reached Wazuh.
4. Identify the Wazuh rule that fired.
5. Compare the Wazuh ATT&CK mapping with the expected technique.
6. Record `PASS`, `PARTIAL`, or `GAP`.
7. Preserve only sanitized evidence in Git.

## Correlation rule

Do not identify an Atomic test only by command name.

Correlate the endpoint, execution window, process image, command line, parent process, Wazuh agent, rule ID, and ATT&CK mapping.

Wazuh Agent SCA activity can independently generate PowerShell and account-discovery commands. Those events must not be classified as controlled Atomic executions.

## Recovery

Snapshots:

- `PW-301-Pre-AtomicRedTeam`
- `PW-301-AtomicRedTeam-Validated`

Use a recovery point before introducing new techniques or changing detection rules when rollback may be required.

## PurpleWatch design requirement

PurpleWatch must expose approved test identifiers, not a free-form remote command field.

Target workflow:

`approved test -> controlled execution -> telemetry -> detection -> ATT&CK comparison -> gap -> improvement -> retest`
