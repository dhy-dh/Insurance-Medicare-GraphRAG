from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.models import HealthResponse
from app.neo4j_client import neo4j_client
from app import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await neo4j_client.connect()
    yield
    # Shutdown
    await neo4j_client.close()


app = FastAPI(
    title="Insurance Medicare GraphRAG API",
    version="0.1.0",
    docs_url="/docs",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api/v1")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    neo4j_status = "ok" if await neo4j_client.health_check() else "fail"
    llm_status = "ok"  # Mock for MVP

    return HealthResponse(
        status="ok" if neo4j_status == "ok" else "degraded",
        neo4j=neo4j_status,
        llm=llm_status,
    )
