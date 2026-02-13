from fastapi import APIRouter, Query, HTTPException
from typing import Optional

from app.models import (
    SubgraphResponse,
    SubgraphStats,
    LinkedEntity,
    Triple,
    AskRequest,
    AskResponse,
    Citation,
    DebugInfo,
)
from app.config import settings
from app.neo4j_client import neo4j_client
from app import entity_linker
from app import subgraph
from app import rag_engine

router = APIRouter()


@router.get("/subgraph", response_model=SubgraphResponse)
async def get_subgraph(
    query: str = Query(..., description="Entity mention to search"),
    hop: int = Query(settings.SUBGRAPH_DEFAULT_HOP, ge=1, le=3),
    limit: int = Query(settings.SUBGRAPH_DEFAULT_LIMIT, ge=1, le=100),
):
    """Query subgraph by entity name"""
    # Entity linking
    linked_entities = await entity_linker.link_entities(query)

    if not linked_entities:
        return SubgraphResponse(
            query=query,
            hop=hop,
            linked_entities=[],
            triples=[],
            cypher="",
            stats=SubgraphStats(triples=0, nodes=0),
        )

    # Get node IDs
    node_ids = [e["node_id"] for e in linked_entities]

    # Fetch subgraph
    raw_triples = await neo4j_client.fetch_subgraph(node_ids, hop=hop, limit=limit)

    # Format triples
    triples = [
        Triple(
            h=t["head"],
            r=t["relation"],
            t=t["tail"],
            source_id=t.get("source_id"),
        )
        for t in raw_triples
    ]

    # Build response
    linked = [
        LinkedEntity(
            mention=e.get("mention", ""),
            node_id=e["node_id"],
            label=e.get("label", ""),
            score=e.get("score", 0.0),
        )
        for e in linked_entities
    ]

    cypher = f"MATCH (a)-[r]-(b) WHERE a.node_id IN {node_ids} RETURN a,r,b LIMIT {limit}"

    return SubgraphResponse(
        query=query,
        hop=hop,
        linked_entities=linked,
        triples=triples,
        cypher=cypher,
        stats=SubgraphStats(triples=len(triples), nodes=len(node_ids)),
    )


@router.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    """Ask a question using GraphRAG"""
    try:
        result = await rag_engine.answer_question(
            question=request.question,
            hop=request.hop,
            limit=request.limit,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
