# 🔌 HVDC 창고 물류 노드 온톨로지 v2.0

**범위**: HVDC 프로젝트 내 창고·현장·해상기지(MOSB) 중심의 물류 노드, 이벤트, 속성, 검증(Shapes), 질의(SPARQL) 표준 정의.

---

## 1) 상위 모델(Concept L1)

```
LogisticsOntology
└── Node
    ├── Warehouse
    │   ├── IndoorWarehouse
    │   ├── OutdoorWarehouse
    │   └── DangerousCargoWarehouse
    ├── Site (Project Site)
    └── OffshoreBase (MOSB)

└── Thing
    ├── Case / Item
    ├── TransportEvent
    └── StockSnapshot
```

> 네임스페이스: `@prefix hvdc: <http://samsung.com/project-logistics#>` / `xsd`, `rdf`, `rdfs`, `owl`, `sh` 일반 표준 사용

---

## 2) 핵심 클래스 정의 (L2)

### 2.1 Node 계열
- **hvdc:Warehouse** ⊂ hvdc:Node
  - **hvdc:IndoorWarehouse**
  - **hvdc:OutdoorWarehouse**
  - **hvdc:DangerousCargoWarehouse**
- **hvdc:Site** ⊂ hvdc:Node  (AGI, DAS, MIR, SHU 등 현장)
- **hvdc:OffshoreBase** ⊂ hvdc:Node  (MOSB)

### 2.2 기타 운영 클래스
- **hvdc:TransportEvent**: 노드 간 이동(Port/WH/MOSB/Site) 및 상태 변경 이벤트
- **hvdc:StockSnapshot**: 특정 시점 노드의 수량·중량·CBM 스냅샷
- **hvdc:Case** / **hvdc:Item**: 패키지/개별 아이템 단위의 식별 개체
- **hvdc:Invoice / hvdc:InvoiceLineItem / hvdc:ChargeSummary**: 비용 객체(연계용)

---

## 3) 핵심 속성 표준(요약)

- **식별자**: `hvdc:hasCase`, `hvdc:hasRecordId`, `hvdc:hasHVDCCode`
- **날짜**: `hvdc:hasDate`, `hvdc:hasOperationMonth`, `hvdc:hasStartDate`, `hvdc:hasFinishDate`
- **위치**: `hvdc:hasLocation`, `hvdc:hasWarehouseName`, `hvdc:hasStorageType`
- **수량**: `hvdc:hasQuantity`, `hvdc:hasPackageCount`, `hvdc:hasWeight`, `hvdc:hasCBM`
- **금액**: `hvdc:hasAmount`, `hvdc:hasRateUSD`, `hvdc:hasTotalUSD`
- **분류**: `hvdc:hasCategory`, `hvdc:hasVendor`, `hvdc:hasTransactionType`, `hvdc:hasLogisticsFlowCode`, `hvdc:hasWHHandling`

> 데이터 타입 예시: `xsd:string`, `xsd:dateTime`, `xsd:integer`, `xsd:decimal`

---

## 4) 표준 노드 인스턴스 (v2 목록)

### 4.1 창고(Warehouse)
- **DSV Al Markaz** (Indoor)
- **DSV Indoor** (Indoor)
- **DSV Outdoor** (Outdoor)
- **DSV MZP** (Outdoor)
- **AAA Storage** (Dangerous 가능/보관 전용)
- **Hauler Indoor** (Indoor)
- **DHL Warehouse** (Indoor/Transit)
- **MOSB** (OffshoreBase로도 분류되는 특수 창고성 노드)

### 4.2 현장(Site)
- **AGI**, **DAS**, **MIR**, **SHU**

> 실제 엑셀 컬럼 표기를 그대로 별칭으로 보존(예: `AAA  Storage` 공백 이슈 포함)하며, 표준 라벨로 매핑.

---

## 5) 물류 흐름 코드(Logistics Flow Code)

**정의**(0~4 고정):
- **0**: Pre Arrival — Planning → Port
- **1**: Direct Port→Site — Port → Site
- **2**: Port→WH→Site — Port → Warehouse → Site
- **3**: Port→WH→MOSB→Site — Port → Warehouse → MOSB → Site
- **4**: Port→WH→WH→MOSB→Site — Port → Warehouse → Warehouse → MOSB → Site

**규칙**
- 비표준 값(예: 6)은 정규화하여 3으로 매핑 가능(데이터 복구 단계에서 적용)
- `hvdc:hasWHHandling`(정수)는 경유 창고 횟수(0~3)를 표현

---

## 6) Turtle 스키마 요약(발췌)

```turtle
@prefix hvdc: <http://samsung.com/project-logistics#> .
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl:  <http://www.w3.org/2002/07/owl#> .

hvdc:Warehouse a owl:Class ; rdfs:label "Warehouse"@en .
hvdc:IndoorWarehouse a owl:Class ; rdfs:subClassOf hvdc:Warehouse .
hvdc:OutdoorWarehouse a owl:Class ; rdfs:subClassOf hvdc:Warehouse .
hvdc:DangerousCargoWarehouse a owl:Class ; rdfs:subClassOf hvdc:Warehouse .

hvdc:Site a owl:Class ; rdfs:label "Project Site"@en .
hvdc:OffshoreBase a owl:Class ; rdfs:label "Offshore Base"@en ; rdfs:subClassOf hvdc:Warehouse .

hvdc:TransportEvent a owl:Class .
hvdc:StockSnapshot a owl:Class .

hvdc:hasDate a owl:DatatypeProperty ; rdfs:range xsd:dateTime .
hvdc:hasLocation a owl:ObjectProperty ; rdfs:range hvdc:Node .
hvdc:hasWarehouseName a owl:DatatypeProperty ; rdfs:range xsd:string .
hvdc:hasQuantity a owl:DatatypeProperty ; rdfs:range xsd:integer .
hvdc:hasWeight a owl:DatatypeProperty ; rdfs:range xsd:decimal .
hvdc:hasCBM a owl:DatatypeProperty ; rdfs:range xsd:decimal .
hvdc:hasAmount a owl:DatatypeProperty ; rdfs:range xsd:decimal .
hvdc:hasLogisticsFlowCode a owl:DatatypeProperty ; rdfs:range xsd:integer .
hvdc:hasWHHandling a owl:DatatypeProperty ; rdfs:range xsd:integer .
```

---

## 7) 예시 인스턴스 & 이벤트(발췌)

```turtle
# 노드 인스턴스
hvdc:DSV_Indoor a hvdc:IndoorWarehouse ; rdfs:label "DSV Indoor" .
hvdc:MOSB_Base a hvdc:OffshoreBase ; rdfs:label "MOSB" .
hvdc:DAS_Site a hvdc:Site ; rdfs:label "DAS" .

# 케이스/이벤트 샘플
hvdc:CASE_208221 a hvdc:Case ; hvdc:hasHVDCCode "HE-208221" .

hvdc:EVT_208221_1 a hvdc:TransportEvent ;
  hvdc:hasCase "HE-208221" ;
  hvdc:hasDate "2025-05-13T08:00:00"^^xsd:dateTime ;
  hvdc:hasLocation hvdc:DSV_Indoor ;
  hvdc:hasQuantity 2 ; hvdc:hasWeight 694.00 ; hvdc:hasCBM 12.50 ;
  hvdc:hasLogisticsFlowCode 3 ; hvdc:hasWHHandling 1 .

hvdc:EVT_208221_2 a hvdc:TransportEvent ;
  hvdc:hasCase "HE-208221" ; hvdc:hasDate "2025-05-15T10:00:00"^^xsd:dateTime ;
  hvdc:hasLocation hvdc:MOSB_Base ; hvdc:hasLogisticsFlowCode 3 ; hvdc:hasWHHandling 2 .

hvdc:EVT_208221_3 a hvdc:TransportEvent ;
  hvdc:hasCase "HE-208221" ; hvdc:hasDate "2025-05-18T16:00:00"^^xsd:dateTime ;
  hvdc:hasLocation hvdc:DAS_Site ; hvdc:hasLogisticsFlowCode 3 ; hvdc:hasWHHandling 2 .
```

---

## 8) SHACL Shapes (검증 규칙)

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .

# Warehouse 노드 검증
hvdc:WarehouseNodeShape a sh:NodeShape ;
  sh:targetClass hvdc:Warehouse ;
  sh:property [ sh:path hvdc:hasWarehouseName ; sh:datatype xsd:string ; sh:minCount 1 ] ;
  sh:property [ sh:path hvdc:hasStorageType ;   sh:datatype xsd:string ; sh:minCount 0 ] .

# TransportEvent 검증 (핵심 4요소)
hvdc:TransportEventShape a sh:NodeShape ;
  sh:targetClass hvdc:TransportEvent ;
  sh:property [ sh:path hvdc:hasCase ;               sh:datatype xsd:string ;  sh:minCount 1 ] ;
  sh:property [ sh:path hvdc:hasDate ;               sh:datatype xsd:dateTime ; sh:minCount 1 ] ;
  sh:property [ sh:path hvdc:hasLocation ;           sh:class hvdc:Node ;       sh:minCount 1 ] ;
  sh:property [ sh:path hvdc:hasLogisticsFlowCode ;  sh:datatype xsd:integer ; sh:minInclusive 0 ; sh:maxInclusive 4 ; sh:minCount 1 ] .
```

---

## 9) SPARQL 질의(운영 예시)

**(A) 월별·창고별 수량/금액 요약**
```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?month ?warehouse (SUM(?amount) AS ?totalAmount) (SUM(?qty) AS ?totalQty)
WHERE {
  ?e a hvdc:TransportEvent ; hvdc:hasLocation ?warehouse ; hvdc:hasDate ?date .
  OPTIONAL { ?e hvdc:hasAmount ?amount }
  OPTIONAL { ?e hvdc:hasQuantity ?qty }
  BIND(SUBSTR(STR(?date), 1, 7) AS ?month)
}
GROUP BY ?month ?warehouse
ORDER BY ?month ?warehouse
```

**(B) Flow Code 분포(wh handling 기반)**
```sparql
PREFIX hvdc: <http://samsung.com/project-logistics#>
SELECT ?flow (COUNT(?e) AS ?cnt)
WHERE {
  ?e a hvdc:TransportEvent ; hvdc:hasLogisticsFlowCode ?flow .
}
GROUP BY ?flow ORDER BY ?flow
```

---

## 10) 매핑 규칙 연동 (Excel → RDF)

- `field_mappings` 예: `Case_No→hasCase`, `Date→hasDate`, `Location→hasLocation`, `Qty→hasQuantity`, `Amount→hasAmount`, `Stack_Status→hasStackStatus`, `DHL Warehouse→hasDHLWarehouse`
- 정규화 규칙: `NULL PKG→1`, `Flow Code 6→3`, 벤더/날짜 표준화
- 분류 코드: `warehouse_codes`(DSV/MOSB/AAA 등), `site_codes`(AGI/DAS/MIR/SHU)

---

## 11) KPI & 거버넌스

- **PKG Accuracy ≥ 99%** = 시스템 PKG / 실제수입PKG
- **Flow Code Coverage** = {0..4} 전체 출현
- **WH Handling 합리성** = 경유 창고 횟수(0~3) 분포 정상성 모니터
- **데이터 품질** = 헤더 탐지/전각 공백/날짜 파싱 오류 0건 기준으로 CI 실패 설정

---

## 12) 운영 가이드

- **Zero‑Edit 원본 보존**: Excel 원본은 ETL 전용 폴더에서만 사용, 수동 편집 금지
- **매핑 버전 잠금**: `hvdc_integrated_mapping_rules_v*.json` 불일치 시 빌드 중단
- **이슈 핸들러**: MOSB·날짜 포맷 변동 감지 시 진단 스크립트 재실행

---

## 13) JSON‑LD 컨텍스트(발췌)

```json
{
  "@context": {
    "hvdc": "http://samsung.com/project-logistics#",
    "hasCase": "hvdc:hasCase",
    "hasDate": {"@id": "hvdc:hasDate", "@type": "xsd:dateTime"},
    "hasLocation": {"@id": "hvdc:hasLocation", "@type": "@id"},
    "hasLogisticsFlowCode": {"@id": "hvdc:hasLogisticsFlowCode", "@type": "xsd:integer"}
  }
}
```

---

## 14) 버전
- v2.0 (2025-10-25): 창고·현장·MOSB 노드 정규화, Flow Code(0~4) 고정, SHACL/질의 포함.

