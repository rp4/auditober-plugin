---
title: Deployment Options
description: "How AssureSwarm is delivered: the managed cloud service, and the self-hosted on-prem option for organizations that run it on their own infrastructure."
---

AssureSwarm is delivered two ways. Most customers use the **managed cloud service**: AssureSwarm operates everything, and each customer's tenant runs in its own isolated environment, its own application instances, its own database, its own document storage, never pooled with other customers. There is nothing to install; you get a tenant address, sign in through your organization's identity provider, and start working.

Organizations with data-residency, regulatory, or network-isolation requirements can instead run AssureSwarm **on their own infrastructure**. The on-prem deployment is the same product, same application, same workflows, same agent access over MCP, packaged to run on a server you control, with your keys, your database, and your documents never leaving your network.

| Option | Operated by | Where your data lives | Best for |
|---|---|---|---|
| Managed cloud | AssureSwarm | An isolated, single-tenant environment dedicated to you | Most teams: fastest to start, zero operations |
| [On-prem](https://docs.assureswarm.com/deployment/on-prem/) | Your IT team | Your servers, your network | Data-residency mandates, strict network boundaries, "no vendor cloud" policies |

Feature behavior is identical in both: the pages in the rest of this documentation apply equally to cloud and on-prem tenants. The differences are operational, who runs the infrastructure, how sign-in is wired to your identity provider, and how updates and backups happen, and those are covered in [On-prem deployment](https://docs.assureswarm.com/deployment/on-prem/).
