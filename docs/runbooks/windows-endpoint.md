# PW-203 — Windows laboratory endpoint

## Objective

Deploy and validate the Windows endpoint used to generate controlled security telemetry for the PurpleWatch Cyber Lab.

## Platform

Validated endpoint:

- Windows 11 Enterprise Evaluation x64
- Hostname: `PW-WIN11-01`
- VirtualBox VM: `PurpleWatch-Windows`
- 2 vCPU
- 4 GiB RAM
- 80 GiB dynamic VDI
- EFI firmware
- TPM 2.0 configured
- VBoxSVGA graphics

## Networking

The endpoint uses two VirtualBox adapters:

- NAT for controlled outbound Internet access.
- Host-Only for private PurpleWatch laboratory communication.

Validated addresses:

- NAT: `10.0.2.15/24`
- Host-Only: `192.168.56.106/24`

The endpoint successfully reached:

- the VirtualBox host on the Host-Only network;
- the Kali lab VM;
- external HTTPS services through NAT.

No router port forwarding or public RDP exposure is configured.

## Administrative access

The local laboratory account is:

`purplewatch`

The account was validated with local administrator privileges.

OpenSSH Server was installed so that the endpoint can be administered from the physical Windows host without relying on VirtualBox clipboard integration.

SSH is reachable through the private Host-Only network on TCP/22.

The firewall rule is limited to:

`192.168.56.0/24`

No passwords or authentication secrets are stored in this repository.

## Installation notes

The endpoint was created from the official Windows 11 Enterprise Evaluation x64 ISO.

SHA-256 validated during deployment:

`300C8A8C470CC94B8502D2851F72A0EFC96F5699387DE86AC2E469544C9DE880`

The evaluation VM is considered disposable laboratory infrastructure.

PurpleWatch portfolio evidence must remain reproducible through repository documentation, configurations, rules, tests and sanitized evidence rather than depending on the lifetime of this specific VM.

## Resource constraint

The physical host has approximately 8 GiB RAM.

Running the Windows endpoint and the Wazuh all-in-one VM simultaneously therefore requires careful resource management.

WSL may be stopped temporarily during memory-intensive VM operations.

## Recovery baseline

A clean VirtualBox snapshot was created before Sysmon and Wazuh Agent installation:

`PW-203-Windows-Clean`

This snapshot provides the recovery baseline for subsequent endpoint instrumentation.

## Next milestones

- PW-204 — Sysmon
- PW-205 — Wazuh Agent
- PW-206 — End-to-end telemetry
