# Form fields reference

Canonical shape for a AssureSwarm step form. Source of truth for the field
definitions is `canvas/apps/core/src/types/form.ts` — keep this in sync.

## The form envelope (`FormResultMetadata`)

A step form is a single JSON object:

    {
      "resultType": "form",
      "fields": [ <FormFieldDefinition>, … ],   // at least one
      "values": {},                              // always start empty
      "submittedAt": null                        // platform sets on submit
    }

- On a **live step** (coach-form-create): send it as `data.fields.formData`.
- On a **template node** (coach-workflow-build --as-template): set it as the
  node's `data.formData`. At instantiation the platform copies the node's
  `data.formData` straight onto the created step, so the form renders at
  `/form/<stepId>`.
- On a **from-scratch workflow node** (coach-workflow-build): set it as the
  node's `data.formData` inside `diagramNodes[]` — copied onto the created
  step the same way when the workflow is created.

Always include `resultType:"form"`, an empty `values:{}`, and
`submittedAt:null`. A form missing `resultType:"form"` or with an empty
`fields` array will not render.

## FormFieldDefinition

    {
      "key": "<kebab-or-snake_case, lowercase>",   // stable id; required
      "label": "<human label>",                     // required
      "type": "text|textarea|number|date|select|checkbox|radio|email|url|file",
      "required": true,                             // optional
      "placeholder": "…",                          // optional
      "helperText": "…",                           // optional
      "defaultValue": <any>,                       // optional
      "options": [{ "label": "Yes", "value": "yes" }],  // select/radio only
      "validation": {                               // optional
        "minLength": 5, "maxLength": 200,
        "pattern": "^[A-Z]", "patternMessage": "…",
        "min": 0, "max": 100,
        "maxFiles": 3, "accept": ".pdf,.docx"       // file only
      }
    }

Rules: keys are unique within a form, lowercase kebab/snake_case. `select`
and `radio` require `options`. `checkbox` is a single yes/no (no options).
`file` accepts `validation.accept` (extension allowlist) and
`validation.maxFiles`.

## Decision-node forms (special case)

A decision node carries `data.kind:"decision"`, `data.decisionField:"<key>"`,
and a `data.formData` whose `fields` contain ONE `select` whose `key` equals
`decisionField`. Keep only this SELECT as the runtime branch selector. Put
rationale in the step result and approver identity in the native approval
record; do not add companion rationale or owner fields. Each branch edge out
of the decision carries `whenValue` (one of that select's option values).
Do not add branching merely to justify a form. If the user requires no forms,
use a workflow without decision branches. See
[workflow-design.md](../coach-workflow-build/references/workflow-design.md).
