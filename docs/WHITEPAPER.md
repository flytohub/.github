# Flyto2 Organization Governance Whitepaper

## Abstract

Flyto2 is maintained across independent repositories, languages, packages, and
public sites. This repository provides the shared governance layer: public
community defaults, reusable security workflows, and a machine-readable
documentation contract. Its purpose is to make repository quality observable
without moving product authority into a central monorepo.

## Design Principles

1. Product behavior stays with the repository that implements it.
2. Organization policy is reusable, versioned, and least-privilege.
3. Durable documentation maps features and source areas to maintained files.
4. Generated references supplement explanations; they do not replace them.
5. A shared gate never substitutes for a product's tests, build, or deployment
   checks.

## Governance Architecture

GitHub applies profile and community files as organization defaults. Calling
repositories opt into pinned reusable workflows for security, CodeQL, SBOM,
and documentation checks. The documentation workflow checks out this policy
repository separately, then audits the caller's own checkout and manifest.
Policy files cannot satisfy the caller's content requirements.

The manifest records audience, lifecycle status, documentation entry points,
source ownership, and feature surfaces. Large or generated repositories may
split source references and explicitly exclude test or generated paths. Every
declared local document and source mapping remains link-checked.

## Trust And Security Model

Reusable workflows request only the permissions required by their job.
Third-party actions are pinned. Product credentials and deployment authority do
not belong here. Vulnerability reports use private GitHub reporting or
security@flyto2.com; public issues are not a disclosure channel.

The audit removes fenced code and inline code before checking public brand
copy, preserving documented compatibility identifiers while rejecting
accidental product naming or contact-domain drift.

## Verifiable Contract

The maintained contract is defined by
[the JSON schema](documentation-contract.schema.json), explained by
[the documentation standard](DOCUMENTATION_STANDARD.md), and implemented by
[the audit script](../scripts/audit-documentation.py). The generated
[Python reference](reference/python-api.md) links every audit function to its
source line. Unit tests cover malformed scope fields, local-link escape,
shared-policy isolation, brand/contact checks, and generated descriptions.

## Limits

This repository cannot prove that a product feature works, a deployment is
healthy, or a public claim is commercially accurate. Those remain obligations
of the owning repository. The governance layer proves that declared ownership,
documentation structure, and reusable checks are internally consistent.

