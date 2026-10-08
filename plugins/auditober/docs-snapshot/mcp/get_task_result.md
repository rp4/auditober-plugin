---
title: get_task_result
description: "Retrieve a durable query task’s result and fresh export link."
---

Retrieve a durable query task’s result and fresh export link. Requires `read:data`.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `taskId` | string | Yes | The task ID returned by `query_data`; at most 64 characters. |

## Example

```json
{
  "name": "get_task_result",
  "arguments": {
    "taskId": "TASK_ID"
  }
}
```

## Behavior

A succeeded small task returns `data`. An exported result returns row count,
columns, a sample, `resource`, a fresh signed `download` URL, format, file
metadata, and truncation information. Load the artifact for complete analysis.
Queued or running tasks return status and a polling note. Failed and cancelled
tasks return terminal status; do not keep polling. If the artifact expired,
rerun the query. Visibility follows the same creator-or-administrator boundary
as [get_task_status](https://docs.assureswarm.com/mcp/get_task_status/).
