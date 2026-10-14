# Auditober plugin

Version 0.27.1. This package contains 31 skills and 4 support agents.

Use these skills to work in your AssureSwarm tenant. Start with `/coach-setup` to verify the connection and available capabilities. The assistant uses the live tenant schema and your current permissions.

Work in your Auditober sandbox at core.assureswarm.com: schema discovery, items, links, workflows, forms, documents, dashboard links and Auditober event help. Changes arrive as suggestions you approve in the app.

## Install and connect

For Claude, upload the native plugin ZIP. The portable distribution also includes a Claude-uploadable root, a Codex payload and `SETUP.md`; follow that guide for your client. Configure your own AssureSwarm MCP endpoint and authenticate in your host. No tenant connection is embedded in this public package.

Authorize the complete MCP tool scope set during initial setup:

```text
openid profile email
read:context read:items read:data read:workflows read:dashboards read:documents
read:suggestions write:suggestions write:documents
```

These scopes cover reads, the review queue, proposed changes and document uploads. Suggestions need human approval in the app; uploads attach files directly when you authorize them. Setup does not request `approve:suggestions`. Current MCP tools also do not need `write:forms`, `write:items`, `write:workflows` or `write:dashboards`.

For an existing portable Codex installation, run `node "<installed-plugin-root>/scripts/codex-mcp.mjs" --scopes default` with the path printed by setup, complete consent and restart the task. Use `--scopes read-only` for read-only access. Updates preserve an earlier explicit scope choice. The helper keeps separate authorization profiles for each tenant and scope set.

A successful login or schema/context read does not prove that all tool scopes were granted. An older read-only OAuth client registration can cap a new grant; use the helper or your host's connection settings to update the registration and reauthorize. An administrator may need to change the registration policy. Do not edit tokens or delete credential files manually.

[Connection guide](https://docs.assureswarm.com/mcp/connect/)

## Working rules

Describe the result you need and provide the relevant item or workflow link when available. Existing workflows resume from their stored steps. New items and workflow changes use suggestions; review them through native approvals. Uploads attach documents directly when you authorize them.

Available tools differ by host. Missing file execution, extraction or independent review leaves a clear handoff with the source and pending action. A prepared draft is not a completed workflow or an approved result.

## Included capabilities

- `/auditober-info`
- `/coach-ask`
- `/coach-autopilot`
- `/coach-bulk-user-change`
- `/coach-dashboard-build`
- `/coach-dashboard-link`
- `/coach-dashboard-view`
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
