# Complete bounded query reads

Read this reference before any complete workflow roster, dependency gate, assignment,
export, document target, dashboard target or template lookup. The tenant schema and
stored graph are authoritative. Query examples substitute resolved tenant IDs.

## Cursor pages

Normal step selections use `first: 25`. Rich export and sweep selections use the
smaller sizes in the checked selections below. The default of 100 is too expensive
for these selections under the production cost limit of 1000.

Select `pageInfo { hasNextPage endCursor }` on every page. Collect nodes by id,
then repeat the same selection with `after: "<endCursor>"` while `hasNextPage`
is true. Require a nonempty, new cursor before each continuation. Finish only on
false. A failed page, GraphQL errors, truncated response, missing or repeating
cursor, missing workflow, or unresolved required predecessor is an incomplete
read. Stop the action and report the blocker; never classify it as an empty
result, execute a step, assign a partial roster, or label an export complete.
An empty first or last page with `hasNextPage: false` is complete.

## Offset pages and name resolution

`allWorkflows`, `workflows`, `workflowTemplates`, `workflowTemplatesPage`,
`users` and `mySuggestions` use `skip/take`. Start at skip:0; keep all filters
and the full selection unchanged; advance skip by the number of rows returned.
Deduplicate by id. Stop at a short page or the API's verified total. When a total
is selected, a short page before that total is an incomplete read. Repeating
pages without new ids, changed totals and GraphQL errors block completion.

Use take:25 for the bounded workflow, suggestion and user selections below.
For a template name, use `workflowTemplatesPage(search: "<name>", skip: 0,
take: 5) { items { id name } total }`; complete its pages before declaring
absence or uniqueness. Read `workflowTemplate(id)` metadata only for narrowed
candidates. `workflowTemplates` has no search argument. If the paged query is
absent from the tenant queryReference, use filtered `workflowTemplates(skip:0,
take:5)` with id/name and complete client-side matching. Catalog source IDs do
not establish a tenant template ID; apply the attachment skill's identity rules.

`dashboardsPage` uses page/limit. Start at page:1, limit:25 and keep search and
filters fixed; advance page by one through the returned totalPages. A missing
page or inconsistent pagination is incomplete. Keep completed dashboards by id
before resolving a name.

`get_current_context.assignedSteps` and `myAssignedSteps` expose a capped queue
without a cursor or offset. Label a mine brief as the returned queue; a full
page cannot establish complete coverage. Do not infer that unreturned work is
absent. For a complete selected workflow, use its cursor roster.

## Graph interpretation

Fetch diagramEdges with the minimal dependency roster. Fetch diagramNodes in a
separate singleton read where graph presence, decisions or critical paths need
interpretation. An explicit graph with nodes and no edges has independent entry
checkpoints. Use stepNumber linear fallback only with evidence of the legacy
representation: the stored graph has no nodes and no edges and the steps have
valid unique integer ordinals for every stored step, with the target matching its
roster entry. Missing or duplicated ordinals anywhere make ordering incomplete. Empty edges alone never establish legacy order.

Resolve each incoming edge's source to a stored diagram node and a fetched step.
All direct predecessors must have status COMPLETED before execution. Missing
sources block the gate even if the other predecessors are completed. Fetch
upstream result bodies and documents with get_step_context only after the complete
roster identifies the predecessors. For decisions, match diagramNodeId to
diagramNodes.id and inspect data.kind, decisionField and branch values; keep that
metadata separate from each step page.

## Checked selections

The complete selections are validated against the real Canvas schema with
`parseAndValidateUnderSecurityPolicy(schema, source, 'production')`. Page sizes
apply to these full selections; adding fields requires validation again.
The historical oversized controls remain in test/fixtures/runtime-queries.json.

### dependency

~~~graphql
{ workflow(id: "contract-test-workflow") { diagramEdges steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status stepNumber diagramNodeId } } } }
~~~

### graph-metadata

~~~graphql
{ workflow(id: "contract-test-workflow") { diagramNodes } }
~~~

### assignment

~~~graphql
{ workflow(id: "contract-test-workflow") { steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status approvedCount requiredApprovals } } } }
~~~

### export

~~~graphql
{ workflow(id: "contract-test-workflow") { id name description status itemId itemType steps(first: 5) { pageInfo { hasNextPage endCursor } nodes { id name description instructions status dueDate approvedCount requiredApprovals approvals { user { id name email } status reviewLevel } } } } }
~~~

### scan

~~~graphql
{ workflow(id: "contract-test-workflow") { id name diagramEdges owners { id name } steps(first: 5) { pageInfo { hasNextPage endCursor } nodes { id name status stepNumber diagramNodeId dueDate updatedAt approvedCount requiredApprovals result { body } approvals { user { id name } status reviewLevel } } } } }
~~~

### document-target

~~~graphql
{ workflow(id: "contract-test-workflow") { steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status } } } }
~~~

### dashboard-step-target

~~~graphql
{ workflow(id: "contract-test-workflow") { steps(first: 25) { nodes { id name } pageInfo { hasNextPage endCursor } } } }
~~~

### template-search

~~~graphql
{ workflowTemplatesPage(search: "review", skip: 0, take: 5) { items { id name } total } }
~~~

### template-metadata

~~~graphql
{ workflowTemplate(id: "contract-test-template") { id name description metadata itemTypeId isActive } }
~~~

### workflow-list

~~~graphql
{ allWorkflows(skip: 0, take: 25) { id name itemId itemType } }
~~~

### item-workflows

~~~graphql
{ workflows(itemType: "audit", itemId: "contract-test-item", skip: 0, take: 25) { id name } }
~~~

### suggestions

~~~graphql
{ mySuggestions(itemType: "step", skip: 0, take: 25) { id targetId agentName status suggestedData createdAt } }
~~~

### user-search

~~~graphql
{ users(searchQuery: "reviewer", skip: 0, take: 25) { id name email } }
~~~

### dashboard-types

~~~graphql
{ dashboardTypes }
~~~

### dashboard-name-search

~~~graphql
{ dashboardsPage(page: 1, limit: 25, search: "review") { items { id name type createdById configJson } page totalPages } }
~~~

### graph-metadata-name

~~~graphql
{ workflow(id: "contract-test-workflow") { name diagramNodes } }
~~~

### template-catalog

~~~graphql
{ workflowTemplates(isActive: true, skip: 0, take: 5) { id name } }
~~~

### query-drilldown

~~~graphql
{ workflow(id: "contract-test-workflow") { id name status steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status stepNumber dueDate } } } }
~~~

### query-singleton

~~~graphql
{ workflow(id: "contract-test-workflow") { id name status steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status } } } }
~~~

### user-name-search

~~~graphql
{ users(search: "reviewer", skip: 0, take: 25) { id name email } }
~~~

### assigned-queue-preview

~~~graphql
{ myAssignedSteps(take: 25) { id name status dueDate workflowId } }
~~~

## Executable paging recipe

Adapt fetch callbacks to query_data responses. Each callback checks the full MCP
envelope for errors or truncation before extracting the selected connection or
list. Missing parent objects raise IncompleteRead. The recipe operates on those
extracted pages; it never handles credentials, changes tenant records or approves
suggestions.

```python
class IncompleteRead(RuntimeError):
    pass

def require_page(response):
    if not isinstance(response, dict) or response.get("errors") or response.get("truncated"):
        raise IncompleteRead("GraphQL errors or malformed page")
    return response

def collect_steps(fetch):
    # fetch(after) returns the selected workflow.steps connection.
    nodes, cursors, after = {}, set(), None
    while True:
        page = require_page(fetch(after))
        info, rows = page.get("pageInfo"), page.get("nodes")
        if not isinstance(info, dict) or not isinstance(rows, list):
            raise IncompleteRead("Missing nodes or pageInfo")
        for node in rows:
            if not isinstance(node, dict) or not node.get("id"):
                raise IncompleteRead("Missing step id")
            nodes[node["id"]] = node
        if info.get("hasNextPage") is False:
            return list(nodes.values())
        cursor = info.get("endCursor")
        if info.get("hasNextPage") is not True or not isinstance(cursor, str) or not cursor.strip() or cursor in cursors:
            raise IncompleteRead("Missing or repeating endCursor")
        cursors.add(cursor)
        after = cursor

def collect_offsets(fetch, take, filters):
    # fetch(skip, take, filters) returns a list or {items, total}.
    if take <= 0:
        raise ValueError("take must be positive")
    skip, nodes = 0, {}
    fixed_filters = dict(filters)
    expected_total = None
    while True:
        response = fetch(skip, take, dict(fixed_filters))
        if isinstance(response, dict):
            response = require_page(response)
            rows, total = response.get("items"), response.get("total")
            if total is not None:
                if type(total) is not int or total < 0 or (expected_total is not None and total != expected_total):
                    raise IncompleteRead("Changing or invalid total")
                expected_total = total
        else:
            rows = response
        if not isinstance(rows, list):
            raise IncompleteRead("Missing offset rows")
        previous_count = len(nodes)
        for node in rows:
            if not isinstance(node, dict) or not node.get("id"):
                raise IncompleteRead("Missing row id")
            nodes[node["id"]] = node
        if rows and len(nodes) == previous_count:
            raise IncompleteRead("Offset pages repeat without new ids")
        if expected_total is not None and len(nodes) == expected_total:
            return list(nodes.values())
        if expected_total is not None and len(nodes) > expected_total:
            raise IncompleteRead("Rows exceed verified total")
        if len(rows) < take:
            if expected_total is not None and len(nodes) != expected_total:
                raise IncompleteRead("Short page before verified total")
            return list(nodes.values())
        skip += len(rows)

def direct_upstream(step, steps, edges, diagram_nodes, legacy_linear=False):
    if not isinstance(edges, list) or not isinstance(diagram_nodes, list):
        raise IncompleteRead("Missing graph representation")
    by_node = {}
    for row in steps:
        node_id = row.get("diagramNodeId")
        if node_id:
            if node_id in by_node and by_node[node_id]["id"] != row["id"]:
                raise IncompleteRead("Multiple steps for one diagram node")
            by_node[node_id] = row
    if not diagram_nodes:
        if edges or not legacy_linear:
            raise IncompleteRead("Unverified legacy representation")
        by_id, by_ordinal = {}, {}
        for row in steps:
            row_id, ordinal = row.get("id"), row.get("stepNumber")
            if not row_id or row_id in by_id or type(ordinal) is not int or ordinal < 0 or ordinal in by_ordinal:
                raise IncompleteRead("Invalid or ambiguous legacy roster")
            by_id[row_id] = row
            by_ordinal[ordinal] = row
        stored_target = by_id.get(step.get("id"))
        if (stored_target is None or type(step.get("stepNumber")) is not int
                or stored_target["stepNumber"] != step["stepNumber"]
                or stored_target.get("diagramNodeId") != step.get("diagramNodeId")):
            raise IncompleteRead("Target disagrees with legacy roster")
        earlier = [ordinal for ordinal in by_ordinal if ordinal < step["stepNumber"]]
        return [by_ordinal[max(earlier)]] if earlier else []
    node_ids = {node.get("id") for node in diagram_nodes}
    if step.get("diagramNodeId") not in node_ids:
        raise IncompleteRead("Target absent from graph")
    predecessors = []
    for edge in edges:
        if edge.get("target") == step["diagramNodeId"]:
            source = edge.get("source")
            if source not in node_ids or source not in by_node:
                raise IncompleteRead("Unresolved required predecessor")
            if by_node[source] not in predecessors:
                predecessors.append(by_node[source])
    return predecessors

def decision_node(step, diagram_nodes):
    matches = [node for node in diagram_nodes if node.get("id") == step.get("diagramNodeId")]
    if len(matches) != 1:
        raise IncompleteRead("Unresolved decision metadata")
    return matches[0] if matches[0].get("data", {}).get("kind") == "decision" else None

```
