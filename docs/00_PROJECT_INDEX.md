# HVDC Project Documentation Index

이 문서는 HVDC 프로젝트의 모든 문서를 체계적으로 정리한 마스터 인덱스입니다.

## 1. 시스템 아키텍처

### 간단 아키텍처 다이어그램
- **[m.md](m.md)** - ASCII + Mermaid 5계층 시각화
  - 사용자 인터페이스
  - AI 인사이트 & 리포트 엔진
  - 지식 그래프 핵심 엔진
  - 데이터 수집 및 정제 계층
  - 원본 데이터 소스

### 전체 시스템 설계 보고서
- **[HVDC_System_Architecture.md](HVDC_System_Architecture.md)** - Protégé 통합 풀스택 MVP 설계
  - 개요 및 목적
  - 전체 시스템 아키텍처 다이어그램 (Mermaid)
  - 10단계별 상세 아키텍처
  - 핵심 데이터 흐름 예시
  - 기술 스택 요약
  - 구현 로드맵 (4주 MVP)
  - 기대 효과
  - 결론 및 다음 행동

---

## 2. 온톨로지 문서

### 온톨로지 메인 인덱스
- **[ontology/README.md](ontology/README.md)** - 온톨로지 문서 통합 인덱스

### Core Ontology (8개)
**개별 문서** (`ontology/core/`)
1. [hvdc-core-framework](ontology/core/1_CORE-01-hvdc-core-framework.md) - 핵심 프레임워크
2. [hvdc-infra-nodes](ontology/core/1_CORE-02-hvdc-infra-nodes.md) - 인프라 노드
3. [hvdc-warehouse-ops](ontology/core/1_CORE-03-hvdc-warehouse-ops.md) - 창고 운영
4. [hvdc-invoice-cost](ontology/core/1_CORE-04-hvdc-invoice-cost.md) - 송장 및 비용 관리
5. [hvdc-bulk-cargo-ops](ontology/core/1_CORE-05-hvdc-bulk-cargo-ops.md) - 벌크 화물 운영
6. [hvdc-doc-guardian](ontology/core/1_CORE-06-hvdc-doc-guardian.md) - 문서 가디언
7. [hvdc-ocr-pipeline](ontology/core/1_CORE-07-hvdc-ocr-pipeline.md) - OCR 파이프라인
8. [hvdc-flow-code-algorithm](ontology/core/1_CORE-08-flow-code.md) - Flow Code 알고리즘

**통합 문서** (`ontology/core_consolidated/`)
- [CONSOLIDATED-01](ontology/core_consolidated/CONSOLIDATED-01-framework-infra.md) - Framework + Infrastructure
- [CONSOLIDATED-02](ontology/core_consolidated/CONSOLIDATED-02-warehouse-flow.md) - Warehouse + Flow Code
- [CONSOLIDATED-03](ontology/core_consolidated/CONSOLIDATED-03-cost-bulk.md) - Cost Management + Bulk Cargo
- [CONSOLIDATED-04](ontology/core_consolidated/CONSOLIDATED-04-document-ocr.md) - Document Guardian + OCR Pipeline
- [Consolidated README](ontology/core_consolidated/README.md)

### Extended Ontology (15개)
**개별 문서** (`ontology/extended/`)
1. [hvdc-ofco-port-ops-en](ontology/extended/2_EXT-01-hvdc-ofco-port-ops-en.md) - OFCO 항만 운영 (영문)
2. [hvdc-ofco-port-ops-ko](ontology/extended/2_EXT-02-hvdc-ofco-port-ops-ko.md) - OFCO 항만 운영 (한글)
3. [hvdc-comm-email](ontology/extended/2_EXT-03-hvdc-comm-email.md) - 이메일 통신 시스템
4. [hvdc-comm-chat](ontology/extended/2_EXT-04-hvdc-comm-chat.md) - 채팅 통신 시스템
5. [hvdc-ops-management](ontology/extended/2_EXT-05-hvdc-ops-management.md) - 운영 관리
6. [hvdc-compliance-customs](ontology/extended/2_EXT-06-hvdc-compliance-customs.md) - 컴플라이언스 및 통관
7. [hvdc-dev-tools](ontology/extended/2_EXT-07-hvdc-dev-tools.md) - 개발 도구

**Material Handling (8개)**
- [08A-overview](ontology/extended/2_EXT-08A-hvdc-material-handling-overview.md) - 물자 취급 개요
- [08B-customs](ontology/extended/2_EXT-08B-hvdc-material-handling-customs.md) - 통관 절차
- [08C-storage](ontology/extended/2_EXT-08C-hvdc-material-handling-storage.md) - 저장 및 내륙 운송
- [08D-offshore](ontology/extended/2_EXT-08D-hvdc-material-handling-offshore.md) - 해상 운송
- [08E-site-receiving](ontology/extended/2_EXT-08E-hvdc-material-handling-site-receiving.md) - 현장 접수
- [08F-transformer](ontology/extended/2_EXT-08F-hvdc-material-handling-transformer.md) - 변압기 취급
- [08G-bulk-integrated](ontology/extended/2_EXT-08G-hvdc-material-handling-bulk-integrated.md) - Bulk Cargo 통합
- [08-consolidated](ontology/extended/2_EXT-08-hvdc-material-handling-consolidated.md) - Material Handling 전체 통합 (3214줄)

---

## 3. 가이드 및 설정

### 시스템 가이드
- **[SYSTEM_ARCHITECTURE_FINAL.md](guides/SYSTEM_ARCHITECTURE_FINAL.md)** - 시스템 아키텍처 최종 가이드
- **[CONFIGURATION_GUIDE.md](guides/CONFIGURATION_GUIDE.md)** - 설정 가이드
- **[USER_GUIDE.md](guides/USER_GUIDE.md)** - 사용자 가이드

### 문서 인덱스
- **[00_DOCUMENTATION_INDEX.md](guides/00_DOCUMENTATION_INDEX.md)** - 문서 인덱스 (guides 폴더 내)

### 명령어 및 모드
- **[Slash_Commands_Modes_List_v2.1.MD](guides/Slash_Commands_Modes_List_v2.1.MD)** - Slash 명령어 및 모드 목록
- **[Slash_Commands_Modes_List_v2.1_머신러더블.txt](guides/Slash_Commands_Modes_List_v2.1_머신러더블.txt)** - 머신 읽기 가능 버전

### MACHO-GPT 지침
- **[지침.MD](guides/지침.MD)** - MACHO-GPT 지침
- **[지침_압축_12k.txt](guides/지침_압축_12k.txt)** - 압축 버전
- **[지침_머신러더블.txt](guides/지침_머신러더블.txt)** - 머신 읽기 가능 버전

---

## 4. 데이터 및 출력

### 참조 데이터 (`data/reference/`)
- **rates/** - 요율 데이터
  - 항공 화물 요율
  - 컨테이너 화물 요율
  - 내륙 운송 요율
  - 계약 내륙 트럭 요금
  - 송장 요율 참조 (Bulk, Full)
- **mappings/** - 매핑 데이터
  - Approved Lane Map
  - OD Lane Mapping
  - 매핑 업데이트

### 원본 데이터 (`data/`)
- **whatsapp/** - WhatsApp 대화 로그
- **excel/** - Excel 원본 파일
- **csv/** - CSV 데이터

### 변환 출력 (`output/`)
- **whatsapp/** - WhatsApp 변환 결과 (JSON)
- **excel/** - Excel 변환 결과 (JSON, CSV)
- **machine_readable/** - 머신러더블 텍스트 문서
- **integrated/** - 통합 데이터베이스
  - `hvdc_integrated_database.json` - 통합 JSON 데이터베이스
  - `hvdc_database_schema.json` - 데이터베이스 스키마
  - `hvdc_database_summary.md` - 데이터베이스 요약
  - `hvdc_documentation_index.md` - 문서 인덱스
  - `README.md` - 통합 데이터베이스 README

---

## 5. 개발 문서

### 프로젝트 정보
- **[../README.md](../README.md)** - 프로젝트 메인 README
- **[../pyproject.toml](../pyproject.toml)** - Python 프로젝트 설정

### 소스 코드 (`src/mrconvert/`)
- `cli.py` - CLI 인터페이스
- `pdf_converter.py` - PDF 변환
- `docx_converter.py` - DOCX 변환
- `excel_converter.py` - Excel 변환
- `whatsapp_parser.py` - WhatsApp 파서
- `bidirectional.py` - 양방향 변환
- `entity_loader.py` - 엔티티 로더
- `types.py` - 타입 정의
- `utils.py` - 유틸리티 함수

### 테스트 (`tests/`)
- `test_smoke.py` - 스모크 테스트
- `test_whatsapp_parser.py` - WhatsApp 파서 테스트
- `test_bidirectional.py` - 양방향 변환 테스트
- `test_cli_bidirectional.py` - CLI 양방향 변환 테스트

---

## 6. 변환된 PDF 문서 (`docs/converted/`)

1. **MAIN.pdf** - 메인 문서
2. **CODE.pdf** - 코드 문서
3. **INVOICE.pdf** - 송장 문서
4. **LOGISTICS AI.pdf** - 물류 AI 문서
5. **BULK CARGO OPERATION.pdf** - 벌크 화물 운영
6. **CIPL·BL Pre-Arrival Guard.pdf** - CIPL·BL 사전 도착 가드

---

## 7. 보관 자료 (`archive/`)

### 구버전 온톨로지
- **legacy_ontology/** - 구버전 온톨로지 폴더들
  - `ontology_complete/` - 완전판 온톨로지
  - `ontology_final/` - 최종 온톨로지
  - `ontology_machine_readable/` - 머신 읽기 가능 온톨로지
  - `ontology_md/` - Markdown 온톨로지
  - `ontology_md_complete/` - 완전판 Markdown 온톨로지

### 임시 파일
- **scripts/** - 일회성 스크립트들 (PDF 변환, 온톨로지 생성 등)
- **duplicate_whatsapp/** - 중복 WhatsApp 출력

---

## 프로젝트 구조 요약

```
mrconvert_v1/
├── docs/
│   ├── 00_PROJECT_INDEX.md (본 문서)
│   ├── m.md (간단 아키텍처)
│   ├── HVDC_System_Architecture.md (전체 설계)
│   ├── ontology/ (Core 8 + Extended 15 + Consolidated)
│   ├── guides/ (9개 가이드 문서)
│   └── converted/ (6개 변환된 PDF)
├── data/ (원본 데이터)
│   ├── reference/ (요율, 매핑)
│   ├── whatsapp/
│   ├── excel/
│   └── csv/
├── output/ (변환 결과 + 통합 DB)
│   ├── whatsapp/
│   ├── excel/
│   ├── machine_readable/
│   └── integrated/
├── archive/ (구버전 + 임시 파일)
├── src/mrconvert/ (Python 패키지)
├── tests/ (테스트 코드)
└── README.md (메인 README)
```

---

## 문서 활용 가이드

### 상세 정보가 필요한 경우
- **개별 온톨로지 문서** 사용 (`ontology/core/`, `ontology/extended/`)
- 각 온톨로지의 상세 정의, SHACL 제약조건, JSON-LD 예제, SPARQL 쿼리 포함

### 전체 개요가 필요한 경우
- **Consolidated 문서** 사용 (`ontology/core_consolidated/`, `ontology/extended/*-consolidated.md`)
- 여러 온톨로지를 한 번에 참조 가능

### 시스템 아키텍처 이해
- **[m.md](m.md)** - 빠른 시각화
- **[HVDC_System_Architecture.md](HVDC_System_Architecture.md)** - 상세 설계

### 실무 가이드
- **[guides/](guides/)** 폴더의 각종 가이드 문서 참조

---

**문서 버전**: unified-3.4 (Core), unified-1.0 (Material Handling)
**최종 업데이트**: 2025-10-26
**총 온톨로지 문서**: Core 8개 + Extended 15개 + Consolidated 6개

