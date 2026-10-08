---
title: get_step_context
description: "One workflow step in full: instructions, form, approvals, documents, and linked items."
---

Call `get_step_context` before you analyze, summarize, or propose a change to a workflow step: it's the source of truth for what's actually on the step right now. It requires the `read:workflows` scope and returns the step in full: its instructions, its form and current answers, its approvals, its documents, and the items linked to it.

## Input

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `stepId` | string | Yes | None | The workflow step ID. |
| `includeUpstreamDocuments` | boolean | No | `false` | Accepted and echoed back in the response; no upstream traversal is performed. To read earlier steps' documents, resolve the workflow's steps (via `query_data`) and call this tool on each upstream step id: each response carries that step's own documents. |

## Example

```json
{
  "name": "get_step_context",
  "arguments": {
    "stepId": "step_123",
    "includeUpstreamDocuments": true
  }
}
```

## Response

**`step`**

The step in full: its name, description, instructions, result, its form and current answers, its approvals, its documents, and its linked items: limited to what the connected user can access.

Read the form from `step.formData`: its `fields`, `values`, and submission
metadata such as `submittedAt`. Do not assume separate `form.fieldCount` or
`form.isSubmitted` properties exist. Saving a proposed result and recording a
native step approval are separate actions.

**`includeUpstreamDocuments`**

Echoes back the value from your request.

**`hint`**

A fixed next-step suggestion (review the step, then propose changes via `suggest_change`).

## Errors

An unknown or inaccessible step ID returns a not-found error that names the step ID you asked for.

## Agent Notes

- Do not assume a step has a single assignee: read the approvals and form fields in the response instead of guessing from the step name or description.
- Use [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) first to find the step IDs relevant to the connected user, rather than asking them to look one up.
- This tool is read-only: it never changes the step. Propose any change with [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/).
- Fetch again after a suggestion on this step is approved; the context you read earlier may no longer reflect it.
