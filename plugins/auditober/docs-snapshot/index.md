---
title: AssureSwarm Docs
description: "User, administrator, and agent documentation for AssureSwarm: structured records, workflows, approvals, forms, dashboards, and MCP-connected AI agents."
---

AssureSwarm is a configurable work management platform. Teams model their work as *items*, issues, risks, audits, controls, vendors, or whatever record types a tenant configures, and run repeatable *workflows* over them: steps, approvals, forms, and documents, all tracked on *dashboards*.

AI agents are first-class users of AssureSwarm, not an add-on. They connect over MCP, read the data they're permitted to see, and propose changes as *suggestions* that a person reviews and approves before anything is applied. This site is written for both audiences: people and agents; every page here is also mirrored as raw Markdown an agent can fetch directly (see [For AI Agents](#for-ai-agents) below).

## Choose Your Path

| Audience             | Start here                                                                                  |
| -------------------- | ------------------------------------------------------------------------------------------- |
| Users                | [Getting started](https://docs.assureswarm.com/getting-started/), [Using AssureSwarm](https://docs.assureswarm.com/using-coworkcanvas/)             |
| Administrators       | [Admin guide](https://docs.assureswarm.com/admin/)                                                                      |
| IT & platform teams  | [Deployment options](https://docs.assureswarm.com/deployment/), [On-prem deployment](https://docs.assureswarm.com/deployment/on-prem/)              |
| Agents & integrators | [Connect an agent](https://docs.assureswarm.com/mcp/connect/), [MCP overview](https://docs.assureswarm.com/mcp/), [Agent operating guide](https://docs.assureswarm.com/agents/) |

## What's In These Docs

| Section                                   | Covers                                                                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [Getting started](https://docs.assureswarm.com/getting-started/)      | First sign-in through your first completed step, form response, and suggestion review.                                   |
| [Concepts](https://docs.assureswarm.com/concepts/)                    | How items, item types, workflows, forms, suggestions, and permissions fit together.                                      |
| [Using AssureSwarm](https://docs.assureswarm.com/using-coworkcanvas/) | Day-to-day tasks: working with items, working a step, reviewing suggestions.                                             |
| [Admin guide](https://docs.assureswarm.com/admin/)                    | Configuring item types, users and access, workflow templates, imports and exports, and AI integrations.                  |
| [Deployment](https://docs.assureswarm.com/deployment/)                | The managed cloud service and the self-hosted on-prem option: requirements, updates, backups, and the security boundary. |
| [Agent operating guide](https://docs.assureswarm.com/agents/)         | How an AI agent should behave in AssureSwarm: read first, suggest changes, stay in scope.                                |
| [MCP](https://docs.assureswarm.com/mcp/)                              | Connecting and calling the MCP tools that give agents read and suggestion access to a tenant.                            |
| [GraphQL](https://docs.assureswarm.com/graphql/)                      | Running read-only queries against the same data model.                                                                   |
| [Reference](https://docs.assureswarm.com/reference/)                  | Field types, scopes, limits, statuses, and glossary in one place.                                                        |
| [Troubleshooting](https://docs.assureswarm.com/troubleshooting/)      | Fixes for common sign-in, access, and connection problems.                                                               |
| [Support](https://docs.assureswarm.com/support/)                      | How to get help, and what to include, and leave out, in a request.                                                       |

## For AI Agents

This site mirrors every page as raw Markdown, so an agent can fetch documentation directly instead of scraping rendered HTML:

```text
https://docs.assureswarm.com/llms.txt: index of all pages
https://docs.assureswarm.com/raw/<path>.md: raw markdown for any page
https://docs.assureswarm.com/raw/index.json: machine-readable file list
https://docs.assureswarm.com/static/contentIndex.json: search index
```

Start at the [Agent operating guide](https://docs.assureswarm.com/agents/): it covers how to connect, what scopes mean, and how the suggestion review cycle works.

## Public Boundary

These docs cover supported product behavior and public integration patterns. They intentionally exclude private deployment details, internal configuration, credentials, and customer data.
