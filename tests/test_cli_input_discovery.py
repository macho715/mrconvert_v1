from __future__ import annotations

from pathlib import Path
from typing import List

from mrconvert.cli import run


def _create_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("sample", encoding="utf-8")


def test_excel_mode_directory_filters_to_spreadsheets(tmp_path, monkeypatch):
    input_dir = tmp_path / "inputs"
    excel_paths = [
        input_dir / "sheet1.xlsx",
        input_dir / "nested" / "sheet2.xls",
    ]
    other_paths = [
        input_dir / "doc1.pdf",
        input_dir / "notes.txt",
    ]

    for path in excel_paths + other_paths:
        _create_file(path)

    captured: dict[str, List[Path]] = {}

    def fake_run_excel_conversion(
        files: List[Path],
        out_dir: Path,
        output_formats: List[str],
        validate_data: bool,
    ) -> int:
        captured["files"] = list(files)
        return 0

    monkeypatch.setattr("mrconvert.cli._run_excel_conversion", fake_run_excel_conversion)

    out_dir = tmp_path / "out"
    exit_code = run([str(input_dir), "--excel-to-json", "--out", str(out_dir)])

    assert exit_code == 0
    assert "files" in captured
    assert {p.resolve() for p in captured["files"]} == {p.resolve() for p in excel_paths}


def test_whatsapp_mode_directory_filters_to_text(tmp_path, monkeypatch):
    input_dir = tmp_path / "inputs"
    txt_paths = [
        input_dir / "chat1.txt",
        input_dir / "nested" / "chat2.txt",
    ]
    other_paths = [
        input_dir / "sheet.xlsx",
        input_dir / "document.pdf",
    ]

    for path in txt_paths + other_paths:
        _create_file(path)

    captured: dict[str, List[Path]] = {}

    def fake_run_whatsapp_conversion(
        files: List[Path],
        out_dir: Path,
        extract_entities: bool,
        entity_csv: str | None,
        validation_report: bool,
    ) -> int:
        captured["files"] = list(files)
        return 0

    monkeypatch.setattr("mrconvert.cli._run_whatsapp_conversion", fake_run_whatsapp_conversion)

    out_dir = tmp_path / "out"
    exit_code = run([str(input_dir), "--whatsapp-to-json", "--out", str(out_dir)])

    assert exit_code == 0
    assert "files" in captured
    assert {p.resolve() for p in captured["files"]} == {p.resolve() for p in txt_paths}
