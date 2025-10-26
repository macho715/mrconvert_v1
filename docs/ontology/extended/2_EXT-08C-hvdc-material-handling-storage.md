---
title: "HVDC Material Handling - Storage & Inland Transportation"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "3. Storage & Inland Transportation"
---

# hvdc-material-handling-hvdc-material-handling-storage · 2_EXT-08C

## Executive Summary

This document defines the ontology for **Storage & Inland Transportation** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Material storage standards and inland transportation

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:StorageLocation | (property list) | relatesTo → | (source) | status |
| mh:IndoorWarehouse | (property list) | relatesTo → | (source) | status |
| mh:OutdoorYard | (property list) | relatesTo → | (source) | status |
| mh:InlandTransport | (property list) | relatesTo → | (source) | status |

## How it works (flow)

Material handling workflow for HVDC project operations.

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

hvdc:Storage a owl:Class ;
    rdfs:label "Storage Facility" ;
    rdfs:comment "Storage facility (Indoor/Outdoor/Port/MOSB yards) - Indoor warehouses (6,000-8,000 sqm) for sensitive materials, outdoor yards for general cargo." .

hvdc:Laydown a owl:Class ;
    rdfs:label "Laydown Area" ;
    rdfs:comment "Site laydown areas (MIR: 35,006㎡, SHU: 10,556㎡, DAS: 35,840㎡, AGI: 47,198㎡)" .

hvdc:InlandTransport a owl:Class ;
    rdfs:label "Inland Transport" ;
    rdfs:comment "Inland transportation operations requiring DOT permit for >90t heavy equipment (Transformers, Spare Cable)" .

hvdc:Preservation a owl:Class ;
    rdfs:label "Material Preservation" ;
    rdfs:comment "Material preservation following Hitachi guidelines (Indoor: +5° to +40°C, RH ≤85%; Indoor heated: +15° to +25°C)" .
```

### Core Properties

```turtle
hvdc:follows a owl:ObjectProperty ;
    rdfs:domain hvdc:Storage ;
    rdfs:range hvdc:Procedure ;
    rdfs:comment "Storage follows Material Management Control Procedure and Annex J classification." .

hvdc:hosts a owl:ObjectProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Storage hvdc:Laydown) ] ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Storage location hosts cargo materials." .

hvdc:transports a owl:ObjectProperty ;
    rdfs:domain hvdc:InlandTransport ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Inland transport handles cargo delivery." .

hvdc:storageType a owl:DatatypeProperty ;
    rdfs:domain hvdc:Storage ;
    rdfs:range xsd:string ;
    rdfs:comment "Storage type: Indoor/Outdoor/Port/MOSB Yard." .

hvdc:areaSqm a owl:DatatypeProperty ;
    rdfs:domain [ owl:unionOf (hvdc:Storage hvdc:Laydown) ] ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Storage/laydown area in square meters." .

hvdc:tempRange a owl:DatatypeProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range xsd:string ;
    rdfs:comment "Temperature range (e.g., +5° to +40°C)." .

hvdc:humidityMax a owl:DatatypeProperty ;
    rdfs:domain hvdc:Preservation ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Maximum relative humidity (e.g., 85%)." .

hvdc:permitRequired a owl:DatatypeProperty ;
    rdfs:domain hvdc:InlandTransport ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether DOT permit is required." .
```

---

## Part 2: Constraints & Validation

### SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

hvdc:StorageShape a sh:NodeShape ;
    sh:targetClass hvdc:Storage ;
    sh:property [
        sh:path hvdc:storageType ;
        sh:in ("Indoor" "Outdoor" "Port" "MOSB Yard") ;
        sh:message "Storage type must be Indoor, Outdoor, Port, or MOSB Yard."
    ] ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 1000.0 ;
        sh:message "Storage area must be at least 1,000 sqm."
    ] .

hvdc:LaydownShape a sh:NodeShape ;
    sh:targetClass hvdc:Laydown ;
    sh:property [
        sh:path hvdc:areaSqm ;
        sh:minInclusive 10000.0 ;
        sh:message "Laydown area must be at least 10,000 sqm (per site requirements)."
    ] .

hvdc:PreservationShape a sh:NodeShape ;
    sh:targetClass hvdc:Preservation ;
    sh:property [
        sh:path hvdc:humidityMax ;
        sh:maxInclusive 85.0 ;
        sh:message "Maximum humidity must not exceed 85% (Hitachi requirement)."
    ] .

hvdc:InlandTransportShape a sh:NodeShape ;
    sh:targetClass hvdc:InlandTransport ;
    sh:property [
        sh:path hvdc:permitRequired ;
        sh:description "DOT permit required for cargo >90t."
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Indoor Warehouse Storage Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:indoor-warehouse-mir",
  "@type": "hvdc:Storage",
  "hvdc:storageType": "Indoor",
  "hvdc:areaSqm": 8000,
  "hvdc:follows": {
    "@id": "hvdc:procedure-annex-j"
  },
  "hvdc:hosts": [
    {
      "@id": "hvdc:cargo-hitachi",
      "hvdc:type": "Electrical Equipment",
      "hvdc:requiresPreservation": {
        "@type": "hvdc:Preservation",
        "hvdc:tempRange": "+5 to +40°C",
        "hvdc:humidityMax": 85
      }
    }
  ]
}
```

**Laydown Area Example**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:laydown-mir",
  "@type": "hvdc:Laydown",
  "hvdc:areaSqm": 35006,
  "hvdc:site": "MIR",
  "hvdc:dimensions": "373m x 193m"
}
```

### SPARQL Queries

**Available Storage Capacity Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?site ?type ?areaSqm ?available
WHERE {
    ?storage a hvdc:Storage ;
             hvdc:areaSqm ?areaSqm ;
             hvdc:storageType ?type .
    OPTIONAL {
        ?storage hvdc:hosts ?cargo .
        ?cargo hvdc:weight ?weight .
    }
    BIND(COALESCE(?areaSqm - SUM(?weight * 0.01), ?areaSqm) AS ?available)
}
GROUP BY ?storage ?site ?type ?areaSqm
HAVING (?available > 1000)
ORDER BY DESC(?available)
```

**Preservation Compliance Check**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?storage ?cargoType ?tempRange ?humidityMax ?compliant
WHERE {
    ?storage a hvdc:Storage ;
             hvdc:hosts ?cargo ;
             hvdc:follows ?procedure .
    ?cargo hvdc:type ?cargoType ;
           hvdc:requiresPreservation ?preservation .
    ?preservation hvdc:tempRange ?tempRange ;
                  hvdc:humidityMax ?humidityMax .
    BIND(IF(?humidityMax <= 85 && REGEX(?tempRange, "\\+5"), "COMPLIANT", "NON-COMPLIANT") AS ?compliant)
}
```

---

## Semantic KPI Layer

### Storage Operations KPIs

- **Storage Utilization Rate**: Percentage of available vs. used storage space (target: 70-85%)
- **Preservation Compliance Rate**: Adherence to temperature/humidity guidelines (Hitachi: ≥95%)
- **Heavy Transport Lead Time**: DOT permit approval to delivery time (SLA: ≤7 days)
- **Laydown Availability**: Site laydown readiness vs. construction schedule (≥95% availability)

---

## Recommended Commands

`/storage-plan optimize --site=MIR` [Site laydown optimization for MIR facility]
`/preservation check --material=Hitachi` [Preservation compliance verification for Hitachi equipment]
`/inland-transport permit --weight=120t` [DOT permit application for heavy cargo transport]
`/laydown-capacity query --site=DAS` [Available laydown capacity at DAS site]
`/storage-classification validate --annex-j` [Storage classification validation per Annex J]

---

## Original Content

### Main Text Content

### 3. Storage & Inland Transportation

These are the operation plans laydowns in each site.
Laydowns will be operated flexibly depending on the construction sequence.
Mirfa Shuweihat DAS Al Ghallan
### 1. 35,006 ㎡ (373m x 193m) 1. 10,556 ㎡ (203m x 52m) 1. 35,840 ㎡ (280m x 120m) 1. 47,198 ㎡ (3 areas)

### 2. For efficiency of Transformer 2. Transportation plan must be 2. Ground condition is good for 2. 3 laydowns need to be managed

delivery and to minimize interference, managed effectively due to narrow stable operation. separately.
### access road will be adjusted. space. 3. Sequence operation efficiency must 3. Security must be strengthened.

### 3. Storage container which is certified 3. Storage container which is certified be considered. Efficiency of sequence operation

### fire protection and equipped AC will fire protection and equipped AC will 4. Storage container which is certified efficiency must be considered.

be prepared in each site for be prepared in each site for fire protection and equipped AC will
chemical, dangerous cargo. chemical, dangerous cargo. be prepared in each site for
chemical, dangerous cargo.
.
1
3
### 3. Storage & Inland Transportation

Heavy equipments (Transformer, Spare Cable) transportation need a special permit (more
than 90TON) from DOT (Department of Transport).
Mina Zayed port
### Unloading/Storage LCT / Barge Inland Transport Site Offloading

MuggaraqPort
- Heavy vessel in Mina - Offloading by Vessel - Proper Vessel arrange - MIR/SHU - Preparation of Stool/Beam
Zayed Port (DAS/AGI/MIR) crane (LCT or Barge)
- From Mussafah Jetty to - Laydown Compaction
- SHU TR in the Muggaraq - Modular Trailer - Loading onto Vessel Site by Road
- Secure access Road
port
### - Stool & Beam for Storage - Sea fastening • Road survey

### - Storage / Preservation

- Preservation (DAS/AGI) • MIR to Mussafah Jetty, • DOT Permit
Inland transportation
• DAS/AGI to Island
1
4
### 4. Offshore Marine Transportation

(ADNOC L&S)
### 4. Offshore Marine Transportation

Comply with ADNOC Offshore HSE standards and carry out yard operation, loading, and
marine transportation in accordance with MOSB internal procedures.
Exit Gate Pass
STEP
1-Focal Point
06
2-Documents
Preparing Exit 3-Exit Gate (cargo)
STEP
1-Project BL Material
05
2-SCT Material
3-Returning Material
Operation LOLO & RORO
STEP
1-Request Crane ( Riggers )
04
Preparing both sides Shipping 2-Request Forklift
STEP
3-Lifting tools if required
1-Shipping (AGI & DAS) 03
2-Inspection by Lifting team
3-BL from Both Islands
Planning Documentation
STEP
Gate Pass 1-SCT-LDA ( receiving )
02
STEP 2-LDA Offloading
1-Focal Point
2-Documents 01 3-Filtering Planning(AGI-DAS)
3-Gate in (Visitors & Vendor cargo )
1
6
### 4. Offshore Marine Transportation

Through smooth communication with ADNOC L&S(ALS), we strive to comply with safety
regulations and ensure timely transportation. In island, ALS will handle same procedure for
offloading, inland transportation and site offloading.
Sub-con Email PL
1-Planning
2-Documents & Certificates.
Shift to Shipping yard
3-Checking Certificates.
4-Enter Gate Pass 1-ALS team collection loading from SCT-
LDA
Planning 2-load to vessel Before
Safety Check !!
Planning & PL
Operation
1-LDA Planning.
Lifting inspection & Certificates
2-Request Offloading Operation.
Inspection
3-coordinate with Island team. 1-Visit Lifting Inspection Office.
2-checking Certificates.
3-inspection SCT-LDA.
Shipping Schedule 4-Approval stamp to PL.
5-Handover Approval PL with Certificates.
1-receiving Priority Cargo Plan.
2-Arranging next Shipment According
Nearest Vessel Schedule. Wells Nu & Vessel Confirm
3-Preparing PL and Share with Island Team
1-Share PL with Certificates of Cargo.

### Tables and Data

### Table 1

| 3. Storage & Inland Transportation |
| --- |
| These are the operation plans laydowns in each site.
Laydowns will be operated flexibly depending on the construction sequence.
Mirfa Shuweihat DAS Al Ghallan
1. 35,006 ㎡ (373m x 193m) 1. 10,556 ㎡ (203m x 52m) 1. 35,840 ㎡ (280m x 120m) 1. 47,198 ㎡ (3 areas)
2. For efficiency of Transformer 2. Transportation plan must be 2. Ground condition is good for 2. 3 laydowns need to be managed
delivery and to minimize interference, managed effectively due to narrow stable operation. separately.
access road will be adjusted. space. 3. Sequence operation efficiency must 3. Security must be strengthened.
3. Storage container which is certified 3. Storage container which is certified be considered. Efficiency of sequence operation
fire protection and equipped AC will fire protection and equipped AC will 4. Storage container which is certified efficiency must be considered.
be prepared in each site for be prepared in each site for fire protection and equipped AC will
chemical, dangerous cargo. chemical, dangerous cargo. be prepared in each site for
chemical, dangerous cargo.
.
1
3 |

### Table 2

| Mirfa | Shuweihat | DAS | Al Ghallan |
| --- | --- | --- | --- |
| 1. 35,006 ㎡ (373m x 193m)
2. For efficiency of Transformer
delivery and to minimize interference,
access road will be adjusted.
3. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo. | 1. 10,556 ㎡ (203m x 52m)
2. Transportation plan must be
managed effectively due to narrow
space.
3. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo. | 1. 35,840 ㎡ (280m x 120m)
2. Ground condition is good for
stable operation.
3. Sequence operation efficiency must
be considered.
4. Storage container which is certified
fire protection and equipped AC will
be prepared in each site for
chemical, dangerous cargo.
. | 1. 47,198 ㎡ (3 areas)
2. 3 laydowns need to be managed
separately.
3. Security must be strengthened.
Efficiency of sequence operation
efficiency must be considered. |

### Table 3

| 3. Storage & Inland Transportation |
| --- |
| Heavy equipments (Transformer, Spare Cable) transportation need a special permit (more
than 90TON) from DOT (Department of Transport).
Mina Zayed port
Unloading/Storage LCT / Barge Inland Transport Site Offloading
MuggaraqPort
- Heavy vessel in Mina - Offloading by Vessel - Proper Vessel arrange - MIR/SHU - Preparation of Stool/Beam
Zayed Port (DAS/AGI/MIR) crane (LCT or Barge)
- From Mussafah Jetty to - Laydown Compaction
- SHU TR in the Muggaraq - Modular Trailer - Loading onto Vessel Site by Road
- Secure access Road
port
- Stool & Beam for Storage - Sea fastening • Road survey
- Storage / Preservation
- Preservation (DAS/AGI) • MIR to Mussafah Jetty, • DOT Permit
Inland transportation
• DAS/AGI to Island
1
4 |

### Table 4

| 4. Offshore Marine Transportation
(ADNOC L&S) |
| --- |

### Table 5

| 4. Offshore Marine Transportation |
| --- |
| Comply with ADNOC Offshore HSE standards and carry out yard operation, loading, and
marine transportation in accordance with MOSB internal procedures.
Exit Gate Pass
STEP
1-Focal Point
06
2-Documents
Preparing Exit 3-Exit Gate (cargo)
STEP
1-Project BL Material
05
2-SCT Material
3-Returning Material
Operation LOLO & RORO
STEP
1-Request Crane ( Riggers )
04
Preparing both sides Shipping 2-Request Forklift
STEP
3-Lifting tools if required
1-Shipping (AGI & DAS) 03
2-Inspection by Lifting team
3-BL from Both Islands
Planning Documentation
STEP
Gate Pass 1-SCT-LDA ( receiving )
02
STEP 2-LDA Offloading
1-Focal Point
2-Documents 01 3-Filtering Planning(AGI-DAS)
3-Gate in (Visitors & Vendor cargo )
1
6 |


*... and 3 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
