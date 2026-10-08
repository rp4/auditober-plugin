# Business apps & third parties (CRM / payment / vendors) — templates

Categories: `crm`, `thirdParties`.
Common products: Salesforce, HubSpot, Dynamics CRM (CRM);
Stripe, Adyen, Braintree, Shopify (e-commerce/payment); plus key
sub-service organizations and critical vendors.

`{{system}}` = the business app or vendor (e.g. Salesforce / Stripe). CRM
and revenue apps are often SOX-relevant (revenue completeness); vendors
drive third-party risk / SOC 2 CC9 and vendor-management controls.

## Controls

- **{{system}} access management & role review** — access to {{system}} is
  role-based, provisioned on request, and recertified periodically.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} configuration & change management** — changes to {{system}}
  objects, workflows, and integrations follow a controlled change process.
  `system: {{system}}` · `itgc_domain: change`
- **{{system}} revenue / transaction data integrity** — data flowing from
  {{system}} into billing/GL is complete, accurate, and reconciled (for
  CRM/payment systems). `system: {{system}}` · `itgc_domain: interfaces`
- **{{system}} payment / PCI safeguards** — cardholder data in {{system}}
  is tokenized/out-of-scope; PCI-DSS obligations are met (payment
  systems). `system: {{system}}`
- **{{system}} vendor risk assessment & monitoring** — {{system}} (as a
  critical vendor / sub-service org) is risk-assessed, has reviewed
  SOC reports, and DR/security is monitored. `system: {{system}}`
- **{{system}} data-sharing & API access control** — integrations and API
  tokens to {{system}} are scoped, inventoried, and rotated. `system: {{system}}` · `itgc_domain: access`

## Risks

- **Over-broad {{system}} access exposes customer or revenue data** —
  users see or export data beyond need. `system: {{system}}`
- **Uncontrolled {{system}} configuration change breaks revenue flow** — a
  workflow/integration change misstates or drops transactions. `system: {{system}}`
- **{{system}} vendor breach or outage impacts the company** — a critical
  sub-service org fails without a monitored SOC report or DR plan.
  `system: {{system}}`
- **Unmanaged {{system}} API token is leaked** — a broad integration
  credential exposes data. `system: {{system}}`

## Policies

- **Third-Party / Vendor Management Policy** — governs {{system}} risk
  assessment, SOC-report review, and monitoring.
- **Logical Access Policy** — governs {{system}} access review and API
  token management.
- **Change Management Policy** — governs {{system}} configuration and
  integration changes.

## Generic fallback

For any business app or vendor not named above, instantiate: a `{{system}}
access review` control (`access`), a `{{system}} change management`
control (`change`), a `{{system}} vendor risk assessment` control, the
"Over-broad {{system}} access exposes data" and "{{system}} vendor breach
impacts the company" risks, and link them to the Vendor Management and
Logical Access policies.
