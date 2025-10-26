---
title: "HVDC Material Handling - Material Handling Overview"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "1. Overview"
---

# hvdc-material-handling-hvdc-material-handling-overview · 2_EXT-08A

## Executive Summary

This document defines the ontology for **Material Handling Overview** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Overall logistics workflow and port information

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:LogisticsFlow | (property list) | relatesTo → | (source) | status |
| mh:Port | (property list) | relatesTo → | (source) | status |
| mh:StorageLocation | (property list) | relatesTo → | (source) | status |
| mh:Project | (property list) | relatesTo → | (source) | status |

## How it works (flow)

1. **Import Planning**: Materials ordered and shipped to UAE ports
2. **Port Handling**: Heavy equipment at Zayed Port, containers at Khalifa Port
3. **Storage**: Materials stored in designated warehouses or outdoor yards
4. **Offshore Transport**: Special materials transported via LCT to offshore sites
5. **Site Receiving**: Materials received and inspected at on-site locations

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:Project a owl:Class ;
    rdfs:label "Project" ;
    rdfs:comment "Represents the HVDC project entity." .

hvdc:Phase a owl:Class ;
    rdfs:label "Phase" ;
    rdfs:comment "Logistics phases (A: Import, B: Offshore)." .

hvdc:Port a owl:Class ;
    rdfs:label "Port" ;
    rdfs:comment "Ports for cargo arrival (Khalifa, Zayed, Jebel Ali)." .

hvdc:MOSB a owl:Class ;
    rdfs:label "MOSB" ;
    rdfs:comment "Mussafah Offshore Supply Base - central logistics hub." .

hvdc:Site a owl:Class ;
    rdfs:label "Site" ;
    rdfs:comment "Onshore (MIR, SHU) and Offshore (DAS, AGI) sites." .

hvdc:Cargo a owl:Class ;
    rdfs:label "Cargo" ;
    rdfs:comment "Materials being handled in logistics operations." .
```

\```turtle
mh:LogisticsFlow a owl:Class ;
    rdfs:label "LogisticsFlow" ;
    rdfs:comment "Class representing logisticsflow" .

mh:Port a owl:Class ;
    rdfs:label "Port" ;
    rdfs:comment "Class representing port" .

mh:StorageLocation a owl:Class ;
    rdfs:label "StorageLocation" ;
    rdfs:comment "Class representing storagelocation" .

mh:Project a owl:Class ;
    rdfs:label "Project" ;
    rdfs:comment "Class representing project" .
\```

### Data Properties

```turtle
hvdc:hasPhase a owl:ObjectProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range hvdc:Phase .

hvdc:involves a owl:ObjectProperty ;
    rdfs:domain hvdc:Phase ;
    rdfs:range [ owl:unionOf (hvdc:Port hvdc:MOSB hvdc:Site) ] .

hvdc:handles a owl:ObjectProperty ;
    rdfs:domain hvdc:Port ;
    rdfs:range hvdc:Cargo .

hvdc:consolidates a owl:ObjectProperty ;
    rdfs:domain hvdc:MOSB ;
    rdfs:range hvdc:Cargo .

hvdc:dispatches a owl:ObjectProperty ;
    rdfs:domain hvdc:MOSB ;
    rdfs:range hvdc:Site .

hvdc:receives a owl:ObjectProperty ;
    rdfs:domain hvdc:Site ;
    rdfs:range hvdc:Cargo .

hvdc:projectName a owl:DatatypeProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range xsd:string .

hvdc:date a owl:DatatypeProperty ;
    rdfs:domain hvdc:Project ;
    rdfs:range xsd:date .

hvdc:phaseType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Phase ;
    rdfs:range xsd:string .

hvdc:name a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Port hvdc:Site) ] ;
    rdfs:range xsd:string .

hvdc:type a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Port hvdc:Site hvdc:Cargo) ] ;
    rdfs:range xsd:string .

hvdc:areaSqm a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:MOSB hvdc:Site) ] ;
    rdfs:range xsd:decimal .
```

\```turtle
mh:has_logisticsflowId a owl:DatatypeProperty ;
    rdfs:label "has logisticsflow ID" ;
    rdfs:domain mh:LogisticsFlow ;
    rdfs:range xsd:string .

mh:has_portId a owl:DatatypeProperty ;
    rdfs:label "has port ID" ;
    rdfs:domain mh:Port ;
    rdfs:range xsd:string .

mh:has_storagelocationId a owl:DatatypeProperty ;
    rdfs:label "has storagelocation ID" ;
    rdfs:domain mh:StorageLocation ;
    rdfs:range xsd:string .

\```

### Object Properties

\```turtle
# Example object properties
mh:locatedAt a owl:ObjectProperty ;
    rdfs:label "located at" ;
    rdfs:domain mh:Material ;
    rdfs:range mh:StorageLocation .
\```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
hvdc:ProjectShape a sh:NodeShape ;
    sh:targetClass hvdc:Project ;
    sh:property [
        sh:path hvdc:projectName ;
        sh:minCount 1 ;
        sh:message "Project must have a name."
    ] ;
    sh:property [
        sh:path hvdc:date ;
        sh:minCount 1 ;
        sh:message "Project must have a date."
    ] .

hvdc:PhaseShape a sh:NodeShape ;
    sh:targetClass hvdc:Phase ;
    sh:property [
        sh:path hvdc:phaseType ;
        sh:in ("A" "B") ;
        sh:message "Phase type must be A or B."
    ] .

hvdc:PortShape a sh:NodeShape ;
    sh:targetClass hvdc:Port ;
    sh:property [
        sh:path hvdc:name ;
        sh:minCount 1 ;
        sh:message "Port must have a name."
    ] ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("Container" "Bulk" "Special") ;
        sh:message "Port type must be Container, Bulk, or Special."
    ] .

hvdc:MOSBShape a sh:NodeShape ;
    sh:targetClass hvdc:MOSB ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 20000.0 ;
        sh:message "MOSB area must be at least 20,000 sqm."
    ] .

hvdc:SiteShape a sh:NodeShape ;
    sh:targetClass hvdc:Site ;
    sh:property [
        sh:path hvdc:name ;
        sh:minCount 1 ;
        sh:message "Site must have a name."
    ] ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("Onshore" "Offshore") ;
        sh:message "Site type must be Onshore or Offshore."
    ] ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 10000.0 ;
        sh:message "Site laydown area must be at least 10,000 sqm."
    ] .
```

\```turtle
mh:LogisticsFlowShape a sh:NodeShape ;
    sh:targetClass mh:LogisticsFlow ;
    sh:property [
        sh:path mh:has_logisticsflowId ;
        sh:minCount 1 ;
        sh:message "LogisticsFlow must have ID"
    ] .

mh:PortShape a sh:NodeShape ;
    sh:targetClass mh:Port ;
    sh:property [
        sh:path mh:has_portId ;
        sh:minCount 1 ;
        sh:message "Port must have ID"
    ] .
\```

---

## Part 3: Examples & Queries

### JSON-LD Examples

```turtle
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "hvdc:project-lightning",
  "@type": "hvdc:Project",
  "hvdc:projectName": "Independent Subsea HVDC System Project (Project Lightning)",
  "hvdc:date": "2024-11-19",
  "hvdc:hasPhase": [
    {
      "@type": "hvdc:Phase",
      "hvdc:phaseType": "A",
      "hvdc:involves": [
        {"@id": "hvdc:port-khalifa"},
        {"@id": "hvdc:port-zayed"}
      ]
    },
    {
      "@type": "hvdc:Phase",
      "hvdc:phaseType": "B",
      "hvdc:involves": [
        {"@id": "hvdc:mosb"},
        {"@id": "hvdc:site-das"}
      ]
    }
  ]
}
```

\```json
{
  "@context": {
    "mh": "https://hvdc-project.com/ontology/material-handling/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "mh:logisticsflow-001",
  "@type": "mh:LogisticsFlow",
  "mh:has_logisticsflowId": "MH-001",
  "mh:hasDescription": "Example logisticsflow"
}
\```

### SPARQL Queries

```turtle
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?phaseType ?entityId
WHERE {
    ?project hvdc:hasPhase ?phase .
    ?phase hvdc:phaseType ?phaseType ;
           hvdc:involves ?entity .
    ?entity @id ?entityId .
}
ORDER BY ?phaseType
```

\```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?logisticsflow ?description WHERE {
    ?logisticsflow a mh:LogisticsFlow .
    ?logisticsflow mh:hasDescription ?description .
}
LIMIT 10
\```

---



## Semantic KPI Layer

### Project Logistics KPIs
- **Phase Completion Rate**: Percentage of Phase A/B completions on schedule
- **Port Handling Efficiency**: Container/Bulk processing time vs. targets
- **MOSB Utilization**: Storage capacity utilization (%)
- **Site Receiving Timeliness**: Materials received vs. ETA
- **Document Compliance**: Customs clearance success rate (≥95%)


## Recommended Commands

/material-handling analyze --phase=A [Import stage analysis]
/material-handling predict-eta --site=MIR [ETA prediction with weather tie]
/material-handling kpi-dash --realtime [Real-time logistics dashboard]
/material-handling optimize-stowage --vessel=LCT [LCT stowage optimization]

---

## Original Content

### Main Text Content

### 1. Overview

### 1. Overview

Perform timely overseas and inland transportation for purchased materials.
DeugroKorea DSV UAE ADNOC L&S
Inland
### Shipping Customs Clearance Port Handling Storage LCT Site Offloading

### Transportation

A B
Overseas DAS / AGI
### 1. You can get comprehensive perspective of logistics in HVDC project. Port Remarks

### 2. Overseas importation (A stage) needs for customs clearance and port handling. Abu Dhabi Khalifa Container

### 3. Materials supplied in the UAE will be delivered to onshore Site. Abu Dhabi Mina zayed BULK

Dubai Jebel Ali CNTR/BULK
However, offshore site materials require B stage through using LCT.
### 4. When cargo arrives at the site, it is received according to the “Material Management Control

Procedure”.
5
### 1. Overview

UAE Port Information
- Heavy equipments in the Zayed Port, general containers in the Khalifa Port (Abu Dhabi)
- In special case suppliers will use via Jebel Ali free zone (Dubai)
- Offshore (DAS/AGI) marine transportation by ADNOC L&S (Mussafah base)
Zayed Port (ADB) Khalifa Port (ADB) Mussafah (ALS MOSB)
- Subsea Cable, Transformer, Land Cable - Most materials from overseas are imported in - Island material transportation base
- Heavy cargo operation containers. - ADNOC L&S (ALS) operation
- RORO berth for LCT or Barge - Container Terminal operation - Operation Yard (20,000sqm)
- SCT/JDN secured “storage area” - CCU (Cargo Carrying Unit) - Container, CCU
(Land cable, Transformer) total 80 ea
Addition
al
### Storage

Area
6
### 2. Customs Clearance


### Tables and Data

### Table 1

| 1. Overview |
| --- |

### Table 2

| 1. Overview |
| --- |
| Perform timely overseas and inland transportation for purchased materials.
DeugroKorea DSV UAE ADNOC L&S
Inland
Shipping Customs Clearance Port Handling Storage LCT Site Offloading
Transportation
A B
Overseas DAS / AGI
1. You can get comprehensive perspective of logistics in HVDC project. Port Remarks
2. Overseas importation (A stage) needs for customs clearance and port handling. Abu Dhabi Khalifa Container
3. Materials supplied in the UAE will be delivered to onshore Site. Abu Dhabi Mina zayed BULK
Dubai Jebel Ali CNTR/BULK
However, offshore site materials require B stage through using LCT.
4. When cargo arrives at the site, it is received according to the “Material Management Control
Procedure”.
5 |

### Table 3

| A |  |  |
| --- | --- | --- |
|  | A | Overseas |

### Table 4

| B |  |  |
| --- | --- | --- |
|  | B | DAS / AGI |

### Table 5

|  | Port | Remarks |
| --- | --- | --- |
| Abu Dhabi | Khalifa | Container |
| Abu Dhabi | Mina zayed | BULK |
| Dubai | Jebel Ali | CNTR/BULK |


*... and 2 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
