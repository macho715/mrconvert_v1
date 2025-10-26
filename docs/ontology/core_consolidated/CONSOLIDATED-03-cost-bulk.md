---
title: "HVDC Cost Management & Bulk Cargo Ontology - Consolidated"
type: "ontology-design"
domain: "cost-bulk-operations"
sub-domains: ["invoice-verification", "cost-guard", "bulk-cargo-operations", "seafastening", "stability-control"]
version: "consolidated-1.0"
date: "2025-10-26"
tags: ["ontology", "hvdc", "cost-management", "bulk-cargo", "invoice", "verification", "consolidated"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "Turtle", "XSD", "IMSBC", "SOLAS"]
status: "active"
source_files: ["1_CORE-04-hvdc-invoice-cost.md", "1_CORE-05-hvdc-bulk-cargo-ops.md"]
---

# hvdc-cost-bulk · CONSOLIDATED-03

## 📑 Table of Contents
1. [Invoice & Cost Management](#section-1)
2. [Bulk Cargo Operations](#section-2)

---

## Section 1: Invoice & Cost Management

### Source
- **Original File**: `1_CORE-04-hvdc-invoice-cost.md`
- **Version**: unified-1.0
- **Date**: 2025-01-19

## Executive Summary

**온톨로지-퍼스트 청구서 시스템**은 "**멀티-키 아이덴티티 그래프**(BL/Container/DO/Invoice/Case/Booking/ShipmentID/.../hvdc_code 아무 키든 OK)" 위에서 **Invoice→Line→OD Lane→RateRef→Δ%→Risk**로 한 번에 캐스케이드합니다. \(EN\-KR: Any\-key in → Resolve → Lane&Rate join → Δ% risk band\.\)
표준요율은 __Air/Container/Bulk 계약 레퍼런스__와 __Inland Trucking\(OD×Unit\) 테이블__을 온톨로지 클래스로 들고, 모든 계산은 __USD 기준·고정환율 1\.00 USD=3\.6725 AED__ 규칙을 따릅니다\.
OD 정규화·조인은 __ApprovedLaneMap/RefDestinationMap__을 통해 수행되고, 결과는 \*\*COST\-GUARD Δ% 밴드\(PASS/WARN/HIGH/CRITICAL\)\*\*로 귀결됩니다\.
감사 트레이스는 __PRISM\.KERNEL__ 포맷\(5\-line recap \+ proof\.artifact JSON\)으로 고정 형식으로 남깁니다\.

__Visual — 핵심 클래스/관계\(요약\)__

__Class__

__핵심 속성__

__관계__

__근거/조인 소스__

__결과__

hvdc:Invoice

docId, vendor, issueDate, currency

hasLine → InvoiceLine

—

상태, 총액, proof

hvdc:InvoiceLine

chargeDesc, qty, unit, draftRateUSD

hasLane → ODLane / uses → RateRef

Inland Trucking/Table, Air/Container/Bulk Rate

Δ%, cg\_band

hvdc:ODLane

origin\_norm, destination\_norm, vehicle, unit

joinedBy → ApprovedLaneMap

RefDestinationMap, Lane stats

median\_rate\_usd

hvdc:RateRef

rate\_usd, tolerance\(±3%\), source\(contract/market/special\)

per Category/Port/Dest/Unit

Air/Container/Bulk/Trucking tables

ref\_rate\_usd

hvdc:CurrencyPolicy

base=USD, fx=3\.6725

validates Invoice/Line

currency\_mismatch rule

환산/락

hvdc:RiskResult

delta\_pct, cg\_band, verdict

from Line vs Ref

COST\-GUARD bands

PASS/FAIL

자료: 표준요율 테이블\(계약\)·고정 FX 규정·Lane 정규화 지도\.

__How it works \(flow\)__

1. __키 해석\(Identity\)__: BL/Container/DO/Invoice/… 입력 → 동일 실체\(Shipment/Doc\) 클러스터 식별\. \(멀티\-키 그래프\)
2. __Lane 정규화__: 원지/착지 명칭을 __RefDestinationMap__으로 정규화 → __ApprovedLaneMap__에서 lane 통계/표준요율 후보 추출\.
3. __Rate 조인__: 라인별 __Category\+Port\+Destination\+Unit__로 계약 요율 테이블 매칭\(±3% 톨러런스\)\.
4. __Δ% & 밴드 산정__: Δ%=\(draft−ref\)/ref×100 → __PASS/WARN/HIGH/CRITICAL__ \(COST\-GUARD\)\. FX는 USD 고정\(3\.6725\)로 비교\.

---

## Section 2: Bulk Cargo Operations

### Source
- **Original File**: `1_CORE-05-hvdc-bulk-cargo-ops.md`
- **Version**: unified-1.0
- **Date**: 2025-01-23

## Executive Summary

**Bulk/Project 화물 해상 운송(적재·양하·고박·안정성·인양) 전 과정**을 **온톨로지(지식 그래프)**로 모델링하여 데이터 일관성, 추적성, 자동화 가능성을 높인다.

**적용 범위**: 철강 구조물, OOG, 프리캐스트(Hollow Core Slab), Breakbulk 전반
**목표 산출물**: 클래스/속성 정의, 제약, 예시 인스턴스, 검증(SHACL), 교환 스키마(CSV), 쿼리(SPARQL) 샘플
**단위**: 길이(m), 중량(t), 각도(deg), 좌표계: 선박 데크 로컬 좌표 (X fwd, Y port→stbd, Z keel→up)
**책임 경계**: 본 모델은 **데이터 표현/검증용**. 공학적 최종 판단(예: Stability 승인, 구조 검토)은 전문 SW/엔지니어 권한

**상위 개념 계층(Top Taxonomy)**:
```
Maritime Logistics
└── Cargo Operation
    ├── Bulk Cargo Operation (BULK)
    │   ├── Planning Phase
    │   ├── Loading Operation
    │   ├── Discharging Operation
    │   ├── Stowage & Lashing
    │   ├── Stability Control
    │   ├── Lifting & Transport Handling
    │   └── Post-Operation (Survey, Handover)
    ├── Documentation (Vessel Loading Plan, Lashing Plan, Stability Report, Rigging Plan)
    ├── Resources (Vessel, Equipment, Manpower)
    ├── Locations (Port, Berth, Jetty, Yard)
    └── Constraints (Safety, Compliance, Environment, Contract)
```

**Visual — 핵심 클래스/관계(요약)**

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| debulk:Cargo | cargoId, cargoType, weight(t), dimL/W/H(m), cogX/Y/Z(m), stackable(boolean), hazmatClass? | placedOn→DeckArea, securedBy→LashingAssembly, handledBy→Equipment | OCR/Table Parser | 상태, 정합성 |
| debulk:Vessel | vesselName, imo?, deckStrength(t/m²), coordinateOrigin | hasDeck→DeckArea, carries→Cargo, operatedBy→Crew | Vessel Registry | 운항 상태 |
| debulk:DeckArea | areaId, usableL/W/H, maxPointLoad, maxUniformLoad | partOf→Vessel, hosts→Cargo | Deck Layout | 적재 용량 |
| debulk:LashingAssembly | requiredCapacity(t), calcTension(t), safetyFactor | appliedTo→Cargo, uses→LashingElement, verifiedBy→Engineer | Lashing Calc | 고박 강도 |
| debulk:LashingElement | wll(t), angleDeg, count, length(m) | partOf→LashingAssembly | Equipment Spec | 유효 용량 |
| debulk:StabilityCase | disp(t), vcg(m), gm(m), rollAngle(deg) | evaluates→Vessel, considers→Cargo | Stability Calc | 안정성 상태 |
| debulk:LiftingPlan | liftId, method, slingAngleDeg, estLoadShare(t) | for→Cargo, uses→RiggingGear, verifiedBy→Engineer | Rigging Design | 인양 계획 |
| debulk:RiggingGear | gearId, type, wll(t), length(m) | partOf→LiftingPlan | Gear Spec | 장비 용량 |
| debulk:Equipment | equipId, type, swl(t), radius(m)? | allocatedTo→OperationTask | Equipment List | 작업 배정 |
| debulk:Manpower | personId, role, certificateId?, contact | assignedTo→OperationTask | Crew Roster | 인력 배정 |
| debulk:OperationTask | taskId, status, start/end(DateTime), sequence | relatesCargo→Cargo, uses→Equipment | Task Planning | 작업 상태 |
| debulk:Port/Jetty/Berth | code, draught, restriction | hosts→OperationTask | Port Database | 위치 정보 |
| debulk:Environment | wind(m/s), seaState, temp, accel_g | affects→LashingAssembly/StabilityCase | Weather API | 환경 영향 |
| debulk:Document | docId, type, version, fileRef | documents→(Plan/Report), about→(Vessel/Cargo) | Document Store | 문서 관리 |

자료: 표준요율 테이블(계약)·고정 FX 규정·Lane 정규화 지도.

**How it works (flow)**

1. **Planning Phase**: 데이터 수집·제약 정의 → Draft → Reviewed → Approved (Loading Plan, Stowage Layout, Lashing Calc Sheet)
2. **Pre-Operation**: 자원 배정·브리핑 → Ready → Mobilized (Equipment & Workforce Plan, JSA)
3. **Execution**: 적재/고박/검사 → In-Progress → Paused/Resumed → Completed (QC Checklist, Photos, Survey Report)
4. **Post-Operation**: 서류/인계 → Completed → Archived (B/L, COA Evidence, Final Report)

**Options (설계 선택지)**

1. **OWL/SHACL 엄격형**: 모든 클래스/속성/제약을 OWL/SHACL로 엄격하게 모델링. *Pros* 의미적 추론↑ / *Cons* 초기 모델링 복잡도↑
2. **하이브리드형(권장)**: OWL + CSV 교환 + SHACL 제약, 부족 구간은 유사 패턴 추천. *Pros* 실용성↑ / *Cons* 온톨로지 일관성 유지 필요
3. **실무 간소형**: 핵심 클래스만 모델링하고 나머지는 확장 가능한 구조. *Pros* 빠른 적용↑ / *Cons* 확장성 제한

**Roadmap (P→Pi→B→O→S + KPI)**

- **Prepare**: 클래스 스키마 정의, SHACL 제약 규칙 작성, CSV 템플릿 준비
- **Pilot**: /switch_mode LATTICE + /logi-master bulk-cargo-planning --deep --stability-check로 샘플 화물 1회전. KPI: 검증정확도 ≥97%, 안전성 ≥95%
- **Build**: 라싱 계산, 안정성 검증, 인양 계획 자동화 시스템 구축
- **Operate**: 실시간 모니터링, 이상 상황 즉시 알림 + 대안 제시
- **Scale**: 3D 좌표 연동, CAD/BIM 링크, 가속도 스펙트럼 분석 추가

**Automation notes**

- **입력 감지 →** /switch_mode LATTICE + /logi-master bulk-cargo-planning (화물→적재→고박→안정성→인양 계획)
- **표준 근거**: IMSBC, SOLAS, Port Notice 등 규정 기반 제약 검증
- **감사 포맷**: SHACL Validation 결과 + Stability Report + Lashing Calculation

**QA / Gap 체크**

- Cargo CSV에 **COG/중량/치수** 누락 없음?
- DeckArea에 **허용하중(균등/점하중)** 입력 완료?
- LashingElements **WLL·각도** 기입 및 세트 매핑 완료?
- StabilityCase에 **GM/VCG/조건** 기록?
- Equipment/Manpower **작업별 배정** 완료?

가정: (i) 모든 화물은 정확한 치수/중량 정보를 보유, (ii) 선박 데크 강도 데이터가 최신으로 유지됨, (iii) 환경 조건은 실시간으로 업데이트됨.

---

## 통합 온톨로지 시스템

### Domain Ontology

#### Core Classes

```turtle
# Cost Management Classes
hvdc:Invoice a owl:Class ;
    rdfs:label "Invoice" ;
    rdfs:comment "청구서 문서" .

hvdc:InvoiceLine a owl:Class ;
    rdfs:label "Invoice Line Item" ;
    rdfs:comment "청구서 라인 항목" .

hvdc:ODLane a owl:Class ;
    rdfs:label "Origin-Destination Lane" ;
    rdfs:comment "출발지-도착지 경로" .

hvdc:RateRef a owl:Class ;
    rdfs:label "Rate Reference" ;
    rdfs:comment "표준 요율 참조" .

hvdc:CurrencyPolicy a owl:Class ;
    rdfs:label "Currency Policy" ;
    rdfs:comment "통화 정책" .

hvdc:RiskResult a owl:Class ;
    rdfs:label "Risk Assessment Result" ;
    rdfs:comment "리스크 평가 결과" .

# Bulk Cargo Classes
debulk:Cargo a owl:Class ;
    rdfs:label "Bulk Cargo" ;
    rdfs:comment "벌크 화물" .

debulk:Vessel a owl:Class ;
    rdfs:label "Vessel" ;
    rdfs:comment "선박" .

debulk:DeckArea a owl:Class ;
    rdfs:label "Deck Area" ;
    rdfs:comment "데크 구역" .

debulk:LashingAssembly a owl:Class ;
    rdfs:label "Lashing Assembly" ;
    rdfs:comment "고박 조립체" .

debulk:StabilityCase a owl:Class ;
    rdfs:label "Stability Case" ;
    rdfs:comment "안정성 케이스" .

debulk:LiftingPlan a owl:Class ;
    rdfs:label "Lifting Plan" ;
    rdfs:comment "인양 계획" .
```

#### Data Properties

```turtle
# Cost Management Properties
hvdc:hasDocId a owl:DatatypeProperty ;
    rdfs:label "has document ID" ;
    rdfs:domain hvdc:Invoice ;
    rdfs:range xsd:string .

hvdc:hasVendor a owl:DatatypeProperty ;
    rdfs:label "has vendor" ;
    rdfs:domain hvdc:Invoice ;
    rdfs:range xsd:string .

hvdc:hasIssueDate a owl:DatatypeProperty ;
    rdfs:label "has issue date" ;
    rdfs:domain hvdc:Invoice ;
    rdfs:range xsd:dateTime .

hvdc:hasCurrency a owl:DatatypeProperty ;
    rdfs:label "has currency" ;
    rdfs:domain hvdc:Invoice ;
    rdfs:range xsd:string .

hvdc:hasChargeDesc a owl:DatatypeProperty ;
    rdfs:label "has charge description" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range xsd:string .

hvdc:hasQuantity a owl:DatatypeProperty ;
    rdfs:label "has quantity" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range xsd:decimal .

hvdc:hasUnit a owl:DatatypeProperty ;
    rdfs:label "has unit" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range xsd:string .

hvdc:hasDraftRateUSD a owl:DatatypeProperty ;
    rdfs:label "has draft rate USD" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range xsd:decimal .

hvdc:hasDeltaPercent a owl:DatatypeProperty ;
    rdfs:label "has delta percentage" ;
    rdfs:domain hvdc:RiskResult ;
    rdfs:range xsd:decimal .

hvdc:hasCostGuardBand a owl:DatatypeProperty ;
    rdfs:label "has cost guard band" ;
    rdfs:domain hvdc:RiskResult ;
    rdfs:range xsd:string .

# Bulk Cargo Properties
debulk:hasCargoId a owl:DatatypeProperty ;
    rdfs:label "has cargo ID" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:string .

debulk:hasCargoType a owl:DatatypeProperty ;
    rdfs:label "has cargo type" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:string .

debulk:hasWeight a owl:DatatypeProperty ;
    rdfs:label "has weight" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasDimensionL a owl:DatatypeProperty ;
    rdfs:label "has length dimension" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasDimensionW a owl:DatatypeProperty ;
    rdfs:label "has width dimension" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasDimensionH a owl:DatatypeProperty ;
    rdfs:label "has height dimension" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasCOGX a owl:DatatypeProperty ;
    rdfs:label "has center of gravity X" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasCOGY a owl:DatatypeProperty ;
    rdfs:label "has center of gravity Y" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:hasCOGZ a owl:DatatypeProperty ;
    rdfs:label "has center of gravity Z" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:decimal .

debulk:isStackable a owl:DatatypeProperty ;
    rdfs:label "is stackable" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:boolean .

debulk:hasHazmatClass a owl:DatatypeProperty ;
    rdfs:label "has hazardous material class" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range xsd:string .

debulk:hasVesselName a owl:DatatypeProperty ;
    rdfs:label "has vessel name" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range xsd:string .

debulk:hasIMO a owl:DatatypeProperty ;
    rdfs:label "has IMO number" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range xsd:string .

debulk:hasDeckStrength a owl:DatatypeProperty ;
    rdfs:label "has deck strength" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range xsd:decimal .

debulk:hasRequiredCapacity a owl:DatatypeProperty ;
    rdfs:label "has required capacity" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range xsd:decimal .

debulk:hasCalcTension a owl:DatatypeProperty ;
    rdfs:label "has calculated tension" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range xsd:decimal .

debulk:hasSafetyFactor a owl:DatatypeProperty ;
    rdfs:label "has safety factor" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range xsd:decimal .

debulk:hasDisplacement a owl:DatatypeProperty ;
    rdfs:label "has displacement" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range xsd:decimal .

debulk:hasVCG a owl:DatatypeProperty ;
    rdfs:label "has vertical center of gravity" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range xsd:decimal .

debulk:hasGM a owl:DatatypeProperty ;
    rdfs:label "has metacentric height" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range xsd:decimal .

debulk:hasRollAngle a owl:DatatypeProperty ;
    rdfs:label "has roll angle" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range xsd:decimal .
```

#### Object Properties

```turtle
# Cost Management Relations
hvdc:hasLine a owl:ObjectProperty ;
    rdfs:label "has invoice line" ;
    rdfs:domain hvdc:Invoice ;
    rdfs:range hvdc:InvoiceLine .

hvdc:hasLane a owl:ObjectProperty ;
    rdfs:label "has origin-destination lane" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range hvdc:ODLane .

hvdc:usesRateRef a owl:ObjectProperty ;
    rdfs:label "uses rate reference" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range hvdc:RateRef .

hvdc:hasRiskResult a owl:ObjectProperty ;
    rdfs:label "has risk result" ;
    rdfs:domain hvdc:InvoiceLine ;
    rdfs:range hvdc:RiskResult .

# Bulk Cargo Relations
debulk:placedOn a owl:ObjectProperty ;
    rdfs:label "placed on deck area" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range debulk:DeckArea .

debulk:securedBy a owl:ObjectProperty ;
    rdfs:label "secured by lashing assembly" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range debulk:LashingAssembly .

debulk:handledBy a owl:ObjectProperty ;
    rdfs:label "handled by equipment" ;
    rdfs:domain debulk:Cargo ;
    rdfs:range debulk:Equipment .

debulk:hasDeck a owl:ObjectProperty ;
    rdfs:label "has deck area" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range debulk:DeckArea .

debulk:carries a owl:ObjectProperty ;
    rdfs:label "carries cargo" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range debulk:Cargo .

debulk:operatedBy a owl:ObjectProperty ;
    rdfs:label "operated by crew" ;
    rdfs:domain debulk:Vessel ;
    rdfs:range debulk:Manpower .

debulk:partOf a owl:ObjectProperty ;
    rdfs:label "part of vessel" ;
    rdfs:domain debulk:DeckArea ;
    rdfs:range debulk:Vessel .

debulk:hosts a owl:ObjectProperty ;
    rdfs:label "hosts cargo" ;
    rdfs:domain debulk:DeckArea ;
    rdfs:range debulk:Cargo .

debulk:appliedTo a owl:ObjectProperty ;
    rdfs:label "applied to cargo" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range debulk:Cargo .

debulk:usesLashingElement a owl:ObjectProperty ;
    rdfs:label "uses lashing element" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range debulk:LashingElement .

debulk:verifiedBy a owl:ObjectProperty ;
    rdfs:label "verified by engineer" ;
    rdfs:domain debulk:LashingAssembly ;
    rdfs:range debulk:Manpower .

debulk:evaluates a owl:ObjectProperty ;
    rdfs:label "evaluates vessel" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range debulk:Vessel .

debulk:considers a owl:ObjectProperty ;
    rdfs:label "considers cargo" ;
    rdfs:domain debulk:StabilityCase ;
    rdfs:range debulk:Cargo .

debulk:forCargo a owl:ObjectProperty ;
    rdfs:label "for cargo" ;
    rdfs:domain debulk:LiftingPlan ;
    rdfs:range debulk:Cargo .

debulk:usesRiggingGear a owl:ObjectProperty ;
    rdfs:label "uses rigging gear" ;
    rdfs:domain debulk:LiftingPlan ;
    rdfs:range debulk:RiggingGear .
```

### Use-case별 제약

#### Cost Management Constraints

```turtle
# Invoice Validation
hvdc:InvoiceShape a sh:NodeShape ;
    sh:targetClass hvdc:Invoice ;
    sh:property [
        sh:path hvdc:hasDocId ;
        sh:minCount 1 ;
        sh:message "Invoice must have document ID"
    ] ;
    sh:property [
        sh:path hvdc:hasVendor ;
        sh:minCount 1 ;
        sh:message "Invoice must have vendor"
    ] ;
    sh:property [
        sh:path hvdc:hasIssueDate ;
        sh:minCount 1 ;
        sh:message "Invoice must have issue date"
    ] ;
    sh:property [
        sh:path hvdc:hasCurrency ;
        sh:hasValue "USD" ;
        sh:message "Currency must be USD"
    ] .

# Invoice Line Validation
hvdc:InvoiceLineShape a sh:NodeShape ;
    sh:targetClass hvdc:InvoiceLine ;
    sh:property [
        sh:path hvdc:hasChargeDesc ;
        sh:minCount 1 ;
        sh:message "Invoice line must have charge description"
    ] ;
    sh:property [
        sh:path hvdc:hasQuantity ;
        sh:minInclusive 0.01 ;
        sh:message "Quantity must be positive"
    ] ;
    sh:property [
        sh:path hvdc:hasDraftRateUSD ;
        sh:minInclusive 0.01 ;
        sh:message "Draft rate must be positive"
    ] .

# Cost Guard Band Validation
hvdc:CostGuardShape a sh:NodeShape ;
    sh:targetClass hvdc:RiskResult ;
    sh:property [
        sh:path hvdc:hasCostGuardBand ;
        sh:in ("PASS", "WARN", "HIGH", "CRITICAL") ;
        sh:message "Cost guard band must be PASS, WARN, HIGH, or CRITICAL"
    ] ;
    sh:property [
        sh:path hvdc:hasDeltaPercent ;
        sh:datatype xsd:decimal ;
        sh:message "Delta percentage must be decimal"
    ] .
```

#### Bulk Cargo Constraints

```turtle
# Cargo Validation
debulk:CargoShape a sh:NodeShape ;
    sh:targetClass debulk:Cargo ;
    sh:property [
        sh:path debulk:hasCargoId ;
        sh:minCount 1 ;
        sh:message "Cargo must have ID"
    ] ;
    sh:property [
        sh:path debulk:hasWeight ;
        sh:minInclusive 0.01 ;
        sh:message "Weight must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasDimensionL ;
        sh:minInclusive 0.01 ;
        sh:message "Length dimension must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasDimensionW ;
        sh:minInclusive 0.01 ;
        sh:message "Width dimension must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasDimensionH ;
        sh:minInclusive 0.01 ;
        sh:message "Height dimension must be positive"
    ] .

# Vessel Validation
debulk:VesselShape a sh:NodeShape ;
    sh:targetClass debulk:Vessel ;
    sh:property [
        sh:path debulk:hasVesselName ;
        sh:minCount 1 ;
        sh:message "Vessel must have name"
    ] ;
    sh:property [
        sh:path debulk:hasDeckStrength ;
        sh:minInclusive 0.01 ;
        sh:message "Deck strength must be positive"
    ] .

# Lashing Assembly Validation
debulk:LashingAssemblyShape a sh:NodeShape ;
    sh:targetClass debulk:LashingAssembly ;
    sh:property [
        sh:path debulk:hasRequiredCapacity ;
        sh:minInclusive 0.01 ;
        sh:message "Required capacity must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasCalcTension ;
        sh:minInclusive 0.01 ;
        sh:message "Calculated tension must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasSafetyFactor ;
        sh:minInclusive 1.0 ;
        sh:message "Safety factor must be at least 1.0"
    ] .

# Stability Case Validation
debulk:StabilityCaseShape a sh:NodeShape ;
    sh:targetClass debulk:StabilityCase ;
    sh:property [
        sh:path debulk:hasDisplacement ;
        sh:minInclusive 0.01 ;
        sh:message "Displacement must be positive"
    ] ;
    sh:property [
        sh:path debulk:hasVCG ;
        sh:minInclusive 0.0 ;
        sh:message "VCG must be non-negative"
    ] ;
    sh:property [
        sh:path debulk:hasGM ;
        sh:minInclusive 0.0 ;
        sh:message "GM must be non-negative"
    ] ;
    sh:property [
        sh:path debulk:hasRollAngle ;
        sh:minInclusive 0.0 ;
        sh:maxInclusive 90.0 ;
        sh:message "Roll angle must be between 0 and 90 degrees"
    ] .
```

### JSON-LD Examples

#### Cost Management Example

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "hvdc:invoice-001",
  "@type": "hvdc:Invoice",
  "hvdc:hasDocId": "INV-2025-001",
  "hvdc:hasVendor": "DSV Logistics",
  "hvdc:hasIssueDate": "2025-01-15T00:00:00Z",
  "hvdc:hasCurrency": "USD",
  "hvdc:hasLine": {
    "@type": "hvdc:InvoiceLine",
    "hvdc:hasChargeDesc": "Inland Transportation",
    "hvdc:hasQuantity": 2.0,
    "hvdc:hasUnit": "TEU",
    "hvdc:hasDraftRateUSD": 1500.00,
    "hvdc:hasLane": {
      "@type": "hvdc:ODLane",
      "hvdc:hasOriginNorm": "MOSB",
      "hvdc:hasDestinationNorm": "MIR Site",
      "hvdc:hasVehicle": "Truck",
      "hvdc:hasUnit": "TEU"
    },
    "hvdc:hasRiskResult": {
      "@type": "hvdc:RiskResult",
      "hvdc:hasDeltaPercent": 5.2,
      "hvdc:hasCostGuardBand": "WARN",
      "hvdc:hasVerdict": "ACCEPTABLE"
    }
  }
}
```

#### Bulk Cargo Example

```json
{
  "@context": {
    "debulk": "https://hvdc-project.com/ontology/bulk/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "debulk:cargo-001",
  "@type": "debulk:Cargo",
  "debulk:hasCargoId": "CGO-2025-001",
  "debulk:hasCargoType": "Steel Structure",
  "debulk:hasWeight": 25.5,
  "debulk:hasDimensionL": 12.0,
  "debulk:hasDimensionW": 3.5,
  "debulk:hasDimensionH": 4.2,
  "debulk:hasCOGX": 6.0,
  "debulk:hasCOGY": 1.75,
  "debulk:hasCOGZ": 2.1,
  "debulk:isStackable": false,
  "debulk:placedOn": {
    "@type": "debulk:DeckArea",
    "debulk:hasAreaId": "DECK-A1",
    "debulk:hasUsableL": 15.0,
    "debulk:hasUsableW": 8.0,
    "debulk:hasMaxPointLoad": 50.0,
    "debulk:hasMaxUniformLoad": 10.0
  },
  "debulk:securedBy": {
    "@type": "debulk:LashingAssembly",
    "debulk:hasRequiredCapacity": 30.0,
    "debulk:hasCalcTension": 25.5,
    "debulk:hasSafetyFactor": 1.2
  }
}
```

### SPARQL Queries

#### Cost Analysis Query

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/>

SELECT
    ?vendor
    (COUNT(?invoice) AS ?invoiceCount)
    (SUM(?totalAmount) AS ?totalAmount)
    (AVG(?deltaPercent) AS ?avgDeltaPercent)
WHERE {
    ?invoice hvdc:hasVendor ?vendor .
    ?invoice hvdc:hasLine ?line .
    ?line hvdc:hasRiskResult ?risk .
    ?risk hvdc:hasDeltaPercent ?deltaPercent .
    ?line hvdc:hasDraftRateUSD ?rate .
    ?line hvdc:hasQuantity ?qty .
    BIND(?rate * ?qty AS ?totalAmount)
}
GROUP BY ?vendor
ORDER BY DESC(?totalAmount)
```

#### Cargo Stability Query

```sparql
PREFIX debulk: <https://hvdc-project.com/ontology/bulk/>

SELECT
    ?cargoId
    ?weight
    ?gm
    ?vcg
    (CASE
        WHEN ?gm > 0.5 THEN "STABLE"
        WHEN ?gm > 0.2 THEN "MARGINAL"
        ELSE "UNSTABLE"
    END AS ?stabilityStatus)
WHERE {
    ?cargo debulk:hasCargoId ?cargoId .
    ?cargo debulk:hasWeight ?weight .
    ?stability debulk:considers ?cargo .
    ?stability debulk:hasGM ?gm .
    ?stability debulk:hasVCG ?vcg .
}
ORDER BY DESC(?gm)
```

### Semantic KPI Layer

#### Cost Management KPIs

- **Cost Guard Compliance**: PASS/WARN/HIGH/CRITICAL 밴드 분포
- **Delta Percentage Distribution**: 요율 편차 통계
- **Vendor Performance**: 공급업체별 비용 효율성
- **Currency Conversion Accuracy**: USD 환율 적용 정확도

#### Bulk Cargo KPIs

- **Cargo Safety Index**: 안정성 기준 준수율
- **Lashing Efficiency**: 고박 용량 대비 실제 사용률
- **Deck Utilization**: 데크 면적 활용도
- **Equipment Utilization**: 장비 사용률

### 추천 명령어

- `/cost-guard analyze --vendor=DSV` [공급업체별 비용 분석]
- `/invoice-verify --strict` [청구서 검증]
- `/bulk-cargo-planning --stability-check` [벌크 화물 안정성 검사]
- `/lashing-calc --cargo=CGO-001` [고박 계산]
- `/stability-report --vessel=VSL-001` [안정성 리포트]

이 통합 온톨로지는 HVDC 프로젝트의 비용 관리와 벌크 화물 운영을 하나의 지식 그래프로 연결하여 데이터 일관성, 추적성, 자동화 가능성을 높입니다.
