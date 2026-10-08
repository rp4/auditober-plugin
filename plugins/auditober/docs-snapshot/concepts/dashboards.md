---
title: Dashboards
description: "Built-in dashboards over your items, workflows, forms, and time data, plus the views that read their filters from a link: Workflow Runs, Workflow Coverage, Third-Party Risk, Risks, Policy Lifecycle, Policy Exceptions and Compliance Requirements."
sidebar:
  order: 7
---

Views
Catalog
Drill
Access

Scroll

Everywhere else in AssureSwarm you change something. Dashboards are the one
surface that only reads, which is what makes them safe to leave open all day and
worth understanding as a layer of their own.

## Built-in views over live queries

A dashboard is a page the product ships: tiles, charts, and tables laid
out for one question, such as what is waiting on you, where running work
is stuck, or how often a workflow template is used. It stores no numbers
of its own.

Those come from the same read-only query surface agents use, run fresh
each time the page loads and scoped to your own
[permissions](https://docs.assureswarm.com/concepts/permissions/). Two people can open the same
dashboard and correctly see different totals.

## Shipped, chosen with a link, or imported

Built-in dashboards cover personal work, workflow operations, capacity,
AI activity, the risk control matrix, SOX, template
usage, workflow coverage, and the item graph. Their availability follows
the tenant's installed dashboard rows and schema. An empty workflow
portfolio shows an empty state.

More appear as your schema grows, because a register cannot exist before
its item type does. Two of the views take their subject from the address
bar: Workflow Runs reads which templates and months you chose, Workflow
Coverage reads which pair of item types. An administrator can also import
a saved coverage view.

## A number, then the rows behind it

Tiles carry a number and nothing else: they are a summary, not a link. The
tables underneath them are where a dashboard opens up, because a table row
can carry you straight to the step, form, or record it stands for, and a
selected bar segment on Workflow Runs lists the workflows it counts.

Filters work on the whole page rather than on the tile you set them on, so
a dashboard that looks empty is often a filter left over from the last
visit. Nothing on the page writes anything: to change something you follow
the link through and work the record.

## Who finds it, and what they see

Built-in dashboards are listed for everyone who can open the Dashboards
section at all, which [page access](https://docs.assureswarm.com/concepts/permissions/) decides. A
saved coverage view is `PRIVATE` or `PUBLIC`: private means its creator
and administrators find it in the gallery, public means everyone in the
tenant does.

Listing shares the page, not the data. Every query still runs as whoever
is reading, so a colleague opening the same view sees their own numbers,
not yours. Favorites sort to the front of the gallery, which is the
fastest way to keep the two or three you actually use in reach.

## Built-in views

Every tenant ships with a set of built-in dashboards, reachable from the
**Dashboards** page in the top navigation. They behave like any other
dashboard: you can favorite them, and they respect the same filters.

Availability depends on the dashboard rows installed in your tenant and its
schema. Executive requires at least one active `control`, `risk`, `issue`,
`audit`, `policy` or `system` type. The table below lists the other schema
requirements. A listed view can have no data yet. Read `dashboardTypes` and
the visible dashboard rows for the connected tenant before building a link.

| Dashboard                                                           | What it shows                                                                                                                                                                                                                     | When it is listed                                                              |
| ------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Executive** (`/dashboards/executive`)                             | Enterprise assurance posture and decisions                                                                                                                                                                                        | once any register item type is active                                          |
| **Operational** (`/dashboards/operations`)                          | Workflow throughput, delay, and accumulated work                                                                                                                                                                                  | always                                                                         |
| **My Work** (`/dashboards/my-work`)                                 | A prioritized view of work requiring action                                                                                                                                                                                       | always                                                                         |
| **Capacity Monitoring** (`/dashboards/capacity-monitoring`)         | Owner workload, due work, and late work                                                                                                                                                                                           | always                                                                         |
| **AI Activity** (`/dashboards/ai-activity`)                         | Suggestion usage and outcome movement                                                                                                                                                                                             | always                                                                         |
| **Risks** (`/dashboards/risks`)                                     | Likelihood and impact of every open risk, treatment and owner, the controls, issues and remediations behind each, and the assessments in flight; replaced the Risk Register on 2026-09-26                                         | once the `risk` item type is active                                            |
| **Risk Control Matrix (RCM)** (`/dashboards/rcm`)                   | Audit fieldwork coverage of controls and the risks they mitigate                                                                                                                                                                  | always                                                                         |
| **Workflow Runs** (`/dashboards/template-runs`)                     | Workflows started each month, split into completed and not completed, with the workflows behind any bar                                                                                                                           | always on builds from 2026-09-24                                               |
| **Workflow Coverage** (`/dashboards/workflow-coverage`)             | Workflow status of the items directly linked to a chosen context, for any pair of item types                                                                                                                                      | always on builds from 2026-09-24                                               |
| **Third-Party Risk** (`/dashboards/third-party-risk`)               | Third parties by tier, reassessment and renewal clocks, where reviews wait on each step, the review trend, and the questionnaires the platform is chasing                                                                         | once the `system` item type is active, on builds from 2026-09-26               |
| **Policy Lifecycle** (`/dashboards/policy-lifecycle`)               | Where policies wait in their review workflows, the review calendar, and the controls, risks, issues and remediations linked to each policy                                                                                        | once the `policy` item type is active, on builds from 2026-09-26               |
| **Policy Exceptions** (`/dashboards/policy-exceptions`)             | The policy waivers in force or requested, tracked through the Policy Exception & Risk Acceptance workflow: where each is in its approval workflow, the expiry watchlist, which policies are being waived, and the history of each | once the `policy` and `issue` item types are active, on builds from 2026-09-28 |
| **Compliance Requirements** (`/dashboards/compliance-requirements`) | Applicability and implementation of every requirement, by framework and by domain, with the controls each maps to                                                                                                                 | once the `requirement` item type is active, on builds from 2026-09-26          |
| **SOX Program** (`/dashboards/sox-program`)                         | Current SOX controls and testing results; key controls or all controls                                                                                                                                                            | once the `control` item type is active                                         |
| **Issues and remediations** (`/dashboards/issues-remediations`)     | Open issues, overdue remediation and validation, by audit and fiscal year                                                                                                                                                         | once the `issue` item type is active                                           |
| **Audit Plan** (`/dashboards/audit-plan`)                           | Planned audit work by year                                                                                                                                                                                                        | once the `audit` item type is active                                           |
| **Personnel** (`/dashboards/personnel`)                             | People, reporting lines and personnel workflows                                                                                                                                                                                   | once the `personnel` item type is active                                       |
| **Model Inventory** (`/dashboards/model-inventory`)                 | Models and their assurance work                                                                                                                                                                                                   | once the `model` item type is active                                           |
| **Item type register** (`/dashboards/register/<slug>`)              | An installed register's items and field filters                                                                                                                                                                                   | only for a visible active register row with that type                          |
| **Universe** (`/dashboards/universe`)                               | Interactive graph of items, templates, runs and steps and how they connect; ego and path focus modes                                                                                                                              | always                                                                         |

:::note\[Read the current catalog]
Operational, My Work, Capacity Monitoring and AI Activity remain listed when
their installed views have no data. Processes and Form Follow-up are retired;
Workflow Operations now redirects to Workflow Runs. The former Controls,
Systems, Issues, Audits and Policies routes also redirect to current views.
The automatic registers for `fsli`, `personnel`, `process` and
`remediation` are retired. Use the current visible dashboard rows.
:::

[Using dashboards](https://docs.assureswarm.com/using-coworkcanvas/using-dashboards/) is the procedure for
working with them, and
[Exploring the universe](https://docs.assureswarm.com/using-coworkcanvas/exploring-the-universe/) covers the
graph view in particular.

## Views you open with a link

Several dashboards keep their subject or their filters in the URL, so the
address bar is the saved view and a link is all it takes to share one.
[Linking to a filtered dashboard](https://docs.assureswarm.com/using-coworkcanvas/dashboard-links/) has the
exact parameters.

**Workflow Runs** takes up to twelve workflow templates and a range of 6, 12, or
24 months. Each month's bar is the workflows started that month from those
templates, stacked into completed (every step approved today) and not
completed. Selecting a segment lists the workflows behind it, with the item,
template, status, completed and incomplete steps, and dates. The CSV export
carries the monthly numbers per template.

**Workflow Coverage** takes a context item, found by searching every item you
can see, and a related item type, then shows the workflow status of the related
items directly linked to that context. An audit as the context with controls as
the related type is a SOX coverage view. Legacy SOX links carrying coverage
parameters redirect there. The current SOX Program page remains available
at `/dashboards/sox-program?controls=key` (or `controls=all`).

**Third-Party Risk**, **Risks**, **Policy Lifecycle**, **Policy Exceptions**
and **Compliance Requirements** (builds from 2026-09-26; Policy Exceptions
from 2026-09-28, when it was split out of Policy Lifecycle) keep their filters
in the URL: scope and tiers, categories and treatment, policy type and
framework (plus open or all exceptions), frameworks and applicability, plus a
search. Every tile, bar, box and cell opens the records
behind it under the charts, and the **Export** menu downloads a CSV or copies
the query an agent can run for the same numbers. Risks replaced the Risk
Register; a Risk Register link still lands on it, and its old `range` and
`scope` parameters are ignored.

## Sharing and visibility

Built-in dashboards need no sharing: everyone with access to the Dashboards
section finds them. A saved coverage view has a name, a description, and a
visibility setting: `PRIVATE`, where only its creator and administrators can
see it, or `PUBLIC`, where everyone in the tenant can. You can favorite the
dashboards you use often so they sort to the front of the gallery.

Visibility governs who finds the page. It does not govern what the page shows:
every query runs as the person reading it, so listing a dashboard never
exposes a record the reader could not already open.

## Importing, and what agents do

Administrators can bring saved coverage views into a tenant through
[bulk import](https://docs.assureswarm.com/admin/imports-and-exports/): each row names a context item type
and a related item type. Agents do not create dashboards. An agent that is
asked for one composes the matching Workflow Runs or Workflow Coverage link
instead, and reads the same numbers through [query\_data](https://docs.assureswarm.com/mcp/query_data/).

And on the query surface underneath

## For agents

A dashboard is a rendering of questions an agent can ask directly.
[query\_data](https://docs.assureswarm.com/mcp/query_data/) answers the same counts and breakdowns a tile
or a chart does, and [GraphQL](https://docs.assureswarm.com/graphql/) exposes the named reads the
built-in pages are built on, including `workflowTemplateRunTrend` and
`workflowTemplateRunTrendDetails` for Workflow Runs and
`workflowCoverageDashboard` for Workflow Coverage. Both are scoped to the
connected user, so an agent's totals match what that person would see on
the page and never exceed it. To show a person a view, an agent sends the
link; there is no dashboard write to propose.
