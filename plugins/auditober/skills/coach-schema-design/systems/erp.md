# ERP & core financial systems — control/risk/policy templates

Category: `erp` (also consolidation/close tooling and material sub-ledgers).
Common products: SAP, Oracle EBS/Fusion, NetSuite, Workday Financials,
Microsoft Dynamics 365, Sage, QuickBooks.

`{{system}}` = the company's real ERP product name (e.g. NetSuite).
ITGC domains apply: `access` / `change` / `operations` / `interfaces`.
This is the SOX ITGC/ITAC engine — most controls here also satisfy
SOC 2 CC6 (logical access) and CC8 (change management).

## Controls

- **{{system}} user access provisioning & de-provisioning** — access is
  granted on approved request and revoked on termination/transfer.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} periodic access recertification** — application owners
  recertify user access and privileged roles at least quarterly.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} segregation-of-duties (SoD) conflict monitoring** —
  conflicting role combinations (e.g. create vendor + pay vendor) are
  monitored and mitigated. `system: {{system}}` · `itgc_domain: access`
- **{{system}} privileged / emergency (firefighter) access logging** —
  elevated access is time-boxed, approved, and activity is logged and
  reviewed. `system: {{system}}` · `itgc_domain: access`
- **{{system}} program-change management** — changes to configuration and
  custom code follow request → test → approve → migrate with segregation
  between developer and migrator. `system: {{system}}` · `itgc_domain: change`
- **{{system}} batch-job & interface monitoring** — scheduled jobs and
  inbound/outbound interfaces (sub-ledger, bank, consolidation) are
  monitored; failures are investigated and reprocessed.
  `system: {{system}}` · `itgc_domain: interfaces`
- **{{system}} backup, recovery & job scheduling** — backups run on
  schedule, restores are tested, and operational failures are resolved.
  `system: {{system}}` · `itgc_domain: operations`
- **{{system}} automated ITACs (3-way match, tolerance, approval limits)**
  — application-embedded automated controls over transaction processing
  are configured and change-controlled. `system: {{system}}` · `itgc_domain: change`

## Risks

- **Unauthorized or unreviewed changes to financial data in {{system}}** —
  configuration or master-data changes bypass approval, misstating the
  financials. `system: {{system}}`
- **SoD conflicts in {{system}} enable fraud** — a single user can both
  initiate and approve/conceal a transaction. `system: {{system}}`
- **Terminated or transferred user retains {{system}} access** — stale
  access enables unauthorized transactions. `system: {{system}}`
- **Undetected {{system}} interface/batch failure corrupts the ledger** —
  a failed feed leaves the general ledger incomplete or duplicated.
  `system: {{system}}`
- **Unapproved program change to {{system}} breaks an automated control** —
  a change silently disables a 3-way match or approval limit.
  `system: {{system}}`

## Policies

- **Logical Access Policy** — governs {{system}} provisioning,
  recertification, SoD, and privileged access.
- **Change Management Policy** — governs {{system}} configuration and
  program changes, including test and approval evidence.
- **IT Operations Policy** — governs {{system}} job scheduling, backup,
  recovery, and interface monitoring.

## Generic fallback

For any ERP/financial system not named above, instantiate: a `{{system}}
access provisioning & recertification` control (`access`), a `{{system}}
change management` control (`change`), a `{{system}} SoD monitoring`
control (`access`), the "Terminated user retains {{system}} access" and
"Unauthorized changes to financial data in {{system}}" risks, and link
them to the Logical Access and Change Management policies.
