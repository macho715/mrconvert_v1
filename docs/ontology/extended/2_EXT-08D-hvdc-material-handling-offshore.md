---
title: "HVDC Material Handling - Offshore Marine Transportation"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "4. Offshore marine Transportation"
---

# hvdc-material-handling-hvdc-material-handling-offshore · 2_EXT-08D

## Executive Summary

This document defines the ontology for **Offshore Marine Transportation** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Offshore marine transportation procedures

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:LCT | (property list) | relatesTo → | (source) | status |
| mh:MarineTransport | (property list) | relatesTo → | (source) | status |
| mh:OffshoreRoute | (property list) | relatesTo → | (source) | status |
| mh:Barge | (property list) | relatesTo → | (source) | status |

## How it works (flow)

Material handling workflow for HVDC project operations.

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:MarineTransport a owl:Class ;
    rdfs:label "Marine Transport" ;
    rdfs:comment "Offshore marine transportation via LCT (MOSB-DAS: 20hrs, MOSB-AGI: 10hrs)" .

hvdc:OperationStep a owl:Class ;
    rdfs:label "Operation Step" ;
    rdfs:comment "MOSB operation steps (Gate pass → Planning → Operation LOLO/RORO → Exit)" .

hvdc:Inspection a owl:Class ;
    rdfs:label "Lifting Inspection" ;
    rdfs:comment "Lifting inspection and safety checks at MOSB and island sites" .

hvdc:HSEStandard a owl:Class ;
    rdfs:label "HSE Standard" ;
    rdfs:comment "ADNOC Offshore HSE compliance standards for ALS operations" .
```

### Core Properties

```turtle
hvdc:compliesWith a owl:ObjectProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range hvdc:HSEStandard ;
    rdfs:comment "Marine transport complies with ADNOC Offshore HSE standards." .

hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range [ owl:unionOf (hvdc:Document hvdc:Permit) ] ;
    rdfs:comment "Operation step requires documentation and permits." .

hvdc:validates a owl:ObjectProperty ;
    rdfs:domain hvdc:Inspection ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Inspection validates cargo condition." .

hvdc:voyageTime a owl:DatatypeProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range xsd:integer ;
    rdfs:comment "Voyage time in hours (e.g., MOSB-DAS: 20hrs)" .

hvdc:vesselType a owl:DatatypeProperty ;
    rdfs:domain hvdc:MarineTransport ;
    rdfs:range xsd:string ;
    rdfs:comment "Vessel type: LCT or Barge" .

hvdc:stepNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range xsd:integer ;
    rdfs:comment "Operation step number (1-6)." .

hvdc:operationType a owl:DatatypeProperty ;
    rdfs:domain hvdc:OperationStep ;
    rdfs:range xsd:string ;
    rdfs:comment "Operation type: LOLO or RORO" .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:MarineTransportShape a sh:NodeShape ;
    sh:targetClass hvdc:MarineTransport ;
    sh:property [
        sh:path hvdc:vesselType ;
        sh:in ("LCT" "Barge") ;
        sh:message "Vessel type must be LCT or Barge."
    ] ;
    sh:property [
        sh:path hvdc:voyageTime ;
        sh:minInclusive 1 ;
        sh:message "Voyage time must be positive (minimum 1 hour)."
    ] .

hvdc:OperationStepShape a sh:NodeShape ;
    sh:targetClass hvdc:OperationStep ;
    sh:property [
        sh:path hvdc:stepNo ;
        sh:minInclusive 1 ;
        sh:maxInclusive 6 ;
        sh:message "Step number must be between 1 and 6."
    ] ;
    sh:property [
        sh:path hvdc:operationType ;
        sh:in ("LOLO" "RORO") ;
        sh:message "Operation type must be LOLO or RORO."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Operation step must have required documentation."
    ] .

hvdc:HSEStandardShape a sh:NodeShape ;
    sh:targetClass hvdc:HSEStandard ;
    sh:property [
        sh:path hvdc:complianceLevel ;
        sh:minCount 1 ;
        sh:message "HSE standard must have compliance level."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**LCT Voyage Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:voyage-mosb-das-001",
  "@type": "hvdc:MarineTransport",
  "hvdc:vesselType": "LCT",
  "hvdc:voyageTime": 20,
  "hvdc:route": "MOSB to DAS",
  "hvdc:compliesWith": {
    "@type": "hvdc:HSEStandard",
    "@id": "hvdc:hse-adnoc-offshore"
  },
  "hvdc:operationSteps": [
    {
      "@type": "hvdc:OperationStep",
      "hvdc:stepNo": 1,
      "hvdc:operationType": "Gate Pass",
      "hvdc:requires": ["Focal Point", "Documents", "Gate in"]
    },
    {
      "@type": "hvdc:OperationStep",
      "hvdc:stepNo": 4,
      "hvdc:operationType": "LOLO",
      "hvdc:requires": ["Crane Request", "Forklift Request", "Lifting tools"]
    }
  ]
}
```

**MOSB Operation Flow Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:operation-mosb-001",
  "@type": "hvdc:OperationStep",
  "hvdc:stepNo": 3,
  "hvdc:operationType": "Shipping",
  "hvdc:focalPoint": "ALS team",
  "hvdc:requires": {
    "@type": "hvdc:Document",
    "hvdc:type": "Packing List"
  },
  "hvdc:validates": {
    "@type": "hvdc:Inspection",
    "hvdc:type": "Lifting"
  }
}
```

### SPARQL Queries

**Marine Transport Schedule Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?voyage ?route ?voyageTime ?vesselType ?delays
WHERE {
    ?voyage a hvdc:MarineTransport ;
             hvdc:route ?route ;
             hvdc:voyageTime ?voyageTime ;
             hvdc:vesselType ?vesselType .
    OPTIONAL {
        ?voyage hvdc:hasDelay ?delays .
    }
}
ORDER BY ?route
```

**HSE Compliance Check Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?operation ?stepNo ?hseCompliant ?requiredDocs
WHERE {
    ?operation a hvdc:OperationStep ;
                hvdc:stepNo ?stepNo ;
                hvdc:requires ?document .
    ?operation hvdc:compliesWith ?hse .
    ?hse a hvdc:HSEStandard .
    OPTIONAL {
        ?operation hvdc:requires ?docList .
        ?docList hvdc:type ?requiredDocs .
    }
    BIND(IF(BOUND(?hse), "COMPLIANT", "NON-COMPLIANT") AS ?hseCompliant)
}
ORDER BY ?stepNo
```

---

## Semantic KPI Layer

### Offshore Marine Operations KPIs

- **Voyage Efficiency Rate**: Actual vs. planned transit times (MOSB-DAS: 20hrs, MOSB-AGI: 10hrs)
- **HSE Compliance Score**: ADNOC Offshore HSE adherence (target: ≥95%)
- **LOLO/RORO Operation Time**: Average operation duration per step (target: ≤4hrs)
- **Document Completeness Rate**: Required documentation availability (target: 100%)

---

## Recommended Commands

`/marine-transport schedule --voyage=MOSB-DAS` [Real-time LCT voyage scheduling from MOSB to DAS island]
`/hse-check validate --operation=LOLO` [HSE compliance validation for LOLO operations]
`/lct-tracking realtime --vessel=LCT-001` [Real-time LCT vessel tracking and status updates]
`/mosb-operation status --step=4` [MOSB operation step status and progress]
`/voyage-delay analyze --route=MOSB-AGI` [Voyage delay analysis and root cause identification]

---

## Original Content

### Main Text Content

### 5. Site Receiving

### 5. Site Receiving

Materials arriving on site are operated according to the “Material Management Control
### Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

### 1. Upon arrive the materials, inspection (with QA/QC) is performed while unpacking

at the time of installation.
### 2. Visual inspection is performed on materials that arrive before construction, and

when materials are released during construction, inspection is performed as above.
### 3. Upon request for inspection, following document will be attached

- Material Inspection Request (Logistic – Construction – Quality – OE)
### - Material Receiving inspection Report

### - Materials Receiving Inspection

- ITP (Inspection and Test plan)
- MAR (Material Approval Request)
- Product test certificate
### 4. As per the site requirement relevant Sub Con Submitting MRS (Material Request

Slip) with relevant drawings.
### 5. After verification and approval from Construction Team proceeding for MIS

(Material Issue Slip) as per the availability of materials.
### 6. Physical issuance of materials to as per the MIS and getting receiving

acknowledgement from Sub con representative in MIS
2
0
### 5. Site Receiving

Materials arriving on site are operated according to the “Material Management Control
### Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

Delivery Plan / Schedule
SUPPLIER / VENDOR SCT PREPARATION HSE SAFETY
•Supplier to provide the •Review packing List •HSE standards -to ensure safety of
workplace and organized process in
### delivery plan which includes •Material Storage Code

receiving materials, equipment, and
the following:
•Alignment of Equipment personnel on-site.
•➢ Packing List availability vs the proposed •➢Verification and Documentation:
Methodology > MS / FRA
•➢Delivery Truck Quantity delivery plan of the Supplier
•➢Hazard Assessment
•➢ETA at Site / Vendor
•➢Control of Entry Points
•➢Target Delivery •Unloading Location •➢Inspection and Compliance
Completion •➢Clear Communication
2
1
### 5. Site Receiving

### Material Receiving

PACKING LIST, LOADING & PERMITS, LIFTING EQUIPMENT & MATERIAL RECEIVING
MANPOWER
UNLOADING CHECKLIST REPORT & INSPECTION
• Collection of Packing • Permit to Work [PTW] •SCT to conduct material
receiving inspection
List, Delivery Notes, and • Tool Box Talk
•Thorough checking of Material
other shipping
• Inspection of Lifting received vs. Packing list.
documents
Equipment and Lifting •SCT to provide MRR if cargo
• Collection of Loading Gears found in good condition and
and Unloading Checklist acceptable
2
2
### 5. Site Receiving

Request for Inspection
MATERIAL IN GOOD DOCUMENTS TO JOINT INSPECTION WITH
CONDITION OE
PREPARE
•Material Inspection Request
• If the cargo is found to be • Joint inspection
(Logistic – Construction –
in good condition and the Quality – OE) together with OE to
### quantity matches packing •➢Material Receiving inspection ensure that material

Report
list, proceed with the received at site meet
### •➢Materials Receiving Inspection

request for inspection •➢ITP (Inspection and Test plan) the required standards
•➢MAR (Material Approval
and specifications as
Request)
per ITP / MAR
•➢Product test certificate [MTC,
SDS, TDS]
2
3
### 5. Site Receiving

Overage, Shortage & Damage Report
OVERAGE, SHORTAGE,
DOCUMENTS TO REVIEW and ACTION
DAMAGE
PREPARE
•If found any overage, shortage,
• Overage, Shortage, • OSD Report shall be
damage, during receiving, SCT
to file an OSDR Damage Report sent to the QA/QC add
documentation. Form Contranctor’s PMO for
•Thorough inspection carried • Commercial Invoice / subsequent action such
out together with Engineering Packing List as claim to the Vendor
Team, and QA/QC Team
/ Supplier
• Delivery Note
• Photo Proof

### Tables and Data

### Table 1

| 5. Site Receiving |
| --- |

### Table 2

| 5. Site Receiving |
| --- |
| Materials arriving on site are operated according to the “Material Management Control
Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
1. Upon arrive the materials, inspection (with QA/QC) is performed while unpacking
at the time of installation.
2. Visual inspection is performed on materials that arrive before construction, and
when materials are released during construction, inspection is performed as above.
3. Upon request for inspection, following document will be attached
- Material Inspection Request (Logistic – Construction – Quality – OE)
- Material Receiving inspection Report
- Materials Receiving Inspection
- ITP (Inspection and Test plan)
- MAR (Material Approval Request)
- Product test certificate
4. As per the site requirement relevant Sub Con Submitting MRS (Material Request
Slip) with relevant drawings.
5. After verification and approval from Construction Team proceeding for MIS
(Material Issue Slip) as per the availability of materials.
6. Physical issuance of materials to as per the MIS and getting receiving
acknowledgement from Sub con representative in MIS
2
0 |

### Table 3

| 5. Site Receiving |
| --- |
| Materials arriving on site are operated according to the “Material Management Control
Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
Delivery Plan / Schedule
SUPPLIER / VENDOR SCT PREPARATION HSE SAFETY
•Supplier to provide the •Review packing List •HSE standards -to ensure safety of
workplace and organized process in
delivery plan which includes •Material Storage Code
receiving materials, equipment, and
the following:
•Alignment of Equipment personnel on-site.
•➢ Packing List availability vs the proposed •➢Verification and Documentation:
Methodology > MS / FRA
•➢Delivery Truck Quantity delivery plan of the Supplier
•➢Hazard Assessment
•➢ETA at Site / Vendor
•➢Control of Entry Points
•➢Target Delivery •Unloading Location •➢Inspection and Compliance
Completion •➢Clear Communication
2
1 |

### Table 4

| 5. Site Receiving |
| --- |
| Material Receiving
PACKING LIST, LOADING & PERMITS, LIFTING EQUIPMENT & MATERIAL RECEIVING
MANPOWER
UNLOADING CHECKLIST REPORT & INSPECTION
• Collection of Packing • Permit to Work [PTW] •SCT to conduct material
receiving inspection
List, Delivery Notes, and • Tool Box Talk
•Thorough checking of Material
other shipping
• Inspection of Lifting received vs. Packing list.
documents
Equipment and Lifting •SCT to provide MRR if cargo
• Collection of Loading Gears found in good condition and
and Unloading Checklist acceptable
2
2 |

### Table 5

| 5. Site Receiving |
| --- |
| Request for Inspection
MATERIAL IN GOOD DOCUMENTS TO JOINT INSPECTION WITH
CONDITION OE
PREPARE
•Material Inspection Request
• If the cargo is found to be • Joint inspection
(Logistic – Construction –
in good condition and the Quality – OE) together with OE to
quantity matches packing •➢Material Receiving inspection ensure that material
Report
list, proceed with the received at site meet
•➢Materials Receiving Inspection
request for inspection •➢ITP (Inspection and Test plan) the required standards
•➢MAR (Material Approval
and specifications as
Request)
per ITP / MAR
•➢Product test certificate [MTC,
SDS, TDS]
2
3 |


*... and 2 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
