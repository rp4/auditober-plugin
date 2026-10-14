# Auditober plugin

The AssureSwarm Swarm plugin for [Auditober 2026](https://assureswarm.com/auditober/), set up for the Auditober sandbox at `https://core.assureswarm.com/mcp`.

It gives your agent the skills the Swarm agent uses: create and update records, link them, build and run workflows, fill forms, upload evidence, query your team's data and open dashboards. It adds `auditober-info`, which answers questions about the event from the [participant guide](https://assureswarm.com/auditober-instructions): sign-in, the Bluth Company data, what to build, how to submit and where to get help.

You need your Auditober invitation. Sign in with your Auditober email address, and use only mock data.

## Install

### Claude Code

```text
/plugin marketplace add rp4/auditober-plugin
/plugin install auditober@auditober-plugin
```

Start a new session, then sign in:

1. Run `/mcp`, select `plugin:auditober:auditober` and choose **Authenticate**.
2. Your browser opens core.assureswarm.com. Sign in, check that the Authorization Request includes the [complete tool scope set](#sign-in) and choose **Authorize Access**.
3. Back in Claude Code, run `/auditober:coach-setup`, or ask what is in your AssureSwarm workspace.

### Claude Desktop and Cowork

Download [`dist/auditober.zip`](dist/auditober.zip) and upload it as it is through **Customize**, then **Plugins**. Complete authentication in Claude when it asks, authorize the [complete tool scope set](#sign-in), then run `/coach-setup`. Claude's [plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) shows the current upload screens.

### Codex

```text
codex plugin marketplace add rp4/auditober-plugin
codex plugin add auditober@auditober-plugin
codex mcp login auditober
```

`codex mcp login` opens your browser at core.assureswarm.com. Sign in, check that the Authorization Request includes the [complete tool scope set](#sign-in) and choose **Authorize Access**, then start a new Codex task and run `coach-setup`. The Codex app reads the same settings, so restart it to see the plugin there.

The installed `.codex.mcp.json` requests the full tool scope set on first sign-in. Claude's `.mcp.json` requests the same scopes through `oauth.scopes`. Each client keeps its own authorization.

### Meta Muse Code

We wrote these steps from Meta's Muse Code documentation and have not tested them yet. Add the server to `~/.config/muse/settings.json`, keeping the settings already in the file:

```json
{
  "schema_version": 1,
  "mcp_servers": {
    "auditober": {
      "transport": "streamable_http",
      "url": "https://core.assureswarm.com/mcp",
      "headers": {},
      "enabled": true,
      "mode": "optional"
    }
  }
}
```

Then run `muse mcp login auditober` and finish the sign-in it starts. Muse Code can import skills from Claude Code with `muse skills import --from claude`; we have not checked whether that includes plugin skills.

### Other agents

ChatGPT, Microsoft Copilot Studio, GitHub Copilot and Gemini CLI connect to the same MCP URL without this plugin. The [Bring your own agent](https://assureswarm.com/auditober-instructions#mcp) section of the guide has the steps for each.

## Sign-in

Every client signs you in through your browser at core.assureswarm.com. There are no API keys or tokens to copy. Authorize the complete MCP tool scope set during initial setup:

```text
openid profile email
read:context read:items read:data read:workflows read:dashboards read:documents
read:suggestions write:suggestions write:documents
```

The read scopes cover your context, records, queries, workflows, dashboards, documents and review queue. `write:suggestions` lets the agent propose changes. Those proposals wait in the Activity Hub (the bee logo at the top left of the app) for human approval. `write:documents` lets it attach files directly when you request an upload. Your account permissions and the tenant's client policy still apply.

The plugin does not request `approve:suggestions`. No current MCP tool needs it, or `write:forms`, `write:items`, `write:workflows` or `write:dashboards`. Forms, records and workflow changes use suggestions; approval remains yours.

A successful login, a visible tool or a successful `get_schema`/`get_current_context` read does not prove the whole scope set was granted. `coach-setup` reports the connection and scope evidence separately. Full tool setup is verified only when the granted scopes cover the requested set. If the host cannot show grant metadata, full tool authorization remains unverified.

If the connection fails:

- It keeps asking you to sign in: use your client's supported authentication flow and finish sign-in in the same browser.
- It connects but sees nothing: check you signed in with your Auditober email address, not another AssureSwarm account.
- Reads work but the review queue, proposals or uploads fail: an older read-only OAuth client registration can cap a new authorization. Update the plugin, use the client's connection settings to update the registration and reauthorize, and check the requested and granted scopes. An administrator may need to change the registration policy. Do not edit tokens or delete credential files manually.
- A change you approved did not appear: open the suggestion from the Activity Hub and check that you approved every change in it, not only some.

If you installed the portable Swarm distribution, its Codex helper can select the full tool scope set with `node "<installed-plugin-root>/scripts/codex-mcp.mjs" --scopes default`, using the path printed by setup. Complete browser consent and restart the task. `--scopes read-only` selects read-only access. Explicit choices persist through updates; the helper uses separate authorization profiles for each tenant and effective scope set.

Still stuck? Email [support@assureswarm.com](mailto:support@assureswarm.com?subject=Auditober) and name the tool you were connecting.

## Updates

- Claude Code: `claude plugin marketplace update auditober-plugin`, then `claude plugin update auditober@auditober-plugin`.
- Codex: `codex plugin marketplace upgrade auditober-plugin`.
- Claude Desktop and Cowork: upload the new `dist/auditober.zip`.

An existing authorization keeps its earlier grant until you reauthorize. After updating Claude Code, open `/mcp`, select `plugin:auditober:auditober` and authenticate again. In Claude Desktop or Cowork, use the connection's authentication settings after uploading the update.

After updating Codex, request the full scope set explicitly:

```text
codex mcp login auditober --scopes openid,profile,email,read:context,read:items,read:data,read:workflows,read:dashboards,read:documents,read:suggestions,write:suggestions,write:documents
```

Complete browser consent, restart the task and run `coach-setup` again. If the granted scopes still fall short, update the old client registration through the client's supported connection settings or ask the tenant administrator to change its policy. Repeated sign-in alone does not expand a registration's allowed scopes.

## What's here

- `plugins/auditober/`: the plugin's skills, agents and references. `.mcp.json` configures Claude's sandbox connection with `oauth.scopes`; `.codex.mcp.json` configures Codex's connection with a `scopes` array. Both request the full MCP tool scope set.
- `plugins/auditober/.codex-plugin/plugin.json`: points Codex to `.codex.mcp.json`.
- `.claude-plugin/marketplace.json`: the marketplace Claude Code reads.
- `.agents/plugins/marketplace.json`: the marketplace Codex reads.
- `dist/auditober.zip`: the same plugin as one upload for Claude Desktop and Cowork.

This repository is generated from the AssureSwarm plugin source; changes made here are overwritten by the next release. To build your own plugin entry, start from these files or the downloads on the [plugins page](https://assureswarm.com/plugins/), and see [Build and submit your entry](https://assureswarm.com/auditober-instructions#entry).
