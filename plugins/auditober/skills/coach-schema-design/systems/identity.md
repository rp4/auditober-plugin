# Identity, access & PAM — control/risk/policy templates

Categories: `identity`, `pam`.
Common products: Okta, Microsoft Entra ID, Ping, Google Workspace,
Active Directory; PAM: CyberArk, BeyondTrust, HashiCorp Vault.

`{{system}}` = the IdP or PAM product (e.g. Okta). Maps to SOC 2 CC6,
ISO 27001 A.5/A.8, and SOX ITGC `access` where it fronts financial apps.

## Controls

- **{{system}} single sign-on & MFA enforcement** — application access is
  brokered through {{system}} with MFA required for all users.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} joiner-mover-leaver provisioning** — accounts are created,
  role-changed, and disabled in {{system}} on authoritative HR events.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} periodic access & group-membership review** — group and
  application assignments in {{system}} are recertified quarterly.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} password & authentication policy** — password length,
  lockout, and session policies are enforced centrally in {{system}}.
  `system: {{system}}` · `itgc_domain: access`
- **{{system}} privileged access management (PAM)** — administrative and
  service credentials are vaulted, checked out with approval, rotated,
  and session-recorded. `system: {{system}}` · `itgc_domain: access`
- **{{system}} authentication & admin-event logging** — sign-in and
  admin-configuration events are logged, centralized, and alerted on
  (impossible travel, admin changes). `system: {{system}}` · `itgc_domain: operations`

## Risks

- **Orphaned or stale {{system}} accounts retain access** — leavers or
  role-changers keep entitlements. `system: {{system}}`
- **Missing MFA on {{system}} enables account takeover** — credential
  stuffing or phishing succeeds without a second factor. `system: {{system}}`
- **Unmanaged privileged credentials in {{system}} are misused** —
  shared/standing admin accounts enable untraceable action. `system: {{system}}`
- **Excessive {{system}} group membership grants unintended access** —
  broad groups over-provision downstream apps. `system: {{system}}`

## Policies

- **Logical Access Policy** — governs {{system}} SSO, MFA, JML, and
  access review.
- **Privileged Access Management Policy** — governs {{system}} vaulting,
  checkout approval, and credential rotation.
- **Password / Authentication Policy** — governs {{system}} password and
  session requirements.

## Generic fallback

For any identity or PAM product not named above, instantiate: a
`{{system}} SSO & MFA enforcement` control (`access`), a `{{system}}
joiner-mover-leaver provisioning` control (`access`), a `{{system}}
access review` control (`access`), the "Stale {{system}} accounts retain
access" and "Missing MFA on {{system}} enables takeover" risks, and link
them to the Logical Access and Password/Authentication policies.
