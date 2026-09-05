# Windows laboratory endpoint

This directory documents the PurpleWatch Windows endpoint.

## PW-203 baseline

Current endpoint:

- Windows 11 Enterprise Evaluation x64
- Hostname: `PW-WIN11-01`
- 2 vCPU
- 4 GiB RAM
- 80 GiB dynamic VDI
- NAT + Host-Only networking
- OpenSSH administration restricted to the private lab network

Private Host-Only address:

`192.168.56.106`

Validated clean recovery snapshot:

`PW-203-Windows-Clean`

## Documentation

- [Cyber Lab topology](../../../docs/architecture/lab-topology.md)
- [Lab isolation policy](../../../docs/security/lab-isolation.md)
- [Lab recovery runbook](../../../docs/runbooks/lab-recovery.md)
- [Windows endpoint deployment](../../../docs/runbooks/windows-endpoint.md)
- [PW-203 validation evidence](../../../docs/evidence/PW-203.md)

## Security boundary

The endpoint is laboratory infrastructure.

No public RDP exposure or router port forwarding is permitted.

Secrets and authentication material must never be committed.

## Next

PW-204 adds Sysmon instrumentation.

PW-205 installs the Wazuh Agent.

PW-206 validates the complete telemetry path.
