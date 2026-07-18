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

## Integration Boundaries

This repo should link to canonical Flyto2 surfaces instead of duplicating deep
product docs: `flyto2.com` for product positioning, `docs.flyto2.com` for
technical mechanics, `blog.flyto2.com` for educational content, and public
GitHub package repositories for source.

## Frontend Surfaces

If this repo contains UI, every screen must follow the Flyto2 Frontend Quality Gate in `AGENTS.md`.

## Update Rule

Update this file when module boundaries, storage, APIs, deployment, or frontend structure changes.
