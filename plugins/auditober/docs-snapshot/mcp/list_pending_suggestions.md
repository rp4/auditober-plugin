---
title: list_pending_suggestions
description: "List suggestions awaiting the connected user’s review."
---

List suggestions awaiting the connected user’s review. Requires `read:suggestions`.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `take` | integer | No | 1–100; default 20. |

## Example

```json
{
  "name": "list_pending_suggestions",
  "arguments": {
    "take": 20
  }
}
```

## Behavior

Returns `count`, a review note, and `suggestions` with IDs, operations, target
types, agent names, creation times, and human `previewUrl` links. `count` is the
full pending count and may exceed the returned list. This tool reads the queue;
it does not approve or reject suggestions. Hand the review links to the human.
