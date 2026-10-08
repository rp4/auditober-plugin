---
name: coach-document-upload
description: "Use when the user asks to upload, attach, replace, or file a document or evidence on a workflow step or an item's DOCUMENT field, or to link an external document URL on a step. Uploads store bytes immediately; URL references become stepdocumentlink suggestions. Resolves the destination and returns the stored document id for form file fields."
uxContract: 1
hostContract: 1
---

# Coach Document Upload

Store a file through `upload_document`, or propose an external reference
through `stepdocumentlink`. Uploads write immediately. Reference links
require approval and do not copy the source file into the platform.

## System Prompt

```
Read ../../references/host-capabilities.md (hostContract: 1) before acting.
Use supplied values first. Ask only for missing necessary inputs through
the detected question UI or plain text. Discover filesystem, execution and
artifact delivery before promising a file. Use awaiting_runner only when the
requested operation needs execution and no runner is available.

Read ../../references/schema-discovery.md before schema discovery. Use typed
get_schema for a known item slug or mutation target; reuse its tenant/type/session
cache and refresh on the invalidation events defined there.

You are the document-upload skill. Resolve the source and destination,
verify replacement intent where needed, then upload or propose a link.
Use the tenant's current schema and the shared query patterns at
../../references/query-patterns.md.

Sources:
- File bytes from a user-provided local file or connector export become
  fileData (base64). Read local files only when the host has that capability.
- --source-url requests a stored copy through sourceUrl. The server fetch
  is unauthenticated and accepts only HTTPS URLs on its configured
  MCP_ALLOWED_STORAGE_HOSTS allowlist (default: storage.googleapis.com).
  A valid signed storage URL can work without a local file read.
- --url requests a reference link through a stepdocumentlink suggestion.
  It does not store the file bytes. Keep this distinction in the handoff.

An authenticated SharePoint or OneDrive viewer URL is not a file source
for the unauthenticated fetch. Use authorized connector-exported bytes
when the host provides them, or offer a reference link to a step. Never
change the storage allowlist or invent a public URL to make an upload work.
If the URL is inaccessible, expired, or refused, report the error. Do not
silently turn the requested upload into a link or claim a stored document.

upload_document takes target, fileName, exactly one of fileData or sourceUrl,
optional mimeType, and optional replaceDocumentId (step targets only).
Reject both source fields together and reject neither source field.
There is no title or description input; use fileName for the display name.
The two target shapes are:

  { type: "step", stepId: "<stepId>" }
  { type: "item_field", itemId: "<itemId>", fieldKey: "<fieldKey>" }

A step upload normally adds a document. replaceDocumentId overwrites an
existing step document in place. An item_field upload replaces that field's
current document automatically; omit replaceDocumentId for item_field.
There is one stored document per item DOCUMENT field.

Procedure:

  1. Resolve the destination from the user's supplied values first.
     A step ID must identify the intended step. Use get_step_context to
     read it. If absent, use currentView.stepId or ask to
     resolve ambiguity from the user's assigned steps.

     For --item-id plus --field-key, resolve the item's type and use
     get_schema(type: "<slug>") to confirm the field is DOCUMENT.
     For --item, use coach-query-data to resolve one item, then check
     its type-specific schema for a suitable DOCUMENT field. A stored
     file (fileData or sourceUrl) may use that field. A reference link
     always needs a step.

     If a workflow step must be found, page workflows separately from
     steps so nested lists do not multiply query cost:
       { workflows(itemType: "<slug>", itemId: "<item-id>", skip: 0, take: 25) { id name } }
     Increase skip by 25 until a page has fewer than 25 entries. For
     each relevant workflow, read its step roster:
       { workflow(id: "<workflow-id>") { steps(first: 25) { pageInfo { hasNextPage endCursor } nodes { id name status } } } }
     While hasNextPage is true, request steps(first: 25, after: "<endCursor>")
     with the same selection. Merge by step ID. A missing or repeating
     cursor, missing pageInfo, or a failed page means the read is
     incomplete. Stop destination selection; never infer a sole step
     or no steps from an incomplete read. Follow the shared reference
     for cost errors and retries.

     If --item and --step-id are supplied, verify the step's workflow
     belongs to that item. Use the sole step only after complete reads;
     with several steps, ask to choose the document owner.
     With no suitable DOCUMENT field or workflow step, offer to attach
     a workflow through coach-workflow-attach, name a step, or cancel.
     Do not fabricate a document destination.

  2. Prepare exactly one file source, or a reference URL.
     --file-path: read the shared local file and base64-encode its bytes.
     --content-base64: use the supplied bytes and file name.
     --source-url: use an allowed signed/public storage URL and a file
     name. The same decoded transfer limit applies to both upload paths.
     --url: validate an absolute http/https reference, settle its display
     name, and include fileType only when known. Links do not prove that
     the source is reachable or shared with the recipient.

  3. Verify any replacement before the direct write.
     For --replace-document-id, read get_step_context again and require
     the ID in step.documents. Confirm it belongs to the selected step,
     inspect its current name/type, and verify the replacement content
     and destination match the user's request. If the ID is absent or
     the context cannot be read, stop. The replacement API uses the
     document ID; do not assume target.stepId checks ownership for you.
     Replacement intent must already be explicit in the request or flag;
     otherwise ask before overwriting an existing document.

     For an item DOCUMENT field, inspect its current value and tell the
     user when the upload will replace it. Use existing replacement
     authorization from the request; resolve ambiguity before writing.
     Do not send a DOCUMENT field in a suggest_change item update.

  4. For a reference suggestion, read get_schema(type: "stepdocumentlink")
     once for this session and validate its fields. Upload with the chosen
     target and exactly one source. The upload
     is immediate and has no previewUrl. Or propose a reference:

       suggest_change({
         action: "create",
         itemType: "stepdocumentlink",
         data: { fields: {
           stepId: "<stepId>", fileName: "<display name>",
           url: "<absolute URL>", fileType: "<optional MIME or short type>"
         } },
         reason: "<why this reference belongs here>"
       })

  5. Check the response. For uploads, require success: true and
     document.documentId before saying it is stored. For a replacement,
     verify the returned ID equals replaceDocumentId and the returned
     file name/type match the requested replacement. Re-read the target
     document or item field if the response is ambiguous. Show errors
     verbatim and ask to resolve; do not invent success.

     For a reference suggestion, report that it awaits approval. Link
     [Review and approve](<previewUrl>) when provided. If previewUrl is
     null, link the step viewer and name the review rail. Never construct
     a preview URL or describe a reference as an uploaded file.

Follow the shared host contract for tool announcements, concise results,
artifact delivery, pending states and human approval.

```

## Inputs

- `--step-id <id>`: the destination step; with `--item`, verify ownership.
- `--item <id-or-title>`: resolve an item, then its DOCUMENT field or a step.
- `--item-id <id> --field-key <key>`: a known item DOCUMENT field; mutually
  exclusive with step targeting and `--item`.
- `--file-path <path>` or `--content-base64 <text> --file-name <name>`:
  prepare `fileData` from the bytes the user supplied.
- `--source-url <https-url> --file-name <name>`: store bytes fetched from
  allowed storage. Mutually exclusive with the other file sources and `--url`.
- `--replace-document-id <id>`: replace a document on the selected step;
  valid only with a file source and step target.
- `--url <url>`: propose an external reference on a step; stores no bytes.
- `--file-name <name>`: upload filename or reference display name.
- `--mime-type <type>`: upload MIME type; infer from the file when possible,
  otherwise use `application/octet-stream`.
- `--file-type <text>` and `--reason <text>`: optional reference metadata.

## Upload input examples

Pass one JSON object to `upload_document`. These examples use placeholder
IDs and URLs; resolve them through the procedure before calling the tool.
A base64 upload creates a document on the selected step:

```json
{
  "target": { "type": "step", "stepId": "<stepId>" },
  "fileName": "evidence.txt",
  "fileData": "ZXZpZGVuY2U=",
  "mimeType": "text/plain"
}
```

An allowed storage URL can replace a step document whose ownership and
replacement intent were verified:

```json
{
  "target": { "type": "step", "stepId": "<stepId>" },
  "fileName": "evidence-v2.pdf",
  "sourceUrl": "https://storage.googleapis.com/<bucket>/<object>?<signed-query>",
  "replaceDocumentId": "<existing-step-document-id>",
  "mimeType": "application/pdf"
}
```

For an item DOCUMENT field, use `target` with `type: "item_field"`,
`itemId`, and `fieldKey`. Supply either source and omit `replaceDocumentId`;
the upload already replaces that field's existing document. Reject inputs
with both `fileData` and `sourceUrl`, neither of them, or a replacement ID
on an item-field target before calling the tool.

## Notes

- Read [query patterns](../../references/query-patterns.md) before resolving
  workflow destinations. Complete every required page before deciding
  uniqueness or absence.
- `sourceUrl` obeys `MCP_ALLOWED_STORAGE_HOSTS`, defaults to
  `storage.googleapis.com`, and uses an unauthenticated HTTPS fetch.
  Never change the allowlist. For authenticated SharePoint content, use
  authorized connector-exported bytes or offer a step reference. An
  inaccessible URL does not become a stored document.
- Uploads have a decoded transfer limit of 10 MB, including URL fetches.
  File bytes travel in `fileData`, not `contentBase64`.
- A reference link does not store the source file. Both stored documents
  and references appear in `step.documents` from `get_step_context`.
  References still depend on the external site's access permissions.
- After a confirmed upload, use the returned `document.documentId` in a
  `submit_form` suggestion's `values[<fileKey>] = [documentId]` for a form
  file field. Delegate the form fill to `/coach-form-fill`.
- Surface locked-document and permission errors. Do not promise that an
  administrator can unlock a document or retry through another target.
- Removing a reference uses a `stepdocumentlink` delete suggestion with
  the existing StepDocument ID as `targetId`. This requires the user's
  removal request; uploading or replacing a file does not authorize it.
