---
title: AI Integrations
description: "Enable the AI platforms your organization uses, understand each person’s browser authorization and the personal-token fallback, and watch what agents actually do in your tenant."
sidebar:
  order: 6
---

Enable
Connect
Watch

Scroll

**AI Integrations**, from the Administration page, is the tenant-wide half of
agent access. The other half belongs to each person: you decide which platforms
may connect at all, and they decide whether to connect one to their own account.

## Enable a platform

**Popular AI Platforms** carries a card each for **Claude**, **ChatGPT**,
**Google Gemini**, and **Microsoft Copilot**, with a toggle on the right of
each. Turning one on registers an OAuth client for that platform in one action,
with its redirect URIs already correct, and turning it off withdraws the
integration for everyone at once.

If enabling a platform produces a client secret, it appears once in a dialog.
Copy it then. **Rotate** issues a replacement later and the old secret stops
working immediately, so rotate only when you are ready to update whatever holds
the current one.

## What each person does next

Enabling a platform does not connect anybody. Each person completes
browser sign-in and consent when the approved AI client asks them to
authorize AssureSwarm. OAuth is the normal connection path; see
[Connect an agent](https://docs.assureswarm.com/mcp/connect/) for the client-specific procedure.

The screenshot shows **AI Agent Setup**, the personal-token fallback for
clients that cannot use OAuth or for short-lived testing. Name a token,
press **Generate Token**, and copy it immediately: it is shown once and
expires after 30 days. Its owner can revoke it from that page.

## Watch it run

The **AI Activity** dashboard is your standing answer to what the agents are
actually doing. The tiles across the top count suggestions pending now,
approved, and rejected, then give you the approval rate and the median time a
decision takes.

Read the approval rate as a quality signal about the agent, not about your
reviewers. A rate near the floor usually means an agent's instructions or its
scopes need narrowing; a long median decision time usually means the review
queue needs an owner.

## The two ways an agent gets in

|                | OAuth client                                                                                       | Personal token                                     |
| -------------- | -------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Audience       | An AI platform many people in the tenant use.                                                      | One person, for their own use.                     |
| Who authorizes | Each person authorizes the client for themselves, then the agent acts within that person's access. | The person generates it for themselves.            |
| Lifetime       | Until the client or the authorization is revoked.                                                  | 30 days, then it expires.                          |
| Your control   | Register the client, restrict its scopes, deactivate it.                                           | Indirect: deactivate the user, or wait for expiry. |

Both paths end in the same place. Whichever one an agent arrives through, it is
acting as exactly one person and can never exceed what that person could do by
hand.

## Custom clients

**Custom Clients**, below the platform cards, is for anything not on the list.
**Create Client** asks for a name and the redirect URIs the platform publishes,
which you take from that platform's own setup documentation rather than inventing.

Most AI platforms register as public clients: they authenticate with PKCE and hold
no secret. A confidential client holds a secret and authenticates with it directly.
Which kind you are creating is the platform's decision, not yours.

Compatible MCP clients can also register themselves, discovering the tenant's
OAuth configuration at:

```text
https://<tenant>.assureswarm.com/.well-known/oauth-authorization-server
```

See the [MCP overview](https://docs.assureswarm.com/mcp/) for the endpoints behind any platform's setup flow.

## Scopes

Each MCP tool requires a scope:

| Tool                       | Required scope      |
| -------------------------- | ------------------- |
| `get_schema`               | `read:data`         |
| `query_data`               | `read:data`         |
| `get_current_context`      | `read:context`      |
| `get_step_context`         | `read:workflows`    |
| `upload_document`          | `write:documents`   |
| `download_document`        | `read:documents`    |
| `suggest_change`           | `write:suggestions` |
| `list_pending_suggestions` | `read:suggestions`  |
| `get_task_status`          | `read:data`         |
| `get_task_result`          | `read:data`         |
| `cancel_task`              | `read:data`         |
| `submit_card_action`       | `read:context`      |

A client that requests authorization without naming scopes receives a default
grant: `openid profile email read:context read:items read:workflows
read:dashboards read:documents read:suggestions write:suggestions read:data
write:documents`. That is broad reading, document upload, and suggestions. It is
not direct writes to items, workflows, or dashboards, because those always go
through a suggestion regardless of scope.

Narrowing a client's allowed scopes below that default is your sharpest tool.
Restrict a reporting agent to `read:data` and `read:context` and it cannot call
`suggest_change` or `upload_document` however it is prompted. See
[Permissions](https://docs.assureswarm.com/concepts/permissions/) for the full scope catalog.

:::note\[Two boundaries, always]
Scopes bound the token: it can only call the tools they allow. The connected
person's own permissions bound everything underneath, page access and item
permissions included. A token is never larger than the person behind it.
:::

## Why broad scopes are less alarming than they look

Even with every scope and full permissions, an agent's write path ends in a
proposal. [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/) creates a pending
[suggestion](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/), never an applied change,
and a person approves it under their own permissions.

Scopes decide what an agent may attempt. People still decide what happens to your
data.

## Cutting access off

Match the revocation to what you are actually trying to stop:

| Situation                               | Action                                                                                                                                     |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| The integration itself is the problem   | Toggle the platform off, or deactivate the custom client. Every user connected through it loses access at once.                            |
| One person should no longer have access | Deactivate the user in [User Permissions](https://docs.assureswarm.com/admin/users-and-access/). That stops everything acting as them, OAuth and personal token alike. |
| One token is suspect                    | Have its owner revoke it on their AI Agent Setup page. It stops working immediately.                                                       |
| Nothing is wrong and you can wait       | Personal tokens expire on their own in 30 days.                                                                                            |

Reach for the narrowest action that solves the problem. Turning a platform off
because one person misused it takes the tool away from everyone else too.

## What lands in the log

Registering a client, toggling a platform, rotating a secret, and deactivating a
client are all recorded in the [activity log](https://docs.assureswarm.com/admin/activity-log/) as
`oauth-client` entries with the administrator who made the change. Individual
suggestions record the proposing agent and the person who decided, so any single
change an agent made is traceable end to end.

And when an agent connects

## For agents

The connection journey a person follows is documented at
[Connect an agent](https://docs.assureswarm.com/mcp/connect/), and the protocol behind it at
[MCP](https://docs.assureswarm.com/mcp/). Once connected, an agent reads with
[get\_schema](https://docs.assureswarm.com/mcp/get_schema/), [query\_data](https://docs.assureswarm.com/mcp/query_data/), and
[get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/), all scoped to its user, and
writes only by proposing through [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/). No
scope grants an agent tenant configuration: it cannot create a user, grant a
page, register a client, or enable a platform.
