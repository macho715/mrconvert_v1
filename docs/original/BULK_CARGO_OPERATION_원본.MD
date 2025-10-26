# BULK CARGO OPERATION 온톨로지 심화 가이드

> 목적: Bulk/Project 화물 해상 운송(적재·양하·고박·안정성·인양) 전 과정을 **온톨로지(지식 그래프)**로 모델링하여 데이터 일관성, 추적성, 자동화 가능성을 높인다.

---

## 0) 범위·전제(Scoped Notes)

* 적용 범위: 철강 구조물, OOG, 프리캐스트(Hollow Core Slab), Breakbulk 전반.
* 목표 산출물: 클래스/속성 정의, 제약, 예시 인스턴스, 검증(SHACL), 교환 스키마(CSV), 쿼리(SPARQL) 샘플.
* 단위: 길이(m), 중량(t), 각도(deg), 좌표계: 선박 데크 로컬 좌표 (X fwd, Y port→stbd, Z keel→up) 예시.
* 책임 경계: 본 모델은 **데이터 표현/검증용**. 공학적 최종 판단(예: Stability 승인, 구조 검토)은 전문 SW/엔지니어 권한.

---

## 1) 상위 개념 계층(Top Taxonomy)

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

---

## 2) 핵심 클래스(Class)와 속성(Properties)

### 2.1 도메인 클래스 개요

| 클래스                  | 의미                        | 핵심 데이터속성(Data Properties)                                                                 | 핵심 객체속성(Object Properties)                                              |
| -------------------- | ------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| **Cargo**            | 운송 대상 개체(유닛/묶음)           | cargoId, cargoType, weight(t), dimL/W/H(m), cogX/Y/Z(m), stackable(boolean), hazmatClass? | placedOn→`DeckArea`, securedBy→`LashingAssembly`, handledBy→`Equipment` |
| **Vessel**           | 선박/바지                     | vesselName, imo?, deckStrength(t/m²), coordinateOrigin                                    | hasDeck→`DeckArea`, carries→`Cargo`, operatedBy→`Crew`                  |
| **DeckArea**         | 데크 구역/슬롯                  | areaId, usableL/W/H, maxPointLoad, maxUniformLoad                                         | partOf→`Vessel`, hosts→`Cargo`                                          |
| **LashingAssembly**  | 고박 체계(턴버클/체인/벨트 집합)       | requiredCapacity(t), calcTension(t), safetyFactor                                         | appliedTo→`Cargo`, uses→`LashingElement`, verifiedBy→`Engineer`         |
| **LashingElement**   | 체인/벨트/와이어 등 단품            | wll(t), angleDeg, count, length(m)                                                        | partOf→`LashingAssembly`                                                |
| **StabilityCase**    | 안정성 케이스(적재상태/해상상태)        | disp(t), vcg(m), gm(m), rollAngle(deg)                                                    | evaluates→`Vessel`, considers→`Cargo`                                   |
| **LiftingPlan**      | 인양 계획                     | liftId, method, slingAngleDeg, estLoadShare(t)                                            | for→`Cargo`, uses→`RiggingGear`, verifiedBy→`Engineer`                  |
| **RiggingGear**      | 슬링/샤클/스프레더                | gearId, type, wll(t), length(m)                                                           | partOf→`LiftingPlan`                                                    |
| **Equipment**        | 크레인/포크리프트/트레일러            | equipId, type, swl(t), radius(m)?                                                         | allocatedTo→`OperationTask`                                             |
| **Manpower**         | 인력(역할 기반)                 | personId, role, certificateId?, contact                                                   | assignedTo→`OperationTask`                                              |
| **OperationTask**    | 작업 단위(Planning/Loading 등) | taskId, status, start/end(DateTime), sequence                                             | relatesCargo→`Cargo`, uses→`Equipment`                                  |
| **Port/Jetty/Berth** | 위치/시설                     | code, draught, restriction                                                                | hosts→`OperationTask`                                                   |
| **Environment**      | 환경조건                      | wind(m/s), seaState, temp, accel_g                                                        | affects→`LashingAssembly`/`StabilityCase`                               |
| **Document**         | 문서/산출물                    | docId, type, version, fileRef                                                             | documents→(Plan/Report), about→(Vessel/Cargo)                           |

> 용어 팁: **LashingAssembly**는 ‘고박 설계 단위(세트)’를, **LashingElement**는 그 구성 부품을 의미.

### 2.2 속성 도메인/레인지(OWL 스타일 요약)

* `securedBy (Cargo → LashingAssembly)` [0..*]
* `appliedTo (LashingAssembly → Cargo)` [1..*]
* `uses (LashingAssembly → LashingElement)` [1..*]
* `placedOn (Cargo → DeckArea)` [1]
* `hosts (DeckArea → Cargo)` [0..*]
* `relatesCargo (OperationTask → Cargo)` [0..*]
* `allocatedTo (Equipment → OperationTask)` [0..*]
* `assignedTo (Manpower → OperationTask)` [0..*]
* `evaluates (StabilityCase → Vessel)` [1]
* `considers (StabilityCase → Cargo)` [0..*]
* `documents (Document → Plan/Report/Task)` [1..*]

### 2.3 제약(Constraints) 예시

* **Deck Strength**: `sum(load_i / footprint_i) ≤ deckStrength` (균등하중·점하중 모두 고려)
* **Lashing WLL**: `Σ(WLL_effective) ≥ requiredCapacity × SF` (SF≥2.0 예시)
* **Sling Angle**: 각도 작아질수록 다리장력 증가: `T_leg = W / (2 × sin(angle))`
* **Stability Gate**: `GM ≥ GM_min`, `VCG ≤ limitVCG`, `heel ≤ 5°` (예시 기준)

---

## 3) 라이프사이클/상태(State Machine)

| Phase     | 주요 Task      | 상태 전이                                    | 핵심 산출물                                           |
| --------- | ------------ | ---------------------------------------- | ------------------------------------------------ |
| Planning  | 데이터 수집·제약 정의 | Draft → Reviewed → Approved              | Loading Plan, Stowage Layout, Lashing Calc Sheet |
| Pre-Op    | 자원 배정·브리핑    | Ready → Mobilized                        | Equipment & Workforce Plan, JSA                  |
| Execution | 적재/고박/검사     | In-Progress → Paused/Resumed → Completed | QC Checklist, Photos, Survey Report              |
| Post-Op   | 서류/인계        | Completed → Archived                     | B/L, COA Evidence, Final Report                  |

---

## 4) 예시 인스턴스(직관용 Turtle)

```turtle
@prefix ex: <http://example.com/bulk#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Cargo_001 a ex:Cargo ;
  ex:cargoType "SteelStructure" ;
  ex:weight "42.5"^^xsd:decimal ;
  ex:dimL "12.0"^^xsd:decimal ; ex:dimW "3.2"^^xsd:decimal ; ex:dimH "3.5"^^xsd:decimal ;
  ex:cogX "5.8"^^xsd:decimal ; ex:cogY "0.0"^^xsd:decimal ; ex:cogZ "1.4"^^xsd:decimal ;
  ex:placedOn ex:Deck_A1 ;
  ex:securedBy ex:LashSet_01 .

ex:Deck_A1 a ex:DeckArea ;
  ex:areaId "A1" ; ex:usableL "20.0"^^xsd:decimal ; ex:usableW "10.0"^^xsd:decimal ;
  ex:maxUniformLoad "15.0"^^xsd:decimal .

ex:LashSet_01 a ex:LashingAssembly ;
  ex:requiredCapacity "1.2"^^xsd:decimal ;  # g·W / μ 등으로 산정된 필요 능력(예)
  ex:uses ex:Chain_10mm_1, ex:Chain_10mm_2 .

ex:Chain_10mm_1 a ex:LashingElement ; ex:wll "6.0"^^xsd:decimal ; ex:angleDeg "45"^^xsd:decimal .
ex:Chain_10mm_2 a ex:LashingElement ; ex:wll "6.0"^^xsd:decimal ; ex:angleDeg "45"^^xsd:decimal .

ex:Stab_LoadedCalm a ex:StabilityCase ;
  ex:gm "1.8"^^xsd:decimal ; ex:vcg "4.2"^^xsd:decimal ; ex:rollAngle "2.0"^^xsd:decimal ;
  ex:evaluates ex:Vessel_ABC ; ex:considers ex:Cargo_001 .
```

---

## 5) SHACL 검증 규칙(요지)

> 데이터 일관성/안전 최소 기준을 자동 검출

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.com/bulk#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:CargoShape a sh:NodeShape ;
  sh:targetClass ex:Cargo ;
  sh:property [ sh:path ex:weight ; sh:datatype xsd:decimal ; sh:minInclusive 0.1 ] ;
  sh:property [ sh:path ex:dimL ; sh:datatype xsd:decimal ; sh:minInclusive 0.1 ] ;
  sh:property [ sh:path ex:placedOn ; sh:minCount 1 ; sh:class ex:DeckArea ] .

ex:LashingAssemblyShape a sh:NodeShape ;
  sh:targetClass ex:LashingAssembly ;
  sh:property [ sh:path ex:uses ; sh:minCount 2 ; sh:class ex:LashingElement ] ;
  sh:rule [ a sh:SPARQLRule ;
    sh:prefixes ( ) ;
    sh:construct """
      CONSTRUCT { ?this ex:status "UNDER_CAPACITY" }
      WHERE {
        ?this ex:requiredCapacity ?req .
        {
          SELECT ?this (SUM(?effWll) AS ?sumWll)
          WHERE { ?this ex:uses ?e . ?e ex:wll ?w . ?e ex:angleDeg ?a .
                  BIND( (?w) * sin(?a * 3.14159/180) AS ?effWll ) }
          GROUP BY ?this
        }
        FILTER (?sumWll < (?req * 2.0))
      }
    """ ] .
```

*해석*: 라싱 요소의 유효 WLL(각도 보정 합계)이 요구능력×안전율(2.0) 미만이면 `UNDER_CAPACITY` 플래그.

---

## 6) 교환 스키마(Operational CSV/Excel 템플릿)

### 6.1 Cargo.csv

| cargoId | type           | weight_t | dimL_m | dimW_m | dimH_m | cogX_m | cogY_m | cogZ_m | stackable | placedOn |
| ------- | -------------- | -------: | -----: | -----: | -----: | -----: | -----: | -----: | :-------: | -------- |
| C001    | SteelStructure |     42.5 |   12.0 |    3.2 |    3.5 |    5.8 |    0.0 |    1.4 |   FALSE   | A1       |

### 6.2 LashingElements.csv

| lashId | type      | wll_t | angle_deg | length_m | assemblyId |
| ------ | --------- | ----: | --------: | -------: | ---------- |
| LE01   | Chain10mm |   6.0 |        45 |      8.0 | LS01       |

### 6.3 DeckAreas.csv

| areaId | vessel     | usableL_m | usableW_m | maxUniform_tpm2 | maxPoint_t |
| ------ | ---------- | --------: | --------: | --------------: | ---------: |
| A1     | Vessel_ABC |        20 |        10 |              15 |         60 |

### 6.4 Tasks.csv (스케줄·자원 배정)

| taskId | phase   | relatesCargo | start_utc        | end_utc          | eq_alloc  | manpower          |
| ------ | ------- | ------------ | ---------------- | ---------------- | --------- | ----------------- |
| T001   | Loading | C001         | 2025-11-02T06:00 | 2025-11-02T10:00 | Crane_M80 | Rigger3,Banksman2 |

---

## 7) 컴피턴시 질문(Competency Questions)

모델이 답해야 할 질의 정의(요구사항 유도용):

1. 특정 `Cargo`의 **총 라싱 유효용량**은 요구능력 대비 충분한가?
2. `DeckArea` A1에 적재된 화물들의 **평균/최대 접지하중**은 허용치 이내인가?
3. 주어진 `StabilityCase`에서 **총중량/VCG/GM 변화**는 기준을 만족하는가?
4. 반경 R에서 크레인의 **SWL ≥ 예상 훅하중**인가? 불충분 시 대체안은?
5. 야간조 작업에 필요한 **인력/자격증/연락망**은 배정되었는가?

---

## 8) SPARQL 질의 예시

```sparql
# Q1: Cargo별 라싱 유효용량 합계 추출
PREFIX ex: <http://example.com/bulk#>
SELECT ?cargo (SUM(?wll*sin(?a*pi()/180)) AS ?sumEffWll)
WHERE {
  ?cargo a ex:Cargo ; ex:securedBy ?ls .
  ?ls ex:uses ?e . ?e ex:wll ?wll ; ex:angleDeg ?a .
}
GROUP BY ?cargo
```

```sparql
# Q2: 데크 허용균등하중 대비 점검
PREFIX ex: <http://example.com/bulk#>
SELECT ?deck ?sumWeight ?area ?uniformLoad ?maxUL
WHERE {
  ?deck a ex:DeckArea ; ex:usableL ?L ; ex:usableW ?W ; ex:maxUniformLoad ?maxUL .
  BIND((?L*?W) AS ?area)
  { SELECT ?deck (SUM(?w) AS ?sumWeight)
    WHERE { ?cargo ex:placedOn ?deck ; ex:weight ?w } GROUP BY ?deck }
  BIND(?sumWeight / ?area AS ?uniformLoad)
}
```

---

## 9) 문서 매핑(Plans ↔ Ontology)

| 문서                        | 온톨로지 매핑                                            | 자동 생성 포인트                     |
| ------------------------- | -------------------------------------------------- | ----------------------------- |
| Vessel Loading Plan       | `OperationTask`, `DeckArea`, `Cargo`               | Gantt/테이블, COG 리스트, Layout 주석 |
| Seafastening/Lashing Plan | `LashingAssembly`, `LashingElement`, `Environment` | 각도·장력 표, 부족 용량 플래그            |
| Stability Report          | `StabilityCase`, `Vessel`, `Cargo`                 | 중량/VCG 집계 표, 한계 비교            |
| Lifting/Rigging Plan      | `LiftingPlan`, `RiggingGear`, `Equipment`          | 다리장력 계산 표, WLL 매칭 체크          |
| Logistics Execution Plan  | `OperationTask`, `Manpower`, `Equipment`           | 교대별 배정표, 연락처 리스트              |

---

## 10) 지배 규칙(정책·규정) 표현 패턴

* `ComplianceRule` 클래스로 규정 항목 정의(예: IMSBC, SOLAS, Port Notice).
* `appliesTo`(Rule→Class/Property), `threshold`(수치), `reference`(문헌식별), `jurisdiction`.
* 규정 점검은 **추론 규칙** 또는 **SHACL/SPARQL**로 구현.

---

## 11) 버전·추적성(Traceability)

* 모든 엔티티에 `version`, `createdAt`, `createdBy`, `sourceDoc` 부여.
* 변경 기록: `supersedes`(구버전), `wasDerivedFrom`(원데이터), `approvalStatus`.
* 파일 링크는 `Document.fileRef`(URI)로 관리.

---

## 12) 최소 OWL 스키마(발췌)

```turtle
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.com/bulk#> .

ex:Cargo a owl:Class ; rdfs:label "Cargo" .
ex:LashingAssembly a owl:Class .
ex:LashingElement a owl:Class .
ex:DeckArea a owl:Class .

ex:securedBy a owl:ObjectProperty ;
  rdfs:domain ex:Cargo ; rdfs:range ex:LashingAssembly .
ex:placedOn a owl:ObjectProperty ;
  rdfs:domain ex:Cargo ; rdfs:range ex:DeckArea .
ex:uses a owl:ObjectProperty ;
  rdfs:domain ex:LashingAssembly ; rdfs:range ex:LashingElement .

ex:weight a owl:DatatypeProperty .
ex:dimL a owl:DatatypeProperty .
ex:cogX a owl:DatatypeProperty .
```

---

## 13) 운영 적용 체크리스트(샘플)

* [ ] Cargo CSV에 **COG/중량/치수** 누락 없음
* [ ] DeckArea에 **허용하중(균등/점하중)** 입력 완료
* [ ] LashingElements **WLL·각도** 기입 및 세트 매핑 완료
* [ ] StabilityCase에 **GM/VCG/조건** 기록
* [ ] Equipment/Manpower **작업별 배정** 완료
* [ ] ComplianceRule **적용 관할** 선택
* [ ] 모든 문서 **버전·승인 상태** 표기

---

## 14) 차후 확장 포인트

* 3D 좌표(모델 ID) 연동, CAD/BIM 링크 속성(`modelRef`)
* 가속도 스펙트럼/항해 구간별 `Environment` 타임시리즈
* 비용/계약(`CostItem`, `LaytimeEvent`) 추가
* 포장/방수/내식(`Packaging`, `Protection`) 속성 추가

---

### 결론

이 온톨로지는 **계획↔실행↔검증**을 하나의 그래프로 잇는다.
동일 데이터를 문서, 체크리스트, 계산, 리포트로 **재사용**할 수 있게 해준다.
CSV/OWL/SHACL 샘플을 기반으로 바로 파일화를 진행하면 현장 적용 속도가 빨라진다.
