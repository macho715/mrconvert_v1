#!/usr/bin/env python3
"""
PDF 구조 분석 스크립트
HVDC_Material Handling Workshop PDF를 분석하여 섹션 구조, 키워드, 테이블 등을 추출
"""

import json
import re
from pathlib import Path
from collections import Counter
from typing import Dict, List, Any

import pdfplumber


def extract_structure(pdf_path: Path) -> Dict[str, Any]:
    """PDF 구조 분석 및 메타데이터 추출"""
    structure = {
        "total_pages": 0,
        "sections": [],
        "keywords": Counter(),
        "tables_count": 0,
        "images_count": 0,
        "page_text_samples": [],
    }

    with pdfplumber.open(pdf_path) as pdf:
        structure["total_pages"] = len(pdf.pages)

        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                # 주요 키워드 추출
                keywords = extract_keywords(text)
                structure["keywords"].update(keywords)

                # 섹션 제목 추출 시도
                if is_section_title(text):
                    structure["sections"].append(
                        {
                            "title": extract_section_title(text),
                            "page": i,
                            "text_sample": text[:500],
                        }
                    )

                # 페이지 샘플 저장 (처음 5페이지만)
                if i <= 5:
                    structure["page_text_samples"].append(
                        {"page": i, "text": text[:1000]}
                    )

            # 테이블 추출
            tables = page.extract_tables()
            if tables:
                structure["tables_count"] += len(tables)
                structure["sections"].append(
                    {"page": i, "type": "table", "table_count": len(tables)}
                )

    # 키워드 상위 20개
    structure["top_keywords"] = dict(structure["keywords"].most_common(20))

    return structure


def extract_keywords(text: str) -> List[str]:
    """텍스트에서 주요 키워드 추출"""
    # Material Handling 관련 키워드
    keywords_pattern = re.compile(
        r"\b(equipment|crane|forklift|hoist|safety|procedure|standard|regulation|"
        r"capacity|load|lifting|handling|inspection|certification|hazard|ppe|"
        r"emergency|compliance|training|risk|operating|maintenance)\b",
        re.IGNORECASE,
    )
    return keywords_pattern.findall(text)


def is_section_title(page_text: str) -> bool:
    """페이지가 섹션 제목인지 판단"""
    # 섹션 제목 패턴: 대문자로 시작, 짧은 텍스트, 특정 형식
    lines = page_text.strip().split("\n")[:5]
    if len(lines) < 2:
        return False

    first_line = lines[0].strip()
    # 제목 가능성: 첫 줄이 대문자로 시작하고 특정 길이 범위
    return (
        len(first_line) < 100
        and first_line[0].isupper()
        and any(
            keyword in first_line.lower()
            for keyword in [
                "workshop",
                "handling",
                "equipment",
                "procedure",
                "safety",
                "standard",
            ]
        )
    )


def extract_section_title(page_text: str) -> str:
    """섹션 제목 추출"""
    lines = page_text.strip().split("\n")
    return lines[0].strip() if lines else "Unknown"


def main():
    pdf_path = Path("HVDC_Material Handling Workshop_(20241119_1).pdf")

    if not pdf_path.exists():
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return

    print(f"PDF 구조 분석 중: {pdf_path}")
    structure = extract_structure(pdf_path)

    # 결과 저장
    output_path = Path("pdf_structure_analysis.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)

    print(f"\n분석 완료!")
    print(f"총 페이지: {structure['total_pages']}")
    print(f"발견된 섹션: {len(structure['sections'])}")
    print(f"테이블 개수: {structure['tables_count']}")
    print(f"\n주요 키워드:")
    for keyword, count in structure["top_keywords"].items():
        print(f"  {keyword}: {count}")

    print(f"\n분석 결과 저장: {output_path}")


if __name__ == "__main__":
    main()
