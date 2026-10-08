---
title: upload_document
description: Upload a file to a workflow step or an item document field, using base64 or an HTTPS source URL.
---

`upload_document` attaches a file to a workflow step or replaces an item document field. It requires the `write:documents` scope.

The upload applies immediately and is attributed to the connected user. It requires access to the target. A step upload can add a document or replace an existing document through `replaceDocumentId`; an item-field upload replaces that field's current document. Confirm the target and any replacement before calling.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `target` | object | Yes | `{ "type": "step", "stepId": "..." }` or `{ "type": "item_field", "itemId": "...", "fieldKey": "..." }`. |
| `fileName` | string | Yes | Display file name, shown to anyone who later views the step's documents. |
| `fileData` | string | Sometimes | Base64 content; use exactly one of this or `sourceUrl`. Decoded size is limited to 10 MB. |
| `sourceUrl` | string | Sometimes | HTTPS source fetched by the server; use instead of `fileData`. |
| `replaceDocumentId` | string | No | Replace an existing step document; valid only for a step target. |
| `mimeType` | string | No | MIME type, such as `text/plain` or `application/pdf`. |

## Example

```json
{
  "name": "upload_document",
  "arguments": {
    "target": { "type": "step", "stepId": "step_123" },
    "fileName": "evidence-summary.txt",
    "fileData": "RXhhbXBsZSBldmlkZW5jZSBzdW1tYXJ5Lg==",
    "mimeType": "text/plain"
  }
}
```

## After the Upload

For a step target, the file appears among the step’s documents, attributed to the connected user. For an item-field target, it replaces the selected document field. There is no pending suggestion.

It then passes a validation stage before it's usable: `pending` → `validated` or `rejected`. See [Documents](https://docs.assureswarm.com/concepts/documents/) for what validation covers.

## Agent Notes

- Upload only files the user actually provided, or explicitly asked you to create.
- Double-check `target`, `replaceDocumentId`, and `fileName` before calling: because this write applies immediately, there's no review step to catch a mistake.
- To link to an external document instead of uploading a file, use [suggest_change](https://docs.assureswarm.com/mcp/suggest_change/) with `itemType: "stepdocumentlink"`: that goes through review, and accepts only `http` or `https` URLs.
- Report whether the upload added or replaced a document. If the user expects a review before replacement, obtain it before calling this direct operation.
