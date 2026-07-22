# Organization Automation Scripts

- `audit-documentation.py` validates the Flyto2 repository documentation
  contract, source ownership, feature evidence, local links, naming, and public
  contact domains. It uses the Python standard library and does not send source
  content to an external service.
- `generate-source-reference.py` creates the exact source-linked Python API
  reference under `docs/reference/`. Run it after changing either script and
  use `--check` in CI to detect drift.

From the repository root:

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/generate-source-reference.py
python3 scripts/generate-source-reference.py --check
python3 scripts/audit-documentation.py . --strict --json
```
