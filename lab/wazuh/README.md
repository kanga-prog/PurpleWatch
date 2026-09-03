# Wazuh central defensive engine

This directory documents the central Wazuh infrastructure used by the PurpleWatch Cyber Lab.

## PW-202 baseline

The current laboratory baseline uses Wazuh 4.14.7 in an all-in-one VirtualBox VM:

- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- Wazuh API

Networking is restricted to NAT plus a private Host-Only laboratory network.

Validated resources:

- 2 vCPU
- approximately 4 GiB RAM
- 2 GiB swap
- 50 GiB dynamic VDI

The validated recovery snapshot is:

`PW-202-Wazuh-Functional`

Vulnerability Detection is temporarily disabled to protect the constrained MVP laboratory from excessive local storage consumption.

## Documentation

- [Cyber Lab topology](../../docs/architecture/lab-topology.md)
- [Lab isolation policy](../../docs/security/lab-isolation.md)
- [Lab recovery runbook](../../docs/runbooks/lab-recovery.md)
- [Wazuh deployment runbook](../../docs/runbooks/wazuh-deployment.md)
- [PW-202 validation evidence](../../docs/evidence/PW-202.md)

## Security boundary

Wazuh services must not be directly exposed to the public Internet.

No secrets, passwords or API credentials belong in this repository.
