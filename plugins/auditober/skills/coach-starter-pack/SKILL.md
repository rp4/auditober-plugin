---
name: coach-starter-pack
description: "Use when the user requests the current Studio starter schema or a checked bulk-import preview from an explicitly supplied JSON file."
uxContract: 1
hostContract: 1
---

# Coach Starter Pack

Prepare an import for admin review. No tenant write occurs in this skill.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Read ../../references/schema-discovery.md for current tenant schema reads.

Check package-manifest.json before naming commands or resources. If this
skill or its input resource is absent, give the supported admin/library
path; do not advertise an excluded skill.

The Studio baseline has 11 types: audit, risk, control, issue, remediation,
process, policy, system, fsli, requirement, personnel. Preserve the real
audit slug when explaining an engagement or assessment cycle. Vendor records
use system.vendor = true. Live tenant customization remains authoritative.

starter-packs/inventory.json ships core.json only. The named audit, grc,
reg, sox and generic overlays are retired. Reject those selections with
the current core or workflow-library alternative. Historical files are
source history, not supported imports. Never map authority_source to
requirement automatically.

Use scripts/prepare_import.py through detected Python execution. It reads
the JSON locally and returns compact counts and the proposed change summary;
do not load the whole core into the conversation. Existing type definitions
are preserved wholesale. The helper does not add missing fields to existing
types or claim item-level idempotency. Deliberate schema extensions need a
separate reviewed admin change.

An explicit --from selects the supplied envelope as its own import, not
an implicit merge with the core. Validate it against declared types and
current typed schemas for existing types. Invalid types, fields, options,
or shapes must be corrected before presenting a prepared artifact.

The helper checks local envelope and field contracts. Admin import preview
still checks permissions, existing item matches, graph/reference validity,
and other product-specific constraints. Report this boundary alongside
the artifact. Run current schema validation when that capability exists.

If execution is unavailable, state awaiting_runner and provide the exact
helper invocation/input handoff plus the existing canonical source and
verified admin Bulk Import link. Do not claim a filtered or validated file.
If artifact delivery is unavailable, give the source/admin path and state
what remains. The admin decides whether to apply the reviewed import.
```

## Inputs

- `--core-only`: current schema-only core; also the default.
- `--from <path>`: explicit custom JSON envelope, validated as supplied.
- `--dry-run`: preview counts and changes without writing an artifact.
- Legacy positional `audit|grc|reg|sox|generic`: rejected as retired.

## Procedure

1. Verify the active tenant and user from the connection. Discover types
   once, then read only the typed schemas needed to assess existing types.
   Use the session rules in schema-discovery.md; an old schema.json is not
   current evidence.
2. Store a temporary helper input containing `tenant_key`, `session_id`,
   and `types` keyed by slug, with each type's normalized `fields` and
   `lifecycle`. Bind it to the verified origin/tenant/user and this session.
   It is execution input, not a persistent schema shortcut.
3. Run the helper, omitting `--out` for a dry run:

   ```text
   python scripts/prepare_import.py --schema <current-projection.json> --tenant-key <verified-key> --session-id <current-session> --out <downloadable-import.json>
   ```

   Add `--from <supplied.json>` for a custom import. Use `--empty-tenant`
   instead of schema arguments only after complete live discovery verifies
   an empty type catalog. The helper paths are relative to this skill.
4. Present type, field, item, template, relationship and custom-list counts,
   preserved types, and any validation failure. Do not omit errors or
   describe a customized tenant as canonical.
5. On success, return the artifact through the host's supported delivery
   mechanism and the verified tenant's `/en/admin/bulk-import` link.
   State that the admin preview and application remain. Do not ask a
   completion question or apply the import.

## Notes

The bundled core has no sample items, workflows, or dashboards. Current
templates come from https://assureswarm.com/workflows/ and are resolved by
the workflow skills that actually ship in package-manifest.json. Review
their purpose and checkpoint design before importing or attaching them.
