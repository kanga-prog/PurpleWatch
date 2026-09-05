# PW-205 — Wazuh Windows Agent deployment

## Objective

Deploy, enroll and validate the Wazuh Agent on the PurpleWatch Windows laboratory endpoint.

## Endpoint

- Hostname: `PW-WIN11-01`
- Endpoint address: `192.168.56.106`
- Wazuh Manager: `192.168.56.105`
- Agent version: `4.14.7`
- Manager version: `4.14.7`

## Package validation

The Windows agent package was obtained from the official Wazuh package distribution.

Package:

`wazuh-agent-4.14.7-1.msi`

Authenticode validation:

- Status: `Valid`
- Signer: `Wazuh, Inc`

SHA-256:

`E967F36B75589D6210244FD58239C7021FA53A77C38D92315C3B3BD115002EDE`

The MSI package is not stored in this repository.

## Private network validation

Before enrollment, the Windows endpoint validated access to the Wazuh Manager over the private Host-Only network:

- TCP/1514 — agent communication
- TCP/1515 — enrollment

Both ports were reachable from `PW-WIN11-01`.

The Wazuh Manager confirmed:

- `wazuh-remoted` running on TCP/1514
- `wazuh-authd` running on TCP/1515

No public Wazuh service exposure is required.

## Installation

The Wazuh Windows Agent was installed silently with:

- Manager address: `192.168.56.105`
- Registration server: `192.168.56.105`
- Agent name: `PW-WIN11-01`

The final installation was performed synchronously so that MSI completion could be verified before starting the service.

Installation result:

`0`

The service is:

- Name: `WazuhSvc`
- Status: `Running`
- Startup type: `Automatic`

## Enrollment

The agent log confirmed:

- key request to `192.168.56.105`
- agent name `PW-WIN11-01`
- valid key received
- connection to `192.168.56.105:1514/tcp`

The enrollment key material is stored locally by the agent and must never be committed or exposed.

## Manager-side validation

The Wazuh Manager registered the Windows endpoint as:

- Agent ID: `001`
- Name: `PW-WIN11-01`
- Status: `Active`

## Sysmon collection

The Wazuh Agent was configured to collect:

`Microsoft-Windows-Sysmon/Operational`

using:

`eventchannel`

The agent log confirmed:

`Analyzing event log: 'Microsoft-Windows-Sysmon/Operational'.`

The end-to-end arrival of a controlled Sysmon event at the Wazuh Manager is validated separately in PW-206.

## Recovery

Snapshot:

`PW-205-Wazuh-Agent-Connected`

UUID:

`ea82c8ad-b6aa-4a21-a2b9-92f6635c6ae1`

Purpose:

Preserve the validated Wazuh Agent and Sysmon collection baseline before PW-206 end-to-end telemetry testing.

## Security

- No enrollment key committed.
- No agent credentials committed.
- No MSI binary committed.
- Wazuh services remain private to the Cyber Lab.
- PW-203 and PW-204 recovery snapshots are preserved.
