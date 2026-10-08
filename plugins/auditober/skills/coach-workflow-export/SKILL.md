---
name: coach-workflow-export
description: "Use whenever the user asks to export, download, archive, snapshot, or bundle a workflow's data. Gathers the complete data of a workflow instance — every step's result, every form's submitted values, every uploaded or linked document — into a local directory: walks the workflow via query_data, downloads attached documents via download_document, and writes a structured local package the operator can archive or share. Read-only; never mutates the workflow."
uxContract: 1
hostContract: 1
---

# Coach Workflow Export

Bundle a workflow's complete data — step results, form values, documents — into a local directory. Read-only.

For redaction-gated formal exports across multiple items, use [`coach-export-package`](../coach-export-package/SKILL.md) instead. This skill is the simpler, raw-dump variant.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Check writable staging, document download and artifact output first. Reuse a supplied path or verified staging area. If unavailable, return awaiting_runner with the workflow ID, query/input manifest and missing output capability. Raw output remains private and unredacted; partial output is not complete.

You are the workflow-export skill. The user wants a complete local
package of a workflow's data: every step's saved result, every form's
submitted values, every document attached to any step. Your job is to
walk the workflow, gather the data, download every document, and write
a structured directory the user can archive.

This skill is READ-ONLY. It does not mutate the workflow. It does not
go through suggest_change. There is no approval cycle — outputs land on
the local filesystem.

This skill does NOT redact. Internal review notes, coaching comments,
and any field flagged internal_only in the schema WILL be included.
For redaction-gated exports, use coach-export-package.

Tools used:
  - query_data to walk the workflow's metadata and steps
  - get_step_context to read each step's result body and form
  - download_document to fetch each attached document's bytes

Read ../../references/query-patterns.md before any complete collection read.
Normal step pages use first:25; rich export and sweep pages use first:5.
Collect nodes by id and follow pageInfo until hasNextPage is false, preserving
the full selection. Missing/repeating endCursor, GraphQL errors, truncation
and unresolved predecessors mean an incomplete read. Stop before execution,
assignment or claiming a complete export. Offset lists use skip/take with
unchanged filters, advance by returned rows, and stop at a short page or the
API's verified total. Never infer absence from one page.

Procedure:

  1. Resolve the workflow. If --workflow-id passed, use it. If
     --workflow-name, call query_data:
     `{ allWorkflows(skip: 0, take: 25) { id name itemId itemType } }` and
     complete offset discovery, then match the name client-side — workflow list queries have no
     text-search argument. On ambiguity, ask only for the unresolved choice. If absent
     and the user is viewing a workflow, use get_current_context's
     currentView.workflowId.

  2. Confirm output location. Default to
     `.coworkcanvas/exports/workflow-<wf-id>-<YYYYMMDD-HHmmss>/`.
     Use a supplied directory override; ask only if the output location is unresolved.

  3. Fetch the workflow metadata via query_data:
     ```
     {
       workflow(id: "<id>") {
         id name description status itemId itemType
         steps(first: 5) {
           pageInfo { hasNextPage endCursor }
           nodes {
             id name description instructions status
             dueDate approvedCount requiredApprovals
             approvals { user { id name email } status reviewLevel }
           }
         }
       }
     }
     ```
     Read and merge every steps page before writing `<dir>/workflow.json`.

  4. For each step, call get_step_context to fetch its result body and
     form. Write to `<dir>/steps/<step-id>.json` containing { step
     metadata, result.body, step.formData.values, step.formData.fields, documents
     metadata }. Keep step.formData.submittedAt and submittedBy alongside the
     fields and values; these describe the saved submission.

  5. For each document on any step (whether uploaded or linked),
     call download_document with the document id. For utf8 bodies,
     write to `<dir>/documents/<step-id>/<filename>`. For binary
     content, write the base64 to `<filename>.b64` and note the
     mimeType in `<dir>/documents/<step-id>/index.json`.

  6. Write a top-level `<dir>/MANIFEST.json` listing every file
     produced with its size and a short label. The operator should be
     able to open this and see the structure without exploring.

  7. Hand off with one-line summary like "Workflow exported — 7
     steps, 14 documents, 3.2 MB.", an action link to open the
     directory `[Open export](<host-returned artifact link or verified local path>)`.

UX contract (see UX-CONTRACT.md).

Follow ../../references/host-capabilities.md for intake and output.
Return the result and its real action/artifact link.
```

## Inputs

- `--workflow-id <id>` or `--workflow-name <text>` — the workflow.
  If absent, infer from current view.
- `--output-dir <path>` — output directory. Default
  `.coworkcanvas/exports/workflow-<wf-id>-<timestamp>/`.

## Procedure

1. Resolve the workflow (id, query_data search, or current view).
2. Confirm output directory.
3. Fetch metadata and every steps page via `query_data`, following
   pageInfo as above. Merge the full roster and write `workflow.json`.
4. For each step, `get_step_context` → write `steps/<step-id>.json`.
5. For each document on any step, `download_document` → write the
   bytes (or base64) under `documents/<step-id>/`.
6. Write `MANIFEST.json` summarizing the package.
7. Hand off with summary + open-export action link.

## Notes

- Read-only by design. This skill never calls suggest_change. The
  workflow's data is unchanged after export.
- No redaction. The output contains every field exactly as stored.
  Internal-only fields, review notes, and coaching comments are
  included. If the export will be shared outside the team, use
  `coach-export-package` instead — it runs the `/coach-redact`
  redaction pass. The gate is not optional once output leaves the team.
- Document handling. utf8 documents (markdown, csv, txt) write as
  text. Binary documents (pdf, docx, xlsx, png, jpg) write as base64
  with a `.b64` suffix and a mimeType note in the per-step
  documents/<step-id>/index.json. The operator can decode binaries
  via `base64 -d` or a small helper script.
- Linked documents. For documents linked via stepdocumentlink
  (external URLs), the export captures the URL + filename + fileType
  in the step's JSON. It does NOT fetch the external URL's content —
  that would require credentials the platform doesn't have.
- Path safety. The output directory is created if it doesn't exist.
  If it already has files, the export fails fast rather than
  overwriting — ask for the missing input to pick a new directory.
- Disk space. A large workflow with many uploaded PDFs can easily
  hit hundreds of MB. The skill should surface estimated size in
  the visible summary so the operator knows. If the documents total
  exceeds 1 GB, ask for authorization before a download beyond the authorized scope.
- Composition. To export ALL workflows attached to an item plus the
  item's own data, use `/coach-export-package --raw` — it calls this skill
  for each attached workflow.
