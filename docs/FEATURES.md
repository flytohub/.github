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

For large generated or content repositories, source-area ownership plus a
canonical feature/whitepaper document and exact-line source reference is the
accepted coverage mode. Site-root links are left to the owning framework's
route and build checks; repository-relative links remain part of this audit.

The standard checkout is excluded from the caller's own tracked-file view, so
its policy files cannot satisfy or contaminate the caller contract. Strict mode
is the reusable workflow default, and stdlib unit tests cover malformed scope
fields, naming/contact checks, and local-link failures.

The organization repository also runs its own Markdown lint, local-link test,
deterministic documentation bundle build, strict contract audit, generated
Python reference check, and Flyto2 Indexer verification. Reusable workflow
success never substitutes for the caller's product tests and build.

## Repository Discovery Governance

`docs/repository-seo.json` inventories all 28 GitHub repositories. It records
visibility, canonical About metadata, required topics, local README authority,
license classification, and dated Ubersuggest intent evidence. Public
repositories receive keyword mappings; private and internal repositories carry
an explicit reason that acquisition SEO is disabled.

`scripts/audit-repository-seo.py` validates the static contract, checks local
README and license truth when a workspace is available, and compares current
GitHub metadata when `--live` is enabled. The contract keeps OSI open-source,
source-available, public-content, and non-public repositories distinct.
