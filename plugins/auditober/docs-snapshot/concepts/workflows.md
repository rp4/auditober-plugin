---
title: Workflows
description: "How AssureSwarm workflows run: templates, steps, approvals with review levels, decision branches, and branch pruning."
sidebar:
  order: 2
---

Anatomy
Roles
Lifecycle
Branches

Scroll

## Structured work, attached to an item

A workflow is an ordered set of steps attached to an
[item](https://docs.assureswarm.com/concepts/items-and-item-types/), with a name, a status, typically
`DRAFT` → `ACTIVE` → `COMPLETED`, and one or more owners. As work
proceeds, AssureSwarm tracks which step is current.

It's created one of two ways, mutually exclusive: from a reusable
**[workflow template](https://docs.assureswarm.com/admin/workflow-templates/)**, or as a **custom
workflow** drawn directly as diagram nodes and edges. Once running, both
behave the same.

## Approvers and review levels: no "assignee"

A step has no single owner field. Work reaches people two ways:
**approvers**, who sign off on the step itself, and **form assignments**,
who answer the step's [form](https://docs.assureswarm.com/concepts/forms/): either, both, or neither.

Every approver has a **review level** for display ordering. Approvers can
act in any order; the step defines how many approvals it requires. Use
dependencies between separate steps when reviews must happen in sequence.

## Status is derived, never set

A step's status comes from its approvals: `PENDING` (none yet),
`IN_PROGRESS` (some, not enough), `COMPLETED` (required approvals met).
Nobody sets it directly.

The workflow's own status is separate: it can sit at `ACTIVE` for the
whole run while steps individually cycle through their lifecycle.

## Decisions route the run: pruning trims it

A diagram can include decision points. Each outgoing branch is labeled
with the "when" value that selects it; whichever outcome comes back is the
branch the run follows.

Optionally, the branches not taken can be **pruned**: explicitly and
permanently removed from that run. The underlying template is untouched.
Agents can propose it too, through
[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/).

## Anatomy of a step, in detail

Each step carries:

| Part                       | What it holds                                                      |
| -------------------------- | ------------------------------------------------------------------ |
| Name, description, summary | What the step is and why it exists.                                |
| Type                       | A plain task, by default.                                          |
| Instructions               | Guidance for whoever does the work.                                |
| Due date                   | Optional.                                                          |
| Result                     | A free-form, Markdown write-up of what the work produced.          |
| Form                       | Optional structured questions: see [Forms](https://docs.assureswarm.com/concepts/forms/).      |
| Documents                  | Files attached to the step: see [Documents](https://docs.assureswarm.com/concepts/documents/). |
| Item links                 | Connections to related items beyond the workflow's own.            |

The result is usually where the substance lives, findings, a write-up, a
summary of what was checked, captured as Markdown so it renders cleanly
wherever the step is viewed, in-app or through
[get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/).

Steps can also link directly to items beyond the workflow's own item, as a
parent, child, sibling, or related record, to tie the work to whatever it
actually touches.

## Assignment, in detail

:::note\[There is no "assignee" field]
Don't assume a step has an assignee: agents and integrations frequently do,
and it's wrong. Approvers act on the step with its full context; form
assignments are narrower by design, and, for
[external respondents](https://docs.assureswarm.com/concepts/forms/) especially, may not see anything
else about the step or workflow.
:::

An approval records the approver and timestamp. **Approve** records sign-off;
**Remove Approval** withdraws it. To request changes, leave the step unapproved
and explain the corrections to the preparer. Accepting an agent's result
suggestion updates the result separately from this native sign-off.

:::note\[A review dependency]
A subject-matter reviewer checks the work in one step. A manager authorizes its
outcome in a second step connected to the first. That edge expresses the
dependency. Giving two approvers different review levels on one step only
changes their display order.
:::

:::caution\[Pruning is permanent]
Pruning removes the not-taken steps from that workflow run for good. It does
not affect the underlying workflow template: only the run it was applied to.
:::

And when an agent works it

## For agents

Every proposed change covered on this page, including `prune-branch`,
goes through [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/) as a
[suggestion](https://docs.assureswarm.com/concepts/suggestions/): the agent proposes, a person decides.
[get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/) surfaces the steps
awaiting *your* approval and your pending form assignments;
[get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/) returns one step in full.
Workflow-level aggregates, `workflowStats` and `dueDateReport`, are
available through [GraphQL](https://docs.assureswarm.com/graphql/).
