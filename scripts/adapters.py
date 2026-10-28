"""Host-specific packaging; shared skill content stays in skills/."""

from pathlib import Path
import json
import shutil

import yaml


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


class CodexAdapter:
    def validate(self, root: Path, catalog: dict) -> None:
        template = json.loads((root / "adapters/codex/plugin.json").read_text(encoding="utf-8"))
        if set(template) != {"$schema", "extensions"}:
            raise ValueError("Codex template must contain only $schema and extensions")
        interface = template["extensions"]["com.openai"]["interface"]
        for field in ("displayName", "shortDescription"):
            if not isinstance(interface.get(field), str) or not interface[field].strip():
                raise ValueError(f"Missing Codex interface field: {field}")
        for skill in catalog["skills"]:
            metadata_path = root / "adapters/codex/skills" / skill / "openai.yaml"
            metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
            if not isinstance(metadata, dict) or not isinstance(metadata.get("interface"), dict):
                raise ValueError(f"Invalid Codex metadata: {skill}")
            interface = metadata["interface"]
            for field in ("display_name", "short_description", "default_prompt"):
                if not isinstance(interface.get(field), str) or not interface[field].strip():
                    raise ValueError(f"Missing {field} in Codex metadata: {skill}")
            if f"${skill}" not in interface["default_prompt"]:
                raise ValueError(f"Codex prompt must reference ${skill}")

    def build(self, root: Path, catalog: dict, destination: Path) -> None:
        plugin = destination / catalog["name"]
        plugin.mkdir()
        for skill in catalog["skills"]:
            target = plugin / "skills" / skill
            shutil.copytree(root / "skills" / skill, target)
            metadata = target / "agents"
            metadata.mkdir()
            shutil.copyfile(
                root / "adapters/codex/skills" / skill / "openai.yaml",
                metadata / "openai.yaml",
            )

        template = json.loads((root / "adapters/codex/plugin.json").read_text(encoding="utf-8"))
        manifest = {key: catalog[key] for key in ("name", "version", "description")}
        manifest.update(template)
        write_json(plugin / "plugin.json", manifest)
        write_json(
            destination / ".agents/plugins/marketplace.json",
            {
                "name": f"{catalog['name']}-local",
                "interface": {"displayName": "RE Skills — local"},
                "plugins": [
                    {
                        "name": catalog["name"],
                        "source": {"source": "local", "path": f"./{catalog['name']}"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Developer Tools",
                    }
                ],
            },
        )


# Add an adapter only after implementing its packaging and validation contracts.
ADAPTERS = {"codex": CodexAdapter()}
