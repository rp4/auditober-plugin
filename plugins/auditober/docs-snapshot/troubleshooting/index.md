---
title: Troubleshooting
description: Symptom-by-symptom fixes for sign-in, access, workflow, form, agent/MCP, suggestion, and import issues.
---

Match your symptom to a fix below. Each entry names who resolves it, you, or an administrator, and links to more detail where it exists. Start with the section that matches your situation: sign-in, access, workflows, forms, agents and MCP, suggestions, or imports.

## Sign-In

Both symptoms below are quick to rule out yourself before you need to involve anyone else.

**Can't sign in at all**

Work through these in order:

1. Confirm you're using your tenant's correct URL.
2. Confirm your account is active, and try a private browser window to rule out a stale session.
3. If your organization signs in with single sign-on, confirm your email domain is on the administrator's allowed list, or that your account already exists: there's no open self-signup.

If none of these explain it, an administrator needs to check your account directly ([Users and access](https://docs.assureswarm.com/admin/users-and-access/)).

**Email and password sign-in is rejected**

Password sign-in is enabled per account, not for the whole tenant. Use single sign-on instead, or ask an administrator to enable password sign-in for your account.

## Missing Pages or Records

Each of these looks like a bug but is actually a permission boundary.

**A page is missing from my navigation**

You don't have page access to it, whether it's a system page or an item type page. Page access beyond the default set is granted individually, so a page you expect to see may simply not be turned on for your account yet.

**I can open a list but not a specific item, or the item is read-only**

This is item visibility or a view-only item permission, not a bug: access to an individual item can be narrower than access to its list.

**An item type disappeared entirely**

The item type behind it may have been deactivated rather than deleted.

All three are fixed by an administrator, not by you: see [Permissions](https://docs.assureswarm.com/concepts/permissions/).

## Workflows and Approvals

Approval sequencing and branch pruning explain most of the confusion here.

**I can't approve a step**

Check whether you are listed as an approver. Review levels only order the display; they do not block later reviewers from approving. If you should be an approver, ask an administrator to check the step's assignments and your access.

**A step won't move to complete**

Not all of its required approvals are in yet. Check with the remaining approvers before assuming something is broken.

**Steps I expected are gone after a decision**

A decision step can prune the branch that wasn't taken, and pruned steps are permanently removed from that workflow run. This is expected behavior, not an error: see [Workflows](https://docs.assureswarm.com/concepts/workflows/).

## Forms

Form problems are almost always about assignment state, not the form's content.

**A form I expected isn't in my Forms Inbox**

The assignment may have been revoked, or you already submitted it: only one assignment is active per person per step at a time. Ask whoever assigned the form to confirm its status.

**My file upload was rejected**

Uploaded documents are validated before they're accepted. Correct the file and re-upload it: see [Documents](https://docs.assureswarm.com/concepts/documents/).

## Agents and MCP

Most of these you can resolve yourself by reconnecting or adjusting the call; a few need an administrator to change access.

| Symptom | Likely Cause | Fix |
|---|---|---|
| `401` or authentication failed | The token expired (personal tokens last 30 days), was revoked, or was mispasted. | Generate a new token or reconnect: see [Connect an agent](https://docs.assureswarm.com/mcp/connect/). |
| Scope error on one tool | The token doesn't carry the scope that tool requires. | Re-authorize including that scope: see the scope table in [Reference](https://docs.assureswarm.com/reference/). |
| Tool result has `isError: true` | Input validation failed: commonly custom fields not nested under `data.fields`, a missing `targetId` on `update`, `delete`, `submit_form`, or `prune-branch`, or an action the target doesn't support. | Check the input shape in [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/). |
| `query_data` rejects the call | Only read queries are allowed, no mutations or subscriptions. | Rewrite the call as a query, see [query_data](https://docs.assureswarm.com/mcp/query_data/). |
| Query or response is too large | Queries cap at 64 KB; responses cap at 2 MB. | Narrow the selection, or request a `csv`/`jsonl` export instead. |
| Work lists come back empty, with a hint in the response | Scope degradation: commonly a missing `read:workflows` scope. | Not an error. Re-authorize with the missing scope if you need that data. |
| The agent sees or does less than the user expects | The connected user's own permissions are always the ceiling, however broad the token's scopes are. | Ask an administrator to review the user's access. |
| Tools don't appear in the client | The MCP URL is wrong (it must end in `/mcp`), or the client wasn't reloaded after connecting. | Recheck the URL and reconnect. |

Most agent errors trace back to one of three things: an expired or under-scoped token, oversized input, or the connected user's own permission ceiling.

## Suggestions

A suggestion never changes anything by itself: these symptoms are almost always about the review step, not a broken agent.

**An agent says it made a change, but nothing changed**

Suggestions only take effect after a person approves them: a successful call means the suggestion is pending review, not applied. Open the pending review yourself, or ask whoever owns the item to review it ([Reviewing suggestions](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/)).

**A suggestion seems stuck**

A stalled apply automatically returns the suggestion to `pending` so it can be reviewed again: nothing needs to be fixed behind the scenes.

**Approving a suggestion failed**

The target may have changed since the suggestion was proposed, so its recorded before-values are stale, or you lack permission for the change. Either way, reject it and ask the agent to re-propose against the current state.

:::tip[No need to escalate a stuck suggestion]
A suggestion that stalls in `processing` resolves itself back to `pending`. You don't need an administrator or Support to intervene: just reopen and review it.
:::

## Imports

Import failures are almost always about the data in the file, not the tenant.

**Some rows failed**

The import results report lists per-row failures. Fix those specific rows and re-run the import: configuration sections like item types and custom lists update in place rather than creating duplicates.

**Relation warnings**

A dangling relation means the referenced item type wasn't included in the file, or doesn't exist yet in the tenant.

**Values were rejected**

Use the stored option value, not the display label, for select and multiselect fields: the two aren't always the same string.

Bulk imports are run by administrators from the Bulk Import area: see [Imports and exports](https://docs.assureswarm.com/admin/imports-and-exports/).

## Asking for Help

Include what you were trying to do, the page or object name, the exact error message, and whether another user can complete the same action. That context lets an administrator or Support reproduce the problem instead of guessing. For anything you can't resolve yourself, use [Support](https://docs.assureswarm.com/support/).

:::caution[Never share credentials when asking for help]
Leave passwords, bearer tokens, OAuth client secrets, private keys, and sensitive document contents out of any support request: describe the symptom instead.
:::
