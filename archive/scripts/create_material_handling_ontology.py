#!/usr/bin/env python3
"""
Material Handling Workshop 온톨로지 마크다운 완전체 생성
RDF/OWL 클래스, 프로퍼티, SHACL, SPARQL 등 온톨로지 요소 포함
"""

from pathlib import Path
from typing import Dict
import json


# 섹션별 온톨로지 메타데이터
SECTION_METADATA = {
    "1. Overview": {
        "id": "2_EXT-08A",
        "slug": "hvdc-material-handling-overview",
        "title": "Material Handling Overview",
        "key_classes": ["LogisticsFlow", "Port", "StorageLocation", "Project"],
        "focus": "Overall logistics workflow and port information",
    },
    "2. Customs Clearance": {
        "id": "2_EXT-08B",
        "slug": "hvdc-material-handling-customs",
        "title": "Customs Clearance",
        "key_classes": [
            "CustomsDocument",
            "AttestationInvoice",
            "BLEndorsement",
            "CustomsDeclaration",
        ],
        "focus": "Customs clearance procedures and documentation",
    },
    "3. Storage & Inland Transportation": {
        "id": "2_EXT-08C",
        "slug": "hvdc-material-handling-storage",
        "title": "Storage & Inland Transportation",
        "key_classes": [
            "StorageLocation",
            "IndoorWarehouse",
            "OutdoorYard",
            "InlandTransport",
        ],
        "focus": "Material storage standards and inland transportation",
    },
    "4. Offshore marine Transportation": {
        "id": "2_EXT-08D",
        "slug": "hvdc-material-handling-offshore",
        "title": "Offshore Marine Transportation",
        "key_classes": ["LCT", "MarineTransport", "OffshoreRoute", "Barge"],
        "focus": "Offshore marine transportation procedures",
    },
    "5. Site Receiving": {
        "id": "2_EXT-08E",
        "slug": "hvdc-material-handling-site-receiving",
        "title": "Site Receiving",
        "key_classes": [
            "MaterialReceiving",
            "Inspection",
            "MRR",
            "MaterialReceivingInspection",
        ],
        "focus": "Site receiving and inspection procedures",
    },
    "6. Material Handling (Transformer)": {
        "id": "2_EXT-08F",
        "slug": "hvdc-material-handling-transformer",
        "title": "Material Handling - Transformer",
        "key_classes": [
            "Transformer",
            "LiftingEquipment",
            "Crane",
            "HandlingProcedure",
            "SafetyCheck",
        ],
        "focus": "Specialized transformer handling and safety procedures",
    },
}


def create_complete_ontology_document(
    section_name: str, section_text: str, tables: list
) -> str:
    """온톨로지 완전체 문서 생성"""

    meta = SECTION_METADATA.get(section_name, SECTION_METADATA["1. Overview"])

    yaml_front_matter = f"""---
title: "HVDC Material Handling - {meta['title']}"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "{section_name}"
---
"""

    # 클래스 정의 생성
    classes_section = generate_classes_section(meta["key_classes"])

    # 프로퍼티 정의 생성
    properties_section = generate_properties_section(meta["key_classes"])

    # 예시 생성
    examples_section = generate_examples_section(meta["key_classes"])

    # 쿼리 생성
    queries_section = generate_queries_section(meta["key_classes"])

    markdown = f"""{yaml_front_matter}
# hvdc-material-handling-{meta['slug']} · {meta['id']}

## Executive Summary

This document defines the ontology for **{meta['title']}** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
{meta['focus']}

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
{generate_class_table(meta['key_classes'])}

## How it works (flow)

{generate_workflow_description(section_name)}

---

## Part 1: Domain Ontology

### Core Classes

\```turtle
{classes_section}
\```

### Data Properties

\```turtle
{properties_section}
\```

### Object Properties

\```turtle
# Example object properties
mh:locatedAt a owl:ObjectProperty ;
    rdfs:label "located at" ;
    rdfs:domain mh:Material ;
    rdfs:range mh:StorageLocation .
\```

---

## Part 2: Constraints & Validation

### SHACL Constraints

\```turtle
{generate_shacl_constraints(meta['key_classes'])}
\```

---

## Part 3: Examples & Queries

### JSON-LD Examples

\```json
{examples_section}
\```

### SPARQL Queries

\```sparql
{queries_section}
\```

---

## Original Content

### Main Text Content

{format_main_content(section_text)}

### Tables and Data

{format_tables_proper(tables)}

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
"""

    return markdown


def generate_class_table(key_classes: list) -> str:
    """클래스 테이블 생성"""
    rows = []
    for cls in key_classes[:5]:  # 최대 5개만
        rows.append(f"| mh:{cls} | (property list) | relatesTo → | (source) | status |")
    if len(key_classes) > 5:
        rows.append(f"| ... | ({len(key_classes)-5} more classes) | ... | ... | ... |")
    return "\n".join(rows)


def generate_classes_section(key_classes: list) -> str:
    """Turtle 클래스 정의 생성"""
    classes = []
    for cls in key_classes:
        classes.append(
            f"""mh:{cls} a owl:Class ;
    rdfs:label "{cls}" ;
    rdfs:comment "Class representing {cls.lower()}" ."""
        )
    return "\n\n".join(classes)


def generate_properties_section(key_classes: list) -> str:
    """데이터 프로퍼티 생성"""
    props = []
    for cls in key_classes[:3]:
        props.append(
            f"""mh:has_{cls.lower()}Id a owl:DatatypeProperty ;
    rdfs:label "has {cls.lower()} ID" ;
    rdfs:domain mh:{cls} ;
    rdfs:range xsd:string .
"""
        )
    return "\n".join(props)


def generate_shacl_constraints(key_classes: list) -> str:
    """SHACL 제약 생성"""
    constraints = []
    for cls in key_classes[:2]:
        constraints.append(
            f"""mh:{cls}Shape a sh:NodeShape ;
    sh:targetClass mh:{cls} ;
    sh:property [
        sh:path mh:has_{cls.lower()}Id ;
        sh:minCount 1 ;
        sh:message "{cls} must have ID"
    ] ."""
        )
    return "\n\n".join(constraints)


def generate_examples_section(key_classes: list) -> str:
    """JSON-LD 예시 생성"""
    first_class = key_classes[0] if key_classes else "Material"
    example = {
        "@context": {
            "mh": "https://hvdc-project.com/ontology/material-handling/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        },
        "@id": f"mh:{first_class.lower()}-001",
        "@type": f"mh:{first_class}",
        f"mh:has_{first_class.lower()}Id": "MH-001",
        "mh:hasDescription": f"Example {first_class.lower()}",
    }
    import json

    return json.dumps(example, indent=2)


def generate_queries_section(key_classes: list) -> str:
    """SPARQL 쿼리 생성"""
    first_class = key_classes[0] if key_classes else "Material"
    query = f"""PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?{first_class.lower()} ?description WHERE {{
    ?{first_class.lower()} a mh:{first_class} .
    ?{first_class.lower()} mh:hasDescription ?description .
}}
LIMIT 10"""
    return query


def generate_workflow_description(section_name: str) -> str:
    """워크플로우 설명 생성"""
    descriptions = {
        "1. Overview": """1. **Import Planning**: Materials ordered and shipped to UAE ports
2. **Port Handling**: Heavy equipment at Zayed Port, containers at Khalifa Port
3. **Storage**: Materials stored in designated warehouses or outdoor yards
4. **Offshore Transport**: Special materials transported via LCT to offshore sites
5. **Site Receiving**: Materials received and inspected at on-site locations""",
        "2. Customs Clearance": """1. **Document Preparation**: BL endorsement, attestation invoice preparation
2. **Customs Declaration**: Filing customs documents with ADNOC/ADOPT code
3. **Duty Payment**: Contractor pays duty and applies for reimbursement
4. **Clearance Completion**: Status shared with ADOPT for information""",
    }
    return descriptions.get(
        section_name, "Material handling workflow for HVDC project operations."
    )


def format_main_content(text: str) -> str:
    """메인 컨텐츠 포맷팅"""
    # 간단한 포맷팅
    lines = text.split("\n")
    formatted = []
    skip_next = False

    for line in lines:
        if "--- Page" in line:
            skip_next = True
            continue
        if skip_next and not line.strip():
            skip_next = False
            continue

        line = line.strip()
        if not line:
            continue

        # 주요 제목 확인
        if any(
            x in line
            for x in [
                "1.",
                "2.",
                "3.",
                "4.",
                "5.",
                "6.",
                "Overview",
                "Customs",
                "Storage",
                "Transportation",
                "Receiving",
                "Handling",
            ]
        ):
            formatted.append(f"### {line}\n")
        else:
            formatted.append(line)

    return "\n".join(formatted[:100])  # 최대 100줄


def format_tables_proper(tables: list) -> str:
    """테이블을 적절한 마크다운 형식으로"""
    if not tables:
        return "No structured tables in this section."

    formatted = []
    for i, table in enumerate(tables[:5], 1):  # 최대 5개 테이블만
        if not table or not any(table):
            continue

        formatted.append(f"### Table {i}\n")

        # 첫 번째 행을 헤더로
        if table and len(table) > 0:
            header = table[0]
            if header and any(header):
                formatted.append(
                    "| " + " | ".join(str(cell or "") for cell in header) + " |"
                )
                formatted.append("| " + " | ".join(["---"] * len(header)) + " |")

                # 나머지 행
                for row in table[1:]:
                    if row and any(row):
                        formatted.append(
                            "| " + " | ".join(str(cell or "") for cell in row) + " |"
                        )

        formatted.append("")  # 빈 줄

    if len(tables) > 5:
        formatted.append(f"\n*... and {len(tables)-5} more tables*")

    return "\n".join(formatted)


def main():
    temp_dir = Path("temp")
    output_dir = Path("docs/ontology/extended")

    # 섹션 파일 처리
    for txt_file in temp_dir.glob("section_*.txt"):
        section_name = (
            txt_file.stem.replace("section_", "").replace("_", " ").replace(".txt", "")
        )
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
        section_key = next(
            (
                k
                for k in SECTION_METADATA.keys()
                if k.lower().replace("&", "and") in section_name.lower()
            ),
            "1. Overview",
        )
        markdown = create_complete_ontology_document(section_key, section_text, tables)

        # 파일명 결정
        meta = SECTION_METADATA[section_key]
        output_filename = f"{meta['id']}-hvdc-material-handling-{meta['slug']}.md"
        output_file = output_dir / output_filename

        # 파일 저장
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"  → {output_file}")

    print("\n온톨로지 변환 완료!")


if __name__ == "__main__":
    main()
