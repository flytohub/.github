# Flyto2 Organization Configuration

This repository provides the public profile, community defaults, reusable
security workflows, and documentation governance shared by the
[Flyto2 GitHub organization](https://github.com/flytohub).

## Start Here

- [Organization profile](profile/README.md)
- [Community paths](COMMUNITY.md)
- [Contribution guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Documentation index](docs/README.md)
- [Documentation standard](docs/DOCUMENTATION_STANDARD.md)

## Reusable Workflows

Calling repositories can use the security, CodeQL, SBOM, and documentation
workflows in `.github/workflows/`. Each caller remains responsible for its
stack-specific build and product verification.

## Installation

Nothing in this repository is installed into a product runtime. GitHub applies
the profile and community-health files at organization scope. Calling
repositories opt into reusable workflows with a pinned `uses:` reference.

## Usage

Use the files in this repository as organization defaults. Product repositories
should keep their own `docs/documentation-manifest.json`, invoke the reusable
documentation workflow, and retain stack-specific tests, builds, API checks,
and deployment gates locally.

## API

The public interfaces are reusable workflow inputs under
`.github/workflows/reusable-*.yml` and the JSON contract in
[`docs/documentation-contract.schema.json`](docs/documentation-contract.schema.json).
The [feature reference](docs/FEATURES.md) explains ownership and failure
boundaries; product APIs are not defined here.

## Configuration

Reusable workflow inputs such as `stack`, language versions, strict mode, and
artifact names are documented beside each workflow. No product credentials or
runtime environment variables belong in this repository.

## Documentation Audit

From this repository root:

```bash
python3 scripts/audit-documentation.py . --json
```

The audit uses only the Python standard library and does not send repository
content to an external service.

Generate and check the source-level automation reference with:

```bash
python3 scripts/generate-source-reference.py
python3 scripts/generate-source-reference.py --check
```

## Architecture

GitHub renders `profile/README.md` and applies default templates automatically.
Reusable workflows execute in caller repositories with least-privilege
permissions. The documentation workflow checks out this repository as the
policy source, then audits the caller's local manifest and files.

## Testing

Run the strict organization gate from this repository root:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/audit-documentation.py . --strict --json
python3 scripts/generate-source-reference.py --check
flyto-index verify . --full-scan --strict
```

CI repeats Markdown lint, local-link tests, a deterministic documentation
bundle build, the dependency-free contract audit, and strict Indexer checks.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Changes to reusable workflows must
preserve least-privilege permissions and pinned third-party actions. Public
copy must match the current owning product repository and avoid unverified
release, compatibility, or support-response claims.

## License

Organization templates and documentation follow the notice in each file or
repository. Product repositories and release artifacts keep their own license;
this repository does not override them.

## Boundaries

This repository does not own Flyto2 product source, product roadmaps, package
APIs, or deployment credentials. Follow links to the relevant product
repository or [docs.flyto2.com](https://docs.flyto2.com) for those details.
