import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from re_skills import ADAPTERS, build_package, validate_repository


class PackagingTests(unittest.TestCase):
    def setUp(self):
        temporary_root = ROOT / ".tmp"
        temporary_root.mkdir(exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=temporary_root)
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for directory in ("skills", "adapters", "scripts"):
            shutil.copytree(ROOT / directory, self.root / directory, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copyfile(ROOT / "re-skills.json", self.root / "re-skills.json")

    def edit_catalog(self, **changes):
        path = self.root / "re-skills.json"
        catalog = json.loads(path.read_text(encoding="utf-8"))
        catalog.update(changes)
        path.write_text(json.dumps(catalog), encoding="utf-8")

    def test_build_preserves_every_skill_resource_and_attaches_metadata(self):
        catalog = validate_repository(self.root)
        destination = build_package(self.root, "codex")
        plugin = destination / catalog["name"]
        manifest = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
        for field in ("name", "version", "description"):
            self.assertEqual(manifest[field], catalog[field])
        for skill in catalog["skills"]:
            source = self.root / "skills" / skill
            for path in source.rglob("*"):
                if path.is_file():
                    output = plugin / "skills" / skill / path.relative_to(source)
                    self.assertEqual(output.read_bytes(), path.read_bytes())
            metadata = self.root / "adapters/codex/skills" / skill / "openai.yaml"
            self.assertEqual(
                (plugin / "skills" / skill / "agents/openai.yaml").read_bytes(),
                metadata.read_bytes(),
            )
        marketplace = json.loads((destination / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual((destination / marketplace["plugins"][0]["source"]["path"]).resolve(), plugin)

    def test_default_preserves_existing_output(self):
        destination = build_package(self.root, "codex")
        sentinel = destination / "keep.txt"
        sentinel.write_text("previous build", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "already exists"):
            build_package(self.root, "codex")
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "previous build")

    def test_optional_prompt_is_checked_when_provided(self):
        path = self.root / "adapters/codex/skills/readable-code/openai.yaml"
        metadata = yaml.safe_load(path.read_text(encoding="utf-8"))
        for prompt in ("", 123, "Use $another-skill"):
            with self.subTest(prompt=prompt):
                metadata["interface"]["default_prompt"] = prompt
                path.write_text(yaml.safe_dump(metadata), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "Codex prompt must reference"):
                    validate_repository(self.root)

    def test_explicit_replace_removes_stale_output(self):
        destination = build_package(self.root, "codex")
        (destination / "stale.txt").write_text("old", encoding="utf-8")
        self.edit_catalog(version="0.2.0")
        build_package(self.root, "codex", replace=True)
        self.assertFalse((destination / "stale.txt").exists())
        manifest = json.loads((destination / "re-skills/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.2.0")

    def test_failed_assembly_preserves_previous_package(self):
        destination = build_package(self.root, "codex")
        sentinel = destination / "keep.txt"
        sentinel.write_text("previous", encoding="utf-8")
        with patch.object(ADAPTERS["codex"], "build", side_effect=OSError("assembly failed")):
            with self.assertRaisesRegex(OSError, "assembly failed"):
                build_package(self.root, "codex", replace=True)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "previous")
        self.assertEqual(list((self.root / "dist").iterdir()), [destination])

    def test_failed_publication_restores_previous_package(self):
        destination = build_package(self.root, "codex")
        (destination / "keep.txt").write_text("previous", encoding="utf-8")
        rename = Path.rename

        def fail_stage_rename(source, target):
            if source.name.startswith(".codex-build-"):
                raise OSError("publication failed")
            return rename(source, target)

        with patch.object(Path, "rename", fail_stage_rename):
            with self.assertRaisesRegex(OSError, "publication failed"):
                build_package(self.root, "codex", replace=True)
        self.assertTrue((destination / "keep.txt").exists())
        self.assertEqual(list((self.root / "dist").iterdir()), [destination])

    def test_unknown_agent_has_no_output(self):
        with self.assertRaisesRegex(ValueError, "Unsupported agent"):
            build_package(self.root, "another-agent")
        self.assertFalse((self.root / "dist").exists())

    def test_catalog_rejects_path_traversal_and_duplicates(self):
        for skills in (["../outside"], ["binary-patch-engineering"] * 2):
            with self.subTest(skills=skills):
                self.edit_catalog(skills=skills)
                with self.assertRaises(ValueError):
                    validate_repository(self.root)

    def test_missing_resource_rejects_build_before_touching_output(self):
        destination = build_package(self.root, "codex")
        original = (destination / "re-skills/plugin.json").read_bytes()
        reference = self.root / "skills/ghidra-re-investigation/references/mcp-connection.md"
        reference.unlink()
        with self.assertRaisesRegex(ValueError, "Broken or escaping local link"):
            build_package(self.root, "codex", replace=True)
        self.assertEqual((destination / "re-skills/plugin.json").read_bytes(), original)

    def test_escaping_reference_is_rejected(self):
        skill = self.root / "skills/binary-patch-engineering/SKILL.md"
        with skill.open("a", encoding="utf-8") as stream:
            stream.write("\n[external local file](../../re-skills.json)\n")
        with self.assertRaisesRegex(ValueError, "escaping local link"):
            validate_repository(self.root)

    def test_cli_works_from_another_working_directory(self):
        script = self.root / "scripts/re_skills.py"
        for arguments in (["validate"], ["build", "--agent", "codex"]):
            result = subprocess.run(
                [sys.executable, str(script), *arguments],
                cwd=self.root / "adapters",
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
