# Insurance+Medicare GraphRAG

基于知识图谱的保险问答系统 (GraphRAG)。支持从保险条款中提取实体与关系，并通过图谱检索增强问答质量。

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Insurance+Medicare GraphRAG                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐              │
│  │  User   │────▶│ Streamlit│────▶│ FastAPI │────▶│  Neo4j  │              │
│  │ (Input) │     │   UI    │     │ Backend │     │ GraphDB │              │
│  └─────────┘     └─────────┘     └─────────┘     └─────────┘              │
│                                              │           │                   │
│                                              ▼           ▼                   │
│                                        ┌─────────┐   ┌─────────┐             │
│                                        │   LLM   │   │  Graph  │             │
│                                        │ Client  │   │ Engine  │             │
│                                        └─────────┘   └─────────┘             │
│                                              │                               │
│                                              ▼                               │
│                                        ┌─────────┐                         │
│                                        │ Prompt  │                         │
│                                        │ Builder │                         │
│                                        └─────────┘                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 一键启动

```bash
# 1. 复制环境配置
cp .env.example .env

# 2. 启动服务 (Neo4j + Backend)
cd deploy
docker compose up --build

# 3. 访问
# - API文档: http://localhost:8000/docs
# - Neo4j Browser: http://localhost:7474
```

## 快速导入样例图谱

```bash
cd kg/scripts
python make_sample_data.py  # 生成样例数据
python load_neo4j.py --uri bolt://localhost:7687 --user neo4j --password your_password
```

## 问答流程

```
┌──────────┐    ┌────────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│ Question │───▶│  Entity    │───▶│ Subgraph │───▶│ Prompt  │───▶│   LLM   │
│          │    │  Linker    │    │ Retrieval│    │ Builder │    │ Generate│
└──────────┘    └────────────┘    └──────────┘    └─────────┘    └─────────┘
                                             │                              │
                                             ▼                              ▼
                                      ┌────────────┐              ┌──────────────┐
                                      │   Graph    │              │   Answer    │
                                      │   (Neo4j) │              │ + Citations │
                                      └────────────┘              └──────────────┘
```

## Demo 示例问题

1. **70岁高血压能买XX护理险吗？**
2. **60岁老人可以购买哪些护理险？**
3. **糖尿病患者是否被XX医疗险承保？**

## 目录说明

```
Insurance-Medicare-GraphRAG/
├── backend/                 # FastAPI 后端服务
│   ├── app/
│   │   ├── config.py       # 配置管理
│   │   ├── models.py       # Pydantic 模型
│   │   ├── main.py        # FastAPI 应用
│   │   ├── routes.py      # API 路由
│   │   ├── neo4j_client.py# Neo4j 客户端
│   │   ├── entity_linker.py# 实体链接
│   │   ├── subgraph.py    # 子图检索
│   │   ├── rag_engine.py  # RAG 引擎
│   │   ├── prompt_builder.py# Prompt 构建
│   │   ├── llm_client.py  # LLM 客户端
│   │   └── logging_utils.py# 日志工具
│   ├── requirements.txt
│   └── Dockerfile
│
├── kg/                     # 图谱构建与导入
│   ├── scripts/
│   │   ├── make_sample_data.py  # 生成样例数据
│   │   ├── validate_data.py     # 数据验证
│   │   └── load_neo4j.py        # 导入 Neo4j
│   └── README.md
│
├── ui/                     # Streamlit 前端
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
│
├── docs/                   # 文档
│   ├── api_contract.md     # API 契约
│   ├── ontology.md         # 本体定义
│   ├── data_contract.md   # 数据格式
│   ├── acceptance.md      # 验收标准
│   └── eval_questions.json# 评估问题集
│
├── deploy/                 # 部署配置
│   ├── docker-compose.yml
│   └── README.md
│
├── data/                   # 数据目录
│   ├── processed/         # 处理后的数据
│   │   ├── nodes.csv
│   │   └── edges.csv
│   ├── synonyms/          # 同义词库
│   │   └── synonyms.json
│   └── logs/              # 运行日志
│
├── scripts/                # 脚本工具
│   └── run_demo.py        # 批量测试
│
├── .env.example
└── README.md
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| GET | `/api/v1/subgraph?query=...` | 查询子图 |
| POST | `/api/v1/ask` | 问答接口 |

详见 [docs/api_contract.md](docs/api_contract.md)
