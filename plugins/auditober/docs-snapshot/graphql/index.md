---
title: GraphQL
description: "The read-only GraphQL surface behind query_data: corrected examples, pagination, aggregate fields, and the full query catalog."
---

Agents query AssureSwarm through the [query_data](https://docs.assureswarm.com/mcp/query_data/) MCP tool, which accepts read-only GraphQL: mutations and subscriptions are rejected. The catalog below is the same one returned live by [get_schema](https://docs.assureswarm.com/mcp/get_schema/) as `queryReference`; prefer the live version when in doubt, since item types and their fields are tenant-specific.

## Ground Rules

- Call [get_schema](https://docs.assureswarm.com/mcp/get_schema/) first and reuse the exact item type slugs and field keys it returns.
- Use GraphQL variables, not string interpolation, for any value that comes from user input or a prior tool result.
- Select only the fields you need: tool responses are capped at 2 MB.
- Item lists are paginated; read `total` and `totalPages` instead of assuming one page holds everything.
- Prefer the aggregate and stats fields below for counting or summarizing: don't page through every item to count it yourself.
- Writes never happen through GraphQL; propose them with [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) instead.

:::tip[Discover before you write]
Call `get_schema` first and reuse the exact field keys it returns: item types, field keys, and option values vary by tenant.
:::

## Core Examples

These four shapes are verified against the live schema.

List item types:

```graphql
query ListItemTypes {
  itemTypes {
    slug
    name
  }
}
```

Inspect one item type's fields:

```graphql
query ItemTypeFields($slug: String!) {
  itemType(slug: $slug) {
    slug
    name
    fieldDefinitions {
      fieldKey
      label
      fieldType
      required
    }
  }
}
```

List items: **`items` returns a paginated object**, select rows via the inner `items` field:

```graphql
query OpenIssues($itemType: String!, $limit: Int) {
  items(itemType: $itemType, limit: $limit) {
    items {
      id
      title
      status
    }
    total
    page
    totalPages
  }
}
```

with variables:

```json
{ "itemType": "issue", "limit": 10 }
```

`total` is always the full matching count, regardless of `limit` or `page`.

Count and break down without paging:

```graphql
query ItemCounts($itemType: String) {
  itemStats(itemType: $itemType) {
    totalCount
    overdueCount
    byStatus {
      group
      label
      count
    }
  }
}
```

## Aggregate and Report Fields

Six fields answer the questions you'd otherwise have to page through every record to answer by hand:

| Field | Answers | Returns |
|---|---|---|
| `itemStats(itemType?)` | Counts and breakdowns by status, owner, and item type | `ItemStats { totalCount, overdueCount, byStatus, byOwner, byItemType }` |
| `workflowStats(itemType?, status?)` | Workflow and step progress, including overdue steps | `WorkflowStats { totalWorkflows, totalSteps, overdueSteps, byStatus, stepsByStatus, stepsByAssignee, averageStepsPerWorkflow }` |
| `suggestionStats(agentId?)` | Agent suggestion volume and approval rate | `SuggestionStats { totalCount, approvalRate, byStatus, byOperation, byAgent, byItemType }` |
| `timeEntryStats(weekStart?, userId?)` | Logged-time totals and breakdowns | `TimeEntryStats { totalHours, pendingApprovalCount, byUser, byItem, byWeek }` |
| `dueDateReport(daysAhead?, includeItems?, includeSteps?)` | What's overdue or coming up | `DueDateReport { overdueItems, overdueSteps, upcomingItems, upcomingSteps }` |
| `teamWorkloadStats(itemTypes?)` | Open work broken down by person | `TeamWorkloadStats { totalSteps, stepsByStatus, stepsByAssignee, stepDetails }` |

Breakdown (`by*`) entries are shaped `{ group, label, count }`. Time breakdowns use `value` in place of `count` for hours.

## Query Catalog

The complete set of queries the schema exposes, grouped by area and matching `get_schema`'s live `queryReference`.

### Identity and Context

| Signature | Purpose |
|---|---|
| `viewer` | The authenticated identity and auth metadata |
| `myContext` | The user's most recent page context |
| `myPageAccess` | The user's page grants |
| `hasPageAccess(pageName)` | Whether the user can access a given page |

### Schema

| Signature | Purpose |
|---|---|
| `itemTypes(includeInactive?, includeInactiveFields?)` | List all item types |
| `itemType(slug, includeInactive?, includeInactiveFields?)` | One item type by slug |
| `itemTypeWithFields(slug, includeInactive?, includeInactiveFields?)` | One item type with its full field list |

### Items

| Signature | Purpose |
|---|---|
| `items(itemType, status?, excludeStatuses?, dashboardDetailType?, ownerId?, createdById?, search?, sortBy?, domain?, fieldFilters?, page?, limit?)` | Paginated item list; `fieldFilters` takes `[{ fieldKey, fieldType, values: [..] }]` |
| `item(id)` | One item by ID |
| `itemWithRelations(id)` | One item with its relationships |
| `itemActivityLogs(itemId, itemType, limit?)` | Activity history for an item |
| `searchItems(query?, search?, itemType?, page?, limit?, take?)` | Search across items |
| `myItems(page?, limit?)` | Items you own |
| `mySharedItems(page?, limit?)` | Items shared with you |
| `allItems(status?, ownerId?, overdue?, search?, skip?, take?)` | Items across item types |
| `itemStats(itemType?)` | Counts and breakdowns for items |

### Relationships and Links

| Signature | Purpose |
|---|---|
| `itemRelationships(itemType, itemId)` | Relationships attached to an item |
| `stepItemLinks(stepId)` | Items linked to a step |
| `stepLinkedEntities(stepIds)` | Entities linked to a set of steps |

### Workflows and Steps

| Signature | Purpose |
|---|---|
| `myWorkflows(includeCompleted?, take?)` | Workflows you're involved in |
| `myAssignedSteps(includeCompleted?, take?)` | Steps awaiting your approval: assignment is via approvals, not an assignee |
| `workflow(id)` | One workflow by ID |
| `workflows(itemType, itemId, search?, skip?, take?)` | Workflows for an item |
| `workflowTemplate(id)` | One workflow template by ID |
| `workflowTemplatesPage(skip?, take?, search?, itemTypeId?, itemTypeIds?, isActive?)` | Paginated template catalog with matching totals |
| `workflowTemplateStepItemLinks(templateId, diagramNodeId)` | Native item links on a template node |
| `workflowTemplates(skip?, take?, itemTypeId?, itemTypeSlug?, isActive?)` | List workflow templates: `take` is capped at 100; page with `skip` |
| `step(id)` | One step by ID |
| `stepByDiagramNode(workflowId, diagramNodeId)` | The step for a diagram node |
| `stepApprovers(stepId)` | The approvers for a step |
| `workflowNodeState(workflowId, nodeId)` | State of a diagram node |
| `allSteps(status?, nameContains?, overdue?, workflowStatus?, domain?, hostItemType?, dashboardDetailType?, overdueAt?, skip?, take?)` | Steps across workflows |
| `allWorkflows(itemType?, status?, ownerId?, domain?, hostItemType?, dashboardDetailType?, skip?, take?)` | Workflows across item types |
| `workflowStats(itemType?, status?)` | Workflow and step progress |

### Documents

| Signature | Purpose |
|---|---|
| `documentDownload(documentId)` | Download metadata for a permitted step or item-field document |

### Forms

| Signature | Purpose |
|---|---|
| `myFormAssignments` | Forms assigned to you |
| `formAssignmentsByStep(stepId)` | Form assignments for a step |
| `previewFormAssignments(stepId, emails)` | Preview form assignments before sending |
| `formStatusReport` | Status of form assignments |

### Suggestions

| Signature | Purpose |
|---|---|
| `suggestion(id, expectedWorkflowId?, expectedParentItemId?)` | One suggestion by ID |
| `mySuggestions(status?, itemType?, skip?, take?)` | Suggestions you created |
| `myPendingSuggestions(skip?, take?)` | Your suggestions still pending review |
| `suggestionsForItem(itemType, itemId, skip?, take?)` | Suggestions targeting an item |
| `myPendingSuggestionCount` | Count of your pending suggestions |
| `mySuggestionStatusCounts` | Your suggestion counts by status |
| `suggestionStats(agentId?)` | Suggestion volume and approval rate |
| `suggestionsByUser` | Suggestion counts by user |
| `suggestionsTimeline` | Suggestion activity over time |

### Dashboards and Visualization

| Signature | Purpose |
|---|---|
| `dashboards(skip?, take?)` | List dashboards |
| `dashboard(id)` | One dashboard by ID |
| `activityTimeline(itemTypes?, actions?, fieldFilters?, startDate?, endDate?, limit?, offset?, after?, userIds?)` | Activity events over a date range |
| `universeData(includeSteps?)` | Data behind the Universe dashboard |
| `universeActivity(startDate, endDate)` | Universe activity over a date range |

### Time Keeping

| Signature | Purpose |
|---|---|
| `myTimeEntries(weekStart)` | Your time entries for a week |
| `myWeeklyTimesheet(weekStart)` | Your timesheet for a week |
| `timeEntry(id)` | One time entry by ID |
| `timeEntries(userId?, itemId?, weekStart?, status?, skip?, take?)` | Time entries across users and items |
| `pendingTimeApprovals(skip?, take?)` | Time entries awaiting your approval |
| `timeEntryStats(weekStart?, userId?)` | Logged-time totals and breakdowns |

### People

| Signature | Purpose |
|---|---|
| `users(itemType?, itemId?, search?, searchQuery?, skip?, take?, role?, includeInactive?, includeExternal?)` | List users |
| `entityPersonnel(entityType, entityId)` | People associated with an entity |
| `itemRoles(itemType, itemId)` | Roles on an item |
| `itemRoleCount(itemType, itemId)` | Count of roles on an item |

### Custom Lists

| Signature | Purpose |
|---|---|
| `customList(id)` | One custom list by ID |
| `customLists(category?, includeInactive?, isSystem?, searchQuery?, skip?, take?)` | List custom lists |
| `customListValues(category)` | Values in a custom list category |
| `customListCategories` | All custom list categories |
| `customListByValue(category, value)` | Look up a custom list entry by its value |

### Settings and Administration

| Signature | Purpose |
|---|---|
| `systemSettings(category?)` | System settings, optionally by category |
| `systemSetting(key)` | One system setting by key |
| `systemSettingCategories` | Available setting categories |
| `brandingSettings` | Tenant branding settings |
| `allowedSsoDomains` | Email domains allowed to sign in via SSO |
| `oauthClients(includeInactive?)` | Registered OAuth clients |
| `oauthClient(id)` | One OAuth client by ID |
| `popularOAuthClients` | Commonly used OAuth clients |
| `adminActivityLogs(entityTypes?, actionTypes?, userId?, startDate?, endDate?, limit?, offset?)` | Admin activity history |
| `adminEntityTypes` | Entity types available to admin activity filters |
| `userPageAccess(userId)` | A user's page access grants |
| `userItemPermissions(userId)` | A user's item permissions |

### Reports and Exports

| Signature | Purpose |
|---|---|
| `dueDateReport(daysAhead?, includeItems?, includeSteps?)` | What's overdue or coming up |
| `teamWorkloadStats(itemTypes?)` | Open work broken down by person |
| `dataExport(exportId)` | Fresh signed download link for a prior [query_data](https://docs.assureswarm.com/mcp/query_data/) export |

### Additional read queries

These complete the current `get_schema.queryReference` catalog. Availability
still depends on the connected user’s access.

| Signature | Purpose |
|---|---|
| `itemTypeDashboardSnapshot(itemTypeSlug, range, populationFilters?)` | Read the standard monthly-status dashboard for an active item type. |
| `itemTypeDashboardDetails(itemTypeSlug, range, populationFilters?, frameId, partitionId, now, skip, take)` | Page the records behind an item-type dashboard status/month cell. |
| `systemDashboardTable(type, tableId, scope?, range, search?, sortKey?, sortDirection?, cursor?, pageSize?, filters?, entityId?)` | Read a permitted analytical dashboard table with search, filters, sorting, and cursor pagination. |
| `mcpTask(id)` | Fetch one durable MCP task by id (creator or admin; null otherwise). |
| `myMcpTasks(status?, take?)` | List my durable MCP tasks, newest first (admins see all). |
| `myItemsUnion(page?, limit?, search?, sources?, statuses?, itemTypes?)` | List owned and shared items as one paginated result, with optional source, status, item-type, and search filters. |
| `dashboardsPage(page?, limit?, search?, types?, visibilities?)` | Search and page the visible dashboard list (favorites first) with an exact total; optional exact type and PUBLIC/PRIVATE visibility filters. |
| `myTimeEntryCalendarAggregate(rangeStart, rangeEnd, bucketMode)` | Aggregate the current user's time entries across a clipped calendar range and bucket mode. |
| `itemTemplateLinks(itemType, itemId)` | List workflow-template links for an item. |
| `instanceEdition` | Get this instance's feature edition: "studio" or "masterpiece" (requires a signed-in actor). |
| `formFollowup(status?, stepName?, templateId?, domain?, hostItemType?, asOf?, sentFrom?, sentTo?, dashboardDetailType?)` | Status of forms sent to recipients: the Form Follow-up system dashboard. |
| `dashboardTypes` | Distinct dashboard type facets visible to the caller (same gating as the dashboards list). |
| `controlsOverview` | Control library rolled up by line of defense: the Controls system dashboard. |
| `risksOverview` | Risk register: the Risks system dashboard. |
| `issuesOverview` | Findings & remediation: the Issues system dashboard. |
| `auditsOverview` | Audit plan: the Audits system dashboard. |
| `policiesOverview` | Policy governance: the Policies system dashboard. |
| `systemsOverview` | Systems & third-party register: the Systems system dashboard (the v10 `system` item type; the vendor Boolean separates third parties from internal systems). |
| `universeFocus(input)` | Resolve one node's neighbourhood for the Universe dashboard focus mode: input { focus: nodeId, depth: 1-6, kinds?: [typeSlug] | null, hops?: [typeSlug] }. |
| `myWork` | The acting user's personal work queues: tasks (every assigned approval + form, ready and waiting, with ready/waitingOn/itemId), the ready-only pendingApprovals/openForms lists, items due soon, actionable suggestions, plus counts. |
| `openRequests` | Outstanding form assignments and pending approvals (the org-wide outbox): KPIs, turnaround buckets, and the waiting list. |
| `workflowOperations` | Operational view of running workflow instances: stage distribution, overdue steps, median cycle time, and bottleneck steps by dwell. |
| `capacityMonitoring` | Open workload by person across running workflows: actionable-now vs queued step counts, overdue, due-next-7-days, and oldest-waiting per user. |
| `aiSuggestionStats(filter?)` | AI suggestion outcomes: status counts, weekly buckets, approval rate, median time-to-decision. |
| `agentUsageStats(filter?)` | Agent tool-call usage from AgentActionLog: per-day by tool and totals by client (auth preamble rows excluded). |
| `aiSuggestionList(filter?, cursor?, limit?)` | Paged AI-suggestion drill-through rows with preview links. |
| `systemDashboardPopulationFilterFields(type)` | Read the dashboard-authorized live population-filter vocabulary for Controls, Risks, Issues, Audits, Policies, or Systems from the corresponding item type. |
| `systemDashboardSnapshot(type, scope?, range, sections?, entityId?, populationFilters?)` | Read one authorized north-star system-dashboard snapshot. |
| `personnelDashboard(focusId?, templateId?, first?, after?)` | Read a bounded personnel org chart with the focused person, visible parent, and a keyset page of at most 24 direct reports (6 by default). |
| `personnelDashboardPeople(search, first?)` | Search visible Personnel items for org-chart navigation. |
| `personnelDashboardTemplates(search?, first?)` | Search workflow templates available to the current viewer for Personnel progress. |
| `workflowCoverageDashboard(contextItemType, relatedItemType, contextItemId?)` | Read workflow coverage for visible items directly related to a selected reporting context. |
| `dashboardMyWorkDetails(now, scopeKind, scopeValue?)` | Read the authorized north-star My Work drill-down source at one snapshot instant. |
| `dashboardCapacityDetails(late, now, ownerId?, scopeKind, scopeValue?, segment?, skip, take)` | Page exact owner-step workload units for the north-star Capacity drill-down, optionally narrowed to one owner and explicit timeliness segment. |
| `dashboardRegisterStateDetails(dashboardType, now, rangeFrom, rangeTo, scopeKind, scopeValue?, skip, state, take, tier?, populationFilters?)` | Page exact register-state populations for north-star drilldowns. |

## Workflow-step pagination

Running workflow steps use cursor pagination. Read `pageInfo` and continue
until `hasNextPage` is false before exporting a workflow or checking every
predecessor. The default first page contains at most 100 steps.

```graphql
query WorkflowSteps($id: String!, $after: String) {
  workflow(id: $id) {
    id
    steps(first: 100, after: $after) {
      nodes { id diagramNodeId name status }
      pageInfo { hasNextPage endCursor }
    }
  }
}
```

Start with `after: null`, then reuse `endCursor` while `hasNextPage` is true.
If a required predecessor cannot be resolved, stop work on its dependent step.
Template nodes are JSON, while instantiated workflow steps use this connection.

## Access Notes

Every query runs as the connected user, under their permissions and the token's scopes. Some fields are admin-flavored and require access you may not have: they fail or return nothing for non-admins. Treat those denials as expected, not as bugs.

:::note[Permissions still apply]
A token never grants more than the connected user already has. Scopes narrow what a query can do; the user's own page access and item permissions still apply underneath.
:::
