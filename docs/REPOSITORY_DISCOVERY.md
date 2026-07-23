# Flyto2 Repository Discovery And SEO

This document is the operating contract for GitHub discovery across the 28
repositories owned by `flytohub`. The machine-readable source is
[`repository-seo.json`](repository-seo.json).

## Scope

GitHub currently exposes 16 public repositories and 12 non-public repositories.
Search discovery applies only to public repositories. Private and internal
repositories still require accurate project memory, but adding acquisition
keywords to them would not create search visibility.

The public portfolio has three legally distinct groups:

- **9 OSI open-source repositories:** Apache-2.0 or MIT projects that may use
  `open-source` language when their own `LICENSE` confirms it.
- **2 source-available repositories:** `flyto-flow` uses PolyForm Shield and
  `flyto-warroom` uses PolyForm Noncommercial. Neither may be described as
  OSI-approved open source.
- **5 public content or routing repositories:** the organization profile,
  blog, docs, landing page, and deprecated `flyto2` shell are publicly readable
  but do not grant a repository-wide open-source license.

Repository visibility and license truth take precedence over SEO copy.

## Keyword Evidence

The 2026-07-23 evidence was collected with Ubersuggest. US English is the
primary developer-acquisition market; Taiwan Traditional Chinese checks remain
directional because the related-keyword inventory is sparse.

| Search intent | Volume | SD | PD | CPC | Primary repositories |
| --- | ---: | ---: | ---: | ---: | --- |
| MCP server | 60,500 | 50 | 33 | $9.36 | Core, AI, Docs, Flow, Indexer |
| AI agent framework | 1,300 | 21 | 25 | $10.30 | AI, Core, Landing |
| AI workflow automation | 1,000 | 59 | 40 | $42.24 | Organization profile, Blog, Blueprint, Docs, Landing |
| workflow templates | 1,000 | 45 | 48 | $8.63 | Blueprint |
| attack surface management | 880 | 44 | 25 | $32.48 | Warroom, Blog, Landing |
| MCP security | 880 | 40 | 48 | $20.08 | Warroom, Blog, Docs |
| design tokens | 720 | 52 | 3 | $5.22 | Design Tokens |
| software localization | 720 | 38 | 6 | $16.13 | i18n |
| code analysis tool | 480 | 41 | 26 | $37.60 | Indexer |
| enterprise workflow automation | 210 | 37 | 6 | $53.22 | Pro Core |
| visual workflow builder | 110 | 41 | 47 | $39.11 | Flow |
| desktop automation software | 40 | 37 | 12 | $23.12 | Legacy desktop discovery only |
| plugin SDK | 30 | 19 | 3 | $0.00 | Plugins JS |
| health digital twin | 10 | 17 | 13 | $0.00 | Health Twin |
| workflow automation engine | 10 | 16 | 7 | $0.00 | Core |

The table records measured demand, not a directive to repeat a phrase. A public
README should answer the matching user problem with concrete installation,
usage, limits, license, and next steps. Generic high-volume terms must not be
used where the repository does not implement that intent.

## GitHub Discovery Contract

Every public repository must have:

1. A Flyto2-specific description that states the implemented outcome.
2. A canonical homepage or documentation URL.
3. Focused topics containing `flyto2` plus the actual product category.
4. A README that explains the pain, first successful command or workflow,
   evidence-backed capabilities, limits, license, contribution path, and links.
5. At least one Ubersuggest-backed intent cluster in `repository-seo.json`.
6. License wording that matches the repository's own `LICENSE` file.

Private and internal repositories must remain in the manifest with
`seo_disabled_reason`. This keeps the 28-repository inventory complete without
pretending those repositories can rank publicly.

## Maintenance

- Run `python3 scripts/audit-repository-seo.py --workspace .. --live` before
  changing GitHub About metadata or making a portfolio-wide SEO claim.
- Refresh Ubersuggest values quarterly and retain the source, market, language,
  date, measurement surface, volume, SD, PD, and CPC.
- Use Search Console impressions and clicks to refine site content once real
  query data exists. Ubersuggest estimates do not prove rankings.
- Keep module totals generated from Flyto2 Core runtime facts. Never copy an
  old count from a screenshot or historical audit.
- Do not buy backlinks, automate unsolicited posts, or publish duplicate
  keyword pages. Package registries, release pages, documentation, standards
  discussions, examples, and earned community references are the durable link
  surfaces.

## Verification

The repository audit validates all 28 entries, public/non-public counts,
license classes, keyword evidence, local README coverage, and optional live
GitHub metadata. The weekly organization workflow runs the deterministic
manifest contract. Run the authenticated `--workspace .. --live` command when
GitHub About metadata changes because the repository-scoped Actions token cannot
enumerate the complete private portfolio.
