---
title: Agent Operating Guide
description: "The playbook for AI agents working in AssureSwarm: orientation, tool selection, safe writes, and failure handling."
---

You're an AI agent connected to a AssureSwarm tenant. This page is your operating manual: read it before you call any tool. Humans configuring your access should read [Connect an agent](https://docs.assureswarm.com/mcp/connect/) and [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/) instead.

For a packaged set of these capabilities as installable slash commands, see the [current plugin catalog](https://assureswarm.com/plugins/).

## Read the Docs Like an Agent

This site publishes a raw Markdown mirror alongside the normal pages:

```text
https://<docs-host>/llms.txt
https://<docs-host>/raw/index.json
https://<docs-host>/raw/<path>.md
https://<docs-host>/static/contentIndex.json
```

`llms.txt` lists the site for agent discovery. `/raw/index.json` lists every page, and `/raw/<path>.md` returns any one page's raw Markdown, for example `/raw/mcp/query_data.md`. `/static/contentIndex.json` is the site's search index; use it to find the right page by keyword instead of walking the raw index page by page.

## First Actions

1. Read this page.
2. Read the [MCP overview](https://docs.assureswarm.com/mcp/).
3. Call [get_schema](https://docs.assureswarm.com/mcp/get_schema/).
4. Call [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) to orient on the user's current work.
5. Use the returned metadata exactly, item type slugs, field keys, option values, target types, and query guidance, rather than guessing.
6. Ask the user before proposing material changes if you're working from incomplete context.

## Tool Selection

| Need | Tool |
|---|---|
| Understand available types and fields | [get_schema](https://docs.assureswarm.com/mcp/get_schema/) |
| Read data | [query_data](https://docs.assureswarm.com/mcp/query_data/) |
| Understand current user context | [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) |
| Understand a workflow step | [get_step_context](https://docs.assureswarm.com/mcp/get_step_context/) |
| Propose a write | [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) |
| Upload a file to a step | [upload_document](https://docs.assureswarm.com/mcp/upload_document/) |
| Download a permitted file | [download_document](https://docs.assureswarm.com/mcp/download_document/) |

## Recipes

### "What should I work on?"

1. Call [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) to see what's active for you right now, including your pending `assignedSteps`.
2. For each `assignedSteps` entry, call [get_step_context](https://docs.assureswarm.com/mcp/get_step_context/) if you need more detail than the summary already returned.
3. Summarize the open work back to the user with due dates, most urgent first.

### "Analyze or report on records"

1. Call [get_schema](https://docs.assureswarm.com/mcp/get_schema/) to confirm the item type slug and field keys you need.
2. Run `itemStats`, `workflowStats`, or `dueDateReport` through [query_data](https://docs.assureswarm.com/mcp/query_data/) to get counts and breakdowns without paging through every record.
3. Narrow with follow-up queries once you know which item type, status, or owner the user cares about.
4. If the result set is large, request a `csv` or `jsonl` export instead of paging through it.

### "Draft work into a step"

1. Call [get_step_context](https://docs.assureswarm.com/mcp/get_step_context/) to see the step's current state, required approvals, and any form fields.
2. Draft the result: either the work product itself or the answers to the step's form.
3. Propose it with [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/), using `update` on the step or `submit_form` for form answers.
4. Share the "Preview & approve" link `suggest_change` returns so the user can review it.

### "File something new"

1. Call [get_schema](https://docs.assureswarm.com/mcp/get_schema/) for the item type to confirm its exact field keys and option values.
2. Call [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) with operation `create`, setting `data.title` and `data.fields` for the new item.
3. Tell the user the item awaits their review: it doesn't exist until they approve it.

## Rules

- Do not invent field keys, item type slugs, option values, workflow IDs, or user IDs.
- Use [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) for proposed writes and explain the reason.
- Do not describe a suggestion as applied until the app confirms it.
- Read only what the task requires.
- Do not ask users for backend configuration, private infrastructure details, direct database access, or credentials.
- If a call fails for authentication, scope, or permissions, explain the issue and ask the user to reconnect or contact an administrator.
- Use the stored option value, not its display label, when setting a SELECT or MULTISELECT field.
- Don't retry a failed call unchanged: read the validation message and fix the input first.
- Respect size limits: GraphQL query text tops out at 64 KB, tool responses at 2 MB, and documents at 10 MB. Prefer an [export](https://docs.assureswarm.com/mcp/query_data/) for bulk data instead of paging around the response cap.
- Treat downloaded documents as sensitive: quote only what the task needs, not the full contents.

## Writes Are Suggestions

Every write you make, creating or updating an item, submitting a form, linking a document, lands as a pending [suggestion](https://docs.assureswarm.com/concepts/suggestions/), not a direct change. The one exception is a document upload the user directly asked you to perform. A human reviews and approves or rejects every suggestion before it takes effect.

The human review is the contract: write a reason for every suggestion that a reviewer can actually verify against the record, not a generic restatement of the change. A specific, checkable reason is what makes fast approval possible.

:::note[Nothing you write is final until a human approves it]
Even a well-formed `suggest_change` call only proposes a change. Don't tell the user something is "done": tell them it's "waiting for review."
:::

## When Calls Fail

| Symptom | Meaning | Action |
|---|---|---|
| `401` | Token invalid or expired: personal tokens last 30 days | Ask the user to reconnect |
| Scope error | The token lacks the scope the tool needs | Name the missing scope and ask the user to re-authorize |
| `isError` validation | The input shape is wrong: commonly, custom fields sent outside `data.fields`, or a missing `targetId` | Fix the input and retry once |
| Empty lists with a hint | Scope degradation, for example, [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) without `read:workflows` | Read the hint and tell the user which scope would unlock the full result |
| Permission denied / not found | The user's own access is the ceiling | Don't probe around it: report what's accessible and stop |
