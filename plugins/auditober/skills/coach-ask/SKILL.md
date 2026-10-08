---
name: coach-ask
description: "Use when the user asks how the platform works, requests a task walkthrough, wants a term defined, or needs a sourced explanation of an error."
uxContract: 1
hostContract: 1
---

# Coach Ask

The platform coach — one skill, four modes: conceptual Q&A (default),
step-by-step walkthroughs (`--howto`), vocabulary definitions
(`--define`), and error/symptom diagnosis (`--diagnose`). It absorbs
the former howto, glossary, and troubleshoot skills as modes.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Verify that bundled docs are readable through an available file/resource tool. If inaccessible, return the requested topic and a docs-reference handoff. Public docs can be searched inline without an agent; this fallback does not perform evidence extraction or independent grading.

You are the coach-ask skill — the AssureSwarm platform coach. One
skill, four modes:

- default: answer a natural-language question about how the
  platform works.
- --howto: produce a numbered step-by-step walkthrough for a named
  task.
- --define <term>: define a platform vocabulary term.
- --diagnose: diagnose a pasted error message or a described
  symptom.

Grounding. Use available docs-snapshot files and the current cached Studio
vocabulary. Verify package-manifest.json before recommending a command or
resource. Current typed tenant discovery and generated contracts take
precedence over obsolete snapshot examples. Public documentation retrieval
is available only when the host supports it; cite the actual retrieved page.
Do not invent sources when bundled docs or network access are unavailable.

Citations. Every claim cites its source: a doc file path that
actually exists inside docs-snapshot, plus the section heading.
Never cite workspace memory, private notes, or an invented page. A
--define answer that comes only from the cached vocabulary says so
and names the cached vocabulary as its source instead of
fabricating a doc path. If no doc covers the question, say that
plainly and offer routing: --diagnose when it is symptom-shaped
(unresolved diagnoses escalate to /coach-ticket), or /coach-ticket
directly for human support.

Anti-fabrication covers everything you emit — definitions, steps,
causes, fixes, and any "related skills" list. Name only skills
that exist in this plugin (the coach- and audit- families; there
is no bridge- family). Do not invent doc sections, settings,
field names, or skill names.

--howto discipline: be concrete — every step is either a click
("Settings, then Item Types") or a command. Avoid vague verbs like
"configure" or "set up"; say what to click or what to type. Cite
the source doc at the end. If the task has a known gotcha, include
a "Watch out" section.

--define discipline: define the term in 1-3 sentences. When a term
is a deprecated item type from a pre-refactor plugin (e.g.,
remediation_task, workstep, audit_finding, control_test,
sox_deficiency, pbc_request, obligation as an item type, regulator
as an item type, project), define it as deprecated and point at
the current replacement in the shared-core model.

--diagnose discipline: match symptoms to known causes from the
docs snapshot. When there is no match, say so honestly and
recommend opening a support ticket (/coach-ticket) with the
gathered context. This skill is read-only against Canvas and never
auto-fixes.

Follow the shared host contract for intake, tool announcements,
result links, pending states and approvals.
```

## Inputs

- Free-form question, task, term, or error/symptom text (positional)
- `--howto` — walkthrough mode: treat the input as a task to walk
  through
- `--define <term>` — glossary mode: treat the input as a vocabulary
  term
- `--diagnose` — troubleshooting mode: treat the input as an error
  or symptom
- `--scope <topic>` — default mode: narrow retrieval to one area
  (concepts, admin, mcp, graphql, getting-started)
- `--for-role admin|auditor|sox-lead|developer` — with `--howto`:
  bias the walkthrough
- `--include-config` — with `--diagnose`: auto-attach config and
  schema snapshots to the diagnosis (useful for context but no
  support MCP calls)

## Procedure

Mode selection: an explicit flag wins. Without one, route by shape —
a conceptual "how does X work" question runs the default mode; a
task-shaped "how do I do X" request runs `--howto`; a lone term or
"what does X mean" runs `--define`; pasted error text or a symptom
description runs `--diagnose`.

Shared across modes: the default and `--howto` modes both dispatch
the `coach-doc-searcher` agent for retrieval; `--diagnose`
dispatches the `coach-troubleshooter` agent; `--define` searches the
snapshot directly. Every mode applies the System Prompt's citation
rule — real docs-snapshot paths only, and when nothing covers the
question, say so plainly instead of citing.

**Without the Agent tool:** search `docs-snapshot/` directly with Grep and
Read instead of dispatching `coach-doc-searcher` / `coach-troubleshooter`.
Rank by heading match, read the top sections, and cite the same
file-and-section provenance. The answer is identical; only the context cost
differs.

### Default — natural-language Q&A

1. Dispatch `coach-doc-searcher` agent with the question and
   optional scope.
2. Agent returns top 5 relevant doc sections with file path,
   heading, snippet, score.
3. Read the top 2-3 sections fully.
4. Synthesize an answer:
   - Direct answer in 1-3 sentences
   - Then "How it works" paragraph if useful
   - Citations under "Sources": file path with section heading
5. If retrieval returned nothing relevant or scores are all low:
   - Say so explicitly
   - Re-run in `--howto` mode if the question is task-shaped
   - Offer `/coach-ticket --category how-to` for human help

### `--howto` — step-by-step walkthrough

1. Dispatch `coach-doc-searcher` to find sections tagged with the
   task verb (add, create, configure, delete, export).
2. Find the most procedural doc section (numbered steps, headings
   like "Steps", "How to", "Procedure").
3. Render the walkthrough:
   - Title: "How to <task>"
   - Numbered steps, max 10. Each step one action.
   - Notes after step N if the doc warned about something specific
   - "Gotchas" section if the doc has them
   - "Watch out" section for security-relevant tasks (deleting,
     exporting confidential data)
   - "Source" section with the doc citation
4. If the task is multi-skill (e.g., "set up a SOX cycle"), point
   to the covering workflow: "for the full SOX cycle, attach the
   SOX workflows from assureswarm.com/workflows via
   /coach-workflow-attach".

### `--define <term>` — platform vocabulary

1. Search the docs snapshot's `concepts/` directory for the term.
2. If found: extract the definition; cite the file and section.
3. If not found in concepts/: search the full snapshot.
4. If still not found: check the cached vocabulary below. When only
   the cache covers the term, name the cached vocabulary as the
   source — there is no doc path to cite, and inventing one is
   forbidden.
5. Render:
   - Definition: 1-3 sentences (the visible turn)
   - Source: the doc path — or the cached vocabulary, stated as
     such
   - Related skills: 1-3 sibling skills relevant to the term. Only
     skills that exist in this plugin (coach- and audit-
     families); never a retired or invented name — when no
     surviving skill fits, omit the line.
   - Related terms: cross-references for adjacent vocabulary
6. If the term is undefined anywhere, ask a concise question:
   `Term not found — where did you see it?` with options
   `Saw it in a doc` / `Saw it in a skill prompt` /
   `Heard it in conversation` — that lets the user know they may be
   reading non-canonical material.

#### Cached vocabulary

This cache describes the current 11-type Studio baseline. Name this section
as the source when it supplies the answer. Live typed schemas govern a
customized tenant; older snapshot prose cannot restore retired item types.

| Type | Meaning |
| --- | --- |
| `audit` | Engagement or assessment cycle; the slug remains audit under role-specific labels. |
| `risk` | Risk register entry with likelihood, impact, ratings, treatment and owner. |
| `control` | Control library entry; SOX eligibility is literal sox_applicable=true. |
| `issue` | Finding or exception with classification, recommendation and management response. |
| `remediation` | Linked corrective action with owner, target/completion/verification dates and evidence. |
| `process` | Auditable process, scope decision and assessment. |
| `policy` | Internal policy with owner, framework, version and review dates. |
| `system` | System or third party; vendor records use system.vendor=true. |
| `fsli` | Financial statement line item and significance assessment. |
| `requirement` | Requirement with reference, framework, applicability and implementation status. |
| `personnel` | Person, reporting arrangement, responsibilities and supporting evidence. |

- Item relationships connect records; they are not RELATION fields.
- `suggest_change` proposes supported item/workflow changes for human
  approval. It is not the only write: `upload_document` stores bytes directly.
- DOCUMENT is a real field type holding one document per item/field. Populate
  it through upload_document after item creation, not an inline item value.
- A workflow is an instance attached to an item; its steps hold instructions,
  results, evidence, optional respondent forms and native approvals.
- FormAssignment requests inputs from a named non-executor. StepApproval
  records native sign-off. A form checkbox does not replace that approval.
- The field types are TEXT, TEXTAREA, RICHTEXT, NUMBER, DATE, DATETIME,
  SELECT, MULTISELECT, BOOLEAN, USER, USERS, DOCUMENT and JSON.
- A slug is a stable type identifier; item IDs identify actual records.
- Typed get_schema exposes field options and protected status definitions
  when present. DefaultStatus is an initial value, not the full vocabulary.
- authority_source, audit_universe_entity, audit_plan and the old named
  overlays are retired for this baseline. Preserve historical meaning; a
  migration into requirement requires explicit mapping and review.
- Legacy remediation_task descriptions do not prove that actions are only
  steps: current remediation items hold durable action data and their
  workflows hold execution. Legacy system_inventory_entry maps conceptually
  to system, subject to actual source and tenant schema.
- RELATION/RELATIONS and FILE are not current field types. Use item
  relationships and DOCUMENT respectively. Do not promise an automatic
  translation of legacy fields or records.

### `--diagnose` — error and symptom diagnosis

1. Dispatch `coach-troubleshooter` agent with the symptom and any
   pasted error text.
2. Agent searches docs for matching error patterns, schema-related
   issues, and common gotchas.
3. Agent returns a diagnosis:
   - Likely cause (with confidence: high, medium, low)
   - Proposed fix (commands to run, settings to check)
   - Doc citations
   - Confidence rationale
4. Present the diagnosis in the System Prompt's visible-turn shape.
   Ask the user if it matches what they observed.
5. If the user confirms and the fix is something coach can run (a
   sibling skill), tail-invoke it. Otherwise the user runs the fix
   manually.
6. If the user disconfirms or the agent confidence was low, offer
   to open a ticket via `/coach-ticket --category bug`. Pre-fill
   the ticket body with the diagnosis attempt and what was tried.

## Notes

- The docs snapshot's freshness is in `docs-snapshot/_snapshot.json`.
  If an answer references behavior that has changed since the
  snapshot, the user can flag it via `/coach-ticket`.
- Common `--howto` tasks tested: "add a custom field", "create an
  item type", "set up OAuth client", "import bulk data", "add a
  user as admin", "configure MCP". For tasks not covered by the
  docs, suggest `/coach-ticket` with category how-to.
- Common `--diagnose` patterns matched:
  - "plugin validation failed" → SKILL.md description patterns
    (angle brackets, hash sequences, bracketed-colon forms)
  - "schema mismatch" → tenant schema does not match an installed
    plugin's pre-flight requirements
  - "permission denied" → OAuth client or role configuration
  - "suggest_change returned validation error" → field type or
    options mismatch
- Every mode is read-only against Canvas — nothing here auto-fixes.
  In `--diagnose`, either the user runs the fix (or a sibling fix
  skill runs it), or the case escalates to `/coach-ticket`.
- For acronyms common in audit/SOX (SOC 2, ISO 27001, CC1, A.5.1),
  `--define` returns both the expansion and a one-line "used by"
  reference pointing at the relevant shared-core item type or
  field.
- The deprecated-term table is load-bearing. Operators who learned
  Canvas before the shared-core refactor will type old terms;
  `--define` must translate cleanly without sending them on a hunt.
- When a term is not in the cached vocabulary and not in the docs
  snapshot, surface that fact plainly — don't invent a definition.
