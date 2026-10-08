---
title: get_schema
description: Discover item types, fields, writable target types, and the read-query catalog before doing anything else.
---

Call `get_schema` first. Every other tool call keys off the field keys, target types, and query signatures it returns.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `type` | string | No | A target type or item type slug to inspect. Omit to get the full discovery payload. |

`get_schema` requires the `read:data` scope.

## What You Get Back

What comes back depends on the `type` argument you send.

**No arguments.** Returns the full discovery payload:

- `queryReference`: the catalog of every read query field and its signature, the same catalog documented in full on [GraphQL](https://docs.assureswarm.com/graphql/).
- `itemTypes`: summaries of the tenant's configured item types.
- `targetTypes`: writable non-item targets for [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/), each with its allowed operations and fields.
- `linkingTypes`: the linking targets: `itemrelationship`, `stepitemlink`, `stepdocumentlink`, and `workflowtemplatestepitemlink`.

```json
{
  "name": "get_schema",
  "arguments": {}
}
```

**`type` set to a target type.** Pass a value such as `"step"`, `"workflow"`, or `"workflowtemplate"` to get that target's schema: name, description, allowed operations, and field definitions.

```json
{
  "name": "get_schema",
  "arguments": { "type": "step" }
}
```

**`type` set to an item type slug.** Pass a value such as `"issue"` to get the full item type, including its field definitions and select option values.

```json
{
  "name": "get_schema",
  "arguments": { "type": "issue" }
}
```

**Unknown `type`.** Returns a text response listing the valid target and linking types and suggesting a bare `get_schema` call.

## Agent Notes

- Use the field keys and option values `get_schema` returns exactly: don't infer them from labels.
- Slugs are tenant-specific. Never reuse a slug from one tenant on another.
- Configuration changes over time. Re-check `get_schema` after an administrator edits item types or fields.
