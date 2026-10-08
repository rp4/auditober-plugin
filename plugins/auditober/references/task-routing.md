# Route the requested action

Choose the action the user asked for. Reuse supplied IDs, context and authorization.
Ask only when an unresolved distinction changes the work.

| Request | Skill | Boundary |
| --- | --- | --- |
| Open a new issue, risk, control or other record | coach-item-create | "Open a new" creates a proposal; it is not a dashboard request. |
| Show overdue issues or open an existing view | coach-dashboard-link | Answer the data question and use supported URL filters. An overdue-only answer does not imply an overdue-only URL filter. |
| Resume or execute an existing workflow | coach-workflow-execute | Resolve the existing run and eligible stored step through workflow-resolution.md. Do not attach another run. |
| Attach a template for a genuinely new cycle | coach-workflow-attach | First resolve existing runs and the requested cycle; use live template identity. |
| Export this workflow | coach-workflow-export | Export the complete selected workflow's steps, results, forms and evidence. |
| Export this item's evidence or a package of items | coach-export-package | Preserve requested item boundaries and redaction requirements. |
| Reassign this one issue or record | coach-item-update | Resolve the live ownership field and only the selected record. |
| Offboard an owner or reassign across their records | coach-bulk-user-change | Establish the cross-record scope and replacement responsibilities. |
| Add, edit or remove a workflow step; author a workflow/template | coach-workflow-build | Use the current step/workflow contract; preserve stored data and graph dependencies. |
| Change step reviewers or due dates | coach-workflow-assign | Native step approvers differ from item ownership. |
| Explain how to do something | coach-ask | A request for instructions alone does not authorize a new record or workflow. |

A --review request reviews the supplied artifact or stored work. It does not attach
workflows, execute later modules, add records or advance a course. A genuinely new
requested action can proceed under its own authorization.

Check package-manifest.json when present. Route only to installed skills. Audit
uses live schema discovery and supported item/workflow operations; schema authoring,
starter-pack preparation and artifact installation are not capabilities of that build.
If the user needs an excluded capability, provide the relevant supported admin/docs
path and identify the missing capability. Never invent a replacement API.

These are instruction-level routing cases. Fixture coverage does not establish that
a host model selected the expected skill; record actual host traces separately.
