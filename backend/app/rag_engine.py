from typing import Dict, Any, List

from app.models import (
    AskResponse,
    Citation,
    DebugInfo,
    Triple,
)
from app.neo4j_client import neo4j_client
from app import entity_linker
from app import subgraph as subgraph_module
from app import prompt_builder
from app.llm_client import llm_client
from app import logging_utils


async def answer_question(
    question: str,
    hop: int = 2,
    limit: int = 20,
) -> AskResponse:
    """Main RAG orchestration"""

    # Step 1: Entity linking
    linked_entities = await entity_linker.link_entities(question)

    if not linked_entities:
        # No entities found - return empty response
        return AskResponse(
            answer="未能在问题中识别出相关实体，请重新描述您的问题。",
            citations=[],
            confidence="low",
            debug=DebugInfo(
                linked_entities=[],
                cypher="",
                triples_used=0,
            ),
        )

    # Step 2: Get node IDs and fetch subgraph
    node_ids = [e["node_id"] for e in linked_entities]
    raw_triples = await neo4j_client.fetch_subgraph(node_ids, hop=hop, limit=limit)

    # Step 3: Format and prioritize triples
    triples = subgraph_module.format_triples(raw_triples)
    triples = subgraph_module.prioritize_triples(triples, topk=limit)

    # Step 4: Build prompt
    prompt = prompt_builder.build_prompt(question, triples)

    # Step 5: Generate answer
    answer_text = await llm_client.generate(prompt)

    # Step 6: Build citations from top triples
    citations = [
        Citation(
            triple=f"({t.h}, {t.r}, {t.t})",
            source_id=t.source_id,
        )
        for t in triples[:5]  # Top 5 citations
    ]

    # Step 7: Calculate confidence
    confidence = _calculate_confidence(triples, linked_entities)

    # Step 8: Log the interaction
    logging_utils.log_question(
        question=question,
        linked_entities=linked_entities,
        cypher=f"MATCH (a)-[r]-(b) WHERE a.node_id IN {node_ids}",
        triples=[t.model_dump() for t in triples],
        prompt=prompt,
        answer=answer_text,
        citations=[c.model_dump() for c in citations],
    )

    return AskResponse(
        answer=answer_text,
        citations=citations,
        confidence=confidence,
        debug=DebugInfo(
            linked_entities=linked_entities,
            cypher=f"MATCH (a)-[r]-(b) WHERE a.node_id IN {node_ids}",
            triples_used=len(triples),
        ),
    )


def _calculate_confidence(triples: List[Triple], linked_entities: List[Dict[str, Any]]) -> str:
    """Calculate confidence based on evidence"""
    if not triples:
        return "low"

    # Check for high-priority relations
    priority_relations = {"AGE_RANGE", "EXCLUDES", "COVERS"}
    has_priority = any(t.r in priority_relations for t in triples)

    # Check evidence count
    evidence_count = len(triples)

    if evidence_count >= 2 and has_priority:
        return "high"
    elif evidence_count >= 1:
        return "medium"
    else:
        return "low"
