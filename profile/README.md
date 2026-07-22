<p align="center">
  <img src="https://flyto2.com/logo.png" width="112" alt="Flyto2 logo" />
</p>

<h1 align="center">Flyto2</h1>

<p align="center">
  <strong>Open-source AI workflow automation with deterministic execution, MCP tools, evidence, and replay.</strong>
</p>

<p align="center">
  <a href="https://flyto2.com">Website</a> |
  <a href="https://docs.flyto2.com">Docs</a> |
  <a href="https://blog.flyto2.com">Blog</a> |
  <a href="https://pypi.org/project/flyto-core/">PyPI</a> |
  <a href="https://www.youtube.com/@Flyto2">YouTube</a> |
  <a href="https://github.com/flytohub/flyto-core/discussions">Discussions</a>
</p>

## Start with one command

```bash
pip install "flyto-core[browser]"
playwright install chromium
flyto recipe competitor-intel --url https://github.com/pricing
```

Flyto2 is for builders who need agents to finish real browser and data work,
not just suggest code. Workflows are explicit, every step emits trace and
evidence, and failed runs can resume from the step that needs attention.

The generated Flyto2 Core catalog currently contains **451 registry-backed
modules across 84 categories**. The count comes from the runtime registry and
is checked in CI, rather than maintained as marketing copy.

```text
workflow -> deterministic steps -> trace -> evidence -> replay
```

## Choose your entry point

| You want to... | Start here |
|---|---|
| Run YAML recipes, browser automation, MCP tools, queues, triggers, trace, evidence, and replay | [flyto-core](https://github.com/flytohub/flyto-core) |
| Give a coding agent dependency, context, impact, security, and documentation gates | [flyto-indexer](https://github.com/flytohub/flyto-indexer) |
| Self-host a source-available security warroom and inspect its public contracts | [flyto-warroom](https://github.com/flytohub/flyto-warroom) |
| Read installation, API, configuration, recipe, and operations guides | [docs.flyto2.com](https://docs.flyto2.com) |
| Compare Flyto2 with n8n, Zapier, Make, Playwright, or LangGraph | [flyto2.com](https://flyto2.com) and [the Flyto2 blog](https://blog.flyto2.com) |
| Ask a question, propose an integration, or share a workflow | [Flyto2 Discussions](https://github.com/flytohub/flyto-core/discussions) |

## Why Flyto2 Core

### Deterministic under the AI layer

Agents can select tools and compose workflows, but the execution layer keeps
inputs, outputs, retries, timing, evidence, and replay explicit. That makes a
failed step debuggable and a successful run repeatable.

### Browser work with proof

Recipes can navigate, click, type, extract structured data, capture desktop and
mobile screenshots, measure Web Vitals, create PDFs, and write reports. The
artifacts belong to the run instead of disappearing into an opaque chat.

### MCP-native code intelligence

Flyto2 Indexer gives coding agents local repository context, dependency graphs,
impact analysis, secret and taint checks, documentation coverage, and strict
completion gates. It does not upload repository source for static analysis.

### Open source where the license says open source

`flyto-core` and `flyto-indexer` are Apache-2.0 projects. Other repositories may
use MIT, source-available, or commercial terms. Check each repository's
`LICENSE` before use; the organization profile does not override it.

## Core workflow example

```yaml
id: competitor_intel_v1
steps:
  - id: launch
    module: browser.launch
    params: { headless: true }
  - id: visit
    module: browser.goto
    params: { url: "{{target_url}}", wait_until: networkidle }
  - id: capture
    module: browser.screenshot
    params: { path: competitor.png, full_page: true }
  - id: close
    module: browser.close
```

Start with the built-in recipes for competitor intelligence, full website
audits, screenshots, SEO checks, and structured extraction. Use the module
catalog when you need lower-level control.

## Repository map

### Open-source foundations

| Repository | Responsibility |
|---|---|
| [flyto-core](https://github.com/flytohub/flyto-core) | Python execution engine, CLI, YAML recipes, browser runtime, modules, MCP, evidence, and replay |
| [flyto-indexer](https://github.com/flytohub/flyto-indexer) | Local code-intelligence CLI and MCP server for context, impact, dependency, security, and quality gates |
| [flyto-i18n](https://github.com/flytohub/flyto-i18n) | Shared locale contracts and translation validation |
| [flyto-design-tokens](https://github.com/flytohub/flyto-design-tokens) | Shared visual tokens and generated CSS/JavaScript references |
| [flyto-plugins-js](https://github.com/flytohub/flyto-plugins-js) | JavaScript plugin SDK and integration contracts |

### Product and public surfaces

| Repository | Responsibility |
|---|---|
| [flyto-warroom](https://github.com/flytohub/flyto-warroom) | Generated source-available Warroom CE distribution, public contracts, installer, and release evidence |
| [flyto-cloud](https://github.com/flytohub/flyto-cloud) | Hosted automation and application surfaces |
| [flyto-code](https://github.com/flytohub/flyto-code) | Security cockpit frontend and product interaction contracts |
| [flyto-app](https://github.com/flytohub/flyto-app) | Flutter mobile command-center client |
| [flyto-cortex](https://github.com/flytohub/flyto-cortex) | Knowledge workspace frontend |
| [flyto-data](https://github.com/flytohub/flyto-data) | Data-product API and management surface |
| [flyto-docs](https://github.com/flytohub/flyto-docs) | Public technical documentation |
| [flyto-landing-page](https://github.com/flytohub/flyto-landing-page) | Product and comparison pages at flyto2.com |
| [flyto-blog](https://github.com/flytohub/flyto-blog) | Technical articles, release stories, and implementation notes |
| [flyto2](https://github.com/flytohub/flyto2) | Deprecated legacy release and security-routing shell; not the active desktop source |

The remaining repositories hold engine services, blueprints, AI helpers,
commercial extensions, admin tools, release memory, and editor integrations.
Each repository README states its own authority and license.

## Community

- Ask usage and design questions in [Discussions](https://github.com/flytohub/flyto-core/discussions).
- Pick a scoped task from [good first issues](https://github.com/flytohub/flyto-core/contribute).
- Share a recipe, MCP setup, integration, or Warroom CE lab through the
  organization showcase template.
- Read [`CONTRIBUTING.md`](https://github.com/flytohub/.github/blob/main/CONTRIBUTING.md)
  before changing shared contracts.
- Report vulnerabilities privately through the repository Security tab or
  `security@flyto2.com`, never through a public issue.

## Contact

- Community: [Flyto2 Discussions](https://github.com/flytohub/flyto-core/discussions)
- Documentation: [docs.flyto2.com](https://docs.flyto2.com)
- Partnerships and press: `hello@flyto2.com`
- Security: `security@flyto2.com`

<p align="center">
  <sub>Built in Taiwan. License terms are declared per repository.</sub>
</p>
