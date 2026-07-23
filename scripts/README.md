# Organization Automation Scripts

- `audit-documentation.py` validates the Flyto2 repository documentation
  contract, source ownership, feature evidence, local links, naming, and public
  contact domains. It uses the Python standard library and does not send source
  content to an external service.
- `generate-source-reference.py` creates the exact source-linked Python API
  reference under `docs/reference/`. Run it after changing either script and
  use `--check` in CI to detect drift.
- `audit-repository-seo.py` validates all 28 GitHub repositories, Ubersuggest
  evidence, public About metadata, topic coverage, and license classification.
  Add `--workspace .. --live` for local license and current GitHub checks.

From the repository root:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/generate-source-reference.py
python3 scripts/generate-source-reference.py --check
python3 scripts/audit-documentation.py . --strict --json
python3 scripts/audit-repository-seo.py --workspace .. --live
```
