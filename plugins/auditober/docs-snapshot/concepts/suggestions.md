---
title: Suggestions
description: "The human-review layer for agent writes: how a proposed change is created, reviewed, applied, and audited."
sidebar:
  order: 6
---

Lifecycle
Actors
Targets
Trail

Scroll

A suggestion is this product's answer to the question "what happens when an
agent wants to change something". The answer is: it asks. Everything below
follows from that one decision.

## A successful call creates a proposal, not a change

Agents, and the in-app AI, write through
[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/), and a successful call does exactly
one thing: it creates a suggestion in `pending`. Nothing in your tenant is
different after that call returns.

From `pending` a person's decision sends it to `processing` while the write
is applied, then `approved`, or straight to `rejected` with nothing applied.
If applying it stalls partway, it falls back to `pending` rather than
half-applying: the apply is built never to run twice.

## Three parties, and the middle one is a person

The agent proposes and records its name, its type, and the reason for the
change. The reviewer decides, seeing the target, the values before, the
values proposed, and that stated reason. The system applies.

A reviewer has three moves, not two: approve, reject, or edit the proposal
and then approve what they actually want written. The write runs **as the
approver**, under the approver's own
[permissions](https://docs.assureswarm.com/concepts/permissions/), so a suggestion cannot be used to
push a change past what its reviewer could have made by hand.

## What a proposal can point at

A suggestion targets one thing: an [item](https://docs.assureswarm.com/concepts/items-and-item-types/)
of any type your tenant has configured, or a step, a
[workflow](https://docs.assureswarm.com/concepts/workflows/), a workflow template, a
[dashboard](https://docs.assureswarm.com/concepts/dashboards/), a time entry, a relationship or link, or
a form assignment. Each target allows its own set of operations.

Tenant configuration is deliberately absent from that list. No agent creates
a user, grants a page, or reshapes an item type, whatever it proposes.

## Every outcome leaves a trail

An approved suggestion lands in the activity trail like any other change,
naming who processed it and when, beside the edits people made by hand.
Nothing an agent does is invisible after the fact.

Above the individual entries sit the aggregates: suggestion volume, approval
rate, and a per-agent breakdown. An agent proposing more than expected, or
getting rejected more often than it should, shows up there first.

## What a suggestion contains

A suggestion records everything a reviewer needs to judge it without digging
elsewhere:

| It records          | As                                                                                                               |
| ------------------- | ---------------------------------------------------------------------------------------------------------------- |
| Operation           | `create`, `update`, `delete`, `submit_form`, or `prune-branch`                                                   |
| Target              | An item of some type, or a step, workflow, workflow template, time entry, relationship, link, or form assignment |
| Proposed data       | What the agent wants the target to look like                                                                     |
| Before state        | For updates, what the target looked like beforehand, so the reviewer sees exactly what would change              |
| Reason              | The agent's stated justification                                                                                 |
| Agent name and type | Who, or what, proposed it                                                                                        |
| Page context        | Where in the product it was proposed from                                                                        |

:::note\[What review looks like]
An agent proposes raising an item's priority from "medium" to "high", with a
one-line reason. The suggestion shows the reviewer the item, the before value,
the proposed value, and the reason. The reviewer approves, and the change is
applied as if the reviewer had made it themselves.
:::

## Lifecycle

| Status       | Meaning                                       |
| ------------ | --------------------------------------------- |
| `pending`    | Waiting for review. Nothing has been applied. |
| `processing` | Approved, and being applied.                  |
| `approved`   | Applied successfully.                         |
| `rejected`   | Declined, and nothing was applied.            |

:::note\[A suggestion is not a change]
Nothing in your tenant is different after `suggest_change` returns. The record,
step, or workflow it targeted stays exactly as it was until someone reviews and
approves it.
:::

## Reviewing and approving

Suggestions surface in the Activity Hub, the review rail down the left of the
app, and as preview banners on the pages they would affect. Every
`suggest_change` response also includes a direct **Preview & approve** link the
agent can hand to a person, which lands on that same preview.

Either way the reviewer sees the before and after values and the agent's reason
before deciding. When you are the reviewer:

1. Check the target is the right one.
2. Check the **before** state still matches reality.
3. Check the change is within what was actually asked for.
4. Check the option values and field keys look sensible.
5. Reject with confidence if any of that is off.

:::tip\[When in doubt, reject]
Rejecting costs the agent nothing: it can re-propose with a correction.
Approving something wrong is harder to undo.
:::

[Reviewing suggestions](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/) is the
full walkthrough, including bulk review and reading a diff.

## Auditability and monitoring

Every suggestion's outcome lands in the activity trail, and the aggregate
numbers, suggestion volume, approval rate, and per-agent breakdowns, are
queryable through `suggestionStats` in [GraphQL](https://docs.assureswarm.com/graphql/). Administrators see
the same tenant-level activity in the [activity log](https://docs.assureswarm.com/admin/activity-log/).

That breakdown is worth reading periodically. An agent proposing more than
expected, or getting rejected more often than it should, is a signal to
investigate before it erodes trust in the whole pattern.

And on the agent's side of the gate

## For agents

[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/) is the only write path, and it takes
an action, a target type, an optional target id, the proposed `data`, and a
`reason`. It returns the created suggestion and a **Preview & approve** link
to hand to a person, never an applied change, so an agent should report what
it proposed rather than claim the change is done. Call
[get\_schema](https://docs.assureswarm.com/mcp/get_schema/) first when proposing item data, so field keys
and option values match the tenant's actual model.
