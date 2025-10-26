#!/usr/bin/env python3
"""
추출된 섹션을 온톨로지 마크다운 형식으로 변환
"""

from pathlib import Path
from typing import Dict
import json


def create_ontology_document(section_name: str, section_text: str, tables: list) -> str:
    """온톨로지 표준 형식 마크다운 생성"""

    # 섹션 번호와 파일명 매핑
    section_mapping = {
        "1. Overview": ("2_EXT-08A", "hvdc-material-handling-overview"),
        "2. Customs Clearance": ("2_EXT-08B", "hvdc-material-handling-customs"),
        "3. Storage & Inland Transportation": (
            "2_EXT-08C",
            "hvdc-material-handling-storage",
        ),
        "4. Offshore marine Transportation": (
            "2_EXT-08D",
            "hvdc-material-handling-offshore",
        ),
        "5. Site Receiving": ("2_EXT-08E", "hvdc-material-handling-site-receiving"),
        "6. Material Handling (Transformer)": (
            "2_EXT-08F",
            "hvdc-material-handling-transformer",
        ),
    }

    # 섹션 명칭 정리
    display_name = section_name.replace("&", "and")
    file_id, file_slug = section_mapping.get(
        section_name, ("2_EXT-08X", "hvdc-material-handling")
    )

    # YAML Front Matter
    yaml_front_matter = f"""---
title: "HVDC Material Handling - {display_name}"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["{display_name.lower()}", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "{section_name}"
---
"""

    # 마크다운 본문
    markdown_content = f"""{yaml_front_matter}
# hvdc-material-handling-{file_id} · {file_id}

## Executive Summary

This document defines the ontology for **{display_name}** in the HVDC Material Handling Workshop. It covers the operational procedures, infrastructure, and safety requirements for logistics and material handling in the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

## Content Overview

### Source Material
- **Source**: HVDC Material Handling Workshop (19th November 2024)
- **Section**: {section_name}
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE

### Key Concepts
The material handling process involves multiple stages including customs clearance, storage, inland transportation, offshore marine transportation, site receiving, and specialized handling procedures.

## Document Structure

### Main Content

{format_section_text(section_text)}

### Data Tables

{format_tables(tables)}
"""

    return markdown_content


def format_section_text(text: str) -> str:
    """섹션 텍스트를 마크다운 형식으로 포맷팅"""
    lines = text.split("\n")
    formatted = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("--- Page"):
            continue
        if any(
            keyword in line.lower()
            for keyword in [
                "overview",
                "customs",
                "storage",
                "transportation",
                "receiving",
                "handling",
            ]
        ):
            formatted.append(f"### {line}\n")
        else:
            formatted.append(line)

    return "\n".join(formatted)


def format_tables(tables: list) -> str:
    """테이블을 마크다운 형식으로 변환"""
    if not tables:
        return "No tables in this section."

    formatted = []
    for i, table in enumerate(tables, 1):
        if not table or not any(table):
            continue

        formatted.append(f"#### Table {i}\n")
        formatted.append("```")

        for row in table:
            if row and any(row):
                formatted.append(" | ".join(str(cell) if cell else "" for cell in row))

        formatted.append("```\n")

    return "\n".join(formatted)


def main():
    temp_dir = Path("temp")
    output_dir = Path("docs/ontology/extended")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 섹션 파일 처리
    for txt_file in temp_dir.glob("section_*.txt"):
        section_name = txt_file.stem.replace("section_", "").replace("_", " ")
        print(f"Processing: {section_name}")

        # 텍스트 읽기
        with open(txt_file, "r", encoding="utf-8") as f:
            section_text = f.read()

        # 테이블 읽기
        tables_file = txt_file.parent / f"{txt_file.stem}_tables.json"
        tables = []
        if tables_file.exists():
            with open(tables_file, "r", encoding="utf-8") as f:
                tables = json.load(f)

        # 온톨로지 문서 생성
        markdown = create_ontology_document(section_name, section_text, tables)

        # 파일명 결정
        section_mapping = {
            "section_1._overview.txt": "2_EXT-08A-hvdc-material-handling-overview.md",
            "section_2._customs_clearance.txt": "2_EXT-08B-hvdc-material-handling-customs.md",
            "section_3._storage_and_inland_transportation.txt": "2_EXT-08C-hvdc-material-handling-storage.md",
            "section_4._offshore_marine_transportation.txt": "2_EXT-08D-hvdc-material-handling-offshore.md",
            "section_5._site_receiving.txt": "2_EXT-08E-hvdc-material-handling-site-receiving.md",
            "section_6._material_handling_(transformer).txt": "2_EXT-08F-hvdc-material-handling-transformer.md",
        }

        output_filename = section_mapping.get(txt_file.name, f"{txt_file.stem}.md")
        output_file = output_dir / output_filename

        # 파일 저장
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"  → {output_file}")

    print("\n변환 완료!")


if __name__ == "__main__":
    main()
