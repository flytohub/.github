#!/usr/bin/env python3
"""Validate a repository against the Flyto2 documentation contract."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT.md",
    "ARCHITECTURE.md",
    "STATE.md",
    "ROADMAP.md",
    "tasks.md",
    "DECISIONS.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "docs/README.md",
    "docs/documentation-manifest.json",
    "workflows/idea-capture.md",
    "workflows/planning.md",
    "workflows/implementation.md",
    "workflows/bugfix.md",
    "workflows/refactor.md",
    "workflows/investigation.md",
    "workflows/wrap-up.md",
    "handoffs/_registry.md",
)
ALLOWED_REPOSITORY_STATUS = {"active", "experimental", "internal", "deprecated", "generated"}
ALLOWED_FEATURE_KIND = {
    "api", "cli", "configuration", "content", "governance", "library",
    "operations", "schema", "ui", "workflow",
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MARKDOWN_LINK = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")
EMAIL_PATTERN = re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE)
EXAMPLE_EMAIL_DOMAINS = {
    "example.com", "example.org", "example.net", "example.invalid",
    "example.test", "test.dev", "localhost",
}
CHECKOUT_EXCLUSIONS = (".flyto-doc-standard/",)


def parse_args() -> argparse.Namespace:
    """Parse the target repository, manifest path, output mode, and strictness."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    parser.add_argument("--manifest", default="docs/documentation-manifest.json")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    return parser.parse_args()


def tracked_files(root: Path) -> list[str]:
    """Return committed and pending repository files without shared-policy checkout files."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        check=True,
        capture_output=True,
    )
    return [
        relative
        for item in result.stdout.split(b"\0")
        if item
        for relative in [item.decode("utf-8")]
        if not relative.startswith(CHECKOUT_EXCLUSIONS)
    ]


def split_target(value: str) -> str:
    """Remove an optional Markdown anchor from a repository path."""
    return value.split("#", 1)[0]


def matches(pattern: str, files: list[str]) -> list[str]:
    """Resolve an exact repository path or glob against the audited file set."""
    if not any(char in pattern for char in "*?["):
        return [pattern] if pattern in files else []
    return [path for path in files if fnmatch.fnmatchcase(path, pattern)]


def validate_path_list(
    *,
    label: str,
    values: object,
    files: list[str],
    errors: list[str],
    documentation: bool = False,
) -> list[str]:
    """Validate a required non-empty path list and return its valid shape."""
    if not isinstance(values, list) or not values or not all(isinstance(item, str) and item for item in values):
        errors.append(f"{label} must be a non-empty string array")
        return []

    for value in values:
        target = split_target(value) if documentation else value
        if documentation:
            if target.startswith(("https://", "http://")):
                continue
            if target not in files:
                errors.append(f"{label} documentation target does not exist: {target}")
        elif not matches(target, files):
            errors.append(f"{label} source pattern matches no tracked file: {target}")
    return values


def validate_manifest(root: Path, manifest_path: Path, files: list[str]) -> tuple[dict, list[str], list[str]]:
    """Validate documentation ownership, feature evidence, and optional scanner scope."""
    errors: list[str] = []
    warnings: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"cannot read manifest: {exc}"], warnings

    if manifest.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if manifest.get("repository") != root.name:
        errors.append(f"repository must be {root.name!r}")
    if manifest.get("status") not in ALLOWED_REPOSITORY_STATUS:
        errors.append("status is missing or unsupported")
    audiences = manifest.get("audiences")
    if not isinstance(audiences, list) or not audiences or not all(isinstance(item, str) and item.strip() for item in audiences):
        errors.append("audiences must be a non-empty string array")

    documentation = manifest.get("documentation")
    required_docs = {"index", "architecture", "state", "security", "changelog", "feature_reference"}
    if not isinstance(documentation, dict):
        errors.append("documentation must be an object")
    else:
        for key in sorted(required_docs):
            value = documentation.get(key)
            if not isinstance(value, str) or split_target(value) not in files:
                errors.append(f"documentation.{key} must reference a tracked file")
        references = documentation.get("source_reference", [])
        if isinstance(references, str):
            references = [references]
        if "source_reference" in documentation and (
            not isinstance(references, list)
            or not references
            or not all(isinstance(item, str) and item for item in references)
        ):
            errors.append("documentation.source_reference must be a path or path array")
        elif isinstance(references, list):
            for reference in references:
                if Path(reference).is_absolute() or ".." in Path(reference).parts:
                    errors.append(f"documentation.source_reference must stay in repository: {reference}")
                elif not matches(reference, files):
                    errors.append(f"documentation.source_reference matches no tracked file: {reference}")
        exclusions = documentation.get("source_reference_exclude", [])
        if isinstance(exclusions, str):
            exclusions = [exclusions]
        if "source_reference_exclude" in documentation and (
            not isinstance(exclusions, list)
            or not exclusions
            or not all(isinstance(item, str) and item for item in exclusions)
        ):
            errors.append("documentation.source_reference_exclude must be a path array")
        elif isinstance(exclusions, list):
            for exclusion in exclusions:
                if Path(exclusion).is_absolute() or ".." in Path(exclusion).parts:
                    errors.append(
                        "documentation.source_reference_exclude must stay in repository: "
                        f"{exclusion}"
                    )
        module_roots = documentation.get("module_roots", [])
        if "module_roots" in documentation and (
            not isinstance(module_roots, list)
            or not all(isinstance(item, str) and item for item in module_roots)
        ):
            errors.append("documentation.module_roots must be a path array")
        elif isinstance(module_roots, list):
            for module_root in module_roots:
                prefix = module_root.rstrip("/") + "/"
                if (
                    Path(module_root).is_absolute()
                    or ".." in Path(module_root).parts
                    or not any(path.startswith(prefix) for path in files)
                ):
                    errors.append(f"documentation.module_roots has no tracked directory: {module_root}")
        if (
            "configuration_not_applicable" in documentation
            and not isinstance(documentation["configuration_not_applicable"], bool)
        ):
            errors.append("documentation.configuration_not_applicable must be boolean")

    source_ids: set[str] = set()
    source_areas = manifest.get("source_areas")
    if not isinstance(source_areas, list) or not source_areas:
        errors.append("source_areas must be a non-empty array")
    else:
        for index, area in enumerate(source_areas):
            label = f"source_areas[{index}]"
            if not isinstance(area, dict):
                errors.append(f"{label} must be an object")
                continue
            area_id = area.get("id")
            if not isinstance(area_id, str) or not ID_PATTERN.fullmatch(area_id):
                errors.append(f"{label}.id must be kebab-case")
            elif area_id in source_ids:
                errors.append(f"duplicate source area id: {area_id}")
            else:
                source_ids.add(area_id)
            if len(str(area.get("description", "")).strip()) < 30:
                errors.append(f"{label}.description must explain ownership")
            validate_path_list(label=f"{label}.paths", values=area.get("paths"), files=files, errors=errors)
            validate_path_list(
                label=f"{label}.documentation",
                values=area.get("documentation"),
                files=files,
                errors=errors,
                documentation=True,
            )

    feature_ids: set[str] = set()
    feature_surfaces = manifest.get("feature_surfaces")
    if not isinstance(feature_surfaces, list) or not feature_surfaces:
        errors.append("feature_surfaces must be a non-empty array")
    else:
        for index, feature in enumerate(feature_surfaces):
            label = f"feature_surfaces[{index}]"
            if not isinstance(feature, dict):
                errors.append(f"{label} must be an object")
                continue
            feature_id = feature.get("id")
            if not isinstance(feature_id, str) or not ID_PATTERN.fullmatch(feature_id):
                errors.append(f"{label}.id must be kebab-case")
            elif feature_id in feature_ids:
                errors.append(f"duplicate feature id: {feature_id}")
            else:
                feature_ids.add(feature_id)
            if len(str(feature.get("title", "")).strip()) < 3:
                errors.append(f"{label}.title is required")
            if feature.get("kind") not in ALLOWED_FEATURE_KIND:
                errors.append(f"{label}.kind is unsupported")
            if feature.get("status") not in ALLOWED_REPOSITORY_STATUS:
                errors.append(f"{label}.status is unsupported")
            if len(str(feature.get("description", "")).strip()) < 40:
                errors.append(f"{label}.description must explain behavior and boundary")
            validate_path_list(label=f"{label}.source", values=feature.get("source"), files=files, errors=errors)
            validate_path_list(
                label=f"{label}.documentation",
                values=feature.get("documentation"),
                files=files,
                errors=errors,
                documentation=True,
            )
            tests = feature.get("tests", [])
            if tests:
                validate_path_list(label=f"{label}.tests", values=tests, files=files, errors=errors)
            verification = feature.get("verification", [])
            if verification and (not isinstance(verification, list) or not all(isinstance(item, str) for item in verification)):
                errors.append(f"{label}.verification must be a string array")
            if feature.get("status") == "active" and not tests and not verification:
                warnings.append(f"{label} is active but has no test path or verification command")

    return manifest, errors, warnings


def check_local_links(root: Path, files: list[str]) -> list[str]:
    """Report Markdown links that escape the repository or target missing local files."""
    warnings: list[str] = []
    tracked = set(files)
    for relative in files:
        if not relative.endswith((".md", ".mdx")):
            continue
        path = root / relative
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for raw_target in MARKDOWN_LINK.findall(content):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "https://", "http://", "mailto:")):
                continue
            target_path = target.split("#", 1)[0].split("?", 1)[0]
            resolved = (path.parent / target_path).resolve()
            try:
                resolved_relative = resolved.relative_to(root).as_posix()
            except ValueError:
                warnings.append(f"{relative}: local link escapes repository: {target}")
                continue
            if resolved_relative not in tracked and not resolved.is_dir():
                warnings.append(f"{relative}: missing local link target: {target}")
    return warnings


def check_brand_and_contacts(root: Path, files: list[str]) -> list[str]:
    """Reject retired product naming and unsupported public contact domains."""
    errors: list[str] = []
    for relative in files:
        if not relative.endswith((".md", ".mdx", ".rst")):
            continue
        path = root / relative
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if re.search(r"\bFlyto\b", content):
            errors.append(f"{relative}: contains retired product name; use Flyto2")
        for email in EMAIL_PATTERN.findall(content):
            if email.lower() == "git@github.com":
                continue
            domain = email.rsplit("@", 1)[1].lower()
            if domain == "flyto2.com" or domain in EXAMPLE_EMAIL_DOMAINS:
                continue
            if domain.endswith((".iam.gserviceaccount.com", ".users.noreply.github.com")):
                continue
            errors.append(f"{relative}: public contact email must use @flyto2.com: {email}")
    return errors


def main() -> int:
    """Run the complete audit and print deterministic text or JSON results."""
    args = parse_args()
    root = Path(args.root).resolve()
    files = tracked_files(root)
    errors = [f"missing required file: {path}" for path in REQUIRED_FILES if path not in files]
    manifest_path = root / args.manifest
    manifest, manifest_errors, warnings = validate_manifest(root, manifest_path, files)
    errors.extend(manifest_errors)
    errors.extend(check_brand_and_contacts(root, files))
    warnings.extend(check_local_links(root, files))

    result = {
        "ok": not errors and (not args.strict or not warnings),
        "repository": root.name,
        "manifest": args.manifest,
        "source_areas": len(manifest.get("source_areas", [])) if manifest else 0,
        "feature_surfaces": len(manifest.get("feature_surfaces", [])) if manifest else 0,
        "errors": sorted(set(errors)),
        "warnings": sorted(set(warnings)),
    }
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=True))
    else:
        status = "PASS" if result["ok"] else "FAIL"
        print(f"documentation contract {status}: {root.name}")
        print(f"source areas: {result['source_areas']}; feature surfaces: {result['feature_surfaces']}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
