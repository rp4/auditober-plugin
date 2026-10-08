---
name: coach-redact
description: "Use when the user asks to redact, scrub, or sanitize a staged directory of outbound content before export — the standalone entry point for ad-hoc redaction passes, and the plugin's single redaction engine: every skill that produces shareable output runs this same pass inline before anything leaves the workspace. Deterministic internal-only patterns are auto-removed, ambiguous ones surfaced for user confirmation, and a redact report written. Build-list rows 7, 30."
uxContract: 1
hostContract: 1
---

# Coach Redact

The universal outbound-safety gate and the plugin's single redaction
engine. Every outbound artifact — report draft, exported workpaper
folder, deficiency narrative, handoff log, regulatory submission —
passes through this procedure before it leaves Canvas's gravity. Run
it standalone over any staged directory, or inline from a calling
skill (`/coach-export-package`, `/coach-render-package`,
`/coach-notify`, `/coach-ticket`, `/coach-security-report`,
`/coach-bulk-user-change --report`): the pattern set, the policy
rules, the severity floor, and the report format live here and
nowhere else.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Verify staging access, the caller's tenant-bound schema snapshot and extractors for every format. Missing access/schema/extractor returns status:halt with state:awaiting_runner, unexamined files and the input manifest. Internal-only field coverage is incomplete without the schema. Never fabricate a clean verdict or completed report.

You are the coach-redact skill, the Auditober plugin's single
redaction engine. Find internal-only content in a staged directory
and remove it deterministically OR surface it for user confirmation.

1. Resolve the staged directory (--staged) and policy (--policy,
   else .coworkcanvas/config.json redaction_policy, default block).
   Policy off requires explicit confirmation in conversation before
   the pass runs.
2. Run the pass over the staged path: load the schema snapshot for
   internal-only fields, apply the deterministic pattern set to every
   markdown file (rewrite with [redacted: kind] markers), apply the
   heuristic pattern set per policy, scan binary documents and flag
   them for user editing, then write _redact-report.md at the staged
   root.
3. Render the verdict: the _redact-report.md path, the summary
   counts, and any unresolved items. On status needs_user, surface
   the flagged spans and stop until they are resolved.

You write only inside the staged directory plus _redact-report.md.
You never call Canvas MCP tools during the pass. Be deterministic and
idempotent: re-running on the same input produces the same output.

Output discipline. Closing pleasantries and recaps are not permitted.
End with the redact-report path plus the structured verdict (status,
counts, unresolved items).
```

## Inputs

- `--staged <path>` — directory of staged outbound content
- `--policy warn|block|off` — overrides `.coworkcanvas/config.json`
  redaction_policy

## Procedure

1. Resolve `--staged` and the policy. `off` requires explicit
   confirmation in conversation before the pass runs.
2. Read the staged directory tree. Load `.coworkcanvas/schema.json`
   when it is the verified current snapshot; otherwise use the caller-supplied
   tenant-bound schema reference to identify internal_only fields.
3. Walk every `.md` file; apply the deterministic patterns below;
   rewrite matches with `[redacted: <kind>]` markers.
4. Apply the heuristic patterns per policy: under `warn`, remove and
   log; under `block`, leave in place and flag.
5. Walk every binary document; extract text via `pdftotext` /
   `unzip`+xml for Office formats; scan for the same patterns; flag —
   never edit a binary.
6. Write `_redact-report.md` at the staged root with sections:
   Removed (deterministic), Removed (heuristic), Requires user
   editing (binary), Skipped (if policy=off), Summary counts.
7. Return the verdict `{ status: "clean" | "needs_user" | "halt",
   removed, flagged, binary_flagged, unresolved }`. Callers halt on
   `needs_user` — no export, draft, or package proceeds with
   unresolved flags.

The calling skill orchestrates steps 2–7 in the verified execution environment.
Protected raw extracts stay in an isolated runner; only bounded findings and
source references enter the conversation. Missing isolation returns halt with
awaiting_runner. The caller carries the actual verdict forward; it never writes a redaction
report or attestation in place of running the pass, and it never
skips the pass because the content "looks clean".

## What gets removed (deterministic, no confirmation)

- Fields flagged `internal_only: true` in the customer's
  `.coworkcanvas/schema.json`.
- Markdown sections titled `## Review Notes`, `## Coaching Notes`,
  `## Internal`, `## Confidential`, `## For Reviewer Only`.
- Inline tags: `[INTERNAL: ...]`, `[REVIEW: ...]`, `[COACHING: ...]`,
  `[DO NOT SHARE: ...]`.
- Watchlist arrays in frontmatter (`watchlist:`, `watchers:`).
- Comments where the author role is `reviewer`, `coach`, `qa_reviewer`,
  or `audit_committee`.

## What gets flagged for user confirmation

- Sentences containing close paraphrases of `for the auditor only`,
  `do not share`, `between us`, `off the record`, `internal
  discussion`, `preliminary view`.
- Full names or HR identifiers within 50 chars of
  performance-evaluation language (`underperforming`, `needs
  improvement`, `exceeds expectations`) in any context.
- Verbatim blocks > 140 chars matching a Canvas item-field value —
  P0 boundary violations (plugin-side markdown should reference
  Canvas, never copy from it).
- Documents containing the literal strings `DRAFT — DO NOT
  DISTRIBUTE`, `PRIVILEGED & CONFIDENTIAL`, `ATTORNEY-CLIENT
  PRIVILEGED` — legal markers; surface and let the user decide.

## What is never touched

- Files outside the staged directory.
- The `_redact-report.md` itself (the pass writes it; it is not
  redacted).
- Binary documents (PDFs, Office files, images) — flagged for user
  editing, never auto-rewritten.

## Policy

The caller passes the policy; absent that, read
`.coworkcanvas/config.json` `redaction_policy` (default `block`):

- `block`: any unresolved ambiguous item halts the caller's flow —
  leave it in place and flag it.
- `warn`: ambiguous items are removed by default but logged as
  "would have flagged" entries so the user can review.
- `off`: skip redaction, log what would have been done. Only valid
  when the caller has already collected an explicit user
  confirmation — never assumed.

## Severity floor

`severity: critical` themed Canvas items and `confidential: true`
contracts/policies ALWAYS require user confirmation, regardless of
configured policy. This floor cannot be lowered.

## Notes

- Callers that produce shareable output run this pass themselves —
  `/coach-export-package`, `/coach-render-package`, `/coach-notify`,
  `/coach-ticket`, `/coach-security-report`, and
  `/coach-bulk-user-change --report` all gate on it. This skill is
  the standalone entry point and the source of truth for the pattern
  set, not a required hop.
- The pass never writes outside the staged directory — modifications
  are contained.
- Binary document redaction is intentionally NOT automated. The pass
  flags; the user edits.
- Mirrors `brain-redactor` from the Second Brain plugin — same
  invariants apply. If a user has both, redaction works the same in
  both contexts.
