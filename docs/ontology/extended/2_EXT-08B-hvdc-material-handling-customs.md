---
title: "HVDC Material Handling - Customs Clearance"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "logistics", "operations"]
version: "unified-1.0"
date: "2024-11-19"
tags: ["ontology", "hvdc", "material-handling", "logistics", "workshop"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD"]
status: "active"
source: "HVDC_Material Handling Workshop_(20241119_1).pdf"
section: "2. Customs Clearance"
---

# hvdc-material-handling-hvdc-material-handling-customs · 2_EXT-08B

## Executive Summary

This document defines the ontology for **Customs Clearance** in the HVDC Material Handling Workshop conducted on 19th November 2024 for the Independent Subsea HVDC System Project (Project Lightning) in the UAE.

### Key Focus
Customs clearance procedures and documentation

### Project Context
- **Project**: Independent Subsea HVDC System Project (Project Lightning)
- **Location**: UAE
- **Workshop Date**: 19th November 2024
- **Workshop Type**: Material Handling Workshop

## Visual — 핵심 클래스/관계(요약)

| Class | 핵심 속성 | 관계 | 근거/조인 소스 | 결과 |
|-------|-----------|------|----------------|------|
| mh:CustomsDocument | (property list) | relatesTo → | (source) | status |
| mh:AttestationInvoice | (property list) | relatesTo → | (source) | status |
| mh:BLEndorsement | (property list) | relatesTo → | (source) | status |
| mh:CustomsDeclaration | (property list) | relatesTo → | (source) | status |

## How it works (flow)

1. **Document Preparation**: BL endorsement, attestation invoice preparation
2. **Customs Declaration**: Filing customs documents with ADNOC/ADOPT code
3. **Duty Payment**: Contractor pays duty and applies for reimbursement
4. **Clearance Completion**: Status shared with ADOPT for information

---

## Part 1: Domain Ontology

### Core Classes

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

hvdc:CustomsDeclaration a owl:Class ;
    rdfs:label "Customs Declaration" ;
    rdfs:comment "Customs clearance declaration process." .

hvdc:Document a owl:Class ;
    rdfs:label "Document" ;
    rdfs:comment "Shipping and customs documents (BL, Invoice, PL, CO)." .

hvdc:Consignee a owl:Class ;
    rdfs:label "Consignee" ;
    rdfs:comment "Recipient company (ADOPT/ADNOC codes)." .

hvdc:eDAS a owl:Class ;
    rdfs:label "eDAS System" ;
    rdfs:comment "Electronic Document Attestation System." .
```

\```turtle
mh:CustomsDocument a owl:Class ;
    rdfs:label "CustomsDocument" ;
    rdfs:comment "Class representing customsdocument" .

mh:AttestationInvoice a owl:Class ;
    rdfs:label "AttestationInvoice" ;
    rdfs:comment "Class representing attestationinvoice" .

mh:BLEndorsement a owl:Class ;
    rdfs:label "BLEndorsement" ;
    rdfs:comment "Class representing blendorsement" .

mh:CustomsDeclaration a owl:Class ;
    rdfs:label "CustomsDeclaration" ;
    rdfs:comment "Class representing customsdeclaration" .
\```

### Data Properties

```turtle
hvdc:submittedTo a owl:ObjectProperty ;
    rdfs:domain hvdc:Document ;
    rdfs:range hvdc:eDAS .

hvdc:endorses a owl:ObjectProperty ;
    rdfs:domain hvdc:Consignee ;
    rdfs:range hvdc:Document .

hvdc:declares a owl:ObjectProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range hvdc:Document .

hvdc:codeNo a owl:DatatypeProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range xsd:string .

hvdc:location a owl:DatatypeProperty ;
    rdfs:domain hvdc:CustomsDeclaration ;
    rdfs:range xsd:string .

hvdc:consigneeName a owl:DatatypeProperty ;
    rdfs:domain hvdc:Consignee ;
    rdfs:range xsd:string .
```

\```turtle
mh:has_customsdocumentId a owl:DatatypeProperty ;
    rdfs:label "has customsdocument ID" ;
    rdfs:domain mh:CustomsDocument ;
    rdfs:range xsd:string .

mh:has_attestationinvoiceId a owl:DatatypeProperty ;
    rdfs:label "has attestationinvoice ID" ;
    rdfs:domain mh:AttestationInvoice ;
    rdfs:range xsd:string .

mh:has_blendorsementId a owl:DatatypeProperty ;
    rdfs:label "has blendorsement ID" ;
    rdfs:domain mh:BLEndorsement ;
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
hvdc:CustomsDeclarationShape a sh:NodeShape ;
    sh:targetClass hvdc:CustomsDeclaration ;
    sh:property [
        sh:path hvdc:codeNo ;
        sh:minCount 1 ;
        sh:message "Customs declaration must have a code."
    ] .

hvdc:DocumentShape a sh:NodeShape ;
    sh:targetClass hvdc:Document ;
    sh:property [
        sh:path hvdc:type ;
        sh:in ("BL" "Invoice" "PL" "CO" "AWB") ;
        sh:message "Document type must be valid shipping/customs document."
    ] .

hvdc:ConsigneeShape a sh:NodeShape ;
    sh:targetClass hvdc:Consignee ;
    sh:property [
        sh:path hvdc:consigneeName ;
        sh:minCount 1 ;
        sh:message "Consignee must have a name."
    ] .
```

\```turtle
mh:CustomsDocumentShape a sh:NodeShape ;
    sh:targetClass mh:CustomsDocument ;
    sh:property [
        sh:path mh:has_customsdocumentId ;
        sh:minCount 1 ;
        sh:message "CustomsDocument must have ID"
    ] .

mh:AttestationInvoiceShape a sh:NodeShape ;
    sh:targetClass mh:AttestationInvoice ;
    sh:property [
        sh:path mh:has_attestationinvoiceId ;
        sh:minCount 1 ;
        sh:message "AttestationInvoice must have ID"
    ] .
\```

---

## Part 3: Examples & Queries

### JSON-LD Examples

```turtle
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/material-handling/"
  },
  "@id": "hvdc:customs-decl-001",
  "@type": "hvdc:CustomsDeclaration",
  "hvdc:codeNo": "CUSTOMS-ADNOC-47150",
  "hvdc:location": "Abu Dhabi",
  "hvdc:declares": {
    "@type": "hvdc:Document",
    "hvdc:type": "BL",
    "hvdc:submittedTo": "hvdc:edas-system"
  },
  "hvdc:endorses": {
    "@type": "hvdc:Consignee",
    "hvdc:consigneeName": "Abu Dhabi Offshore Power Transmission Company Limited LLC"
  }
}
```

\```json
{
  "@context": {
    "mh": "https://hvdc-project.com/ontology/material-handling/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
  },
  "@id": "mh:customsdocument-001",
  "@type": "mh:CustomsDocument",
  "mh:has_customsdocumentId": "MH-001",
  "mh:hasDescription": "Example customsdocument"
}
\```

### SPARQL Queries

```turtle
PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?declarationCode ?location ?documentType
WHERE {
    ?declaration a hvdc:CustomsDeclaration ;
                 hvdc:codeNo ?declarationCode ;
                 hvdc:location ?location ;
                 hvdc:declares ?doc .
    ?doc hvdc:type ?documentType .
}
ORDER BY ?declarationCode
```

\```sparql
PREFIX mh: <https://hvdc-project.com/ontology/material-handling/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?customsdocument ?description WHERE {
    ?customsdocument a mh:CustomsDocument .
    ?customsdocument mh:hasDescription ?description .
}
LIMIT 10
\```

---



## Semantic KPI Layer

### Customs Clearance KPIs
- **Clearance Time**: Average time from submission to approval
- **Document Accuracy**: First-time approval rate (≥98%)
- **Duty Accuracy**: Duty calculation accuracy (100%)
- **Compliance Rate**: Regulations adherence (UAE customs)


## Recommended Commands

/customs-clearance verify --docs [Document validation]
/customs-clearance track --status [Status tracking]
/customs-clearance analyze --duty [Duty calculation analysis]

---

## Original Content

### Main Text Content

### 2. Customs Clearance

### Customs clearance is carried out in compliance with UAE customs regulations and

appropriate shipping documents.
### Shipping Document eDAS System BL Endorsement Customs Clearance Delivery

### - BL (Bill of lading) - Attestation Invoice - BL endorsement - Customs Declaration - Delivery plan

by ADOPT
### or AWB (Airway Bill) - QR code * Shipping document - Transportation

(only Stamp)
* Attestation Invoice
- Commercial Invoice * Review Commercial
* Consignee : ADOPT
### Invoice and Customs

- Packing List
approval
- CO (Certificate of Origin)
### 1. Consignee Name : Abu Dhabi Offshore Power Transmission Company Limited LLC.

Location Description Code No
### - ADNOC (47150) was used as Customs code.

Abu Dhabi ADNOC 47150
### 2. In case of import via Dubai, we will use ADOPT (Dubai) code.

Abu Dhabi ADOPT 1485718
- Contractor pay Duty and apply for reimbursement. Dubai ADOPT 89901
- e.g. ZENER (Fire Fighting materials), from Jebel Ali free zone
### 3. Once customs clearance is completed, the status will be shared to ADOPT for their information.

8
### 2. Customs Clearance

### eDAS (Attestation Invoice) Customs Declaration Duty payment Status

9
### 3. Storage & Inland Transportation

### 3. Storage & Inland Transportation

Materials that arrived at the site should be operated according to the “Material Management
### Control Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”

### 1. Storage standards are operated according to Material Storage classification (Annex J)

### 2. In particular, materials from Hitachi are operated according to the standards settled by the

supplier. “operated' means that include all activities for offloading, material positioning and
storage, once cargos arrive at the site”
- It is specified in the “Case List” provided for each shipment.
### 3. Hitachi recommendation :

- Indoor : closed, controlled +5°to +40° C, maximum humidity 85%.
- Indoor heated : closed, controlled +15°to +25° C, maximum humidity 85%.
### 4. In addition, we plan to secure an indoor warehouse near MIR/SHU by September.

1
1
### 3. Storage & Inland Transportation

Delivery locations are designated and operated according to the characteristics of each site
and the conditions of storage.
Indoor warehouse Outdoor Yard Zayed port Yard MOSB Yard
- Temp controlled Indoor warehouse - Temporary storage for DAS/AGI - Temporary storage for DAS/AGI - Temporary storage for DAS/AGI
materials (eg. Hitachi) Transformer related materials
- Hitachi/Siemens electrical Materials
### - Mussafah Area (8,000sqm) - Port Storage (1,100sqm) - MOSB Storage (20,000sqm)

- Mussafah Area (6,000sqm)
- 10km from MOSB - While storage, preservation activity - Waiting for Loading operation
- 5km from MOSB
* Timely delivery as per installation * Timely delivery as per installation * Timely delivery as per installation
*SHU Indoor warehouse : 30th/Oct
time in sites time in sites time in sites
MIR Indoor warehouse : End of Nov
1
2

### Tables and Data

### Table 1

| 2. Customs Clearance |
| --- |
| Customs clearance is carried out in compliance with UAE customs regulations and
appropriate shipping documents.
Shipping Document eDAS System BL Endorsement Customs Clearance Delivery
- BL (Bill of lading) - Attestation Invoice - BL endorsement - Customs Declaration - Delivery plan
by ADOPT
or AWB (Airway Bill) - QR code * Shipping document - Transportation
(only Stamp)
* Attestation Invoice
- Commercial Invoice * Review Commercial
* Consignee : ADOPT
Invoice and Customs
- Packing List
approval
- CO (Certificate of Origin)
1. Consignee Name : Abu Dhabi Offshore Power Transmission Company Limited LLC.
Location Description Code No
- ADNOC (47150) was used as Customs code.
Abu Dhabi ADNOC 47150
2. In case of import via Dubai, we will use ADOPT (Dubai) code.
Abu Dhabi ADOPT 1485718
- Contractor pay Duty and apply for reimbursement. Dubai ADOPT 89901
- e.g. ZENER (Fire Fighting materials), from Jebel Ali free zone
3. Once customs clearance is completed, the status will be shared to ADOPT for their information.
8 |

### Table 2

| Location | Description | Code No |
| --- | --- | --- |
| Abu Dhabi | ADNOC | 47150 |
| Abu Dhabi | ADOPT | 1485718 |
| Dubai | ADOPT | 89901 |

### Table 3

| 2. Customs Clearance |
| --- |
| eDAS (Attestation Invoice) Customs Declaration Duty payment Status
9 |

### Table 4

| 3. Storage & Inland Transportation |
| --- |

### Table 5

| 3. Storage & Inland Transportation |
| --- |
| Materials that arrived at the site should be operated according to the “Material Management
Control Procedure(SJT-19LT-QLT-PL-023)-05.Oct.2022”
1. Storage standards are operated according to Material Storage classification (Annex J)
2. In particular, materials from Hitachi are operated according to the standards settled by the
supplier. “operated' means that include all activities for offloading, material positioning and
storage, once cargos arrive at the site”
- It is specified in the “Case List” provided for each shipment.
3. Hitachi recommendation :
- Indoor : closed, controlled +5°to +40° C, maximum humidity 85%.
- Indoor heated : closed, controlled +15°to +25° C, maximum humidity 85%.
4. In addition, we plan to secure an indoor warehouse near MIR/SHU by September.
1
1 |


*... and 1 more tables*

---

## Related Ontologies

- [Core Logistics Framework](../core/1_CORE-01-hvdc-core-framework.md)
- [Infrastructure Nodes](../core/1_CORE-02-hvdc-infra-nodes.md)
- [Warehouse Operations](../core/1_CORE-03-hvdc-warehouse-ops.md)
