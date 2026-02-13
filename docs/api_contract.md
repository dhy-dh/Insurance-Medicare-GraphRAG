# API Contract

## Endpoints

### 1. GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "neo4j": "ok",
  "llm": "ok"
}
```

### 2. GET /subgraph
Query subgraph by mention/entity name.

**Query Parameters:**
- `query` (required): Entity mention to search
- `hop` (optional, default=2): Number of hops to traverse
- `limit` (optional, default=20): Maximum number of triples to return

**Response:**
```json
{
  "query": "高血压",
  "hop": 2,
  "linked_entities": [
    {
      "mention": "高血压",
      "node_id": "d_001",
      "label": "Disease",
      "score": 0.92
    }
  ],
  "triples": [
    {
      "h": "XX护理险",
      "r": "AGE_RANGE",
      "t": "60-75",
      "source_id": "clause_12"
    },
    {
      "h": "XX护理险",
      "r": "EXCLUDES",
      "t": "高血压",
      "source_id": "clause_08"
    }
  ],
  "cypher": "MATCH ...",
  "stats": {
    "triples": 12,
    "nodes": 8
  }
}
```

### 3. POST /ask
Ask a question using GraphRAG.

**Request:**
```json
{
  "question": "70岁高血压能买XX护理险吗？",
  "hop": 2,
  "limit": 20
}
```

**Response:**
```json
{
  "answer": "结论+解释+建议补充信息",
  "citations": [
    {
      "triple": "(XX护理险, AGE_RANGE, 60-75)",
      "source_id": "clause_12"
    },
    {
      "triple": "(XX护理险, EXCLUDES, 高血压)",
      "source_id": "clause_08"
    }
  ],
  "confidence": "low|medium|high",
  "debug": {
    "linked_entities": [...],
    "cypher": "...",
    "triples_used": 8
  }
}
```
