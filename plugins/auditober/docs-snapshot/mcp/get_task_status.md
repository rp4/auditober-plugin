---
title: get_task_status
description: "Check a durable task started by an asynchronous query."
---

Check a durable task started by an asynchronous query. Requires `read:data`.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `taskId` | string | Yes | The task ID returned by `query_data`; at most 64 characters. |

## Example

```json
{
  "name": "get_task_status",
  "arguments": {
    "taskId": "TASK_ID"
  }
}
```

## Behavior

Returns `taskId`, `type`, `status`, timestamps, and `error`. Poll while work is
queued or running. On `succeeded`, call [get_task_result](https://docs.assureswarm.com/mcp/get_task_result/).
Stop on `failed` or `cancelled`. Tasks are visible to their creator or an
administrator; inaccessible and unknown IDs both produce a not-found error.
