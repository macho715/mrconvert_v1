from __future__ import annotations

import json
from pathlib import Path

from mrconvert import cli, image_converter
from mrconvert.utils import OCRConfig, walk_inputs


def test_process_file_handles_image(monkeypatch, tmp_path):
    captured: dict[str, Path | OCRConfig] = {}

    def fake_extract_image(path: Path, ocr: OCRConfig | None = None):
        captured["path"] = path
        captured["ocr"] = ocr or OCRConfig()
        return {"meta": {"source": str(path)}, "text": "hello", "markdown": "hello", "tables": []}

    monkeypatch.setattr(image_converter, "extract_image", fake_extract_image)

    input_dir = tmp_path / "input"
    input_dir.mkdir()
    img_path = input_dir / "sample.png"
    img_path.write_bytes(b"fake")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    cli._process_file(
        img_path,
        out_dir,
        formats=["txt", "json"],
        tables="none",
        keep_layout=False,
        ocr_mode="auto",
        lang="eng",
    )

    assert captured["path"] == img_path
    assert isinstance(captured["ocr"], OCRConfig)

    txt_output = out_dir / "sample.txt"
    json_output = out_dir / "sample.json"

    assert txt_output.read_text(encoding="utf-8") == "hello"
    assert json.loads(json_output.read_text(encoding="utf-8"))["text"] == "hello"


def test_extract_image_without_pillow(monkeypatch, tmp_path):
    monkeypatch.setattr(image_converter, "Image", None)

    result = image_converter.extract_image(tmp_path / "missing.png")

    assert result["text"] == ""
    assert result["markdown"] == ""
    assert result["meta"]["type"] == "image"


def test_walk_inputs_collects_images(tmp_path):
    img_path = tmp_path / "scan.jpg"
    img_path.write_bytes(b"fake")

    collected = list(walk_inputs(tmp_path))

    assert img_path in collected
