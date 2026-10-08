# Workflow design standard — checkpoints, honest edges, real storage

Owned by `/coach-workflow-build` (one-off instances and `--as-template`
catalog templates); `/coach-workflow-attach` applies it when enriching.
Apply this whenever authoring nodes and edges; it is what separates a
workflow agents can run — and humans can govern — from a checklist.

## 1. Nodes are human review checkpoints

A node exists where a **human contribution changes the work or authorizes
its outcome**. Name the judgment, knowledge, challenge or meaningful choice
needed there. Consecutive agent-autonomous sub-tasks a human would only review
together collapse into ONE node, their procedures folded into that node's
`instructions` as numbered substeps. Instructions stay thorough for agents;
humans are spared approving every small step.

- Use the fewest checkpoints that preserve the human contributions and real
  dependencies. There is no minimum or preferred step count. Two checkpoints
  can be a complete workflow; four intervention cases do not require four steps.
- Gather human contributions and dependencies before decomposing agent work.
  Put the autonomous work supporting each contribution in that node's procedure.
- A decision the runtime takes (branch selection) is always its own node.

For each proposed node, identify the person or role, the reviewed deliverable,
and the contribution that warrants their involvement. Apply Ethan Mollick's
four intervention cases from [Agency and Agents](https://www.oneusefulthing.org/p/agency-and-agents)
(August 31, 2026): **approval**, **expertise**, **variance**, and **interest**
(his fourth case is "because something is interesting"). These are situations
for seeking human help, not a fixed sequence. Our workflow application is:

| Case | What the human contributes |
|---|---|
| Approval | An authorized decision about commitments, exceptions or risk. |
| Expertise | Context or specialist judgment that could change the conclusion. |
| Variance | A challenge to assumptions or an alternative the agent may miss. |
| Interest | A meaningful choice the person wants to make and learn from. |

Merge adjacent checkpoints when the same people can review the same package
and make those contributions together. Preserve separate gates when different
authority, independent review, or a real dependency requires them. Retrieval,
comparison, drafting, filing, scheduling and confirmation-only work normally
belong in a substantive checkpoint's procedure. Do not add an opening scope
confirmation or a closing bookkeeping step without a specific human decision.

### Forms collect someone else's input

A data-collection form is only for missing information supplied by someone
who is not executing the workflow or step. Name that respondent or role, the
missing information, and how their response will be used before adding a form.
Being an outside vendor alone does not justify a questionnaire when the needed
information is already available. Never invent a respondent to justify a form.
Identifying a respondent or approving a form schema does not authorize sending
messages or invitations. Prepare the request and use existing session authority;
obtain authorization before sending when the user has not authorized outreach.

The executor's analysis, evidence summary, assessment and conclusion belong in
the **step result**, with source files as step documents and durable facts in
the appropriate item fields. Human sign-off uses the step's native review and
approval records. Do not duplicate results or approvals in self-addressed forms.
Omit `data.formData` entirely on ordinary review steps.

The existing runtime uses a form SELECT as its branch selector. For a genuinely
branching decision, retain only the SELECT named by `decisionField`; it is a
technical routing field. Put rationale in the step result and approver identity
in the native approval record. Do not add branching merely to justify a form.
If the user requires no forms at all, use a design without decision branches.

## 2. Edges are dependencies, not sequence

An edge `P → N` means **N needs P's reviewed output to start**. Build the
edge list from real dependencies, never by chaining steps in the order they
were mentioned:

- For each node, name the upstream output it consumes; add only those edges.
- Nodes with no in-workflow predecessor are parallel entries — expected and
  good. Independent streams reconverge at the node that genuinely needs all
  of them (a join: multiple incoming edges, waits for all).
- Drop redundant edges (if A→B→C exists, no A→C).
- Genuinely sequential chains stay sequential — never fabricate parallelism
  across a real dependency.
- Decision branches carry `whenValue` + `label` and reconverge downstream;
  build every branch (the platform prunes the not-taken one at run time).

## 3. Step instructions — the content shape

Task nodes: `**Objective**` — one sentence on the checkpoint's outcome;
`**Inputs**` — what it consumes AND where each lives (see §5);
`**Procedure**` — numbered, concrete substeps an agent can execute
unassisted; `**Record in Canvas**` — the writes, per §5's surfaces;
`**Exit criteria**` — what the human reviewer checks before sign-off.
Decision nodes: `**Objective**` / `**Decision criteria**` (one bullet per
branch value, stating when it applies) / `**Record in Canvas**` /
`**Exit criteria**`. Self-contained — no references to external documents
the reader can't reach from the workflow.
See §6 for the one sanctioned way to name a plugin skill in instructions (the accelerator callout) and the machine-readable `performedBy` block.

## 4. The I/O contract (name it in the description)

The workflow's `description` states, in one or two sentences:
- **Anchor** — what the workflow runs on. A build (`/coach-workflow-build`)
  attaches to a concrete parent item — pick the type deliberately (an
  engagement phase runs on the existing Audit item and ENRICHES it; a
  recurring ops/compliance cycle runs on an Audit item created per cycle;
  a register lifecycle runs on the register's own item). A template names
  its intended anchor type so instantiators attach it to the right thing.
- **Inputs** — what must already exist when it starts. The subject that
  already exists is an INPUT: never author a step that "creates" the
  anchor (enrich, don't seed; a recurring rollover creates only the NEXT
  period's record).
- **Named deliverable(s)** — call outputs by their recognized domain name
  (the Risk & Control Matrix (RCM), the planning memo, the attestation
  package), not "the outputs".
- **Handoff** — the downstream workflow or owner that consumes the result,
  if one exists.

## 5. Record in Canvas — map every write to a real surface

First read the known type's current typed schema under
[schema discovery](../../../references/schema-discovery.md). These 11 Studio
types describe the baseline; customized tenant fields/options remain authoritative.

| Type (slug) | Role | Example fields to verify live |
|---|---|---|
| Audit (`audit`) | engagements and assessment cycles | `audit_type`, `scope`, `lead_auditor`, `fiscal_year`, `report_date` |
| Risk (`risk`) | risk register | `likelihood`, `impact`, `inherent_rating`, `residual_rating`, `treatment`, `risk_owner` |
| Control (`control`) | controls and SOX testing host | `control_id`, `framework`, `control_class`, `itgc_domain`, `sox_applicable`, `frequency` |
| Issue (`issue`) | findings and exceptions | `severity`, `issue_type`, `sox_deficiency`, `recommendation`, `management_response`, `issue_owner` |
| Remediation (`remediation`) | linked corrective actions | `plan`, `action_owner`, `target_date`, `completed_date`, `verified_date`, `evidence` |
| Process (`process`) | auditable processes | `process_type`, `process_owner`, `in_scope`, `scope_rationale` |
| Policy (`policy`) | policy library | `policy_type`, `policy_owner`, `framework`, `version`, `next_review_date` |
| System (`system`) | systems and vendor records | `vendor`, `category`, `tier`, `business_owner`, `next_reassessment_date` |
| FSLI (`fsli`) | financial statement line items | `statement`, `balance`, `significant`, `assertions`, `assessed_fy` |
| Requirement (`requirement`) | requirements and applicability | `reference`, `framework`, `applicability`, `implementation_status`, `evidence` |
| Personnel (`personnel`) | people and responsibilities | `personnel_key`, `full_name`, `user_account`, `responsibilities`, `source_evidence` |

Vendor is `system.vendor = true`, not a `vendor` item type in this baseline.
Preserve the audit slug regardless of its role-specific display label.

Every Record-in-Canvas bullet maps to exactly one surface:
- **Item create** — type + the fields set (via `/coach-item-create`)
- **Item field update** — `Type.field` keys verbatim (`/coach-item-update`)
- **Item relationship** — which two items link (`/coach-items-link`)
- **Step result** — the executor's findings, evidence references and conclusion;
  inspect the current step schema for the supported result representation
- **Step form** — a named non-executing respondent's requested inputs, or the
  minimal runtime branch selector described in §1
- **Step document** — the file + format attached to THIS step
  (`/coach-document-upload`)
- **Workflow instance** — the run itself as the audit trail

For SOX, set literal `Control.sox_applicable = true`, host the qualifying
`metadata.kind = "audit-testing"` workflow directly on that Control, and keep the
cycle at `Workflow.customFields.sox.fiscalYear`. The Test step owns period/kind
and published results; do not create a separate testing item.
The metadata prerequisite must already exist through a supported admin or
schema path and be verified on the stored template. The current MCP
`workflowtemplate` field allowlist does not persist metadata; a template
suggestion containing that undeclared field does not establish the marker.

Rules that keep it honest:
- Never invent a field. If the tenant schema has no home for something
  (KRIs, feed configs, rosters), attach a document to the step and say so.
- **Exceptions/waivers/risk acceptances are Issues, never a type**:
  `issue_type: policy_exception`, `exception_approver` (granting authority),
  `exception_expiry_date` (the filterable expiry index) — linked to the
  Policy and/or Risk, with `treatment: accept` set on an accepted Risk.
  SOX test exceptions use `issue_type: exception`.
- Findings/gaps/actions are Issues with the right `issue_type`
  (`deficiency` / `observation` / `finding`), `source`, owner, and dates.
- Policies and their review cycles live on Policy items; vendors and their
  reassessment cadence on Vendor items — not in loose documents, when the
  tenant has those types.

### Native risk and control links

When the user requests linked risks or controls, resolve the actual tenant
records and record the purpose and applicability of each association. URLs in
instructions and IDs in metadata are references; they do not create native
links or prove that a control operated.

Inspect `get_schema(type: "workflowtemplatestepitemlink")` before proposing
template links. The supported relationship target creates a link using
`templateId`, `diagramNodeId`, `itemId` and `kind: "related"`. These native
template-step links are copied to instances. Do not invent node fields such
as `linkedItems` or assume an ignored field will establish a relationship.

For a new template or instance, inspect the current create contract. The
current workflow and workflowtemplate schemas expose create-only stepLinks
in data.fields: [{ diagramNodeId, itemId, kind: "related" }]. Resolve real
tenant item IDs and match explicit unique graph node IDs; include requested
links in the create suggestion so they apply atomically on approval. Template
links copy to instances. Existing templates use standalone link suggestions;
updates reject stepLinks. Verify stored links after acceptance.

If the connected tenant does not expose stepLinks and cannot create
links atomically, prepare an exact node-to-record link plan alongside the
template suggestion and disclose the dependency in the review handoff. After
the user approves the template, resolve its real ID, propose the native links,
and verify them with `workflowTemplateStepItemLinks` after approval. Do not
instantiate a template with requested links until those links are verified.
Distinguish **planned**, **pending approval**, and **verified linked** in status
reports. Never approve your own suggestions.

## 6. Automation — accelerator callouts and `performedBy`

Instructions are **self-contained**: a vanilla agent operating AssureSwarm with no
plugin installed can execute them. The ONLY place a `/slash-command` may appear in
instruction prose is one **sanctioned accelerator callout**, placed after
`**Exit criteria**`, at most one per step, and only where a named Auditober plugin skill
genuinely automates that step's work:

> **⚡ Auditober plugin accelerator:** `/skill-name` — one line on what it automates.

A slash-command anywhere else in prose makes the workflow plugin-dependent — don't.
Most steps get no accelerator; never decorate, never name a skill that merely *could*
be adjacent.

When a step is automated, also set the machine-readable `data.performedBy` on the node:

    data.performedBy = { primitives: ["<skill-id>"], agent: "<agent-id>", note: "..." }

- `primitives` — the Auditober plugin skill id(s) that run the step. **Any skill named in
  an accelerator callout MUST appear here.**
- `agent` — a single domain agent id where domain judgment is delegated (optional).
- `note` — a short free-text clarification (optional).

Sparse by design — set `performedBy` only where the mapping is unambiguous; most nodes
carry nothing. Heuristic: uploads → `coach-document-upload`; record create →
`coach-item-create`; linking → `coach-items-link`; queries → `coach-query-data`;
notifications → `coach-notify`; monitoring/cadence → `coach-workflow-scan`; domain
judgment → `agent: "<domain>-artist"` with a note.
