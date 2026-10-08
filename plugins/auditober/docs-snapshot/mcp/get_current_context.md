---
title: get_current_context
description: "The connected user's current page and assigned work: approvals to give, forms to answer, workflows they own."
---

Call `get_current_context` early in a conversation: before you assume what page the user is on, or what work belongs to them. It requires the `read:context` scope. The response combines the user's current page context with the work assigned to or owned by them: steps awaiting their approval, forms they need to answer, and workflows they own.

## Input

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `includeCompleted` | boolean | No | `false` | Include completed work alongside pending work. |
| `limit` | integer | No | `10` | Maximum items per list. Range 1–100. |

## Example

```json
{
  "name": "get_current_context",
  "arguments": {
    "includeCompleted": false,
    "limit": 10
  }
}
```

## Response

**`currentView`**

The user's most recent page context. When they're viewing a specific item, workflow, step, or diagram node, this identifies it; otherwise it reflects just the page type or URL. `null` when the current page isn't known.

**`currentWorkflowSteps`**

Present when `currentView` shows the user looking at a workflow: that workflow's steps, up to `limit` of them.

**`ownedWorkflows`**

The workflows the user owns.

**`assignedSteps`**

The steps awaiting the user's approval. Only pending approvals are included unless `includeCompleted` is `true`. Each entry includes the user's own approval status and review level for that step.

**`assignedForms`**

The user's form assignments.

**`note`**

A fixed explanation of the assignment model: AssureSwarm has no single step "assignee": approvals and form assignments are what route work to people.

**`hint`**

A next-step suggestion based on the rest of the response, for example "You are viewing step X. Use get_step_context for details."

## Assignment Model

:::note[There's no step assignee]
AssureSwarm steps don't have a single "assignee." Work reaches people through **approvals** (who needs to sign off, and at what review level) and **form assignments** (who needs to answer a step's form). The `assignedSteps` and `assignedForms` fields above reflect both channels. See [Workflows](https://docs.assureswarm.com/concepts/workflows/) for how steps, approvals, and forms fit together.
:::

## Scope Degradation

If the connected token doesn't include the `read:workflows` scope, `get_current_context` still succeeds rather than returning an error. The work-related lists in the response come back empty, and `hint` names the scope you're missing. Re-authorize the connection with `read:workflows` included to have those lists populated on the next call.

## Agent Notes

- Call it before assuming what the user is currently looking at or what's on their plate.
- Follow `hint`: it's generated from the same response and usually names the next tool call worth making.
- Use the IDs this tool returns, for steps, workflows, items, directly in your next calls, instead of asking the user to paste IDs.
- If a work list comes back empty, check `hint` before concluding the user has nothing assigned; it may be a missing scope, not an empty inbox.
