# Resolve an existing workflow before proposing a run

Read this with [bounded queries](query-patterns.md) and
[host capabilities](host-capabilities.md). A public sourceTemplateId identifies
a source. It is never a tenant template ID, workflow ID or step ID.

## Parent, cycle and source

Parse supplied parent, workflow, template and cycle values first. Resolve the
parent item and its active item type through the connected tenant. Establish the
intended period/cycle from the supplied request and attributable item/run evidence.
A cycle is a decision supported by those records, not an invented GraphQL field.
If the period is unclear, ask for that missing scope before selecting a run.
A module invocation or an existing run's completion does not request a new cycle.

The generated workflow-catalog.json schemaVersion 2 distinguishes studio-seed
sources from workflow-library sources. Seed rows include anchorType,
autoCreateOnItem and historical graph evidence. Library rows retain immutable
release pins. Neither grants access, imports a template, nor authorizes replacing
a tenant graph. Audit modules use the source IDs listed below, even if a tenant
has renamed the template.

| Module | Parent and source |
|---|---|
| audit-planning | audit: coworkcanvas:template:audit-planning-scoping; fsli significance work: coworkcanvas:template:fsli-significance-assessment |
| audit-narratives | process: coworkcanvas:template:process-narrative-walkthrough |
| audit-uar | system: coworkcanvas:template:periodic-user-access-review and, when warranted, coworkcanvas:template:privileged-access-review |
| audit-itgc | control: workflow-library:itgc-change-provisioning-testing |
| audit-third-party | system: coworkcanvas:template:system-third-party-risk-review; critical-tier SOC work: coworkcanvas:template:system-soc-report-cuec-review |
| audit-sampling | audit: workflow-library:substantive-testing-data-analytics |
| audit-fraud-je | audit: workflow-library:fraud-risk-je-testing |
| audit-reporting | audit: coworkcanvas:template:audit-fieldwork-reporting; issue: coworkcanvas:template:issue-triage-disposition |
| audit-remediation | remediation: coworkcanvas:template:remediation-delivery-validation; control retest: coworkcanvas:template:control-remediation-retest-closure |
| audit-continuous | audit: workflow-library:continuous-monitoring-agent-evaluation |

## Resolve tenant template identity

Read a supplied tenant template ID directly. For a source ID, use an existing
source-to-tenant mapping only after verifying its origin, tenant_id and user_id
against the current session, rereading the template, checking active/anchor
compatibility and confirming the mapping's provenance. A stale mapping is discarded.

The template's itemTypeId must equal the resolved parent's item type ID. A null or
missing binding cannot authorize a proposal; an administrator must bind an untyped
template before use.

WorkflowTemplate exposes metadata, not a top-level sourceTemplateId. Imported
seed identity is metadata.__coworkcanvasTransfer.sourceTemplateId. Installed
library identity also has metadata.library.sourceTemplateId, aliases[].sourceTemplateId
and metadata.libraryInstallation.sourceTemplateId. A library-copy transfer ID
and copiedFrom evidence identify a distinct customized copy; present it as an
option, never silently select it over the original. Do not treat a display-name
match or a source-less metadata fragment as verified source provenance. For
source-less older templates, require a validated import/admin mapping bound to
the current tenant and record; do not guess from historical node counts.

Without a verified mapping, discover every visible compatible template with
bounded offsets. Name search is a narrowing aid; an old-name search that finds
nothing cannot establish absence of a renamed template. For example:

```graphql
query { workflowTemplates(skip: 0, take: 5, itemTypeSlug: "audit") { id name } }
query { workflowTemplate(id: "<tenant-template-id>") { id name itemTypeId isActive autoCreateOnItem metadata } }
```

Repeat the first operation with skip advanced by returned rows, preserving the
selection and filters; fetch the second separately for each discovered candidate.
Include inactive templates when resolving historical runs; only an active
compatible template may be used for a proposed new run. If multiple installed
variants match, obtain a contextual template choice: title, source/release,
customization/copy evidence and anchor. A verified explicit choice may select
one compatible variant. If none resolves, return the missing source/prerequisite
and the admin library-import preview handoff. Installation and source updates
require their existing approval/review flow and read-back; do not import here.

## Resolve runs and recheck before proposing

Page all workflows for the exact parent, with unchanged filters:

```graphql
query { workflows(itemType: "audit", itemId: "<parent-id>", skip: 0, take: 25) { id name templateId itemId itemType status createdAt updatedAt } }
```

Complete offsets before deciding. Match run.templateId to a verified tenant
template, then establish its cycle and compatibility from the stored run,
results, period evidence and graph. A missing templateId/source or unknown cycle
is unresolved evidence; do not discard it to manufacture absence. Include prior
completed and cancelled runs in discovery and preserve them as history.

Reuse a compatible run for the intended cycle, including an already completed
current-cycle run: report its completion or outstanding review; do not repeat
completed steps or propose another copy. For multiple compatible runs, ask for a
contextual choice with IDs, period, state and distinguishing evidence. Do not
delete duplicates. An explicitly new cycle requires a distinct warranted period;
preserve prior runs and first check whether that cycle already has a run.
If prior runs exist but the cycle is ambiguous or no new-cycle decision was given,
resolve that decision before proposing.

Only a complete no-match permits a create proposal. Immediately before
suggest_change, reread the template, complete the parent run pages again and
check relevant pending workflow-create suggestions for that parent/template/cycle.
A pending matching proposal returns awaiting_approval and its real review link.
A capped personal suggestion preview cannot prove that no relevant proposal
exists; resolve the pending state with the authorized requester/reviewer or a
complete available surface. If visibility or paging is incomplete, stop with
that limitation. This prevents routine reruns and auto-created runs from
generating a second suggestion, but does not claim server-side atomic uniqueness.
After approval, resolve the actual run ID and steps by reading back; a previewUrl
or pending suggestion is not a created instance.

## Execute the stored checkpoints

Read the resolved run's graph separately from its bounded step roster and
instructions. Follow query-patterns.md for first:25 dependency/status pages and
first:5 rich selections; collect all pages before mapping or claiming completeness.
Use the stored nodes, edges, instructions, dependencies, results and reviewer
assignments. Map the needed work to the checkpoint whose instructions require it.
Resolve actual step IDs from the roster or stepByDiagramNode(workflowId,
diagramNodeId) using a node ID read from that run. Verify returned membership.
Never derive a step ID from a source label, numeric position or catalog snapshot.

Older four-node Bluth and current reduced Studio graphs are compatibility
evidence. Preserve deliberate tenant changes and real authority, including
independent reviewers and native approvals. Numbered module procedures describe
automation within checkpoints, not extra nodes. Do not recreate a removed node,
merge tenant checkpoints, overwrite a custom graph or infer dependency order
from roster order. Use coach-workflow-execute with the resolved instance step ID
only when its stored dependencies and approval conditions permit execution.
Review against the stored exit criteria. When no checkpoint supports the required
procedure, explain the mismatch and obtain the engagement lead's decision.

Executor work belongs in results, evidence in documents and sign-off in native
approvals. Forms collect only genuinely missing facts from a named non-executing
respondent outside the relevant participant roster. Keep the fewest justified
human interventions and identify their role and approval, expertise, variance
or interest contribution. A compatibility snapshot cannot authorize graph edits.

## Executable decision recipe

This recipe consumes normalized, cited observations after real bounded reads.
Its cycle and completion inputs are evidence summaries, not new tenant fields.
It plans reuse/choice/proposal states; it does not execute tools, establish
provenance, verify live approvals or provide an atomic uniqueness guarantee.

```python
def source_identities(template):
    metadata = template.get("metadata") or {}
    if not isinstance(metadata, dict):
        return set()
    transfer = metadata.get("__coworkcanvasTransfer") or {}
    library = metadata.get("library") or {}
    installation = metadata.get("libraryInstallation") or {}
    identities = []
    for row in (transfer, library, installation):
        if isinstance(row, dict):
            identities.append(row.get("sourceTemplateId"))
    if isinstance(library, dict):
        aliases = library.get("aliases") or []
        if isinstance(aliases, list):
            identities.extend(a.get("sourceTemplateId") for a in aliases if isinstance(a, dict))
    return {v for v in identities if isinstance(v, str) and v.strip()}


def resolve_workflow_run(request, context, templates, runs, pending, observed, mapping=None):
    if not all(context.get(k) for k in ("origin", "tenant_id", "user_id")):
        return {"state": "needs_context"}
    if not all(request.get(k) for k in ("parent_id", "item_type_id", "source_id", "cycle")):
        return {"state": "needs_input"}
    source = request["source_id"]
    compatible = [t for t in templates if type(t.get("isActive")) is bool
                  and t.get("itemTypeId") == request["item_type_id"]]
    mapped = None
    if mapping and mapping.get("verified") is True and mapping.get("source_id") == source:
        if all(mapping.get(k) == context[k] for k in ("origin", "tenant_id", "user_id")):
            mapped = next((t for t in compatible if t.get("id") == mapping.get("template_id")
                           and (source in source_identities(t) or mapping.get("import_evidence_verified") is True)), None)
    if not mapped and observed.get("templates_complete") is not True:
        return {"state": "incomplete"}
    candidates = [mapped] if mapped else [t for t in compatible if source in source_identities(t)]
    explicit = request.get("template_id")
    if explicit:
        candidates = [t for t in candidates if t.get("id") == explicit]
    if not candidates:
        return {"state": "needs_template"}
    if len(candidates) > 1:
        return {"state": "choose_template", "template_ids": sorted(t["id"] for t in candidates)}
    template_id = candidates[0]["id"]
    if observed.get("runs_complete") is not True:
        return {"state": "incomplete"}
    parent_runs = [r for r in runs if r.get("itemId") == request["parent_id"]]
    if any(not r.get("templateId") for r in parent_runs):
        return {"state": "needs_run_identity"}
    matches = [r for r in parent_runs if r.get("templateId") == template_id]
    if any(not r.get("cycle") for r in matches):
        return {"state": "needs_cycle_decision"}
    current = [r for r in matches if r.get("cycle") == request["cycle"]]
    if any(r.get("status") == "CANCELLED" for r in current):
        return {"state": "needs_cycle_decision"}
    selected = request.get("workflow_id")
    if selected:
        current = [r for r in current if r.get("id") == selected]
        if not current:
            return {"state": "needs_run_choice"}
    if len(current) > 1:
        return {"state": "choose_run", "workflow_ids": sorted(r["id"] for r in current),
                "template_id": template_id}
    if current:
        return {"state": "reuse", "workflow_id": current[0]["id"], "template_id": template_id}
    if matches and request.get("new_cycle") is not True:
        return {"state": "needs_cycle_decision"}
    if candidates[0].get("isActive") is not True:
        return {"state": "needs_active_template"}
    if observed.get("fresh") is not True:
        return {"state": "recheck"}
    if observed.get("pending_complete") is not True:
        return {"state": "incomplete"}
    if any(not p.get("template_id") for p in pending):
        return {"state": "needs_pending_scope"}
    if any(p.get("template_id") == template_id and not p.get("cycle") for p in pending):
        return {"state": "needs_pending_scope"}
    if any(p.get("template_id") == template_id and p.get("cycle") == request["cycle"] for p in pending):
        return {"state": "awaiting_approval"}
    return {"state": "propose", "template_id": template_id}


def resolve_checkpoint(steps, node_id, complete):
    if complete is not True or not steps or any(not s.get("id") for s in steps):
        raise ValueError("Incomplete stored step roster")
    if len({s["id"] for s in steps}) != len(steps):
        raise ValueError("Ambiguous stored step roster")
    matches = [s for s in steps if s.get("diagramNodeId") == node_id]
    if len(matches) != 1:
        raise ValueError("Missing or ambiguous stored checkpoint")
    return matches[0]["id"]
```
