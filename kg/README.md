# Knowledge Graph Scripts

## Quick Start

### Generate sample data
```bash
cd kg/scripts
python make_sample_data.py
```

This creates:
- `data/processed/nodes.csv`
- `data/processed/edges.csv`
- `data/synonyms/synonyms.json`

### Validate data
```bash
python validate_data.py
```

### Load into Neo4j
```bash
python load_neo4j.py --uri bolt://localhost:7687 --user neo4j --password your_password
```

Or use environment variables:
```bash
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=your_password
python load_neo4j.py
```

## Verify in Neo4j Browser

Run these queries:
```cypher
// Count nodes
MATCH (n) RETURN labels(n)[0] AS type, count(*) AS count

// Get sample data
MATCH (n:Disease) RETURN n LIMIT 5
MATCH (n:InsuranceProduct) RETURN n LIMIT 5

// Query relationships
MATCH (p:InsuranceProduct)-[r]->(d:Disease) RETURN p.name, type(r), d.name LIMIT 10
```
