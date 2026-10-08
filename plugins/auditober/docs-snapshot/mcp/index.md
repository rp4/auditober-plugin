---
title: MCP Overview
description: "The AssureSwarm MCP server: endpoint, protocol, authentication, scopes, tools, limits, and error behavior."
---

The AssureSwarm MCP server lets approved AI agents inspect schema, read permitted data, exchange documents, and propose changes as human-reviewed [suggestions](https://docs.assureswarm.com/concepts/suggestions/). New here? The step-by-step client setup lives in [Connect an agent](https://docs.assureswarm.com/mcp/connect/). For a ready-made set of slash commands built on these tools, see the [current plugin catalog](https://assureswarm.com/plugins/).

## Endpoint and Protocol

Your tenant's MCP server is available at:

```text
https://<tenant>.assureswarm.com/mcp
```

| Property             | Value                                                                 |
| -------------------- | --------------------------------------------------------------------- |
| Transport            | Streamable HTTP                                                       |
| Request format       | JSON-RPC 2.0                                                          |
| MCP protocol version | Negotiates `2024-11-05`, `2025-03-26`, `2025-06-18`, and `2025-11-25` |
| Server name          | `coworkcanvas-mcp`                                                    |
| Server version       | `1.0.0`                                                               |

## Authentication

Every call carries:

```http
Authorization: Bearer <access-token>
```

There are two ways to get a token:

* **OAuth 2.0**: for AI platform integrations. Uses the authorization code flow, with PKCE for public clients. Dynamic client registration is supported.
* **Personal tokens**: for individual use. Generated on your tenant's OAuth Setup page; they expire after 30 days.

Clients can discover the OAuth endpoints automatically:

```text
https://<tenant>.assureswarm.com/.well-known/oauth-authorization-server
https://<tenant>.assureswarm.com/.well-known/oauth-protected-resource
```

See [Connect an agent](https://docs.assureswarm.com/mcp/connect/) for setup steps and [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/) for how administrators govern access.

## Tools and Scopes

| Tool                                                         | Purpose                                                                            | Required scope      |
| ------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------- |
| [get\_schema](https://docs.assureswarm.com/mcp/get_schema/)                              | Inspect item types, fields, target types, and the query catalog                    | `read:data`         |
| [query\_data](https://docs.assureswarm.com/mcp/query_data/)                              | Run read-only GraphQL queries                                                      | `read:data`         |
| [get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/)           | The connected user's page context and assigned work                                | `read:context`      |
| [get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/)                 | One workflow step in full                                                          | `read:workflows`    |
| [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/)                      | Propose creates, updates, deletes, form submissions, and branch pruning for review | `write:suggestions` |
| [list\_pending\_suggestions](https://docs.assureswarm.com/mcp/list_pending_suggestions/) | List suggestions awaiting human review                                             | `read:suggestions`  |
| [get\_task\_status](https://docs.assureswarm.com/mcp/get_task_status/)                   | Check an asynchronous query task                                                   | `read:data`         |
| [get\_task\_result](https://docs.assureswarm.com/mcp/get_task_result/)                   | Retrieve a completed query task result                                             | `read:data`         |
| [cancel\_task](https://docs.assureswarm.com/mcp/cancel_task/)                            | Cancel a queued or running query task                                              | `read:data`         |
| [submit\_card\_action](https://docs.assureswarm.com/mcp/submit_card_action/)             | Relay a human decision from a card with its single-use token                       | `read:context`      |
| [upload\_document](https://docs.assureswarm.com/mcp/upload_document/)                    | Upload to a step or replace an item document field                                 | `write:documents`   |
| [download\_document](https://docs.assureswarm.com/mcp/download_document/)                | Retrieve a permitted document                                                      | `read:documents`    |

A token missing a tool's required scope gets a scope error for that tool only: it doesn't affect the rest of the session. Some tools degrade gracefully instead of erroring: `get_current_context` returns empty work lists with a hint when `read:workflows` is missing.

## Permissions Model

:::note\[The token acts as the connected user]
Scopes narrow what a token may do; they never grant more than the connected user's own permissions. Page access, item permissions, and visibility still apply underneath every call. Proposed record changes land as [suggestions](https://docs.assureswarm.com/concepts/suggestions/) pending human approval. Document uploads and cancellation of the caller’s query tasks are direct operations. Card actions relay a human decision using a single-use possession token; the model gains no approval authority.
:::

See [Permissions](https://docs.assureswarm.com/concepts/permissions/) for the full model.

## Request Format

List tools:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

Call a tool:

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "get_schema",
    "arguments": {}
  }
}
```

## Limits

| Limit                         | Value                                               |
| ----------------------------- | --------------------------------------------------- |
| Query text (`query_data`)     | ≤ 64 KB                                             |
| Tool response                 | ≤ 2 MB                                              |
| Document upload (decoded)     | ≤ 10 MB                                             |
| Document download             | ≤ 10 MB (default cap 5 MB unless `maxBytes` is set) |
| `get_current_context` `limit` | 1–100 (default 10)                                  |
| Personal token lifetime       | 30 days                                             |

See [Reference](https://docs.assureswarm.com/reference/) for the full limits list.

## Errors

MCP errors fall into two categories:

* **Protocol errors**: malformed JSON-RPC, an unknown tool name. These fail at the transport level, before any tool runs.
* **Tool-level errors**: returned inside a successful JSON-RPC envelope with `isError: true`. These cover input validation failures, permission denials, and rejected GraphQL operations (for example, sending a `mutation` to `query_data`).

Input validation errors name the offending field. Read the error before retrying: never retry the same call unchanged.

## Agent Notes

* Read the [Agent operating guide](https://docs.assureswarm.com/agents/) before you start.
* Call `get_schema` first.
* Use `query_data` only for reads.
* Use `suggest_change` for proposed writes.
* A token does not bypass AssureSwarm permissions.
* Do not retry the same failing call unchanged.
