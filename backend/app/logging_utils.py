import os
import json
from datetime import datetime
from typing import Dict, Any, List

from app.config import settings


def get_log_dir() -> str:
    """Get log directory"""
    log_dir = settings.LOG_DIR
    if not os.path.isabs(log_dir):
        # Relative to project root
        log_dir = os.path.join(os.path.dirname(__file__), "../../../", log_dir)

    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def log_question(
    question: str,
    linked_entities: List[Dict[str, Any]],
    cypher: str,
    triples: List[Dict[str, Any]],
    prompt: str,
    answer: str,
    citations: List[Dict[str, Any]],
) -> None:
    """Log question and answer to JSONL file"""

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "linked_entities": linked_entities,
        "cypher": cypher,
        "triples": triples,
        "prompt": prompt,
        "answer": answer,
        "citations": citations,
    }

    log_file = os.path.join(get_log_dir(), "qa_logs.jsonl")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
