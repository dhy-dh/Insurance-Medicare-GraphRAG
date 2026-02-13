# Deployment Guide

## Quick Start

### Step 1: Copy environment configuration
```bash
cp .env.example .env
```

Edit `.env` to set your Neo4j password:
```
NEO4J_PASSWORD=your_secure_password
```

### Step 2: Start services
```bash
docker compose up --build
```

### Step 3: Access services
- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474
  - Login: neo4j / your_password

## Services

### Neo4j
- Bolt: `bolt://localhost:7687`
- HTTP: `http://localhost:7474`

### Backend (FastAPI)
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

## Troubleshooting

### Neo4j won't start
- Check Docker logs: `docker logs insurance-neo4j`
- Verify memory allocation in docker-compose.yml

### Backend can't connect to Neo4j
- Wait for Neo4j to be ready (health check)
- Verify NEO4J_PASSWORD in .env matches

### Check logs
```bash
# Backend logs
docker logs insurance-backend

# Neo4j logs
docker logs insurance-neo4j
```
