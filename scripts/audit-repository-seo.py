#!/usr/bin/env python3
"""Validate Flyto2 repository discovery, keyword evidence, and license truth."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "docs" / "repository-seo.json"
PUBLIC_LICENSE_CLASSES = {
    "osi-open-source",
    "source-available",
    "public-content",
}
METRIC_FIELDS = {
    "volume": int,
    "seo_difficulty": int,
    "paid_difficulty": int,
    "cpc_usd": (int, float),
}


def parse_args() -> argparse.Namespace:
    """Parse manifest, workspace, live GitHub, and JSON output options."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def load_manifest(path: Path) -> dict:
    """Load the repository SEO manifest as a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("manifest root must be an object")
    return value


def validate_keywords(manifest: dict) -> tuple[set[str], list[str]]:
    """Validate dated Ubersuggest keyword evidence and return its identifiers."""
    errors: list[str] = []
    if manifest.get("source") != "Ubersuggest":
        errors.append("source must be Ubersuggest")
    measured_at = manifest.get("measured_at")
    if not isinstance(measured_at, str) or len(measured_at.split("-")) != 3:
        errors.append("measured_at must be an ISO date")

    keywords = manifest.get("keywords")
    if not isinstance(keywords, list) or not keywords:
        return set(), [*errors, "keywords must be a non-empty array"]

    identifiers: set[str] = set()
    for index, row in enumerate(keywords):
        label = f"keywords[{index}]"
        if not isinstance(row, dict):
            errors.append(f"{label} must be an object")
            continue
        identifier = row.get("id")
        if not isinstance(identifier, str) or not identifier:
            errors.append(f"{label}.id is required")
        elif identifier in identifiers:
            errors.append(f"duplicate keyword id: {identifier}")
        else:
            identifiers.add(identifier)
        for field in ("keyword", "country", "language", "metric_surface"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(f"{label}.{field} is required")
        for field, expected_type in METRIC_FIELDS.items():
            value = row.get(field)
            if not isinstance(value, expected_type) or isinstance(value, bool) or value < 0:
                errors.append(f"{label}.{field} must be a non-negative number")
    return identifiers, errors


def repository_map(manifest: dict) -> tuple[dict[str, dict], list[str]]:
    """Return repositories keyed by name and report duplicate or malformed rows."""
    errors: list[str] = []
    repositories = manifest.get("repositories")
    if not isinstance(repositories, list):
        return {}, ["repositories must be an array"]
    mapped: dict[str, dict] = {}
    for index, repository in enumerate(repositories):
        if not isinstance(repository, dict):
            errors.append(f"repositories[{index}] must be an object")
            continue
        name = repository.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"repositories[{index}].name is required")
        elif name in mapped:
            errors.append(f"duplicate repository: {name}")
        else:
            mapped[name] = repository
    return mapped, errors


def validate_repositories(manifest: dict, keyword_ids: set[str]) -> tuple[dict[str, dict], list[str]]:
    """Validate portfolio counts, public discovery data, and keyword mappings."""
    repositories, errors = repository_map(manifest)
    portfolio = manifest.get("portfolio", {})
    public = [row for row in repositories.values() if row.get("visibility") == "PUBLIC"]
    non_public = [row for row in repositories.values() if row.get("visibility") != "PUBLIC"]
    open_source = [row for row in public if row.get("license_class") == "osi-open-source"]
    source_available = [row for row in public if row.get("license_class") == "source-available"]
    public_content = [row for row in public if row.get("license_class") == "public-content"]
    observed = {
        "expected_repositories": len(repositories),
        "expected_public": len(public),
        "expected_non_public": len(non_public),
        "expected_osi_open_source": len(open_source),
        "expected_source_available": len(source_available),
        "expected_public_content": len(public_content),
    }
    for key, count in observed.items():
        if portfolio.get(key) != count:
            errors.append(f"portfolio.{key} is {portfolio.get(key)!r}, observed {count}")

    for name, repository in repositories.items():
        visibility = repository.get("visibility")
        license_class = repository.get("license_class")
        if visibility == "PUBLIC":
            if license_class not in PUBLIC_LICENSE_CLASSES:
                errors.append(f"{name}: unsupported public license class {license_class!r}")
            for field in ("homepage", "description", "readme"):
                if not isinstance(repository.get(field), str) or not repository[field].strip():
                    errors.append(f"{name}: {field} is required for public discovery")
            topics = repository.get("required_topics")
            if not isinstance(topics, list) or "flyto2" not in topics or len(topics) < 4:
                errors.append(f"{name}: required_topics must include flyto2 and at least four topics")
            mapped_keywords = repository.get("keyword_ids")
            if not isinstance(mapped_keywords, list) or not mapped_keywords:
                errors.append(f"{name}: at least one Ubersuggest keyword is required")
            else:
                unknown = sorted(set(mapped_keywords) - keyword_ids)
                if unknown:
                    errors.append(f"{name}: unknown keyword ids: {', '.join(unknown)}")
            if license_class == "osi-open-source" and repository.get("spdx") not in {"Apache-2.0", "MIT"}:
                errors.append(f"{name}: OSI project must declare an approved SPDX id")
            if license_class == "source-available" and "open-source" in set(topics or []):
                errors.append(f"{name}: source-available repository cannot require open-source topic")
        else:
            if license_class != "non-public":
                errors.append(f"{name}: non-public repository must use non-public license class")
            if not repository.get("seo_disabled_reason"):
                errors.append(f"{name}: non-public repository needs seo_disabled_reason")
            if repository.get("keyword_ids"):
                errors.append(f"{name}: non-public repository must not target acquisition keywords")
    return repositories, errors


def detect_license(repository_root: Path) -> tuple[str, str | None]:
    """Classify a local repository license without treating visibility as permission."""
    license_path = repository_root / "LICENSE"
    if not license_path.is_file():
        return "public-content", None
    text = license_path.read_text(encoding="utf-8", errors="replace")[:5000]
    if "PolyForm Shield License" in text:
        return "source-available", "PolyForm-Shield-1.0.0"
    if "PolyForm Noncommercial License" in text:
        return "source-available", "PolyForm-Noncommercial-1.0.0"
    if "Apache License" in text and "Version 2.0" in text:
        return "osi-open-source", "Apache-2.0"
    if text.lstrip().startswith("MIT License"):
        return "osi-open-source", "MIT"
    return "unclassified", None


def validate_workspace(workspace: Path, repositories: dict[str, dict]) -> list[str]:
    """Compare public manifest entries with local READMEs and license files."""
    errors: list[str] = []
    for name, repository in repositories.items():
        root = workspace / name
        if not (root / ".git").exists():
            errors.append(f"{name}: local git checkout missing from {workspace}")
            continue
        if repository.get("visibility") != "PUBLIC":
            continue
        readme = root / repository["readme"]
        if not readme.is_file():
            errors.append(f"{name}: public README missing: {repository['readme']}")
        else:
            text = readme.read_text(encoding="utf-8", errors="replace")
            if "Flyto2" not in text:
                errors.append(f"{name}: public README does not identify Flyto2")
        observed_class, observed_spdx = detect_license(root)
        expected_class = repository["license_class"]
        if observed_class != expected_class:
            errors.append(f"{name}: license class {observed_class}, expected {expected_class}")
        if repository.get("spdx") and repository["spdx"] != observed_spdx:
            errors.append(f"{name}: license {observed_spdx}, expected {repository['spdx']}")
    return errors


def live_repositories(owner: str) -> dict[str, dict]:
    """Read current GitHub About metadata with the authenticated gh CLI."""
    fields = "name,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics"
    result = subprocess.run(
        ["gh", "repo", "list", owner, "--limit", "100", "--json", fields],
        check=True,
        capture_output=True,
        text=True,
    )
    return {row["name"]: row for row in json.loads(result.stdout)}


def validate_live(manifest: dict, repositories: dict[str, dict]) -> list[str]:
    """Compare the manifest with current GitHub visibility and About metadata."""
    errors: list[str] = []
    owner = manifest.get("portfolio", {}).get("owner")
    try:
        live = live_repositories(owner)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return [f"cannot read live GitHub repositories: {exc}"]
    missing = sorted(set(repositories) - set(live))
    extra = sorted(set(live) - set(repositories))
    if missing:
        errors.append(f"GitHub is missing manifest repositories: {', '.join(missing)}")
    if extra:
        errors.append(f"manifest is missing GitHub repositories: {', '.join(extra)}")
    default_branch = manifest.get("portfolio", {}).get("default_branch")
    for name in sorted(set(repositories) & set(live)):
        expected = repositories[name]
        observed = live[name]
        if observed.get("visibility") != expected.get("visibility"):
            errors.append(f"{name}: live visibility {observed.get('visibility')}, expected {expected.get('visibility')}")
        branch = (observed.get("defaultBranchRef") or {}).get("name")
        if branch != default_branch:
            errors.append(f"{name}: default branch {branch!r}, expected {default_branch!r}")
        if expected.get("visibility") != "PUBLIC":
            continue
        for field, live_field in (("description", "description"), ("homepage", "homepageUrl")):
            if observed.get(live_field) != expected.get(field):
                errors.append(f"{name}: live {field} differs from repository-seo.json")
        topics = {row["name"] for row in observed.get("repositoryTopics", [])}
        missing_topics = sorted(set(expected.get("required_topics", [])) - topics)
        if missing_topics:
            errors.append(f"{name}: live topics missing {', '.join(missing_topics)}")
        if expected.get("license_class") == "source-available" and "open-source" in topics:
            errors.append(f"{name}: live topics mislabel source-available code as open-source")
    return errors


def audit(manifest_path: Path, workspace: Path | None = None, live: bool = False) -> dict:
    """Run the complete deterministic and optional live repository SEO audit."""
    manifest = load_manifest(manifest_path)
    keyword_ids, errors = validate_keywords(manifest)
    repositories, repository_errors = validate_repositories(manifest, keyword_ids)
    errors.extend(repository_errors)
    if workspace is not None:
        errors.extend(validate_workspace(workspace.resolve(), repositories))
    if live:
        errors.extend(validate_live(manifest, repositories))
    return {
        "ok": not errors,
        "repositories": len(repositories),
        "public": sum(row.get("visibility") == "PUBLIC" for row in repositories.values()),
        "non_public": sum(row.get("visibility") != "PUBLIC" for row in repositories.values()),
        "keywords": len(keyword_ids),
        "source": manifest.get("source"),
        "measured_at": manifest.get("measured_at"),
        "errors": sorted(set(errors)),
    }


def main() -> int:
    """Execute the audit and return a CI-friendly status code."""
    args = parse_args()
    try:
        result = audit(args.manifest.resolve(), args.workspace, args.live)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        result = {"ok": False, "errors": [str(exc)]}
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    elif result["ok"]:
        print(
            "repository SEO contract passed: "
            f"{result['repositories']} repositories, {result['public']} public, "
            f"{result['non_public']} non-public, {result['keywords']} Ubersuggest terms"
        )
    else:
        print("repository SEO contract failed:", file=sys.stderr)
        for error in result["errors"]:
            print(f"- {error}", file=sys.stderr)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
