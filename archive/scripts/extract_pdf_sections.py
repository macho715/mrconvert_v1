#!/usr/bin/env python3
"""
PDF 섹션별 내용 추출 스크립트
Material Handling Workshop PDF를 각 섹션별로 추출
"""

import json
from pathlib import Path
from typing import List, Dict

import pdfplumber


# INDEX 기반 섹션 매핑 (PDF 2페이지 참조)
SECTION_PAGES = {
    "1. Overview": (4, 7),  # 페이지 범위 추정
    "2. Customs Clearance": (8, 12),
    "3. Storage & Inland Transportation": (13, 18),
    "4. Offshore marine Transportation": (19, 25),
    "5. Site Receiving": (26, 32),
    "6. Material Handling (Transformer)": (33, 43),
}


def extract_page_text(pdf_path: Path, page_num: int) -> Dict:
    """특정 페이지의 텍스트와 테이블 추출"""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]  # 0-based index
        text = page.extract_text()
        tables = page.extract_tables()

        return {
            "page": page_num,
            "text": text,
            "tables": tables,
            "table_count": len(tables) if tables else 0,
        }


def extract_section(pdf_path: Path, start_page: int, end_page: int) -> Dict:
    """특정 페이지 범위의 내용 추출"""
    section_data = {
        "start_page": start_page,
        "end_page": end_page,
        "pages": [],
        "all_tables": [],
        "text": "",
    }

    for page_num in range(start_page, end_page + 1):
        page_data = extract_page_text(pdf_path, page_num)
        section_data["pages"].append(
            {"page": page_data["page"], "text": page_data["text"]}
        )
        section_data["text"] += f"\n\n--- Page {page_num} ---\n\n{page_data['text']}"
        section_data["all_tables"].extend(page_data["tables"])

    return section_data


def main():
    pdf_path = Path("HVDC_Material Handling Workshop_(20241119_1).pdf")

    if not pdf_path.exists():
        print(f"PDF 파일을 찾을 수 없습니다: {pdf_path}")
        return

    # 임시 디렉토리 생성
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)

    # 각 섹션 추출
    for section_name, (start, end) in SECTION_PAGES.items():
        print(f"\nExtracting: {section_name} (Pages {start}-{end})")
        section_data = extract_section(pdf_path, start, end)

        # 텍스트 파일 저장
        section_filename = section_name.lower().replace(" ", "_").replace("&", "and")
        section_file = temp_dir / f"section_{section_filename}.txt"
        with open(section_file, "w", encoding="utf-8") as f:
            f.write(section_data["text"])

        # 테이블 저장
        if section_data["all_tables"]:
            tables_file = temp_dir / f"section_{section_filename}_tables.json"
            with open(tables_file, "w", encoding="utf-8") as f:
                json.dump(section_data["all_tables"], f, indent=2, ensure_ascii=False)

        print(f"  → {section_file}")
        print(f"  → Tables: {len(section_data['all_tables'])} tables extracted")

    print("\n추출 완료!")


if __name__ == "__main__":
    main()
