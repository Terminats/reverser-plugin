"""Validate shared skills and assemble a package for a supported host."""

import argparse
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
from urllib.parse import unquote, urlsplit
import uuid

import yaml

from adapters import ADAPTERS


ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
LINK = re.compile(r"\[[^\]\n]+\]\(([^)\n]+)\)")


def is_link(path: Path) -> bool:
    # os.path.isjunction was added in Python 3.12; 3.11 still exposes reparse tags.
    if path.is_symlink():
        return True
    return path.exists() and bool(getattr(path.lstat(), "st_reparse_tag", 0))


def read_catalog(root: Path) -> dict:
    catalog = json.loads((root / "re-skills.json").read_text(encoding="utf-8"))
    expected = {"format_version", "name", "version", "description", "skills"}
    if not isinstance(catalog, dict) or set(catalog) != expected:
        raise ValueError("Catalog must contain: " + ", ".join(sorted(expected)))
    if type(catalog["format_version"]) is not int or catalog["format_version"] != 1:
        raise ValueError("Unsupported catalog format_version")
    if not isinstance(catalog["name"], str) or not IDENTIFIER.fullmatch(catalog["name"]):
        raise ValueError("Invalid package name")
    if not isinstance(catalog["version"], str) or not VERSION.fullmatch(catalog["version"]):
        raise ValueError("Package version must be MAJOR.MINOR.PATCH")
    if not isinstance(catalog["description"], str) or not catalog["description"].strip():
        raise ValueError("Package description is required")
    skills = catalog["skills"]
    if not isinstance(skills, list) or not skills:
        raise ValueError("Catalog must list at least one skill")
    for skill in skills:
        if not isinstance(skill, str) or len(skill) > 64 or not IDENTIFIER.fullmatch(skill):
            raise ValueError(f"Invalid skill ID: {skill!r}")
    if len(set(skills)) != len(skills):
        raise ValueError("Duplicate skill IDs")
    return catalog


def check_source_tree(directory: Path) -> None:
    """Reject links and unexpected generated/private files before copying."""
    for path in (directory, *directory.rglob("*")):
        if is_link(path):
            raise ValueError(f"Source links are not supported: {path}")
        if path.name in {".git", ".env", "__pycache__", ".venv"}:
            raise ValueError(f"Unexpected source artifact: {path}")


def validate_links(document: Path, boundary: Path) -> None:
    for match in LINK.finditer(document.read_text(encoding="utf-8")):
        target = match[1].strip().split(' "', 1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        destination = (document.parent / unquote(parsed.path)).resolve()
        if not destination.is_relative_to(boundary.resolve()) or not destination.exists():
            raise ValueError(f"Broken or escaping local link in {document}: {target}")


def validate_skill(directory: Path, skill: str) -> None:
    check_source_tree(directory)
    text = (directory / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {skill}")
    frontmatter = yaml.safe_load(match[1])
    if not isinstance(frontmatter, dict) or frontmatter.get("name") != skill:
        raise ValueError(f"Frontmatter name must match skill ID: {skill}")
    description = frontmatter.get("description")
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError(f"Invalid skill description: {skill}")
    if not text[match.end():].strip():
        raise ValueError(f"Empty skill instructions: {skill}")
    if (directory / "agents").exists():
        raise ValueError(f"Host metadata belongs in adapters/, not skills/{skill}/agents")
    for document in directory.rglob("*.md"):
        validate_links(document, directory)


def validate_repository(root: Path, agent: str | None = None) -> dict:
    catalog = read_catalog(root)
    check_source_tree(root / "skills")
    actual = {path.name for path in (root / "skills").iterdir() if path.is_dir()}
    if actual != set(catalog["skills"]):
        raise ValueError("Catalog skill IDs must match directories in skills/")
    for skill in catalog["skills"]:
        validate_skill(root / "skills" / skill, skill)
    selected = ADAPTERS if agent is None else {agent: get_adapter(agent)}
    for name, adapter in selected.items():
        check_source_tree(root / "adapters" / name)
        adapter.validate(root, catalog)
    return catalog


def get_adapter(agent: str):
    if agent not in ADAPTERS:
        raise ValueError(f"Unsupported agent: {agent}. Supported: {', '.join(ADAPTERS)}")
    return ADAPTERS[agent]


def build_package(root: Path, agent: str, replace: bool = False) -> Path:
    adapter = get_adapter(agent)
    catalog = validate_repository(root, agent)
    dist = root / "dist"
    destination = dist / agent
    # Check the resolved absolute destination before moving or deleting anything.
    if is_link(dist) or dist.resolve() != root.resolve() / "dist":
        raise ValueError("dist/ must be a real directory directly inside the repository")
    if is_link(destination):
        raise ValueError("Build destination must not be a link")
    if destination.exists() and not destination.is_dir():
        raise ValueError(f"Build destination is not a directory: {destination}")
    if destination.exists() and not replace:
        raise ValueError(f"Output already exists: {destination}. Use --replace to rebuild.")

    dist.mkdir(exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=f".{agent}-build-", dir=dist))
    backup = dist / f".{agent}-previous-{uuid.uuid4().hex}"
    try:
        adapter.build(root, catalog, stage)
        if destination.exists():
            destination.rename(backup)
        try:
            stage.rename(destination)
        except OSError:
            if backup.exists():
                backup.rename(destination)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    if backup.exists():
        shutil.rmtree(backup)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    validate = commands.add_parser("validate", help="Validate catalog, skills, links and adapters")
    validate.add_argument("--agent", help="Validate one adapter instead of all implemented adapters")
    build = commands.add_parser("build", help="Build a plugin and local marketplace in dist/<agent>/")
    build.add_argument("--agent", required=True)
    build.add_argument("--replace", action="store_true", help="Replace this adapter's previous build")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            catalog = validate_repository(ROOT, args.agent)
            print(f"Valid: {len(catalog['skills'])} skills; adapters: {args.agent or ', '.join(ADAPTERS)}")
        else:
            print(f"Built: {build_package(ROOT, args.agent, args.replace)}")
    except (ValueError, OSError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
