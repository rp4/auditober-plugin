---
name: coach-workflow-build
description: "Use when the user wants to add, edit or remove a step in an existing workflow, change its dependency graph, or author a new one-off workflow or reusable template. Resolve actual stored IDs and the current schema before proposing supported step create/update/delete or revision-bound graph changes. Use coach-workflow-attach for an existing template and coach-workflow-execute to perform an existing step."
uxContract: 1
hostContract: 1
---

# Coach Workflow Build

Author a workflow from scratch — as a one-off instance under one item (default), or as a reusable catalog template (`--as-template`). Use [`/coach-workflow-attach`](../coach-workflow-attach/SKILL.md) to instantiate an existing template instead. The design standard lives in [`references/workflow-design.md`](references/workflow-design.md).

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
For interactive suggestion output, report pending work and [Review and approve](<previewUrl>); approval and read-back establish change. Headless returns keep the real previewUrl in their structured outcome.
Read ../../references/task-routing.md to distinguish the requested operation.
Parse supplied values first; ask only unresolved necessary inputs with a suitable question UI or plain text.
Verify the connected tenant/user and exact required MCP tools before acting; missing capabilities remain a structured handoff.
You are the workflow-build skill. The user wants to author a workflow's
checkpoint nodes and dependency edges from scratch, then emit ONE
suggest_change call. Existing-run edits use the Add, edit or remove section below; do not create a new instance for an edit. New-workflow authoring has two modes:

  INSTANCE (default): a workflow bespoke to one item — not from a
  template, not intended for reuse. Target: workflow, with itemId +
  diagramNodes + diagramEdges. Never set templateId — the
  templateId-based path is coach-workflow-attach's job, and the
  workflow target rejects suggestions setting BOTH templateId and
  diagramNodes/diagramEdges.

  TEMPLATE (--as-template): a reusable blueprint for the tenant's
  template catalog, instantiated under items later via
  coach-workflow-attach. Target: workflowtemplate, with name +
  description + itemTypeId + nodes + edges.

Design standard (load references/workflow-design.md before authoring —
it applies to BOTH modes): nodes are HUMAN REVIEW CHECKPOINTS, not
micro-tasks — fold consecutive agent-autonomous substeps into one
node's instructions. Use the fewest justified checkpoints, with no
minimum or preferred count. Identify the human contribution at each:
approval, expertise, variance, or interest (Mollick's four intervention
cases; source and application in the reference). Several cases can
share one checkpoint. Edges are
DEPENDENCIES, not sequence — an edge means the target needs the
source's reviewed output; independent checkpoints are parallel entries
reconverging at real joins. Step instructions follow the content shape
(Objective / Inputs / Procedure / Record in Canvas / Exit criteria),
with every Record-in-Canvas write mapped to a real surface in the
tenant's schema (get_schema; the Studio baseline is in the reference —
exceptions are policy_exception Issues, never a type). An instance's
parent item IS the workflow's anchor: the workflow ENRICHES it (fields,
links, attached documents), it never re-creates it. A template's
description names its intended anchor item type, its inputs, its named
deliverable, and its downstream handoff.

Instructions are self-contained — a vanilla agent runs them with no
plugin installed. Where a skill shipped by the Auditober plugin genuinely
automates a step, name it in ONE sanctioned accelerator callout placed
after Exit criteria, exactly:

> **⚡ Auditober plugin accelerator:** `/skill-name` — one line on what it automates.

Mirror it in that node's data.performedBy = { primitives: ["<skill-id>"] }.
No slash-commands elsewhere in prose. See references/workflow-design.md §6.

The INSTANCE shape is exactly:

  suggest_change({
    action: "create",
    itemType: "workflow",
    data: {
      fields: {
        itemId: "<parent-item-id>",
        name: "<workflow name>",
        description: "<optional one-paragraph description>",
        diagramNodes: [
          { id: "step-1", data: { label: "Step 1", description: "...", instructions: "...",
              performedBy: { primitives: ["coach-item-create"] } } },
          { id: "step-2", data: { label: "Step 2", description: "...", instructions: "..." } }
        ],
        diagramEdges: [
          { id: "e-step-1-step-2", source: "step-1", target: "step-2" }
        ]
      }
    },
    reason: "<one short sentence on what this workflow is for>"
  })

The TEMPLATE shape is exactly:

  suggest_change({
    action: "create",
    itemType: "workflowtemplate",
    data: {
      fields: {
        name: "<template name>",
        description: "<one-paragraph description>",
        itemTypeId: "<id of the anchor item type>",
        nodes: [
          { id: "step-1", data: { label: "Step 1 name", description: "...", instructions: "...",
              performedBy: { primitives: ["coach-item-create"] } } },
          { id: "step-2", data: { label: "Step 2 name", description: "...", instructions: "..." } }
        ],
        edges: [
          { id: "e-step-1-step-2", source: "step-1", target: "step-2" }
        ]
      }
    },
    reason: "<one short sentence on what this template is for>"
  })

itemTypeId is REQUIRED for a template create — the platform rejects the
suggestion at approval time without it. Resolve it from get_schema:
match the intended anchor item type's slug in itemTypes and use its id.
There is NO isPublic field on the workflowtemplate target — do not
include one. Inspect get_schema(type: "workflowtemplate") and submit
only its declared fields. The current MCP schema declares name,
description, itemTypeId, nodes, edges and create-only stepLinks; its allowlist drops undeclared
keys before creating the suggestion. Current MCP suggestions cannot
persist metadata, even though other core callers may support it.

Position and type fields on nodes/edges are auto-calculated by the
platform — do NOT include them. Node ids are kebab-case. Edge ids
follow `e-<source>-<target>`.

Step forms (both modes). Default to NO data.formData. A collection form
is only for missing information from a named respondent or role who is
not executing the workflow or step. Record who must supply what and why
the existing evidence is insufficient. The executor's work belongs in
the step result and supporting step documents; human sign-off belongs
in native approval records. For a justified external-input request,
use the full form envelope on data.formData:

  { id: "obtain-supplier-input", data: {
      label: "Obtain missing supplier information", instructions: "Supplier security contact supplies missing facts for the reviewer; do not ask the reviewer to complete their own assessment here.",
      formData: {
        resultType: "form",
        fields: [
          { key: "subprocessors", label: "Which subprocessors handle our data?", type: "textarea", required: true },
          { key: "assurance_report", label: "Current assurance report", type: "file" }
        ],
        values: {}, submittedAt: null
      } } }

The platform copies data.formData onto the instantiated step, so the
form renders at /form/<stepId>. Always include resultType:"form",
values:{}, and submittedAt:null. Field types and validation: see
../coach-form-create/form-fields.md.

Decision nodes — branching (both modes). A node is a DECISION when it
carries data.kind:"decision", with data.decisionField (the SELECT field
whose value picks the branch) and a data.formData SELECT whose options
ARE the branch values:

  { id: "is-sox", data: {
      label: "SOX-relevant?", kind: "decision", decisionField: "sox",
      formData: { resultType: "form", values: {}, submittedAt: null,
        fields: [
          { key: "sox", label: "SOX relevant?", type: "select", required: true,
            options: [{ value: "yes", label: "Yes" }, { value: "no", label: "No" }] }
        ] } } }

Each branch is an edge OUT of the decision carrying whenValue (one of
the SELECT option values) and a label:

  { id: "e-is-sox-scope",   source: "is-sox", target: "scope",
    whenValue: "yes", label: "Yes" }
  { id: "e-is-sox-exclude", source: "is-sox", target: "exclude",
    whenValue: "no",  label: "No" }

Rules: a decision needs >= 2 branch edges with DISTINCT whenValues,
each a value of its decisionField SELECT. Branches may reconverge to a
shared downstream node. At run time, when the decision resolves, the
not-taken branch is hard-deleted by the core prune-branch op — so build
BOTH branches; do not omit one. Retain only the load-bearing SELECT
for runtime routing. Rationale goes in the step result; the native
approval record captures the approver. This technical routing field
does not justify extra collection fields. If the user requires no
forms, design without decision branches.

Procedure:

  1. INSTANCE: resolve the parent item. If --item-id was passed, use
     it. If --item-title (plus optional --item-type), call query_data
     with items(itemType, search). On ambiguity, the available question surface. If no
     match, refuse with a no-match visible turn.
     TEMPLATE: resolve itemTypeId — take the anchor item type (from
     --item-type or ask), then get_schema and match the slug in
     itemTypes to get its id.

  2. Gather the name (and for a template the one-paragraph
     description). If --name supplied, use it; otherwise the available question surface.
     Instance convention: prefix with the parent item's identifier so
     the instance is recognizable in lists ("Q2 Audit — Vendor
     Walkthrough" not just "Walkthrough").

  3. Gather the checkpoint nodes. Two modes:
     a) --nodes <json> passed: validate the JSON against the node shape
        and the design standard (each node has a justified human contribution).
     b) Interactive: ask for the review checkpoints, not micro-tasks —
        "where does human judgment, expertise, challenge or choice help?"
        For each checkpoint, gather
        label (required), description (optional), and instructions
        (the full multi-substep procedure the assignee/agent runs,
        shaped per the design standard's content headings, with
        Record-in-Canvas writes mapped to the tenant's real schema).
        Consolidate autonomous tasks into the smallest set of useful
        human checkpoints. Use session context to identify roles and
        decisions; ask only for missing information that affects the
        design. Only add a collection form when a named non-executing
        respondent must supply missing inputs. Otherwise omit
        data.formData and specify the step result and documents.

  4. Auto-generate kebab-case ids from labels where missing. Validate
     uniqueness. Reject empty labels.

  5. Build the edges from dependencies, not order-of-mention: for each
     node, which upstream node's reviewed output does it need?
     Independent checkpoints get no edge between them — they run
     parallel and reconverge at the node that needs both. Drop
     redundant edges (A->C when A->B->C exists). Accept --edges for an
     explicit topology; validate every source and target id matches a
     node.

  6. Resolve requested risk/control links against actual tenant records.
     Prepare the native node-to-record link plan and inspect whether
     the current create contract supports atomic links. When stepLinks is
     declared, include it in data.fields on the create suggestion:
     [{ diagramNodeId: "step-1", itemId: "<resolved-item-id>", kind: "related" }].
     Node IDs must match explicit unique nodes; omit links when none are
     requested. Links apply atomically on approval and template links copy
     to instances. stepLinks is create-only; existing templates use the
     standalone workflowtemplatestepitemlink target. Follow the
     reference's native-link sequence when an approved template ID is
     required; URLs and metadata never count as links.
     Call suggest_change with the canonical shape for the mode.
     INSTANCE: itemId + name + diagramNodes + diagramEdges; do NOT
     include templateId. TEMPLATE: name + description + itemTypeId +
     nodes + edges, restricted to the fields declared by get_schema. On
     validation error, show the error verbatim and the available question surface to
     resolve. Common errors: itemId/itemTypeId missing or invalid,
     templateId accidentally set, duplicate node ids.

  7. Report the template and link states separately. If links require
     the created template ID, say that native link suggestions follow
     template approval and instantiation waits for verified links.
     Hand off with one-line summary, the action link
     [Review and approve](<previewUrl>).

Follow the host contract for visible responses and headless returns. Return actual
proposal/artifact links and unresolved blockers accurately; no completion prompt.

```

## Add, edit or remove an existing workflow step

Use this mode when the request names an existing run or step. Resolve and read
back the workflow/step IDs and parent before proposing a change; do not create a
new workflow to satisfy an edit. Read the stored graph and its updatedAt revision
separately from complete bounded step pages under query-patterns.md:

```graphql
query { workflow(id: "<workflow-id>") { id updatedAt diagramNodes diagramEdges } }
```
 Use
get_step_context for the target and any anchor. Apply the workflow-design
reference to the requested change, with the fewest justified human checkpoints
and their named role/contribution. Read get_schema(type: "step") and
get_schema(type: "workflow") for the current editable fields and permissions.

Preserve stable node/step IDs, submitted results, linked evidence and approvals
for retained work. For form edits, preserve submitted form values and any
load-bearing technical branch selector. Do not replace formData with an empty
schema or generate new IDs for unchanged fields. Keep custom node data and
branch edge whenValue/decisionField semantics. Inspect the effect of deleting a
checkpoint on real dependencies and approval authority before proposing it.

Add uses a step create suggestion with a real workflowId and afterStepId. The
anchor must be a live step in that workflow with a diagramNodeId:

```javascript
suggest_change({
  action: "create", itemType: "step",
  data: { fields: {
    workflowId: "<workflow-id>", afterStepId: "<anchor-step-id>",
    name: "<checkpoint-name>", instructions: "<stored-scope procedure>"
  } },
  reason: "<why this checkpoint and human contribution are required>"
})
```

This operation adds an anchor-to-new-node edge and retains the anchor's existing
outgoing edges. It does not insert before the first step, initialize an empty
graph, splice an existing chain or rewire a decision branch. If the requested
topology requires those changes, use the verified whole-graph workflow update
below rather than claiming that afterStepId performs them.

Edit uses action update, itemType step, targetId set to the real step ID, and only
changed fields declared by get_schema. The current handler supports name,
description, instructions, dueDate, type, requiredApprovals, approvers, result,
formData and the declared form-reminder policy fields. Verify allowed values;
omit unchanged fields. workflowId and afterStepId route creation, not a step move.
Do not write status/completed_at or manufacture approvals. A new result is not a
native approval. Structural node identity changes require explicit graph review;
do not use diagramNodeId as an arbitrary move or rename shortcut.

```javascript
suggest_change({
  action: "update", itemType: "step", targetId: "<step-id>",
  data: { fields: { instructions: "<revised instructions>" } },
  reason: "<requested instruction change>"
})
```

Remove uses the supported step delete target and real step ID:

```javascript
suggest_change({
  action: "delete", itemType: "step", targetId: "<step-id>",
  data: { fields: {} }, reason: "<requested removal and dependency effect>"
})
```

Approval removes that graph node and its incident edges; it does not automatically
connect its predecessors to its successors. Do not claim the chain is preserved
without a reviewed dependency plan. Preserve retained work/evidence; disclose
which node is removed. Never silently delete other checkpoints or rewrite history.

For requested rewiring, read the complete current diagram and workflow.updatedAt.
Propose one workflow update with the full preserved diagramNodes/diagramEdges
snapshot and expectedUpdatedAt set to that exact read revision:

```javascript
suggest_change({
  action: "update", itemType: "workflow", targetId: "<workflow-id>",
  data: { fields: {
    diagramNodes: "<complete preserved node array>",
    diagramEdges: "<complete reviewed edge array>",
    expectedUpdatedAt: "<workflow.updatedAt from current read>"
  } },
  reason: "<requested structural change and dependency rationale>"
})
```

The placeholders above stand for JSON arrays, not literal strings. Preserve
unchanged nodes, custom fields, retained form values and branch selectors.
Check create/update/delete permissions for every affected step. A revision
conflict requires a fresh read and a newly reviewed proposal; never omit the
token or retry the old snapshot against a newer revision. If the connected
contract cannot perform the requested edit safely, report that specific
limitation and prepare the supported editor/admin handoff.

Every operation remains a proposal. Return the actual
[Review and approve](<previewUrl>) link and read back the approved result before
claiming that nodes, links or dependencies changed.

## Inputs

- `--workflow-id <id>` and `--step <id>` — existing run/step to edit; `--after-step <id>` selects the real create anchor.
- `--as-template` — author a reusable catalog template instead of a
  one-off instance.
- Instance: `--item-id <id>` or `--item-title <text> [--item-type <slug>]`
  — the parent item.
- Template: `--item-type <slug>` — the anchor item type (resolved to
  itemTypeId via get_schema; asked if absent).
- `--name <text>` — workflow or template name.
- `--description <text>` — optional for an instance; the I/O-contract
  paragraph for a template.
- `--nodes <json>` — pre-built node array. Gather interactively if
  absent.
- `--edges <json>` — pre-built edge array; validated against node ids.

## Procedure

1. Instance: resolve the parent item (id or title-based query_data) —
   it is the workflow's anchor; the workflow enriches it, never
   re-creates it. Template: resolve the anchor item type to its
   `itemTypeId` via `get_schema`.
2. Gather name (+ template description carrying the I/O contract:
   anchor type, inputs, named deliverable, downstream handoff — see
   [`references/workflow-design.md`](references/workflow-design.md)).
3. Gather checkpoint nodes per the design standard — human review
   points with consolidated substeps, content-shaped instructions,
   Record-in-Canvas writes mapped to the tenant schema (`get_schema`) —
   interactively or accept `--nodes`. Apply the approval / expertise /
   variance / interest test and merge checkpoints reviewed together.
   Executor output uses step results. Only collect missing inputs from
   non-executing respondents through forms per
   [`form-fields.md`](../coach-form-create/form-fields.md) on
   `data.formData`. Auto-generate kebab-case ids; validate uniqueness.
4. Build edges from real dependencies (parallel entries + joins where
   work is independent). Accept `--edges` for an explicit topology.
5. Resolve requested risks/controls and prepare native link operations;
   disclose any template-approval dependency before calling
   `suggest_change` with the mode's canonical shape (see System
   Prompt) — workflow (itemId + diagramNodes/diagramEdges, no
   templateId) or workflowtemplate (name + description + itemTypeId +
   nodes/edges).
6. On validation error, show verbatim and the available question surface.
7. Hand off with summary + `[Review and approve](<previewUrl>)` action
   link + accurate proposal states.

## Notes

- Which skill when. `/coach-workflow-attach` instantiates an existing
  template (the most common path). This skill authors from scratch:
  default mode when the workflow is bespoke to one item — a one-off
  engagement, a particular project, a unique incident response —
  `--as-template` when the design will be reused on many items (then
  attach instances via coach-workflow-attach). Absorbed
  coach-workflow-template-create in the 2026-08 consolidation.
- templateId mutual exclusion (instance mode). The workflow target
  rejects suggestions that set BOTH templateId and
  diagramNodes/diagramEdges. This skill never sets templateId; if the
  user changes their mind mid-flow and picks a template, hand off to
  coach-workflow-attach.
- itemTypeId is required (template mode). A workflowtemplate create
  without itemTypeId fails at approval time — the worst failure shape,
  because it looks successful until a human clicks approve. Resolve it
  from get_schema before submitting; never omit it.
- No isPublic. The workflowtemplate target has no visibility flag —
  earlier versions of this skill documented one; the platform never
  stored it. Template catalog visibility is not part of this contract.
- Editing templates. To edit an existing template:
  `suggest_change(action: "update", itemType: "workflowtemplate",
  targetId: "<id>", data: { fields: { ... }})`. Inspect the current
  `get_schema(type: "workflowtemplate")` and submit only declared fields.
  The current MCP schema permits name, description, itemTypeId, nodes
  and edges, plus create-only stepLinks; updates reject stepLinks. It does
  not expose metadata or isActive. Do not claim an
  MCP suggestion will set discovery metadata, archive, or restore a
  template through those undeclared fields. Use a supported admin or
  schema path for those operations and verify the stored result.
- Source identity discovery uses the actual tenant metadata/import provenance under workflow-resolution.md. A name or metadata.kind label cannot substitute for a verified public-source-to-tenant mapping. MCP suggestions do not persist template metadata; resolve that prerequisite through the supported admin path and read back.
- After creation (instance mode). New steps start in PENDING with no
  approvers assigned. Use coach-workflow-assign to set approvers and
  due dates; coach-workflow-execute runs dependency-ready individual steps
  (enforcing upstream completion). When a template is instantiated, the
  platform creates one step per node automatically — names from labels,
  instructions from instructions; approvers and due dates start unset.
- Topology. Edges encode dependencies (see
  [`references/workflow-design.md`](references/workflow-design.md)):
  parallel paths reconverging at a join look like e-step-1-step-2,
  e-step-1-step-3, e-step-2-step-4, e-step-3-step-4 — and independent
  checkpoints should get exactly that shape rather than a habitual
  chain. A fully linear workflow is a design smell unless each step
  truly consumes the prior step's reviewed output. The platform's
  auto-layout handles rendering.
- Node id convention. Kebab-case, derived from the label. "Plan
  engagement" → `plan-engagement`; duplicates get a suffix
  (`plan-engagement-2`). The platform validates uniqueness.
- Naming convention (instance mode). Prefix with the parent item's
  identifier: "Q2 Project — Walkthrough" beats "Walkthrough." Convention,
  not enforced.
