# HVDC Project Ontology Documentation

이 디렉토리는 HVDC 프로젝트의 온톨로지 문서를 포함합니다. 문서는 Core와 Extended 두 그룹으로 구성되어 있으며, 각각 논리적 순서로 정렬되어 있습니다.

## Core Ontology Documents

핵심 물류 시스템 온톨로지 문서들입니다.

1. **hvdc-core-framework** (`1_CORE-01-hvdc-core-framework.md`)
   - HVDC 프로젝트 핵심 프레임워크 온톨로지
   - 버전: unified-3.4

2. **hvdc-infra-nodes** (`1_CORE-02-hvdc-infra-nodes.md`)
   - 물리적 인프라 노드 온톨로지
   - 버전: unified-3.4

3. **hvdc-warehouse-ops** (`1_CORE-03-hvdc-warehouse-ops.md`)
   - 창고 운영 온톨로지
   - 버전: unified-3.4

4. **hvdc-invoice-cost** (`1_CORE-04-hvdc-invoice-cost.md`)
   - 송장 및 비용 관리 온톨로지
   - 버전: unified-3.4

5. **hvdc-bulk-cargo-ops** (`1_CORE-05-hvdc-bulk-cargo-ops.md`)
   - 벌크 화물 운영 온톨로지
   - 버전: unified-3.4

6. **hvdc-doc-guardian** (`1_CORE-06-hvdc-doc-guardian.md`)
   - 물류 문서 가디언 온톨로지
   - 버전: unified-3.4

7. **hvdc-ocr-pipeline** (`1_CORE-07-hvdc-ocr-pipeline.md`)
   - OCR 파이프라인 온톨로지
   - 버전: unified-3.4

8. **hvdc-flow-code-algorithm** (`1_CORE-08-flow-code.md`)
   - Flow Code 알고리즘 및 물류 흐름 패턴 온톨로지
   - 버전: unified-3.4

## Extended Ontology Documents

확장된 기능 및 특수 목적 온톨로지 문서들입니다.

1. **hvdc-ofco-port-ops (en)** (`2_EXT-01-hvdc-ofco-port-ops-en.md`)
   - OFCO 항만 운영 온톨로지 (영문)
   - 버전: unified-3.4

2. **hvdc-ofco-port-ops (ko)** (`2_EXT-02-hvdc-ofco-port-ops-ko.md`)
   - OFCO 항만 운영 온톨로지 (한글)
   - 버전: unified-3.4

3. **hvdc-comm-email** (`2_EXT-03-hvdc-comm-email.md`)
   - 이메일 통신 시스템 온톨로지
   - 버전: unified-3.4

4. **hvdc-comm-chat** (`2_EXT-04-hvdc-comm-chat.md`)
   - 채팅 통신 시스템 온톨로지
   - 버전: unified-3.4

5. **hvdc-ops-management** (`2_EXT-05-hvdc-ops-management.md`)
   - 운영 관리 온톨로지
   - 버전: unified-3.4

6. **hvdc-compliance-customs** (`2_EXT-06-hvdc-compliance-customs.md`)
   - 컴플라이언스 및 통관 온톨로지
   - 버전: unified-3.4

7. **hvdc-dev-tools** (`2_EXT-07-hvdc-dev-tools.md`)
   - 개발 도구 온톨로지
   - 버전: unified-3.4

8. **hvdc-material-handling-overview** (`2_EXT-08A-hvdc-material-handling-overview.md`)
   - 물자 취급 개요 온톨로지
   - 버전: unified-1.0
   - 출처: HVDC Material Handling Workshop (2024-11-19)

9. **hvdc-material-handling-customs** (`2_EXT-08B-hvdc-material-handling-customs.md`)
   - 통관 절차 온톨로지
   - 버전: unified-1.0
   - 출처: HVDC Material Handling Workshop (2024-11-19)

10. **hvdc-material-handling-storage** (`2_EXT-08C-hvdc-material-handling-storage.md`)
    - 저장 및 내륙 운송 온톨로지
    - 버전: unified-1.0
    - 출처: HVDC Material Handling Workshop (2024-11-19)

11. **hvdc-material-handling-offshore** (`2_EXT-08D-hvdc-material-handling-offshore.md`)
    - 해상 운송 온톨로지
    - 버전: unified-1.0
    - 출처: HVDC Material Handling Workshop (2024-11-19)

12. **hvdc-material-handling-site-receiving** (`2_EXT-08E-hvdc-material-handling-site-receiving.md`)
    - 현장 접수 온톨로지
    - 버전: unified-1.0
    - 출처: HVDC Material Handling Workshop (2024-11-19)

13. **hvdc-material-handling-transformer** (`2_EXT-08F-hvdc-material-handling-transformer.md`)
    - 변압기 취급 온톨로지
    - 버전: unified-1.0
    - 출처: HVDC Material Handling Workshop (2024-11-19)

14. **hvdc-material-handling-bulk-integrated** (`2_EXT-08G-hvdc-material-handling-bulk-integrated.md`)
    - 물자 취급 및 벌크 화물 통합 온톨로지
    - 버전: integrated-1.0
    - 출처: HVDC Material Handling Workshop + Bulk Cargo Operations
    - 설명: 물자 취급과 벌크 화물 운영을 통합한 종합 온톨로지

## Consolidated Documents

통합 문서는 관련 온톨로지를 하나의 문서로 통합하여 전체 도메인을 조망할 수 있도록 합니다.

### Core Consolidated (`core_consolidated/`)

1. **CONSOLIDATED-01: Framework + Infrastructure** (`CONSOLIDATED-01-framework-infrastructure.md`)
   - 통합: Core 01 (Framework) + Core 02 (Infrastructure Nodes)
   - 1,001줄 (목표 ~1,000줄)

2. **CONSOLIDATED-02: Warehouse + Flow Code** (`CONSOLIDATED-02-warehouse-flow.md`)
   - 통합: Core 03 (Warehouse Ops) + Core 08 (Flow Code)
   - 1,133줄 (목표 ~1,000줄)

3. **CONSOLIDATED-03: Cost + Bulk Cargo** (`CONSOLIDATED-03-cost-bulk.md`)
   - 통합: Core 04 (Invoice/Cost) + Core 05 (Bulk Cargo)
   - 1,069줄 (목표 ~1,000줄)

4. **CONSOLIDATED-04: Document + OCR** (`CONSOLIDATED-04-document-ocr.md`)
   - 통합: Core 06 (Doc Guardian) + Core 07 (OCR Pipeline)
   - 1,038줄 (목표 ~1,000줄)

### Extended Consolidated (`extended/`)

1. **Material Handling Consolidated** (`2_EXT-08-hvdc-material-handling-consolidated.md`)
   - 통합: 2_EXT-08A ~ 2_EXT-08G (7개 Material Handling 문서)
   - 3,214줄
   - 전체 물자 취급 프로세스의 완전한 통합 뷰

## 문서 구조

각 온톨로지 문서는 다음 구조를 따릅니다:

- **YAML Front Matter**: 메타데이터 (제목, 타입, 도메인, 버전 등)
- **Executive Summary**: 문서 개요
- **Visual Ontology Stack**: 시각적 온톨로지 구조
- **Part 1**: 핵심 온톨로지 시스템
- **Part 2**: 구현 세부사항
- **Part 3**: 운영 통합
- **JSON-LD Examples**: 실제 사용 예시
- **SPARQL Queries**: 쿼리 예시
- **Semantic KPI Layer**: 핵심 성과 지표
- **추천 명령어**: 관련 명령어 목록

## 버전 관리

모든 문서는 `unified-3.4` 버전을 사용하며, 일관된 온톨로지 구조를 유지합니다.

## 참고사항

- 모든 문서는 `hvdc-` 접두사로 시작하는 제목을 사용합니다
- Core 문서는 `1_CORE-XX` 형식, Extended 문서는 `2_EXT-XX` 형식의 파일명을 사용합니다
- 문서 간 상호 참조는 상대 경로를 사용합니다


