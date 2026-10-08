---
title: Connect an Enterprise AI Agent
description: Administrator-led OAuth setup for connecting AssureSwarm to Claude Desktop, Claude Code, Codex CLI, Microsoft Copilot Studio, Gemini, or ChatGPT.
---

For a corporate deployment, the workspace or platform administrator sets up and approves the AssureSwarm MCP connection first. Employees then sign in to AssureSwarm only when the approved platform asks them to authorize their own access. This keeps client registration, scopes, and available tools under organizational control.

Use **OAuth** for the hosted platforms below. A personal token is an exception for short-lived testing or clients that cannot use OAuth.

## Enterprise Setup: Administrator First

Before inviting employees to use an AI connection:

1. In **Admin -> AI Integrations**, allow the platform's OAuth client and restrict it to the minimum scopes it needs.
2. In the AI platform's administrative settings, create and approve the AssureSwarm MCP connection using the URL below.
3. Test the connection with an administrator account, select which tools the platform may expose, and publish or assign the connection to the intended group.
4. Tell employees to select the approved app or connector in a new chat. They may be asked to sign in to AssureSwarm, but they do not create the corporate integration themselves.

The connected agent can never exceed the signed-in person's AssureSwarm permissions. See [AI integrations](https://docs.assureswarm.com/admin/ai-integrations/) for governance and revocation.

## Exception: Personal-Token Testing

Use a personal token only when the client cannot complete the OAuth path below.

1. Sign in to your tenant.
2. Open the **OAuth Setup** page.
3. Name the token and generate it.
4. Copy it immediately - it is shown once.
5. It expires after 30 days. Generate a new one when it does.

:::caution[Treat a personal token like a password]
Anyone holding it can act as you, within your own permissions and the token's scopes. Do not paste it into shared configuration, source control, or a chat. Revoke and replace any token that is exposed.
:::

## Your MCP URL

Use the exact MCP URL supplied by your organization, including its custom domain when applicable. Every client below needs that endpoint; a typical hosted URL looks like this:

```text
https://<tenant>.assureswarm.com/mcp
```

AssureSwarm also supports OAuth discovery and dynamic client registration. Most clients below find these endpoints automatically:

```text
https://<tenant>.assureswarm.com/.well-known/oauth-authorization-server
https://<tenant>.assureswarm.com/.well-known/oauth-protected-resource
```

## Plugin Distribution for Codex, Claude, and Copilot

Download the Swarm or Audit plugin distribution from [assureswarm.com/plugins](https://assureswarm.com/plugins/).

For Claude on the web, Desktop or Cowork, upload the distribution ZIP as downloaded through **Customize -> Plugins**. Enable your organization's approved AssureSwarm connector, complete sign-in, then run `coach-setup`. See [Claude's plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) for the current upload interface. Direct upload does not require a local Node.js installation.

For Codex, Claude Code or GitHub Copilot in VS Code, extract the same distribution and run this command with Node.js 20 or later and npm:

```text
node setup.mjs
```

Choose your clients and enter the exact MCP URL supplied by your organization. You can supply both choices directly:

```text
node setup.mjs --clients codex,claude,copilot --mcp-url https://tenant.example/mcp
```

Setup prepares separate client packages from the same release. It installs Codex and Claude Code plugins when their CLIs are available and prints manual steps otherwise. For Claude Desktop/Cowork, it creates a Claude import ZIP; for VS Code, it creates a settings fragment to merge into your existing settings. Each app keeps its own connection and browser authorization.

Codex uses the bundled browser connection helper and verifies authenticated read calls. The installer reports prepared files, installed plugins and authenticated connections separately. Start a new client session after installation, then run `coach-setup` to select the connection and capture your workspace's schema. To recheck an installed Codex connection:

```text
node "<installed-plugin-root>/scripts/codex-mcp.mjs" --check
```

Use `--setup` in place of `--check` when browser sign-in is needed. Keep the helper running while consent completes. Do not reuse an expired callback tab or clear another client's OAuth cache.

The native `swarmplugin.zip` and `auditplugin.zip` downloads remain available for
direct Claude import. Setup checks the tools the current host exposes.
Evidence extraction and independent grading require a supported isolated
worker or a verified external return packet. If that capability is missing,
the skill prepares a handoff and reports the work as pending. Deterministic
analytics can use their documented isolated script runner. Installation alone
does not supply missing tools or prove an authenticated connection.

## Why OAuth Is the Enterprise Default

OAuth is the recommended path for Claude Desktop, the developer CLIs (Claude Code, Codex, Gemini CLI), Microsoft Copilot Studio, Gemini, and ChatGPT:

- Employees sign in on the AssureSwarm site only when the approved platform prompts them; they do not paste a AssureSwarm personal token into the AI application.
- The application receives a scoped authorization for the person who signed in, not a shared tenant credential.
- Administrators can govern or revoke the client from **Admin -> AI Integrations**.

Request only the scopes the agent needs. For read-only reporting, `read:data` is usually sufficient; see [MCP overview](https://docs.assureswarm.com/mcp/) for the tool-to-scope mapping.

## Claude Desktop

First, the Claude workspace administrator must allow custom connectors under the organization's Claude settings. An authorized administrator or designated connector owner then opens **Settings -> Connectors**, chooses **Add custom connector**, and enters the MCP URL above. Claude opens the AssureSwarm sign-in and consent flow automatically.

After the connector is approved for the organization, employees enable it in a new chat and complete AssureSwarm sign-in only if Claude asks them to authorize their own access.

Current Claude Desktop remote connectors are configured in **Settings -> Connectors**; do not add this remote URL to `claude_desktop_config.json`. See Anthropic's [custom remote connector guide](https://support.anthropic.com/en/articles/11175166-about-custom-integrations-using-remote-mcp).

## Claude Code and Codex CLI

For an MCP-only connection, use the client's native browser OAuth flow below. If the plugin distribution already supplies a working connection, reuse it. Do not add a duplicate server or remove an entry used by another tenant.

### Claude Code

Inspect configured servers with `claude mcp list`. If none points to the intended tenant, add one using its exact URL:

```text
claude mcp add --transport http coworkcanvas https://tenant.example/mcp
```

Use an unused server name if `coworkcanvas` already identifies another tenant. Start a new session, run `/mcp`, select the server and choose **Authenticate**. Complete browser sign-in and consent. If the pending flow expires, restart authentication from `/mcp`.

See [Claude Code's MCP guide](https://code.claude.com/docs/en/mcp).

### Codex CLI

Inspect existing servers with `codex mcp list`. Inspect the matching entry before changing it:

```text
codex mcp get coworkcanvas
```

If no entry points to the intended tenant, add one with an unused name and the exact URL supplied by your organization:

```text
codex mcp add coworkcanvas --url https://tenant.example/mcp
```

Adding the server saves configuration. Browser authentication is a separate command:

```text
codex mcp login coworkcanvas
```

Complete sign-in and consent, then verify `get_schema` and `get_current_context` through that connection. A successful `initialize` response or a tool listing alone does not prove authenticated access to the tenant.

If native login fails with a confirmed OAuth metadata incompatibility, use the public plugin distribution's bundled Codex helper. It uses pinned `mcp-remote@0.8.6` with the configured endpoint and browser OAuth. Before installing it, inspect existing connections and avoid enabling two entries for the same tenant. Do not clear OAuth caches or modify Claude or Copilot settings to troubleshoot Codex. See the [Codex MCP guide](https://developers.openai.com/codex/mcp/) and [`mcp-remote` documentation](https://github.com/punkpeye/mcp-remote).

Start with read access. The client must request additional scopes before browser
consent can grant them. A write-capable tool in the catalog does not prove that
the current authorization includes its scope.

For the installed Codex plugin helper, choose the complete additional scope set
needed on top of its read-only defaults and reauthorize:

```text
node "<installed-plugin-root>/scripts/codex-mcp.mjs" --scopes "read:suggestions write:suggestions write:documents"
```

The argument accepts spaces or commas. This example enables pending-suggestion
reads, proposed changes, and document uploads. Each selection replaces the
previous additional selection; include any additional scopes you still need.
Use `--scopes default` to return to the read-only defaults.
The helper saves the selection and preserves it on updates. Complete the new
browser consent, then check authenticated reads with `--check`. That check does not verify write
authorization. Native CLI
connections use their own scope-selection and login controls.

## GitHub Copilot in VS Code

The plugin distribution prepares a Claude-format plugin and `vscode.settings.json`. Merge its `chat.plugins.enabled` and `chat.pluginLocations` entries into your VS Code user settings, preserving other settings and plugins. Reload if needed, review and trust the plugin, then start its MCP server and complete browser sign-in. Verify `get_schema` and `get_current_context`.

If your editor does not support agent plugins, use the prepared `vscode.mcp.json` for the connection alone. Open **MCP: Open User Configuration** from the Command Palette and merge its server entry into the existing `servers` object. Use either the plugin or this MCP-only fallback so that the same server is not loaded twice. See the [VS Code plugin guide](https://code.visualstudio.com/docs/agent-customization/agent-plugins) and [MCP guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

## Microsoft Copilot Studio

An administrator or authorized maker configures the MCP server in the Copilot Studio agent that the business will use:

1. Open **Tools**, select **Add a tool**, then select **New tool -> Model Context Protocol**.
2. Enter a server name and description, then set **Server URL** to the AssureSwarm MCP URL above.
3. Select **OAuth 2.0** as the authentication type. Dynamic client registration and discovery are the simplest option when shown by the wizard.
4. Create the connection and complete the AssureSwarm sign-in and consent flow.
5. Add the created tool to the agent, select the tools it may use, then test and publish the agent.

If your Copilot Studio configuration requires a manually registered OAuth client, register its redirect URI and requested scopes in **Admin -> AI Integrations** before completing the wizard. Share the published agent only with the intended employees. See Microsoft's [MCP onboarding guide](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent).

## Gemini

### Gemini CLI

For a managed Gemini CLI deployment, an administrator should distribute or approve the configuration. Add the remote HTTP server, then start the OAuth flow:

```text
gemini mcp add --transport http coworkcanvas https://<tenant>.assureswarm.com/mcp
```

In Gemini CLI, run:

```text
/mcp auth coworkcanvas
```

Your browser opens to AssureSwarm for sign-in and consent. Confirm the connection with `gemini mcp list`. Gemini CLI can discover AssureSwarm's OAuth endpoints and handle dynamic client registration. See the [Gemini CLI MCP guide](https://geminicli.com/docs/tools/mcp-server/).

### Gemini Enterprise

In Gemini Enterprise, an administrator creates a **Custom MCP Server** data store. Use the MCP URL above and configure OAuth with the AssureSwarm authorization and token URLs discovered from your tenant. If Gemini Enterprise requires a registered client, first register its redirect URI and requested scopes in **Admin -> AI Integrations**, then enter its client ID and secret in Gemini Enterprise. Assign the resulting data store or app to the intended employee groups. See [Set up your custom MCP server data store](https://cloud.google.com/gemini/enterprise/docs/connectors/custom-mcp-server/set-up-custom-mcp-server).

## ChatGPT

ChatGPT connects to remote MCP servers through a custom app. For corporate workspaces, individual employees normally cannot enable Developer mode or create a new corporate MCP app. A ChatGPT workspace administrator or owner must enable the capability, create the app, and publish it to the intended users.

1. In ChatGPT on the web, the workspace administrator enables **Developer mode** under the workspace's Apps or Connected Data settings.
2. The administrator selects **Create** under Apps.
3. Enter the AssureSwarm MCP URL and choose **OAuth** authentication.
4. Select **Scan Tools**, complete the AssureSwarm sign-in and consent flow, then create and enable the app.
5. The administrator tests the app, configures its available actions and access, then publishes it.
6. Employees start a new chat and select the approved app from the tools menu.

ChatGPT uses the endpoint's OAuth metadata during setup. If it asks to authenticate again after a session expires, reconnect the app or ask your administrator to verify refresh-token settings. See OpenAI's [developer mode and MCP apps guide](https://help.openai.com/en/articles/12584461-developer-mode-and-full-mcp-connectors-in-chatgpt-beta).

## Personal-Token Fallback

Use a personal token only for a client that cannot complete the OAuth path above. Pass it as an `Authorization: Bearer <your-token>` header using that client's secure credential mechanism.

## Verify the Connection

Ask your agent to call `get_schema`, then `get_current_context`. Confirm that the returned schema and signed-in identity belong to the intended tenant. A listed tool or prepared configuration alone does not verify this access.

See the [Agent operating guide](https://docs.assureswarm.com/agents/) for how to work effectively once connected.

## When It Doesn't Work

| Symptom                         | Check                                                                                                            |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| OAuth window does not open      | Confirm the URL ends in `/mcp`, then reconnect or use the client-specific Authenticate option.                   |
| `401` error                     | Reconnect through OAuth. For token fallback, the token may be expired (30 days), revoked, or pasted incorrectly. |
| `403` or a scope error          | The authorization lacks the tool's required scope - check the tools table on [MCP overview](https://docs.assureswarm.com/mcp/).           |
| Tools don't appear              | The client may need a reload, a new chat, or an administrator to approve the connector.                          |
| Connects, but results are empty | Your own access is the ceiling - see [Permissions](https://docs.assureswarm.com/concepts/permissions/).                                  |
| Codex is configured but has no authenticated tools | Run `codex mcp login <name>`, complete browser consent, then verify `tools/list`, `get_schema`, and `get_current_context`. |
| Codex fails during OAuth metadata discovery | Verify the intended tenant, then use the distribution's bundled Codex helper without duplicating an existing connection. |
| Consent page sat unapproved and now sign-in fails | Restart authentication in the client or its bundled helper instead of reusing the expired browser callback tab. |

See [Troubleshooting](https://docs.assureswarm.com/troubleshooting/) for more.
