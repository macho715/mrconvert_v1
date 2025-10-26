---
title: "HVDC Material Handling & Bulk Cargo Ontology - Integrated"
type: "ontology-design"
domain: "material-handling-bulk-cargo"
sub-domains: ["bulk-cargo-operations", "seafastening", "stability-control", "lashing", "lifting"]
version: "integrated-1.0"
date: "2025-01-09"
tags: ["bulk-cargo", "stowage", "lashing", "stability", "lifting-plan", "integrated"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "IMSBC", "SOLAS"]
status: "active"
source_files: ["HVDC_Material Handling Workshop_(20241119_1).pdf", "1_CORE-05-hvdc-bulk-cargo-ops.md"]
---

# hvdc-material-handling-bulk-integrated · 2_EXT-08G

## Executive Summary

This integrated ontology combines material handling processes from the HVDC Material Handling Workshop with bulk cargo operations, creating a unified knowledge graph for the Independent Subsea HVDC System Project (Project Lightning) in the UAE. It encompasses overseas importation (Phase A), offshore marine transportation (Phase B), and detailed bulk cargo handling including planning, loading/discharging, stowage/lashing, stability control, and lifting operations.

### Key Integration Points

- **Material Handling Workflows**: Overview, Customs, Storage, Offshore Transport, Site Receiving, Transformer handling
- **Bulk Cargo Operations**: Stowage planning, lashing assemblies, stability calculations, lifting plans with rigging gear
- **Unified Classes**: Cargo, Vessel, DeckArea, LashingAssembly, StabilityCase, LiftingPlan
- **Compliance Standards**: UAE customs, ADNOC HSE, IMSBC, SOLAS, supplier preservation guidelines

## Visual — 핵심 클래스/관계(통합 요약)

| Class | Key Properties | Relations | Basis/Join Source | Outcome |
|-------|---------------|-----------|-------------------|---------|
| hvdc:Cargo | cargoId, type, weight(t), dimsL/W/H(m), cogX/Y/Z(m), stackable(boolean) | placedOn → DeckArea, securedBy → LashingAssembly, handledBy → Equipment | Material Handling + Bulk Ops | Status, Integrity |
| hvdc:Vessel | vesselName, imo?, deckStrength(t/m²) | hasDeck → DeckArea, carries → Cargo | Vessel Registry | Operational Status |
| hvdc:DeckArea | areaId, usableL/W/H, maxPointLoad | partOf → Vessel, hosts → Cargo | Deck Layout | Load Capacity |
| hvdc:LashingAssembly | requiredCapacity(t), calcTension(t), safetyFactor | appliedTo → Cargo, uses → LashingElement | Lashing Calc | Securing Strength |
| hvdc:StabilityCase | disp(t), vcg(m), gm(m), rollAngle(deg) | evaluates → Vessel, considers → Cargo | Stability Calc | Stability Status |
| hvdc:LiftingPlan | liftId, method, slingAngleDeg | for → Cargo, uses → RiggingGear | Rigging Design | Lifting Plan |
| hvdc:Environment | wind(m/s), seaState, temp | affects → LashingAssembly/StabilityCase | Weather API | Environmental Impact |

## How it Works (Integrated Flow)

**Planning Phase**: Data collection/constraints → Draft/Reviewed/Approved plans (stowage, lashing, stability, lifting)
**Pre-Operation**: Resource allocation/briefing → Mobilized (JSA, PTW, equipment checks)
**Execution**: Loading/lashing/inspection → Completed (QC, photos, surveys)
**Post-Operation**: Docs/handover → Archived (B/L, COA, reports, preservation logs)

---

## Part 1: Integrated Domain Ontology

### Core Classes (Unified hvdc: Namespace)

```turtle
@prefix hvdc: <https://hvdc-project.com/ontology/integrated/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# From Material Handling
hvdc:Project a owl:Class .
hvdc:Phase a owl:Class .
hvdc:Port a owl:Class .
hvdc:MOSB a owl:Class .
hvdc:Site a owl:Class .
hvdc:TransportMeans a owl:Class .
hvdc:Operation a owl:Class .
hvdc:Document a owl:Class .

# Bulk-Specific Classes (Unified with Material Handling)
hvdc:Cargo a owl:Class ;
    rdfs:comment "Unified cargo class for bulk and project cargo (transformers, steel structures, OOG)" .

hvdc:Vessel a owl:Class ;
    rdfs:subClassOf hvdc:TransportMeans ;
    rdfs:comment "Marine vessel (LCT, Barge) with deck areas for cargo stowage" .

hvdc:DeckArea a owl:Class ;
    rdfs:comment "Deck area on vessel with usable dimensions and load capacity" .

hvdc:LashingAssembly a owl:Class ;
    rdfs:comment "Lashing assembly securing cargo with calculated tension and safety factors" .

hvdc:LashingElement a owl:Class ;
    rdfs:comment "Individual lashing element (chain, wire, turnbuckle) within assembly" .

hvdc:StabilityCase a owl:Class ;
    rdfs:comment "Stability case evaluating vessel stability with GM, VCG, roll angles" .

hvdc:LiftingPlan a owl:Class ;
    rdfs:comment "Lifting plan with method, rigging gear, sling angles for cargo handling" .

hvdc:RiggingGear a owl:Class ;
    rdfs:comment "Rigging gear (sling, shackle, spreader) used in lifting operations" .

hvdc:Equipment a owl:Class ;
    rdfs:comment "Equipment (crane, forklift, SPMT) for cargo handling operations" .

hvdc:Manpower a owl:Class ;
    rdfs:comment "Manpower (riggers, operators, surveyors) for operations" .

hvdc:OperationTask a owl:Class ;
    rdfs:subClassOf hvdc:Operation ;
    rdfs:comment "Specific operation task (loading, discharging, lashing, inspection)" .

hvdc:Environment a owl:Class ;
    rdfs:comment "Environmental conditions (wind, sea state, temperature) affecting operations" .
```

### Core Properties (Integrated)

```turtle
# Material Handling Object Properties
hvdc:hasPhase a owl:ObjectProperty .
hvdc:involves a owl:ObjectProperty .
hvdc:handles a owl:ObjectProperty .
hvdc:consolidates a owl:ObjectProperty .
hvdc:dispatches a owl:ObjectProperty .
hvdc:receives a owl:ObjectProperty .
hvdc:transportedBy a owl:ObjectProperty .
hvdc:usedIn a owl:ObjectProperty .
hvdc:requires a owl:ObjectProperty .

# Bulk Cargo Object Properties (Integrated)
hvdc:placedOn a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:DeckArea ;
    rdfs:comment "Cargo placed on specific deck area" .

hvdc:securedBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:LashingAssembly ;
    rdfs:comment "Cargo secured by lashing assembly" .

hvdc:handledBy a owl:ObjectProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range hvdc:Equipment ;
    rdfs:comment "Cargo handled by specific equipment" .

hvdc:hasDeck a owl:ObjectProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range hvdc:DeckArea ;
    rdfs:comment "Vessel has deck areas" .

hvdc:carries a owl:ObjectProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Vessel carries cargo" .

hvdc:appliedTo a owl:ObjectProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Lashing assembly applied to cargo" .

hvdc:uses a owl:ObjectProperty ;
    rdfs:domain [ owl:unionOf (hvdc:LashingAssembly hvdc:LiftingPlan) ] ;
    rdfs:range [ owl:unionOf (hvdc:LashingElement hvdc:RiggingGear) ] ;
    rdfs:comment "Assembly or plan uses elements/gear" .

hvdc:evaluates a owl:ObjectProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range hvdc:Vessel ;
    rdfs:comment "Stability case evaluates vessel" .

hvdc:considers a owl:ObjectProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Stability case considers cargo loading" .

hvdc:for a owl:ObjectProperty ;
    rdfs:domain hvdc:LiftingPlan ;
    rdfs:range hvdc:Cargo ;
    rdfs:comment "Lifting plan for specific cargo" .

hvdc:affects a owl:ObjectProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range [ owl:unionOf (hvdc:LashingAssembly hvdc:StabilityCase) ] ;
    rdfs:comment "Environment affects assemblies/stability" .

# Material Handling Data Properties
hvdc:projectName a owl:DatatypeProperty .
hvdc:date a owl:DatatypeProperty .
hvdc:phaseType a owl:DatatypeProperty .
hvdc:name a owl:DatatypeProperty .
hvdc:type a owl:DatatypeProperty .
hvdc:areaSqm a owl:DatatypeProperty .
hvdc:weight a owl:DatatypeProperty .
hvdc:dims a owl:DatatypeProperty .
hvdc:voyageTime a owl:DatatypeProperty .

# Bulk Cargo Data Properties (Integrated)
hvdc:cargoId a owl:DatatypeProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range xsd:string ;
    rdfs:comment "Unique cargo identifier" .

hvdc:stackable a owl:DatatypeProperty ;
    rdfs:domain hvdc:Cargo ;
    rdfs:range xsd:boolean ;
    rdfs:comment "Whether cargo can be stacked" .

hvdc:deckStrength a owl:DatatypeProperty ;
    rdfs:domain hvdc:Vessel ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Deck strength in t/m²" .

hvdc:requiredCapacity a owl:DatatypeProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Required lashing capacity in tons" .

hvdc:safetyFactor a owl:DatatypeProperty ;
    rdfs:domain hvdc:LashingAssembly ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Safety factor (≥1.0)" .

hvdc:disp a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Displacement in tons" .

hvdc:vcg a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Vertical center of gravity in meters" .

hvdc:gm a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Metacentric height in meters (GM)" .

hvdc:rollAngle a owl:DatatypeProperty ;
    rdfs:domain hvdc:StabilityCase ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Roll angle in degrees" .

hvdc:slingAngleDeg a owl:DatatypeProperty ;
    rdfs:domain hvdc:LiftingPlan ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Sling angle in degrees" .

hvdc:wind a owl:DatatypeProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range xsd:decimal ;
    rdfs:comment "Wind speed in m/s" .

hvdc:seaState a owl:DatatypeProperty ;
    rdfs:domain hvdc:Environment ;
    rdfs:range xsd:integer ;
    rdfs:comment "Sea state index (0-9)" .
```

---

## Part 2: SHACL Constraints

```turtle
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix hvdc: <https://hvdc-project.com/ontology/integrated/> .

# Material Handling Constraints (Excerpt)
hvdc:ProjectShape a sh:NodeShape ;
    sh:targetClass hvdc:Project ;
    sh:property [ sh:path hvdc:projectName ; sh:minCount 1 ] .

# Bulk Cargo Constraints (Integrated)
hvdc:CargoShape a sh:NodeShape ;
    sh:targetClass hvdc:Cargo ;
    sh:property [
        sh:path hvdc:cargoId ;
        sh:minCount 1 ;
        sh:message "Cargo must have ID"
    ] ;
    sh:property [
        sh:path hvdc:weight ;
        sh:minInclusive 0.01 ;
        sh:message "Weight must be positive"
    ] ;
    sh:property [
        sh:path hvdc:cogX ;
        sh:minInclusive 0.0 ;
        sh:message "COG X must be non-negative"
    ] .

hvdc:VesselShape a sh:NodeShape ;
    sh:targetClass hvdc:Vessel ;
    sh:property [
        sh:path hvdc:deckStrength ;
        sh:minInclusive 0.01 ;
        sh:message "Deck strength must be positive"
    ] .

hvdc:LashingAssemblyShape a sh:NodeShape ;
    sh:targetClass hvdc:LashingAssembly ;
    sh:property [
        sh:path hvdc:safetyFactor ;
        sh:minInclusive 1.0 ;
        sh:message "Safety factor must be at least 1.0"
    ] .

hvdc:StabilityCaseShape a sh:NodeShape ;
    sh:targetClass hvdc:StabilityCase ;
    sh:property [
        sh:path hvdc:gm ;
        sh:minInclusive 0.0 ;
        sh:message "GM must be non-negative"
    ] ;
    sh:property [
        sh:path hvdc:rollAngle ;
        sh:maxInclusive 90.0 ;
        sh:message "Roll angle must not exceed 90 degrees"
    ] .
```

---

## Part 3: Examples & Queries

### JSON-LD Examples

**Integrated Cargo Example (Steel Structure)**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/integrated/"
  },
  "@id": "hvdc:cargo-001",
  "@type": "hvdc:Cargo",
  "hvdc:cargoId": "CGO-2025-001",
  "hvdc:type": "Steel Structure",
  "hvdc:weight": 25.5,
  "hvdc:dimsL": 12.0,
  "hvdc:dimsW": 3.5,
  "hvdc:dimsH": 4.2,
  "hvdc:cogX": 6.0,
  "hvdc:cogY": 1.75,
  "hvdc:cogZ": 2.1,
  "hvdc:stackable": false,
  "hvdc:placedOn": {
    "@type": "hvdc:DeckArea",
    "@id": "hvdc:deck-a1",
    "hvdc:areaId": "DECK-A1",
    "hvdc:maxPointLoad": 50.0
  },
  "hvdc:securedBy": {
    "@type": "hvdc:LashingAssembly",
    "@id": "hvdc:lashing-001",
    "hvdc:requiredCapacity": 30.0,
    "hvdc:safetyFactor": 1.2
  },
  "hvdc:transportedBy": {
    "@type": "hvdc:TransportMeans",
    "@id": "hvdc:lct-001",
    "hvdc:vesselType": "LCT"
  }
}
```

**Transformer with Bulk Lifting**

```json
{
  "@context": {
    "hvdc": "https://hvdc-project.com/ontology/integrated/"
  },
  "@id": "hvdc:transformer-das-1",
  "@type": "hvdc:Cargo",
  "hvdc:cargoId": "TR-DAS-1",
  "hvdc:type": "Transformer",
  "hvdc:weight": 200.0,
  "hvdc:dimsL": 10.0,
  "hvdc:dimsW": 5.0,
  "hvdc:dimsH": 6.0,
  "hvdc:for": {
    "@type": "hvdc:LiftingPlan",
    "@id": "hvdc:lift-das-1",
    "hvdc:method": "Skidding",
    "hvdc:slingAngleDeg": 45,
    "hvdc:uses": {
      "@type": "hvdc:RiggingGear",
      "@id": "hvdc:rigging-sling-001",
      "hvdc:type": "Sling"
    }
  },
  "hvdc:preservation": {
    "@type": "hvdc:PreservationCheck",
    "hvdc:gasType": "Dry air",
    "hvdc:gaugeLevel": 12.5
  }
}
```

### SPARQL Queries

**Cargo Stability Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?cargoId ?weight ?gm ?stabilityStatus
WHERE {
    ?cargo hvdc:cargoId ?cargoId ;
           hvdc:weight ?weight .
    ?stability hvdc:considers ?cargo ;
               hvdc:gm ?gm .
    BIND(IF(?gm > 0.5, "STABLE", IF(?gm > 0.2, "MARGINAL", "UNSTABLE")) AS ?stabilityStatus)
}
ORDER BY DESC(?gm)
```

**Operation Documents Query**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?operationType ?documentType ?status
WHERE {
    ?operation hvdc:type ?operationType ;
               hvdc:requires ?document .
    ?document hvdc:type ?documentType .
    OPTIONAL {
        ?operation hvdc:status ?status .
    }
}
ORDER BY ?operationType ?documentType
```

**Integrated Lashing Safety Check**

```sparql
PREFIX hvdc: <https://hvdc-project.com/ontology/integrated/>

SELECT ?cargo ?cargoId ?requiredCapacity ?calcTension ?safetyFactor ?safe
WHERE {
    ?cargo hvdc:cargoId ?cargoId ;
           hvdc:securedBy ?lashing .
    ?lashing hvdc:requiredCapacity ?requiredCapacity ;
             hvdc:calcTension ?calcTension ;
             hvdc:safetyFactor ?safetyFactor .
    BIND(IF(?safetyFactor >= 1.0 && ?calcTension >= ?requiredCapacity, "SAFE", "UNSAFE") AS ?safe)
}
ORDER BY DESC(?safetyFactor)
```

---

## Semantic KPI Layer

### Integrated KPIs

- **Cargo Safety Index**: Stability compliance rate across all phases (target: ≥95%)
- **Lashing Efficiency**: Capacity vs. usage in marine transport (target: ≥85%)
- **Deck Utilization**: Area exploitation in MOSB/vessels (target: 70-85%)
- **Handling Incident Rate**: Zero target in lifting/stowage operations
- **Preservation Adherence**: Temp/RH compliance for bulk items (target: 100%)
- **Voyage Optimization**: Actual vs. planned times with stability factors (target: ≥90%)

---

## Recommended Commands

`/bulk-cargo plan --stowage=lct` [Bulk cargo stowage planning for LCT operations]
`/lashing-calc validate --safety-factor=1.2` [Lashing assembly calculation and safety factor validation]
`/stability-check evaluate --gm=0.5` [Vessel stability evaluation with GM/VCG/roll angle analysis]
`/lifting-plan optimize --method=Skidding` [Lifting plan optimization with rigging gear selection]
`/cargo-traceability track --cargo=cgo-001` [End-to-end cargo traceability from port to site]

---

## Related Ontologies

- [Material Handling Overview](./2_EXT-08A-hvdc-material-handling-overview.md) - Overall logistics workflow
- [Material Handling Customs](./2_EXT-08B-hvdc-material-handling-customs.md) - Customs clearance procedures
- [Material Handling Storage](./2_EXT-08C-hvdc-material-handling-storage.md) - Storage and inland transportation
- [Material Handling Offshore](./2_EXT-08D-hvdc-material-handling-offshore.md) - Offshore marine transportation
- [Material Handling Site Receiving](./2_EXT-08E-hvdc-material-handling-site-receiving.md) - Site receiving and inspection
- [Material Handling Transformer](./2_EXT-08F-hvdc-material-handling-transformer.md) - Transformer handling procedures
- [Bulk Cargo Operations](../core/1_CORE-05-hvdc-bulk-cargo-ops.md) - Core bulk cargo ontology

---

## Original Content

This integrated ontology document combines:

1. **Material Handling Workshop content** from `HVDC_Material Handling Workshop_(20241119_1).pdf` (6 sections covering Overview, Customs, Storage, Offshore Transport, Site Receiving, and Transformer handling)

2. **Bulk Cargo Operations ontology** from `1_CORE-05-hvdc-bulk-cargo-ops.md` (detailed stowage, lashing, stability, and lifting operations)

### Integration Benefits

- **Unified Knowledge Graph**: Single ontology namespace (`hvdc:`) for all material handling and bulk cargo operations
- **End-to-End Traceability**: Track cargo from port arrival through storage, transport, and installation
- **Automated Validation**: SHACL constraints ensure safety and compliance across all operations
- **Predictive Analytics**: Integrated KPIs support decision-making and risk management
- **Compliance Enforcement**: UAE customs, ADNOC HSE, IMSBC, SOLAS standards embedded in constraints

This consolidated approach enables comprehensive logistics management for the HVDC project, supporting both operational execution and strategic planning.

