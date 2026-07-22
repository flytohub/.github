# STATE.md

Last reviewed: 2026-07-22

## Current State

`.github` is part of the 27-repository Flyto2 workspace memory standardization.
It now carries the org-wide community map, good-first intake, and showcase
intake for reusable workflows, MCP examples, browser automations, and Warroom
CE labs.

Organization documentation governance now has a written standard, JSON schema,
dependency-free audit, and reusable GitHub Actions workflow. Per-repository
manifest rollout is tracked by the workspace documentation audit.
The organization repository also carries a generated exact-line Python
reference and a local lint/test/build/verify CI loop.

## Known Risks

- Keep public copy aligned with Flyto2 naming and current URLs.
- Keep frontend changes aligned with accessibility, responsive design, visual hierarchy, navigation, and content clarity standards.

## Verification

- 2026-07-18: Markdown/content-only update; verified by source review,
  brand/email scan, and git diff checks in the community expansion pass.
- 2026-07-22: documentation contract audited with
  `python3 scripts/audit-documentation.py . --json`.
