#!/usr/bin/env python3
"""
Load data into Neo4j

Usage:
    python load_neo4j.py --uri bolt://localhost:7687 --user neo4j --password your_password
"""

import csv
import json
import os
import argparse
from neo4j import GraphDatabase


def load_nodes(driver, nodes_file: str):
    """Load nodes into Neo4j"""
    print(f"Loading nodes from {nodes_file}...")

    with open(nodes_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        nodes = list(reader)

    # Batch insert
    query = """
    MERGE (n:Entity {node_id: $node_id})
    SET n.name = $name,
        n.label = $label
    """

    with driver.session() as session:
        # Add properties based on label
        for node in nodes:
            label = node["label"]

            # Build query based on label
            if label == "InsuranceProduct":
                q = """
                MERGE (n:InsuranceProduct {node_id: $node_id})
                SET n.name = $name
                """
                params = {"node_id": node["node_id"], "name": node["name"]}
                if node.get("age_min"):
                    params["age_min"] = int(node["age_min"])
                if node.get("age_max"):
                    params["age_max"] = int(node["age_max"])
                if node.get("product_id"):
                    params["product_id"] = node["product_id"]
            elif label == "Disease":
                q = """
                MERGE (n:Disease {node_id: $node_id})
                SET n.name = $name
                """
                params = {"node_id": node["node_id"], "name": node["name"]}
            elif label == "Drug":
                q = """
                MERGE (n:Drug {node_id: $node_id})
                SET n.name = $name
                """
                params = {"node_id": node["node_id"], "name": node["name"]}
            elif label == "ElderCareOrg":
                q = """
                MERGE (n:ElderCareOrg {node_id: $node_id})
                SET n.name = $name
                """
                params = {"node_id": node["node_id"], "name": node["name"]}
                if node.get("city"):
                    params["city"] = node["city"]
            elif label == "Service":
                q = """
                MERGE (n:Service {node_id: $node_id})
                SET n.name = $name
                """
                params = {"node_id": node["node_id"], "name": node["name"]}
            else:
                q = """
                MERGE (n:Entity {node_id: $node_id})
                SET n.name = $name, n.label = $label
                """
                params = {"node_id": node["node_id"], "name": node["name"], "label": label}

            session.run(q, **params)

            # Add aliases if exists
            if node.get("aliases_json"):
                try:
                    aliases = json.loads(node["aliases_json"])
                    if aliases:
                        session.run(
                            """
                            MATCH (n {node_id: $node_id})
                            SET n.aliases = $aliases
                            """,
                            node_id=node["node_id"],
                            aliases=aliases,
                        )
                except json.JSONDecodeError:
                    pass

    print(f"  ✓ Loaded {len(nodes)} nodes")


def load_edges(driver, edges_file: str):
    """Load edges into Neo4j"""
    print(f"Loading edges from {edges_file}...")

    with open(edges_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        edges = list(reader)

    # Map relation to Cypher type
    relation_map = {
        "TREATS": "TREATS",
        "COVERS": "COVERS",
        "EXCLUDES": "EXCLUDES",
        "AGE_RANGE": "AGE_RANGE",
        "PROVIDES": "PROVIDES",
    }

    with driver.session() as session:
        for edge in edges:
            rel_type = edge["relation"]
            cypher_type = relation_map.get(rel_type, rel_type)

            query = f"""
            MATCH (a {{node_id: $head_id}})
            MATCH (b {{node_id: $tail_id}})
            MERGE (a)-[r:{cypher_type}]->(b)
            SET r.source_id = $source_id
            """

            session.run(
                query,
                head_id=edge["head_id"],
                tail_id=edge["tail_id"],
                source_id=edge.get("source_id", ""),
            )

    print(f"  ✓ Loaded {len(edges)} edges")


def create_indexes(driver):
    """Create indexes"""
    print("Creating indexes...")

    with driver.session() as session:
        session.run("CREATE INDEX node_id_index IF NOT EXISTS FOR (n:Entity) ON (n.node_id)")
        session.run("CREATE INDEX name_index IF NOT EXISTS FOR (n:Entity) ON (n.name)")

    print("  ✓ Indexes created")


def verify_data(driver):
    """Verify data was loaded"""
    print("\nVerifying data...")

    with driver.session() as session:
        # Count nodes
        result = session.run("MATCH (n) RETURN count(n) as count")
        node_count = result.single()["count"]
        print(f"  Total nodes: {node_count}")

        # Count by label
        result = session.run("MATCH (n) RETURN labels(n)[0] as label, count(n) as count")
        print("  By label:")
        for record in result:
            print(f"    - {record['label']}: {record['count']}")

        # Count relationships
        result = session.run("MATCH ()-[r]->() RETURN count(r) as count")
        rel_count = result.single()["count"]
        print(f"  Total relationships: {rel_count}")


def main():
    parser = argparse.ArgumentParser(description="Load data into Neo4j")
    parser.add_argument("--uri", default="bolt://localhost:7687", help="Neo4j URI")
    parser.add_argument("--user", default="neo4j", help="Neo4j user")
    parser.add_argument("--password", default="neo4j_password", help="Neo4j password")
    parser.add_argument("--nodes", default="data/processed/nodes.csv", help="Nodes CSV file")
    parser.add_argument("--edges", default="data/processed/edges.csv", help="Edges CSV file")
    args = parser.parse_args()

    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.chdir("..")  # Go to kg/ directory

    # Connect to Neo4j
    print(f"Connecting to Neo4j at {args.uri}...")
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))

    try:
        # Load data
        load_nodes(driver, args.nodes)
        load_edges(driver, args.edges)
        create_indexes(driver)
        verify_data(driver)

        print("\n✓ Data loaded successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise
    finally:
        driver.close()


if __name__ == "__main__":
    main()
