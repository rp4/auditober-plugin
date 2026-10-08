---
title: Admin Guide
description: "Nine guides to configuring a tenant: users and access, item types, custom lists, templates, data, AI, sign-on, settings, and the audit trail."
---

Administrators decide what a tenant tracks, who can see it, how work moves through
it, and which agents are allowed to help. Almost every choice here is visible to
somebody else as a page they can or cannot open, a field they must fill, or a
button that is not there. These guides are written around that: what you change,
and what your colleagues see afterwards.

The **Admin** entry appears in the top navigation only for administrators.

## The Administration page

Six cards, one per configuration area:

| Card             | Route                  | What it governs                                                    | Guide                                                  |
| ---------------- | ---------------------- | ------------------------------------------------------------------ | ------------------------------------------------------ |
| User Permissions | `/admin/permissions`   | Accounts, page access, item access, the admin flag.                | [Users and access](https://docs.assureswarm.com/admin/users-and-access/)           |
| Item Types       | `/admin/item-types`    | The record types your tenant tracks and their fields.              | [Item types and fields](https://docs.assureswarm.com/admin/item-types-and-fields/) |
| AI Integrations  | `/admin/oauth-clients` | Which AI platforms may connect, and on what terms.                 | [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/)             |
| System Settings  | `/admin/settings`      | Sign-in providers, allowed domains, document validation, branding. | [Tenant settings](https://docs.assureswarm.com/admin/tenant-settings/)             |
| Data Management  | `/admin/bulk-import`   | Exports, JSON imports, CSV user imports.                           | [Imports and exports](https://docs.assureswarm.com/admin/imports-and-exports/)     |
| Admin Activity   | `/admin/activity`      | The audit trail for everything above.                              | [Activity log](https://docs.assureswarm.com/admin/activity-log/)                   |

Three more surfaces are yours to govern without being cards on that page:

| Surface            | Where it is                                     | Guide                                            |
| ------------------ | ----------------------------------------------- | ------------------------------------------------ |
| Custom lists       | `/admin/custom-lists`, reached directly         | [Custom lists](https://docs.assureswarm.com/admin/custom-lists/)             |
| Workflow templates | The **Templates** page in the top navigation    | [Workflow templates](https://docs.assureswarm.com/admin/workflow-templates/) |
| Single sign-on     | The System Settings card, plus support for SAML | [Single sign-on](https://docs.assureswarm.com/admin/single-sign-on/)         |

## Start from what you need to do

| I need to                                              | Read                                                   |
| ------------------------------------------------------ | ------------------------------------------------------ |
| Add somebody, or fix what they can see                 | [Users and access](https://docs.assureswarm.com/admin/users-and-access/)           |
| Model a new kind of record                             | [Item types and fields](https://docs.assureswarm.com/admin/item-types-and-fields/) |
| Fix a dropdown that is missing an option               | [Custom lists](https://docs.assureswarm.com/admin/custom-lists/)                   |
| Standardize a process people keep improvising          | [Workflow templates](https://docs.assureswarm.com/admin/workflow-templates/)       |
| Load a dataset, or take a copy of the configuration    | [Imports and exports](https://docs.assureswarm.com/admin/imports-and-exports/)     |
| Let people connect Claude, ChatGPT, Gemini, or Copilot | [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/)             |
| Turn on Google, Microsoft, or SAML sign-in             | [Single sign-on](https://docs.assureswarm.com/admin/single-sign-on/)               |
| Change something that affects the whole tenant         | [Tenant settings](https://docs.assureswarm.com/admin/tenant-settings/)             |
| Work out who changed something, and when               | [Activity log](https://docs.assureswarm.com/admin/activity-log/)                   |

## Your first hour on a new tenant

Configuration has real dependencies, and the order below respects them. Jumping to
an import before any item types exist leaves nothing to import into.

1. **Sign-in.** Confirm you can get in, then decide how everyone else will:
   providers, allowed domains, or accounts you create by hand.
   [Single sign-on](https://docs.assureswarm.com/admin/single-sign-on/)
2. **Custom lists.** Create the shared vocabularies your fields will reference,
   before the fields reference them. [Custom lists](https://docs.assureswarm.com/admin/custom-lists/)
3. **Item types and fields.** Model the records the tenant will track. Slugs and
   field keys are the decisions that outlive everything else here.
   [Item types and fields](https://docs.assureswarm.com/admin/item-types-and-fields/)
4. **People and access.** Create the accounts and grant the pages, now that there
   are pages worth granting. [Users and access](https://docs.assureswarm.com/admin/users-and-access/)
5. **Workflow templates.** Build the repeatable processes that run against those
   records. [Workflow templates](https://docs.assureswarm.com/admin/workflow-templates/)
6. **Data.** Import what you already have, once the shape it lands in exists.
   [Imports and exports](https://docs.assureswarm.com/admin/imports-and-exports/)
7. **AI integrations.** Enable the platforms your organization uses, once there is
   something for an agent to be useful about.
   [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/)

:::tip\[Configure before you populate]
Item types, custom lists, and workflow templates are far easier to get right
before the tenant holds real data and running workflows that depend on them.
:::

## Editions

Some configuration is gated by edition. On **Studio**, the Item Types card is
hidden and its editor shows an upgrade notice, and on the Custom Lists page
creating and deleting values are unavailable while editing labels and toggling
values active still work. Enterprise SAML is licensed separately. Each guide
notes its own gating where it applies.

## What administrators cannot do

Two limits are worth knowing before somebody asks you to work around them:

* **You cannot see more than your permissions allow by accident.** The admin flag
  grants access to every page deliberately and visibly, and every use of it is
  recorded.
* **No agent can configure the tenant.** Creating a user, granting a page,
  registering a client, and reshaping an item type are not proposable by an agent
  at all. Agents read your configuration and propose changes to *records*, which a
  person then approves. See
  [Reviewing suggestions](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/).
