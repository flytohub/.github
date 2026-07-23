# DECISIONS.md

## 2026-07-23 - Separate Discovery From License Classification

Decision: keep one 28-repository discovery manifest, but apply acquisition SEO
only to the 16 public repositories and describe a project as open source only
when its own OSI-approved license permits that wording.

Rationale: GitHub visibility, search demand, and software licensing answer
different questions. Treating all public source as open source creates legal
and trust risk; treating private repositories as SEO targets creates noise.

Consequences:

- Ubersuggest evidence is dated and mapped to every public repository.
- PolyForm projects use source-available language.
- Private and internal repositories remain inventoried with SEO disabled.
- A scheduled audit detects GitHub About, topics, count, and license drift.

## 2026-07-22 - Adopt Machine-Readable Documentation Contracts

Decision: every Flyto2 repository maps source areas and feature surfaces to
durable docs and verification evidence through
`docs/documentation-manifest.json`.

Rationale: a shared contract can detect undocumented features and stale claims
without copying audit logic into 28 repositories.

Consequences:

- This repository owns the schema, audit, and reusable workflow.
- Product repositories own their manifests and prose.
- Language-native API references remain authoritative for public symbols.

## 2026-07-16 - Adopt Flyto2 Workspace Memory Standard

Decision: `.github` follows the Flyto2 project memory scaffold and frontend quality gate.

Rationale: All 28 Flyto2 repositories need consistent handoff context, durable decisions, and UI quality constraints.

Consequences:

- Root memory files must stay current.
- UI changes must avoid the eight forbidden frontend failures in `AGENTS.md`.
- Handoffs must be registered in `handoffs/_registry.md`.

## 2026-07-18 - Make Community Intake Org-Wide

Decision: `.github` owns the default Flyto2 community map, good-first issue
template, and showcase intake so all public repos share one contribution path
unless a repo overrides it.

Rationale: community growth should not depend on each repository separately
remembering to define the same entry points. Org defaults make the 27-repo
workspace easier to understand and easier to contribute to.

Consequences:

- Public examples should point back to one canonical page, post, docs URL,
  package page, or repository.
- Social promotion stays review-first and credential-free in source.
