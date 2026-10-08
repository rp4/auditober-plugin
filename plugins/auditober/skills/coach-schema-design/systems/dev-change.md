# Dev & change (SCM / CI-CD / ITSM) — control/risk/policy templates

Categories: `scm`, `cicd`, `itsm`.
Common products: GitHub, GitLab (SCM); GitHub Actions, GitLab CI,
Jenkins (CI/CD); Jira, ServiceNow (ITSM/ticketing).

`{{system}}` = the SCM / CI-CD / ITSM product (e.g. GitHub). Maps to
SOC 2 CC8 (change management), ISO 27001 A.8, and SOX ITGC `change`.

## Controls

- **{{system}} branch protection & mandatory code review** — changes to
  protected branches require peer review and passing checks before merge.
  `system: {{system}}` · `itgc_domain: change`
- **{{system}} pipeline access & deployment approval** — production
  deployment via {{system}} requires approval and is segregated from the
  author. `system: {{system}}` · `itgc_domain: change`
- **{{system}} repository / project access management** — repo and
  pipeline access is granted by role and reviewed periodically.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} change ticketing & traceability** — production changes are
  tracked to an approved {{system}} ticket linking request, test, and
  deployment evidence. `system: {{system}}` · `itgc_domain: change`
- **{{system}} secrets & CI credential protection** — pipeline secrets are
  stored in a managed store, scoped, and rotated; not hardcoded.
  `system: {{system}}` · `itgc_domain: change`
- **{{system}} audit logging of changes & approvals** — merge, deploy, and
  ticket-approval events are logged and retained. `system: {{system}}` · `itgc_domain: operations`

## Risks

- **Unreviewed change merged and deployed via {{system}}** — code reaches
  production without peer review or approval. `system: {{system}}`
- **Developer self-approves and deploys own change in {{system}}** — no
  segregation between author and deployer. `system: {{system}}`
- **Leaked {{system}} pipeline secret grants environment access** —
  hardcoded or over-scoped CI credentials are exfiltrated. `system: {{system}}`
- **Untracked emergency change in {{system}} lacks approval trail** —
  hotfix bypasses the ticketing/change record. `system: {{system}}`

## Policies

- **Change Management Policy** — governs {{system}} review, approval,
  ticketing, and deployment segregation.
- **Secure Development / SDLC Policy** — governs {{system}} branch
  protection, testing, and secrets handling.
- **Logical Access Policy** — governs {{system}} repository and pipeline
  access reviews.

## Generic fallback

For any dev/change tool not named above, instantiate: a `{{system}} change
review & approval` control (`change`), a `{{system}} deployment
segregation` control (`change`), a `{{system}} access review` control
(`access`), the "Unreviewed change deployed via {{system}}" and
"Developer self-approves own change in {{system}}" risks, and link them to
the Change Management and SDLC policies.
