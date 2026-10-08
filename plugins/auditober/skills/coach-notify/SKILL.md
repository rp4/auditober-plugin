---
name: coach-notify
description: "Use when the user asks to prepare a stakeholder notification, nudge, reminder or distribution list about an AssureSwarm item or step. Resolve recipients from verified tenant fields and available directories, redact the draft and create it through the actual mail-draft operation when available. Without one, return copyable text or an artifact; never claim that a draft was sent."
uxContract: 1
hostContract: 1
---

# Coach Notify

One skill for both halves of outbound comms. **dl** replaces "paste
names from the org chart into the To: line" with a structured roster
pulled from authoritative sources; **draft** replaces "open Outlook,
type a paragraph referencing the AssureSwarm record, copy-paste the link"
with a one-line invocation. The modes compose: build the roster, then
draft to it.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Reuse provided recipients/mode. Verify directory and mail-draft operations. Missing directory access retains unresolved recipients; missing draft creation returns redacted copyable text and no mailbox-draft claim. Scheduling needs a successful real scheduler result. Draft mode never sends.

You are the notify skill — the plugin's one outbound-comms primitive.

Two modes:

  dl     Assemble the right recipients for a AssureSwarm item's
         distribution from authoritative sources, deduplicate, and
         return a structured roster the user can paste into any
         email client or feed straight into draft mode.
  draft  Given a AssureSwarm item (a doc request form on a workflow Step,
         a workflow Step with an open question, an issue update),
         compose a notification email draft.

Mode selection: --dl <spec> alone runs dl mode; composition flags
(--template, --via, --recipients) run draft mode; --dl combined with
composition flags runs dl first and feeds the roster into draft. If
the mode is not discernible from the invocation, ask for the missing input to
pick one.

dl mode:

  1. Query the item's verified team and stakeholder fields via
     coach-query-data.

  2. Decide the role set from the --dl spec:
       - board: board + audit-committee members, board secretary,
         CAE, executive sponsors (CEO/CFO)
       - audit-committee: AC chair, AC members, CAE, lead auditor,
         audit committee secretary
       - management: business owner(s) of in-scope processes,
         finance controller (if SOX), CRO/CCO, lead auditor
       - broad: management + audit team + portfolio manager + AC
         chair
       - an explicit comma-separated role list, e.g.
         cco,gc,external-regulator-liaison — each token is one role
         to resolve
       - custom: gather the roles from the user

  3. For each role, look up the person in priority order:
       a) Live custom-field assignments on the item
          (audit_committee_chair, business_owner, cae, ...)
       b) Workday directory lookup by role title (if Workday MCP
          configured)
       c) Outlook directory lookup (if Outlook MCP configured)
       d) Otherwise: surface as unresolved

  4. Dedupe by email.

  5. Return: [{ name, email, role, source }] plus an
     unresolved: [...] list of roles you could not fill.

  For SOX-relevant items in a board or audit-committee distribution,
  verify the AC chair is included and warn if not (the AC chair MUST
  be on the report distribution per most firms' SOX procedures).

  dl mode is read-only over the directory. It never modifies Canvas,
  Workday, or Outlook records. Lookups and dedupe only — no judgment
  calls on whether a person should be excluded.

draft mode: compose the email draft with:

- Subject line that includes the item type and short title
- Body that summarizes the ask in 2-3 sentences
- A clickable Canvas link
- The expected response action
- The due date

Never send. The output is a draft that the user reviews and sends
manually (via Gmail draft, Outlook draft, or copy-paste). The
literal send_message MCP tool is excluded from this skill's tool
surface in both modes; create_draft is the only email-MCP call it
ever makes.

Every draft is outbound content: run it through the /coach-redact
redaction pass before delivery, exactly like coach-ticket does. Halt on
`status: needs_user` — never deliver an unredacted draft to any
channel, including the clipboard file.

The skill addresses tenant-discovered items, including the eleven core types:
audit, risk, control, issue, remediation, process, policy, system, fsli,
requirement and personnel. Native workflow steps use get_step_context.

UX contract (see ../../references/host-capabilities.md). Before each necessary question
(mode pick, custom roles, an unresolved role, a missing due date),
your entire turn is one sentence naming the field. Option
description carries the explanation; the question label is one
short clause. Before each tool call, your entire visible turn is
one short sentence naming the action.

Output discipline. Closing pleasantries and recaps are not
permitted. dl mode ends with the CSV path plus the recipient count
(and the unresolved roles, if any). draft mode ends with the draft
summary (recipient count + delivery channel + draft location) plus
the redaction report path when patterns were auto-removed.
```

## Modes

### dl — build the distribution list

- `--item <item-id>` — required; the item whose distribution is being
  built (an audit, an issue, a report or attestation item)
- `--dl <spec>` — required; a named role set (`board`,
  `audit-committee`, `management`, `broad`), an explicit
  comma-separated role list (`cco,gc,external-regulator-liaison`), or
  `custom` (roles gathered interactively through available intake)
- `--out <path>` — default: print to stdout + write to
  `.coworkcanvas/dls/<item-slug>-<spec>.csv` (with a sibling `.md`
  markdown table)

### draft — compose the email draft

- `--item <item-id>` — required, what's being notified about; may
  also be a Step id when prefixed `step:<id>`
- `--recipients <user-id|email,...>` — optional; if missing, derive
  from the item's team / watchlist / Step watchers, or pass
  `--dl <spec>` to build the roster via dl mode first
- `--template default|urgent|reminder` — default: default
- `--via gmail|outlook|clipboard` — default: clipboard (the user
  pastes wherever they like)

## Procedure

### dl mode

1. Query the item's team and stakeholder fields via
   `coach-query-data`.
2. Walk the role set for the chosen spec (named set, explicit
   comma-separated list, or custom roles gathered from the user).
3. For each role, resolve the person via the priority chain:
   Canvas custom fields → Workday → Outlook → unresolved.
4. Dedupe the resolved set by email.
5. Render as CSV (one row per recipient: name, email, role, source)
   and as a markdown table the user can paste into a draft.
6. Surface anyone in the roster whose email lookup failed or whose
   role is ambiguous — ask for the missing input to resolve, or leave them on
   the `unresolved` list.
7. For SOX-relevant items in a `board` or `audit-committee`
   distribution, verify the AC chair is included; warn if not.
8. Save to `--out` and print the count.

### draft mode

1. Resolve the target. If `--item` is `step:<id>`, fetch the Step
   via `get_step_context` and pull its parent item for additional
   context. Otherwise `query_data` against the item with the
   notification-relevant fields (`lead`, `team`, `watchlist`, due
   dates).
2. Resolve recipients:
   - If `--recipients` supplied, use those.
   - If `--dl <spec>` supplied, run dl mode first and use its
     deduplicated roster.
   - Else: union of `lead` + `team` + `watchlist` on the parent
     item, plus the Step's watchers / assignee when relevant. For
     complex resolution (role-based lookups, Workday/Outlook
     directory queries), that is dl mode's job — run it.
3. Compose the draft using the selected template:
   - `default`: cordial, summary + ask + link + due
   - `urgent`: same content with `Urgent — ` subject prefix and
     bold the due date
   - `reminder`: implies a prior message; subject `Reminder: ...`
     and body opens with "Following up on..."
4. Redact: run the `/coach-redact` redaction pass over the draft body
   (subject + body + any quoted item content). If it returns
   `status: needs_user`, surface the flagged spans and stop until the
   user resolves them. Auto-removed patterns proceed silently — the
   redaction report path goes in the final summary. The gate is not
   optional.
5. Deliver per `--via`:
   - `gmail` or `outlook`: Discover the installed connector's draft
     creation tool and read its input schema. Match the provider and
     mailbox, then pass recipients, subject and body using that schema.
     Tool names vary by host; never guess a namespace or substitute a
     send tool. Only call a capability that saves a draft without sending.
     If it is unavailable, return the redacted copy for the user to paste
     and state that no mailbox draft was created.
   - `clipboard`: return the redacted subject, recipients and body as
     copyable text. If a writable filesystem is available, also save
     `.coworkcanvas/drafts/<item-slug>-<date>.md` and report that path.
   Confirm the tool returned a draft ID or location before claiming the
   mailbox draft exists. Never send or treat draft creation as permission
   for later outreach.

## Notes

- The skill carries no send tool; the literal `send_message` MCP tool
  is excluded from its tool surface. Drafts only — in both modes, the
  user hits send.
- Redaction is not optional: stakeholder emails quote Canvas content
  to external parties (auditees, process owners, regulators), so the
  same `/coach-redact` gate that protects exports and support tickets
  runs here. Skills and workflow steps that layer on top (e.g. report
  socialization, `/coach-render-package` packaging) inherit the gate
  by delegating composition to this skill.
- The modes compose. For mass notifications (more than 5 recipients),
  run dl mode to build the recipient list first, then draft to it —
  either in one invocation (`--dl <spec> --via outlook`) or by
  passing `--recipients` from the saved CSV.
- `/coach-render-package` delegates its distribution step here: after
  packaging, it invokes dl mode (`--dl <spec>`) so the rendered
  package lands with a ready roster.
- `/coach-workflow-scan` pairs from the other side: its sweep mode
  classifies step status and names who to nudge; draft mode writes the
  nudge to that named user.
- The typical document-request pattern — create the request form on a
  Step, then immediately notify the auditee — is operated by the
  `audit-engagement-lifecycle` workflow's document-request steps,
  which hand the notification to this skill's draft mode.
- dl mode is read-only over the directory. It never modifies Canvas,
  Workday, or Outlook records.
- For SOX-relevant projects, ensure the audit-committee chair is in the
  `board` / `audit-committee` distribution. The agent verifies this;
  surface a warning if missing.
- Supersedes the two audit-domain comms skills (the stakeholder
  notifier and the DL builder); both are now modes of this one
  generic primitive, so the redaction gate lives in exactly one
  place.
- Historical context: earlier versions of the notify path referenced
  a `workstep` item type for the "Step with an open question" case.
  That type has been removed — Steps are platform entities reached
  via `get_step_context`.
