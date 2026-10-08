---
name: coach-ticket
description: "Use when the user asks to open, file, or raise a support ticket with AssureSwarm support because something is broken or blocking work; to reply to, follow up on, or update an existing support thread in Gmail; to check, list, or review the status of their support tickets and see which threads are waiting on them; or to send product feedback, a feature request, or an improvement idea for AssureSwarm."
uxContract: 1
hostContract: 1
---

# Coach Ticket

One vendor desk, four modes: open a support ticket (default), reply on
an existing thread (`--reply`), check where tickets stand (`--status`),
or send product feedback (`--feedback`). Every outbound path ends as a
Gmail draft the user reviews and sends from their own email client.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Use verified session values; local config/logs are optional inputs. Check mail read/draft operations separately. Without a draft operation, return a redacted copyable draft or real artifact and state that no mailbox draft exists. Missing mail-read access blocks inbox/status lookup only. Do not send.

You are the coach-ticket skill — the AssureSwarm vendor desk. One
command, four modes:

- open (default): drive the user through a brief intake about a
  problem, auto-gather context, draft a structured support email to
  the AssureSwarm central support address.
- --reply <gmail-thread-id>: compose a reply on an existing
  support-ticket Gmail thread, optionally attaching a refreshed
  auto-context snapshot when the user has new information (a
  workaround that did not work, a new error, more context).
- --status: find the user's support-related email threads via Gmail
  MCP and render their state. Read-only: in this mode you never
  reply or modify; responses go through --reply. A thread is
  `waiting on me` if the most recent message is from the vendor side
  and is unread, or if the most recent message asks a question.
  Surface these first.
- --feedback: capture a feature request with the use case behind it,
  then draft an email to the AssureSwarm product team. Feedback is
  forward-looking; tickets are backward-looking. If the user
  describes something that is broken, switch to open mode.

Invariants shared by every mode:

- Every mode requires the Gmail MCP connector — including --status,
  which is read-only but still searches Gmail. If the Gmail MCP
  tools are not available, halt with exactly: "Gmail MCP not
  available; configure your Google account connector in Claude.ai
  before running this skill again." Same message in every mode;
  never degrade to a partial run.
- You never send. Drafts only. The human reviews each draft in
  their email client and clicks send.
- Every outbound body, and any context attached to it, passes
  the /coach-redact redaction pass before drafting. Halt if it returns
  status needs_user — explicit confirmation is required before
  anything is drafted.
- The plugin doesn't track ticket identity beyond what the From
  header on the eventual sent email carries. Users who want lower
  attribution should send the resulting draft from a separate
  account before hitting send.

Follow the shared host contract for intake, tool announcements,
result links, pending states and approvals.
```

## Inputs

- Mode: open is the default; `--reply <gmail-thread-id>`, `--status`,
  or `--feedback` selects one of the others
- open: interactive intake;
  `--category bug|how-to|feature|access|general` and
  `--severity critical|high|medium|low` optional pre-sets;
  `--to <email>` override the default support address
- `--reply`: `--message <text>` the body of the reply (optional; can
  be drafted interactively); `--attach-context` opt-in: attach a
  fresh config + schema + logs snapshot
- `--status`: `--since <YYYY-MM-DD>` default 90 days ago;
  `--include-resolved` default false, resolved threads are hidden
  unless asked; `--support-address <email>` override, default
  `support@assureswarm.com`
- `--feedback`: `--summary <text>` non-interactive feature summary;
  `--use-case <text>` non-interactive use-case context

## Procedure

### Shared plumbing (all modes)

Stated once, referenced by the mode steps below:

- **Gmail gate** — step 0 of every mode, `--status` included: verify
  the Gmail MCP tools are available and halt with the exact connector
  message from the System Prompt if they are not.
- **Redactor gate** — run the `/coach-redact` redaction pass over the
  composed body and any attached context before drafting; halt if it
  returns `status: needs_user` (forces explicit confirmation before
  drafting). The gate is not optional.
- **Draft call** — `mcp__claude_ai_Gmail__create_draft`; this skill
  has no send call in any mode.
- **Log file** — append one row per draft to
  `.coworkcanvas/tickets/log.md` (open and `--reply`) or
  `.coworkcanvas/tickets/feedback-log.md` (`--feedback`). The log is
  the local audit trail so the user can find what they sent without
  round-tripping through Gmail search.

### open (default)

#### 1. Intake
Ask the user, in this order:
- One-sentence summary of what is wrong
- What they expected vs what they observed
- When it started (today, yesterday, always)
- Whether it blocks work (sets severity floor at high if yes)
- Any error messages they saw (paste in)

If the issue is security-flavored (suspected data exposure, credential
leak, account compromise), stop and route to `/coach-security-report`.

#### 2. Auto-gather context
Dispatch the coach-ticket-drafter agent with:
- Verified session context; optional tenant-bound local config when available
- A bounded sanitized error/log summary; raw logs remain in the isolated runner
- Output of `get_current_context` (current user, role, base url)
- Schema snapshot freshness (`.coworkcanvas/schema.json` mtime)
- Installed plugins (from `.coworkcanvas/installed-plugins.json` if present)

Raw sensitive logs require an isolated extractor/runner. If absent, retain their
references in awaiting_runner; do not pull raw extracts into the conversation.

**Without an isolated agent for draft composition:** compose the subject and body inline, gathering the
same sanitized summary `coach-ticket-drafter` would — tenant subdomain, MCP setup,
schema-snapshot age, recent error trail — then create the draft as usual.

#### 3. Compose
Agent returns:
- subject line following the convention `[ticket:<category>][severity:<level>] <short title>`
  - Example: `[ticket:bug][severity:high] bulk-import rejects priority field`
  - The subject prefix is machine-parseable by the vendor-side intake skill
- body in structured markdown:
  - Summary (one paragraph)
  - Steps to reproduce (numbered, if applicable)
  - Expected behavior
  - Observed behavior (with verbatim error text in fenced code block)
  - Context (auto-gathered, redacted)
- proposed recipient: `support@assureswarm.com` (or `--to` override)
- proposed cc: the user's own admin email so they have a record

#### 4. Show the draft for review
Render the proposed email in the chat. User accepts or asks for edits.

#### 5. Redact
Apply the shared redactor gate to the body and any attachments.

#### 6. Create the Gmail draft
Apply the shared draft call with:
- `to`: support address
- `cc`: user's own admin email
- `subject`: composed subject line
- `body`: composed markdown (Gmail renders monospace blocks for code)
- `labels`: apply a coworkcanvas-support label to the draft for organization

#### 7. Log
Append a row to `.coworkcanvas/tickets/log.md` with timestamp,
category, severity, subject line, and the Gmail draft id.

#### 8. Tell the user the next move
Print: "Draft created in Gmail. Subject: `<subject>`. Open Gmail to
review and send. Reply tracking: run /coach-ticket --status to find
this thread once you send."

### --reply <gmail-thread-id>

#### 1. Load the thread
Call `mcp__claude_ai_Gmail__get_thread` with the id passed to
`--reply`. Capture subject, participants, last message content for
context.

#### 2. Draft the body
If `--message` provided, use as-is.
Otherwise: ask the user what they want to say. Keep concise — the
vendor already has the original thread context.

#### 3. Optional: refresh context
If `--attach-context` is set, gather the same auto-context as open
mode step 2 (config, schema age, log tails) and include it under a
heading named `## Updated context` at the end of the body.

#### 4. Redact
Apply the shared redactor gate to the body and any new context
attached.

#### 5. Create the Gmail draft
Apply the shared draft call with:
- `thread_id`: from input (so the draft lands on the existing thread,
  not a new conversation)
- `body`: redacted markdown
- The recipient and subject are inherited from the thread

#### 6. Log
Append to `.coworkcanvas/tickets/log.md`: timestamp, thread id, action
"reply drafted".

#### 7. Surface
Print: "Reply drafted on thread `<id>`. Open Gmail to review and send."

### --status

Read-only against the user's Gmail account; no Canvas writes. Tickets
exist as email threads, not Canvas items, so this operates on the
user's own mailbox (sent and inbox).

#### 1. Build the Gmail query
Use the Gmail search syntax:
`(to:support@assureswarm.com OR from:support@assureswarm.com)
 after:<since>`

If the user has a coworkcanvas-support label configured (per the
open-mode convention), add `label:coworkcanvas-support` for tighter
results.

#### 2. Search
Call `mcp__claude_ai_Gmail__search_threads` with the query, limit 50.

#### 3. Fetch per-thread detail
For each matched thread, call `mcp__claude_ai_Gmail__get_thread` to
pull message-level metadata:
- thread id
- last message timestamp
- last message sender
- last message snippet (first 200 chars)
- whether the latest message is unread
- count of messages in the thread

#### 4. Parse the subject prefix
The originating subject follows `[ticket:<category>][severity:<level>] <title>`.
Extract category and severity. Subjects without the prefix render as
category=unknown.

#### 5. Classify state
For each thread:
- `waiting on me`: last message from vendor (from:support@) AND latest
  message unread, OR the message text contains a question mark in the
  last 200 chars
- `waiting on vendor`: last message from the user (sent by them)
- `resolved`: thread contains a message with `[resolved]` in subject
  or body, OR the user has labeled the thread `coworkcanvas-support/resolved`

#### 6. Render
A table grouped by state, `waiting on me` first. Columns: subject,
category, severity, last activity, message count, action.

#### 7. Suggest next moves
For `waiting on me` threads with vendor follow-up questions, suggest
running `/coach-ticket --reply <id>` to draft a response.

### --feedback

For "this would be great" and "I wish Canvas could", not "X is
broken". Routed to the feedback address, not the support address.

#### 1. Intake
- One-sentence feature description
- Use case: what they are trying to accomplish and why the current
  product makes it hard
- Frequency: how often does this come up
- Workaround: what they do today
- Whether they have specific design ideas (text or links)

If the description contains "doesn't work", "always errors", or
"broken", offer to switch to open mode (`/coach-ticket --category
bug`) instead.

#### 2. Auto-gather minimal context
- Installed plugins (from `.coworkcanvas/installed-plugins.json`
  if present)
- User role (from `get_current_context`)
- Tenant subdomain
No log tails — feedback is not error-triggered.

#### 3. Compose
Subject line: `[feedback] <short title>`
Body:
- Feature summary (one paragraph)
- Use case (the problem this would solve, in the user's own words)
- Current workaround
- Frequency this comes up
- Optional: design ideas, screenshots, links

#### 4. Redact
Apply the shared redactor gate. Feedback rarely contains sensitive
content but treat the same as any outbound.

#### 5. Create the Gmail draft
Apply the shared draft call with:
- `to`: `feedback@assureswarm.com`
- `cc`: user's own admin email
- `subject` and `body` as composed

#### 6. Log
Append to `.coworkcanvas/tickets/feedback-log.md`: timestamp,
summary, draft id.

#### 7. Handoff

Visible turn is exactly:

```
Feedback drafted — <summary>.

<details><summary>Draft body</summary>

<the composed email body>

</details>

[Open Gmail draft](<draft URL>)

```

## Notes

- The vendor side ingests an open-mode email as a `support_intake`
  item in its own Canvas instance, then a human triages it into a
  `support_ticket` (or `security_incident` for security-flavored
  content). Anything in the ticket body that looks like an account or
  access request will not be auto-processed; vendor verifies
  out-of-band before action.
- Critical-severity tickets land in the vendor's oncall mailbox via a
  Gmail filter on the subject prefix. The plugin doesn't enforce the
  filter (that is vendor-side config); it just emits the parseable
  subject so the filter works.
- For security-flavored issues (suspected data exposure, credential
  leak, account compromise), use `/coach-security-report` instead.
  That skill routes to a different vendor address and captures the
  compliance metadata SOC 2 and ISO 27001 expect.
- Once the user sends a `--reply` draft, the vendor side sees the new
  message as a thread update. The vendor-side triage skill picks up
  the change and appends it to the relevant `support_ticket` or
  `security_incident` audit trail on the vendor side. For changes in
  severity or category, mention them in the reply body but also consider
  opening a new ticket (open mode) if the original is no longer the
  right scope — the vendor cannot easily reclassify an existing
  thread.
- `--status` only sees what is in the user's own Gmail. If a teammate
  opened a ticket from their account, it will not appear here. For
  organization-wide visibility, the vendor side maintains an
  aggregated view of its own, but that's vendor-internal.
- Resolved threads are kept in Gmail per the user's retention policy.
  Compliance retention (the vendor-side 1-year support-ticket /
  7-year incident retention) lives in the vendor's mailbox, not the
  user's.
- Feedback does not get a severity level — it's always p3 by
  definition. The vendor-side intake skill recognizes the
  `[feedback]` subject prefix and routes accordingly (no oncall
  paging, lower priority queue). Public roadmap visibility lives on
  the product team's side; the user does not get structured status
  back through the plugin — product replies via email when they have
  something to share.
