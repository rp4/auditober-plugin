# Security tooling (EDR / SIEM / VM / DLP / secrets) — templates

Category: `security`.
Common products: CrowdStrike, SentinelOne, Microsoft Defender (EDR);
Splunk, Sentinel, Elastic, Sumo Logic (SIEM/log mgmt); Qualys, Tenable,
Rapid7 (vulnerability scanner); DLP tools; HashiCorp Vault, AWS Secrets
Manager, Doppler (secrets manager).

`{{system}}` = the security product (e.g. CrowdStrike). Maps to SOC 2
CC7 (system operations / monitoring), ISO 27001 A.8, and CIS controls.

## Controls

- **{{system}} endpoint detection & response (EDR) coverage** — {{system}}
  agents are deployed to all in-scope endpoints/servers; coverage gaps are
  monitored. `system: {{system}}` · `itgc_domain: operations`
- **{{system}} security monitoring & alerting (SIEM)** — logs are ingested
  into {{system}}, correlation rules alert on threats, and alerts are
  triaged. `system: {{system}}` · `itgc_domain: operations`
- **{{system}} vulnerability scanning & remediation** — {{system}} scans on
  a schedule; findings are risk-ranked and remediated within SLA.
  `system: {{system}}` · `itgc_domain: operations`
- **{{system}} data loss prevention (DLP)** — {{system}} policies detect
  and block exfiltration of sensitive data across channels. `system: {{system}}`
- **{{system}} secrets management** — application and infrastructure
  secrets are stored in {{system}}, access-controlled, and rotated.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} incident response integration** — {{system}} alerts feed the
  incident-response process with defined severity and escalation.
  `system: {{system}}` · `itgc_domain: operations`

## Risks

- **{{system}} coverage gap leaves endpoints unprotected** — unmonitored
  hosts allow undetected compromise. `system: {{system}}`
- **Unmonitored logs in {{system}} delay breach detection** — missing or
  untuned rules let attacks go unnoticed. `system: {{system}}`
- **Unremediated vulnerabilities found by {{system}} are exploited** —
  known CVEs persist past SLA. `system: {{system}}`
- **Secrets sprawl outside {{system}} are leaked** — hardcoded or
  unrotated credentials are exposed. `system: {{system}}`

## Policies

- **Security Monitoring & Incident Response Policy** — governs {{system}}
  EDR/SIEM coverage, alerting, and escalation.
- **Vulnerability Management Policy** — governs {{system}} scanning
  cadence and remediation SLAs.
- **Data Loss Prevention Policy** — governs {{system}} DLP rules and
  handling of blocked events.

## Generic fallback

For any security tool not named above, instantiate: a `{{system}}
coverage & monitoring` control (`operations`), a `{{system}} alerting &
incident escalation` control (`operations`), the "{{system}} coverage gap
leaves endpoints unprotected" and "Unmonitored {{system}} delays breach
detection" risks, and link them to the Security Monitoring & Incident
Response policy.
