#!/usr/bin/env python3
"""
Validate data files for GraphRAG

Checks:
- CSV format and required fields
- Node IDs are unique
- Referenced node IDs exist
- Relation types are valid
- JSON aliases are valid
"""

import csv
import json
import os
import sys


VALID_RELATIONS = {"TREATS", "COVERS", "EXCLUDES", "AGE_RANGE", "PROVIDES"}
VALID_LABELS = {"Disease", "Drug", "InsuranceProduct", "ElderCareOrg", "Service"}


def validate_nodes(nodes_file: str) -> tuple:
    """Validate nodes CSV"""
    errors = []
    warnings = []
    node_ids = set()

    if not os.path.exists(nodes_file):
        return [f"Nodes file not found: {nodes_file}"], [], set()

    with open(nodes_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check required fields
            if not row.get("node_id"):
                errors.append(f"Missing node_id at row")
                continue

            if not row.get("label"):
                errors.append(f"Missing label for node_id: {row['node_id']}")
                continue

            if not row.get("name"):
                errors.append(f"Missing name for node_id: {row['node_id']}")

            # Check unique node_id
            if row["node_id"] in node_ids:
                errors.append(f"Duplicate node_id: {row['node_id']}")
            node_ids.add(row["node_id"])

            # Check label
            if row["label"] not in VALID_LABELS:
                warnings.append(f"Unknown label: {row['label']} for node_id: {row['node_id']}")

            # Validate aliases JSON
            if row.get("aliases_json"):
                try:
                    aliases = json.loads(row["aliases_json"])
                    if not isinstance(aliases, list):
                        errors.append(f"aliases_json must be array for node_id: {row['node_id']}")
                except json.JSONDecodeError:
                    errors.append(f"Invalid JSON in aliases_json for node_id: {row['node_id']}")

    return errors, warnings, node_ids


def validate_edges(edges_file: str, node_ids: set) -> tuple:
    """Validate edges CSV"""
    errors = []
    warnings = []

    if not os.path.exists(edges_file):
        return [f"Edges file not found: {edges_file}"], []

    with open(edges_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Check required fields
            if not row.get("head_id"):
                errors.append(f"Missing head_id at row")
                continue

            if not row.get("tail_id"):
                errors.append(f"Missing tail_id at row")
                continue

            if not row.get("relation"):
                errors.append(f"Missing relation for {row.get('head_id')} -> {row.get('tail_id')}")

            # Check relation type
            if row.get("relation") not in VALID_RELATIONS:
                warnings.append(f"Unknown relation type: {row['relation']}")

            # Check node existence
            if row["head_id"] not in node_ids:
                errors.append(f"head_id not found: {row['head_id']}")

            if row["tail_id"] not in node_ids:
                errors.append(f"tail_id not found: {row['tail_id']}")

    return errors, warnings


def main():
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")  # Go to kg/ directory

    nodes_file = "data/processed/nodes.csv"
    edges_file = "data/processed/edges.csv"

    print("Validating data files...\n")

    # Validate nodes
    print(f"Validating {nodes_file}...")
    node_errors, node_warnings, node_ids = validate_nodes(nodes_file)

    if node_errors:
        print(f"  ❌ Errors: {len(node_errors)}")
        for e in node_errors:
            print(f"    - {e}")
    else:
        print(f"  ✓ No errors")

    if node_warnings:
        print(f"  ⚠ Warnings: {len(node_warnings)}")
        for w in node_warnings:
            print(f"    - {w}")

    print(f"\n  Found {len(node_ids)} unique nodes")

    # Validate edges
    print(f"\nValidating {edges_file}...")
    edge_errors, edge_warnings = validate_edges(edges_file, node_ids)

    if edge_errors:
        print(f"  ❌ Errors: {len(edge_errors)}")
        for e in edge_errors:
            print(f"    - {e}")
    else:
        print(f"  ✓ No errors")

    if edge_warnings:
        print(f"  ⚠ Warnings: {len(edge_warnings)}")
        for w in edge_warnings[:5]:  # Show first 5
            print(f"    - {w}")

    # Summary
    total_errors = len(node_errors) + len(edge_errors)
    if total_errors > 0:
        print(f"\n❌ Validation failed with {total_errors} errors")
        sys.exit(1)
    else:
        print(f"\n✓ Validation passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
