# ARCHITECTURE.md

## Overview

`.github` is the org-wide community health repository for Flyto2. GitHub uses
these files as defaults for public repositories that do not define their own
issue templates, PR template, contributing guide, support policy, or security
policy.

## Owned Surfaces

- `profile/README.md`: public GitHub organization profile.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`, and
  `COMMUNITY.md`: default community and maintainer guidance.
- `ISSUE_TEMPLATE/` and `DISCUSSION_TEMPLATE/`: default intake paths for bug
  reports, features, good first issues, Q&A, ideas, and showcases.
- `.github/workflows/reusable-*.yml`: reusable security workflow templates.
- `docs/DOCUMENTATION_STANDARD.md`: organization documentation policy.
- `docs/documentation-contract.schema.json`: feature-to-document contract schema.
- `scripts/audit-documentation.py`: dependency-free repository documentation audit.
- `scripts/generate-source-reference.py`: deterministic source-level API index.

## Integration Boundaries

This repo should link to canonical Flyto2 surfaces instead of duplicating deep
product docs: `flyto2.com` for product positioning, `docs.flyto2.com` for
technical mechanics, `blog.flyto2.com` for educational content, and public
GitHub package repositories for source.

Repository documentation workflows check out this repository into
`.flyto-doc-standard/` and execute the shared audit against the caller checkout.
The caller retains its own manifest and product-specific build/reference gates.

## Frontend Surfaces

If this repo contains UI, every screen must follow the Flyto2 Frontend Quality Gate in `AGENTS.md`.

## Update Rule

Update this file when module boundaries, storage, APIs, deployment, or frontend structure changes.
