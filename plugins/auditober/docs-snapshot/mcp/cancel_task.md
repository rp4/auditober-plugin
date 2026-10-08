---
title: cancel_task
description: "Stop a queued or running asynchronous query task."
---

Stop a queued or running asynchronous query task. Requires `read:data`.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `taskId` | string | Yes | The task ID returned by `query_data`; at most 64 characters. |

## Example

```json
{
  "name": "cancel_task",
  "arguments": {
    "taskId": "TASK_ID"
  }
}
```

## Behavior

Returns `taskId` and `status: "cancelled"` after a successful cancellation.
The caller must own the task or be an administrator. A task that has already
finished cannot be cancelled. Cancellation does not delete an export artifact
already created. This operation stops computation directly; it does not
create a record-change suggestion.
