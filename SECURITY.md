# Security Policy

This file is org-wide. Unless a specific repo overrides it with its own
`SECURITY.md`, these rules apply to every `flytohub/*` project.

## Reporting a vulnerability

**Please do not open a public issue for security bugs.**

- 📧 **security@flyto2.com** — preferred
- 🔒 If the repository's `Security` tab offers **Report a vulnerability**, use
  that private form. Otherwise, use the email address above.

Include, when you can:

1. The repo + version (commit SHA or release tag) you reproduced on
2. A minimal reproducer (or a sanitised PoC)
3. What you believe the impact is
4. Whether you've contacted anyone else about this

We target an acknowledgement within **3 business days** and an initial triage
update within **10 business days**. These are best-effort response targets, not
an SLA. Remediation and disclosure timing depends on severity, reproducibility,
affected maintainers, and coordinated-disclosure constraints.

## Scope

In scope:

- Source in actively maintained public `flytohub/*` repositories
- Flyto2-operated public services under `flyto2.com`
- Release artifacts published by the official `flytohub` organization

Out of scope (do not probe):

- Third-party SaaS we integrate with (Firebase, Cloud Run, Stripe, etc.)
- Social-engineering attacks against team members or customers
- Physical attacks against our offices
- DoS / volumetric attacks
- Findings that only impact unsupported browsers / OS versions

## Responsible disclosure

We don't currently run a paid bounty program. When a public fix has release
notes, we may credit the reporter with their consent. Report quality and impact
inform triage priority, but do not create a payment or response-time promise.

## Known not-secrets

A few things can look like leaked credentials but are expected-public:

- **Firebase Web API keys** (`AIza...`) and `google-services.json` /
  `GoogleService-Info.plist` on mobile: these identify the project but
  enforcement lives in Firebase Security Rules + domain allowlist.
  [Official Firebase guidance.](https://firebase.google.com/docs/projects/api-keys)
- OAuth **client IDs** (not secrets) in frontend `.env.example`
- Public GCP **project IDs** — infrastructure identifiers, not secrets

If you're unsure, report it — we'd rather review a false positive than
miss a real one.
