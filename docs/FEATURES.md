# Organization Feature Reference

This reference maps the Flyto2 organization repository's public and maintainer
surfaces. Product features remain documented in their owning repositories.

## Organization Profile

`profile/README.md` is the first GitHub organization page visitors see. It
introduces Flyto2, links to the product, documentation, blog, packages, and
community paths, and must not carry implementation claims that belong to a
product repository.

## Community Intake

Issue and discussion templates provide consistent intake for bugs, feature
requests, good-first contributions, Q&A, ideas, and showcases. Repository-local
templates may override these defaults when a product requires additional
technical context.

## Community Policies

The contribution, conduct, support, security, and community documents are
organization defaults. Security reports use the private process in
`SECURITY.md`; public issues are not a vulnerability-reporting channel.

## Reusable Security Workflows

- `reusable-security.yml` performs secret and dependency scanning by stack.
- `reusable-codeql.yml` runs CodeQL for supported languages.
- `reusable-sbom.yml` creates CycloneDX SBOM evidence and scans it with Grype.

Calling repositories own their stack selection and any build prerequisites.

## Documentation Governance

`reusable-documentation.yml` checks out this repository's standard and runs the
dependency-free documentation contract audit against the caller. The audit
checks required memory files, feature/source mappings, local links, Flyto2
naming, and public contact domains. Product-specific API generators and site
builds stay in the caller repository.

The standard checkout is excluded from the caller's own tracked-file view, so
its policy files cannot satisfy or contaminate the caller contract. Strict mode
is the reusable workflow default, and stdlib unit tests cover malformed scope
fields, naming/contact checks, and local-link failures.

The organization repository also runs its own Markdown lint, local-link test,
deterministic documentation bundle build, strict contract audit, generated
Python reference check, and Flyto2 Indexer verification. Reusable workflow
success never substitutes for the caller's product tests and build.
