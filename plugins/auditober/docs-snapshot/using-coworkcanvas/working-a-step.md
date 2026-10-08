---
title: Working a Step
description: "Complete workflow steps: instructions, results, forms, documents, approvals and review levels, and decision outcomes."
sidebar:
  order: 3
---

Find
Work
Review
Approve
Evidence

Scroll

## Find your work

Steps waiting on you show up in a few places: the workflow view on the item
the step belongs to, dashboards that track due or overdue work, and your own
approval and form queues.

There's no single "assignee": you're involved either as an **approver**
(you sign off on the step) or a **form respondent** (you answer a form
attached to it). See [Workflows](https://docs.assureswarm.com/concepts/workflows/) for how steps,
approvals, and forms fit together.

## Do the work

Open the workflow and select the step. Read its description and
instructions, and check the due date. Then produce the outcome: depending
on how the step is set up, that means writing a **result** (Markdown is
supported), completing the step's [form](https://docs.assureswarm.com/concepts/forms/), attaching
**documents**, or a combination of these.

## Approvals and review levels

Approvers sign off on a step. Review levels order the displayed approver
list; approvers can act in any order. A step's
status is derived from its approvals: `PENDING` (none yet),
`IN_PROGRESS` (some but not all), `COMPLETED` (all required approvals met).

The approval control is for listed approvers. An earlier review level
does not block your approval. If a review must precede another, define
separate steps connected by a dependency.

## Approve, or request corrections

When the work is ready, press **Approve**. The step footer also offers
**Remove Approval** to withdraw your approval. To request corrections,
leave the step unapproved and tell the preparer what needs to change in
the result or through your team's communication channel. Some steps are decision points: the
outcome you record selects which branch the workflow continues on, and
steps on a branch that wasn't taken may be pruned from that run.

## Documents on steps

Attach evidence, files or links, where a step asks for it. Uploads
validate before they count toward the step; if an upload is rejected,
re-upload it rather than assuming it went through. See
[Documents](https://docs.assureswarm.com/concepts/documents/) for more.

And when an agent works it

## For agents

Agents see the steps awaiting your approval and the forms assigned to you
through [get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/), and can pull a single
step in full through [get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/). From there, an
agent can draft a result, propose form answers, or upload a document you've
given it: everything lands as a
[suggestion](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/) for you to review,
except a document upload you directly asked the agent to make. Accepting
a result suggestion saves the result; it does not record a native step
approval. Review the saved work, then use **Approve** on the step. Check
its status before treating it as completed.
