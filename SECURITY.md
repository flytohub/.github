# Security Policy

This file is org-wide. Unless a specific repo overrides it with its own
`SECURITY.md`, these rules apply to every `flytohub/*` project.

## Reporting a vulnerability

**Please do not open a public issue for security bugs.**

- 📧 **security@flyto2.com** — preferred
- 🔒 GitHub private vulnerability reporting is enabled on every repo:
  navigate to `Security → Report a vulnerability` on the repo page

Include, when you can:

1. The repo + version (commit SHA or release tag) you reproduced on
2. A minimal reproducer (or a sanitised PoC)
3. What you believe the impact is
4. Whether you've contacted anyone else about this

We'll acknowledge within **24 hours** and give you a triage verdict
within **72 hours**. We aim to ship a fix and disclose within 90 days.

## Scope

In scope:

- Any source under `flytohub/*`
- Our hosted services: `flyto2.com`, `cloud.flyto2.com`, `cortex.flyto2.com`,
  `docs.flyto2.com`
- Our desktop builds published on `flyto2.com/app.html`

Out of scope (do not probe):

- Third-party SaaS we integrate with (Firebase, Cloud Run, Stripe, etc.)
- Social-engineering attacks against team members or customers
- Physical attacks against our offices
- DoS / volumetric attacks
- Findings that only impact unsupported browsers / OS versions

## Responsible disclosure

We don't currently run a paid bounty program, but we credit every
reporter who follows this policy in the release notes of the fix
(opt-out available). Repeat reporters of high-quality findings get
priority triage.

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
