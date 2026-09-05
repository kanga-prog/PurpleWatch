# PurpleWatch Wazuh Windows Agent

This directory contains the reproducible Wazuh Agent configuration used by the PurpleWatch Windows laboratory endpoint.

## Endpoint

- Hostname: `PW-WIN11-01`
- Wazuh Agent: `4.14.7`
- Wazuh Manager: `192.168.56.105`
- Agent ID observed on Manager: `001`

## Communication

Private Cyber Lab transport:

- TCP/1514 — agent communication
- TCP/1515 — enrollment

No public Wazuh service exposure is required.

## Sysmon collection

The agent collects:

`Microsoft-Windows-Sysmon/Operational`

using:

`sysmon-localfile.xml`

This fragment is inserted inside the Windows agent `ossec.conf`.

It allows Sysmon telemetry generated on the Windows endpoint to be forwarded to the Wazuh Manager.

## Security

Do not commit:

- `client.keys`
- enrollment credentials
- private keys
- Wazuh MSI packages
- raw sensitive event logs

Only sanitized configuration and evidence belong in this repository.

## Validation

PW-205 confirmed:

- Wazuh Agent service running
- successful enrollment
- active connection to the Manager
- agent visible as `Active`
- Sysmon Operational event channel loaded by the agent

## Documentation

- [PW-205 deployment runbook](../../../../docs/runbooks/wazuh-agent-deployment.md)
- [PW-205 evidence](../../../../docs/evidence/PW-205.md)

## Next

PW-206 validates the complete path:

`Windows → Sysmon → Wazuh Agent → Wazuh Manager`
