#!/usr/bin/env python3
"""
Merge 7 Material Handling ontology documents into a single consolidated file.
All original files are preserved (not deleted).
"""

import pathlib

# Define source files
source_files = [
    ("2_EXT-08A-hvdc-material-handling-overview.md", "Overview", 1),
    ("2_EXT-08B-hvdc-material-handling-customs.md", "Customs Clearance", 2),
    (
        "2_EXT-08C-hvdc-material-handling-storage.md",
        "Storage & Inland Transportation",
        3,
    ),
    (
        "2_EXT-08D-hvdc-material-handling-offshore.md",
        "Offshore Marine Transportation",
        4,
    ),
    ("2_EXT-08E-hvdc-material-handling-site-receiving.md", "Site Receiving", 5),
    ("2_EXT-08F-hvdc-material-handling-transformer.md", "Transformer Handling", 6),
    ("2_EXT-08G-hvdc-material-handling-bulk-integrated.md", "Bulk Cargo Operations", 7),
]

# Base directory
base_dir = pathlib.Path(__file__).parent.parent / "docs" / "ontology" / "extended"

# Output file
output_file = base_dir / "2_EXT-08-hvdc-material-handling-consolidated.md"


def extract_section_content(file_path):
    """Extract content after Executive Summary"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the first "---" after the front matter
    # Skip the YAML front matter and extract everything after it
    parts = content.split("---\n\n", 2)
    if len(parts) >= 3:
        # Return everything after the second "---\n\n"
        return parts[2]
    else:
        # Fallback: return everything after the first 20 lines (should skip front matter and heading)
        lines = content.split("\n")
        return "\n".join(lines[15:])  # Skip front matter and H1


# Build consolidated content
consolidated = """---
title: "HVDC Material Handling Ontology - Consolidated"
type: "ontology-design"
domain: "material-handling"
sub-domains: ["workshop", "customs", "storage", "offshore", "receiving", "transformer", "bulk-cargo"]
version: "consolidated-1.0"
date: "2025-10-26"
tags: ["ontology", "hvdc", "material-handling", "consolidated"]
standards: ["RDF", "OWL", "SHACL", "SPARQL", "JSON-LD", "IMSBC", "SOLAS"]
status: "active"
source_files: [
  "2_EXT-08A-hvdc-material-handling-overview.md",
  "2_EXT-08B-hvdc-material-handling-customs.md",
  "2_EXT-08C-hvdc-material-handling-storage.md",
  "2_EXT-08D-hvdc-material-handling-offshore.md",
  "2_EXT-08E-hvdc-material-handling-site-receiving.md",
  "2_EXT-08F-hvdc-material-handling-transformer.md",
  "2_EXT-08G-hvdc-material-handling-bulk-integrated.md"
]
---

# hvdc-material-handling-consolidated · 2_EXT-08

## Executive Summary

This consolidated document merges 7 Material Handling ontology documents covering the complete logistics workflow for the Independent Subsea HVDC System Project (Project Lightning) in the UAE. It encompasses:

- **Overview**: Project logistics workflow and port information
- **Customs Clearance**: UAE customs procedures and documentation
- **Storage & Inland Transportation**: Storage standards and heavy equipment transport
- **Offshore Marine Transportation**: LCT operations and MOSB procedures
- **Site Receiving**: Material inspection and issuance procedures
- **Transformer Handling**: Specialized heavy equipment operations
- **Bulk Cargo Operations**: Integrated stowage, lashing, stability, and lifting

All content from the individual documents is preserved in their respective sections below.

## Table of Contents

1. [Overview](#section-1-overview) - Overall logistics workflow and port information
2. [Customs Clearance](#section-2-customs-clearance) - Customs procedures and documentation
3. [Storage & Inland Transportation](#section-3-storage--inland-transportation) - Storage standards and inland transport
4. [Offshore Marine Transportation](#section-4-offshore-marine-transportation) - LCT operations and MOSB procedures
5. [Site Receiving](#section-5-site-receiving) - Material inspection and issuance
6. [Transformer Handling](#section-6-transformer-handling) - Specialized transformer operations
7. [Bulk Cargo Operations](#section-7-bulk-cargo-operations) - Integrated bulk cargo handling

---

"""

# Process each source file
for filename, section_name, section_num in source_files:
    source_path = base_dir / filename

    if not source_path.exists():
        print(f"Warning: {filename} not found")
        continue

    # Add section header
    consolidated += f"## Section {section_num}: {section_name}\n\n"
    consolidated += "### Source\n\n"
    consolidated += f"- **Original File**: {filename}\n"

    # Read original file to get metadata
    with open(source_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    # Extract version and date from front matter
    lines = original_content.split("\n")
    version = "unified-1.0"
    date = "2024-11-19"
    for i, line in enumerate(lines):
        if "version:" in line:
            version = line.split("version:")[1].strip().strip('"')
        elif "date:" in line:
            date = line.split("date:")[1].strip().strip('"')

    consolidated += f"- **Version**: {version}\n"
    consolidated += f"- **Date**: {date}\n\n"

    # Extract content (skip front matter and H1)
    content = extract_section_content(source_path)
    consolidated += content
    consolidated += "\n\n---\n\n"

# Write consolidated file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(consolidated)

print(f"Consolidated file created: {output_file}")

# Count lines
with open(output_file, "r", encoding="utf-8") as f:
    line_count = len(f.readlines())

print(f"Total lines: {line_count}")


