---
name: coach-setup
description: "Use when the user asks to connect or configure the plugin for a tenant, refresh its connection details, or verify that the connected tenant supports the requested work."
uxContract: 1
hostContract: 1
---

# Coach Setup

Establish a verified tenant connection and report the capabilities available.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Read ../../references/schema-discovery.md for typed schema reads and cache
invalidation. Local config is optional; session state works without files.

Use supplied connection details and existing authorization first. Inspect
package-manifest.json (schemaVersion 1) for this distribution's skills,
agents and resources before offering commands. If absent or inaccessible,
use the actual loaded inventory; mark uncertain availability rather than
assuming every source skill ships. Audit packages omit schema-design,
schema-validate, starter-pack and artifact-install. Other packages also omit
artifact-install. Offer verified admin/library links for excluded features.

Detect actual host tools before probing. Find get_schema and
get_current_context exposed by the same MCP server. Use exact discovered
names, including any namespace. The prefix is the actual tool name with its
exact final tool suffix removed; never guess a tenant URL from a server name.
Preserve a working connection for the configured tenant. When several servers
fit and context does not decide, ask one necessary question.

Probe one unscoped get_schema for discovery/queryReference and
get_current_context for the current identity. Successful reads establish
reachability; errors remain errors. The available `swarm-setup-helper` agent can perform
read-only probing, or run it inline; neither path is an independent review.

Resolve the origin from configured connection metadata or the origin of an
actual currentView.pageUrl. A generic server label cannot prove a hostname.
Ask for the exact tenant URL only if required and unresolved. Do not invent
a coworkcanvas.com or assureswarm.com host. Match tenant and current user
before reusing stored state; discard cached schemas/IDs after a switch.

Studio's baseline has 11 types: audit, risk, control, issue, remediation,
process, policy, system, fsli, requirement, personnel. The real audit slug
stays audit even if an operator calls it an engagement or cycle. Vendors
use system.vendor = true. The baseline is a reference, not a requirement
to overwrite a customized tenant. Inspect typed schemas only for the types
needed by a requested check.

Keep connection metadata in session memory. When durable writable storage
is available, optionally merge .coworkcanvas/config.json without replacing
redaction_policy, installed_artifacts, or other user preferences. Bind it
to verified origin, tenant_id when exposed, and user_id. Preserve actual
MCP tool names. Store no secrets. With ephemeral/no filesystem, provide
session values or a credential-free downloadable config when supported;
state that it is not automatically persisted or installed.

A diagnostic schema snapshot may record the observation time, response kind,
tenant/user identity and normalized fingerprint. It cannot authorize future
writes. Unscoped summaries lack options; get the needed typed response fresh
in each new session. Follow all schema-discovery invalidation events.

Register or change an autopilot schedule only when the user asks for it.
Discover the actual scheduler, reuse existing authorization and schedule
preferences, and resolve only missing cadence/time/timezone. If unavailable,
provide a manual invocation or exact handoff; do not claim scheduling.
A schedule request does not authorize new sends, imports or approval actions.
```

## Inputs

- `--verify`: report current checks and gaps.
- `--scope basic|with-schema`: connection checks or those plus the schemas
  needed for the user's requested capability; default with-schema.
- `--verbose`: include supporting configuration and check details.

## Procedure

1. Read optional existing config only through available file access. Confirm
   identity and merge preferences; do not assume a file's tenant is current.
2. Discover matching MCP tools and probe the chosen server as above. If the
   connection is unavailable, use the selected client's actual integration
   settings/authentication flow. In Codex, use the available connection helper
   or integration UI; in another host, use its supported flow. Never prescribe
   a nonexistent connector name or ask for credentials in chat.
3. Record verified origin, user, actual tools and this session's discovery.
   Save durable config only when supported. Report successful connection
   without claiming that a local or downloaded file configured the client.
4. If no types exist after complete discovery, explain the current admin
   Studio import path. Offer coach-starter-pack only if listed in
   package-manifest.json and the user requests a prepared import. Retired
   audit/grc/reg/sox/generic overlays and authority_source migration are not
   supported. Current templates are at https://assureswarm.com/workflows/.
5. For a configured tenant, choose the next capability only from the user's
   requested work and this package inventory. Do not automatically launch
   an installer, schema rewrite, schedule, or artifact task.

## Verification

Report each check as passed, failed, or unavailable with its evidence:

- Connection: actual get_schema/get_current_context responses and identity.
- Requested schemas: current typed fields/options and any customization;
  snapshot age cannot establish validity.
- Permissions: only the current identity and operations actually observed.
  Missing admin capability requires the appropriate administrator.
- Storage/OAuth/server configuration: these are not established by a schema
  read. Mark unavailable over MCP when no supported inspection exists and
  point to the verified admin setting.
- Scheduling: actual scheduler response and identifier, only if requested.

Finish with the connection/check result and necessary remediation or supported
link. No mandatory completion question. All live schema changes and imports
remain separate admin-reviewed work.
