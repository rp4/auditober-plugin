---
name: coach-form-create
description: "Use when the user asks to create, add, build, or design a workflow-step form for missing inputs from someone who is not executing the workflow or step. Executor work belongs in step results. Validates field definitions and proposes the schema through suggest_change; filling an existing form is coach-form-fill."
uxContract: 1
hostContract: 1
---

# Coach Form Create

Author a form that collects missing information from someone who is not executing the workflow or step. The schema lands on the step's `formData` field and renders at `/form/<stepId>`. Executor work belongs in the step result. For populating an existing form with values, use [`/coach-form-fill`](../coach-form-fill/SKILL.md).

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first; ask only necessary unresolved inputs through the
actual question tool or plain text. Check dependencies before promising files.

Parse all supplied field definitions first. Batch unresolved respondent, field-shape and replacement-intent questions. Do not run an add-another-field loop when the requested form is already supplied.

You are the form-create skill. The user wants to add a form to a
workflow step so a non-executing respondent can provide missing inputs via
/form/<stepId>. Your job is to design the form schema (fields + types +
options + required flags) and emit ONE suggest_change call against the
step target that sets the form field.

This is NOT for filling a form (that's coach-form-fill). This is for
defining the form's schema in the first place.

Before designing fields, identify the respondent or role, the missing
information, and why existing evidence does not supply it. If the
executor is recording their own analysis, tests, conclusions or
approval, use the step result and native review records instead of
creating a form. Do not invent a respondent to justify a questionnaire.
Use known session context; ask only when a material detail is missing.
Creating or approving a form does not authorize sending it. Prepare the
request, then use existing session authority or obtain authorization
before sending messages or invitations to the respondent.
The workflow-build skill documents the minimal SELECT needed by a
genuine runtime decision branch. That technical field does not justify
extra rationale or owner fields; these belong in the result and native
approval record. See ../coach-workflow-build/references/workflow-design.md.

The correct shape is exactly:

  suggest_change({
    action: "update",
    itemType: "step",
    targetId: "<stepId>",
    data: {
      fields: {
        formData: {
          resultType: "form",
          fields: [
            {
              key: "<fieldKey>",
              label: "<human-readable label>",
              type: "<text|textarea|number|date|select|checkbox|radio|email|url|file>",
              required: true,
              placeholder: "<optional placeholder>",
              helperText: "<optional helper text>",
              options: [{ label: "Yes", value: "yes" }, ...],
              validation: { minLength: 5, maxLength: 200, pattern: "^[A-Z]", min: 0, max: 100, maxFiles: 3, accept: ".pdf,.docx" }
            }
          ],
          values: {},
          submittedAt: null
        }
      }
    },
    reason: "<one short sentence on what this form captures>"
  })

For a new form, values starts empty and submittedAt starts null. The
platform manages submission state. For an existing form, follow the
preservation rules below; do not reset its values or submission metadata.
Use coach-form-fill to propose new responses.

Field types supported by the platform: text, textarea, number, date,
select, checkbox, radio, email, url, file. The select and radio types
require options; checkbox does not (a checkbox is a single yes/no). The
file type accepts validation.accept for extension allowlist and
validation.maxFiles for the count cap.

Procedure:

  1. Resolve the target step. If --step-id was passed, use it. If
     absent, check get_current_context's currentView.stepId. If still
     ambiguous, ask for the missing input to pick from the user's assignedSteps.

  2. Read get_step_context's step.formData.fields. A non-empty array
     means a form already exists. Require explicit replacement intent
     from the user's request or --replace before changing its schema.
     If intent is missing, If unresolved, ask: "Replace existing schema /
     Switch to coach-form-fill / Cancel". Apply the form-state and
     decision-selector preservation rules below before building a change.

  3. Confirm the non-executing respondent and missing-input purpose
     from the session. Do not make a self-addressed result form.
     Gather only fields necessary for that request. Two modes:
     a) --fields <json> passed: validate the JSON against the field
        shape and proceed.
      b) Missing inputs: batch unresolved field types, keys, labels and options.
         Reuse every complete definition already supplied.

  3.5. Validation. Reject duplicate field keys. Reject non-kebab-case
       keys (the platform expects lowercase + underscores or
       lowercase + hyphens). Reject select/radio types without
       options.

  4. Build the form JSON per the canonical shape above. For a new
     form, set resultType: "form", values: {}, submittedAt: null.
     For an existing form, preserve its retained values and submission
     metadata as described below. --replace never permits removing or
     changing a runtime decision selector.

  5. Call suggest_change. On validation error (the platform also
     validates the form shape), show the error verbatim and
     ask for the missing input to resolve.

  6. Hand off with one-line summary, the action link
     [Review and approve](<previewUrl>).

UX contract (see ../../references/host-capabilities.md).

Follow ../../references/host-capabilities.md for intake and output.
Return the result and its real action/artifact link.
```

## Inputs

- `--step-id <id>` — the step to add the form to. If absent, infer from
  current view.
- `--fields <json>` — optional, a pre-built array of field definitions.
  If present, skip interactive gathering and just validate.
- `--replace` — explicit intent to replace an existing schema. Preserve
  runtime decision fields and their values. It does not authorize
  discarding responses or resetting submission metadata.

## Procedure

1. Resolve the step (id, current view, or pick).
2. Call `get_step_context` and inspect `step.formData.fields` using the
   state table below. An existing form requires explicit replacement
   intent; otherwise If unresolved, ask: "Replace existing schema / Switch
   to coach-form-fill / Cancel". Check its runtime decision selector.
3. Identify the non-executing respondent and missing inputs; use step
   results instead for executor work. Gather field definitions.
   If `--fields` was passed, validate;
   otherwise batch unresolved type, key, label, required, options and validation
   inputs. Reuse complete definitions already supplied.
4. Validate: duplicate keys, non-kebab-case keys, select/radio
   without options, file type with invalid `accept` pattern.
5. Build the form JSON. New forms start with `resultType: "form"`,
   `values: {}`, `submittedAt: null`. Existing forms retain the state
   described below.
6. Call:

       suggest_change({
         action: "update",
         itemType: "step",
         targetId: "<stepId>",
         data: { fields: { formData: { ... } } },
         reason: "<short why>"
       })

7. On validation error, show the actionable error and ask only if input is needed.
8. Hand off with summary + action link.

## Existing form and decision state

| Observed state | Action |
|---|---|
| `step.formData` missing or null | No stored form; create one only for the justified missing inputs. |
| `step.formData.fields` is an empty array | No fields; check for retained values and submission metadata before changing the envelope. |
| `step.formData.fields` is a non-empty array | Existing form; require explicit replacement intent and preserve retained responses. |
| Non-null form data with missing fields or a malformed fields value | Stop and report the unsupported state; do not treat it as an empty form. |

Before replacing an existing schema, use `step.workflowId` and
`step.diagramNodeId` to inspect its stored workflow node and outgoing
edges. Read the workflow's graph separately from its paged step roster,
following [query patterns](../../references/query-patterns.md). If the
node is a decision, preserve the SELECT named by `decisionField`, its
key, options, and existing entry in `step.formData.values` unchanged.
Its option values must still match the outgoing branch values. If this
cannot be verified, stop the replacement. Changes to branch logic need
a separate workflow change; `--replace` does not authorize them.

Copy existing values for retained fields and preserve `submittedAt` and
`submittedBy`. Do not silently discard responses when removing fields
or changing their types: resolve that loss explicitly before proposing
the schema. Keep the technical selector even when replacing all other
fields. Leave executor analysis in results and sign-off in native approvals.

## Notes

- Field keys are stable identifiers. Once set, downstream
  coach-form-fill calls reference these keys. Choose them carefully —
  changing a key later means resubmitting forms. Use kebab-case or
  snake_case (the platform accepts either) and lowercase only.
- Required vs. validation. `required: true` is the simplest constraint.
  More granular constraints go in the `validation` object: `minLength`
  / `maxLength` for text, `min` / `max` for numbers, `pattern` for
  regex (anchored — use ^...$), `maxFiles` + `accept` for file fields
  (e.g., `{ maxFiles: 3, accept: ".pdf,.docx" }`).
- File fields. Type "file" accepts uploads via the form UI. The
  resulting values entry is an array of document ids (the same ids
  returned by upload_document). When coach-form-fill populates the
  form, it sets `values[<fileKey>]` to `[documentId]`.
- Schema-change semantics. Updating `step.formData` via this skill creates
  a SCHEMA-CHANGE suggestion. The preview lands in the schema-diff UI
  on the step viewer (not on /form/<stepId>) — this is the right place
  for schema changes. After approval, the form becomes available at
  /form/<stepId>.
- Distinction from coach-form-fill. coach-form-fill uses `action:
  "submit_form"` with `data.fields.values` populated. This skill uses
  `action: "update"` with `data.fields.formData` (the schema). DO NOT
  confuse them — coach-form-fill lands the preview on the form page;
  coach-form-create lands it in the schema-diff UI. Each is correct for
  its purpose.
- Forms on archived steps. Once a step is archived, its form schema
  is locked. The suggest_change will fail with a permission error —
  surface that verbatim.
- Field shape reference. The field types, options, validation, and the full
  form envelope are documented once in [`form-fields.md`](./form-fields.md).
  Keep field authoring consistent with it.
