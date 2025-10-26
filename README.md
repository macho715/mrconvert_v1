# mrconvert_v1 - Document Conversion & Ontology Framework

## 프로젝트 개요

MACHO-GPT 시스템을 위한 문서 변환 및 온톨로지 프레임워크입니다. WhatsApp 대화, Excel 파일, Markdown 문서를 기계 읽기 가능한 형식으로 변환하고, 물류 및 화물 운송 관련 온톨로지를 체계적으로 관리합니다.

## 📖 주요 문서

### 시스템 아키텍처
- [간단 아키텍처 다이어그램](docs/m.md) - ASCII + Mermaid 5계층 시각화
- [전체 시스템 설계 보고서](docs/HVDC_System_Architecture.md) - Protégé 통합 풀스택 MVP

### 온톨로지 문서
- [온톨로지 인덱스](docs/ontology/README.md)
  - Core: 8개 핵심 온톨로지 + 4개 통합 문서
  - Extended: 15개 확장 온톨로지
  - Material Handling: 6개 개별 + 2개 통합

### 가이드
- [프로젝트 문서 인덱스](docs/00_PROJECT_INDEX.md) - 모든 문서 통합 인덱스
- [시스템 아키텍처 가이드](docs/guides/SYSTEM_ARCHITECTURE_FINAL.md)
- [설정 가이드](docs/guides/CONFIGURATION_GUIDE.md)
- [사용자 가이드](docs/guides/USER_GUIDE.md)

---

## 프로젝트 구조

### 📚 문서 (`docs/`)
- `ontology/` - 표준화된 온톨로지 문서 (Core 8 + Extended 15 + Consolidated)
- `original/` - 원본 온톨로지 문서 보관
- `guides/` - 설정 및 사용자 가이드
- `converted/` - 변환된 PDF 문서

### 📁 데이터 (`data/`)
- `whatsapp/` - WhatsApp 대화 로그
- `excel/` - Excel 원본 파일
- `csv/` - CSV 데이터
- `reference/` - 참조 데이터 (요율표, 매핑 등)
  - `rates/` - 요율 데이터 (항공, 컨테이너, 내륙 운송 등)
  - `mappings/` - 매핑 데이터 (Lane Map, OD Mapping 등)

### 📤 출력 (`output/`)
- `whatsapp/` - WhatsApp 변환 결과 (JSON)
- `excel/` - Excel 변환 결과 (JSON, CSV)
- `machine_readable/` - 머신러더블 텍스트 문서
- `integrated/` - 통합 데이터베이스

### 🗄️ 보관 (`archive/`)
- `legacy_ontology/` - 구버전 온톨로지 폴더들
- `duplicate_whatsapp/` - 중복 WhatsApp 출력
- `scripts/` - 임시 스크립트

### 💻 소스 코드 (`src/`, `tests/`)
- Python 패키지 및 테스트 코드

## 주요 기능

### 1. 문서 변환
- **WhatsApp 대화**: JSON 형식으로 변환, 엔티티 추출
- **Excel 파일**: 구조화된 JSON/CSV로 변환
- **이미지 스캔(PNG/JPG/TIFF)**: OCR을 통해 텍스트/Markdown/JSON 출력 생성
- **Markdown 문서**: 머신러더블 텍스트로 변환

### 2. 온톨로지 관리
- **핵심 온톨로지**: 5개 주요 온톨로지 (물류 프레임워크, 비용 관리, 문서 검증, 벌크 화물, OCR 파이프라인)
- **확장 온톨로지**: 8개 확장 온톨로지 (포트 운영, 커뮤니케이션, 운영 관리, 규정 준수, 개발 도구)

### 3. 데이터 통합
- **통합 데이터베이스**: 모든 참조 데이터를 하나의 JSON으로 통합
- **스키마 정의**: 구조화된 데이터 스키마 제공
- **인덱스**: 문서 및 데이터 인덱스 관리

## Install (Python ≥ 3.13)
```bash
pip install -e ".[ocr]"
# or without OCR
pip install -e .
```

## CLI

### Text Extraction Mode (Default)
```bash
mrconvert INPUT_PATH --out OUT_DIR --format txt md json --tables csv --ocr auto --lang kor+eng
```

### Bidirectional Conversion Mode
```bash
mrconvert INPUT_PATH --to-docx    # PDF → DOCX
mrconvert INPUT_PATH --to-pdf     # DOCX → PDF
```

### Examples

#### Text Extraction
```bash
# 1) Convert a single PDF to Markdown + JSON with tables as CSV
mrconvert sample.pdf --out out --format md json --tables csv

# 2) Bulk convert a folder, OCR when needed
mrconvert ./incoming --out ./out --format txt --ocr auto --lang kor+eng

# 3) Force OCR (e.g., scanned PDF)
mrconvert scan.pdf --out out --format txt --ocr force

# 3-b) OCR a scanned image (PNG/JPG)
mrconvert invoice.png --out out --format txt md --ocr auto
```

#### Bidirectional Conversion
```bash
# 4) Convert PDF to DOCX
mrconvert document.pdf --to-docx --out ./converted

# 5) Convert DOCX to PDF
mrconvert document.docx --to-pdf

# 6) Batch convert multiple files
mrconvert ./pdfs --to-docx --out ./docx_output
```

## Output
For `--format json`, schema:
```json
{
  "meta": {
    "source": "<path>",
  "type": "pdf|docx|image",
    "pages": 10,
    "parsed_at": "YYYY-MM-DDTHH:MM:SSZ",
    "ocr": {"used": true, "engine": "ocrmypdf|pytesseract|none", "lang": "kor+eng"}
  },
  "text": "...plain text...",
  "markdown": "...optional markdown...",
  "tables": [
    {"page": 1, "index": 0, "rows": [["A","B"],["1","2"]]}
  ]
}
```

## Notes
- **.doc** (legacy) not supported directly. Use LibreOffice to convert to .docx:
  `soffice --headless --convert-to docx file.doc`
- OCR quality depends on the engine and language packs installed.

MIT License.
