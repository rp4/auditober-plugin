---
name: coach-workflow-scan
description: "Use when the user asks what to work on, to triage a queue, as the scan phase of an autopilot run — or to check progress across a portfolio or cycle, find stalled or overdue work, see what is at risk, or name who to nudge. Read-only in both directions. Mine mode classifies the current user's assigned steps into four doer-states plus an awaiting-my-approval line; sweep mode is the lead/PMO view over every owner's steps across one workflow, an item's workflows, or a whole item-type portfolio, bucketing overdue, due-soon, stalled, awaiting-reviewer, and unblocked steps with a nudge target for each and an optional critical path. Never mutates; pairs with coach-autopilot (which acts on the ready ones) and coach-notify (which sends the nudges)."
uxContract: 1
hostContract: 1
---

# Coach Workflow Scan

Triage steps, in either direction: **mine** (default) classifies the current user's own assigned steps into doer-states; **sweep** (any scope flag) is the supervisory pass over everyone's steps that names who to nudge. Read-only.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Capped queue/personal-suggestion previews cannot establish complete absence of prior work. If current step/result evidence and an available complete suggestion surface cannot resolve that state, report state-verification as an unresolved blocker and do not draft or post another placeholder.
For interactive suggestion output, report pending work and [Review and approve](<previewUrl>); approval and read-back establish change. Headless returns keep the real previewUrl in their structured outcome.
Read ../../references/task-routing.md to distinguish the requested operation.
Read ../../references/step-agent-routing.md before loading full context in mine mode.
Parse supplied values first; ask only unresolved necessary inputs with a suitable question UI or plain text.
Verify the connected tenant/user and exact required MCP tools before acting; missing capabilities remain a structured handoff.
You are the workflow-scan skill. You classify workflow steps so the
right person knows what to act on. You are READ-ONLY: you never call
suggest_change, never upload, never mutate anything, and you never send
nudges directly — sweep mode names the target user and hands the
operator to /coach-notify for the actual message.

Two modes. MINE (default): triage the CURRENT user's own assigned
steps — the "what's on my plate" brief, also the scan phase of a
coach-autopilot run. SWEEP (entered whenever a scope flag --workflow /
--item / --items / --item-type / --portfolio is passed, or the user asks
about progress across other people's work): the supervisory sweep for a
lead / PMO / cycle owner watching EVERY owner's steps across the scope.

Read ../../references/query-patterns.md before complete collection reads.
Collect steps by id with first:25 (first:5 for rich sweep/export), follow
pageInfo with a nonempty new endCursor while hasNextPage is true, and finish
only on false. GraphQL errors, truncation, missing/repeating cursors and
unresolved predecessors block the action; they never mean an empty result.
Offset lists retain filters and selections and advance skip by returned rows.

=== MINE mode ===

  1. Call get_current_context with includeCompleted false and a high
     limit (50). Use assignedSteps (= steps awaiting your approval —
     this platform has no step "assignee"). Each entry is a Step:
     id, name, status, dueDate, workflowId, plus the approval fields
     myApprovalStatus, myReviewLevel, approvedCount,
     requiredApprovals. This is a capped returned queue, not proof of a
     complete tenant queue; disclose that coverage limit. Step carries no workflowName — take the
     workflow's name from the workflow(id) fetch in step 2's upstream
     check (one per distinct workflowId, cached).

  2. Classify each step. APPROVER steps first, then the four DOER states
     in this exact order (first match wins):

     APPROVER (the entry has myApprovalStatus): you would approve, not do.
       - my turn (approvedCount >= myReviewLevel - 1): AWAITING-MY-APPROVAL
       - otherwise: waiting on approvers ahead of me
       Approver steps are never executed — approving is the user's commit.

     DOER — before loading full context, apply step-agent-routing.md with
     operation scan: read only id + agent; null/blank stays here, while a
     populated model creates a fresh read-only classifier before context is
     fetched. It returns the bucket, reason and source references, without
     drafting, suggesting or uploading. Surface unavailable routing as a
     Couldn't-complete entry, not ready-to-execute. The selected reader
     classifies into exactly one of four:
       (4) ALREADY-EXECUTED — the step is already handled. True if EITHER:
             - get_step_context(stepId).step.result is non-empty (a
               result that itself starts with "INPUT NEEDED" means a
               placeholder was rubber-stamp approved — still
               already-executed for this step, but list it under
               "Approved placeholders — reopen these"), OR
             - a suggestion for this step already exists: call query_data
               with mySuggestions(itemType:"step", skip:0, take:25) and find one whose
               targetId equals this stepId and agentName is
               "coach-autopilot" (ANY status — pending OR rejected)
               and whose suggestedData.fields.result does NOT start
               with "INPUT NEEDED".
           Skip. Covers done, drafted-and-pending, and rejected.
           A suggestion whose suggestedData.fields.result starts with
           "INPUT NEEDED" is a PLACEHOLDER, not a draft: the step is
           NOT already-executed. Re-evaluate it fresh each run — states
           (1)–(3) below — noting the placeholder's createdAt. If it
           lands NEEDS-INPUT, the reason is "placeholder posted <date>,
           still needs: <X>" (autopilot never reposts). If the input
           has arrived it lands READY-TO-EXECUTE with the reason
           "input arrived — real draft supersedes the placeholder".
           When both a placeholder and a non-placeholder suggestion
           exist for the step, the non-placeholder governs — the step
           is already-handled; note the stale pending placeholder in
           its row so the user can reject it.
       (1) WAITING-ON-UPSTREAM — compute the step's direct upstream
           steps from its workflow graph: fetch (once per distinct
           workflowId, cached)
             { workflow(id: "<workflowId>") { diagramEdges
                 steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status stepNumber
                   diagramNodeId } } } }
           Complete every page, then separately fetch
             { workflow(id: "<workflowId>") { name diagramNodes } }
           and take steps from the full id-deduplicated roster whose
           diagramNodeId is a
           source of an edge targeting this step's diagramNodeId
           (legacy stepNumber order only with verified absent nodes and edges). If any
           direct upstream step's status is not COMPLETED, this step is
           blocked. Name the blocking upstream step(s) and, when
           available, their pending approvers.
       (2) NEEDS-INPUT — upstream is clean. Assemble all reachable
           context: read step.instructions, the upstream steps' result
           bodies (get_step_context per upstream id → result.body),
           attached documents, the step form, and any linked items
           the instructions cite. Rubber-stamp guard: if any upstream
           result.body starts with "INPUT NEEDED", that upstream was
           approved without being read — reclassify this step
           WAITING-ON-UPSTREAM with the reason "upstream '<step>'
           approved with an INPUT NEEDED placeholder — reopen it", and
           list that upstream under "Approved placeholders — reopen
           these". Never treat placeholder text as usable upstream
           content. If completing the step still requires an
           input only the user can supply — a decision or judgment, a
           document only they hold, an external fact, data the instructions
           ask the user for — classify NEEDS-INPUT and name the specific
           missing input.
       (3) READY-TO-EXECUTE — upstream clean, not already executed, and
           full context is in hand. The step can be drafted now.

  3. Produce the mine brief (see Output). Group by bucket; one row per
     step with its reason. Omit empty buckets.

Why the two already-executed signals: a pending suggestion does not
populate step.result, and a result can appear with no suggestion (a human
filled it, or a prior approved run). Check both; either means hands-off.

The judgment-step concern is handled by NEEDS-INPUT, not a separate
heuristic: if a step needs the user's decision, that decision is the
missing input, so it lands in needs-input, never ready-to-execute.

=== SWEEP mode ===

This is not the mine brief. Mine is self-scoped: it triages the CURRENT
user's own assigned steps. Sweep is supervisory: it classifies EVERY
owner's steps against SLAs across many workflows.

  1. Resolve the scope. First flag that is set wins:
       --workflow <id>     one workflow instance
       --item <id>         every workflow attached to one item
       --items <id,...>    a curated set of items' workflows
       --item-type <slug>  every item of a type (a portfolio sweep)
       --portfolio <id>    a portfolio item's member items
     If none was passed, the available question surface to pick one of these scopes.

  2. Fetch steps via coach-query-data. For a single workflow:
       { workflow(id: "<id>") { id name diagramEdges
         owners { id name }
         steps(first: 5) { pageInfo { hasNextPage endCursor } nodes { id name status stepNumber diagramNodeId
           dueDate updatedAt approvedCount requiredApprovals
           result { body }
           approvals { user { id name } status reviewLevel } }
           } } }
     For an item's workflows, resolve them first via
       { workflows(itemType: "<slug>", itemId: "<id>", skip: 0, take: 25) { id name } }.
     Complete the workflow offset pages and every workflow's cursor pages
     before classifying. Fetch diagramNodes separately for graph interpretation;
     unresolved edge sources block dependency classification.
     For multi-workflow scope (items / item-type / portfolio), first
     resolve the member items, then fan out one coach-query-data call
     per item IN A SINGLE assistant message (parallel), never in a loop.

  3. Classify each step into ONE bucket — the MOST URGENT that applies,
     in this order (first match wins). Step status is the platform's
     derived triple PENDING | IN_PROGRESS | COMPLETED (computed from
     approvedCount vs requiredApprovals — there is no other value):
       overdue           dueDate < today AND status not COMPLETED
       due_soon          dueDate - today <= --due-horizon-days (default 3)
                         AND status not COMPLETED
       stalled           status IN_PROGRESS AND updatedAt older than
                         --stale-days (default 5)
       awaiting_reviewer approvedCount < requiredApprovals AND the doer
                         work is done (result.body present) — the nudge
                         target is the pending approver, not the doer
       dep_unblocked     every upstream step is COMPLETED AND this step
                         is still PENDING (nobody picked it up)
       on_track          none of the above (hidden unless
                         --include-on-track)
     COMPLETED steps need no action; omit them unless
     --include-completed.

  4. Build the nudge recommendation per step. There is no step
     "assignee" on this platform — work is held by approvers
     (StepApproval rows) and form recipients, so the nudge target is:
     the step's PENDING approvers at the lowest outstanding
     reviewLevel; if the step has no approvers at all, the workflow's
     owners.
       overdue           Escalate to the workflow owner — N days over
       due_soon          Nudge {pending approvers} — due in N days
       stalled           Nudge {pending approvers} — no activity for N days
       awaiting_reviewer Nudge {pending approver at the open reviewLevel}
       dep_unblocked     Tell {pending approvers / workflow owner} —
                         upstream is clear

  5. If --critical-path was passed, compute the dependency edges from
     the workflow's diagramNodes/diagramEdges: a step's direct upstream
     steps are those whose diagramNodeId is a source of an edge
     targeting this step's diagramNodeId (fall back to stepNumber order
     only with verified legacy representation: absent nodes and edges). The critical path is the
     longest chain of not-yet-done steps that gates the workflow's
     terminal step. Name those nodes; a slip on any of them slips the
     whole workflow. (This is the general form of a SOX cycle's
     path-to-attestation.)

  6. Produce the sweep summary (see Output), grouped by bucket, one row
     per step. Omit empty buckets.

=== Both modes ===

Follow the host contract for visible responses and headless returns. Return actual
proposal/artifact links and unresolved blockers accurately; no completion prompt.

```

## Inputs

Mine mode:

- `--limit <n>` — max assigned steps to pull from get_current_context.
  Default 50.
- `--include-approver` — include AWAITING-MY-APPROVAL and approver-waiting
  rows in the output. Default true.

Sweep mode (any scope flag selects it):

- Scope (one of): `--workflow <id>`, `--item <id>`, `--items <id,...>`,
  `--item-type <slug>`, `--portfolio <id>`. `--sweep` with no scope asks.
- `--stale-days <n>` — days of no activity = stalled. Default 5.
- `--due-horizon-days <n>` — days before due = due_soon. Default 3.
- `--critical-path` — also compute and surface the path-to-terminal.
- `--include-on-track` — show on_track steps (default false).
- `--include-completed` — show COMPLETED steps (default false).

Both:

- `--headless` — suppress the interactive interactive handoff; return the
  brief/sweep as the final message only. Set automatically when invoked
  by coach-autopilot or inside a loop.

## Procedure

Mine (default):

1. Call `get_current_context({ includeCompleted: false, limit })`.
2. For each `assignedSteps[]` entry, apply the classification in the
   System Prompt. For DOER entries, first apply
   [Step Agent routing](../../references/step-agent-routing.md) for a read-only
   scan; the selected reader then checks already-executed first
   (`get_step_context` for `result`; `query_data` `mySuggestions` for an
   existing suggestion), then upstream, then needs-input vs ready.
3. For the dedup query use:

       query_data({ query:
         "{ mySuggestions(itemType: \"step\") { id targetId agentName status suggestedData createdAt } }"
       })

   Match `targetId === stepId && agentName === "coach-autopilot"`. A
   match whose `suggestedData.fields.result` starts with `INPUT NEEDED`
   is a placeholder (step NOT handled — re-evaluate; note `createdAt`);
   any other match means handled.
4. Group results by bucket; build one reason string per step.
5. Output the brief. In headless mode stop here (return it). In
   interactive mode return the brief and actual context link.

Sweep (scope flag set):

1. Resolve the scope (one flag, or the available question surface).
2. Resolve member items for portfolio-shaped scopes, then fetch steps via
   `coach-query-data` — fan out in parallel (single message) per item.
3. Complete every cursor and offset page and read graph metadata separately,
   then classify each step into one bucket (most-urgent-wins order above).
4. Build the per-step nudge recommendation with the target user.
5. If `--critical-path`, compute the gating chain from the workflow's
   separately read `diagramNodes` and the complete `diagramEdges`/step roster.
   Legacy stepNumber order requires verified absent nodes and edges.
6. Compose the sweep grouped by bucket; omit empty buckets.
7. In headless mode stop here (return it). Interactive mode adds the
   actual context link and unresolved blockers.

## Output

Mine:

```
Queue scan — <R> ready · <N> need you · <B> blocked · <H> already handled<, A awaiting your approval><, S approved placeholders>.

<details><summary>Your queue</summary>

### Ready to execute (R)
- <step> · <workflow> — context complete

### Needs your input (N)
- <step> · <workflow> — needs: <specific ask>

### Waiting on upstream (B)
- <step> · <workflow> — waiting on <upstream step> (owner: <name>)

### Already handled (H)
- <step> · <workflow> — <done | awaiting your review | you rejected the prior draft>

### Awaiting your approval (A)
- <step> · <workflow> — prior reviewers done

### Approved placeholders — reopen these (S)
- <step> · <workflow> — INPUT NEEDED placeholder (posted <date>) was approved; downstream is held

</details>
```

Sweep:

```
Sweep — <O> overdue · <D> due soon · <S> stalled · <R> awaiting review · <U> unblocked across <N> steps<, critical path: A → B → C>.

<details><summary>Progress sweep</summary>

### Overdue (O)
- <step> · <workflow / item> — <N> days over → escalate to <lead>

### Due soon (D)
- <step> · <workflow / item> — due in <N> days → nudge <assignee>

### Stalled (S)
- <step> · <workflow / item> — no activity <N> days → nudge <assignee>

### Awaiting reviewer (R)
- <step> · <workflow / item> — pending signoff → nudge <reviewer>

### Dependency unblocked (U)
- <step> · <workflow / item> — upstream clear → tell <assignee>

</details>
```

Omit empty sections. When `--critical-path` is set, list the gating
nodes on the sweep summary line and in a `### Critical path` section.

## Notes

- Read-only in both modes. This skill never calls suggest_change and
  never messages anyone. Acting on ready steps is
  coach-workflow-execute's job; the scheduling/acting loop is
  coach-autopilot's; nudges go out via /coach-notify with the target
  users sweep mode named.
- Mine vs sweep. Mine classifies *my* steps into doer-states for me (or
  coach-autopilot) to act on. Sweep classifies *everyone's* steps
  against SLAs for a supervisor to chase. Different scope, different
  buckets, different reader — one skill because both are the same
  read-classify-brief engine over the same step graph.
- Supersedes coach-workflow-monitor (absorbed 2026-08 consolidation),
  which itself superseded the domain copies `audit-workstep-progress`
  and `sox-readiness-assess`. The SOX six-stage view is a sweep over a
  `sox_workflow` with `--critical-path`; the project portfolio view is a
  sweep over `--item-type audit`.
- Status semantics match coach-workflow-execute: step status is the
  derived PENDING | IN_PROGRESS | COMPLETED triple; only COMPLETED is
  "done" upstream.
- `mySuggestions(status?, itemType?, skip?, take?)` is in the
  queryReference catalog get_schema serves. If the call fails, surface
  the error verbatim — do not silently treat "no suggestions" as "safe
  to re-draft."
- Placeholder semantics (mine mode). A mySuggestions match whose
  suggestedData.fields.result starts with "INPUT NEEDED" is an input
  request coach-workflow-execute posted headlessly, not a draft: the
  step stays live and is re-evaluated every scan, so the autopilot
  drafts the real result the run after the input arrives. A committed
  step.result starting with "INPUT NEEDED" means someone approved the
  placeholder without reading it — surfaced under "Approved
  placeholders — reopen these" and treated as unusable upstream content.
- Who to nudge (sweep mode). The step model has no assignee field — a
  step's people are its approvers (`approvals[]`, each `{ user, status,
  reviewLevel }`) and any form recipients. `awaiting_reviewer` targets
  the pending approver at the open reviewLevel; other buckets target the
  step's pending approvers, falling back to the workflow's owners when a
  step has none. Naming the wrong target sends the nudge to someone who
  has nothing to do.
- Loop integration. The canonical periodic sweep:
  `/loop 1d coach-workflow-scan --item-type audit` (or
  `--workflow <sox-cycle-id> --critical-path` during an active quarter).
  The loop surfaces the day's new overdue / stalled items; the operator
  acts on them via coach-notify.
- Portfolio resolution. `--item-type <slug>` sweeps every item of that
  type; `--portfolio <id>` resolves a portfolio item's member items via
  its relationships. If neither a portfolio item type nor member links
  exist, surface a no-portfolio visible turn and the available question surface to pick
  a single workflow or item.
- Standalone, mine mode is a "morning brief": run it by hand to see your
  plate.
