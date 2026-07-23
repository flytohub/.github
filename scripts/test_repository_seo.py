"""Tests for the Flyto2 repository discovery and SEO contract."""

from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("audit-repository-seo.py")
SPEC = importlib.util.spec_from_file_location("audit_repository_seo", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class RepositorySeoAuditTests(unittest.TestCase):
    """Exercise portfolio counts, licensing, and Ubersuggest evidence rules."""

    def setUp(self) -> None:
        """Load an isolated copy of the checked-in discovery manifest."""
        self.manifest = AUDIT.load_manifest(AUDIT.DEFAULT_MANIFEST)

    def test_checked_in_manifest_is_complete(self) -> None:
        """Keep all 28 repositories mapped to a deliberate discovery policy."""
        keywords, keyword_errors = AUDIT.validate_keywords(self.manifest)
        repositories, repository_errors = AUDIT.validate_repositories(self.manifest, keywords)

        self.assertEqual(keyword_errors, [])
        self.assertEqual(repository_errors, [])
        self.assertEqual(len(repositories), 28)

    def test_source_available_project_cannot_require_open_source_topic(self) -> None:
        """Prevent SEO copy from overriding PolyForm license boundaries."""
        manifest = copy.deepcopy(self.manifest)
        flow = next(row for row in manifest["repositories"] if row["name"] == "flyto-flow")
        flow["required_topics"].append("open-source")
        keywords, _ = AUDIT.validate_keywords(manifest)

        _, errors = AUDIT.validate_repositories(manifest, keywords)

        self.assertTrue(any("cannot require open-source topic" in error for error in errors))

    def test_non_public_project_cannot_target_keywords(self) -> None:
        """Avoid meaningless acquisition SEO on private and internal source."""
        manifest = copy.deepcopy(self.manifest)
        admin = next(row for row in manifest["repositories"] if row["name"] == "flyto-admin")
        admin["keyword_ids"] = ["ai-workflow-automation"]
        keywords, _ = AUDIT.validate_keywords(manifest)

        _, errors = AUDIT.validate_repositories(manifest, keywords)

        self.assertTrue(any("must not target acquisition keywords" in error for error in errors))

    def test_license_detection_distinguishes_osi_and_polyform(self) -> None:
        """Classify source availability separately from OSI open source."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "LICENSE").write_text(
                "# PolyForm Shield License 1.0.0\n",
                encoding="utf-8",
            )
            self.assertEqual(
                AUDIT.detect_license(root),
                ("source-available", "PolyForm-Shield-1.0.0"),
            )


if __name__ == "__main__":
    unittest.main()
