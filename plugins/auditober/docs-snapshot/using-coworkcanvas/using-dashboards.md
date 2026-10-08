---
title: Using Dashboards
description: "Find a dashboard, read what it is telling you, drill into the records behind a number, watch work and agents in flight, and share a view with a link."
sidebar:
  order: 7
---

Gallery
Read
Drill
Monitor

Scroll

A dashboard is a built-in page of tiles, charts, and tables over live queries
against your items, workflows, forms, and time entries.
[Dashboards](https://docs.assureswarm.com/concepts/dashboards/) covers the model; this page is how to
actually use them.

## Find one in the gallery

**Dashboards** in the top navigation opens the gallery: one card per
dashboard, each showing its description, its category, and, for a saved
coverage view, whether it is `PUBLIC` or `PRIVATE`. Search narrows by
name, and **Filter** narrows by category and by visibility.

Dashboards you have favorited sort to the front, so the star on a card is
worth using on the two or three you open every day.

## Read the numbers, then the list

**My Work** is the one to start from: tiles across the top count your
pending approvals, open forms, items due soon, and open items, and the list
below them, **Needs your action**, spells out each one with what it is, what
it belongs to, and when it was due.

Tiles summarize. Lists are where you act: select a row and you land on the
step, form, or record behind it.

## Find where work is stuck

**Workflow Operations** answers the operational question: of everything
running, what is not moving. It counts active workflows, overdue steps,
median cycle time, and on-time completion, then breaks workflows down by
stage and ranks **Bottleneck steps** by how long work sits there and how
many runs are waiting.

Beneath that, an overdue table names each late step, its workflow, its due
date, and how many days over it is. Filter the whole page to one template to
compare one process against itself over time.

## Watch what the agents are doing

**AI Activity** measures the agent side of the tenant: how many suggestions
are pending now, how many were approved, how many rejected, the resulting
approval rate, and the median time people take to decide. The chart plots
suggestions by status over time, and a second chart plots agent tool calls
per day.

Filter it by status, agent, item type, or date range. A rising rejection
rate is a signal to tighten the instructions an agent is working from.

## The dashboards you start with

Every tenant gets a set of built-in dashboards, reachable from the gallery like
any other:

| Dashboard               | What it answers                                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| My Work                 | What is waiting on me right now.                                                                                               |
| Workflow Operations     | Where running work is stuck.                                                                                                   |
| Capacity Monitoring     | Who is carrying how much open work.                                                                                            |
| Form Follow-up          | Which forms are outstanding, overdue, or returned.                                                                             |
| AI Activity             | What agents proposed, and what people decided.                                                                                 |
| Operational             | Work in flight, team load, forms, and open requests on one page.                                                               |
| Processes               | How processes, their templates, and their controls and risks fit together.                                                     |
| Risk Control Matrix     | Which controls and risks each audit covers, and where the gaps are.                                                            |
| Workflow Runs           | How often chosen templates are used each month, and how many of those runs finished.                                           |
| Workflow Coverage       | The workflow status of the items linked to a context, for any pair of item types.                                              |
| Third-Party Risk        | Which third parties need reassessment or renewal, where their reviews wait, and which questionnaires are out.                  |
| Risks                   | Which open risks are rated high, unrated, uncovered or unowned, and what issues, remediations and assessments sit behind them. |
| Policy Lifecycle        | Where each policy waits in its review and what it is linked to.                                                                |
| Policy Exceptions       | Which policy waivers are in force or requested, where each is in its approval workflow, and which are expiring.                |
| Compliance Requirements | Which requirements apply, how far each is implemented, and which map to no control.                                            |
| Universe                | How everything connects.                                                                                                       |

The operational pages are always there: before any workflow is running they show
an empty state rather than disappearing.

On top of those, posture and register pages appear as your tenant's schema grows:
an executive summary, and a register for each of the control, risk, issue,
audit, policy, and system item types your tenant has active (Risks replaced
the Risk Register on 2026-09-26; Third-Party Risk, Policy Lifecycle, Policy
Exceptions and Compliance Requirements need the system, policy, policy plus
issue, and requirement item types). Administrators
can also import saved coverage views, so your gallery may be longer than this
list.

## Reading any dashboard

The vocabulary is small and repeats everywhere:

| Element | What to do with it                                                                                             |
| ------- | -------------------------------------------------------------------------------------------------------------- |
| Tile    | Read the number, then find the list that explains it.                                                          |
| Chart   | Compare across time, status, or owner. On Workflow Runs, select a bar segment to list the workflows it counts. |
| Table   | The records themselves: this is where you drill through.                                                       |
| Filter  | Narrows the whole page at once.                                                                                |

Filters apply to the whole page, not just the element you set them on, so a
dashboard that looks empty is often a filter left over from your last visit.

## Choosing what a dashboard shows

Six dashboards take their subject or their filters from you rather than from
the tenant:

* **Workflow Runs** asks for one or more workflow templates and a range of 6,
  12, or 24 months. Each month's bar is the workflows started that month from
  those templates, stacked into completed and not completed. Select a segment
  to see the workflows behind it, with their items, statuses, and step counts.
  The **Export** menu downloads the monthly numbers per template as CSV, or
  copies the query an agent can run for the same numbers.
* **Workflow Coverage** asks for a context item, which you find by searching
  every item you can see, and a related item type such as controls or audits,
  then shows the workflow status of everything of that type directly linked to
  the item. The former SOX Program dashboard is this view with an audit and
  controls; its old link lands here.
* **Third-Party Risk** starts from the systems whose vendor field is true,
  lets you switch to every system, narrow by tier, and pick the review
  templates behind the box plot and the trend.
* **Risks** narrows the open register by category and treatment, and picks
  the assessment templates behind the trend.
* **Policy Lifecycle** narrows by policy type and framework, and picks the
  review templates behind the lifecycle panels.
* **Policy Exceptions** narrows by the waived policy's type and framework,
  and shows the open exceptions or all of them.
* **Compliance Requirements** narrows by framework, applicability and
  implementation status.

All of them keep every choice in the address bar. Copy the URL to share exactly what
you are looking at; [Linking to a filtered dashboard](https://docs.assureswarm.com/using-coworkcanvas/dashboard-links/)
lists the parameters.

## Saved views, and who sees them

A saved coverage view (one an administrator imported) is `PRIVATE` by default:
only its creator and administrators see it. Set it to `PUBLIC` and everyone in
the tenant can, though page access still governs who can reach the Dashboards
section at all. Favorite the ones you use to keep them at the front of the
gallery.

Dashboards read; they do not write. Nothing you do on one changes a record. To
change something, follow the link through to the item, step, or form and work it
there.

## When an agent sends you a dashboard

Agents do not create dashboards. When you ask one to show you template usage or
coverage, it composes the link to the matching view with your selection already
in it, so opening the link lands you on the filtered page. Ask it for the
numbers as well and it reads them with the same query the page runs.

And on the query surface underneath

## For agents

Dashboards and agents read the same data.
[query\_data](https://docs.assureswarm.com/mcp/query_data/) answers the same questions a dashboard
does, counts and breakdowns by status, owner, or due date, and
[GraphQL](https://docs.assureswarm.com/graphql/) exposes the named reads the built-in pages use,
including `workflowTemplateRunTrend`, `workflowTemplateRunTrendDetails`,
and `workflowCoverageDashboard`. Everything is scoped to the user's
[permissions](https://docs.assureswarm.com/concepts/permissions/), so an agent's numbers never include
records its user could not open. To show a person a view, an agent sends
the link; there is no dashboard to propose through
[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/).
