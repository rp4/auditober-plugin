---
title: query_data
description: "Run read-only GraphQL queries: with variables, size limits, and CSV/JSONL export for large results."
---

Use `query_data` to run read-only GraphQL queries against your tenant's data: the same schema `get_schema` documents, with variables, size limits, and export for results too large to return inline.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `query` | string | Yes | A read-only GraphQL query, ≤ 64 KB. Anything starting with `mutation` or `subscription` is rejected. |
| `variables` | object | No | Variables referenced by the query. |
| `export` | object | No | Large-result export: `{ "format": "csv" }` or `{ "format": "jsonl" }`. |
| `async` | boolean | No | Queue a durable export task; supply `export.format`. |

`query_data` requires the `read:data` scope.

## Read-Only Enforcement

`query_data` only runs read operations: a query whose top-level operation is `mutation` or `subscription` is rejected before it executes. Use [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) to propose writes instead; those still route through human review before anything changes.

## Examples

**List item types.** Get every item type's slug and name in one call.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query ListTypes { itemTypes { slug name } }"
  }
}
```

**Paginated items.** `items` returns a paginated object, not a bare list: read the nested `items` field for the rows.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query OpenIssues($itemType: String!, $limit: Int) { items(itemType: $itemType, limit: $limit) { items { id title status } total page totalPages } }",
    "variables": { "itemType": "issue", "limit": 10 }
  }
}
```

`total` is the full matching count regardless of page size: prefer `itemStats` when you only need a count.

**Counting without paging.** Use `itemStats` for counts and status breakdowns without paging through items.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query Counts($itemType: String) { itemStats(itemType: $itemType) { totalCount overdueCount byStatus { group label count } } }",
    "variables": { "itemType": "issue" }
  }
}
```

**Large export.** Add `export` when a result set is too large to return inline.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query AllOpen { allItems(status: \"OPEN\") { id title status } }",
    "export": { "format": "csv" }
  }
}
```

**List workflow templates.** Get every template's name and description in one call. `take` is capped at 100: page with `skip` for larger libraries.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query Templates { workflowTemplates(take: 100, isActive: true) { id name description itemTypeId isActive } }"
  }
}
```

**Full template detail.** A template's steps and flow map are stored as JSON on the record, not as a nested field selection: `nodes` is the array of steps (each node's `data` carries its `label`, `description`, and any `formData.fields` form schema) and `edges` is the diagram map (source → target, with labels on branch edges).

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query Template($id: String!) { workflowTemplate(id: $id) { id name description nodes edges metadata } }",
    "variables": { "id": "TEMPLATE_ID" }
  }
}
```

`nodes`, `edges`, and `metadata` come back as raw JSON: parse them client-side to walk the steps and branching. (Templates hold steps as JSON; a running [workflow](https://docs.assureswarm.com/graphql/) instead exposes its steps as queryable rows via `step`, `allSteps`, and related fields.)

## Large Results and Export

Tool responses are capped at 2 MB. If a result is close to or over that limit, narrow the field selection, page it with `items`/`limit`, or set `export`.

With `export.format` set, `query_data` writes the full result to a downloadable file. The response itself carries a sample of rows, a signed `download` URL, and metadata such as the row count: not the full dataset inline. Download links expire; fetch a fresh one anytime with the `dataExport(exportId)` query. Exports also note whether the result was truncated.

## Asynchronous exports

Set `async: true` with `export.format` to queue work and receive a task ID.
Without the format, the server asks for it rather than starting the export.
Use [get_task_status](https://docs.assureswarm.com/mcp/get_task_status/) to poll, then
[get_task_result](https://docs.assureswarm.com/mcp/get_task_result/) when the status is `succeeded`.
Stop polling on `failed` or `cancelled`; inspect the reported error.
[cancel_task](https://docs.assureswarm.com/mcp/cancel_task/) stops a queued or running task you own.

```json
{
  "name": "query_data",
  "arguments": {
    "query": "query Types { itemTypes { slug name } }",
    "export": { "format": "jsonl" },
    "async": true
  }
}
```

Large export responses use `resource` and `download` for the artifact URI and
signed download URL. Task result reads refresh the signed link while the
artifact remains available; rerun the query if the artifact has expired.

## Query Discovery

`get_schema`'s `queryReference` field returns the full catalog of read query fields and their signatures: every field you can put inside a `query_data` call. The same catalog is documented in full on [GraphQL](https://docs.assureswarm.com/graphql/).

## Agent Notes

- Narrow field selections to what you need.
- Prefer `variables` over string-interpolating values into the query.
- Use stats fields like `itemStats` for aggregates instead of paging through every item.
- Use [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) for writes: `query_data` never mutates data.
