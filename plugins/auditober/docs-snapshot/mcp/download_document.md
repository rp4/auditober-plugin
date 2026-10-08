---
title: download_document
description: Retrieve a document the connected user can access, with byte-size caps.
---

`download_document` retrieves a document by ID, subject to byte-size caps. It requires the `read:documents` scope.

Access follows the connected user's own permissions on the step, workflow, or item the document belongs to: a token cannot read a document the connected user couldn't otherwise open in the app.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `documentId` | string | Yes | The document ID to download. |
| `maxBytes` | integer | No | Maximum bytes to return. The hard ceiling is 10 MB, regardless of what you request. When you omit `maxBytes`, the effective default cap is 5 MB. |

## Example

```json
{
  "name": "download_document",
  "arguments": {
    "documentId": "doc_123",
    "maxBytes": 1048576
  }
}
```

## Finding Document IDs

Get a step's document IDs from [get_step_context](https://docs.assureswarm.com/mcp/get_step_context/): its response lists the documents attached to that step.

You can also look them up with document-related fields through [query_data](https://docs.assureswarm.com/mcp/query_data/) when you need to search or filter across more than one step.

## Agent Notes

- Respect document sensitivity: summarize only what the current task needs.
- If a document is larger than the cap, ask the user how to proceed instead of guessing at how to chunk it.
- Set `maxBytes` explicitly when you only need to preview part of a large file: it's cheaper than downloading the full default and discarding most of it.
