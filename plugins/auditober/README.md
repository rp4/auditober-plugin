# Auditober plugin

Version 0.26.2. This package contains 29 skills and 4 support agents.

Use these skills to work in your AssureSwarm tenant. Start with `/coach-setup` to verify the connection and available capabilities. The assistant uses the live tenant schema and your current permissions.

Work in your Auditober sandbox at core.assureswarm.com: schema discovery, items, links, workflows, forms, documents, dashboard links and Auditober event help. Changes arrive as suggestions you approve in the app.

## Install and connect

For Claude, upload the native plugin ZIP. The portable distribution also includes a Claude-uploadable root, a Codex payload and `SETUP.md`; follow that guide for your client. Configure your own AssureSwarm MCP endpoint and authenticate in your host. No tenant connection is embedded in this public package.

[Connection guide](https://docs.assureswarm.com/mcp/connect/)

## Working rules

Describe the result you need and provide the relevant item or workflow link when available. Existing workflows resume from their stored steps. New items and workflow changes use suggestions; review them through native approvals. Uploads attach documents directly when you authorize them.

Available tools differ by host. Missing file execution, extraction or independent review leaves a clear handoff with the source and pending action. A prepared draft is not a completed workflow or an approved result.

## Included capabilities

- `/auditober-info`
- `/coach-ask`
- `/coach-autopilot`
- `/coach-bulk-user-change`
- `/coach-dashboard-link`
- `/coach-document-upload`
- `/coach-export-package`
- `/coach-form-create`
- `/coach-form-fill`
- `/coach-item-create`
- `/coach-item-update`
- `/coach-items-link`
- `/coach-notify`
- `/coach-query-data`
- `/coach-redact`
- `/coach-render-package`
- `/coach-schema-design`
- `/coach-schema-validate`
- `/coach-security-report`
- `/coach-setup`
- `/coach-starter-pack`
- `/coach-ticket`
- `/coach-tour`
- `/coach-workflow-assign`
- `/coach-workflow-attach`
- `/coach-workflow-build`
- `/coach-workflow-execute`
- `/coach-workflow-export`
- `/coach-workflow-scan`

## Help

[AssureSwarm documentation](https://docs.assureswarm.com/) · [Plugin catalog](https://assureswarm.com/plugins/)

Contact [AssureSwarm support](mailto:support@assureswarm.com). This package is licensed under MIT; see `LICENSE`.
