---
title: Reference
description: Glossary, statuses, field types, scopes, limits, and other exact values for AssureSwarm users and agents.
---

This page is a lookup: exact terminology, statuses, field types, scopes, and limits used across AssureSwarm. It favors precision over explanation, for the ideas behind these terms, start with [Concepts](https://docs.assureswarm.com/concepts/).

## Glossary

Definitions here match [Concepts](https://docs.assureswarm.com/concepts/); read that page for fuller explanations.

| Term | Meaning |
|---|---|
| Agent | An AI assistant or integration that connects to AssureSwarm through MCP or GraphQL to read data and propose changes. |
| Allowed sign-in domain | An email domain an administrator has listed as permitted for single sign-on, so a new account can provision on first sign-in. |
| Approver | A user assigned to decide on a step's approval, at a specific review level. |
| Custom list | An administrator-managed set of option values that a select or multiselect field can draw from. |
| Dashboard | A built-in read-only page of tiles, charts, and tables over tenant data; Workflow Runs and Workflow Coverage take their subject from the URL. |
| Decision | A workflow branch point whose outcome determines which subsequent steps apply. |
| Field | A single piece of structured data on an item or workflow object. |
| Field key | The stable, machine-readable identifier for a field, used in imports, exports, GraphQL, and agent calls. |
| Form | A structured set of questions attached to a workflow step. |
| Form assignment | Assigns a form to one specific person for one step; only one is active per person per step. |
| Item | A single record in AssureSwarm, of a configured item type. |
| Item permission | An access rule controlling whether a user can view or edit a specific item or set of items. |
| Item type | The configured definition of a kind of item: its fields, statuses, labels, and behavior. |
| MCP | Model Context Protocol, the interface agents use to call AssureSwarm tools. |
| Owner | The user, or users, responsible for an item. |
| Page access | The setting controlling which system pages and item type pages a user sees in navigation. |
| Personal token | An access token generated from the OAuth Setup page for individual use; valid for 30 days. |
| Relationship | A typed link between two items: `parent`, `child`, `sibling`, or `related`. |
| Review level | The display-order tier for approvers on a step; it does not enforce approval order. |
| Scope | An OAuth permission grant that limits which MCP tools and data a token can use. |
| Step | A unit of work inside a workflow. |
| Suggestion | A proposed change from an agent, held pending until a person approves or rejects it. |
| Tenant | A AssureSwarm environment for one organization, reachable at its own tenant URL. |
| Workflow | A structured sequence of steps attached to an item, tracking a piece of work to completion. |
| Workflow template | A reusable, predefined workflow definition that new workflows are created from. |

## System Pages

| Page | What It's For | Default Access (Regular User) |
|---|---|---|
| Dashboards | Monitor work through the [built-in views](https://docs.assureswarm.com/concepts/dashboards/#built-in-views) such as My Work, Workflow Operations, Workflow Runs, Workflow Coverage, and Universe. | Granted by default |
| Templates | Browse, and with permission manage, reusable workflow templates. | Granted by default |
| Time Keeping | Log and review time entries by item and week, when your tenant has it enabled. | Granted by default |
| My Items | Find items assigned to or owned by you. | Granted by default |
| Settings | Manage your personal account preferences. | Not granted by default |
| Admin | Configure the tenant: item types, users, workflow templates, integrations, and more. | Not granted by default |
| Item type pages (one per configured type) | Browse, create, and update items of that type. | Granted per user |
| Forms Inbox | Respond to forms assigned to you for a workflow step. | Follows form assignment, not page access: reaches external collaborators too |

## Field Types

| Type | Stores |
|---|---|
| TEXT | A single line of plain text. |
| TEXTAREA | Multiple lines of plain text. |
| RICHTEXT | Formatted text. |
| NUMBER | A numeric value. |
| DATE | A calendar date. |
| DATETIME | A date and time. |
| SELECT | One value chosen from a list of options. |
| MULTISELECT | One or more values chosen from a list of options. |
| BOOLEAN | A true/false value. |
| USER | A single user reference. |
| USERS | Multiple user references. |
| RELATION | A single link to an item of a configured item type. |
| RELATIONS | Multiple links to items of a configured item type. |
| JSON | Structured data that doesn't fit another field type. |

SELECT and MULTISELECT options come from either field-level options or a linked custom list. Agents and imports must use the stored option **values** returned by schema metadata, not display labels. RELATION and RELATIONS fields each point at a configured item type.

## Relationship Kinds

| Kind | Meaning |
|---|---|
| `parent` | The related item is a parent of this item. |
| `child` | The related item is a child of this item. |
| `sibling` | The related item is a peer of this item. |
| `related` | A general association with no hierarchy implied. Default kind when none is specified. |

The same four kinds link a workflow step directly to an item (step-item links).

## Statuses

| Object | Lifecycle | Notes |
|---|---|---|
| Item | Configured per item type. | New items start at the item type's default status. |
| Workflow | Typically `DRAFT` → `ACTIVE` → `COMPLETED`. | Status is visible on workflow views. |
| Step | `PENDING` → `IN_PROGRESS` → `COMPLETED`. | Derived from approvals: pending until activity starts, completed once required approvals are met. |
| Approval | Pending until the approver decides. | Records native sign-off; review level orders the display, and approvals can happen in any order. |
| Form assignment | Active → submitted, or revoked. | One active assignment per person per step. |
| Time entry | `DRAFT` → `SUBMITTED` → `APPROVED` / `REJECTED`. | Weekly, per item. |
| Suggestion | `pending` → `processing` → `approved` / `rejected`. | A stalled `processing` suggestion returns to `pending` automatically. |
| Document validation | `pending` → `validated` / `rejected`. | A rejected upload must be re-uploaded. |

## OAuth Scopes

Each tool needs one scope on the connecting token:

| Tool | Required Scope |
|---|---|
| [get_schema](https://docs.assureswarm.com/mcp/get_schema/) | `read:data` |
| [query_data](https://docs.assureswarm.com/mcp/query_data/) | `read:data` |
| [get_current_context](https://docs.assureswarm.com/mcp/get_current_context/) | `read:context` |
| [get_step_context](https://docs.assureswarm.com/mcp/get_step_context/) | `read:workflows` |
| [upload_document](https://docs.assureswarm.com/mcp/upload_document/) | `write:documents` |
| [download_document](https://docs.assureswarm.com/mcp/download_document/) | `read:documents` |
| [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) | `write:suggestions` |
| [list_pending_suggestions](https://docs.assureswarm.com/mcp/list_pending_suggestions/) | `read:suggestions` |
| [get_task_status](https://docs.assureswarm.com/mcp/get_task_status/) | `read:data` |
| [get_task_result](https://docs.assureswarm.com/mcp/get_task_result/) | `read:data` |
| [cancel_task](https://docs.assureswarm.com/mcp/cancel_task/) | `read:data` |
| [submit_card_action](https://docs.assureswarm.com/mcp/submit_card_action/) | `read:context` |

The full scope set:

| Category | Scopes |
|---|---|
| Identity | `openid`, `profile`, `email` |
| Read | `read:context`, `read:items`, `read:data`, `read:workflows`, `read:dashboards`, `read:documents`, `read:suggestions` |
| Write | `write:forms`, `write:items`, `write:workflows`, `write:dashboards`, `write:documents`, `write:suggestions` |
| Human approval | `approve:suggestions`; excluded from default grants and never required by an MCP tool. |

A scope-less authorization request receives the default grant: `openid profile email read:context read:items read:workflows read:dashboards read:documents read:suggestions write:suggestions read:data write:documents`.

:::note[Scopes only narrow: they never expand]
A token's scopes limit what it can do. Page access, item permissions, and visibility still apply underneath, so a token never exceeds the connected user's own permissions.
:::

## Limits

| Limit | Value |
|---|---|
| `query_data.query` length | 64 KB maximum |
| Tool response size | 2 MB maximum |
| Document upload | 10 MB decoded maximum |
| Document download | 10 MB maximum; 5 MB default cap unless `maxBytes` is set |
| `get_current_context.limit` | 1–100, default 10 |
| Personal token lifetime | 30 days |
| Large-result export formats | `csv`, `jsonl` (links expire; refresh with the `dataExport(exportId)` query) |

## `suggest_change` Targets

| Target Type | Allowed Operations |
|---|---|
| Item type slugs (tenant-specific: discover with `get_schema`) | `create`, `update`, `delete` |
| `step` | `create`, `update`, `delete`, `submit_form` |
| `workflow` | `create`, `update`, `delete`, `prune-branch` |
| `workflowtemplate` | `create`, `update`, `delete` |
| `timeentry` | `create`, `update`, `delete` |
| `itemrelationship` | `create`, `delete` |
| `stepitemlink` | `create`, `delete` |
| `stepdocumentlink` | `create`, `delete` |
| `formassignment` | `create`, `delete` |
| `workflowtemplatestepitemlink` | `create`, `delete` |

Full input shape and examples: [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/).

## Bulk Import Sections

A bulk import envelope declares `format` and `version`, then puts selected
sections under `data`: `users`, `customLists`, `itemTypes`, `dashboards`,
`items`, `workflows`, `itemTemplateLinks`, `workflowTemplateStepLinks`,
`workflowsAttached`, and `itemRelationships`. Users import before records that
reference their emails. See [Imports and exports](https://docs.assureswarm.com/admin/imports-and-exports/)
for the executable shape and destination-version requirements.

## Public Documentation Boundary

Included: product concepts, in-app workflows, administrator workflows, MCP usage, read-only GraphQL examples, and safe troubleshooting.

Excluded: private deployment details, infrastructure configuration, direct database recovery commands, internal implementation notes, customer-specific data, secrets, tokens, passwords, and proprietary operational procedures.
