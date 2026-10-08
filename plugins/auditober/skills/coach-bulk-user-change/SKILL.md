---
name: coach-bulk-user-change
description: "Use when the user asks to offboard an owner, reassign work across a person's records or steps, or prepare a cross-record handoff report. Resolve the live tenant schema and exact scope; propose changes through native suggestions. Reassigning one issue or item uses coach-item-update."
uxContract: 1
hostContract: 1
---

# Canvas Bulk User Change

One-shot replacement for "click into 47 items and remove this person" —
and, with `--report`, the departing-person handoff document built from
the same exhaustive assignment sweep.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

A dry run remains a dry run until submission is authorized; the native preview is still the approval boundary. Report mode requires staging/artifact output and redaction support. Missing support preserves inputs and returns awaiting_runner, without claiming a saved or cleared report.

You are the bulk-user-change skill. When a user leaves the
organization, transfers teams, goes on leave, or changes roles, you
generate the full list of Canvas items and workflow Steps where
they're assigned, and then either propose the change batch (default)
or compile the handoff document (--report).

Never apply changes directly. Every removal/reassignment is a
suggest_change payload that the admin reviews and approves in Canvas
as a single batch. Report mode is READ-ONLY — it writes one local
markdown file and never calls suggest_change.

Be exhaustive — in both modes. Missing one watchlist field or one step
approval means the departed user keeps phantom access, and a skipped
item means the covering person discovers it the hard way. Always query
every assignment surface across the shared core item types (audit,
issue, risk, control, process, policy, authority_source) and every
workflow Step attached to those items (steps hold people as approvers
and form recipients — there is no step assignee and no step watcher
list on this platform).

Follow the shared host contract for intake, tool announcements,
result links, pending states and approvals.
```

## Inputs

- `--user <user-id|email>` — required. The subject.
- `--action remove|reassign|change-role` — required unless `--report`.
- `--report` — compile the handoff document instead of proposing
  changes (read-only).
- `--reassign-to <user-id|email>` — required if action is reassign
- `--new-role <role>` — required if action is change-role
- `--scope <portfolio|all>` — default: all
- `--dry-run` — list what would change, no suggest_change calls
- Report mode only: `--coverage <user-id|email>` (who's taking over),
  `--start <YYYY-MM-DD>` / `--end <YYYY-MM-DD>` (coverage window),
  `--out <path>` (default `.coworkcanvas/handoffs/<user-slug>-<date>.md`)

## Procedure

### 1. Resolve the subject
- Query Canvas for the user record by id or email.
- Capture: user id, name, current role, current teams.
- Report mode with `--coverage`: query the covering user similarly.

### 2. Discover all assignment surfaces (both modes)
For the configured tenant, query every place a user can be assigned
across the shared core item types:

- **audit**: `lead`, `team` array, `watchlist` array
- **issue**: `owner`, `watchlist` array
- **risk**: `owner`
- **control**: `owner`
- **process**: `owner`
- **policy**: `owner`, `approver`
- **authority_source**: `owner`
- **Custom USER fields**: any field with type `USER` or `USERS`
  on any item type — query the schema for the field type and
  enumerate.

Then enumerate Step-level assignments on every Workflow attached to
the items above (the platform holds step people as approvals and form
assignments — there is no Step.assignee or step watcher list):

- **StepApproval**: the subject appears in `step.approvals[]`
  (`{ userId, status, reviewLevel }`) — any status.
- **FormAssignment**: the subject is a form recipient
  (`myFormAssignments` / `formAssignmentsByStep(stepId)`; recipient =
  `userId`).

Build a list of `{ target_type, target_id, target_title, field_name,
role }` tuples. `target_type` is either `item` or `step` so the
downstream `suggest_change` payload routes correctly.

### 3. Group and summarize (both modes)
Group by target type. Print a summary:

```
Found 47 assignments for jane.smith@company.com:
  audit                3 lead, 8 team
  issue                12 owner, 4 watchlist
  control              5 owner
  policy               2 owner, 1 approver
  step_approval        14 approver
  form_assignment      4 recipient
```

In `--report` mode, continue at step 9. Otherwise continue at step 4.

### 4. Plan the changes
For each tuple, the planned change depends on `--action`:

- **remove**: drop from arrays; null out scalar fields IF the field is
  optional. If required (e.g., `control.owner` cannot be null),
  surface as "blocker" — the admin must reassign first.
- **reassign**: replace with `--reassign-to` in arrays and scalars.
- **change-role**: update role attribute only; no assignment changes.

### 5. Surface blockers
If any required scalar field would be left null after `remove`, call
a concise question: `<N> blockers — required fields would be
left null. How to proceed?` with options
`Specify reassignment target` / `Skip blockers, apply rest` /
`Cancel batch`. Do not silently drop required-field assignments.

### 6. Build the suggest_change batch
For each planned change:
- One `suggest_change` payload per assignment: `action: "update"` with
  `itemType` set to the item's type slug (e.g. `"control"`) for
  item-level people fields, or `itemType: "step"` with the Step's id
  for approver changes (`data.fields.approvers` — the full replacement
  array of `{ userId, reviewLevel }`). Form assignments cannot be
  edited in place: propose a `formassignment` delete (targetId = the
  assignment id) and, for reassignment, a `formassignment` create with
  the replacement's email in `userEmails`.
- There is no batch parameter on suggest_change — prefix every
  payload's `reason` with the same batch tag
  (`bulk-user-change <subject> <date>: …`) so the admin can filter and
  approve the set together in Canvas.

### 7. Dry-run vs apply

For `--dry-run`: visible turn is the assignment summary plus an
a concise question: `<N> changes planned — proceed?` with
options `Submit batch` / `Refine scope` / `Cancel`. Do not call
`suggest_change` until the user picks Submit.

Otherwise: call `suggest_change` for each payload with the shared
reason batch tag. Visible turn after the batch lands:

```
Batch drafted — <N> changes across <M> surfaces for <subject>.

<details><summary>Assignments found</summary>

<the grouped table from step 3>

</details>

[Review and approve](<previewUrl>)

```

### 8. Write to audit log
Append a row to `.coworkcanvas/bulk-changes-log.md`:

```markdown
## 2026-05-12T14:33 — Bulk user change

- Subject: jane.smith@company.com (user-id: u-1234)
- Action: remove (--scope all)
- Changes proposed: 47 across 6 surfaces (4 item types + Steps + StepApprovals)
- Batch id: batch-abc123
- Executed by: <get_current_context.user>
```

Change mode ends here.

### 9. Report mode — capture state per item
For each item where the subject holds an *active* role (not historical
viewers), capture:
- Current status / phase
- Last activity timestamp
- Next-action description (read from the next incomplete Step on the
  item's attached Workflow, or latest activity, or pending approval)
- Due date / SLA breach risk (per Step due dates and per item)
- Key stakeholders (other people assigned on the item or its Steps)
- Open blockers (overdue dependencies, steps stuck awaiting an
  approver, instructions flagged `[BLOCKER]`)

### 10. Report mode — render the markdown

```markdown
# Handoff Log — <Subject Name>

Generated: <timestamp>
Coverage: <covering person, dates>

## Summary
- <N> projects (incl. <N> in execution)
- <N> issues (incl. <N> overdue)
- <N> risks owned
- <N> controls owned
- <N> processes owned
- <N> policies owned or pending approval
- <N> authority_source items tracked
- <N> open workflow Steps where the subject is an approver or form recipient

## Hot items (overdue or breaching this week)
[list, sorted by days-until-breach]

## Audits
### <audit title> (<audit_type>, role)
- Status: <status>
- Last activity: <relative>
- Next action: <next incomplete Step on attached Workflow>
- Stakeholders: <names>
- Blockers: <list, if any>
- Canvas: [link]

[repeat per item]

## Issues
[same shape, including severity and linked_controls]

## Risks
[same shape]

## Controls
[same shape, including last test Step status]

## Processes
[same shape]

## Policies
[same shape, including last_reviewed_at and pending approvals]

## Authority sources
[same shape]

## Cross-cutting (open Steps, pending approvals, FormAssignments)
[Steps where the subject is an approver or form recipient, grouped by parent item]

## What I'd do first
[Generated 3-bullet suggestion: items most likely to need attention in week 1]
```

### 11. Report mode — redact and write
Run the `/coach-redact` redaction pass with policy=warn (the handoff
is internal but covering people don't always have the same access;
redact internal-only fields just in case) before anything is written
for sharing. The gate is not optional.

Write to `--out`. Final turn:
"Handoff for <subject> compiled at <path>. <N> items across <M>
item-type domains.".

## Notes

- Idempotent, both modes. Re-running a change batch for the same
  subject after approval finds no remaining assignments and prints
  "Already clean." Re-running the report produces the same file with
  refreshed state — useful as a status check, not just a one-shot
  before departure.
- Offboarding = report + reassign. The natural full flow is `--report`
  first (so the covering person has the map), then the change batch —
  the user can request either mode independently.
- For terminations, pair with HR system data so the skill can verify
  the subject is genuinely separated (avoid accidental purges of users
  who are merely on PTO).
- The `change-role` action does not affect assignments — it just shifts
  the role label. Use `reassign` if the role change implies the user
  shouldn't own current work.
- Step-level assignments often outnumber item-level assignments. A
  user may own only a handful of items but hold approvals or form
  assignments on dozens of Steps across attached Workflows. The Step
  sweep is non-negotiable in both modes.
- The report is NOT auto-shared. The user reviews then chooses how to
  hand it off. "What I'd do first" is generated heuristically; treat
  as a starting point, not gospel.
- This is the **Canvas half** of a departure package. The vault half —
  the departing person's personal synthesis, open todos, decisions,
  and key contacts — is `/brain-handoff` in the Second Brain plugin. A
  complete handoff runs both and hands over the pair.
