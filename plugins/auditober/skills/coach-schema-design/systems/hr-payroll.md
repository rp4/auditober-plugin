# HR & payroll (HRIS / payroll) — control/risk/policy templates

Categories: `hris`, `payroll`.
Common products: Workday HCM, BambooHR, SAP SuccessFactors, UKG (HRIS);
ADP, Paychex, Gusto, Rippling (payroll).

`{{system}}` = the HRIS or payroll product (e.g. Workday HCM / ADP). The
HRIS is the authoritative source for joiner-mover-leaver; payroll is a
SOX-relevant financial sub-process. Maps to SOX ITGC/ITAC, SOC 2 CC6.

## Controls

- **{{system}} HR data as authoritative JML source** — hires, transfers,
  and terminations in {{system}} drive downstream provisioning/
  deprovisioning timely and completely. `system: {{system}}` · `itgc_domain: access`
- **{{system}} access & role administration** — access to sensitive HR /
  payroll data is least-privilege and reviewed periodically.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} payroll change authorization** — pay-rate, bank-detail, and
  master-data changes require independent approval before processing.
  `system: {{system}}` · `itgc_domain: change`
- **{{system}} payroll run review & reconciliation** — each payroll run is
  reviewed for completeness/accuracy and reconciled to the GL.
  `system: {{system}}` · `itgc_domain: interfaces`
- **{{system}} segregation of duties (payroll)** — the person who edits
  employee/pay master data cannot also approve and disburse payroll.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} sensitive HR data protection** — PII/compensation data is
  access-restricted, encrypted, and audit-logged. `system: {{system}}`

## Risks

- **Terminated employee not deprovisioned because {{system}} event was
  missed** — the JML source fails to trigger access removal. `system: {{system}}`
- **Unauthorized payroll or bank-detail change in {{system}} causes
  fraudulent payment** — no independent approval of master-data change.
  `system: {{system}}`
- **SoD conflict in {{system}} lets one person set up and pay an
  employee** — ghost-employee or diversion fraud. `system: {{system}}`
- **Payroll-to-GL reconciliation gap in {{system}} misstates expense** —
  interface errors post incorrect payroll expense. `system: {{system}}`

## Policies

- **Logical Access Policy** — governs {{system}} access administration and
  JML-driven provisioning.
- **Payroll Policy** — governs {{system}} change authorization, run
  review, and SoD.
- **Data Classification & Handling Policy** — governs {{system}}
  protection of sensitive HR/compensation data.

## Generic fallback

For any HRIS or payroll system not named above, instantiate: a `{{system}}
JML source-of-truth` control (`access`), a `{{system}} payroll change
authorization` control (`change`), a `{{system}} SoD` control (`access`),
the "Terminated employee not deprovisioned from {{system}}" and
"Unauthorized payroll change in {{system}}" risks, and link them to the
Logical Access and Payroll policies.
