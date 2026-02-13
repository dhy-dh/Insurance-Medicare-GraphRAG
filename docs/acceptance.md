# Acceptance Criteria

## Functional Requirements

### F1: Health Check
- [ ] GET /health returns {"status":"ok","neo4j":"ok|fail","llm":"ok|fail"}
- [ ] Neo4j connectivity is verified

### F2: Subgraph Query
- [ ] GET /subgraph?query=高血压 returns linked entities
- [ ] Response includes triples with source_id
- [ ] Stats show correct counts

### F3: Question Answering
- [ ] POST /ask accepts question JSON
- [ ] Response includes answer, citations, confidence
- [ ] citations reference source_id from triples

### F4: Entity Linking
- [ ] Extracts age from question (e.g., "70岁")
- [ ] Matches entities by name and aliases
- [ ] Returns scored linked_entities

### F5: Evidence Retrieval
- [ ] Retrieves 1-2 hop subgraph
- [ ] Prioritizes evidence by relation type
- [ ] Limits results by TOP_K

### F6: LLM Integration
- [ ] Generates answer based only on triples
- [ ] Reports "unable to determine" if insufficient evidence
- [ ] Includes citations in answer

## Non-Functional Requirements

### N1: Performance
- [ ] /health responds < 100ms
- [ ] /subgraph responds < 2s
- [ ] /ask responds < 10s

### N2: Logging
- [ ] Every /ask request logged to JSONL
- [ ] Logs include: timestamp, question, linked_entities, cypher, triples, answer

### N3: Docker Deployment
- [ ] docker-compose up starts all services
- [ ] Backend accessible at localhost:8000/docs
- [ ] Neo4j accessible at localhost:7474

## Demo Questions (for validation)

1. 70岁高血压能买XX护理险吗？
2. 60岁老人可以购买哪些护理险？
3. 糖尿病患者是否被XX医疗险承保？
4. XX护理险的等待期是多久？
5. 高血压患者能获得哪些服务？
6. 65岁老人在XX养老院能享受什么服务？
7. 哪些产品覆盖糖尿病？
8. 哪些产品排除高血压？
9. 80岁老人能买什么保险？
10. XX公司提供哪些养老服务？
