---
title: Linking to a filtered dashboard
description: Build a shareable AssureSwarm dashboard URL that preserves its filters, search, sorting, expansion, and Universe view state.
sidebar:
  order: 8
---

## What a dashboard link is

Everything you can filter, search, sort, expand or select on these dashboards
is in the URL. Copy the address bar and the recipient sees the same view; an
agent can compose one the same way.

For example, this link opens the Risk Control Matrix for a selected audit:

```text
https://acme.assureswarm.com/dashboards/rcm?range=6m&entity=aud123
```

## Building the absolute URL

Build a link from `https://<tenant>.assureswarm.com` and a locale-free
path such as `/dashboards/rcm`. An agent can get the origin from
`get_current_context` → `currentView.pageUrl`, or from the plugin's
`canvas_url`.

Unknown keys are removed when the dashboard loads. A non-empty value for a
declared filter key is retained even if it matches no current option or returns
no rows; the table simply shows no rows. Malformed reserved values, such as an
invalid sort, search, or expansion value, are canonicalized away.

```text
https://acme.assureswarm.com/dashboards/rcm?range=12m&RCM_MATRIX.q=vendor
```

## Shared parameters

These parameters apply where the dashboard offers them:

| Parameter            | Meaning                                                        |
| -------------------- | -------------------------------------------------------------- |
| `range=6m\|12m\|ytd` | Reporting range. `6m` is the default and is added when absent. |
| `scope=<domain>`     | A dashboard scope, where the dashboard offers scope selection. |
| `entity=<auditId>`   | The selected audit on Risk Control Matrix only.                |

```text
https://acme.assureswarm.com/dashboards/rcm?range=12m&entity=aud123
```

## Table parameters

Table state uses `<tableId>.<key>`. Every table may use `q` for search and
`sort=<key>.<asc|desc>` for sort order, expressed as
`<tableId>.q` and `<tableId>.sort`. Expandable tables use one or more
`expand=<rowId>[/<childRowId>]` parameters.

Only table keys in the current dashboard composition are accepted. Use a
sort key supplied by that table, followed by lowercase `asc` or `desc`.
For example, `RCM_MATRIX.sort=coverage.desc` is valid;
`RCM_MATRIX.sort=unknown.desc` is not. A table definition elsewhere in the
product does not make its keys valid on this page.

The Processes and Form Follow-up dashboards are retired and redirect to the
dashboard list. Workflow Operations redirects to Workflow Runs. Use the
current tenant dashboard catalog instead of composing their former filters.

## RCM (`/dashboards/rcm`)

Risk Control Matrix uses table ID `RCM_MATRIX`. Select its audit with
`entity=<auditId>`, then use `RCM_MATRIX.audit`, `RCM_MATRIX.type`, and
`RCM_MATRIX.coverage`; get their values from the table's `filterOptions`.
Use `RCM_MATRIX.q` for search and
`RCM_MATRIX.sort=<key>.<asc|desc>` with one of
`item|audit|coverage|signedOff`.

```text
https://acme.assureswarm.com/dashboards/rcm?range=12m&entity=aud123&RCM_MATRIX.coverage=pending&RCM_MATRIX.sort=signedOff.desc
```

## Universe (`/dashboards/universe`)

Universe filters have two URL modes. With no Universe filter keys, the implicit
default selects every value in every item-type filterable field and shows every
ordinary fieldless item type. Synthetic types have mode-specific defaults. The
full graph shows only `_workflow_template`; ego and path focus show
`_workflow_template` plus `_template_step`. `_workflow` and `_step` are hidden
by default in all three modes.

Once any Universe filter key is present, the URL is an explicit, complete
snapshot. It emits every filterable field as
`<typeSlug>.<fieldKey>=v1,v2` or `<typeSlug>.<fieldKey>=` for zero selected
values, and every fieldless type as `<typeSlug>=visible` or `<typeSlug>=` when
hidden. A complete snapshot includes all four synthetic selectors. Each
explicit empty value remains in the canonical URL.

Do not omit individual selectors from an explicit snapshot. The legacy parser
treats an omitted filterable field as empty and an omitted fieldless type as
hidden; omission invokes the mode-specific defaults above only when the URL
contains no Universe filter keys at all. Universe view state uses `q`,
`node=<nodeId>`, `window=7d|30d|90d|1y`, and the focus-mode keys `focus`,
`depth` and `hops` described below. The run-time steps kind is an ordinary
fieldless type: `_step=visible` shows it, `_step=` hides it (`steps=1` is no
longer read).

Universe owns `q`, `node`, `window`, `focus`, `depth` and `hops`: writing a view
replaces those six keys, then writes only non-default values. The canonical
defaults are no search, no selected node, and `window=30d` omitted from the URL.

For a schema whose only item-type selectors are `control.status` and a
fieldless `risk` type, this link is a complete explicit snapshot that shows
only run steps among the synthetic kinds:

```text
https://acme.assureswarm.com/dashboards/universe?control.status=active,planned&risk=visible&_workflow_template=&_template_step=&_workflow=&_step=visible&q=vendor&node=itm123&window=90d
```

To share the same schema with no control statuses selected and the risk type
hidden while retaining the full-graph synthetic defaults, retain every
selector:

```text
https://acme.assureswarm.com/dashboards/universe?control.status=&risk=&_workflow_template=visible&_template_step=&_workflow=&_step=
```

## Universe focus (`/dashboards/universe?focus=…`)

Focus mode draws the neighbourhood of one node: the node at the centre and
every node within a number of hops on concentric rings. It has two shapes:

* **Ego mode**: the same kinds are followed at every hop.
* **Path mode**: one kind per hop, so a link can say "this audit → its workflow
  runs → their steps → the controls in those steps → the templates those
  controls are linked to → every run of those templates".

### Focus URL grammar

| Parameter    | Grammar                         | Default               | Notes                                                                                                                                 |
| ------------ | ------------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `focus`      | a node id (below)               | none (the full graph) | An unknown or invisible id is cleared and the full graph shown.                                                                       |
| `depth`      | `1` … `6`                       | `2` (omitted)         | Ego mode only; ignored when `hops` is present.                                                                                        |
| `hops`       | comma-separated type slugs, 1–6 | none (ego mode)       | Path mode. Ring *k* contains only the kind `hops[k-1]`. Unknown slugs are dropped and the URL corrected.                              |
| type filters | the Universe grammar above      | see below             | Ego mode: the visible types are the kinds followed at every hop. Path mode: the path decides; type filters are ignored for traversal. |

Node ids: items use the item id; workflow templates `template-<templateId>`;
template steps `tstep-<templateId>:<diagramNodeId>`; workflow runs
`workflow-<workflowId>`; run steps `step-<stepId>`.

Kinds (type slugs): every item type slug plus the synthetic kinds
`_workflow_template`, `_template_step`, `_workflow` (runs) and `_step` (run
steps). With no Universe filter keys, ego mode follows every item type plus
`_workflow_template` and `_template_step`; list kinds explicitly to narrow
(any filter key makes the URL a complete snapshot, exactly as above).

Each ring keeps at most 150 nodes per kind, choosing the most connected, and
folds the rest into one "N more `<kind>`" node. Narrow the kinds or reduce the
depth when a link reports that cap.

```text
/dashboards/universe?focus=<processId>&depth=2
/dashboards/universe?focus=<processId>&depth=3&process=visible&_workflow_template=visible&_template_step=visible&control=visible&risk=visible&_workflow=&_step=
/dashboards/universe?focus=<auditId>&hops=_workflow,_step,control,_workflow_template,_workflow
```

The `universeFocus` query returns the accepted server neighbourhood for an
agent (`input { focus, depth, kinds, hops }`). Its accepted `focus`, `depth`,
`hops`, `kinds` and `capped` values correspond to the page's focus state, as do
each node's `ring` and `collapsed` values.

The page's JSON download is not a raw copy of that response. It exports the
currently drawn subset after the client applies type and field filters, search,
and timeline playback. Edge records keep the GraphQL shape: `id`, `sourceId`,
`targetId`, `edgeType` and `label`. Export nodes are normalized to `id`,
`typeSlug`, `kind`, `title`, `status`, `ring`, `href` and `collapsed`; they omit
the GraphQL node's `description` and `filterFields` and add the display `kind`.

## Workflow Runs (`/dashboards/template-runs`)

Workflow Runs uses its own parameters, not the shared table grammar.
`templates=<templateId>,<templateId>` selects up to twelve workflow templates
in the order given (ids from `workflowTemplatesPage`; an unknown or invisible
id is reported on the page, not dropped). `range=6m|12m|24m` picks the number
of whole calendar months ending now; `12m` is used when absent (`ytd` is not
accepted here). `month=YYYY-MM&state=complete|open` opens one bar segment: the
workflows started in that month that are complete now, or not. A month outside
the range is ignored.

```text
https://acme.assureswarm.com/dashboards/template-runs?templates=tmpl123,tmpl456&range=12m
https://acme.assureswarm.com/dashboards/template-runs?templates=tmpl123&range=6m&month=2026-09&state=open
```

The page's numbers come from `workflowTemplateRunTrend(templateIds, from, to)`
and the workflows behind a segment from
`workflowTemplateRunTrendDetails(templateIds, month, state, from, to)`; the
page's **Copy query for agents** action hands you both documents with the
current variables filled in.

## Workflow Coverage (`/dashboards/workflow-coverage`)

The page has two controls: a searchable picker for the context item and a
select for the related item type. In the URL they are
`contextItemType=<slug>&context=<itemId>` (the picked item and its type; slugs
from `itemTypes`, ids from `searchItems` or `items`) and
`relatedItemType=<slug>`. With all three present the page mounts the coverage
view, which keeps its own `q=<search>`, `coverage=without-workflows|<groupId>`
and `workflows=<groupId>,<groupId>` (template groups from the view's
summaries); with the two types but no `context` the page waits for an item to
be picked. Changing the item or the related type clears the view parameters.
Old SOX coverage links carrying `context`, `q`, `coverage`, `workflows`,
`contextItemType` or `relatedItemType` redirect here. The current SOX
Program page has its own controls selector, described below.

```text
https://acme.assureswarm.com/dashboards/workflow-coverage?contextItemType=audit&relatedItemType=control&context=aud123
```

The data comes from
`workflowCoverageDashboard(contextItemType, relatedItemType, contextItemId)`.

## SOX Program (`/dashboards/sox-program`)

The current program page accepts `controls=key|all`; key controls are the
default. It reads `soxProgramDashboard`. Do not add old coverage parameters
to this page, since those select the legacy redirect described above.

```text
https://acme.assureswarm.com/dashboards/sox-program?controls=all
```

## Issues and remediations (`/dashboards/issues-remediations`)

The URL accepts only `audit=<auditId>` and `fy=<fiscalYear>`. It has no
overdue-only URL filter. Read `issuesRemediationsDashboard` for an overdue
answer: select returned issues whose `dueState` is `past_due`, use
`daysLate` and `counts.pastDue`, and check `issuesCapped` and
`linksCapped` before claiming complete coverage. Here, past due means the
earliest open linked remediation target is before today. Link the dashboard
as the wider context.

```text
https://acme.assureswarm.com/dashboards/issues-remediations?audit=aud123&fy=2026
```

## Audit Plan, Personnel and Model Inventory

Audit Plan accepts `year=2000..2100`. Personnel accepts a live personnel
`focus` ID, live `template` ID, `first=6|12|24` and the returned opaque
`after` cursor; clear the cursor when either selection changes. Model
Inventory accepts a live `model` item ID. Their routes are
`/dashboards/audit-plan`, `/dashboards/personnel` and
`/dashboards/model-inventory`.

## Third-Party Risk (`/dashboards/third-party-risk`)

Third-Party Risk uses its own parameters. `scope=vendors|all` keeps the
systems whose `vendor` field is true (the default) or every system.
`tiers=<tier>,<tier>` keeps some criticality tiers (lowercase tokens from the
`system` item type's `tier` field, such as `critical,high`).
`templates=<templateId>,<templateId>` narrows the review panels to up to
twelve templates of the `system` item type; every one of them counts when
absent. `q=<text>` searches titles and owners.

```text
https://acme.assureswarm.com/dashboards/third-party-risk?scope=vendors&tiers=critical,high
https://acme.assureswarm.com/dashboards/third-party-risk?scope=all&templates=tmpl123&q=payroll
```

The page's numbers come from `thirdPartyRiskDashboard(scope, tiers,
templateIds, search)`, the follow-up panel from `formFollowup(hostItemType:
"system")`, and the workflows behind a bar of the review trend from
`workflowTemplateRunTrendDetails`.

## Risks (`/dashboards/risks`)

Risks replaced the Risk Register on 2026-09-26 and keeps its filters in the
URL. `categories=<token>,<token>` keeps some risk categories (lowercase
tokens of the `risk` item type's `category` field). `treatments=<token>`
keeps some treatments (`mitigate`, `accept`, `transfer`, `avoid`, or `none`
for risks whose treatment is not decided). `templates=<templateId>,…`
narrows the assessment trend to up to twelve templates of the `risk` item
type. `q=<text>` searches titles, owners, categories and linked control
titles. The Risk Register's `range` and `scope` parameters are ignored.

```text
https://acme.assureswarm.com/dashboards/risks?categories=cyber_security,privacy&treatments=mitigate
https://acme.assureswarm.com/dashboards/risks?treatments=none&q=vendor
```

The page's numbers come from `risksDashboard(categories, treatments,
templateIds, search)`; the register-over-time chart from
`itemTypeDashboardSnapshot(itemTypeSlug: "risk", range: { from, to, grain:
MONTH })` and its bars from `itemTypeDashboardDetails`; the agent line from
`aiSuggestionStats(filter: { itemType: "risk", dateFrom })`.

## Policy Lifecycle (`/dashboards/policy-lifecycle`)

`type=<token>` keeps one policy type (a `policy_type` token such as
`standard`); `framework=<token>` keeps the policies of one framework (a
`framework` token such as `hipaa`); `templates=<templateId>,…` narrows the
lifecycle panels to up to twelve templates of the `policy` item type;
`q=<text>` searches titles and owners.

```text
https://acme.assureswarm.com/dashboards/policy-lifecycle?type=standard&framework=hipaa
https://acme.assureswarm.com/dashboards/policy-lifecycle?templates=tmpl_annual_review&q=access
```

The page's numbers come from `policyLifecycleDashboard(policyType,
framework, search, templateIds)`. The policy exceptions moved to their own
page on 2026-09-28 (below); an `exceptions=` parameter on this page is
ignored.

## Policy Exceptions (`/dashboards/policy-exceptions`)

`type=<token>` and `framework=<token>` keep the exceptions of the policies of
one policy type or one framework (the same tokens as Policy Lifecycle);
`scope=open|all` shows the exceptions in force or requested (the default) or
every one; `q=<text>` searches exception titles, policy titles, owners and
approvers.

```text
https://acme.assureswarm.com/dashboards/policy-exceptions?type=standard
https://acme.assureswarm.com/dashboards/policy-exceptions?scope=all&q=workstation
```

The page's numbers come from `policyExceptionsDashboard(policyType,
framework, search, scope)`; an exception's history drawer reads
`itemActivityLogs` and `suggestionsForItem` for that issue.
Exceptions are tracked by the **Policy Exception & Risk Acceptance** workflow: the issue-type template whose `metadata.kind` is `policy-exception-risk-acceptance` (seeded from Studio v21). An exception's stage is the current step of its run of that template, `stages` counts the exceptions waiting at each step, and `withoutWorkflow` lists the open ones that have no run yet. A workspace without the template falls back to any workflow on the exception.

## Compliance Requirements (`/dashboards/compliance-requirements`)

`frameworks=<token>,<token>` keeps some frameworks (tokens of the
`requirement` item type's `framework` field, such as `hipaa,pci-dss`);
`applicability=<token>` keeps `applicable`, `not_applicable` or
`pending_review`; `implementation=<token>` keeps `implemented`,
`partially_implemented`, `planned` or `not_implemented`; `q=<text>` searches
references, titles, owners and mapped control titles.

```text
https://acme.assureswarm.com/dashboards/compliance-requirements?frameworks=hipaa,pci-dss&applicability=applicable
https://acme.assureswarm.com/dashboards/compliance-requirements?implementation=not_implemented
```

The page's numbers come from `complianceRequirementsDashboard(frameworks,
applicability, implementation, search)`.

## Where the values come from

| Value               | Source                               |
| ------------------- | ------------------------------------ |
| Table filter values | `systemDashboardTable.filterOptions` |
| Item IDs            | `items(itemType:, search:)`          |
| Type slugs          | `itemTypes`                          |
| Template IDs        | `workflowTemplatesPage(search:)`     |
| Select tokens (tiers, categories, frameworks, types) | `itemType(slug:).fieldDefinitions` options |

```text
systemDashboardTable(type: RISK_CONTROL_MATRIX, tableId: "RCM_MATRIX")
```
