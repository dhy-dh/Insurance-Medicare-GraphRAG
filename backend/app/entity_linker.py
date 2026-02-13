import re
import json
import os
from typing import List, Dict, Any, Optional

from app.neo4j_client import neo4j_client


# Load synonyms
def load_synonyms() -> Dict[str, List[str]]:
    """Load synonyms from file"""
    synonyms_path = os.path.join(os.path.dirname(__file__), "../../../data/synonyms/synonyms.json")
    if os.path.exists(synonyms_path):
        with open(synonyms_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


SYNONYMS = load_synonyms()


def extract_age(question: str) -> Optional[int]:
    """Extract age from question using regex"""
    match = re.search(r"(\d{1,3})岁", question)
    if match:
        return int(match.group(1))
    return None


def expand_with_synonyms(mention: str) -> List[str]:
    """Expand mention with synonyms"""
    mentions = [mention]
    # Check if mention is a key
    if mention in SYNONYMS:
        mentions.extend(SYNONYMS[mention])
    # Check if mention is a value
    for key, values in SYNONYMS.items():
        if mention in values:
            mentions.append(key)
    return mentions


async def link_entities(question: str) -> List[Dict[str, Any]]:
    """
    Link entities from question to graph nodes

    Returns list of linked entities with scores
    """
    # Extract key terms (simplified: split by common delimiters)
    # In production, use NLP for entity extraction
    terms = re.split(r"[，。、？?！!\s,]+", question)
    terms = [t.strip() for t in terms if t.strip() and len(t.strip()) > 1]

    linked_entities = []

    for term in terms:
        # Expand with synonyms
        expanded_terms = expand_with_synonyms(term)

        for exp_term in expanded_terms:
            # Query Neo4j
            nodes = await neo4j_client.find_nodes_by_name_or_alias(exp_term, topk=5)

            for node in nodes:
                # Check if already in list
                existing = next(
                    (e for e in linked_entities if e["node_id"] == node["node_id"]),
                    None,
                )
                if existing:
                    # Update with higher score
                    if node["score"] > existing["score"]:
                        existing["score"] = node["score"]
                        existing["mention"] = term
                else:
                    linked_entities.append({
                        "mention": term,
                        "node_id": node["node_id"],
                        "label": node["label"],
                        "score": node["score"],
                    })

    # Sort by score descending
    linked_entities.sort(key=lambda x: x["score"], reverse=True)

    return linked_entities
