---
title: suggest_change
description: "Propose creates, updates, deletes, form submissions, and branch pruning: every proposal waits for human review."
---

`suggest_change` proposes a create, update, delete, form submission, or workflow branch prune. It requires the `write:suggestions` scope, and it never writes directly: every call produces a pending suggestion that a person reviews and approves or rejects. See [Suggestions](https://docs.assureswarm.com/concepts/suggestions/) for the full review lifecycle.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `action` | string | Yes | One of `create`, `update`, `delete`, `submit_form`, `prune-branch`. |
| `itemType` | string | Yes | A tenant item type slug, or one of the target types listed in Actions by Target below. Case-insensitive; normalized to lowercase. |
| `targetId` | string | Sometimes | Required for `update`, `delete`, `submit_form`, and `prune-branch`. |
| `data` | object | Sometimes | Accepts only `title`, `status`, and `fields`. Any other key is rejected: the error names the stray keys and points at `data.fields`. |
| `reason` | string | No | Why you're proposing the change. Optional, but strongly recommended: the reviewer sees it. |
| `agentName` | string | No | Name of the proposing agent, shown to the reviewer. |
| `agentType` | string | No | One of `unknown`, `oauth-agent`, `mcp-agent`, `ai-agent`. Any other value is stored as `unknown`. |

## Actions by Target

Which actions are valid depends on the target named in `itemType`. Any configured item type accepts create, update, and delete; a handful of built-in targets extend or narrow that set:

| Target (`itemType` value) | create | update | delete | submit_form | prune-branch |
|---|---|---|---|---|---|
| any configured item type slug | ✓ | ✓ | ✓ | No | No |
| `step` | ✓ | ✓ | ✓ | ✓ | No |
| `workflow` | ✓ | ✓ | ✓ | No | ✓ |
| `workflowtemplate` | ✓ | ✓ | ✓ | No | No |
| `timeentry` | ✓ | ✓ | ✓ | No | No |
| `itemrelationship` | ✓ | No | ✓ | No | No |
| `stepitemlink` | ✓ | No | ✓ | No | No |
| `stepdocumentlink` | ✓ | No | ✓ | No | No |
| `formassignment` | ✓ | No | ✓ | No | No |
| `workflowtemplatestepitemlink` | ✓ | No | ✓ | No | No |

### Field Notes for Common Targets

- **`step` create**: requires `workflowId`. Optional: `afterStepId` to position the new step, `instructions`, `dueDate` (ISO 8601), and `approvers` as `[{ userId, reviewLevel }]`.
- **`timeentry`**: rows are weekly: `itemId`, `weekStart`, and per-day hour fields.
- **`formassignment` create**: requires `stepId` and `userEmails` (a non-empty array of email addresses).
- **`itemrelationship` create**: requires `sourceItemId` and `targetItemId`. Optional `kind`: `parent`, `child`, `sibling`, or `related` (default `related`).
- **`workflowtemplate` and `workflow` create**: optional `stepLinks`, an array of `{ diagramNodeId, itemId, kind? }`, links step nodes to items in the same suggestion; the reviewer sees them on the preview and one approval creates everything. `diagramNodeId` must be an explicit, unique node `id` in `nodes` / `diagramNodes` (or the template's nodes when creating a workflow from `templateId`, where the links are added on top of the template's own). `kind` defaults to `related`. Not accepted on update: link existing templates and workflows with `workflowtemplatestepitemlink` and `stepitemlink`.

- **`workflowtemplate` create**: requires `itemTypeId`, the anchor item type. Its MCP fields are name, description, itemTypeId, nodes, edges, and create-only stepLinks. It has no `isPublic` flag and does not expose metadata or automatic-creation settings.
- **`workflowtemplatestepitemlink` create**: requires `templateId`, `diagramNodeId`, and `itemId`; optional `kind`. Delete uses the existing link row ID as `targetId`.

Accepting a `step` result update saves the work product. Native step approval
is a separate human action; inspect approval counts and status before reporting
the step complete.

## Validation Rules

These apply before a suggestion is ever created: a call that breaks one is rejected outright, with nothing left to review:

- `create` on a configured item type requires `data.title`.
- `submit_form` is valid only with `itemType: "step"`, and requires the answers object at `data.fields.values`.
- Custom and editable fields always nest under `data.fields`: never directly under `data`.
- `stepdocumentlink` creates accept only fully-qualified `http` or `https` URLs.
- `workflow` creates take either `templateId` or `diagramNodes` plus `diagramEdges` under `data.fields`: never both.
- `stepLinks` is create-only; a malformed entry or a link to a node that is not in the submitted graph is rejected before a suggestion exists. Item visibility and per-step limits are checked when the reviewer approves.
- Discover each target's exact fields with [get_schema](https://docs.assureswarm.com/mcp/get_schema/) (for example, `{"type": "step"}`); item type slugs are tenant-specific.

## Examples

Three common calls:

### Create an Item

```json
{
  "name": "suggest_change",
  "arguments": {
    "action": "create",
    "itemType": "issue",
    "data": {
      "title": "Missing evidence on access review",
      "fields": {
        "priority": "medium",
        "summary": "The Q2 access review step has no supporting document attached."
      }
    },
    "reason": "The user asked for a draft issue for the missing evidence."
  }
}
```

### Propose Form Answers

```json
{
  "name": "suggest_change",
  "arguments": {
    "action": "submit_form",
    "itemType": "step",
    "targetId": "<step-id>",
    "data": {
      "fields": {
        "values": {
          "control_operating": "yes",
          "notes": "Verified against the July extract."
        }
      }
    },
    "reason": "Drafted from the document the user shared."
  }
}
```

### Prune a Not-Taken Branch

```json
{
  "name": "suggest_change",
  "arguments": {
    "action": "prune-branch",
    "itemType": "workflow",
    "targetId": "<workflow-id>",
    "data": {
      "fields": {
        "decisionNodeId": "<decision-node-id>",
        "takenValue": "approved"
      }
    },
    "reason": "The decision resolved to approved; removing the rejected branch."
  }
}
```

Pruning permanently deletes steps that are reachable only through the not-taken branch. See [Workflows](https://docs.assureswarm.com/concepts/workflows/). Discover the exact fields for your workflow with `get_schema` (`{"type": "workflow"}`).

## Response

`suggest_change` returns a text confirmation, not the created or updated object itself. It states that the suggestion was created and must be approved before it takes effect, and it includes:

- The suggestion ID.
- Its status (`pending`).
- A **"Preview & approve"** link you can hand to the user: or, if none is returned, a note that the suggestion now appears in their review sidebar.

## Agent Notes

- Keep each suggestion small and focused. One change per call is easier for a reviewer to judge than a bundle.
- Always include a `reason`: it's the main context the reviewer has for the change.
- Share the "Preview & approve" link, or point the user to their review sidebar, so they know where to act on it.
- Never tell the user a change is done. It stays pending until a person approves it in the app.
- When you're unsure of an item type slug or a target's exact fields, call [get_schema](https://docs.assureswarm.com/mcp/get_schema/) instead of guessing: both are tenant-specific.
