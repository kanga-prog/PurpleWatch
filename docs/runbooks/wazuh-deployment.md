# PW-202 — Wazuh all-in-one deployment

## Objective

Deploy and validate the central Wazuh defensive infrastructure for the PurpleWatch Cyber Lab.

## Architecture

PurpleWatch uses a Wazuh all-in-one virtual machine containing:

- Wazuh Manager 4.14.7
- Wazuh Indexer 4.14.7
- Wazuh Dashboard 4.14.7
- Wazuh API

The VM runs in VirtualBox and remains isolated from the public Internet.

## Network model

Two VirtualBox interfaces are used:

- NAT for controlled outbound access to official updates and downloads.
- Host-Only networking for private laboratory administration and endpoint communication.

No router port forwarding is configured.

Wazuh Dashboard, API, enrollment services, SSH and Indexer must not be exposed directly to the public Internet.

## Virtual machine resources

Validated laboratory allocation:

- CPU: 2 vCPU
- RAM: approximately 4 GiB
- Swap: 2 GiB
- Root disk: 50 GiB dynamic VDI
- Filesystem: XFS

This sizing is intentionally constrained because the physical laboratory host has limited RAM.

## Installation source

The official Wazuh 4.14.7 OVA was used.

The downloaded image was validated against the official SHA-512 checksum before import.

SHA-512:

`16973f765ca9ecdf292237314277b02fa2187996e36c499d599e43fb0fa80ae3a3cc33add7a22f0b2d284e7b82c03d829cd04728afa4b06cc66be73068c3b7f2`

## Storage incident and mitigation

The imported virtual disk initially exposed only 25 GiB to the guest.

During the first Wazuh initialization, the root filesystem reached 98% utilization.

Investigation identified most of the consumption under:

- `/var/ossec/queue/vd/feed`
- `/var/ossec/queue/vd_updater/tmp`

The disk pressure triggered the OpenSearch flood-stage protection and temporarily placed the Dashboard index in read-only mode.

The mitigation was:

1. Temporarily disable Vulnerability Detection for the PurpleWatch MVP.
2. Stop the Wazuh Manager.
3. Remove the temporary Vulnerability Detection updater cache.
4. Restart and validate Wazuh.
5. Convert the original VMDK to a dynamic VDI.
6. Expand the virtual disk from 25 GiB to 50 GiB.
7. Validate the XFS root filesystem at 50 GiB.

After stabilization, root filesystem utilization was approximately 38%.

Vulnerability Detection remains intentionally disabled until it can be re-evaluated without risking the core PurpleWatch telemetry pipeline.

## Memory stabilization

The VM has approximately 4 GiB RAM.

A persistent 2 GiB swap file was configured:

`/swapfile none swap sw 0 0`

This provides additional protection against transient memory pressure without replacing the need for adequate physical RAM.

## Wazuh Manager startup

A slow startup previously exceeded the packaged systemd timeout.

A local systemd override was created instead of modifying the vendor unit:

`/etc/systemd/system/wazuh-manager.service.d/purplewatch.conf`

Configured values:

- `TimeoutStartSec=180`
- `TimeoutStopSec=180`

The Manager subsequently started successfully and all required Wazuh daemons were validated.

## VirtualBox Guest Additions

The `vboxguest` kernel module is loaded.

The compatibility `rc-local.service` initially failed because `/etc/rc.d/rc.local` lacked a shell interpreter declaration.

A `#!/bin/bash` shebang was added and the service was successfully restored.

## Health validation

The following services were validated as active:

- `wazuh-manager`
- `wazuh-indexer`
- `wazuh-dashboard`

Final system validation reported zero failed systemd units.

The Wazuh API reports version 4.14.7 and the Dashboard successfully displays indexed security alerts.

## Recovery point

A VirtualBox snapshot was created after successful stabilization:

`PW-202-Wazuh-Functional`

It represents the functional PW-202 baseline before deployment of the Windows endpoint, Sysmon and Wazuh Agent.

## Security notes

- No secrets are stored in this repository.
- No public port forwarding is configured.
- Administration is restricted to the private Cyber Lab.
- Default credentials must be replaced during the PurpleWatch security-hardening phase before any broader exposure.
- Arbitrary remote command execution is outside the PurpleWatch architecture.

## Known follow-up

WSL-to-VirtualBox Host-Only connectivity is not yet available.

This does not block PW-202 administration because the Windows host can reach the Wazuh VM. A controlled connectivity path will be addressed when the PurpleWatch backend begins consuming the Wazuh API.

## Next milestone

PW-203 deploys the Windows laboratory endpoint.

The subsequent target chain is:

Windows → Sysmon → Wazuh Agent → Wazuh Manager → Wazuh Indexer → Dashboard.
