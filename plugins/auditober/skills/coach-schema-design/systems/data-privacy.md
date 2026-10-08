# Data & privacy (databases / warehouse / regulated data) — templates

Categories: `db`, `warehouse`, `regulatedData`.
Common products: PostgreSQL, MySQL, SQL Server, Oracle DB (databases);
Snowflake, BigQuery, Redshift, Databricks (warehouse).
Regulated data types: PII, PHI, PCI-cardholder, CUI.

`{{system}}` = the database/warehouse product (e.g. Snowflake), or the
regulated data type where a control is data-specific. Maps to SOC 2
CC6/C1 (confidentiality), ISO 27001 A.8, GDPR, HIPAA, PCI-DSS.

## Controls

- **{{system}} access control & least privilege** — database/warehouse
  roles grant least privilege; access is granted on request and reviewed.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} encryption & key management** — data at rest and in transit
  is encrypted; keys are managed and rotated. `system: {{system}}`
- **{{system}} data classification & masking** — sensitive columns are
  classified; masking / tokenization / row-level policies protect PII,
  PHI, and cardholder data. `system: {{system}}`
- **{{system}} query & access audit logging** — access to sensitive data
  is logged and monitored for anomalous queries/exports. `system: {{system}}` · `itgc_domain: operations`
- **{{system}} data retention & secure disposal** — data is retained per
  policy and securely deleted at end of life. `system: {{system}}`
- **{{system}} backup, integrity & recovery** — backups are taken,
  integrity-checked, and restores are tested. `system: {{system}}` · `itgc_domain: operations`
- **Data subject rights / consent handling** — access, deletion, and
  consent requests for regulated data are fulfilled within statutory
  timelines. (privacy)

## Risks

- **Excessive {{system}} access exposes regulated data** — broad roles let
  users read PII/PHI/cardholder data beyond need-to-know. `system: {{system}}`
- **Unencrypted or unmasked sensitive data in {{system}} is exfiltrated** —
  a breach or bulk export leaks regulated data. `system: {{system}}`
- **Over-retention of regulated data in {{system}} breaches privacy law** —
  data kept past its lawful basis. `system: {{system}}`
- **Undetected anomalous export from {{system}}** — large or off-hours
  extracts go unmonitored. `system: {{system}}`

## Policies

- **Data Classification & Handling Policy** — governs {{system}}
  classification, masking, and encryption of regulated data.
- **Data Retention & Disposal Policy** — governs {{system}} retention
  schedules and secure deletion.
- **Privacy Policy / Data Protection Policy** — governs consent, data
  subject rights, and lawful processing of PII/PHI.

## Generic fallback

For any database, warehouse, or regulated-data store not named above,
instantiate: a `{{system}} least-privilege access` control (`access`), a
`{{system}} encryption & classification` control, a `{{system}} access
audit logging` control (`operations`), the "Excessive {{system}} access
exposes regulated data" and "Unencrypted data in {{system}} exfiltrated"
risks, and link them to the Data Classification & Handling and Data
Retention policies.
