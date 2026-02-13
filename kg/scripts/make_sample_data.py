#!/usr/bin/env python3
"""
Generate sample data for Insurance Medicare GraphRAG

Creates:
- data/processed/nodes.csv
- data/processed/edges.csv
- data/synonyms/synonyms.json
"""

import os
import csv
import json
import argparse


def ensure_dirs():
    """Create necessary directories"""
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/synonyms", exist_ok=True)


def generate_nodes() -> list:
    """Generate sample nodes"""
    nodes = []

    # Diseases
    diseases = [
        ("d_001", "Disease", "高血压", '["原发性高血压", "HTN"]', None, None, None, None, None, "doc_001"),
        ("d_002", "Disease", "糖尿病", '["DM", "2型糖尿病"]', None, None, None, None, None, "doc_001"),
        ("d_003", "Disease", "冠心病", None, None, None, None, None, None, "doc_001"),
        ("d_004", "Disease", "脑卒中", '["中风", "脑血管意外"]', None, None, None, None, None, "doc_001"),
        ("d_005", "Disease", "慢性肾病", None, None, None, None, None, None, "doc_001"),
        ("d_006", "Disease", "阿尔茨海默病", '["老年痴呆"]', None, None, None, None, None, "doc_002"),
    ]
    for d in diseases:
        nodes.append({
            "node_id": d[0],
            "label": d[1],
            "name": d[2],
            "aliases_json": d[3],
            "age_min": d[4],
            "age_max": d[5],
            "product_id": d[6],
            "org_id": d[7],
            "city": d[8],
            "source_id": d[9],
        })

    # Insurance Products
    products = [
        ("p_001", "InsuranceProduct", "XX护理险", '["长期护理保险", "护理险"]', 60, 75, "PROD001", None, None, "doc_002"),
        ("p_002", "InsuranceProduct", "XX医疗险", '["百万医疗险"]', 18, 60, "PROD002", None, None, "doc_003"),
        ("p_003", "InsuranceProduct", "XX重疾险", '["重大疾病保险"]', 0, 55, "PROD003", None, None, "doc_004"),
        ("p_004", "InsuranceProduct", "尊享护理险", None, 65, 80, "PROD004", None, None, "doc_005"),
        ("p_005", "InsuranceProduct", "安心医疗险", None, 30, 65, "PROD005", None, None, "doc_003"),
    ]
    for p in products:
        nodes.append({
            "node_id": p[0],
            "label": p[1],
            "name": p[2],
            "aliases_json": p[3],
            "age_min": p[4],
            "age_max": p[5],
            "product_id": p[6],
            "org_id": p[7],
            "city": p[8],
            "source_id": p[9],
        })

    # Elder Care Organizations
    orgs = [
        ("o_001", "ElderCareOrg", "XX养老院", None, None, None, None, "北京", "doc_006"),
        ("o_002", "ElderCareOrg", "爱心护理中心", None, None, None, None, "上海", "doc_006"),
        ("o_003", "ElderCareOrg", "康养社区", '["养老社区"]', None, None, None, None, "深圳", "doc_006"),
    ]
    for o in orgs:
        nodes.append({
            "node_id": o[0],
            "label": o[1],
            "name": o[2],
            "aliases_json": o[3],
            "age_min": o[4],
            "age_max": o[5],
            "product_id": o[6],
            "org_id": o[7],
            "city": o[8],
            "source_id": o[9],
        })

    # Services
    services = [
        ("s_001", "Service", "日常护理", '["基础护理"]'),
        ("s_002", "Service", "专业护理", '["术后护理", "重症护理"]'),
        ("s_003", "Service", "康复训练", None),
        ("s_004", "Service", "健康管理", None),
        ("s_005", "Service", "医疗服务", '["医疗协助"]'),
    ]
    for s in services:
        nodes.append({
            "node_id": s[0],
            "label": s[1],
            "name": s[2],
            "aliases_json": s[3],
            "age_min": None,
            "age_max": None,
            "product_id": None,
            "org_id": None,
            "city": None,
            "source_id": "doc_006",
        })

    # Drugs
    drugs = [
        ("dr_001", "Drug", "二甲双胍", '["格华止"]', None, None, None, None, None, "doc_007"),
        ("dr_002", "Drug", "胰岛素", None, None, None, None, None, None, "doc_007"),
        ("dr_003", "Drug", "硝苯地平", '["拜新同"]', None, None, None, None, None, "doc_007"),
    ]
    for dr in drugs:
        nodes.append({
            "node_id": dr[0],
            "label": dr[1],
            "name": dr[2],
            "aliases_json": dr[3],
            "age_min": dr[4],
            "age_max": dr[5],
            "product_id": dr[6],
            "org_id": dr[7],
            "city": dr[8],
            "source_id": dr[9],
        })

    return nodes


def generate_edges() -> list:
    """Generate sample edges"""
    edges = [
        # Coverage relationships
        ("p_001", "COVERS", "d_001", "clause_12"),
        ("p_001", "COVERS", "d_006", "clause_13"),
        ("p_002", "COVERS", "d_001", "clause_08"),
        ("p_002", "COVERS", "d_002", "clause_09"),
        ("p_002", "COVERS", "d_003", "clause_10"),
        ("p_003", "COVERS", "d_002", "clause_05"),
        ("p_003", "COVERS", "d_003", "clause_06"),
        ("p_003", "COVERS", "d_004", "clause_07"),
        ("p_004", "COVERS", "d_001", "clause_15"),
        ("p_004", "COVERS", "d_005", "clause_16"),
        ("p_005", "COVERS", "d_001", "clause_20"),
        ("p_005", "COVERS", "d_003", "clause_21"),

        # Exclusion relationships
        ("p_001", "EXCLUDES", "d_001", "clause_08"),
        ("p_002", "EXCLUDES", "d_004", "clause_11"),
        ("p_003", "EXCLUDES", "d_005", "clause_08"),

        # Age range (stored as property)
        # Note: For simplicity, we'll add these as edges too
        ("p_001", "AGE_RANGE", "p_001", "clause_01"),
        ("p_002", "AGE_RANGE", "p_002", "clause_02"),
        ("p_003", "AGE_RANGE", "p_003", "clause_03"),
        ("p_004", "AGE_RANGE", "p_004", "clause_04"),
        ("p_005", "AGE_RANGE", "p_005", "clause_19"),

        # Drug treats disease
        ("dr_001", "TREATS", "d_002", "drug_01"),
        ("dr_002", "TREATS", "d_002", "drug_02"),
        ("dr_003", "TREATS", "d_001", "drug_03"),

        # Elder care provides services
        ("o_001", "PROVIDES", "s_001", "org_service_01"),
        ("o_001", "PROVIDES", "s_003", "org_service_02"),
        ("o_002", "PROVIDES", "s_001", "org_service_03"),
        ("o_002", "PROVIDES", "s_002", "org_service_04"),
        ("o_003", "PROVIDES", "s_001", "org_service_05"),
        ("o_003", "PROVIDES", "s_003", "org_service_06"),
        ("o_003", "PROVIDES", "s_004", "org_service_07"),
    ]

    return [{"head_id": e[0], "relation": e[1], "tail_id": e[2], "source_id": e[3]} for e in edges]


def generate_synonyms() -> dict:
    """Generate sample synonyms"""
    return {
        "高血压": ["原发性高血压", "HTN"],
        "糖尿病": ["DM", "2型糖尿病"],
        "护理险": ["长期护理保险", "长期护理险"],
        "中风": ["脑卒中", "脑血管意外"],
        "老年痴呆": ["阿尔茨海默病"],
        "护理": ["日常护理", "专业护理"],
    }


def save_nodes(nodes: list):
    """Save nodes to CSV"""
    fieldnames = ["node_id", "label", "name", "aliases_json", "age_min", "age_max", "product_id", "org_id", "city", "source_id"]

    with open("data/processed/nodes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(nodes)

    print(f"Created nodes.csv with {len(nodes)} nodes")


def save_edges(edges: list):
    """Save edges to CSV"""
    fieldnames = ["head_id", "relation", "tail_id", "source_id"]

    with open("data/processed/edges.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(edges)

    print(f"Created edges.csv with {len(edges)} edges")


def save_synonyms(synonyms: dict):
    """Save synonyms to JSON"""
    with open("data/synonyms/synonyms.json", "w", encoding="utf-8") as f:
        json.dump(synonyms, f, ensure_ascii=False, indent=2)

    print(f"Created synonyms.json with {len(synonyms)} entries")


def main():
    parser = argparse.ArgumentParser(description="Generate sample data for GraphRAG")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    args = parser.parse_args()

    # Change to output directory
    if args.output_dir != ".":
        os.chdir(args.output_dir)

    ensure_dirs()

    nodes = generate_nodes()
    edges = generate_edges()
    synonyms = generate_synonyms()

    save_nodes(nodes)
    save_edges(edges)
    save_synonyms(synonyms)

    print("\n✓ Sample data generated successfully!")
    print(f"  - {len(nodes)} nodes")
    print(f"  - {len(edges)} edges")
    print(f"  - {len(synonyms)} synonym entries")


if __name__ == "__main__":
    main()
