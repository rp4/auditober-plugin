---
title: submit_card_action
description: "Relay a human decision from an approval or task card."
---

Relay a human decision from an approval or task card. Requires `read:context`.

## Input

| Field | Type | Required | Notes |
|---|---|---|---|
| `token` | string | Yes | Single-use possession token from human-facing card HTML; 16–256 characters. |
| `action` | string | Yes | `approve`, `reject`, or `cancel`, as permitted by that card. |

## Behavior

A supported client renders the card for the human. Its button sends the card’s
single-use token and decision; core binds that token to a person, subject, and
permitted actions. The token is never part of model-facing tool results.

The tool’s `read:context` scope does not authorize approval. An agent must not
extract, guess, or request a card token, and must not approve its own proposal.
Use the human review link when cards are unavailable. `approve:suggestions`
is a separate human authority scope, excluded from default grants and never
required by this MCP tool.

Successful calls report the user’s decision, subject, and any creation
warnings. Invalid, expired, consumed, mismatched, or unauthorized tokens all
return `invalid or expired card token`. No model-executable approval example
is provided because the credential belongs to the human card.
