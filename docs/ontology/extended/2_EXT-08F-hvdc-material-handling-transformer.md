---
title: "HVDC Material Handling - Material Handling - Transformer"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "6. Material Handling (Transformer)"
---

# hvdc-material-handling-hvdc-material-handling-transformer · 2_EXT-08F

## Executive Summary

This document defines the ontology for **Material Handling - Transformer** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Specialized transformer handling and safety procedures

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:Transformer | (property list) | relatesTo → | (source) | status |
| mh:LiftingEquipment | (property list) | relatesTo → | (source) | status |
| mh:Crane | (property list) | relatesTo → | (source) | status |
| mh:HandlingProcedure | (property list) | relatesTo → | (source) | status |
| mh:SafetyCheck | (property list) | relatesTo → | (source) | status |

## How it works (flow)

Material handling workflow for HVDC project operations.

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Transformer a owl:Class ;
    rdfs:label "Transformer Cargo" ;
    rdfs:comment "Transformer cargo (200t, DAS/Zakum clusters) - specialized heavy equipment handling" .

hvdc:Procedure a owl:Class ;
    rdfs:label "Handling Procedure" ;
    rdfs:comment "Handling procedures (Top-Up, On-Foundation, Skidding) with PTW, FRA, risk assessments" .

hvdc:PreservationCheck a owl:Class ;
    rdfs:label "Preservation Check" ;
    rdfs:comment "Impact recorder and gas top-up checks (Dry air for DAS cluster, N2 for Zakum cluster)" .

hvdc:LiftingPlan a owl:Class ;
    rdfs:label "Lifting Plan" ;
    rdfs:comment "SPMT/crane lifting operations with rigging gear, sling angles, load sharing" .
```

### Core Properties

```turtle
hvdc:transportedBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range [ owl:unionOf (hvdc:SPMT hvdc:LCT hvdc:Crane) ] ;
    rdfs:comment "Transformer transported by SPMT, LCT, or Crane equipment." .

hvdc:requires a owl:ObjectProperty ;
    rdfs:domain hvdc:Procedure ;
    rdfs:range [ owl:unionOf (hvdc:Equipment hvdc:Document hvdc:Permit) ] ;
    rdfs:comment "Procedure requires equipment, documents, and PTW." .

hvdc:performsOn a owl:ObjectProperty ;
    rdfs:domain hvdc:PreservationCheck ;
    rdfs:range hvdc:Transformer ;
    rdfs:comment "Preservation check performed on transformer." .

hvdc:unitNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:string ;
    rdfs:comment "Transformer unit number (e.g., DAS-1, AGI-1)." .

hvdc:ETD a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:date ;
    rdfs:comment "Estimated Time of Departure from origin." .

hvdc:ETA a owl:DatatypeProperty ;
    rdfs:domain hvdc:Transformer ;
    rdfs:range xsd:date ;
    rdfs:comment "Estimated Time of Arrival at port." .

hvdc:gaugeLevel a owl:DatatypeProperty ;
    rdfs:domain hvdc:PreservationCheck ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Preservation gauge level (weekly monitoring)." .

hvdc:method a owl:DatatypeProperty ;
    rdfs:domain hvdc:Procedure ;
    rdfs:range xsd:string ;
    rdfs:comment "Procedure method: Top-Up, On-Foundation, Skidding." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:TransformerShape a sh:NodeShape ;
    sh:targetClass hvdc:Transformer ;
    sh:property [
        sh:path hvdc:unitNo ;
        sh:minCount 1 ;
        sh:message "Transformer must have unit number."
    ] ;
    sh:property [
        sh:path hvdc:weight ;
        sh:minInclusive 100.0 ;
        sh:maxInclusive 250.0 ;
        sh:message "Transformer weight must be between 100-250t."
    ] .

hvdc:ProcedureShape a sh:NodeShape ;
    sh:targetClass hvdc:Procedure ;
    sh:property [
        sh:path hvdc:method ;
        sh:in ("Top-Up" "On-Foundation" "Skidding") ;
        sh:message "Procedure method must be Top-Up, On-Foundation, or Skidding."
    ] ;
    sh:property [
        sh:path hvdc:requires ;
        sh:minCount 1 ;
        sh:message "Procedure must have required equipment/documents."
    ] .

hvdc:PreservationCheckShape a sh:NodeShape ;
    sh:targetClass hvdc:PreservationCheck ;
    sh:property [
        sh:path hvdc:gaugeLevel ;
        sh:minInclusive 0.0 ;
        sh:message "Gauge level must be non-negative."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Transformer with SPMT Transport Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:transformer-das-1",
  "@type": "hvdc:Transformer",
  "hvdc:unitNo": "DAS-1",
  "hvdc:weight": 200.0,
  "hvdc:ETD": "2024-02-19",
  "hvdc:ETA": "2024-04-21",
  "hvdc:origin": "Sweden",
  "hvdc:arrivalPort": "Mina Zayed",
  "hvdc:transportedBy": {
    "@type": "hvdc:SPMT",
    "hvdc:capacity": 250,
    "hvdc:requires": {
      "@type": "hvdc:Document",
      "@id": "hvdc:ptw-001",
      "hvdc:type": "PTW"
    }
  },
  "hvdc:preservation": {
    "@type": "hvdc:PreservationCheck",
    "hvdc:gasType": "Dry air",
    "hvdc:gaugeLevel": 12.5
  }
}
```

**Lifting Plan Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:lifting-plan-das-1",
  "@type": "hvdc:LiftingPlan",
  "hvdc:method": "Skidding",
  "hvdc:for": "hvdc:transformer-das-1",
  "hvdc:uses": {
    "@type": "hvdc:RiggingGear",
    "hvdc:type": "Sling",
    "hvdc:slingAngle": 45
  },
  "hvdc:loadShare": 50.0
}
```

### SPARQL Queries

**Transformer Delivery Schedule Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?unit ?cluster ?ETD ?ETA ?onSite ?port ?status
WHERE {
    ?transformer a hvdc:Transformer ;
                 hvdc:unitNo ?unit ;
                 hvdc:cluster ?cluster ;
                 hvdc:ETD ?ETD ;
                 hvdc:ETA ?ETA ;
                 hvdc:arrivalPort ?port ;
                 hvdc:onSite ?onSite .
    OPTIONAL {
        ?transformer hvdc:transportStatus ?status .
    }
}
ORDER BY ?cluster ?unit
```

**Preservation Compliance Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?transformer ?unitNo ?gasType ?gaugeLevel ?lastCheck ?compliant
WHERE {
    ?transformer a hvdc:Transformer ;
                 hvdc:unitNo ?unitNo ;
                 hvdc:preservation ?check .
    ?check hvdc:gasType ?gasType ;
           hvdc:gaugeLevel ?gaugeLevel ;
           hvdc:lastCheck ?lastCheck .
    BIND(IF(?gaugeLevel >= 10.0 && ?lastCheck >= NOW() - "P7D"^^xsd:duration, "COMPLIANT", "NON-COMPLIANT") AS ?compliant)
}
ORDER BY ?unitNo
```

---

## Semantic KPI Layer

### Transformer Handling KPIs

- **On-Time Delivery Rate**: Actual vs. planned arrival (target: ≥95%)
- **Preservation Compliance**: Gauge level maintenance and gas top-up adherence (target: 100%)
- **Safety Incident Rate**: Zero target in lifting/stowage operations
- **Document Compliance Rate**: PTW, FRA, stability calc completeness (target: 100%)

---

## Recommended Commands

`/transformer-handle preserve --check=gauge` [Transformer preservation gauge level check and gas top-up procedure]
`/transformer-schedule track --unit=DAS-1` [Real-time transformer delivery schedule tracking]
`/spmt-operation plan --weight=200t` [SPMT operation planning with load distribution calculations]
`/lifting-plan generate --method=Skidding` [Lifting plan generation with rigging gear specifications]
`/preservation-log weekly --cluster=DAS` [Weekly preservation log review for DAS cluster transformers]

---

---

## Original Content

### Main Text Content

### 6. Material Handling

### Transportation Process [On-Shore_MIR,SHU]

▪ Unloading of the Heavy vessel is carried out at the port using a crane within own Vessel.
▪ When unloading, load directly onto the SPMT or Hydraulic Trailer on which the beam is mounted.
▪ Temporarily storage (Steel Mat, Stool and Beam) at the port before transport.
▪ Mirfa TRs are transported Barge from Mina Zayed to Mussafah (not allowed inland in Mina Zayed Road)
▪ Proceed with inland transportation after DOT prior approval and police approval (only night time)
### Unloading from Vessel Temporary Storage at port Barge Transportation Inland Transportation

3
3
### 6. Material Handling

### Transportation Process [Off Shore _ DAS,AGI] :

Transformers using SMPT equipment shipped an LCT vessel.
①Transformers are carefully lifted from the Vessel using ②Multiple transformers are securely positioned and ③Mats and stools are installed on the LCT deck to evenly
a crane and placed onto SMPT equipment for transport. fastened onto SMPT trailers, prepared for roll-on distribute the load and prepare for safe transformer
operations. placement..
④The LCT ramp is aligned and secured to facilitate the ⑤The roll-on operation begins, with SMPT equipment ⑥Final lashing and sea fastening are performed to secure
smooth movement of SMPT trailers onto the vessel deck. transporting the transformers onto the LCT vessel via the transformers safely for marine transportation.
the ramp.
3
4
### 6. Material Handling

### Transportation Process [Off Shore _ DAS,AGI] :

These documents are mandatory to be submitted prior to the roll-on/off operation of the transformer at the port to ensure safe and
efficient handling of the equipment. (28 to 30 page)
### 1.1 Preparation and Approvals

### 2. HSE Documentation:

### 1.Permit to Work (PTW):

### 1.Risk Assessments: Covering all operational activities.

### 1.Hot Work Permit:For lashing/sea fastening and cutting activities.

### 2.Method Statements:Detailed operational and safety guidelines.

### 2.Working Over Water Permit:For all operations conducted over water.

### 3.ADNOC Tide Table: Approved tide schedules to align operations with safety

### 3.HSE Approvals: Comprehensive approval for safety and environmental plans.

standards.
Hot Work Permit Risk Assessments
3
5
### 6. Material Handling

### 1.2 Technical Documents

### 3.SPMT and Loading Operations: 5. Mooring Operations:

### 1.SPMT Certificates:Pre-and post-inspection reports. 1.Mooring Arrangement Plan:Layout and pull force details (MT/KN).

### 2.RoRo Ramp Strength Calculation:Based on trailer axle loads and load 2.Mooring Rope Certificates:Compliance certifications.

### distribution. 3.Bollard SWL Certificate:Strength verification of bollards.

### 3.Stowage Plan:Transformer configuration and load arrangement on LCT.

### 6. Vessel Specifications:

### 4.Stability and Ballasting: 1.GA Plan:General arrangement drawings of the LCT.

### 1.Ballast Calculation:Stability adjustments and contingency planning. 2.Deck Strength Data:Structural integrity information

### 2.Stability Booklet:Documentation for LCT stability and draft planning

RoRo Ramp
Ballast Calculation Mooring Arrangement Plan
Strength Calculation
3
6
### 6. Material Handling

### 1.3 Operational Documentation

7. Work Plans and Schedules:
### 1.Sequence of Operations:Step-by-step workflow for Roll-On operations.

### 2.Tug and Pilot Plans:Scheduling of tugboats and pilots.

8. Completion Documentation:
### 1.Post-Loading Inspection Reports.

### 2.Completion Certificate for Roll-On Operations.

Document Name: Certificate of Sail away Approval(C.O.A)
Purpose:
The purpose of this document is to certify the approval for the sail away of two transformers.
It confirms that a pre-sailaway inspection was conducted, and the vessel was found fit for
the voyage.
Usage:
This certificate serves as official approval from the Marine Warranty Surveyor for the
transportation of the cargo by sea. It is used to ensure compliance with safety standards
and operational procedures for the voyage, providing assurance to stakeholders, insurers,
and relevant authorities.
3
7
### 6. Material Handling

### Site Receiving & Storage

▪ Conduct Site survey before transportation (checking turning radius, obstacles, etc.)
▪ Laydown Ground compaction and Mat, Stool positioning
▪ Safety induction prior works.
▪ Unloading works (Jackdown) will be performed under supervision of technical engineer (Al Faris & Mammoet).
▪ During the storage, preservation is implemented according to Hitachi recommendations (Dry air or N2 gas flling)
### Laydown –Mat, Stool Setup Backward In Jackdown& Receiving Storage & Preservation

▪ Beam replacement (June.2024)
▪ HE (7.5 m, transportation)
### → MMT (5.8 m. long term storage)

3
8
### 6. Material Handling

Check Impact Recorder & Preservation
▪ Mobile scaffolding will be used to check impact recorder and the condition of top side.
▪ Open protection box → four incident lamps are placed on the measuring unit → Test button is located to the right of the
incident lamps → Push the test button and release (with Hitachi engineer)
▪ For preservation, check the gauge measuring on weekly and make the log sheet.
▪ If under standard level, refill dry air (DAS cluster) and N2 gas (Zakum cluster)
Checking Impact Recorder Preservation (Gauge check, etc)
3
9
### 6. Material Handling

DRY AIR PRESSURE TOP UP PROCEDURE (Continued)
▪ Lifting Personnel to the Top of the Transformer

### Tables and Data

### Table 1

| 6. Material Handling |
| --- |
| Transportation Process [On-Shore_MIR,SHU]
▪ Unloading of the Heavy vessel is carried out at the port using a crane within own Vessel.
▪ When unloading, load directly onto the SPMT or Hydraulic Trailer on which the beam is mounted.
▪ Temporarily storage (Steel Mat, Stool and Beam) at the port before transport.
▪ Mirfa TRs are transported Barge from Mina Zayed to Mussafah (not allowed inland in Mina Zayed Road)
▪ Proceed with inland transportation after DOT prior approval and police approval (only night time)
Unloading from Vessel Temporary Storage at port Barge Transportation Inland Transportation
3
3 |

### Table 2

| 6. Material Handling |
| --- |
| Transportation Process [Off Shore _ DAS,AGI] :
Transformers using SMPT equipment shipped an LCT vessel.
①Transformers are carefully lifted from the Vessel using ②Multiple transformers are securely positioned and ③Mats and stools are installed on the LCT deck to evenly
a crane and placed onto SMPT equipment for transport. fastened onto SMPT trailers, prepared for roll-on distribute the load and prepare for safe transformer
operations. placement..
④The LCT ramp is aligned and secured to facilitate the ⑤The roll-on operation begins, with SMPT equipment ⑥Final lashing and sea fastening are performed to secure
smooth movement of SMPT trailers onto the vessel deck. transporting the transformers onto the LCT vessel via the transformers safely for marine transportation.
the ramp.
3
4 |

### Table 3

| 6. Material Handling |
| --- |
| Transportation Process [Off Shore _ DAS,AGI] :
These documents are mandatory to be submitted prior to the roll-on/off operation of the transformer at the port to ensure safe and
efficient handling of the equipment. (28 to 30 page)
1.1 Preparation and Approvals
2. HSE Documentation:
1.Permit to Work (PTW):
1.Risk Assessments: Covering all operational activities.
1.Hot Work Permit:For lashing/sea fastening and cutting activities.
2.Method Statements:Detailed operational and safety guidelines.
2.Working Over Water Permit:For all operations conducted over water.
3.ADNOC Tide Table: Approved tide schedules to align operations with safety
3.HSE Approvals: Comprehensive approval for safety and environmental plans.
standards.
Hot Work Permit Risk Assessments
3
5 |

### Table 4


### Table 5



*... and 8 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
