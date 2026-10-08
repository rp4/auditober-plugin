---
title: Workflow Templates
description: "Govern the template library: what a blueprint contains, how approvals and branches are designed, and why editing one never disturbs a running workflow."
sidebar:
  order: 4
---

Library
Blueprint
Steps
Publish

Scroll

[Using templates](https://docs.assureswarm.com/using-coworkcanvas/using-templates/) is the mechanics of the
editor. This page is the governance: what belongs in a template, how approvals and
branches should be designed, and what a change costs once people are running work
from it.

## The library you are governing

Templates live on the **Templates** page in the top navigation. That
page grant allows access to the library, while each template's required
anchor item type determines its visibility.

Managing a template requires `edit_all` on its anchor item type or
administrator status. The Templates page grant alone does not authorize
creation, editing, or deletion. Configure both in
[User Permissions](https://docs.assureswarm.com/admin/users-and-access/).

## A blueprint, not a running workflow

The designer is a canvas of step nodes and the connections between them, so a
template is a graph rather than a list and can branch. Starting work from it
creates a separate, running [workflow](https://docs.assureswarm.com/using-coworkcanvas/running-workflows/)
on an item, and from that moment the two are independent.

This is the property that makes templates safe to improve. A later edit
reaches only workflows started afterwards, work already in flight is
undisturbed, and someone reshaping their own running workflow never touches
your blueprint.

## Write steps for the person who has to do them

Selecting a node opens its configuration: the step name, a description, the
instructions, and an optional form. Name the action rather than the position,
so "Review vendor contract" and not "Step 3", and write instructions for
someone meeting the process for the first time.

Use the fewest checkpoints that preserve a real human contribution:
approval, expertise, variance (choosing between alternatives), or interest
(a decision people want to own). Name the role and its contribution, and
keep autonomous work inside the checkpoint's instructions.

Put executor work in the result, evidence in documents, and sign-off in
native approvals. Add a collection form only for missing input from a
named person or role outside the workflow's execution. Preserve the select
field needed for an existing technical branch selector.

## The name is what everyone else sees

The name and description at the top of the designer are the whole of what a
colleague reads in the library before choosing this template, so make them say
what the process is for and when to use it. **Save Changes** writes the entire
blueprint at once: nodes, connections, and every step's configuration.

Review a template against this page before others start work from it. Correcting a
template is cheap; correcting the twenty workflows somebody started from a
confusing one is not.

## Approvals and review levels

A step's status is derived from its approvals and never set by hand: `PENDING`
with none recorded, `IN_PROGRESS` with some but fewer than required, `COMPLETED`
once the required approvals are in.

When you design a step, set how many approvals it requires, who the approvers are,
and each approver's **review level**. Review level controls display order;
approvers can approve in any order. Put a subject-matter check and a subsequent
authorization in separate steps with a dependency when order is required.

Choose required-approval counts deliberately. Too low and the step is a formality
that adds process without adding scrutiny; too high and it becomes a bottleneck
nobody can clear, especially when one of the required approvers is often
unavailable.

## Decision branches

A step can branch into more than one outgoing path. Label each branch with the
outcome value that selects it, and keep those values short and unambiguous:
`approved` and `rejected` read better than anything longer or more interpretive.
Two branches with overlapping or vague outcome values make the decision ambiguous
at exactly the moment it matters.

Decide per template whether the branch not taken should be pruned once the
decision resolves, and write your convention into the template description. Anyone
reading the template later should learn the behavior there rather than the first
time a workflow runs.

:::caution\[Pruning is permanent]
Pruning removes the not-taken steps from that specific running workflow for good.
It does not touch the template, so the next workflow started from it still carries
the full branch, but for the run it was applied to the branch is gone.
:::

## Visibility and lifecycle

Every template requires an anchor item type. It inherits visibility from
that type's permissions; there is no Public/private template flag. Choose an
anchor the intended users can access, and restrict authoring through its
`edit_all` permission.

The **Active** setting controls whether new workflows can start from the
template. Deactivate a retired template to stop new runs; existing runs remain
independent and continue. Moving a template to another item type or deactivating
it also clears its automatic-creation selection. Configure automatic workflows
on the [item type](https://docs.assureswarm.com/admin/item-types-and-fields/#automatic-workflows).

Every one of these changes is recorded in the
[activity log](https://docs.assureswarm.com/admin/activity-log/) as a `workflow-template` entry.

## Where templates come from

1. **Built in-app**, step by step. The most control, and the natural choice for a
   process specific to your organization.
2. **Proposed by an agent.** An agent can draft a template with
   [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/). It arrives marked **AI Suggestion**,
   opened in the designer rather than a read-only preview, so you can move nodes,
   rewrite instructions, and fix names before pressing **Approve & Create** or
   **Reject**.
3. **Adapted from an open-source template.** The
   [open-source workflow library](https://assureswarm.com/workflows/) publishes
   ready-made templates you can bring in and adjust.

However a template arrives, review it against this page before people start work from it.
Treat a proposed template as a first draft: correcting a drafted process is
usually faster than drawing one from scratch, but the structure is still yours to
sign off on.

And when an agent drafts one

## For agents

An agent proposes a template through [suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/)
against the workflow-template target, which supports create, update, and
delete, and gets back a **Preview & approve** link to hand to a person.
Nothing exists until someone approves it, and the approval runs under that
person's [permissions](https://docs.assureswarm.com/concepts/permissions/).
[get\_schema](https://docs.assureswarm.com/mcp/get_schema/) comes first: every template must be anchored
to an item type through `itemTypeId`. Use names and fields the tenant has.
The MCP template target exposes name, description, itemTypeId, nodes,
edges, and optional create-only `stepLinks`. Include native links to known
items in that create suggestion so one approval creates the template and
its links atomically. For an existing template, use
`workflowtemplatestepitemlink`, then verify links through
`workflowTemplateStepItemLinks`. Stored links copy to new workflows.
The MCP target does not expose automatic-creation settings or metadata.
