---
title: Permissions
description: "The AssureSwarm access model: the sign-in gate, page access, item permissions, the admin flag, and agent token scopes."
sidebar:
  order: 5
---

Sign in
Pages
Records
Agents

Scroll

Four questions, asked in order: can this person sign in, which pages exist for
them, which records on those pages can they open, and what may an agent do on
their behalf. Every layer narrows the one outside it, and none of them widens
it.

## The outer gate: signing in

A person can sign in only if one of two things is true: they already have an
active account in the tenant, or their email domain is on the tenant's
**allowed sign-in domain** list, in which case their first single sign-on
provisions the account.

Email and password sign-in exists too, but only where an administrator has
enabled it for that account. There is no open self-signup: somebody always
grants access first. Deactivating a user cuts off access immediately while
leaving their history, approvals, and submissions intact.

## Page access decides what exists

Every user is granted specific pages: one per configured
[item type](https://docs.assureswarm.com/concepts/items-and-item-types/), plus Dashboards, Templates,
Time Keeping, My Items, and Admin. A page a person has not been granted does
not appear in their navigation at all, and the direct link is refused with
an **Access Denied** screen naming the area.

A regular new user gets the standard member set and no Admin. Item type
pages are granted one at a time, deliberately. There is no Workflows entry
to grant: a [workflow](https://docs.assureswarm.com/concepts/workflows/) opens from the item it is
attached to.

## Item access decides what you can open

Underneath page access, each item carries its own **visibility**, either
`public` or `private`, and a person can hold an **item permission** on a
specific record: `view` to open and read it, `edit` to change it as well.
There is one permission row per person per record.

An item type's page grant has a level: `view_public`, `view_all`, or
`edit_all`. The latter two cover every item of that type, including private
items. With `view_public`, ownership and individual grants determine which
private records you can open.

## Agents inherit a person's boundary

An agent is always authorized per user, through OAuth or a personal token,
and narrowed further by **scopes**, one required per MCP tool. Scopes only
subtract: a token never grants more than the connected person already has,
and everything it does is attributed to them.

The **admin flag** is the one thing that is not a page grant. An
administrator reaches every page and can change what everyone else reaches,
so promote deliberately and demote as soon as the role no longer needs it.

## Roles

| Role          | Access                                                                                                             |
| ------------- | ------------------------------------------------------------------------------------------------------------------ |
| Administrator | The full Admin area and tenant configuration, plus implicit access to every page.                                  |
| Member        | Regular access, scoped by page access and item permissions.                                                        |
| External      | A limited account, typically a form respondent who sees only their assigned form and not the surrounding workflow. |

Administrators can promote another user to administrator or remove that access:
see [Users and access](https://docs.assureswarm.com/admin/users-and-access/).

## Item visibility and permissions

An item's visibility is `public` or `private`. Item type page access combines
with ownership and individual `view` or `edit` grants:

| Page access level | Record access                                                                                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------------------- |
| `view_public`     | Read public items; private items need ownership or an individual grant.                                               |
| `view_all`        | Read every item of that type, including private items. Ownership or an individual edit grant can also permit editing. |
| `edit_all`        | Read and edit every item of that type, including private items.                                                       |

An individual grant applies to one record. Ownership also carries access.
Administrators have broader access through their administrator role.

:::caution\[Private items remain visible to type-wide readers]
Marking a record private does not hide it from someone with `view_all` or
`edit_all` on its item type. Review those page levels before storing sensitive
records.
:::

## Workflows, dashboards, and documents

Three object types inherit their access from what they are attached to, rather
than carrying a permission model of their own:

* A [workflow](https://docs.assureswarm.com/concepts/workflows/) follows the item it belongs to, plus workflow ownership.
* A [dashboard](https://docs.assureswarm.com/concepts/dashboards/) is either private or public.
* A [document](https://docs.assureswarm.com/concepts/documents/) follows the chain up through its step, workflow, and item.

## Agents, tokens, and scopes

Each MCP tool requires a specific scope:

| Tool                       | Required scope      |
| -------------------------- | ------------------- |
| `get_schema`               | `read:data`         |
| `query_data`               | `read:data`         |
| `get_current_context`      | `read:context`      |
| `get_step_context`         | `read:workflows`    |
| `upload_document`          | `write:documents`   |
| `download_document`        | `read:documents`    |
| `suggest_change`           | `write:suggestions` |
| `list_pending_suggestions` | `read:suggestions`  |
| `get_task_status`          | `read:data`         |
| `get_task_result`          | `read:data`         |
| `cancel_task`              | `read:data`         |
| `submit_card_action`       | `read:context`      |

The full scope list is in [Reference](https://docs.assureswarm.com/reference/).

Agents connect either through an OAuth client an administrator registers, see
[AI integrations](https://docs.assureswarm.com/admin/ai-integrations/), which is the path for multi-user
platforms, or through a personal token for individual use. Personal tokens are
generated from the AI Agent Setup page and expire after 30 days.

Whichever path an agent takes, `write:suggestions` is the scope that lets it
propose changes at all, and every proposal still lands as a
[suggestion](https://docs.assureswarm.com/concepts/suggestions/) for a person to review.

:::note\[A token never exceeds the connected user's own permissions]
Scopes only narrow what a token can do, they never grant more than the
connected user already has. Page access, item permissions, and visibility all
still apply underneath, and whatever an agent does is attributed to that user.
:::

## Auditing

Admin configuration changes and item activity are both logged and reviewable:
tenant-wide changes in the [activity log](https://docs.assureswarm.com/admin/activity-log/), and a single
record's history in its own activity feed. It is the same trail a suggestion's
outcome lands in once it is processed, see [Suggestions](https://docs.assureswarm.com/concepts/suggestions/).

And when an agent acts for someone

## For agents

Everything on this page bounds agents too. A token authorizes one person, so
[get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/) and
[query\_data](https://docs.assureswarm.com/mcp/query_data/) return exactly that person's slice of the
tenant and nothing wider. Writes go through
[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/) and are applied as the **approver**,
under the approver's permissions, which is what stops a proposal being used
to reach past what its reviewer could have done by hand. Tenant
configuration is not a suggestion target at all: no agent creates a user,
grants a page, or promotes an administrator.
