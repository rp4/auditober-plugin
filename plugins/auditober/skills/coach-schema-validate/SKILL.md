---
name: coach-schema-validate
description: "Use when the user asks to validate, lint, or check a schema JSON file before pasting it into the Bulk Import admin page. Lints against the platform's bulk-import format — catching missing data wrapper, slug collisions, invalid field types (including the retired RELATION / RELATIONS), missing required keys, leftover relatedItemTypeSlug keys, and search-flag combinations rejected at import — and reports every issue with file path and field path."
uxContract: 1
hostContract: 1
---

# Coach Schema Validate

The pre-flight check before pasting JSON into the Bulk Import admin page.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first. Ask only for missing necessary inputs through
the detected question UI or plain text. Discover filesystem, execution and
artifact delivery before promising a file. Use awaiting_runner only when the
requested operation needs execution and no runner is available.

You are the schema-validate skill. Read a schema JSON file and
report every violation against the platform's bulk-import contract
(the input shape accepted by /api/admin/import and the Bulk Import
admin page).

Be specific: file path and field path on every issue. Distinguish
errors (will fail import) from warnings (will succeed but is
probably a mistake).

Follow the shared host contract for tool announcements, concise results,
artifact delivery, pending states and human approval.

```

## Inputs

- `--file <path>` — required, the schema JSON to lint

## Procedure

1. Parse the JSON; bail if parse fails.
2. Run checks. Anything in the "errors" group below is a hard
   ERROR (will cause the bulk-import endpoint to either reject the
   payload or silently no-op a section). Warnings are best-practice
   issues that still import cleanly.
   - **Top-level (errors)**:
     - `data` object is present. The endpoint returns 400 "missing
       data field" without it.
     - `data.itemTypes`, if present, is an array.
     - `data.items`, if present, is a plain object keyed by item-type
       slug. ERROR if it is an array — the endpoint iterates
       `Object.entries`, treats array indices "0", "1", … as slugs,
       finds no match, and records one error per item with no items
       actually created. The result rendering in the UI shows
       `items: 0: [object Object], 1: [object Object], …`, which is
       the recognizable symptom.
     - `data.customLists`, if present, is an array.
   - **Top-level (warnings)**:
     - `version` is a string (defaulted by the importer if missing).
   - **Each item type** under `data.itemTypes`:
     - slug is lowercase, alphanumeric plus underscore, unique.
     - name and namePlural present.
     - icon is a known Lucide name (lookup against bundled
       lucide-names.json).
     - color is a 7-character hex code starting with #.
     - displayOrder is an integer.
     - The field array may be keyed **either** `FieldDefinition` **or**
       `fieldDefinitions` — the importer resolves
       `row.FieldDefinition ?? row.fieldDefinitions`, so both import
       identically. `FieldDefinition` is the preferred spelling and is
       what the shipped packs should use, but **do NOT flag
       `fieldDefinitions` as an error** — the plugin's own
       `starter-packs/core.json` uses it, and reporting it as broken
       sends people chasing a non-bug.
     - **ERROR** only on the lowercase `fields` array. That one really
       is silently dropped, and the item type imports with zero fields.
       Suggested fix: rename the key to `FieldDefinition`.
   - **Each field** in the field array:
     - fieldKey is camelCase, unique within the item type.
     - label present.
     - fieldType is one of the 13 platform enum values exactly: TEXT,
       TEXTAREA, RICHTEXT, NUMBER, DATE, DATETIME, SELECT,
       MULTISELECT, BOOLEAN, USER, USERS, DOCUMENT, JSON.
     - **ERROR** on any non-enum value, including the common-looking
       wrong values: CHECKBOX (use BOOLEAN), MULTI_SELECT (use
       MULTISELECT), FILE (use DOCUMENT), URL or EMAIL (use TEXT).
       These fail in the importer's own `normalizeFieldType` guard
       (`Unsupported field type: <value>`), before Prisma is involved
       — so look there, not at the database layer, when one gets
       through. Suggested fix per case.
     - **ERROR** on `RELATION`, `RELATIONS`, or `MULTISELECT_RELATION`.
       Relations are no longer a field type — the platform deleted
       every relation FieldDefinition and stripped those keys out of
       item field data, so a schema declaring one now fails import.
       Suggested fix: delete the field definition and model the link
       as an `itemrelationship` suggestion instead (`/coach-items-link`
       — suggest_change `create` / `delete` against
       `itemType: "itemrelationship"`; there is no update).
     - **WARNING** on a leftover `relatedItemTypeSlug` (or the older
       `relationTarget`) key on any field. Both are obsolete now that
       the relation types are gone and the importer ignores them.
       Suggested fix: drop the key.
     - SELECT and MULTISELECT have a non-empty options array; each
       option has both value and label.
     - **ERROR** on a DOCUMENT field that carries any of: `required`,
       `isFilterable`, `isSearchable`, `options`, `defaultValue`,
       `validation`, `customListCategory`, `relatedItemTypeSlug`. The
       platform asserts all eight and rejects the import with the
       matching message (`Document fields cannot be required`,
       `… cannot be searchable`, and so on). A DOCUMENT field is a
       bare declaration: one document per (item, fieldKey), uploaded
       after the item exists via `upload_document` with an
       `item_field` target. This is the most likely way a
       well-intentioned DOCUMENT field fails import — `required: true`
       on a mandatory-evidence field looks obviously correct and is
       rejected.
     - isSearchable only true for TEXT, TEXTAREA, RICHTEXT.
     - order is an integer.
3. Custom lists under `data.customLists`:
   - Each entry has `category`, `value`, `label`.
   - sortOrder is an integer if present.
   - Flat array of tuples — not the legacy nested
     `{ category, values: [...] }` shape.
4. Items under `data.items`:
   - **ERROR** if `data.items` is an array. It must be an object
     keyed by item-type slug, with the value being an array of items
     of that type. The common wrong shape is `[{ itemType: "...",
     title: "..." }, ...]`; the right shape is
     `{ "<slug>": [{ title: "...", fields: { ... } }, ...] }`.
   - Each top-level key matches an itemType slug that exists either
     in this file's `data.itemTypes` or in the tenant.
   - Each item has `title`. Optional: `status`, `visibility`,
     `dueDate`, `fields`.
   - **ERROR** if an item's `fields` map carries a value for a
     DOCUMENT field. Documents are never seeded inline — the platform
     rejects the write with "<Label> uploads after item creation".
     Suggested fix: drop the key and upload the file after import via
     `upload_document` with target
     `{ type: "item_field", itemId, fieldKey }`.
5. Cross-reference checks:
   - Every field that references a custom list by category has that
     category present in `customLists`.
   - No field definition anywhere in the file uses `RELATION`,
     `RELATIONS`, or a leftover `relatedItemTypeSlug`. Item-to-item
     links are not schema — they are `itemrelationship` rows created
     after import through suggest_change.

## Output

A markdown report:
- Top: counts (errors, warnings, info)
- Errors section: each error with file path, item type slug, field
  key (if applicable), description, suggested fix
- Warnings section: same shape
- Pass case: a single line confirming the file is ready for
  the Bulk Import admin page

## Notes

- The silent-failure modes that historically bit users — the
  endpoint accepts the upload as 200-success but the data does not
  fully land — are all hard ERRORS now: lowercase `fields` instead
  of `FieldDefinition`, `items` as an array instead of a
  slug-keyed object, `MULTI_SELECT` or `MULTISELECT_RELATION`
  instead of `MULTISELECT`, and `URL`/`EMAIL` instead of `TEXT`.
- `fieldDefinitions` is NOT one of them. The importer reads
  `row.FieldDefinition ?? row.fieldDefinitions`, so that spelling
  lands correctly; only lowercase `fields` is dropped. A validator
  that errors on `fieldDefinitions` is a false positive — it would
  condemn the plugin's own `starter-packs/core.json`, and a live QA
  run was already misled into reporting exactly that.
- `RELATION` and `RELATIONS` were removed from the field-type enum.
  The migration deleted every relation FieldDefinition and stripped
  those keys out of item field data, so a schema that still declares
  one is an ERROR — and `relatedItemTypeSlug` has nothing left to
  point at. Relationships are `itemrelationship` suggestions
  (`/coach-items-link`), created and deleted through suggest_change;
  there is no update.
- `DOCUMENT` is the newest type: one document per (item, fieldKey),
  declared in the schema but never valued in `data.items`. The file
  lands afterwards through `upload_document` with an `item_field`
  target, and each upload replaces the current document.
- Other common errors: missing top-level `data` wrapper (rejected
  with "missing data field"); slug collisions when adding a starter
  pack on top of an existing schema; an item's `fields` map carrying
  a value for a DOCUMENT field; missing required keys on legacy
  hand-edited schemas.
- The validator never edits the file. It reports; the user fixes;
  re-run.
- Schema, item types, fields, and custom lists are admin-page
  concerns and flow through `/en/admin/bulk-import`, not
  suggest_change.
