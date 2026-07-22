# Flyto2 Documentation Standard

This standard applies to every repository in the Flyto2 GitHub organization.
It keeps user documentation, contributor memory, generated references, and
historical handoffs separate so a large Markdown tree remains navigable.

## Documentation Layers

| Layer | Audience | Required location | Purpose |
|---|---|---|---|
| Entry point | New users | `README.md` | Explain the product boundary, first successful use, and next links. |
| Durable docs | Users and operators | `docs/` | Explain features, public interfaces, configuration, security, and operations. |
| Project memory | Maintainers and agents | Repository root | Record architecture, current state, roadmap, decisions, and change history. |
| Source reference | Integrators | Language-native docs or `docs/reference/` | Cover public functions, classes, types, commands, routes, and schemas. |
| Workflows | Contributors and agents | `workflows/` | Define repeatable planning, implementation, investigation, and wrap-up procedures. |
| Handoffs | Maintainers and agents | `handoffs/` | Preserve dated context that should not be presented as current product truth. |

## Required Files

Every repository must maintain:

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`
- `PROJECT.md`
- `ARCHITECTURE.md`
- `STATE.md`
- `ROADMAP.md`
- `tasks.md`
- `DECISIONS.md`
- `CHANGELOG.md`
- `SECURITY.md`
- `docs/README.md`
- `docs/documentation-manifest.json`
- `workflows/idea-capture.md`
- `workflows/planning.md`
- `workflows/implementation.md`
- `workflows/bugfix.md`
- `workflows/refactor.md`
- `workflows/investigation.md`
- `workflows/wrap-up.md`
- `handoffs/_registry.md`

`CONTRIBUTING.md` is required for repositories that accept contributions.
Deprecated or generated repositories must still document why they exist and
where the current source of truth lives.

## Feature Coverage Contract

`docs/documentation-manifest.json` is the machine-readable map between product
surfaces and their evidence. Small repositories should list explicit feature
surfaces. Large, generated, or content-heavy repositories may use source areas
plus a canonical feature reference or whitepaper and an exact-line generated
source reference; this avoids duplicating thousands of declarations as feature
rows. An explicit feature surface records:

- a stable identifier and plain-language description;
- whether it is active, experimental, deprecated, generated, or internal;
- the source paths that implement it;
- the durable documents that explain it;
- tests or verification commands that prove the documented behavior where
  applicable.

The manifest does not replace prose. It prevents features from silently
appearing in code without an owning document and prevents documentation from
claiming behavior that has no source path.

## Public Interface Rule

Document public interfaces at the level appropriate to the language:

- Python packages: public modules, exported classes/functions, CLI commands,
  exceptions, configuration, and meaningful docstrings.
- Go services: OpenAPI routes, exported domain contracts, package boundaries,
  store interfaces, configuration, migrations, and operator runbooks. Internal
  helpers stay in GoDoc when their invariants are not obvious.
- TypeScript/JavaScript packages: package exports, components intended for
  reuse, hooks, configuration, events, and build commands.
- Applications: user workflows, routes/screens, API ownership, loading and
  failure states, configuration, deployment, and troubleshooting.
- Content repositories: publishing model, metadata schema, sitemap/discovery
  surfaces, automation, and editorial checks.

Generated files must identify their generator and regeneration command. Do not
hand-edit generated references.

`documentation.source_reference` may be one repository-local file or a list of
files/globs that link declarations to exact source lines. Use
`source_reference_exclude` only for vendored dependencies or fixtures whose
authority belongs to another repository; it does not suppress source or
security scanning. A repository with no runtime configuration may set
`configuration_not_applicable` to `true` instead of creating a fake
`.env.example`.

## Writing Rules

- Use the name **Flyto2**. Do not use the retired product name.
- Public contact addresses must use `@flyto2.com`.
- Describe shipped behavior in the present tense and planned behavior in the
  roadmap. Do not mix both in one feature table.
- Prefer one canonical explanation and link to it. Do not duplicate large
  blocks across repositories.
- Every command must state its working directory, prerequisites, and whether it
  changes external state when that is not obvious.
- Every API example must state authentication and tenant/organization scope.
- Security-sensitive examples use placeholders, never working credentials.
- Historical audits and handoffs must show their date and current status.

## Verification

Run the organization audit from a repository root:

```bash
python .flyto-doc-standard/scripts/audit-documentation.py . --json
```

Repository CI calls the same script through the reusable documentation
workflow. Product-specific build, link, OpenAPI, TypeDoc, GoDoc, dartdoc, or
mkdocstrings checks remain in the owning repository.
