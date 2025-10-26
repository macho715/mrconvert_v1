---
title: "HVDC Material Handling - Site Receiving"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "5. Site Receiving"
---

# hvdc-material-handling-hvdc-material-handling-site-receiving · 2_EXT-08E

## Executive Summary

This document defines the ontology for **Site Receiving** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Site receiving and inspection procedures

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:MaterialReceiving | (property list) | relatesTo → | (source) | status |
| mh:Inspection | (property list) | relatesTo → | (source) | status |
| mh:MRR | (property list) | relatesTo → | (source) | status |
| mh:MaterialReceivingInspection | (property list) | relatesTo → | (source) | status |

## How it works (flow)

Material handling workflow for HVDC project operations.

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Receiving a owl:Class ;
    rdfs:label "Material Receiving" ;
    rdfs:comment "Site material receiving process following Material Management Control Procedure (Good/OSD classification)" .

hvdc:RequestSlip a owl:Class ;
    rdfs:label "Request Slip" ;
    rdfs:comment "Material request/issuance slips (MRS: Material Request Slip, MIS: Material Issue Slip)" .

hvdc:Inspection a owl:Class ;
    rdfs:label "Material Inspection" ;
    rdfs:comment "Material inspection documents (MRR: Material Receiving Report, MRI: Material Receiving Inspection, ITP: Inspection Test Plan, MAR: Material Approval Request)" .
```

### Core Properties

```turtle
hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:Receiving ;
    rdfs:range hvdc:Inspection ;
    rdfs:comment "Receiving requires joint inspection with OE/QA." .

hvdc:approves a owl:ObjectProperty ;
    rdfs:domain hvdc:RequestSlip ;
    rdfs:range hvdc:Team ;
    rdfs:comment "Request slip approved by Construction Team." .

hvdc:appliesTo a owl:ObjectProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Preservation guidelines apply to cargo." .

hvdc:receivingType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Receiving ;
    rdfs:range xsd:string ;
    rdfs:comment "Receiving type: Good or OSD (Overage, Shortage, Damage)." .

hvdc:slipType a owl:DatatypeProperty ;
    rdfs:domain hvdc:RequestSlip ;
    rdfs:range xsd:string ;
    rdfs:comment "Slip type: MRS or MIS." .

hvdc:inspectionResult a owl:DatatypeProperty ;
    rdfs:domain hvdc:Inspection ;
    rdfs:range xsd:string ;
    rdfs:comment "Inspection result status." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:ReceivingShape a sh:NodeShape ;
    sh:targetClass hvdc:Receiving ;
    sh:property [
        sh:path hvdc:receivingType ;
        sh:in ("Good" "OSD") ;
        sh:message "Receiving type must be Good or OSD."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Receiving must have required inspection."
    ] .

hvdc:RequestSlipShape a sh:NodeShape ;
    sh:targetClass hvdc:RequestSlip ;
    sh:property [
        sh:path hvdc:slipType ;
        sh:in ("MRS" "MIS") ;
        sh:message "Slip type must be MRS or MIS."
    ] ;
    sh:property [
        sh:path hvdc:approves ;
        sh:minCount 1 ;
        sh:message "Request slip must have approving team."
    ] .

hvdc:InspectionShape a sh:NodeShape ;
    sh:targetClass hvdc:Inspection ;
    sh:property [
        sh:path hvdc:inspectionResult ;
        sh:minCount 1 ;
        sh:message "Inspection must have result status."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Material Receiving with MRR Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:receiving-001",
  "@type": "hvdc:Receiving",
  "hvdc:receivingType": "Good",
  "hvdc:requires": {
    "@type": "hvdc:Inspection",
    "@id": "hvdc:inspection-mrr-001",
    "hvdc:type": "MRR",
    "hvdc:inspectionResult": "Accepted"
  },
  "hvdc:cargo": {
    "@id": "hvdc:cargo-hitachi-001",
    "hvdc:type": "Electrical Equipment"
  }
}
```

**Material Request Slip Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:slip-mrs-001",
  "@type": "hvdc:RequestSlip",
  "hvdc:slipType": "MRS",
  "hvdc:approves": {
    "@type": "hvdc:Team",
    "@id": "hvdc:team-construction"
  },
  "hvdc:status": "Approved"
}
```

### SPARQL Queries

**Receiving Status Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?receiving ?type ?inspectionResult ?status
WHERE {
    ?receiving a hvdc:Receiving ;
               hvdc:receivingType ?type ;
               hvdc:requires ?inspection .
    ?inspection hvdc:inspectionResult ?inspectionResult .
    OPTIONAL {
        ?receiving hvdc:relatedTo ?slip .
        ?slip hvdc:status ?status .
    }
}
ORDER BY ?type
```

**OSD Incident Report Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?receiving ?cargoType ?osdReason ?severity
WHERE {
    ?receiving a hvdc:Receiving ;
               hvdc:receivingType "OSD" ;
               hvdc:cargo ?cargo .
    ?cargo hvdc:type ?cargoType .
    ?receiving hvdc:hasDiscrepancy ?osdReason ;
               hvdc:severity ?severity .
}
ORDER BY DESC(?severity)
```

---

## Semantic KPI Layer

### Site Receiving KPIs

- **First-Time Acceptance Rate**: Percentage of cargo accepted without discrepancies (target: ≥90%)
- **Inspection Completion Time**: Average time from arrival to inspection completion (SLA: ≤24hrs)
- **OSD Incident Rate**: Overage, Shortage, Damage occurrences (target: ≤5%)
- **Request Slip Processing Time**: MRS to MIS issuance time (target: ≤48hrs)

---

## Recommended Commands

`/site-receiving inspect --cargo=TR-001` [Material inspection workflow for transformer cargo]
`/material-request generate --slip=MRS` [Material Request Slip generation and approval workflow]
`/preservation-check temperature --site=MIR` [Preservation temperature/humidity compliance check at site]
`/osd-report generate --type=damage` [OSD (Overage, Shortage, Damage) report generation]
`/inspection-document attach --type=ITP` [Joint inspection with OE/QA team, attach ITP/MAR documents]

---

---

## Original Content

### Main Text Content

### 5. Site Receiving

### Material Storage & Preservations

HANDLING &
INDOOR MATERIALS OUTDOOR &
PRESERVATION
OUTDOOR COVERED
•SCT to follow and implement
• The Manufacturer’s storage • Review of Manufacturer’s
### the Manufacturer’s storage instruction or guide shall be Storage Instructions and

instructions and guidelines reviewed before Guidelines
placing in storage and followed. • SCT to ensure that all OUTDOOR
•OUTDOOR,
• The air temperature shall be & OUTDOOR COVERED cases or
•OUTDOOR COVERED,
maintained as per boxes [HITACHI] are properly
•INDOOR Manufacturer’s Guidelines covered with tarpaulin or plastic
sheeting.
2
6
### 5. Site Receiving

FORMS
Loading & unloading checklist Material checklist
▪ For unloaded cargo, a visual check is
▪ For Loading and unloading checklist, this documents not only protect the cargo and the parties performed on the packaging and damage
involved in unloading works but also uphold the safety standards, and ensuring the compliance with status of the materials.
the transportation and safety regulation.
2
7
### 5. Site Receiving

FORMS
ITP
MRR
MAR
MRI
2
8
### 5. Site Receiving

FORMS
MATERIAL RECEIVING REPORT
MATERIAL REQUEST SLIP MATERIAL ISSUANCE SLIP
2
9
### 6. Material Handling

(Transformer)
### 6. Material Handling

Transformer Delivery Schedule [DAS Cluster]
▪ This transformer is manufactured in factory situated in Sweden.
▪ Hitachi transports to the relevant site. (SHU : Site, DAS: Zayed Port)
▪ Before arrival at the site, SCT prepares for receiving by submitting MS, approval and conducting FRA.
▪ Temporarily it is kept at Site or Zayed port before TR building complete
▪ During the storage, preservation is implemented according to Hitachi recommendations (Gauge measure - Dry air filling)
SHU DAS
Unit ETD ETA Arrival Port On-Site Unit ETD ETA Arrival Port On-Site
1 2024-04-09 2024-05-24 Mugharraq 2024-06-11 1 2024-02-19 2024-04-21 Mina Zayed 2024-11-03
2 2024-04-09 2024-05-24 Mugharraq 2024-06-11 2 2024-02-19 2024-04-21 Mina Zayed 2024-11-03
3 2024-04-09 2024-05-24 Mugharraq 2024-06-13 3 2024-07-11 2024-09-02 Mina Zayed Feb. 2025
4 2024-04-09 2024-05-24 Mugharraq 2024-06-13 4 2024-07-11 2024-09-02 Mina Zayed Feb. 2025
5 2024-05-16 2024-07-21 Mugharraq 2024-08-01 5 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
6 2024-05-16 2024-07-21 Mugharraq 2024-08-01 6 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
Spare 2024-05-16 2024-07-21 Mugharraq 2024-08-01 Spare 2024-07-11 2024-09-02 Mina Zayed Mar. 2025
3
1
### 6. Material Handling

Transformer Delivery Schedule [Zakum Cluster]
▪ This transformer is manufactured in a factory in Brazil.
▪ Hitachi is transporting to the relevant site. (MIR : Site, AGI: Zayed Port)
▪ Before arriving at the site, SCT prepare for receiving by submitting MS, approval and conducting FRA.
▪ Temporarily it is stored at Site or Zayed port before TR building is completed.
▪ During the storage, preservation is implemented according to Hitachi recommendations (Gauge measure – N2 gas flling)
MIR AGI
Unit ETD ETA Arrival Port On-Site Unit ETD ETA Arrival Port On-Site
1 2024-02-23 2024-03-31 Mina Zayed 2024-06-04 1 2024-08-01 2024-09-01 Mina Zayed Apr. 2025
2 2024-02-23 2024-03-31 Mina Zayed 2024-06-04 2 2024-08-01 2024-09-01 Mina Zayed Apr. 2025
3 2024-04-07 2024-04-29 Mina Zayed 2024-06-09 3 2024-09-30 2024-11-01 Mina Zayed May. 2025
4 2024-04-07 2024-04-29 Mina Zayed 2024-06-09 4 2024-09-30 2024-11-01 Mina Zayed May. 2025
5 2024-06-02 2024-07-25 Mina Zayed 2024-08-26 5 2024-09-30 2024-11-01 Mina Zayed May. 2025
6 2024-06-02 2024-07-25 Mina Zayed 2024-08-26 6 2024-10-25 2024-12-10 Mina Zayed Jun. 2025
Spare 2024-06-02 2024-07-25 Mina Zayed 2024-09-07 Spare 2024-10-25 2024-12-10 Mina Zayed Jun. 2025
3
2

### Tables and Data

### Table 1

| 5. Site Receiving |
| --- |
| Material Storage & Preservations
HANDLING &
INDOOR MATERIALS OUTDOOR &
PRESERVATION
OUTDOOR COVERED
•SCT to follow and implement
• The Manufacturer’s storage • Review of Manufacturer’s
the Manufacturer’s storage instruction or guide shall be Storage Instructions and
instructions and guidelines reviewed before Guidelines
placing in storage and followed. • SCT to ensure that all OUTDOOR
•OUTDOOR,
• The air temperature shall be & OUTDOOR COVERED cases or
•OUTDOOR COVERED,
maintained as per boxes [HITACHI] are properly
•INDOOR Manufacturer’s Guidelines covered with tarpaulin or plastic
sheeting.
2
6 |

### Table 2

| 5. Site Receiving |
| --- |
| FORMS
Loading & unloading checklist Material checklist
▪ For unloaded cargo, a visual check is
▪ For Loading and unloading checklist, this documents not only protect the cargo and the parties performed on the packaging and damage
involved in unloading works but also uphold the safety standards, and ensuring the compliance with status of the materials.
the transportation and safety regulation.
2
7 |

### Table 3

| 5. Site Receiving |
| --- |
| FORMS
ITP
MRR
MAR
MRI
2
8 |

### Table 4

| 5. Site Receiving |
| --- |
| FORMS
MATERIAL RECEIVING REPORT
MATERIAL REQUEST SLIP MATERIAL ISSUANCE SLIP
2
9 |

### Table 5

| 6. Material Handling
(Transformer) |
| --- |


*... and 6 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
