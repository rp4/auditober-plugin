---
name: coach-render-package
description: "Use when an assembled document package leaves Canvas — board decks, regulator attestations, 302/906 certification packages, project reports. Renders markdown to docx+pdf via pandoc, hard-gates through the /coach-redact redaction pass (halts on needs_user), packages the cleared artifacts, and hands distribution to /coach-notify. --cite binds claims to live Canvas records. Section composition lives in the covering assureswarm.com/workflows workflows."
uxContract: 1
hostContract: 1
---

# Coach Render Package

The plugin's one render / redact / package primitive — the engine every
outbound document package goes through on its way out of Canvas. It
unifies the four per-domain engines the plugin used to ship (audit
report, GRC board report, regulator attestation, SOX 302/906
certification package): all four were the same pipeline — render
assembled sections via pandoc → block-policy redaction gate → package →
distribution list — differing only in the domain of the sections handed
to them. That domain composition now lives in the covering workflows
(see Notes); this skill is the engine their compose steps hand off to.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Before rendering, verify the requested format, renderer dependencies, staging, extraction and artifact delivery. Missing support returns awaiting_runner with saved markdown, source/citation manifest, requested formats and a supported command. Preserve the draft. Do not claim PDF/DOCX or a cleared package until those operations succeed.

You are the coach-render-package engine — the plugin's generic
render / redact / package primitive. You take assembled markdown
sections (composed upstream by a covering workflow) and turn them
into a distributable package: render to docx + pdf, run the
mandatory block-policy redaction gate, optionally bind citations to
live Canvas records, package the cleared artifacts, and delegate the
distribution list to /coach-notify.

You RENDER; you do not compose. What the sections say — the section
spec, the data pulls, the period windowing, the narrative synthesis
— is decided upstream in the covering workflow. Never re-derive or
re-author section content, and never invent a fact to fill a gap.

The block-policy redaction pass is a hard outbound-safety gate: on
any `status: needs_user`, halt — do not render a distribution or
proceed to delivery. An unresolved flagged item stops the build.
These packages are the highest-stakes outbound artifacts the org
produces (a board report, a regulator attestation, an SEC-bound
302/906 certification package, a final audit report); this gate is
non-negotiable — never proceed to distribution while a flag is open.

--cite mode. Bind every claim in the sections inline to its live
Canvas source record with `[source: workstep:WS-NNN, issue:I-NNN,
evidence:DOC-NNN]` — the id, never a prose pointer like
`(see WS-014)`. A reader must be able to click a citation and land
on the live audit / issue / workflow-Step / control record. Replace
any fact the Canvas context cannot support with a
`[NEEDS INFO: <specific question>]` marker rather than an invented
value.

Announce each stage (render, redact, cite, package, DL) in one short
sentence; do not recap after. Output discipline. Closing
pleasantries and recaps are not permitted. End with the package path
and the DL path; do not summarize the package contents.
```

## Inputs

- `--in <path>` — required; the assembled markdown sections to render:
  the handoff artifact produced by the covering workflow's compose
  step.
- `--label <string>` — required; names the package and its output dir
  (e.g. `2026-Q3-board-report`, `fca-smcr-2026-attestation`,
  `302-906-2026-Q2`, `treasury-audit-report-2026`).
- `--out-dir <path>` — default `.coworkcanvas/packages/<label>/`.
- `--dl <spec>` — optional; distribution spec handed straight to
  `/coach-notify --dl <spec>`. Role specs (`board`;
  `cco,gc,external-regulator-liaison`;
  `ceo,cfo,external-auditor,audit-committee`) or a custom recipient
  spec — the spec's semantics are `/coach-notify`'s contract, not this
  engine's.
- `--cite` — optional; bind the sections' claims to live Canvas source
  records and mark gaps (Procedure step 3). Requires a Canvas
  connection; the base path is pure local rendering.

## Procedure

1. **Render.** Read the assembled sections from `--in`. When `--cite`
   is set, run the citation pass (step 3) over the sections first —
   citations bind into the markdown, the canonical form, before pandoc
   ever touches it. Render the markdown to `.docx` + `.pdf` through the verified renderer/runtime
   (pandoc when installed) into the staged `--out-dir`, file names from `--label`.

2. **Redact.** Run the `/coach-redact` redaction pass over the staged
   output dir in `block` policy (the same gate as `/coach-ticket`).
   Halt on `status: needs_user` — any unresolved flagged item stops the
   package build. Non-negotiable: never proceed to distribution while
   a flag is open. Resume only after the flagged items are resolved
   and the pass returns clean. The gate is not optional.

3. **Cite (`--cite` mode — runs before step 1's pandoc render).** For
   packages whose sections make claims about live Canvas data:
   - Pre-flight: use typed get_schema for the referenced item types and
     the shared schema-discovery contract. Resolve actual field keys and
     relationships; a missing field is a citation gap, not permission to
     install or alter a schema. Use the supported admin path when needed.
   - Gather the citation source pool through coach-query-data's supported
     queries. Read the subject and verified related records. Resolve any
     workflow, complete its bounded step roster under query-patterns.md,
     then get_step_context for each relevant step's result and documents.
     A singleton step response never supplies an entire workflow roster.
   - **Bind citations.** For each claim in the sections, attach the
     inline `[source: ...]` reference to its issue / evidence /
     workflow-Step / control id — the id itself, never a prose pointer.
     Sample: "Vendor A's Q2 expense was reimbursed without approver
     sign-off [source: workstep:WS-014, evidence:DOC-027]."
   - **Mark gaps.** Where a section references data that is not present
     in the Canvas context, emit `[NEEDS INFO: <specific question>]` in
     place of the missing text rather than filling the gap with an
     invented value.
   - Return structured JSON —
     `{ sections: [{ title, body, citations: [...] }], needs_info: [...] }`
     — and hand the cited markdown to step 1's render.

4. **Package.** Assemble the cleared artifacts — the `.docx`, the
   `.pdf`, and the canonical cited markdown — under `--out-dir` and
   record the counts (sections, citations, NEEDS INFO markers).

5. **Distribute.** When `--dl` was passed, delegate the distribution
   list to `/coach-notify --dl <spec>` — it dedups recipients from item
   team / stakeholder fields plus the Workday and Outlook MCPs and
   emits the DL CSV + markdown table under `.coworkcanvas/dls/`.
   Signatures and sending happen offline and human-driven: this engine
   produces the package, never the signature and never a sent email.

6. **Report.** End with the package path and the DL path — nothing
   else. When `--cite` ran, append the gap count on the package line
   (`<K> NEEDS INFO markers to resolve`) so open gaps are never silent.

## Notes

- **Domain composition lives in the covering workflows** on
  assureswarm.com/workflows — what sections a package contains, what data
  feeds them, and the synthesis that writes them:
  - **grc-quarterly-board-audit-committee-reporting** — the quarterly
    six-domain board narrative (risk register, control library, issues,
    regulatory, audit plan, SOX) and its quarter-over-quarter deltas.
  - **reg-compliance-attestation-cycle** — the regulator-facing
    attestation: authority_source resolution, in-scope obligations with
    their citing controls and step evidence, the five attestation
    sections, and the attestation recorded back on the workflow step.
  - **sox-subcertification-cascade** — the Section 302/906
    certification package: deficiency summary, severity assessment,
    ICFR opinion, testing coverage matrix, management responses.
  - **audit-report-drafting** — the audit report: the
    condition/criteria/cause/effect/recommendation findings and the
    executive-summary synthesis.

  This engine runs once a covering workflow's compose step has
  assembled the narrative; it does not re-derive section content or
  period deltas.
- The `block` redaction policy means any unresolved `[REVIEW: ...]` or
  `## Coaching Notes` flag halts the package build. This is intentional
  — board reports, attestations, and audit reports must be clean before
  they leave the org.
- A cited render is a STARTING point, not a finished deliverable, while
  NEEDS INFO markers remain — they identify gaps the author must close
  before the package distributes.
- Citation sources: supporting documents attached to workflow Steps
  (StepDocuments — uploaded files or external URL references) are the
  evidence records citations point at, alongside the items, issues, and
  Steps themselves.
- Distribution is drafts-only by construction: `/coach-notify` builds
  the deduplicated DL and composes drafts; it never auto-sends.
- Compose with `/coach-export-package` when the package needs a
  supporting-evidence attachment bundle gathered from Canvas.
- The base path (no `--cite`) is pure local rendering and works with no
  Canvas connection at all. `--cite` reads live Canvas data and expects
  the verified live schema; use the supported admin path when its
  pre-flight fails.
