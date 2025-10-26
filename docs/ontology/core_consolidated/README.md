# HVDC Core Ontology - Consolidated Documentation

## Overview

This directory contains consolidated versions of the HVDC Core Ontology documentation, merging related concepts into comprehensive documents for better understanding and maintenance.

## File Mapping

| Consolidated File | Original Files | Description |
|------------------|----------------|-------------|
| `CONSOLIDATED-01-framework-infra.md` | `1_CORE-01-hvdc-core-framework.md`<br>`1_CORE-02-hvdc-infra-nodes.md` | Core logistics framework and infrastructure nodes |
| `CONSOLIDATED-02-warehouse-flow.md` | `1_CORE-03-hvdc-warehouse-ops.md`<br>`1_CORE-08-flow-code.md` | Warehouse operations and flow code algorithms |
| `CONSOLIDATED-03-cost-bulk.md` | `1_CORE-04-hvdc-invoice-cost.md`<br>`1_CORE-05-hvdc-bulk-cargo-ops.md` | Cost management and bulk cargo operations |
| `CONSOLIDATED-04-document-ocr.md` | `1_CORE-06-hvdc-doc-guardian.md`<br>`1_CORE-07-hvdc-ocr-pipeline.md` | Document guardian and OCR pipeline |

## Content Preservation

All consolidated files maintain the complete content from their original sources:

- **YAML Front Matter**: Combined metadata from source files
- **Part Structure**: Clear separation between original file contents
- **Source Attribution**: Each section includes source file information
- **Cross-References**: Internal links updated for consolidated structure
- **Ontology Definitions**: Complete RDF/OWL/SHACL definitions preserved

## Usage

### For Developers
- Use consolidated files for comprehensive understanding of related concepts
- Reference original files for specific implementation details
- Cross-reference between consolidated files for system-wide understanding

### For Documentation
- Consolidated files provide complete context for each domain
- Source file references maintain traceability
- Table of Contents provides quick navigation

## Verification

### Line Count Verification
Each consolidated file's line count should equal the sum of its source files:

- `CONSOLIDATED-01`: Framework + Infra content
- `CONSOLIDATED-02`: Warehouse + Flow content
- `CONSOLIDATED-03`: Cost + Bulk content
- `CONSOLIDATED-04`: Document + OCR content

### Content Integrity
- All original content preserved
- No information loss during consolidation
- Proper attribution maintained
- Cross-references updated

## Original File References

### Core Framework & Infrastructure
- **Source**: `docs/ontology/core/1_CORE-01-hvdc-core-framework.md`
- **Source**: `docs/ontology/core/1_CORE-02-hvdc-infra-nodes.md`
- **Consolidated**: `CONSOLIDATED-01-framework-infra.md`

### Warehouse Operations & Flow Codes
- **Source**: `docs/ontology/core/1_CORE-03-hvdc-warehouse-ops.md`
- **Source**: `docs/ontology/core/1_CORE-08-flow-code.md`
- **Consolidated**: `CONSOLIDATED-02-warehouse-flow.md`

### Cost Management & Bulk Cargo
- **Source**: `docs/ontology/core/1_CORE-04-hvdc-invoice-cost.md`
- **Source**: `docs/ontology/core/1_CORE-05-hvdc-bulk-cargo-ops.md`
- **Consolidated**: `CONSOLIDATED-03-cost-bulk.md`

### Document Guardian & OCR Pipeline
- **Source**: `docs/ontology/core/1_CORE-06-hvdc-doc-guardian.md`
- **Source**: `docs/ontology/core/1_CORE-07-hvdc-ocr-pipeline.md`
- **Consolidated**: `CONSOLIDATED-04-document-ocr.md`

## Maintenance

### Updates
- Update consolidated files when source files change
- Maintain source attribution and version information
- Update cross-references as needed

### Version Control
- Track changes to both source and consolidated files
- Maintain consistency between versions
- Document consolidation rationale

## Standards Compliance

All consolidated files maintain compliance with:
- **RDF/OWL**: Semantic web standards
- **SHACL**: Shape constraint validation
- **SPARQL**: Query language support
- **JSON-LD**: Linked data serialization
- **Turtle**: RDF serialization format

## Contact

For questions about consolidation or content updates, refer to the original source files or contact the HVDC project team.
