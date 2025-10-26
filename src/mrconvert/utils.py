from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Dict, Any


def _normalize_suffixes(suffixes: Iterable[str] | None) -> set[str]:
    normalized: set[str] = set()
    if suffixes is None:
        return {".pdf", ".docx"}

    for suffix in suffixes:
        cleaned = suffix.strip().lower()
        if not cleaned:
            continue
        if not cleaned.startswith("."):
            cleaned = f".{cleaned}"
        normalized.add(cleaned)

    return normalized

def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-{2,}", "-", name).strip("-")
    return name or "file"

def write_text(out_dir: Path, stem: str, content: str, ext: str) -> Path:
    p = out_dir / f"{slugify(stem)}.{ext}"
    p.write_text(content, encoding="utf-8")
    return p

def write_json(out_dir: Path, stem: str, data: Dict[str, Any]) -> Path:
    p = out_dir / f"{slugify(stem)}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

@dataclass
class OCRConfig:
    mode: str = "auto"  # "off" | "auto" | "force"
    lang: str | None = None  # e.g. "kor+eng"

def is_pdf(path: Path) -> bool:
    return path.suffix.lower() == ".pdf"

def is_docx(path: Path) -> bool:
    return path.suffix.lower() == ".docx"

def walk_inputs(input_path: Path, suffixes: Iterable[str] | None = None) -> Iterable[Path]:
    normalized_suffixes = _normalize_suffixes(suffixes)

    def matches(path: Path) -> bool:
        suffix = path.suffix.lower()
        if suffixes is None:
            return suffix in normalized_suffixes
        if not normalized_suffixes:
            return False
        return suffix in normalized_suffixes

    if input_path.is_file():
        if matches(input_path):
            yield input_path
        return

    for p in input_path.rglob("*"):
        if p.is_file() and matches(p):
            yield p
