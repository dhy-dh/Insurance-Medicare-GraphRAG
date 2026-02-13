# Data Contract

## Directory Structure
```
data/
├── processed/
│   ├── nodes.csv
│   └── edges.csv
├── synonyms/
│   └── synonyms.json
└── logs/
```

## nodes.csv Format

| Column | Required | Description |
|--------|----------|-------------|
| node_id | Yes | Unique identifier |
| label | Yes | Node label (Disease/Drug/InsuranceProduct/ElderCareOrg/Service) |
| name | Yes | Primary name |
| aliases_json | No | JSON array of alternative names |
| age_min | No | Minimum age (for InsuranceProduct) |
| age_max | No | Maximum age (for InsuranceProduct) |
| product_id | No | Product ID (for InsuranceProduct) |
| org_id | No | Organization ID (for ElderCareOrg) |
| city | No | City (for ElderCareOrg) |
| source_id | No | Source document ID |

### Example
```csv
node_id,label,name,aliases_json,age_min,age_max,product_id,source_id
d_001,Disease,高血压,"[""原发性高血压"",""HTN""]",,,,doc_001
p_001,InsuranceProduct,XX护理险,"[""长期护理保险""]",60,75,prod_001,doc_002
```

## edges.csv Format

| Column | Required | Description |
|--------|----------|-------------|
| head_id | Yes | Source node_id |
| relation | Yes | Relationship type |
| tail_id | Yes | Target node_id |
| source_id | No | Source document ID |

### Example
```csv
head_id,relation,tail_id,source_id
p_001,COVERS,d_001,clause_12
p_001,EXCLUDES,d_001,clause_08
```

## synonyms.json Format

```json
{
  "高血压": ["原发性高血压", "HTN"],
  "护理险": ["长期护理保险", "长期护理险"],
  "糖尿病": ["DM", "糖尿病"]
}
```

## Validation Rules
1. node_id must be unique
2. head_id and tail_id must exist in nodes.csv
3. relation must be one of: TREATS, COVERS, EXCLUDES, AGE_RANGE, PROVIDES
4. aliases_json must be valid JSON array if provided
