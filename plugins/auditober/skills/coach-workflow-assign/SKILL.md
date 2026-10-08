---
name: coach-workflow-assign
description: "Use whenever the user asks to assign, schedule, set deadlines, or pick approvers for the steps of a workflow. Sets approvers and due dates on a workflow instance via suggest_change against the step target — walking the steps, resolving users by name or email to user ids, and submitting one update suggestion per step that sets the approvers array and dueDate field."
uxContract: 1
hostContract: 1
---

# Coach Workflow Assign

Bulk-assign approvers and due dates across a workflow's steps. One suggestion per step (the platform requires update-by-step for these fields). Designed for the typical assign-them-all-at-once flow.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
For interactive suggestion output, report pending work and [Review and approve](<previewUrl>); approval and read-back establish change. Headless returns keep the real previewUrl in their structured outcome.
Read ../../references/task-routing.md to distinguish the requested operation.
Parse supplied values first; ask only unresolved necessary inputs with a suitable question UI or plain text.
Verify the connected tenant/user and exact required MCP tools before acting; missing capabilities remain a structured handoff.
You are the workflow-assign skill. The user wants to set approvers
and/or due dates on the steps of a workflow instance. Your job is to walk
the workflow's steps, gather the approver and due-date inputs, resolve
user names or emails to user ids, and emit ONE suggest_change call per
step that updates the approvers and dueDate fields.

The correct shape per step is exactly:

  suggest_change({
    action: "update",
    itemType: "step",
    targetId: "<stepId>",
    data: {
      fields: {
        approvers: [
          { userId: "<id>", reviewLevel: 1 }
        ],
        dueDate: "<ISO 8601 datetime>"
      }
    },
    reason: "<one short sentence on what is being assigned>"
  })

approvers is a JSON array. Each element is { userId, reviewLevel }. The
reviewLevel controls display order (1, 2, 3, ...); approvals may occur
in any order. For required sequential review, use distinct workflow
checkpoints with dependency edges. The total number of entries determines `requiredApprovals` on
the step.

dueDate is ISO 8601 datetime (e.g., 2026-06-15T17:00:00Z). DATE-only
strings are rejected — always include time + timezone.

Read ../../references/query-patterns.md before any complete collection read.
Normal step pages use first:25; rich export and sweep pages use first:5.
Collect nodes by id and follow pageInfo until hasNextPage is false, preserving
the full selection. Missing/repeating endCursor, GraphQL errors, truncation
and unresolved predecessors mean an incomplete read. Stop before execution,
assignment or claiming a complete export. Offset lists use skip/take with
unchanged filters, advance by returned rows, and stop at a short page or the
API's verified total. Never infer absence from one page.

Procedure:

  1. Resolve the workflow. If --workflow-id was passed, use it. If
     --workflow-name, page allWorkflows(skip: 0, take: 25)
     { id name itemId itemType } and match names after complete discovery. If neither, ask via
     the available question surface using get_current_context's currentView.workflowId or
     the user's assigned workflows.

  2. Fetch the workflow's steps. Use query_data:
     `{ workflow(id: "<id>") { steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status
     approvedCount requiredApprovals } } } }`. Complete every cursor page, then walk the id-deduplicated roster; skip
     steps already in COMPLETED.

  3. Gather assignments. Two modes:
     a) Bulk same-assignee + same-due-date. The user names one person
        and one date that apply to every step. Confirm with
        the available question surface before fanning out.
     b) Per-step. The user wants different people or dates per step.
        Use supplied per-step values first and ask only missing assignments. For dates,
        if the user supplies a single "due by" date, schedule each step
        evenly between today and that date. Otherwise ask per step.

  4. Resolve user names to ids. For each name/email, call query_data:
     `{ users(searchQuery: "<name>", skip: 0, take: 25) { id name email } }`. On ambiguity
     (multiple matches), the available question surface to pick. On no match, surface
     the typo or invite the user to add the person via the admin UI.

  5. Emit one suggest_change per step. Fanning out across many steps in
     one batch is fine — the user approves them all on the suggestions
     dashboard.

  6. After the last suggest_change, hand off with a one-line summary
     covering how many assignment proposals were drafted, the action link to the
     workflow page (which surfaces the suggestions).

Follow the host contract for visible responses and headless returns. Return actual
proposal/artifact links and unresolved blockers accurately; no completion prompt.

```

## Inputs

- `--workflow-id <id>` or `--workflow-name <text>` — the workflow
  instance. If absent, use `get_current_context`'s currentView.
- `--assignee <name|email>` — optional, the assignee for all steps.
- `--due-by <ISO 8601>` — optional, the final due date. If set without
  per-step dates, steps are spread evenly.
- `--per-step <json>` — optional, an array of { stepName, assignee,
  dueDate } for explicit per-step control.

## Procedure

1. Resolve the workflow. Use the id if provided; otherwise query_data or
   `get_current_context`. If still ambiguous, the available question surface.
2. Fetch every steps page via `query_data`, following pageInfo as above.
   Skip COMPLETED only after collecting the full roster.
3. Infer the supplied mode from --per-step or an explicit --assignee scope. Ask for bulk versus per-step only when that necessary scope is unresolved.
4. Gather assignments. Resolve every named user to a user id via
   `query_data` + `users(searchQuery: ...)`.
5. For each step, emit:

       suggest_change({
         action: "update",
         itemType: "step",
         targetId: "<stepId>",
         data: {
           fields: {
             approvers: [{ userId: "<uid>", reviewLevel: 1 }],
             dueDate: "<iso8601>"
           }
         },
         reason: "<short why>"
       })

6. Hand off with the batch summary + action link to the workflow page +
   accurate proposal states.

## Notes

- One assignment per call, sequenced. The platform does not have a
  bulk-assign endpoint; this skill emits one `suggest_change` per step.
  When the user approves them on the suggestions dashboard, each step's
  approvers and dueDate are set independently. If the user only wants to
  approve some, that's fine — partial application is allowed.
- Multi-approver steps. To require multiple sign-offs, pass an array
  with multiple `{ userId, reviewLevel }` entries. reviewLevel is
  a display ordinal: 1, 2, 3. Approvals may occur in any order;
  use dependent checkpoints when one review must precede another.
- Date format strictness. The platform requires ISO 8601 datetime with
  a timezone offset (Z or +HH:mm). Plain `2026-06-15` is rejected.
  Construct dates carefully — when the user says "next Friday at 5pm",
  resolve to a concrete ISO datetime and confirm via the available question surface
  before submitting.
- Date spreading. If the user gives a single `--due-by` and N steps,
  spread the dates as `today + (i / N) * (due-by - today)`. Show the
  computed schedule in a details block before submitting.
- Steps already COMPLETED. Skip them. The platform will reject an
  update on a COMPLETED step's approvers (the approval history is
  immutable). The skill should not even try.
- User search precision. `users(searchQuery)` hits names and emails.
  When two users share a first name (Alice Smith and Alice Jones), the
  query returns both. the available question surface to pick — don't guess.
