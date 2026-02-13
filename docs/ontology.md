# Ontology Definition

## Node Labels

### Disease
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| node_id | string | Yes | Unique identifier (e.g., d_001) |
| name | string | Yes | Disease name |
| icd_code | string | No | ICD-10 code |
| aliases | list[string] | No | Alternative names |
| source_id | string | No | Source document ID |

### Drug
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| node_id | string | Yes | Unique identifier |
| name | string | Yes | Drug name |
| aliases | list[string] | No | Alternative names |
| source_id | string | No | Source document ID |

### InsuranceProduct
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| node_id | string | Yes | Unique identifier |
| product_id | string | Yes | Product code |
| name | string | Yes | Product name |
| type | string | No | Product type (护理险/医疗险/重疾险) |
| age_min | int | No | Minimum age |
| age_max | int | No | Maximum age |
| waiting_period_days | int | No | Waiting period |
| aliases | list[string] | No | Alternative names |
| source_id | string | Yes | Source document ID |

### ElderCareOrg
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| node_id | string | Yes | Unique identifier |
| org_id | string | Yes | Organization ID |
| name | string | Yes | Organization name |
| city | string | No | City |
| services | list[string] | No | Services offered |
| aliases | list[string] | No | Alternative names |
| source_id | string | No | Source document ID |

### Service
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| node_id | string | Yes | Unique identifier |
| name | string | Yes | Service name |
| aliases | list[string] | No | Alternative names |

## Relationship Types

| Relation | From | To | Properties |
|----------|------|-----|------------|
| TREATS | Drug | Disease | source_id |
| COVERS | InsuranceProduct | Disease | source_id |
| EXCLUDES | InsuranceProduct | Disease | source_id |
| AGE_RANGE | InsuranceProduct | InsuranceProduct | source_id, value (e.g., "60-75") |
| PROVIDES | ElderCareOrg | Service | source_id |

### Priority Order (for evidence ranking)
1. AGE_RANGE
2. EXCLUDES
3. COVERS
4. TREATS
5. PROVIDES
