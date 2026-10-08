---
title: On-Prem Deployment
description: "Run AssureSwarm on your own infrastructure: what ships, system and network requirements, sign-in options, updates, backups, licensing, and the security boundary."
---

On-prem AssureSwarm runs the full product on a server your organization controls. It is the same software the managed cloud runs, the application, the sign-in service, and the MCP endpoint your AI agents connect to, packaged as a self-contained set of containers with its own database and document storage. Your data, your documents, and your encryption keys stay inside your network.

On-prem is part of **Private Collection**, our dedicated commercial tier: it runs the full Masterpiece feature set on hardware you control. [Contact us](https://docs.assureswarm.com/support/) to start an evaluation.

:::note[One install, one organization]
An on-prem install serves a single organization: it is the on-prem equivalent of the dedicated, isolated tenant you would get in the managed cloud. It is not a multi-tenant server.
:::

## What Ships

The deployment is delivered as a versioned bundle: an installer, a set of container images pinned by digest, and operations tooling. The installer asks a short set of questions (your domain, TLS certificates, initial administrator emails, license file), generates every secret and encryption key **locally on your server**, and brings the stack up. AssureSwarm never sees or holds your keys.

| Component | What it does |
|---|---|
| Web application | The AssureSwarm app your team signs into |
| MCP endpoint | The agent-facing API, served under `/mcp` on your app address: see [Connect an agent](https://docs.assureswarm.com/mcp/connect/) |
| Sign-in service | Handles SSO with your identity provider; runs entirely inside your network |
| Database | Bundled PostgreSQL holding all tenant data |
| Object storage | Bundled S3-compatible store for documents and file uploads |
| Reverse proxy | Terminates TLS for the three hostnames below |
| Scheduled jobs | Built-in housekeeping (retention pruning, cleanup) and nightly backups |

## System Requirements

| Requirement | Baseline |
|---|---|
| Server | One VM or physical host, 4 vCPU / 8 GB RAM / 100 GB disk to start |
| Software | A current Docker Engine with the Compose plugin |
| Time | NTP-synchronized clock (signed URLs and sign-in tokens are time-sensitive) |
| DNS | Three names on your domain, e.g. `canvas.example.com`, `auth.canvas.example.com`, `storage.canvas.example.com`: one wildcard record covers all three |
| TLS | A wildcard or three-name certificate; bring your own, use your internal CA, or let the appliance obtain one automatically |

Larger teams can scale the application's resources with documented settings; the baseline above is sized for a typical department-scale rollout.

## Network Boundary

Outbound connectivity is needed only to pull software: the container registry and release bundles, over HTTPS. Beyond that, the appliance makes no calls to AssureSwarm: **no telemetry, no license phone-home, no data egress**. If you enable "Sign in with Google" or "Sign in with Microsoft", the sign-in flow reaches those identity services; SAML against an identity provider inside your network needs no internet at all.

Inbound exposure is your choice. If your AI agents run inside your network, the MCP endpoint never needs to be reachable from outside; if you want agents or users connecting from elsewhere, expose the hostnames through your existing edge controls.

## Signing In

The on-prem sign-in service supports the same options as the cloud:

- **SAML**: connect Okta, Microsoft Entra ID, ADFS, Keycloak, or any SAML 2.0 identity provider. This is the recommended path, and works with identity providers that are themselves on-prem.
- **Google or Microsoft sign-in**: supported, with one difference from the cloud: because the sign-in addresses are on *your* domain, your team registers its own OAuth application with Google or Microsoft and supplies the client credentials during setup.

User provisioning works as in the cloud: administrators listed at install time can sign in immediately, and [allowed sign-in domains](https://docs.assureswarm.com/admin/users-and-access/) auto-provision everyone else.

## Updates

- Releases are cut regularly (roughly monthly) as versioned bundles, with release notes.
- Updating is a single operation run by your administrator: it snapshots the database first, then rolls the stack to the new version. Database migrations apply automatically.
- Versions can be skipped: updating from an older release straight to the newest is supported.
- The current and previous release are supported at any time; staying within that window keeps you eligible for support.

There are no forced or automatic updates. Your team chooses when to move.

## Backups and Recovery

The appliance backs itself up nightly, database and document storage, with a configurable retention window, and the same tooling restores from any backup. Every update also takes a pre-update snapshot, which is the rollback point if an update needs to be undone. Moving backup copies off the server (to your backup infrastructure) is your team's responsibility and is covered in the operations guide.

## Licensing

On-prem installs use a signed license file issued for your organization, verified locally: no license server, no online activation. If a license lapses, administrators see a renewal notice and a grace period begins; **the product keeps working**. There is no remote kill switch.

## Security Posture

- **Keys are yours.** Every secret, database credentials, session and token signing keys, the field-encryption key protecting sensitive values at rest, is generated on your server at install time. AssureSwarm never has them.
- **Audit trail.** The tenant [activity log](https://docs.assureswarm.com/admin/) behaves exactly as in the cloud, and the database enforces its append-only audit records. The appliance also emits structured security-event logs that your team can ship to your SIEM, so audit evidence can be copied into infrastructure the application itself cannot touch.
- **Isolation.** Only the reverse proxy accepts connections; the database, object storage, and internal services are not directly reachable.

:::note[The trade you are making]
In the managed cloud, AssureSwarm operates infrastructure-level safeguards beneath the application, independent audit-log archival, managed database controls, monitored operations. On-prem, your organization owns that layer: host hardening, OS patching, backup custody, and SIEM retention are in your hands. Anyone with root access to the host can, by definition, reach everything on it. For most organizations choosing on-prem, that is precisely the point, but it is a responsibility transfer worth naming.
:::

## Not in the First Release

Planned but not part of the initial on-prem release:

- Kubernetes / Helm packaging (the appliance targets a single Docker host)
- Multi-node high availability
- Fully offline (air-gapped) delivery: the design is compatible with it, but v1 assumes outbound registry access

If one of these is a hard requirement for your environment, [tell us](https://docs.assureswarm.com/support/): it directly informs what ships next.

## Getting Started

1. [Contact us](https://docs.assureswarm.com/support/) to scope an evaluation: environment review, license, and registry access.
2. Provision the server, DNS names, and certificate from the requirements above.
3. Run the installer with your license file; sign in as one of the initial administrators.
4. Configure your tenant exactly as the [Admin guide](https://docs.assureswarm.com/admin/) describes: from here on, cloud and on-prem documentation are one and the same.
