"""Regression tests for organization documentation governance scripts."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parent


def load_script(name: str, filename: str):
    """Load a hyphenated organization script as an importable test module."""
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


AUDIT = load_script("flyto2_documentation_audit", "audit-documentation.py")
GENERATOR = load_script("flyto2_source_reference", "generate-source-reference.py")


class DocumentationAuditTests(unittest.TestCase):
    """Exercise contract scope, isolation, branding, links, and generated references."""

    def write_manifest(self, root: Path, documentation: dict) -> tuple[Path, list[str]]:
        """Create a minimal valid repository manifest and return its tracked file set."""
        files = [
            "README.md",
            "ARCHITECTURE.md",
            "STATE.md",
            "SECURITY.md",
            "CHANGELOG.md",
            "docs/README.md",
            "docs/FEATURES.md",
            "scripts/tool.py",
        ]
        docs = root / "docs"
        docs.mkdir(parents=True)
        manifest = {
            "schema_version": 1,
            "repository": root.name,
            "status": "active",
            "audiences": ["maintainers"],
            "documentation": {
                "index": "docs/README.md",
                "architecture": "ARCHITECTURE.md",
                "state": "STATE.md",
                "security": "SECURITY.md",
                "changelog": "CHANGELOG.md",
                "feature_reference": "docs/FEATURES.md",
                **documentation,
            },
            "source_areas": [{
                "id": "automation",
                "description": "Owns the repository automation contract and its public documentation.",
                "paths": ["scripts/*.py"],
                "documentation": ["docs/FEATURES.md"],
            }],
            "feature_surfaces": [{
                "id": "documentation-audit",
                "title": "Documentation audit",
                "kind": "workflow",
                "status": "active",
                "description": "Validates the repository documentation contract and reports actionable failures.",
                "source": ["scripts/tool.py"],
                "documentation": ["docs/FEATURES.md"],
                "verification": ["python scripts/tool.py"],
            }],
        }
        manifest_path = docs / "documentation-manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        files.append("docs/documentation-manifest.json")
        return manifest_path, files

    def test_empty_module_roots_declares_no_source_modules(self):
        """Accept an explicit empty source-module scope for content-only repositories."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "demo"
            root.mkdir()
            manifest_path, files = self.write_manifest(root, {"module_roots": []})

            _, errors, warnings = AUDIT.validate_manifest(root, manifest_path, files)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_scope_fields_reject_false_instead_of_silently_disabling_checks(self):
        """Reject boolean false where source-reference path arrays are required."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "demo"
            root.mkdir()
            manifest_path, files = self.write_manifest(
                root,
                {
                    "source_reference": False,
                    "source_reference_exclude": False,
                    "module_roots": False,
                },
            )

            _, errors, _ = AUDIT.validate_manifest(root, manifest_path, files)

        self.assertIn("documentation.source_reference must be a path or path array", errors)
        self.assertIn("documentation.source_reference_exclude must be a path array", errors)
        self.assertIn("documentation.module_roots must be a path array", errors)

    def test_shared_policy_checkout_is_not_counted_as_caller_content(self):
        """Exclude reusable-workflow policy files from the caller repository inventory."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "demo"
            root.mkdir()
            (root / "README.md").write_text("# Demo\n", encoding="utf-8")
            shared = root / ".flyto-doc-standard"
            shared.mkdir()
            (shared / "POLICY.md").write_text("# Policy\n", encoding="utf-8")
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "add", "README.md"], check=True)

            files = AUDIT.tracked_files(root)

        self.assertIn("README.md", files)
        self.assertNotIn(".flyto-doc-standard/POLICY.md", files)

    def test_brand_and_contact_check_rejects_retired_name_and_domain(self):
        """Report public Markdown that uses the retired name or a foreign email domain."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text(
                "# Flyto\n\nContact admin@invalid.example.\n",
                encoding="utf-8",
            )

            errors = AUDIT.check_brand_and_contacts(root, ["README.md"])

        self.assertEqual(len(errors), 2)

    def test_local_link_check_reports_missing_and_escaping_targets(self):
        """Report missing local files and links that resolve outside the repository."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "demo"
            root.mkdir()
            (root / "README.md").write_text(
                "[missing](docs/missing.md) [outside](../outside.md)\n",
                encoding="utf-8",
            )

            warnings = AUDIT.check_local_links(root, ["README.md"])

        self.assertEqual(len(warnings), 2)

    def test_generated_reference_uses_docstrings_and_exact_source_links(self):
        """Keep the automation reference descriptive and linked to exact source lines."""
        rendered = GENERATOR.render()

        self.assertIn("Parse the target repository", rendered)
        self.assertIn("scripts/audit-documentation.py#L", rendered)
        self.assertNotIn("Implements parse args", rendered)


if __name__ == "__main__":
    unittest.main()
