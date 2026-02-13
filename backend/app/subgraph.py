from typing import List, Dict, Any
from app.models import Triple

# Priority order for relations
RELATION_PRIORITY = [
    "AGE_RANGE",
    "EXCLUDES",
    "COVERS",
    "TREATS",
    "PROVIDES",
]


def format_triples(raw_triples: List[Dict[str, Any]]) -> List[Triple]:
    """Format raw Neo4j results into Triple objects"""
    triples = []
    for t in raw_triples:
        triples.append(
            Triple(
                h=t.get("head", ""),
                r=t.get("relation", ""),
                t=t.get("tail", ""),
                source_id=t.get("source_id"),
            )
        )
    return triples


def prioritize_triples(triples: List[Triple], topk: int = 20) -> List[Triple]:
    """
    Prioritize triples by relation type

    Priority order:
    1. AGE_RANGE
    2. EXCLUDES
    3. COVERS
    4. TREATS
    5. PROVIDES
    """
    # Sort by priority
    sorted_triples = sorted(
        triples,
        key=lambda t: (
            RELATION_PRIORITY.index(t.r) if t.r in RELATION_PRIORITY else len(RELATION_PRIORITY),
            -len(t.source_id or ""),  # Prefer with source_id
        ),
    )

    return sorted_triples[:topk]


def get_subgraph_stats(triples: List[Triple], node_ids: List[str]) -> Dict[str, int]:
    """Calculate subgraph statistics"""
    unique_nodes = set(node_ids)
    for t in triples:
        unique_nodes.add(t.h)
        unique_nodes.add(t.t)

    return {
        "triples": len(triples),
        "nodes": len(unique_nodes),
    }
