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

1. Run `/mcp`, select `plugin:auditober:auditober` and choose **Authenticate**. From a terminal, `claude mcp login plugin:auditober:auditober` does the same.
2. Your browser opens core.assureswarm.com. Sign in, check the Authorization Request and choose **Authorize Access**.
3. Back in Claude Code, run `/auditober:coach-setup`, or ask what is in your AssureSwarm workspace.

### Claude Desktop and Cowork

Download [`dist/auditober.zip`](dist/auditober.zip) and upload it as it is through **Customize**, then **Plugins**. Complete authentication in Claude when it asks, then run `/coach-setup`. Claude's [plugin guide](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) shows the current upload screens.

### Codex

```text
codex plugin marketplace add rp4/auditober-plugin
codex plugin add auditober@auditober-plugin
codex mcp login auditober
```

`codex mcp login` opens your browser at core.assureswarm.com. Sign in, check the Authorization Request and choose **Authorize Access**, then start a new Codex task and run `coach-setup`. The Codex app reads the same settings, so restart it to see the plugin there.

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

Every client signs you in through your browser at core.assureswarm.com. There are no API keys or tokens to copy. The agent gets only the access your own account has, and every change it proposes waits in the Activity Hub (the bee logo at the top left of the app) until you approve it.

If the connection fails:

- It keeps asking you to sign in: remove the connection, add it again, and finish the sign-in in the same browser.
- It connects but sees nothing: check you signed in with your Auditober email address, not another AssureSwarm account.
- A change you approved did not appear: open the suggestion from the Activity Hub and check that you approved every change in it, not only some.

Still stuck? Email [support@assureswarm.com](mailto:support@assureswarm.com?subject=Auditober) and name the tool you were connecting.

## Updates

- Claude Code: `claude plugin marketplace update auditober-plugin`, then `claude plugin update auditober@auditober-plugin`.
- Codex: `codex plugin marketplace upgrade auditober-plugin`.
- Claude Desktop and Cowork: upload the new `dist/auditober.zip`.

## What's here

- `plugins/auditober/`: the plugin (skills, agents, references, and `.mcp.json` pointing at the sandbox).
- `.claude-plugin/marketplace.json`: the marketplace Claude Code reads.
- `.agents/plugins/marketplace.json`: the marketplace Codex reads.
- `dist/auditober.zip`: the same plugin as one upload for Claude Desktop and Cowork.

This repository is generated from the AssureSwarm plugin source; changes made here are overwritten by the next release. To build your own plugin entry, start from these files or the downloads on the [plugins page](https://assureswarm.com/plugins/), and see [Build and submit your entry](https://assureswarm.com/auditober-instructions#entry).
