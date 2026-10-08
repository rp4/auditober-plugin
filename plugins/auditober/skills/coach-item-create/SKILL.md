---
name: coach-item-create
description: "Use whenever the user asks to create, add, draft, or open a new item of a known type (e.g., audit, risk, control, issue, policy, process). Works for any admin-configured item type: reads the type's schema via get_schema, gathers required fields interactively if not supplied, validates values against field definitions, and submits a single suggest_change action create suggestion for human approval."
uxContract: 1
hostContract: 1
---

# Coach Item Create

Create a single item of any item type. Schema-driven validation. One suggestion per call.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first. Ask only for missing necessary inputs through
the detected question UI or plain text. Discover filesystem, execution and
artifact delivery before promising a file. Use awaiting_runner only when the
requested operation needs execution and no runner is available.

Read ../../references/schema-discovery.md before schema discovery. Use typed
get_schema for a known item slug or mutation target; reuse its tenant/type/session
cache and refresh on the invalidation events defined there.

You are the item-create skill. The user wants to create a new item of an
admin-configured item type. Your job is to read the type's schema, gather
required field values from the conversation or through the detected question UI or plain text, and emit
ONE suggest_change call in the canonical create shape so the assignee sees
the suggestion preview and can approve.

The correct shape is exactly:

  suggest_change({
    action: "create",
    itemType: "<slug>",
    data: { fields: { "<fieldKey>": <value>, ... } },
    reason: "<one short sentence on why this item is being created>"
  })

The "itemType" is the item type's slug (e.g., "audit", "risk", "control",
"issue"). The "fields" map uses the schema's field keys exactly —
case-sensitive, no aliases. MULTISELECT fields take an array of option
values. DATE fields take an ISO 8601 date string. USER fields take a user
id. DOCUMENT fields take NO value here — canvas rejects the create with
"<Label> uploads after item creation"; the file goes up afterwards via
upload_document. Relationships are not fields either: link the new item to
another one after it exists, with /coach-items-link.

Procedure:

  1. Call get_schema(type: "<slug>") for the known item type's field definitions. If the
     user named a type that does not exist in the schema, refuse with the
     unknown-type visible turn and offer to pick a valid type when the intended type remains unclear.

  2. Walk the schema's fields. For each `required: true` field, check the
     conversation or arguments for a value. If absent, ask to
     gather it. For SELECT and MULTISELECT, use the option values as the
     choices. For BOOLEAN, two options. For free-text, ask without options.
     Skip DOCUMENT fields entirely — never ask for one and never put one
     in the payload, even when the schema marks it required.

  3. Optional fields. Do not interrogate the user for every optional field
     — that becomes a multi-page form. Include any optional values the user
     has already provided in the conversation; leave the rest unset.

  4. Validate. The skill itself does not need to re-validate (suggest_change
     does that), but catch obvious errors before the call — e.g., an
     unrecognized SELECT value, a date that is not ISO 8601, an empty
     required string. Show the error verbatim and ask to fix.

  5. Call suggest_change with the canonical shape above. If it returns a
     validation error, show the error verbatim and ask to
     resolve. Do not silently coerce values.

  6. Hand off with one-line summary, the action link wrapping previewUrl.

Follow the shared host contract for tool announcements, concise results,
artifact delivery, pending states and human approval.

```

## Inputs

- `--type <slug>` — item type slug (e.g., `audit`, `risk`, `control`). If
  absent, ask the user.
- `--values <json>` — optional, a JSON object of field keys to values. If
  partial, gather the rest interactively.
- `--reason <text>` — optional, one sentence for the suggestion's reason
  field; helps the approver decide whether to accept.

## Procedure

1. Call `get_schema(type: "<slug>")` for the known type. If it does not exist,
   refuse through the detected question UI or plain text offering the closest valid types as picks.
2. Build the values map. For each `required: true` field on the type:
   - If the user provided a value (in args or conversation), use it.
   - If not, ask to gather it. SELECT and MULTISELECT use the
     schema's options; free-text uses a single open question.
3. Include any optional field values the user has already supplied. Don't
   interrogate for every optional field.
4. Call:

       suggest_change({
         action: "create",
         itemType: "<slug>",
         data: { fields: { ... } },
         reason: "<short why>"
       })

5. On validation error, show the error verbatim and ask to
   resolve.
6. Hand off with summary + `[Review and approve](<previewUrl>)`.

## Notes

- Field key case sensitivity. The schema's field keys are case-sensitive.
  `phase` is not `Phase` is not `PHASE`. Use the schema's exact case.
- Relationships are not fields. There is no RELATION or RELATIONS
  fieldType — an item-to-item link is an `itemrelationship` row created by
  its own `suggest_change` (`create` / `delete` only). If the user says
  "create this issue and link it to the control", create the item here,
  then hand off to `/coach-items-link` for the link.
- DOCUMENT fields. One document per (item, fieldKey), and the value cannot
  be set at create time — `suggest_change` fails with "<Label> uploads
  after item creation". Create the item first, then upload with
  `upload_document` targeting `{ type: "item_field", itemId, fieldKey }`
  (see `/coach-document-upload --item`). Each upload replaces the current
  document.
- MULTISELECT field values. Pass an array of option `value` strings, not
  labels. The schema's options each have `{ value, label }`; use `value`.
- DATE and DATETIME fields. Use ISO 8601: `YYYY-MM-DD` for DATE,
  `YYYY-MM-DDTHH:mm:ssZ` for DATETIME. Reject anything else upfront.
- USER fields. The value is the user's id. Use `query_data` with
  `users(searchQuery: "...")` to resolve a name or email to an id.
- Title. Almost every item type has a required `title` field. If the user
  describes the item clearly, use a short factual title in the suggestion
  preview. Ask only when the intended item or title remains ambiguous.
- This skill creates one item. To create many at once (e.g., a starter
  pack), use the admin Bulk Import page at `/en/admin/bulk-import`. That
  path is not gated by `suggest_change`.
