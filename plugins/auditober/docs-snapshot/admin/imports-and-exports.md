---
title: Imports and Exports
description: "Move configuration and data through Data Management: choosing what to export, the JSON import file, and the CSV user import."
sidebar:
  order: 5
---

Tabs
Choose
Export
Import
Users

Scroll

**Data Management**, from the Administration page, is a single surface for three
jobs: taking a copy of what you have configured, loading a prepared dataset, and
bringing a list of people in from a spreadsheet.

## Three tabs, three jobs

**Export Data** writes your configuration and records out as a JSON file.
**Import Data** reads that same shape back in. **Import Users** is separate and
takes a CSV, because creating people is a different operation from creating
records.

Take an export before any risky configuration change. It is the fastest way
back, and diffing a before-and-after pair is the clearest way to see exactly
what a change moved.

## Choose what leaves

Each data type is selected independently, one tile per section of the transfer
file, so an export can be as narrow as a single kind of record. **Select All**
and **Clear All**, at the top right of the card, set every tile in one move.

Pick the narrowest set that answers the question. A configuration backup is
usually item types, custom lists, dashboards, and templates without the items;
a migration to another tenant your organization runs usually wants everything.

## Export to JSON

**Export to JSON** downloads the selected sections as one file. Select the
destination transfer version to match what the receiving tenant supports.
The file can contain personal data: owners, approvers, and form respondents
are referenced by email, and a Users export includes names, administrator
flags, and page access. The envelope also identifies the exporting admin.

These are identity and assignment records. Historical approval decisions
and activity history remain in the source tenant. Review the selected
sections and recipient before sharing an export.

## Import a prepared dataset

The **Import Data** tab takes a `.json` file, dropped onto the page or chosen
from a file picker. Sections are processed in a fixed order, and configuration
rows update in place rather than duplicating, so fixing and re-running a
corrected file is the expected workflow rather than a last resort.

Results come back per section with created and updated counts and per-row
failure details, so you correct the specific rows that failed instead of
re-checking the ones that already landed.

## Import a list of people

The **Import Users** tab takes a `.csv`. The only required column is `email`;
`name` and `isAdmin` are optional, and boolean values accept `true`/`false`,
`yes`/`no`, or `1`/`0`. **Download Template** gives you a correctly-shaped
file, and the page previews the first rows before anything is written.

Each row comes back as **created**, **restored**, **skipped**, or **error**.
Restored means a previously deactivated account came back, which is why a
re-run of the same list is safe. Imported people arrive with no page access
beyond the defaults, so pair the import with a pass through
[User Permissions](https://docs.assureswarm.com/admin/users-and-access/).

## The import file

A transfer file declares its format and version and places every selected
section inside `data`. The sections are processed in dependency order:

1. `users`: accounts, names, administrator flags, and page access.
2. `customLists`: the value lists fields and filters reference.
3. `itemTypes`: record types and their field definitions.
4. `dashboards`: dashboard definitions.
5. `items`: an object keyed by item type slug, each value a list of item rows.
6. `workflows`: workflow templates and their step definitions.
7. `itemTemplateLinks`: links from items to workflow templates.
8. `workflowTemplateStepLinks`: links from template nodes to items.
9. `workflowsAttached`: running workflows, steps, and linked items.
10. `itemRelationships`: links between items.

You can omit sections whose dependencies already exist in the destination.
This small example adds an item to an existing `issue` type:

```json
{
  "format": "coworkcanvas",
  "version": "2.7",
  "data": {
    "items": {
      "issue": [
        { "title": "Example issue", "status": "OPEN", "fields": {} }
      ]
    }
  }
}
```

Use the receiving tenant's item type slug, stored status value, and required
fields. `coworkcanvas` is the transfer dialect marker, even on AssureSwarm.
Do not move sections out of `data` or change the version to bypass validation.

## Destination versions and identity data

The export destination-version selector governs which capabilities can leave
the source tenant. Confirm the receiver's supported version before selecting it:

| Minimum version | Capability                                                                    |
| --------------- | ----------------------------------------------------------------------------- |
| 2.3             | Source identity references for items and dependent links.                     |
| 2.4             | Users and email-referenced item owners, step approvers, and form assignments. |
| 2.5             | Automatic-workflow configuration on templates.                                |
| 2.6             | Item-to-template links.                                                       |
| 2.7             | Template-step-to-item links.                                                  |

An older destination can reject newer envelopes. Selecting an older version
does not make unsupported configuration portable: the exporter refuses
selections it cannot preserve safely, including automatic workflows on a
destination below 2.5. Link sections also require their template dependencies.
Email references must resolve to active destination users; the Users section
can supply those accounts first. Missing identities fail the affected rows.

Exported owner and approver emails preserve assignments, not historical
sign-off. Names, emails, administrator flags, page grants, respondent
assignments, and the exporter email are personal or access information; inspect
them before sending the file outside your organization. An export is not a
complete tenant backup.

## Running an import safely

1. **Start with a small test file**, a handful of rows across the sections you are
   changing, not the full dataset.
2. **Use the slugs and field keys already configured.** They are the join keys, and
   a typo creates a second thing rather than updating the first.
3. **Provide required fields** on every row. A missing required field fails that
   row.
4. **Use stored values, not display labels**, for `SELECT` and `MULTISELECT`
   fields. See [Custom lists](https://docs.assureswarm.com/admin/custom-lists/).
5. **Read the results**, fix what failed, and re-run the corrected file.

:::tip\[Re-running is the normal workflow]
Configuration rows update in place instead of duplicating, so re-running a
corrected file, including the rows that already succeeded, is safe. Import
requests also carry an idempotency key, so a retried submission of the same import
does not apply twice.
:::

Requests are size limited. Split a very large dataset into several files rather
than sending one enormous request: by section, by item type, or by batch of rows,
whichever divides your data most naturally.

## Reading the results

| Reported                            | Where                                                                                                                          |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Created and updated counts          | Every section.                                                                                                                 |
| Per-row errors with failure details | Every section.                                                                                                                 |
| Dangling relations                  | Additionally for `itemTypes`: a `RELATION` or `RELATIONS` field pointing at a type that is in neither the file nor the tenant. |
| Created and replaced counts         | For [dashboards](https://docs.assureswarm.com/concepts/dashboards/), instead of created and updated.                                                       |

## When not to use this

Bulk export is built for configuration and modest data volumes, not large-scale
analysis. To pull a lot of item data out for reporting, use
[query\_data](https://docs.assureswarm.com/mcp/query_data/)'s large-result export, which writes CSV or JSONL
from a GraphQL query. That also lets you shape exactly which fields and which
records come out, rather than exporting an item type wholesale.

And when an agent moves data

## For agents

This page is an administrator's surface, and agents do not use it. An agent's
read path for the same data is [query\_data](https://docs.assureswarm.com/mcp/query_data/), with its
`export` mode for results too large to return inline, and
[get\_schema](https://docs.assureswarm.com/mcp/get_schema/) for the shape behind them. Files that belong to
a step move through [upload\_document](https://docs.assureswarm.com/mcp/upload_document/) and
[download\_document](https://docs.assureswarm.com/mcp/download_document/) instead. Bulk configuration
changes stay with people.
