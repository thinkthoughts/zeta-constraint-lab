from __future__ import annotations

import json
from pathlib import Path


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: str | Path, data: dict):
    path = Path(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
