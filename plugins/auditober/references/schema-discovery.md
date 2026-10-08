# Schema discovery

Read the smallest schema needed, then reuse that response within the current
task/session. This contract applies with or without a filesystem.

## Pick the read

| Need | Read |
| --- | --- |
| Known item slug | `get_schema(type: "<slug>")` |
| Known mutation target | `get_schema(type: "itemrelationship")`, `stepdocumentlink`, or the actual target |
| Unknown item type or query signatures | One unscoped `get_schema` for discovery or `queryReference` |

Only the unscoped response contains `queryReference`. Its item summaries omit
option arrays and default statuses. They cannot validate SELECT values. After
discovering a slug, read its typed response once. Reserved mutation targets
return `targetType` and fields; item types return `itemType` and fields. Keep
these response kinds separate. Check the actual tool result before using it.

## Session cache

Keep each successful raw response and normalized projection under this policy:

```json
{
  "cache_key": ["tenant", "session", "kind", "type"],
  "storage": "session_memory",
  "persistent_write_shortcut": false,
  "invalidate_on": [
    "tenant_switch", "session_change", "schema_change", "import_change",
    "validation_failure", "explicit_refresh"
  ]
}
```

Use the verified endpoint/tenant identity and current user for the tenant key,
the current task/session identity, response kind, and exact type or discovery
marker. A changed user/permission scope also starts a new cache. A second use
of the same type in this session reuses the cached response. A schema import
invalidates affected entries; if its scope is unknown, clear the tenant cache.
After a validation failure, evict the relevant entry and read it again before
offering corrected values. Failed or partial responses never populate the cache.

A local snapshot can record diagnostics, source metadata, and fingerprints.
It does not prove freshness. Without a server revision, every new session
reads each type it needs before a write or suggestion. File age, matching
endpoint text, and the vendored fingerprint do not waive that read. When no
filesystem exists, keep the same cache in conversation/session memory; do not
claim it will survive the session.

## Normalize what the response exposes

For each item type, retain its slug; each field's exact fieldKey, fieldType,
required flag, and option values; and the lifecycle default and status options.
Move the protected `status` SELECT out of custom fields into
`lifecycle.statuses`. Sort field keys and option values and deduplicate option
values; accept strings or objects with a string `value`. Exclude tenant-local
IDs, labels, descriptions, display order, and timestamps. Unsupported option
shapes or a malformed status definition require a corrected read.

The projection is `{slug, fields: {key: {type, required, options}},
lifecycle: {defaultStatus, statuses}}`. A missing status definition means
`statuses: null`, not an empty vocabulary or a singleton inferred from the
default. Hash compact UTF-8 JSON with sorted keys using SHA-256. Keep raw
metadata for display and validation details the projection does not represent.
The dev verifier is `test/tools/sync_studio_schema.py`.

For mutation targets retain the exposed target kind, operations, field types,
requiredness, and options in a separate cache entry. Do not compare a target
schema with an item-type fingerprint.

## Lifecycle and pinned values

The tenant's protected `status` field is the lifecycle authority. Typed
`get_schema` includes its options when that definition exists. If absent,
read `itemType(slug: "<slug>") { coreFields { fieldKey fieldType options } }`
to look for the status definition. If still unavailable, do not invent a
transition. `defaultStatus` chooses the initial value; it is not a vocabulary.

The vendored Studio reference records its schema artifact/version/hash and
normalized fingerprints. Canonical schema-only exports omit protected status
definitions. Their `lifecycle.statuses` stays null. Separate
`lifecycleProfiles` record the expected result of a named fresh seed import:
declared options plus the default plus statuses present in that seed, following
the cited importer source and hash. Existing tenant data or options may expand
that result. This import provenance is not proof of any current tenant's schema.

Before using pinned `itgc_domain`, `tier`, `issue_type`, or other options,
compare the relevant type's current projection. Use an import profile only
when its exact source/context is established; construct an expected projection
with those statuses and compare it to the live definition. Match all exposed
custom fields, requiredness, options, default, and statuses. A match permits
reuse of canonical mappings for this session. Unknown lifecycle evidence or
any mismatch selects the customized-schema path: use live keys/options and
required fields, ask only for missing necessary values, and explain any
unavailable operation. Never add fields or coerce values to make a tenant
match the fixture.

For planning, verified statuses such as PLANNING, FIELDWORK, and REPORTING can
narrow candidates. If suitable statuses are unknown, list the audit type with
bounded complete pagination and resolve the engagement from those results.
Do not turn an unverified PLANNED filter into a claim that no audit exists.

## Cache recipe

This in-memory recipe illustrates the cache policy; the host may keep the same
record in session context. `fetch` must return a complete successful response
or raise. It contains no filesystem operation.

```python
def schema_for(cache, tenant, session, kind, type_name, fetch, invalidate=False):
    if invalidate:
        cache.clear()
    key = (tenant, session, kind, type_name)
    if key not in cache:
        cache[key] = fetch(type_name)
    return cache[key]
```
