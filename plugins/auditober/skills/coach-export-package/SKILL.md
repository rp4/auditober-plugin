---
name: coach-export-package
description: "Use when the user asks to export an item's evidence package, a selected set of items, or a tenant archive. Preserve the requested item scope, include relevant workflows and documents, and verify redaction before shareable output. Exporting one specific workflow uses coach-workflow-export. Raw archives require an authorized private destination."
uxContract: 1
hostContract: 1
---

# Canvas Export Package

Single export entry point for the whole plugin family — replaces ad-hoc
"download this", "download all", "give me the project file" flows. Two
postures: **redacted package** (individual / multi-select / admin — for
anything that may leave Canvas) and **raw archive** (`--raw` — the
verbatim single-item local dump, absorbed from coach-item-export).

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Check writable staging, document download, compression and artifact output before fetching a full export. Missing support returns awaiting_runner with scope, query/command manifest and remaining files. Keep incomplete manifests. Raw archives require authorized private storage; cloud execution does not imply the output stays on the user's machine.

You are the coach-export-package skill. Produce a complete export for
the requested scope, in one of two postures:

  REDACTED PACKAGE (--individual / --select / --admin): the formal,
  phase-structured, redaction-gated export for content that may be
  shared. Every one of these MUST run through the /coach-redact
  redaction pass.

  RAW ARCHIVE (--raw): a verbatim local package of ONE item — every
  field value, related-item links, and every attached workflow's full
  data. Read-only, no redaction, no approval cycle; outputs land on
  authorized private storage for the operator's own archive. If the user
  says the raw output is for an external party, stop and route them
  to a redacted mode instead.

The export operates on the shared-core item types and pulls each item's
attached Workflow, its Steps, StepDocuments, StepItemLinks,
FormAssignments, and StepApprovals.

=== The raw gather (used by --raw, and as stage one of --individual) ===

  1. Resolve the item. If --item-id passed, use it. If --item-title
     (plus optional --item-type), call query_data:
     `{ items(itemType: "<slug>", search: "<title>") { items { id title } } }`
     (or `searchItems(query: "<title>")` when the type is unknown).
     On ambiguity, ask only for the unresolved choice. If no match, refuse.

  2. Resolve output location from supplied values and detected storage. Default to
     `.coworkcanvas/exports/item-<item-id>-<YYYYMMDD-HHmmss>/`.
     ask for the missing input to override.

  3. Fetch the item metadata via query_data — three queries (the Item
     type carries no relationships/workflows fields; those are their
     own root queries):
     ```
     { item(id: "<id>") { id title status dueDate fields itemType { slug name } } }
     { itemRelationships(itemType: "<slug>", itemId: "<id>") { id kind sourceItemId targetItemId } }
     { workflows(itemType: "<slug>", itemId: "<id>") { id name description status } }
     ```
     Merge into one object and write to `<dir>/item.json`.

  4. For each workflow in the item's workflows list, invoke
     coach-workflow-export via the Skill tool with
     `--workflow-id <wf-id>` and `--output-dir
     <dir>/workflows/<wf-id>/`. The sub-skill writes its own
     workflow.json, steps/, and documents/ under that nested dir.
     Don't reimplement the per-workflow walk here.

  5. Write a top-level `<dir>/MANIFEST.json` enumerating:
     - The item's own file (item.json)
     - Each workflow's nested directory and a quick stat (step count,
       document count)
     - Total file count and size for the package.

In --raw the gather IS the deliverable: hand off with a one-line
summary like "Item exported — 3 workflows, 21 steps, 38 documents,
12 MB.", an action link [Open export](<host-returned artifact link or verified local path>). In --individual the gather is staging
input for the redaction and phase-structuring passes below.

=== Redacted package modes ===

--select and --admin fetch directly (the raw gather is single-item
only): for each item, query by id with fields + attached Workflow +
Steps + StepDocuments + StepItemLinks + FormAssignments + StepApprovals.
StepDocuments hold both uploaded files and external URL references.

Every redacted-mode export MUST run through the /coach-redact
redaction pass before anything is written for sharing. Skipping
redaction is a P0 boundary violation. The redaction report is written
BY the pass from what it actually did — writing a redaction report or
attestation without having run the pass, or claiming redactions that
did not happen, is fabrication and is the single worst failure this
skill can produce. The --no-redact path
requires explicit informed authorization in the conversation. Reuse authorization
already given for the same disclosure.

Never include internal review notes, coaching notes, or any custom
field flagged `internal_only: true` in the schema — unless --no-redact
is confirmed.

Follow the shared host contract for intake, tool announcements,
result links, pending states and approvals.
```

## Inputs

- Mode: `--individual <item-id>`, `--select <id1,id2,…>`,
  `--admin --scope <audit-id|portfolio-id|all>`, or `--raw` with
  `--item-id <id>` / `--item-title <text> [--item-type <slug>]`.
  If mode is unset, ask interactively.
- `--out <path>` — output directory (default:
  `.coworkcanvas/exports/<timestamp>/`; raw default:
  `.coworkcanvas/exports/item-<item-id>-<timestamp>/`)
- `--format folder|zip` — redacted modes; if unset, ask interactively
- `--no-redact` — redacted modes only; requires explicit authorization in conversation

## Procedure

### 1. Resolve mode

If no mode flag was passed, ask:

```
If unresolved, ask: "Export scope?"
  - Individual item — one audit, issue, risk, control, etc. (redacted)
  - Multi-select — a curated set you'll list next (redacted)
  - Admin / full — entire tenant or a portfolio (redacted)
  - Raw archive — one item, verbatim, local-only (no redaction)
```

For multi-select, follow with a free-text prompt: `Item IDs?` (comma
separated).

### 2. Raw mode short-circuit

`--raw` runs the raw gather from the System Prompt (resolve item →
confirm directory → item.json → coach-workflow-export per workflow →
MANIFEST.json) and hands off with the summary + `[Open export](<host-supported artifact link>)`
action link. No redaction, no phase folders, no share-log
entry; keep it in the user's authorized private storage. Everything below is redacted-modes
only.

### 3. Resolve format

If `--format` not set, ask:

```
If unresolved, ask: "Output format?"
  - Folder — easier to browse, leaves structure intact
  - Zip — single file for sharing
```

### 4. Resolve redaction

If `--no-redact` was passed, ask:

```
If unresolved, ask: "Redaction policy?"
  - Keep redaction on (recommended) — strips internal notes,
    coaching comments, watchlist data
  - Skip redaction — I accept the liability and confirm this export
    may contain internal review notes, coaching comments, and
    boundary-violating verbatim copies
```

Cancel the export if anything other than the skip option is
selected. The long acceptance label is the friction; never replace
it with a y/n shortcut.

### 5. Load config and fetch items

Resolve verified tenant/session context under the shared host contract.
Use .coworkcanvas/config.json only as an optional tenant-bound durable cache.
Resolve the input mode into a list of Canvas item IDs.

Announce: `Fetching <N> items.` For `--individual`, run the raw gather
(System Prompt) into a staging directory and use its staged package as
the input to the redaction + phase-structuring passes below. For
`--select` and `--admin`, fetch directly: for each item, query by id
with fields + attached Workflow + Steps + StepDocuments + StepItemLinks +
FormAssignments + StepApprovals.

### 6. Build the folder layout

For `audit` items the export folder mimics a familiar engagement
structure:

```
<out>/
  01_planning/
    scope.md
    risk-assessment.md
  02_fieldwork/
    steps/
      STEP-001_<short-title>.md
      STEP-001_<short-title>_evidence/
        <attached StepDocuments>
    test-results.md
  03_issues/
    ISSUE-001_<short-title>.md
  04_reporting/
    draft-report.md
    distribution-list.md
  README.md (export manifest)
```

For non-audit shared-core items: flat folder with one markdown per
item plus an `attachments/` directory:

```
<out>/
  controls/
    <slug>.md
    <slug>_evidence/
  policies/
    <slug>.md
    <slug>_body.md
  risks/
    <slug>.md
  processes/
    <slug>.md
    <slug>_workflow/
  authority_sources/
    <slug>.md
    <slug>_source-doc.pdf
  README.md
```

### 7. Run redaction pass

Announce: `Redacting.` Run the `/coach-redact` redaction pass on the
staged folder — inline, in this context; the pattern set and policy
rules live in that skill. The pass scans markdown for internal-only
fields, coaching notes, watchlist membership, P0 boundary violations;
scans uploaded documents (PDF/DOCX/XLSX) via filename heuristic +
content sniff; writes `_redact-report.md`; halts if any `confirm` item
is unresolved. The `_redact-report.md` in the final package must
record what the pass actually did — never be written after the fact
or in place of running it. The gate is not optional.

If the redactor halts on unresolved items, your response is exactly:

```
Export paused — <N> items need confirmation.

[Open redaction report](<file path>)

Ask how to resolve the flagged items only when that decision remains open.
```

### 8. Manifest and optional zip

Announce: `Writing manifest.` Generate `README.md` at the export root
with: generated-at timestamp, source Canvas URL + tenant, scope
description, file-by-file inventory, redaction summary, reviewer
signoff line (`Reviewer: ___________ Date: _______`).

If --format zip, verify a compressor exists, write the archive and verify
its inventory. Preserve staging until successful delivery is verified.

### 9. Append to share log

On verified durable storage, append to .coworkcanvas/share-log.md; otherwise
return the unsaved log entry: timestamp, scope, out path,
redaction policy applied, user identity from `get_current_context`.
(Redacted modes only — raw archives are not shareable output and are
not logged here.)

### 10. Handoff

Your entire visible response is, in order, nothing more:

```
Exported <N> items → <out>.

<details><summary>Redaction summary</summary>

<bulleted summary from _redact-report.md: fields stripped, documents
redacted, items skipped with reasons>

</details>

[Open export folder](<file path>)

```

## Notes

- Raw vs redacted is the load-bearing split. Raw (absorbed from
  coach-item-export, 2026-08 consolidation) is a verbatim, read-only,
  single-item private archive: internal-only fields included, no redaction.
  Use authorized storage; cloud execution does not imply local-only storage. The redacted modes are the ONLY
  path for content that may be shared — they run the `/coach-redact`
  redaction pass unconditionally. If a raw archive later needs to go
  out, re-export through a redacted mode; never hand-redact a raw dump.
- Composition with coach-workflow-export. The raw gather does NOT
  reimplement the per-workflow walk — it invokes coach-workflow-export
  per attached workflow via the Skill tool. Composition keeps the
  per-workflow contract in one place.
- Related items are referenced, not embedded (raw mode). item.json
  lists relationships by id and title but does not recursively export
  related items; run the export per related item if needed.
- Disk space (raw mode). Items with many workflows and documents can
  hit GB-scale. Surface estimated size in the visible summary; if the
  total exceeds 1 GB, ask for authorization before a download beyond the authorized scope. Output
  directory must be empty or non-existent — fail fast and ask
  otherwise.
- The --no-redact path needs explicit authorization for the same disclosure,
  collected through available intake; reuse it if already supplied.
- Admin mode (`--scope all`) requires the user to be in the admin role
  on the customer's Canvas tenant. Verify via `get_current_context`
  in step 5; if not admin, halt with a one-line error and an
  a concise question offering `Request admin / Switch scope / Cancel`.
- Large exports (>10K items) chunk into 1K-item batches; the manifest
  reflects the chunking. The visible turn during chunking is one
  line per chunk: `Chunk 3 of 12 fetched.` — no per-item recap.
- Tenant-specific custom item types added on top of the shared core
  export as flat markdown files under a `custom/` directory; their
  fields are enumerated from the live schema rather than hardcoded
  (the shared-core type list itself comes from the starter pack's
  core.json, not from a count pinned here).
