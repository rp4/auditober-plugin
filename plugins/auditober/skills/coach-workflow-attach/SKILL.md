---
name: coach-workflow-attach
description: "Use whenever the user asks to attach, instantiate, apply, or run a workflow on an item. Resolve the parent, intended cycle and tenant template, reuse compatible existing or pending work, and propose a new instance only after a complete fresh no-match. Public source identity is distinct from tenant IDs."
uxContract: 1
hostContract: 1
---

# Coach Workflow Attach

Resolve existing work before proposing a workflow instance. A suggestion is
pending approval; read back the approved run before assigning or executing it.

## System Prompt

```
You are the workflow-attach skill.
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Read ../../references/workflow-resolution.md before selecting a template or run.
Read ../../references/query-patterns.md before complete collection reads.
Parse supplied inputs first and ask only unresolved necessary scope or choices.

Resolve the parent item, intended cycle, source identity and tenant template.
Page the complete parent workflow roster; reuse compatible stored work rather
than creating another instance. Resolve ambiguous templates/runs contextually.
A new cycle must be explicit and warranted. Preserve completed history and
customized graphs. Immediately before any create suggestion, reread the
template and all parent runs and resolve relevant pending suggestions.

When the shared resolver permits a create proposal, use exactly:
suggest_change({
  action: "create",
  itemType: "workflow",
  data: {
    fields: {
      itemId: "<parent-item-id>",
      templateId: "<verified-tenant-template-id>",
      name: "<optional-workflow-name>"
    }
  },
  reason: "<one short sentence explaining the warranted new run>"
})
Omit name unless supplied or needed to distinguish the agreed cycle. Default to
the stored template name. templateId is a tenant ID, never the public source ID.
After success, return the proposal and [Review and approve](<previewUrl>) from
the tool. Native human approval and read-back establish the created run.
```

## Inputs

- `--item-id <id>` or `--item-title <text> [--item-type <slug>]` — parent.
- `--template-id <tenant-id>`, `--source-template-id <public-source-id>` or
  `--template-name <text>` — template identity or discovery input.
- `--workflow-id <run-id>` — an existing run choice, verified against parent,
  source and intended cycle.
- `--cycle <period>` — intended period with attributable scope evidence.
- `--new-cycle` — explicit request for a distinct warranted cycle, subject to
  existing/pending-run checks. It does not duplicate a current-cycle run.
- `--name <text>`, `--reason <text>` — optional proposal values.

## Procedure

1. Resolve the parent and cycle under the shared workflow-resolution reference.
   Read supplied IDs back; complete title searches before choosing or declaring
   absence. On ambiguity, use the available question UI or plain text. Headless
   work returns needs_input with the unresolved values.
2. Resolve a supplied tenant template or public source identity. Name discovery
   uses this complete operation and completes offsets:

   query { workflowTemplatesPage(search: "<name>", skip: 0, take: 5) { items { id name } total } }

    A no-match old
   name requires complete compatible discovery before claiming absence.
   Read each narrowed `workflowTemplate(id: "<tenant-id>")` with
   `id name description metadata itemTypeId isActive autoCreateOnItem`.
   Source IDs live in actual metadata/import provenance; do not request a
   nonexistent top-level sourceTemplateId field. Validate active/anchor
   compatibility and origin/tenant/user-bound cached mappings. Present multiple
   installed variants contextually; preserve customized copies.
3. Page `workflows(itemType: "<slug>", itemId: "<parent-id>", skip: 0, take: 25)`
   with the complete shared selection. Resolve cycles, stored graph compatibility
   and real IDs. Reuse the suitable current run; a completed current run is
   history to report, not a trigger to start again. Multiple matches require a
   contextual choice. Never delete pre-existing duplicates.
4. Only a complete fresh no-match allows a proposal. Recheck relevant pending
   workflow-create suggestions immediately before suggest_change. A matching
   pending proposal returns awaiting_approval. Capped personal previews cannot
   prove absence. Missing pages, errors, uncertain cycles or unresolved identity
   block creation and are reported accurately.
5. Submit one canonical create suggestion. Show any validation error accurately;
   resolve its cause before retrying. After authorized approval, read back the
   actual workflow ID, complete steps and stored dependencies. Use
   /coach-workflow-assign and /coach-workflow-execute with real IDs and the stored
   reviewer/approval authority.

## Missing templates and custom workflows

workflow-catalog.json identifies public sources and immutable release pins. It
does not install templates or grant permissions. Missing library templates use
the admin import preview with prerequisite resolution and approval/read-back.
A changed release cannot replace a customized tenant procedure without the
administrator's review.

For a user-requested custom workflow, read coach-workflow-build and
../coach-workflow-build/references/workflow-design.md before authoring. Resolve
the parent/cycle and existing/pending custom runs first. Use the same checkpoint,
form and authority rules: fewest justified human interventions, with their named
role and approval, expertise, variance or interest contribution. Executor work
uses results, evidence uses documents and sign-off uses native approvals.

The alternate create shape sets itemId, name, diagramNodes and diagramEdges in
data.fields and omits templateId. Template and custom graph paths are mutually
exclusive. Position and type are calculated by the platform and must be omitted.
Use get_schema(type: "workflow") for the exact target shape and coach-workflow-build's strict
decision/form/performedBy structures. The optional data.performedBy block uses
primitives (skill IDs), agent and note; it describes automation within the
checkpoint and does not replace its human authority. If requested risks/controls are template
relationships, verify native workflowTemplateStepItemLinks after their approved
read-back before instantiating; prose links and pending suggestions do not satisfy
that prerequisite.

## Notes

A verified source identity permits lookup; it does not authorize imports,
template updates, assignments, execution or human approvals. Repeated module
invocations reuse the six catalog auto-create sources after complete discovery.
The client recheck narrows duplicate risk without claiming server-side atomic
uniqueness. Preserve unresolved evidence and history; do not manufacture an
empty roster from incomplete reads.
