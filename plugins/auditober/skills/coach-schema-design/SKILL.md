---
name: coach-schema-design
description: "Use when the user asks to design, plan, or draft a Canvas schema — figuring out what item types and fields to set up for their domain; to add fields to an existing item type; to add a single new item type to an existing schema; to build the options for a SELECT or MULTISELECT field — an enum-style option list such as severity, status, frequency, regulators, regions, or audit-phase; or to export, back up, dump, or diff the current tenant's schema, or migrate it to another tenant. Five modes on one skill: the full design interview by default, plus --add-field, --add-type, --options, and --export for incremental changes."
uxContract: 1
hostContract: 1
---

# Coach Schema Design

The biggest hurdle in AssureSwarm onboarding is figuring out what item
types and fields to set up — the default mode drives that interview and
produces a complete JSON that an admin can paste into the Bulk Import
admin page. Four incremental modes (`--add-field`, `--add-type`,
`--options`, `--export`) handle every later schema change through the
same file format.

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

You are the schema-authoring skill — one skill, five modes. With no
flag, run the full design interview: interview the user about their
work domain, then produce a complete Canvas schema JSON. With
--add-field <type-slug>, add fields to an existing item type. With
--add-type, add one item type to the existing schema with a
sensible initial field set. With --options, produce option arrays
for SELECT and MULTISELECT fields, either by picking a canned
template or defining options interactively. With --export, call
get_schema and write the live tenant schema to a versioned JSON
file in the workspace schemas folder. Every mode reads and writes
the bulk-import shape consumed by /api/admin/import and the Bulk
Import admin page.

The workspace schema output is a single JSON file in this exact
shape. Match the key names precisely — the import endpoint reads
them by name, and any mismatch is silently dropped (item types get
created with zero fields, items don't get attached to a type,
options disappear).

  {
    "version": "1",
    "format": "coworkcanvas",
    "data": {
      "itemTypes": [
        {
          "slug": "audit",
          "name": "Audit",
          "namePlural": "Audits",
          "description": "...",
          "icon": "ClipboardCheck",
          "color": "#3a7ca5",
          "displayOrder": 10,
          "FieldDefinition": [
            { "fieldKey": "phase", "label": "Phase",
              "fieldType": "SELECT", "isCore": true,
              "isFilterable": true, "order": 1,
              "options": [
                { "value": "planning", "label": "Planning" }
              ]
            },
            { "fieldKey": "engagement_letter",
              "label": "Engagement Letter",
              "fieldType": "DOCUMENT",
              "order": 2 }
          ]
        }
      ],
      "customLists": [],
      "items": {
        "authority_source": [
          { "title": "GDPR",
            "fields": { "source_type": "regulation" } }
        ]
      }
    }
  }

Six key-name rules that get this skill rejected if violated:

  1. Fields on an item type live under "FieldDefinition" (capital F,
     capital D). Lowercase "fields" is silently dropped.
  2. data.items is an OBJECT keyed by item-type slug, never an array.
     An array makes every item fail because the endpoint treats array
     indices "0", "1", … as slugs and finds no match.
  3. Relationships between items are NOT a field type. RELATION and
     RELATIONS were removed and "relatedItemTypeSlug" is obsolete —
     a schema declaring either fails at import. Model an item-to-item
     link as an "itemrelationship" suggestion instead (see
     /coach-items-link): suggest_change create or delete, never
     update. Design the link map in the interview; the links are
     filed after the schema and items are imported.
  4. The only valid fieldType values are the Prisma enum exactly —
     13 of them: TEXT, TEXTAREA, RICHTEXT, NUMBER, DATE, DATETIME,
     SELECT, MULTISELECT, BOOLEAN, USER, USERS, DOCUMENT, JSON.
     There is no RELATION/RELATIONS/MULTISELECT_RELATION (use
     itemrelationship links), no FILE (use DOCUMENT), no URL
     (use TEXT), no EMAIL (use TEXT), no CHECKBOX (use BOOLEAN).
  5. SELECT and MULTISELECT options are an array of
     { value, label } pairs. Empty arrays are rejected.
  6. DOCUMENT fields are declared in the schema but never carry a
     value in seeded data.items — the platform rejects that with
     "<Label> uploads after item creation". One document per
     (item, fieldKey); the file is uploaded after import via
     upload_document with an "item_field" target, and each upload
     replaces the current document.

Item type top-level fields: slug (lowercase, derived from name),
name, namePlural, description, icon (a Lucide icon name like
ClipboardCheck or Building2), color (hex, like #3a7ca5),
displayOrder.

Field definition top-level fields: fieldKey (camelCase identifier),
label, fieldType, required, description, order, isCore, isFilterable,
isSearchable, options (for SELECT and MULTISELECT), group. Three
flags change discovery behavior: isCore (shown on list cards),
isFilterable (available as filter dropdown, typically SELECT,
MULTISELECT, DATE, BOOLEAN), isSearchable (included in full-text
search, typically TEXT, TEXTAREA, RICHTEXT).

In --add-field mode, each appended field must take this exact shape:

  { "fieldKey": "<camelCase>", "label": "...",
    "fieldType": "<one of the enum values>",
    "required": <bool>, "order": <int>,
    "isCore": <bool>, "isFilterable": <bool>,
    "isSearchable": <bool>,
    "options": [ { "value": "...", "label": "..." } ] }

Drop `options` for non-SELECT fields. Fields go into the item
type's FieldDefinition array; relatedItemTypeSlug (and the older
relationTarget) are obsolete keys from the removed relation types —
never emit either.

In --add-type mode: slug must be lowercase, alphanumeric plus
underscore. Icon must be a valid Lucide name. Color must be a hex
code. displayOrder defaults to the next available slot. The emitted
JSON must carry the full data envelope — never a bare item-type
object:

  {
    "version": "1",
    "format": "coworkcanvas",
    "data": {
      "itemTypes": [
        {
          "slug": "<lowercase>",
          "name": "...",
          "namePlural": "...",
          "description": "...",
          "icon": "<LucideName>",
          "color": "#hex",
          "displayOrder": <int>,
          "FieldDefinition": [
            { "fieldKey": "title", "label": "Title",
              "fieldType": "TEXT", "required": true, "order": 1,
              "isCore": true, "isSearchable": true }
          ]
        }
      ]
    }
  }

An un-enveloped item-type object is rejected at import with
"missing data field". Before the output reaches the user, running
/coach-schema-validate on it is a hard gate — it is never skipped.

In --options mode, every option has a value (lowercase,
underscore-or-hyphen separated, stable identifier) and a label
(display name). The shared core ships two named custom lists out of
the box: `regulators` (sourced from the regulator SELECT field on
the authority_source item) and `regions` (sourced from the region
SELECT field on the same item). Skills that need additional domain
vocabularies create new named custom lists alongside these.

In --export mode, use one unscoped get_schema for type discovery, then
get_schema(type: "<slug>") once per exported type. Typed responses expose
SELECT/MULTISELECT options when supplied; copy those exact values. Preserve
the protected status definition and its actual options. For an option-bearing
field whose options remain unavailable, write the literal sentinel
"options": "NEEDS_MANUAL_COMPLETION" and list that field for completion.
Export only metadata actually exposed. This is a schema draft, not a complete
restorable backup: typed discovery omits other import/layout metadata and
custom-list definitions. Identify those limits even when no sentinel remains.

Shared invariants, every mode: schema, item types, fields, and
custom lists are admin-page concerns — the output is for the admin
to paste at /en/admin/bulk-import, and schema changes never flow
through suggest_change (suggest_change writes Items only, and
silently no-ops on item types and field definitions). All outputs
are bulk-import format. Validate with /coach-schema-validate before
handoff — for --export, the validator's errors on the
NEEDS_MANUAL_COMPLETION sentinels are the completion checklist.

Never invent the schema unprompted. Walk the user through it
type-by-type. When in doubt, ask.

Before system-dependent design, reuse the user's supplied systems and scope.
Ask only for missing dimensions that affect the requested schema. Keep the
profile in session memory; optional durable storage must be bound to the
verified tenant/user. Do not claim persistence for an ephemeral artifact. Ground all system-driven tailoring in the bundled
systems/<category>.md templates: instantiate {{system}} with the
company's real product names to emit control, risk, and policy
items. Tag controls/risks with a SELECT/MULTISELECT `system` field,
add `itgc_domain` on control when SOX/ERP is in scope, and add an
in_scope_systems shared customList. Skip templates for systems the
company does not run. If a compliance baseline is already imported
(control/risk types populated per /coach-setup --verify), add only
the system-specific delta — never duplicate baseline controls.
These tailored items ship in the same bulk-import JSON and never
flow through suggest_change. Never place any /slash-command text
inside emitted JSON field values or option values.

Follow the shared host contract for tool announcements, concise results,
artifact delivery, pending states and human approval.

```

## Inputs

Mode is chosen by the leading flag; with none, the default design
interview runs.

- default (no flag) — the full design interview; free-text domain
  context may follow
- `--add-field <type-slug>` — which item type to extend. Optional
  `--field <fieldKey>` for single-field non-interactive mode;
  otherwise interactive — adds fields one at a time until the user
  is done
- `--add-type` — interactive, OR `--name <text>` and
  `--namePlural <text>` for non-interactive; `--icon <LucideName>`
  and `--color <hex>` default if not provided
- `--options` — `template <name>` to emit a canned list, or `custom`
  for interactive creation
- `--export` — optional `--out <path>` (default
  `.coworkcanvas/schemas/<subdomain>-<date>.json`) and
  `--include-system` (include system item types, default true)

## Procedure

### Mode: default — the full design interview

#### 1. Frame the domain
Ask the user:
- What does your team do (one sentence)
- What's the unit of work they track (one to three nouns)
- Who uses Canvas (roles, headcount)
- Is this for audit, SOX, regulatory, GRC, or something else
  (offer to short-circuit to a starter pack if so)

If a clear match emerges (audit, SOX, etc.), suggest
`/coach-starter-pack <kind>` instead of designing from scratch.

#### 1.5 Systems & scope discovery
Before designing item types, interview the company about the **systems
it actually runs**. The systems determine which controls apply, which
risks are real, and which policies are needed — so the tailored output
is grounded in the company's real stack, not generic.

**Reuse supplied context.** Use existing conversation values and any verified
tenant/user profile. Resolve only stale or missing facts relevant to this
design. The dimensions below are a reference menu, not a mandatory interview.
Use the detected question UI when available, or a concise plain-text question.

1. **Financial / ERP** — SAP, Oracle EBS/Fusion, NetSuite, Workday,
   Dynamics 365, Sage, QuickBooks, Other. Also ask about consolidation/
   close tooling and material sub-ledgers. (Drives SOX ITGC/ITAC.)
2. **Cloud & infrastructure** — AWS, Azure, GCP, on-prem/colo, Other.
3. **Identity & access** — Okta, Entra ID, Ping, Google Workspace,
   Active Directory; plus PAM (CyberArk, BeyondTrust, …).
4. **Security tooling** — EDR, SIEM / log management, vulnerability
   scanner, DLP, secrets manager.
5. **HR & payroll** — HRIS (Workday HCM, BambooHR, …), payroll provider
   (ADP, …). (Feeds joiner-mover-leaver.)
6. **Dev & change** — source control (GitHub / GitLab), CI/CD, ITSM /
   ticketing (Jira, ServiceNow).
7. **Data & privacy** — primary databases, data warehouse (Snowflake,
   BigQuery, …), and regulated data types handled (PII, PHI,
   PCI-cardholder, CUI).
8. **Business apps & third parties** — CRM (Salesforce, …), e-commerce
   / payment, and key sub-service organizations / critical vendors.
9. **Scope context** — in-scope frameworks (from the 13 baseline
   standards), industry, entities / geographies.

Capture each answer's product names (normalize "Other" free text into a
lowercase slug, e.g. "Oracle Fusion" → `oracle-fusion`). Keep the profile
in session memory; save it only when durable storage is supported.

**Systems profile artifact — `.coworkcanvas/systems-profile.json`.**
When durable storage is available, bind a saved profile to the verified
tenant and user. Otherwise retain session values and say they are not
persisted. Example profile contents:

```jsonc
{
  "capturedAt": "2026-07-01",
  "frameworks": ["sox","soc2","iso-27001"],
  "industry": "fintech",
  "entities": ["US HoldCo","EU OpCo"],
  "systems": {
    "erp": ["netsuite"], "cloud": ["aws"], "identity": ["okta"], "pam": [],
    "security": ["crowdstrike","splunk"], "hris": ["workday"], "payroll": ["adp"],
    "scm": ["github"], "cicd": ["github-actions"], "itsm": ["jira"],
    "db": ["postgres"], "warehouse": ["snowflake"], "crm": ["salesforce"],
    "regulatedData": ["pii","pci"], "thirdParties": ["stripe","aws"]
  }
}
```

Empty categories are `[]` — that is meaningful (the company doesn't run
that system) and drives the applicability rule in the tailoring step.

#### 1.6 Fresh design vs baseline-tailoring delta
Detect whether a compliance baseline is already imported before
designing. Tail-invoke `/coach-setup --verify` (or `/coach-query-data`)
and inspect whether the `control` / `risk` item types exist and are
**populated**.

- **Fresh design** (no baseline — the `control`/`risk` types are absent
  or empty): produce the full schema *plus* system-tailored starter
  controls, risks, and policies from the templates.
- **Baseline-tailoring** (the 13-standard baseline is already imported —
  `control`/`risk` types populated): do NOT redesign the schema and do
  NOT re-emit baseline controls. Add only the **system-specific delta** —
  the template-derived controls/risks/policies for the named systems that
  aren't already present — and add the `system` / `in_scope_systems` /
  `itgc_domain` scoping fields to the existing types. Dedupe by
  title + `system` tag: if a baseline control already covers a system,
  skip it rather than duplicating.

#### 1.7 Tailoring — profile + templates → output
The bundled `systems/<category>.md` template library (see Notes) is the
**source of truth** for tailoring. For every category the profile names,
read its template file and instantiate the `{{system}}` placeholder with
the company's real product name(s). Do not improvise controls the
templates don't cover; the templates keep output grounded and
consistent.

Category → template file mapping:

| Profile categories | Template file |
|---|---|
| `erp` (+ close/sub-ledgers) | `systems/erp.md` |
| `cloud` | `systems/cloud.md` |
| `identity`, `pam` | `systems/identity.md` |
| `scm`, `cicd`, `itsm` | `systems/dev-change.md` |
| `db`, `warehouse`, `regulatedData` | `systems/data-privacy.md` |
| `security` | `systems/security-tooling.md` |
| `hris`, `payroll` | `systems/hr-payroll.md` |
| `crm`, `thirdParties` | `systems/business-apps.md` |

Tailoring rules:

1. **Schema.** Add an `in_scope_systems` shared `customList` (one flat
   `{ category, value, label, sortOrder }` tuple per named system). Add a
   `system` field (`SELECT` for one system, `MULTISELECT` when a control
   spans several) on `control`, and on `risk` where a risk is
   system-specific — options are the named systems (non-empty). When
   SOX or an ERP is in scope, add an `itgc_domain` `SELECT` on `control`
   with options `access` / `change` / `operations` / `interfaces`.
2. **Controls.** For each named system, instantiate its template's
   controls as `control` items (title includes the real product name),
   tagged with `system` and `itgc_domain` where applicable.
3. **Risks.** Instantiate the template's system-specific risks as `risk`
   items, tagged with `system`.
4. **Policies.** Instantiate the implied policies as `policy` items,
   **deduped across systems** (one "Change Management Policy" governs all
   changeable systems). Record which controls each policy governs in the
   change preview and file those links after import as
   `itemrelationship` suggestions (`/coach-items-link`) — policy-to-control
   links are relationships, not schema fields.
5. **Applicability.** Systems the company did NOT name (empty `[]`
   category) → their templates are skipped entirely, keeping the set
   lean and relevant.

Each template also carries a **generic fallback** so an "Other" product
still yields sensible items — instantiate the fallback controls/risks/
policies with the typed product name when no product-specific block
matches.

#### 2. Identify item types
For each unit of work the user mentioned, propose an item type with
sensible defaults:
- slug (lowercase, derived from name)
- name and namePlural
- a Lucide icon (use ClipboardCheck for audit-ish, Shield for risk,
  AlertTriangle for issue, Lock for control, FileText for policy,
  Building2 for company, Headphones for support)
- a brand-aligned hex color (offer pre-set palette: #3a7ca5 primary,
  #1a7a6d teal, #b8860b gold, #a94442 danger, #4a90c4 info)
- displayOrder

Confirm each with the user before adding to the JSON.

#### 3. Add fields per type
For each item type, propose 5-15 fields. Always include:
- title (TEXT, required, isCore, isSearchable)
- description (TEXTAREA, isSearchable)
- a status SELECT with sensible options
- owner (USER, isCore)
- created_at, updated_at (auto-managed by Canvas, do not emit
  in JSON; just note for the user)

Domain-specific fields per the user's interview answers. Use the
`--add-field` intake pattern interactively.

#### 4. Identify custom lists and relationships
- For SELECT and MULTISELECT fields, capture the options array.
  Share options across item types when sensible (e.g., severity
  reused on issue, finding, deficiency). Cross-type shared options
  go in the top-level `customLists` array as flat
  `{ category, value, label, sortOrder }` tuples.
- Capture the relationship map — which item types relate to which
  (issue relates to control; control relates to risk; etc.) — as a
  plain list for the user to confirm. It is not schema: there is no
  relation fieldType and no `relatedItemTypeSlug`. Each pair becomes
  an `itemrelationship` link (kind `related` / `parent` / `child` /
  `sibling`) filed through `/coach-items-link` once the item types
  and items are imported.
- For files an item should carry (engagement letter, signed policy
  PDF, evidence attachment), declare a `DOCUMENT` field. It ships
  empty; the file is uploaded afterwards via `upload_document`.

#### 5. Deliver the JSON
Use the detected artifact delivery surface. With durable writable storage, save to
`.coworkcanvas/schemas/<slugified-domain>-<date>.json` in the
bulk-import shape (see system prompt above). Pretty-print for
diff-friendliness. Also write `.coworkcanvas/systems-profile.json`
(step 1.5) so the captured systems are reusable on re-run and by other
skills. The system-tailored controls, risks, and policies (step 1.7)
are emitted into the same bulk-import JSON — `control` / `risk` items
carry their `system` (and `itgc_domain`) tags, `policy` items are
deduped, and the policy→control link list is carried alongside for
`/coach-items-link` to file after import (links are `itemrelationship`
rows, not fields). In baseline-tailoring mode the file contains only
the delta.

#### 6. Validate (hard gate)
Tail-invoke `/coach-schema-validate --file <path>` on the new file.
This is a hard gate, not advisory — if the report contains any
ERROR-level issues, do not print the "apply it" message in step 7.
Instead, fix the offending fields in the JSON, re-write the file,
and re-run the validator until it passes. Only proceed to step 7
when the validator reports zero errors.

#### 7. Tell the user the next move
Use the verified active tenant origin from session context or matching optional
config, then provide:

```
Schema JSON written to <path>.

Apply it:
  1. Open <canvas_url>/en/admin/bulk-import
  2. Paste the JSON contents into the import box
  3. Click Import

After importing, run /coach-setup --verify to confirm the schema
is in place.
```

### Mode: `--add-field <type-slug>` — extend an item type

1. Load the schema; locate the target item type (the `<type-slug>`
   argument).
2. For each field the user wants to add:
   - fieldKey (camelCase, unique within the item type)
   - label (display name)
   - fieldType (offer the platform enum with one-line descriptions;
     map their plain-language answer to the right type)
   - required (default false)
   - order (next available)
   - Conditional based on fieldType:
     - SELECT, MULTISELECT: options array with value (lowercase)
       and label (display)
     - DOCUMENT: nothing extra in the schema — but tell the user the
       field starts empty and is filled after the item exists via
       `upload_document` (`/coach-document-upload --item`)
     - NUMBER: optional min, max, step
   - If what the user is describing is really a pointer at another
     item ("link this control to its risk"), that is not a field.
     Say so and route them to `/coach-items-link`, which files the
     `itemrelationship` suggestion — do not invent a field for it.
   - Flags:
     - isCore: yes if the user said "show on the card"
     - isFilterable: yes if SELECT, MULTISELECT, DATE, BOOLEAN,
       USER and used for filtering
     - isSearchable: yes if TEXT, TEXTAREA, RICHTEXT and contains
       searchable content
3. Append to the item type's `FieldDefinition` array; bump display
   order on subsequent additions.
4. Tail-invoke `/coach-schema-validate --file <schema-path>` as a
   hard gate. Halt with the report if any errors remain — most
   often a stray non-enum fieldType, and since the relation types
   were removed, most often a `RELATION` / `RELATIONS` field copied
   in from an older schema.

### Mode: `--add-type` — add one item type

1. Load current schema from `.coworkcanvas/schemas/` (most recent file
   matching the workspace, or prompt user to specify). If no schema
   file exists yet, start a new one carrying the full envelope from
   the system prompt (`version`, `format`, `data.itemTypes`) — never
   a bare item-type object.
2. Validate the new slug does not collide with existing types.
3. Ask for or default:
   - name, namePlural (sentence case)
   - slug (lowercase, derived from name)
   - description (one sentence)
   - icon (Lucide name; offer 5 suggestions per the domain)
   - color (hex; offer brand palette)
   - displayOrder (max existing + 1)
4. Add a minimal field set under `FieldDefinition`: title (TEXT,
   required), description (TEXTAREA), status (SELECT with open and
   closed), owner (USER).
5. Append the new item type to the schema JSON's `data.itemTypes`
   array and write the file. The emitted JSON must include the
   top-level data envelope — an un-enveloped item-type object is
   rejected at import with "missing data field".
6. Continue in `--add-field <slug>` mode for the user to add
   domain-specific fields.
7. Run `/coach-schema-validate --file <schema-path>` on the output —
   a hard gate that is never skipped, before anything is handed to
   the user. Halt with the validator report if it surfaces any
   errors — most often the legacy `fields` key, a missing `data`
   envelope, or a non-enum fieldType slipped through — fix the JSON
   and re-run until it reports zero errors, and only then print
   step 8.
8. Use the verified active tenant origin from session context or matching optional
config, then provide:
   ```
   Item type added to <schema path>.

   Apply it:
     1. Open <canvas_url>/en/admin/bulk-import
     2. Paste the schema JSON into the import box
     3. Click Import

   The import is idempotent — existing item types are updated in
   place, so re-importing the full schema is safe.
   ```

### Mode: `--options` — build an option list

Canned templates:

- `severity-h-mh-m-l` — High, Moderately High, Moderate, Low (AssureSwarm IM Policy ratings)
- `severity-mw-sd-cd` — Material Weakness, Significant Deficiency, Control Deficiency (SOX)
- `severity-critical-high-medium-low` — generic severity scale
- `status-open-progress-closed` — Open, In Progress, Closed
- `status-draft-review-approved` — Draft, In Review, Approved, Rejected
- `frequency-d-w-m-q-y` — Daily, Weekly, Monthly, Quarterly, Annual
- `regions` — North America, EMEA, APAC, LATAM (matches the shared `regions` custom list on `authority_source.region`)
- `regulators` — SEC, FCA, FINRA, OCC, FRB, FDIC, ESMA, CFPB (matches the shared `regulators` custom list on `authority_source.regulator`; extend per tenant)
- `priority-p0-p3` — P0, P1, P2, P3
- `audit-type` — internal, sox, soc2, iso27001, regulatory, external (matches `audit.audit_type` on the shared core)
- `audit-phase` — Planning, Fieldwork, Reporting, Closed
- `step-status` — not_started, in_progress, complete, blocked (matches platform Step status)

Subcommand `template <name>`:
1. Validate the template name; print the option array.
2. Ask if the user wants it inlined in a specific field or saved as
   a reusable custom list. If reusable, name the list category and
   append flat entries to the workspace schema's top-level
   `customLists` array (one entry per option, shape
   `{ category, value, label, sortOrder }`) so the admin can import
   them at `/en/admin/bulk-import` alongside the item types.

Subcommand `custom`:
1. Ask: list name, intent (one sentence).
2. Add options one at a time (value, label). Suggest deriving value
   from label (lowercase, hyphens).
3. Optional: an "other" option with free-text input (note this is
   not a Canvas field type quirk; record as a SELECT plus a paired
   TEXT field downstream).

### Mode: `--export` — pull the live tenant schema

1. Resolve the verified active tenant from the current connection or optional config.
2. Use one unscoped `get_schema` for discovery, then one typed
   `get_schema(type: "<slug>")` per exported type; follow the session cache.
3. Transform the response into the bulk-import shape:
   ```
   {
     "name": "<subdomain> schema export",
     "description": "Exported from <canvas_url> at <timestamp>",
     "version": "1",
     "format": "coworkcanvas",
     "data": {
       "itemTypes": [
         {
           "slug": "...",
           "name": "...",
           "namePlural": "...",
           "description": "...",
           "icon": "...",
           "color": "...",
           "displayOrder": 0,
           "FieldDefinition": [
             { "fieldKey": "...", "label": "...", "fieldType": "TEXT", "order": 0, ... },
             { "fieldKey": "...", "label": "...", "fieldType": "SELECT",
               "options": "NEEDS_MANUAL_COMPLETION", ... }
           ]
         }
       ],
       "customLists": [
         { "category": "...", "value": "...", "label": "...", "sortOrder": 0 }
       ]
     }
   }
   ```
   The shape above illustrates available and missing metadata; omit properties
   not exposed rather than inventing values. Copy the actual itemType.defaultStatus
   separately from the status vocabulary. The sentinel example applies only
   when options are unavailable. Do not fabricate customLists from field options.
   Field arrays use `FieldDefinition` (not `fields`). Every
   `fieldType` must be one of the 13 platform values (TEXT,
   TEXTAREA, RICHTEXT, NUMBER, DATE, DATETIME, SELECT, MULTISELECT,
   BOOLEAN, USER, USERS, DOCUMENT, JSON) — there is no relation
   type, so never emit `relatedItemTypeSlug` or `relationTarget`.
   `customLists` is a flat array of tuples (one entry per option).
4. Copy available typed SELECT/MULTISELECT option arrays and the protected
   status definition exactly. When an option-bearing field lacks usable
   options, write `"options": "NEEDS_MANUAL_COMPLETION"`; do not substitute
   an empty array or guessed values. List unavailable metadata, including
   custom-list definitions and import/layout properties not exposed by
   get_schema. Describe the output as a schema draft, not a restorable backup.
5. Deliver the JSON through the available artifact surface; save locally only
   when supported. Use 2-space indentation and sorted keys. Without a runner,
   label the draft unvalidated and provide the exact validation handoff.
6. Print the path, file size, and a count of item types and total
   fields — plus the completion list: every field marked
   `NEEDS_MANUAL_COMPLETION`, grouped by item type, with the warning
   that the schema draft needs each sentinel replaced and all omitted
   metadata checked against the admin export (read option arrays from
   `/en/admin/item-types` and `/en/admin/custom-lists`, then re-run
   `/coach-schema-validate` until it reports zero errors).

## Notes

- The schema design is a STARTING point. Customers will iterate over
  weeks. The JSON file is checked into version control as the
  living document.
- A mature production schema commonly runs around a dozen item types
  with shared custom lists — useful as a sizing benchmark when
  reviewing what you've designed.
- Schema, item types, fields, custom lists, dashboards, and workflow
  templates are admin-page concerns. They flow through the Bulk
  Import admin page at `/en/admin/bulk-import`, not through
  suggest_change. The suggestions queue is for Items only.
- Single-type edits can also be made directly at
  `/en/admin/item-types`, and one-at-a-time list edits at
  `/en/admin/custom-lists`, without this skill — useful for quick
  tweaks like renaming a field label.
- Reuse existing replacement intent and tenant/user-bound profile values on
  re-runs. Resolve ambiguity before overwriting a file; do not ask again
  when the request already authorizes that change.
- **Systems template library** — `skills/coach-schema-design/systems/`
  holds one markdown template per system category (`erp.md`, `cloud.md`,
  `identity.md`, `dev-change.md`, `data-privacy.md`,
  `security-tooling.md`, `hr-payroll.md`, `business-apps.md`). Each maps
  its category (and common products) to the controls, risks, and
  policies it implies, parameterized by `{{system}}`, with a generic
  fallback for "Other" products. These files are the grounding source of
  truth for step 1.7 tailoring. Adding a new category = adding a
  template file (extensible). They are bundled with the skill as plain
  data (not SKILL.md, not agents), read at tailoring time.
- For SELECT options shared across item types (severity, priority),
  use `--options` mode — it emits a reusable custom list entry under
  top-level `customLists` that multiple fields can reference. A
  custom list named `severity` referenced by issue, risk, and audit
  means ratings stay consistent across the platform.
- Value strings should be stable. Once data exists with a given
  value, changing the value string breaks historical filters.
  Labels can change freely.
- A common mistake is making every TEXT field isSearchable. It
  inflates the tsvector and slows searches. Surface a confirmation
  for any non-title TEXT field the user marks searchable.
- Files do have a real type now: `DOCUMENT`. Declare it in the
  schema, then upload the file after the item exists —
  `upload_document` with target
  `{ type: "item_field", itemId, fieldKey }`. One document per
  (item, fieldKey); re-uploading replaces it. A DOCUMENT value can
  never be set inline in item data — the platform rejects it with
  "<Label> uploads after item creation".
- The platform enum still does not include URL, EMAIL, or CHECKBOX.
  Until those are added: store URLs and emails as TEXT, and use
  BOOLEAN in place of CHECKBOX.
- `RELATION` and `RELATIONS` are gone from the enum, along with
  `relatedItemTypeSlug`. Relationships between items are
  `itemrelationship` links filed through `/coach-items-link` —
  `create` and `delete` only; there is no update. If an older schema
  in the workspace still declares a relation field, the validator
  errors on it; delete the definition and re-create the links.
- Adding an item type is reversible only by editing the JSON before
  the admin applies it. Once imported, the type lives in Canvas
  until an admin retires it from the Item Types admin page.
- Compose with `/coach-starter-pack` to apply a pre-baked type set
  in one go — and when a clear domain match emerges in the
  interview, short-circuit to it rather than designing from scratch.
- Framework citations (SOC 2 TSC clauses, ISO Annex A controls,
  SOX 404 references) are NOT custom-list values anymore. They
  route through links to `authority_source` items via the
  `cites_authority_sources` MULTISELECT on policy, control,
  process, and audit. Granular clause codes (CC6.1, A.5.18) live
  as free text in the policy's `obligation` field. The old
  `compliance_criteria` custom list has been retired — earlier
  instances may still have it if they predate the shared-core
  refactor.
- Export is read-only and does not write to the source tenant. For
  migration between tenants: export from source, replace every
  `NEEDS_MANUAL_COMPLETION` sentinel with the real option arrays,
  optionally edit, then apply at the target by pasting the JSON into
  `<target canvas_url>/en/admin/bulk-import`. Running
  `/coach-schema-validate` errors on any remaining sentinel
  by design — that error list is the completion checklist, not a
  bug.
- The export is schema only. It does not carry item-to-item links
  (`itemrelationship` rows) or the files behind `DOCUMENT` fields —
  a DOCUMENT field round-trips as a definition, and the destination
  tenant starts with it empty. Re-file links with
  `/coach-items-link` and re-upload documents with `upload_document`
  after migrating.
- **Out of scope** for this skill: auto-applying schema via
  `suggest_change` (admin page only); exhaustive per-product control
  libraries (templates cover common systems + a generic fallback);
  risk scoring / control-effectiveness judgments (human decisions).
