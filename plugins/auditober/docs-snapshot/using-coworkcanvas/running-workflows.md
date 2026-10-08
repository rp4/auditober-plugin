---
title: Running Workflows
description: "Open a running workflow, read where it stands, work the step that is waiting, and approve it."
sidebar:
  order: 5
---

Open
Read
Step
Approve

Scroll

[Workflows](https://docs.assureswarm.com/concepts/workflows/) explains what a workflow is made of: steps,
approvers, review levels, and decision branches. This page is the day-to-day
procedure for operating one that is already running.

## Open the run

A workflow opens from the item it is attached to, or from a link on a
dashboard: there is no Workflows entry in the top navigation. It renders as
a diagram, one node per step, connected in the order the work has to happen.

Read it top to bottom. Completed steps carry a green outline and a
**Completed** label, steps not yet started read **Pending**, and the small
icons on a node show what it holds, such as a form or documents.

## See who it is waiting on

The step in progress shows an approval count in place of a status, such as
`0/1 approved`, with an avatar for each approver it still needs. That is the
whole answer to "who is on the hook right now".

A step has no assignee field. People reach a step as **approvers**, who sign
off on it, or as **form respondents**, who answer its
[form](https://docs.assureswarm.com/concepts/forms/). Review levels order the approver display;
they allow approvals in any order. Separate steps and dependency edges
express reviews that must happen in sequence.

## Open the step beside the diagram

Select a step node and the step viewer opens to its right, with the diagram
still in view. It carries the step's approvers and approval count, its
description and instructions, the step result, the step form, supporting
documents, and any linked items.

Drag the divider between the two to give either side more room, and select
another node to switch the panel to that step.
[Working a step](https://docs.assureswarm.com/using-coworkcanvas/working-a-step/) covers producing the
outcome itself.

## Approve it

When the work is in place, press **Approve** at the bottom of the step
viewer. The button appears only if you are one of the step's approvers.

Status is derived from approvals, never set by hand: `PENDING` with none in,
`IN_PROGRESS` with some but not enough, `COMPLETED` once the required
approvals are recorded. If you approved too early, **Remove Approval** takes
it back and the step reopens for editing.

## Step statuses

| Status        | What it means                                            |
| ------------- | -------------------------------------------------------- |
| `PENDING`     | No approvals recorded yet.                               |
| `IN_PROGRESS` | Some approvals are in, but fewer than the step requires. |
| `COMPLETED`   | The required approvals are in.                           |

:::note\[A completed step is locked]
Once a step reaches `COMPLETED` it stops accepting changes: no edits to the
step, no new documents, no new form assignments. Remove an approval to reopen
it, make the correction, then approve it again.
:::

## Keeping the view current

The header shows how long ago the view last refreshed and carries a **Refresh**
button. The page also refreshes itself every few seconds while you have it open,
so an approval recorded by a colleague appears without you reloading.

## Reshaping a running workflow

**Edit Mode**, in the header, turns the diagram into an editor for people who
can edit that workflow. In it you can add steps, rename them, rewire the
connections between them, and delete steps or the workflow itself. Save writes
the whole diagram at once, and leaving with unsaved changes warns you first.

Editing a running workflow changes only that run. The
[template](https://docs.assureswarm.com/using-coworkcanvas/using-templates/) it came from is untouched, and
so is every other workflow started from it.

Steps can also be decision points, where the outcome recorded on the step
selects which outgoing branch the run follows. Branches that were not taken can
be pruned from the run, permanently, without touching the template. See
[Workflows](https://docs.assureswarm.com/concepts/workflows/) for how branching and pruning work.

## When an agent proposes a workflow

An agent can propose a whole workflow. It arrives as a preview: the diagram it
would create, marked **Will be created**, with the step count and the
instruction the agent was given. Nothing exists yet, and no step is running,
until you approve it from the
[suggestion](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/).

Review the shape before you approve: the steps, their order, and where
approvals sit. A workflow is easier to correct as a proposal than as a run
already underway.

And when an agent follows the run

## For agents

[get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/) surfaces the steps awaiting
your approval, and [get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/) returns one
step in full: instructions, result, form, documents, and approvals. Writes
go through [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/), which covers step
updates, workflow creation, and `prune-branch`, and each one waits as a
[suggestion](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/) until a person
approves it. Workflow-level aggregates, `workflowStats` and
`dueDateReport`, are available through [GraphQL](https://docs.assureswarm.com/graphql/).
