from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from rich.console import Console
from rich.progress import track

from . import (
    pdf_converter,
    docx_converter,
    bidirectional,
    whatsapp_parser,
    image_converter,
)
from .utils import ensure_dir, write_text, write_json, walk_inputs, OCRConfig, IMAGE_SUFFIXES

console = Console()


def _process_file(
    path: Path,
    out_dir: Path,
    formats: List[str],
    tables: str,
    keep_layout: bool,
    ocr_mode: str,
    lang: str | None,
):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        data = pdf_converter.extract_pdf(
            path, keep_layout=keep_layout, ocr=OCRConfig(mode=ocr_mode, lang=lang)
        )
    elif suffix == ".docx":
        data = docx_converter.extract_docx(path)
    elif suffix in IMAGE_SUFFIXES:
        data = image_converter.extract_image(
            path, ocr=OCRConfig(mode=ocr_mode, lang=lang)
        )
    else:
        console.print(f"[yellow]Skip unsupported file:[/] {path}")
        return

    stem = path.stem
    # Write formats
    if "txt" in formats:
        write_text(out_dir, stem, data.get("text") or "", "txt")
    if "md" in formats:
        md = data.get("markdown")
        if md is None:
            # fallback to text if no markdown available (e.g., PDF)
            md = data.get("text") or ""
        write_text(out_dir, stem, md, "md")
    if "json" in formats:
        write_json(out_dir, stem, data)

    # Tables
    if tables in {"csv", "json"} and data.get("tables"):
        import csv, json as _json

        for t in data["tables"]:
            page = t.get("page")
            idx = t.get("index")
            rows = t.get("rows") or []
            if tables == "csv":
                csv_path = out_dir / f"{stem}.table-{page or 'NA'}-{idx or 0}.csv"
                with csv_path.open("w", newline="", encoding="utf-8") as f:
                    w = csv.writer(f)
                    w.writerows(rows)
            else:
                json_path = out_dir / f"{stem}.table-{page or 'NA'}-{idx or 0}.json"
                json_path.write_text(
                    _json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8"
                )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mrconvert",
        description=(
            "Convert PDF/DOCX/image files to machine-readable TXT/MD/JSON or bidirectional "
            "PDF↔DOCX conversion."
        ),
    )
    p.add_argument("input", help="File or folder containing .pdf/.docx/.png/.jpg")
    p.add_argument(
        "--out",
        dest="out",
        default="./mr_out",
        help="Output directory (default: ./mr_out)",
    )

    # Text extraction mode (existing)
    text_group = p.add_argument_group("Text extraction mode")
    text_group.add_argument(
        "--format",
        dest="formats",
        nargs="+",
        choices=["txt", "md", "json"],
        default=["txt"],
        help="Output formats",
    )
    text_group.add_argument(
        "--tables",
        dest="tables",
        choices=["none", "csv", "json"],
        default="csv",
        help="Export detected tables",
    )
    text_group.add_argument(
        "--keep-layout",
        action="store_true",
        help="Preserve approximate layout for PDF text extraction",
    )
    text_group.add_argument(
        "--ocr",
        choices=["off", "auto", "force"],
        default="auto",
        help="OCR policy for PDFs",
    )
    text_group.add_argument(
        "--lang", default=None, help="OCR language (e.g., 'kor+eng')"
    )

    # Bidirectional conversion mode (new)
    convert_group = p.add_argument_group("Bidirectional conversion mode")
    convert_group.add_argument(
        "--to-docx", action="store_true", help="Convert PDF to DOCX"
    )
    convert_group.add_argument(
        "--to-pdf", action="store_true", help="Convert DOCX to PDF"
    )

    # WhatsApp conversion mode (new)
    whatsapp_group = p.add_argument_group("WhatsApp conversion mode")
    whatsapp_group.add_argument(
        "--whatsapp-to-json", action="store_true", help="Convert WhatsApp chat to JSON"
    )
    whatsapp_group.add_argument(
        "--extract-entities",
        action="store_true",
        help="Extract logistics entities from WhatsApp chat",
    )
    whatsapp_group.add_argument(
        "--entity-csv",
        help="Path to CSV file containing entity definitions for enhanced extraction",
    )
    whatsapp_group.add_argument(
        "--validation-report",
        action="store_true",
        help="Generate validation report comparing detected entities with CSV data",
    )

    # Excel conversion mode
    excel_group = p.add_argument_group("Excel conversion mode")
    excel_group.add_argument(
        "--excel-to-json",
        action="store_true",
        help="Convert Excel file to machine-readable formats (JSON, CSV, Markdown)",
    )
    excel_group.add_argument(
        "--output-formats",
        nargs="+",
        choices=["json", "csv", "md"],
        default=["json", "csv", "md"],
        help="Output formats for Excel conversion (default: json csv md)",
    )
    excel_group.add_argument(
        "--validate-data",
        action="store_true",
        help="Validate Excel data and generate validation report",
    )

    return p


def run(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    args = build_parser().parse_args(argv)

    # Validate arguments
    if args.to_docx and args.to_pdf:
        console.print("[red]Error:[/] Cannot use both --to-docx and --to-pdf")
        raise SystemExit(1)

    if (args.to_docx or args.to_pdf) and (
        len(args.formats) > 1
        or "md" in args.formats
        or "json" in args.formats
        or args.tables != "csv"
    ):
        console.print(
            "[red]Error:[/] --to-docx/--to-pdf cannot be used with --format/--tables options"
        )
        raise SystemExit(1)

    if args.whatsapp_to_json and (args.to_docx or args.to_pdf):
        console.print(
            "[red]Error:[/] --whatsapp-to-json cannot be used with --to-docx/--to-pdf"
        )
        raise SystemExit(1)

    in_path = Path(args.input).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    ensure_dir(out_dir)

    files = list(walk_inputs(in_path))
    if not files:
        console.print(f"[red]No files found under:[/] {in_path}")
        return 2

    # Check if we're in Excel conversion mode
    if args.excel_to_json:
        return _run_excel_conversion(
            files,
            out_dir,
            args.output_formats,
            args.validate_data,
        )
    # Check if we're in WhatsApp conversion mode
    elif args.whatsapp_to_json:
        return _run_whatsapp_conversion(
            files,
            out_dir,
            args.extract_entities,
            args.entity_csv,
            args.validation_report,
        )
    # Check if we're in bidirectional conversion mode
    elif args.to_docx or args.to_pdf:
        return _run_bidirectional_conversion(files, out_dir, args.to_docx, args.to_pdf)
    else:
        return _run_text_extraction(files, out_dir, args)


def _run_bidirectional_conversion(
    files: List[Path], out_dir: Path, to_docx: bool, to_pdf: bool
) -> int:
    """Run bidirectional PDF↔DOCX conversion"""
    console.print(
        f"[bold]mrconvert[/] · Bidirectional conversion · {len(files)} file(s) → {out_dir}"
    )

    for f in track(files, description="Converting"):
        try:
            if to_docx and f.suffix.lower() == ".pdf":
                dst = out_dir / f"{f.stem}.docx"
                result = bidirectional.pdf_to_docx(f, dst)
                console.print(
                    f"[green][{result.engine}][/] {f.name} → {result.output.name}"
                )
            elif to_pdf and f.suffix.lower() == ".docx":
                dst = out_dir / f"{f.stem}.pdf"
                result = bidirectional.docx_to_pdf(f, dst)
                console.print(
                    f"[green][{result.engine}][/] {f.name} → {result.output.name}"
                )
            else:
                console.print(
                    f"[yellow]Skip:[/] {f.name} (wrong file type for conversion)"
                )
        except Exception as e:
            console.print(f"[red]Error:[/] {f} — {e}")

    console.print("[green]Done.[/]")
    return 0


def _run_whatsapp_conversion(
    files: List[Path],
    out_dir: Path,
    extract_entities: bool,
    entity_csv: str = None,
    validation_report: bool = False,
) -> int:
    """Run WhatsApp to JSON conversion mode"""
    console.print(
        f"[bold]mrconvert[/] · WhatsApp to JSON conversion · {len(files)} file(s) → {out_dir}"
    )

    parser = whatsapp_parser.WhatsAppParser(entity_csv)

    for f in track(files, description="Converting"):
        try:
            if f.suffix.lower() != ".txt":
                console.print(f"[yellow]Skip:[/] {f.name} (not a .txt file)")
                continue

            console.print(f"[blue]Processing:[/] {f.name}")

            # Parse WhatsApp file
            parsed_data = parser.parse_file(str(f))

            # Save main conversation JSON
            output_path = out_dir / f"{f.stem}_conversation.json"
            parser.save_to_json(parsed_data, str(output_path))
            console.print(f"[green]✓[/] {output_path.name}")

            # Extract entities if requested
            if extract_entities:
                entities_data = parser.extract_entities_only(str(f))
                entities_path = out_dir / f"{f.stem}_entities.json"
                parser.save_to_json(entities_data, str(entities_path))
                console.print(f"[green]✓[/] {entities_path.name}")

                # Save statistics separately
                stats_data = {
                    "conversation_info": parsed_data["conversation"],
                    "statistics": parsed_data["conversation"]["statistics"],
                }
                stats_path = out_dir / f"{f.stem}_statistics.json"
                parser.save_to_json(stats_data, str(stats_path))
                console.print(f"[green]✓[/] {stats_path.name}")

        except Exception as e:
            console.print(f"[red]Error:[/] {f} — {e}")

    console.print("[green]Done.[/]")
    return 0


def _run_excel_conversion(
    files: List[Path], out_dir: Path, output_formats: List[str], validate_data: bool
) -> int:
    """Run Excel to JSON/CSV/Markdown conversion mode"""
    console.print("[blue]Excel 변환 모드 시작[/]")

    try:
        from . import excel_converter
    except ModuleNotFoundError as exc:
        console.print(
            "[red]Error:[/] Excel conversion requires optional dependencies (pandas/openpyxl)."
        )
        console.print(f"[red]Detail:[/] {exc}")
        return 2

    converter = excel_converter.ExcelConverter()

    for file_path in track(files, description="Converting"):
        if not file_path.suffix.lower() in [".xlsx", ".xls"]:
            console.print(f"[yellow]Excel 파일이 아닙니다:[/] {file_path}")
            continue

        try:
            console.print(f"Processing: {file_path.name}")

            # Excel 파일 변환
            converted_files = converter.convert_excel_file(
                str(file_path),
                str(out_dir),
                formats=output_formats,
                validate=validate_data,
            )

            # 변환 결과 출력
            for format_type, output_path in converted_files.items():
                console.print(f"✓ {Path(output_path).name}")

        except Exception as e:
            console.print(f"[red]Excel 파일 변환 실패:[/] {file_path.name} - {e}")
            continue

    console.print("[green]Excel 변환 완료[/]")
    return 0


def _run_text_extraction(files: List[Path], out_dir: Path, args) -> int:
    """Run text extraction mode (existing functionality)"""
    console.print(
        f"[bold]mrconvert[/] · Text extraction · {len(files)} file(s) → {out_dir}"
    )

    for f in track(files, description="Converting"):
        try:
            _process_file(
                f,
                out_dir,
                formats=args.formats,
                tables=args.tables,
                keep_layout=args.keep_layout,
                ocr_mode=args.ocr,
                lang=args.lang,
            )
        except Exception as e:
            console.print(f"[red]Error:[/] {f} — {e}")

    console.print("[green]Done.[/]")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
