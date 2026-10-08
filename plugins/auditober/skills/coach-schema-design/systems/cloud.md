# Cloud & infrastructure — control/risk/policy templates

Category: `cloud`.
Common products: AWS, Azure, GCP, on-prem / colo.

`{{system}}` = the cloud/infra platform (e.g. AWS). Maps primarily to
SOC 2 CC6/CC7, ISO 27001 A.8, and CIS benchmarks. Where an ERP is hosted
here, the `operations` ITGC domain also applies.

## Controls

- **{{system}} account / subscription baseline hardening** — accounts are
  configured against a CIS/vendor benchmark; drift is detected.
  `system: {{system}}` · `itgc_domain: operations`
- **{{system}} IAM least-privilege & root/owner protection** — IAM
  policies grant least privilege; root/global-admin credentials are
  vaulted with MFA and used only by exception. `system: {{system}}` · `itgc_domain: access`
- **{{system}} network segmentation & security groups** — ingress/egress
  is restricted; public exposure of storage and databases is prevented.
  `system: {{system}}` · `itgc_domain: operations`
- **{{system}} encryption at rest & in transit** — data volumes, object
  storage, and databases use managed encryption; TLS is enforced.
  `system: {{system}}`
- **{{system}} logging & monitoring (CloudTrail / Activity Log / Audit
  Logs)** — control-plane logs are enabled, centralized, and alerted on.
  `system: {{system}}` · `itgc_domain: operations`
- **{{system}} infrastructure change management (IaC review)** —
  infrastructure changes go through peer-reviewed IaC pipelines, not
  console click-ops. `system: {{system}}` · `itgc_domain: change`
- **{{system}} backup & disaster-recovery** — critical data is backed up
  cross-region/zone and recovery is tested against RTO/RPO.
  `system: {{system}}` · `itgc_domain: operations`

## Risks

- **Misconfigured {{system}} resource exposes data publicly** — an open
  storage bucket or security group leaks sensitive data. `system: {{system}}`
- **Over-privileged {{system}} IAM principal is compromised** — a leaked
  key or role grants attacker broad access. `system: {{system}}`
- **Unlogged {{system}} activity prevents breach detection** — disabled
  or gap-filled audit logs hide malicious action. `system: {{system}}`
- **{{system}} outage without tested recovery causes prolonged downtime** —
  no cross-region failover or untested restores. `system: {{system}}`

## Policies

- **Cloud Security Policy** — governs {{system}} hardening, IAM,
  segmentation, and encryption.
- **Logging & Monitoring Policy** — governs {{system}} audit logging and
  alerting.
- **Business Continuity & Disaster Recovery Policy** — governs {{system}}
  backup and recovery objectives.

## Generic fallback

For any cloud/infra platform not named above, instantiate: a `{{system}}
IAM least-privilege` control (`access`), a `{{system}} configuration
hardening & logging` control (`operations`), a `{{system}} encryption`
control, the "Misconfigured {{system}} exposes data publicly" and
"Over-privileged {{system}} principal compromised" risks, and link them
to the Cloud Security and Logging & Monitoring policies.
