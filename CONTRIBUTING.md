# Contributing

Thanks for helping Flyto. Org-wide defaults live here. If a repo ships
its own `CONTRIBUTING.md` it takes precedence.

## Before you start

- **Search first.** Someone may already be on it. Check issues, PRs, and
  [Discussions](https://github.com/flytohub/flyto-core/discussions).
- **Small fix (typo, broken link, obvious bug)** → PR straight to `main`.
- **Anything non-trivial** → open an issue or discussion first. Getting
  alignment before writing code saves both of us rework.

## Setting up

Every repo's README has a `Quick start` block. If it doesn't, open an
issue — missing onboarding counts as a bug.

## Coding style

- **Small diffs.** One PR = one conceptual change. Don't mix refactors
  with behaviour changes.
- **Tests** for any new behaviour. Bug fixes should include a regression
  test that fails without the fix.
- **Follow the file you're editing.** If there's an established pattern
  in the area you're touching, match it rather than importing a
  different style.
- **Comments for *why*, not *what*.** The code already says what it
  does; tell future us the motivation.
- **Docs when the public surface changes.** Update the README / docs /
  OpenAPI spec in the same PR.

## Commits

- Conventional-ish format, short imperative summary:
  ```
  auth: purge expired tokens from getAccessToken()
  ```
- Body (wrap at 72 cols) only when the *why* doesn't fit in the subject.
- Reference issues with `Fixes #123` / `Refs #123` when it applies.

## PRs

- Fill out the PR template. It's there to save the reviewer time.
- Keep the PR open to feedback — we may suggest restructures for
  larger changes. That's normal, not a rejection.
- CI must be green before review. If you think CI is wrong, say so in
  the description.

## Licensing

By contributing you agree that:

- Your contribution is your own work, or you have permission to
  contribute it.
- It's licensed to the project under the repo's `LICENSE` file.
- For Pro / commercial repos, additional terms may apply — those repos'
  CONTRIBUTING files spell them out.

## Code of Conduct

Everyone here follows the [Code of Conduct](./CODE_OF_CONDUCT.md). No
exceptions.

## Contact

- Discussion / Q&A: [GitHub Discussions](https://github.com/flytohub/flyto-core/discussions)
- Security: see [SECURITY.md](./SECURITY.md) — do **not** open a public issue
- Everything else: hello@flyto2.com
