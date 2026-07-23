# Flyto2 Organization Documentation

This directory owns organization-wide contracts. Product mechanics remain in
the repository that implements them and in [docs.flyto2.com](https://docs.flyto2.com).

## Standards

- [Governance whitepaper](WHITEPAPER.md) explains the cross-repository policy,
  trust, and verification model.
- [Documentation standard](DOCUMENTATION_STANDARD.md) defines the required
  information architecture, feature coverage contract, and writing rules.
- [Documentation contract schema](documentation-contract.schema.json) defines
  `docs/documentation-manifest.json` for every Flyto2 repository.
- [Repository discovery and SEO](REPOSITORY_DISCOVERY.md) defines the 28-repo
  GitHub metadata, license, and Ubersuggest keyword contract.
- [Repository SEO manifest](repository-seo.json) is the machine-readable source
  for public discovery and non-public SEO exclusions.
- [Organization feature reference](FEATURES.md) maps community and reusable
  workflow surfaces to their source of truth.
- [Generated Python API reference](reference/python-api.md) links every
  organization automation function to its maintained source line.

The matching audit implementation is
[`scripts/audit-documentation.py`](../scripts/audit-documentation.py), and CI
uses the reusable workflow at
[`reusable-documentation.yml`](../.github/workflows/reusable-documentation.yml).

## Organization Operations

- [Architecture](../ARCHITECTURE.md)
- [Current state](../STATE.md)
- [Roadmap](../ROADMAP.md)
- [Decisions](../DECISIONS.md)
- [Tasks](../tasks.md)
- [Community guide](../COMMUNITY.md)
- [Contributing](../CONTRIBUTING.md)
- [Security](../SECURITY.md)

Public templates and profile content must also follow the frontend and content
quality rules in [AGENTS.md](../AGENTS.md).
