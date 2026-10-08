# Auditober instructions

Source: https://assureswarm.com/auditober-instructions, captured 7 October
2026. Headings carry the page anchors, so `#submit` links to
https://assureswarm.com/auditober-instructions#submit. Video captions and
button labels are left out; every instruction, fact and link is kept.

Get into your sandbox, build your entry and send it in.

Contents: 1. Start here · 2. Find your way around · 3. How AssureSwarm
works · 4. Do the work · 5. Bring your own agent · 6. Build and submit your
entry · 7. Get help and give feedback.

## 1. Start here (`#start`, `#before-you-start`)

October 2026. Online, free sandbox.

**Build your Auditober entry.** In the app: workflows and evidence flows.
Built externally: dashboards using MCP data, and plugins extending our
existing plugins.

- Open the app: https://core.assureswarm.com/
- Open the Swarm agent: https://demo.assureswarm.com/
- Submit by 31 October. Cutoff time and timezone to be confirmed.

**Training.** October 8: Audit Engineering with Cherry Hill Advisory.
Program and CPE details: https://assureswarm.com/auditober/#training

**Live help.** Book your office hours at
https://calendar.app.google/Lk1xH6hJJVfKARuD6 and pick a time on the
booking calendar.

**Email your entry or ask a question.** support@assureswarm.com (subject
"Auditober"). Attachments: 25 MB or less, combined. You can enter multiple
categories. No category needed in your email.

### Joining, AI allowance and eligibility

Join with your work email on the Auditober signup page
(https://assureswarm.com/auditober/). Signup joins the update list; your
invitation gives you sandbox access. You need the invitation and a web
browser. To enter the event, email your submission files.

Your sandbox has two parts. The app (https://core.assureswarm.com/) holds
your team's copy of the Bluth Company audit data. The Swarm agent
(https://demo.assureswarm.com/) is an AI assistant that works in the app
for you. Use only mock data; keep your organization's data out of the
sandbox.

Each team shares a $50 Swarm agent allowance across the event, subject to a
daily limit. See AI allowance (`#limits`). Your own AI agent is optional;
its provider's account requirements, usage limits and charges apply
separately.

Awards are for practitioners working in an organization's internal audit
function, according to the event page (https://assureswarm.com/auditober/).
Full eligibility rules have not yet been published. Ask the organizers if
you are unsure whether you qualify.

Clips marked Illustration on the page show an example setup or
conversation.

## 2. Find your way around (`#around`)

### The app at core.assureswarm.com (`#core-tour`)

The icons across the top take you to Dashboards, one page for each kind of
record (risks, controls, issues, policies and the rest), My Items,
Templates, Time and Admin. Hover over an icon to see its name. The bee logo
at the top left opens the Activity Hub, where the agent's suggestions wait
for you. Every record has its own page, and you can share any page's link
with your team.

### Your team (`#team`)

Everyone who signed up from the same company is on one team. People given
accounts for the event start as admins; teammates you add later can be
Users or Admins. As an admin, you can see and change everything your
teammates build. People who signed up with a personal email address each
get a team of their own. To see who is on your team, click the Admin icon
(the last one in the top bar), then User Permissions.

Other teams cannot browse your sandbox. Check your submission files and
linked workflows for private data before sharing them. Review the
submission checklist (`#submission-checklist`) before emailing your entry.

### Sign in to the Swarm agent (`#agent-sign-in`)

1. Go to https://demo.assureswarm.com/ and choose Sign in with AssureSwarm.
2. The agent sends you to core.assureswarm.com. Sign in there if you are
   not already, then check the Authorization Request and choose Authorize
   Access.
3. You land back in the chat, signed in as yourself. The agent can only see
   and change what you can.

### The agent at demo.assureswarm.com (`#agent-tour`)

- Type a request in plain English, or type / to pick a skill such as
  item-create, workflow-build or query-data.
- New chat clears the conversation. Feedback sends us an issue or an idea
  (see `#feedback`).
- The panel on the right shows the app (Canvas), a report or a dashboard
  next to the chat, so you can watch changes land.
- Use the user menu at the top right to open Dashboards or Sign Out. Follow
  the email submission instructions to enter Auditober.

Conversations with the agent are recorded so we can improve the product,
and the AssureSwarm team can read them. The chat shows a notice when
recording is on.

### My Work (`#my-work`)

My Work lists the workflow steps assigned to you and the ones ready to
start. It is the first place to look when you come back to the sandbox.

### A record's page (`#item-page`)

Open any risk, control, issue or policy to see its fields, its linked
records, its documents and the workflows that run on it. Click a title or a
field to edit it in place.

### The Bluth Company data (`#bluth`)

Every team starts with the same fictional company, so entries can be
compared fairly. Your copy holds 744 records: 200 risks, 200 controls, 129
compliance requirements, 53 processes, 47 policies, 28 issues, 18
remediations, 20 financial statement line items, 16 people, 14 systems, 10
models and 9 audits. They are joined by 2,223 links and worked on by 50
workflow templates with 236 runs in progress or complete.

Change anything you like. Your edits stay in your team.

## 3. How AssureSwarm works (`#concepts`)

These eight ideas explain the records, workflows and agents you will use in
your sandbox.

### Items and item types (`#items`)

Every record is an item: a risk, a control, an issue, a policy, an audit.
Each item type has its own fields, set by the team's admins. An admin can
add a field or a new item type. See Create or change a record
(`#create-item`) for the steps.

### Workflows (`#workflows`)

A workflow is a piece of audit work written down as steps, so agents and
auditors run it the same way every time. You define it once as a template,
then start a run of it on an item, such as a walkthrough on a process. Each
step has instructions, a result that records what was done, and approvers
who sign it off. An approved step locks.

### Forms (`#forms`)

A step can send a form to someone who is not running the workflow, such as
a control owner who has to answer three questions. Use a form only for
information you cannot get any other way. The person running the step
writes their work in the step result, and sign-off is the step's approval.

### Links (`#links`)

Items link to each other: a risk to the controls that address it, a control
to the process it sits in, an issue to the control that failed. Steps link
to the items they test. These links are what let a dashboard answer which
processes have no tested controls?

### The Universe: your audit knowledge graph (`#universe`)

The Universe dashboard draws every item and link as one graph. Pick an item
to focus on it and see what sits one or two links away, such as every
control, workflow and issue connected to one process.

### Dashboards (`#dashboards`)

The app has 19 built-in dashboards, all filled from your team's data:
Universe, Org Chart, Executive, Operational, My Work, AI Activity, Capacity
Monitoring, Workflow Runs, Risks, Third-Party Risk, Policy Lifecycle,
Policy Exceptions, Audit Plan, Model Inventory, Issues and Remediations,
RCM, Compliance Requirements, SOX Program and Workflow Coverage.

For your Auditober dashboard entry, build an HTML dashboard outside the
app, using data from the AssureSwarm MCP. See what to build
(`#choose-entry`) and which files to submit (`#skill-plugin-entry`).

### Suggestions and review (`#suggestions`)

Agents never change your records directly. Everything an agent wants to do
arrives as a suggestion in the Activity Hub, which opens from the bee logo
at the top left. Click a suggestion to see each proposed change marked on
the page, then approve or reject each change with the check or the X, or
all of them at once. Nothing is saved until you do. The AI Activity
dashboard shows every suggestion and what happened to it.

### MCP (`#mcp-concept`)

The Model Context Protocol (MCP) is the standard way an AI agent connects
to an outside system. AssureSwarm is built on it. The Swarm agent uses MCP
to work in your sandbox, and you can connect Claude, ChatGPT, Codex or
Gemini the same way. Every agent has only the access of the person who
signed it in, and its changes go through the same suggestion review. Use
Bring your own agent (`#mcp`) for the connection steps and troubleshooting.

## 4. Do the work (`#howto`)

You can do each task by hand in the app or ask the agent to do it. Copy a
prompt into the agent chat and replace any details in square brackets.
Review the agent's suggestions in the Activity Hub: open it with the bee
logo at the top left, then approve or reject them (see `#suggestions`).

### Create or change a record (`#create-item`)

By hand:

1. In the top bar, click the icon for the kind of record, for example
   Risks. Hover over an icon to see its name.
2. Click New Risk at the top right of the list.
3. Fill in the fields on the Create Risk page and click Create.

To change a record, open it. Click the title to rename it, or click the
description to edit it. Every other field is in the Details card on the
right: click a field, change it, and click Save changes. Click All n fields
to see the ones that are hidden.

With the agent:

- Create a record: "Create a new risk called “Vendor invoices are paid
  twice” for the Accounts Payable process."
- Change a record: "Rename the risk “Vendor invoices are paid twice” to
  “Duplicate vendor payments”."

### Link two records (`#link-items`)

By hand:

1. Open one of the two records.
2. In the Linked Items card on the right, click +.
3. Type part of the other record's name and click it in the results.

Links you add by hand are related links. To remove one, click the X next to
it.

With the agent:

- Link two records: "Link the “Duplicate vendor payments” risk to the
  three-way match control."
- Link several records: "Link every accounts payable control to the
  Accounts Payable process."

### Build a workflow template (`#build-workflow`)

By hand:

1. Click the Templates icon in the top bar, then Create Template.
2. Give the workflow a name and a description, and choose the item type it
   runs on, for example Process.
3. Click Add Step once for each step.
4. Click a step to open Configure Step. Name it, write its Instructions, and
   click Save Changes.
5. Click Save Template.

With the agent:

- Build a template: "Build a reusable workflow template for reviewing
  vendor master data changes. It should run on Process records, with human
  review where judgment or sign-off is needed."

The agent drafts a workflow template and sends it for approval. Strong
workflows keep human sign-off to the points where it adds judgment. Add a
form to a step only when someone outside the workflow has to supply
information.

### Run a workflow (`#run-workflow`)

By hand:

1. Open the record. In the Workflows card, click Add Workflow, tick the
   template, and confirm.
2. Click View on the new workflow, then click a step to open it.
3. Choose Add, then Approver. Pick who signs off and at which level, and
   click Save approvers. Add a due date the same way.
4. On the Step Result card, click Edit, write what you did and found, and
   click Save.
5. The approver clicks Approve. When every required approver has approved,
   the step locks. Remove Approval unlocks it.

With the agent:

- Start a workflow: "Run the walkthrough template on the Accounts Payable
  process."
- Set an approver: "Set [reviewer name] as the approver for the steps in
  that workflow, with a due date of [date]."
- Do a step: "Do the next ready step in that workflow using its linked
  records and documents, and draft the step result for my review."
- Work through my queue: "Draft the ready workflow steps assigned to me in
  one pass and report anything that still needs my input."

Review the draft results, then approve each step yourself. Only a person
can sign off a step.

### Attach evidence (`#evidence`)

By hand:

1. Open the step. In Supporting Documents, click Add. If the section is
   missing, choose Add, then Supporting document, at the top of the step.
2. Choose Upload File, or drag a file onto the section.
3. To point to an online document instead, choose Link External URL, paste
   a OneDrive, SharePoint or Google Drive link, and click Link.

On a record, upload a file into any document field. Links to online
documents go on steps only.

With the agent: attach a mock file to the chat, then use the upload prompt.
For an online document, use the link prompt.

- Upload a file: "Upload the file I attached as supporting evidence for
  [step name] in [workflow name] on [record name]."
- Link a document: "Link [document URL] as supporting evidence for [step
  name] in [workflow name] on [record name]."

Attach the evidence before asking the agent to do the step. Use mock files
only. Nothing from your organization belongs in the sandbox.

### Find what you need (`#query`)

By hand:

- Every list, such as Risks, has a search box, a Filter button for that
  record type's fields, and a sort by due date or creation date.
- Click Select to pick records and download them.
- On a dashboard, open Filter to narrow its scope and reporting range.

There is no search across all record types. Start from the list or
dashboard closest to your question.

With the agent:

- Summarize risks: "How many high or critical residual risks do we have, by
  category?"
- Find overdue work: "List every overdue remediation with its owner."

## 5. Bring your own agent (`#mcp`)

You can connect the AI tool you already use to your sandbox. Every client
uses the same address and signs you in through core.assureswarm.com.

MCP URL: `https://core.assureswarm.com/mcp`

### Claude Desktop (and claude.ai) (`#mcp-claude`)

1. Open Settings, then Connectors, and choose Add custom connector.
2. Paste the MCP URL and add the connector.
3. Sign in to AssureSwarm in the window Claude opens and approve access.
4. In a new chat, turn the connector on and ask what is in my AssureSwarm
   workspace?

On a Claude Team or Enterprise plan, your workspace owner may have to allow
custom connectors first.

### ChatGPT (`#mcp-chatgpt`)

1. In ChatGPT on the web, turn on Developer mode in the Apps settings.
2. Choose Create, paste the MCP URL and pick OAuth.
3. Choose Scan Tools, sign in to AssureSwarm and approve access, then
   create the app.
4. Start a new chat and select the app from the tools menu.

In a company ChatGPT workspace, only an owner or admin can turn on
Developer mode.

### Copilot (`#mcp-copilot`)

Microsoft Copilot Studio (you need maker rights in your organization's
Copilot Studio):

1. In your agent, open Tools, choose Add a tool, then New tool and Model
   Context Protocol.
2. Enter a server name, paste the MCP URL as the Server URL, and choose
   OAuth 2.0 with dynamic discovery.
3. Create the connection, sign in to AssureSwarm and choose Authorize
   Access, then add the tool to your agent and test it.

GitHub Copilot in VS Code: open the Command Palette, run MCP: Open User
Configuration, and add a server under `servers` with the MCP URL. Start it
and sign in when asked. The AssureSwarm plugin can also set this up for
you.

Copilot Studio options that need a manually registered OAuth client are not
available on the Auditober sandbox. Use dynamic discovery.

### Claude Code, Codex CLI and Gemini CLI (`#mcp-cli`)

Claude Code: add the server, then run `/mcp` in a new session, select it
and choose Authenticate.

```text
claude mcp add --transport http assureswarm https://core.assureswarm.com/mcp
```

Codex CLI: add the server, then sign in.

```text
codex mcp add assureswarm --url https://core.assureswarm.com/mcp
codex mcp login assureswarm
```

Gemini CLI: add the server, then run `/mcp auth assureswarm` inside Gemini
CLI.

```text
gemini mcp add --transport http assureswarm https://core.assureswarm.com/mcp
```

If you already have a server called `assureswarm` pointing somewhere else,
pick another name.

### The AssureSwarm plugin (`#mcp-plugin`)

The plugin gives Claude, Codex and GitHub Copilot the same audit skills the
Swarm agent has. Download it from https://assureswarm.com/plugins/, extract
it, and run `node setup.mjs` (Node.js 20 or later). Enter the MCP URL above
when it asks. Then start a new session and run coach-setup.

### If the connection fails (`#mcp-troubleshooting`)

- It keeps asking you to sign in: remove the connector, add it again, and
  finish the sign-in in the same browser.
- It connects but sees nothing: check you signed in with your Auditober
  email address, not another AssureSwarm account.
- A change you approved did not appear: open the suggestion from the
  Activity Hub and check that you approved every change in it, not only
  some.

Still stuck? Email support@assureswarm.com and name the tool you were
connecting.

## 6. Build and submit your entry (`#entry`)

### Choose what to build (`#choose-entry`)

You can enter a workflow or evidence flow, a dashboard or a plugin. The four
categories are risk assessment, testing, operational audit and most
creative. You can participate in multiple categories; you do not need to
specify a category when submitting.

- Workflows and evidence flows: build and run them within the AssureSwarm
  app, using the Bluth mock data. Your submission includes links to those
  workflows or evidence flows in the app.
- Dashboards: build them outside the app with your own agent or
  development tools, using data from the AssureSwarm MCP. Submit the HTML
  file with instructions for connecting and running it.
- Plugins: build them outside the app, on top of an existing AssureSwarm
  plugin. Extend its files and skills, then test your version with your own
  agent connected over MCP.

### Start from our plugin and data (`#starting-points`)

For a plugin entry, start from an existing AssureSwarm plugin and extend it
outside the app. Use the Bluth mock data to test your entry.

- The AssureSwarm plugin: the skills the Swarm agent uses, as editable
  files. Download the Audit plugin
  (https://assureswarm.com/plugins/auditplugin-distribution.zip) for audit
  work, or the Swarm plugin
  (https://assureswarm.com/plugins/swarmplugin-distribution.zip) for the
  general operator skills. Each ZIP sets itself up for Claude, Codex and
  GitHub Copilot (see `#mcp-plugin`). Copy a skill, change it, and run your
  version from your own agent. The plugins page
  (https://assureswarm.com/plugins/) lists every variant.
- The Bluth Company data: the same data set every team starts with, as
  https://assureswarm.com/auditober-instructions/downloads/bluth-company-auditober.json
  (3.4 MB). You can import an edited copy from Admin, then Data Management.
  Records are always added as new ones, so first remove from the file any
  records your team already has.

### Submit by email (`#submit`)

Send all Auditober submissions to support@assureswarm.com as email
attachments. Submitting an entry means you agree to the open-source
contribution terms below (`#open-source`).

Accepted files are Word documents (`.doc` or `.docx`), PowerPoint
presentations (`.ppt` or `.pptx`), HTML files (`.html`), Markdown files
(`.md`) and plugin ZIP files (`.zip`). Keep the combined attachment size to
25 MB or less.

- Use the subject `Auditober submission: [team name] / [entry title]`.
- Include your name or team name and the entry title.
- Attach your files and include links to any workflows or evidence flows
  you built in the app. The file guidance below explains what to send for
  each type of entry.
- In your email or an attached document, explain the audit problem, what
  you built, how another participant can use it and what happened when you
  tested it on mock data.

Entries close on October 31, 2026. The exact cutoff time and timezone are
still to be confirmed. Keep a copy of your sent email and attachments.

### Files and links to include (`#skill-plugin-entry`)

- Workflows and evidence flows built in the app: include a link to each one
  in your email or write-up. Open it in the app and copy its page URL.
  Attach a Word document, PowerPoint presentation or Markdown file
  explaining what it does and how to use it.
- Dashboards built externally: attach the HTML file and check that it uses
  data from the AssureSwarm MCP. Include the setup steps needed to connect
  and run it.
- Plugins built externally: attach your extended plugin as a ZIP with its
  files and installation instructions. Name the existing AssureSwarm plugin
  you started from and explain what you added or changed.

### Before you email your entry (`#submission-checklist`)

- Open the files you plan to attach and try the entry on mock data. Check
  that it does what your write-up describes.
- Check each workflow or evidence-flow link opens in the app. For a
  dashboard, test that the attached HTML uses MCP data; for a plugin, check
  that the ZIP contains your extended plugin and the files needed to run
  it.
- Explain any changes to the provided templates or data. For a plugin
  entry, identify the base plugin and your changes.
- Remove real organization names, private data, passwords and access
  tokens from the files and linked content you share.
- Check that all attachments together are 25 MB or less. Keep your own copy
  of the source files and any sandbox data you need.

For corrections or questions about an entry you have sent, reply in the
same email thread and identify the entry title. If your email bounces or
your mail service rejects an attachment, contact support@assureswarm.com
(subject "Auditober submission help") without the attachment and describe
the problem.

### Open-source contribution (`#open-source`)

Every Auditober entry is a contribution to the audit community's shared
playbook. By submitting an entry, you grant AssureSwarm and anyone who
receives the entry a perpetual, worldwide, royalty-free and irrevocable
license to use, copy, modify, publish, distribute and build on it, in whole
or in part, for any purpose. AssureSwarm may release any entry to the
public under an open-source license of its choosing, without attribution
and without payment beyond any prize awarded.

Once you submit, the solution is the community's to use. Neither you nor
your team will hold exclusive rights to it, and you may not restrict how
others use, adapt or share it. Submit only work you have the right to
contribute. If your employer may have rights in what you build, confirm
with them before you submit.

### Judging, prizes and sharing (`#event-rules`)

The event page (https://assureswarm.com/auditober/) lists four category
winners. Each wins an AuditKeyboard and a QAIP readiness review from Cherry
Hill Advisory; the winners also share $1,000,000 in AssureSwarm
subscriptions. Winners are planned for November.

Entries will be shared anonymously with participants, under the
open-source contribution terms above. The full judging process, panel,
announcement date and prize terms have not yet been published. The date
sandbox access ends has not been announced either. Keep your own export
and contact the organizers if any of these details affect your entry.

## 7. Get help and give feedback (`#help`)

### Report an issue or suggest an improvement (`#feedback`)

1. In the agent, choose Feedback at the top of the chat.
2. Pick Report an issue or Suggest an improvement. The agent drafts a title
   and description from your conversation. Edit them freely.
3. For an issue, set the severity. A screenshot of your screen is attached
   automatically; remove it or replace it if you want. Then choose Submit
   issue.

Say what you were trying to do, what you expected, and what happened. If
your team's AI allowance has run out, you can still write and send feedback
by hand.

### Ask a question (`#questions`)

- Ask the Swarm agent. It knows the product and can look things up in your
  sandbox.
- Book your office hours (https://calendar.app.google/Lk1xH6hJJVfKARuD6)
  for product, build or submission questions.
- Email support@assureswarm.com (subject "Auditober question").

### Office hours (`#office-hours`)

Bring questions about your sandbox, your entry or the submission steps.
Book your office hours at https://calendar.app.google/Lk1xH6hJJVfKARuD6 and
choose a time on the calendar.

### Your team's AI allowance (`#limits`)

Each team shares a $50 AI allowance for the whole of Auditober, with a
daily limit on top. The top of the agent shows what your team has used
today, for example Team budget $0.00 / $25.00 today. The allowance covers
the Swarm agent's chats, feedback drafting and document reading, and it
does not reset each month. When it runs out, the agent tells you and stops
making AI calls. The app, the dashboards and any agent you connect yourself
keep working. Your own agent uses its provider's allowance or billing,
separately from the included Swarm allowance. Check the amount shown in the
chat for your team's current daily limit.

## Site links

Privacy Policy: https://assureswarm.com/privacy · Terms of Service:
https://assureswarm.com/terms · Contact: support@assureswarm.com
