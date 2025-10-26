#!/usr/bin/env python3
"""
Enhance Material Handling ontology documents with detailed ontology system from consolidated file.
"""
import re
from pathlib import Path

def get_ontology_content_for_section(section_name: str) -> dict:
    """Extract ontology content for specific section from consolidated file."""

    section_mapping = {
        "Overview": {
            "classes": """@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .

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
    rdfs:comment "Materials being handled in logistics operations." .""",

            "properties": """hvdc:hasPhase a owl:ObjectProperty ;
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
    rdfs:range xsd:decimal .""",

            "shacl": """hvdc:ProjectShape a sh:NodeShape ;
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
    ] .""",

            "jsonld": """{
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
}""",

            "sparql": """PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?phaseType ?entityId
WHERE {
    ?project hvdc:hasPhase ?phase .
    ?phase hvdc:phaseType ?phaseType ;
           hvdc:involves ?entity .
    ?entity @id ?entityId .
}
ORDER BY ?phaseType""",

            "kpi": """## Semantic KPI Layer

### Project Logistics KPIs
- **Phase Completion Rate**: Percentage of Phase A/B completions on schedule
- **Port Handling Efficiency**: Container/Bulk processing time vs. targets
- **MOSB Utilization**: Storage capacity utilization (%)
- **Site Receiving Timeliness**: Materials received vs. ETA
- **Document Compliance**: Customs clearance success rate (≥95%)""",

            "commands": """## Recommended Commands

/material-handling analyze --phase=A [Import stage analysis]
/material-handling predict-eta --site=MIR [ETA prediction with weather tie]
/material-handling kpi-dash --realtime [Real-time logistics dashboard]
/material-handling optimize-stowage --vessel=LCT [LCT stowage optimization]"""
        },

        "Customs": {
            "classes": """hvdc:CustomsDeclaration a owl:Class ;
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
    rdfs:comment "Electronic Document Attestation System." .""",

            "properties": """hvdc:submittedTo a owl:ObjectProperty ;
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
    rdfs:range xsd:string .""",

            "shacl": """hvdc:CustomsDeclarationShape a sh:NodeShape ;
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
    ] .""",

            "jsonld": """{
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
}""",

            "sparql": """PREFIX hvdc: <https://hvdc-project.com/ontology/material-handling/>

SELECT ?declarationCode ?location ?documentType
WHERE {
    ?declaration a hvdc:CustomsDeclaration ;
                 hvdc:codeNo ?declarationCode ;
                 hvdc:location ?location ;
                 hvdc:declares ?doc .
    ?doc hvdc:type ?documentType .
}
ORDER BY ?declarationCode""",

            "kpi": """## Semantic KPI Layer

### Customs Clearance KPIs
- **Clearance Time**: Average time from submission to approval
- **Document Accuracy**: First-time approval rate (≥98%)
- **Duty Accuracy**: Duty calculation accuracy (100%)
- **Compliance Rate**: Regulations adherence (UAE customs)""",

            "commands": """## Recommended Commands

/customs-clearance verify --docs [Document validation]
/customs-clearance track --status [Status tracking]
/customs-clearance analyze --duty [Duty calculation analysis]"""
        }
    }

    return section_mapping.get(section_name, {})

def enhance_document(doc_path: Path, section_name: str) -> None:
    """Enhance a document with ontology content."""

    content = doc_path.read_text(encoding='utf-8')
    ontology = get_ontology_content_for_section(section_name)

    if not ontology:
        print(f"No ontology content found for {section_name}")
        return

    # Find the position after "## Part 3: Examples & Queries" section
    patterns = {
        "Core Classes": {
            "insert_after": "### Core Classes",
            "content": ontology.get("classes", ""),
            "prefix": "@prefix hvdc: <https://hvdc-project.com/ontology/material-handling/> .\n@prefix owl: <http://www.w3.org/2002/07/owl#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n@prefix sh: <http://www.w3.org/ns/shacl#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n"
        },
        "Core Properties": {
            "insert_after": "### Data Properties",
            "content": ontology.get("properties", ""),
            "prefix": ""
        },
        "SHACL Constraints": {
            "insert_after": "### SHACL Constraints",
            "content": ontology.get("shacl", ""),
            "prefix": ""
        },
        "JSON-LD Examples": {
            "insert_after": "### JSON-LD Examples",
            "content": ontology.get("jsonld", ""),
            "prefix": ""
        },
        "SPARQL Queries": {
            "insert_after": "### SPARQL Queries",
            "content": ontology.get("sparql", ""),
            "prefix": ""
        }
    }

    # Replace placeholder content
    for key, pattern_info in patterns.items():
        pattern = f"({pattern_info['insert_after']})"
        replacement = f"\\1\n\n```turtle\n{pattern_info['prefix']}{pattern_info['content']}\n```"

        content = re.sub(
            pattern,
            replacement,
            content,
            count=1,
            flags=re.MULTILINE
        )

    # Add KPI and Commands sections before "## Original Content"
    if "## Original Content" in content and ontology.get("kpi") and ontology.get("commands"):
        insert_position = content.find("## Original Content")

        kpi_section = f"\n\n{ontology['kpi']}\n\n"
        commands_section = f"\n{ontology['commands']}\n\n---\n\n"

        content = content[:insert_position] + kpi_section + commands_section + content[insert_position:]

    doc_path.write_text(content, encoding='utf-8')
    print(f"Enhanced: {doc_path.name}")

def main():
    """Main execution."""
    base_dir = Path("docs/ontology/extended")

    mapping = {
        "2_EXT-08A-hvdc-material-handling-overview.md": "Overview",
        "2_EXT-08B-hvdc-material-handling-customs.md": "Customs",
        "2_EXT-08C-hvdc-material-handling-storage.md": "Storage",
        "2_EXT-08D-hvdc-material-handling-offshore.md": "Offshore",
        "2_EXT-08E-hvdc-material-handling-site-receiving.md": "SiteReceiving",
        "2_EXT-08F-hvdc-material-handling-transformer.md": "Transformer"
    }

    for filename, section in mapping.items():
        doc_path = base_dir / filename
        if doc_path.exists():
            enhance_document(doc_path, section)
        else:
            print(f"Not found: {doc_path}")

if __name__ == "__main__":
    main()

