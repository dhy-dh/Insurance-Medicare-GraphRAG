from typing import Optional, List, Any, Dict
from pydantic import BaseModel


# Health Check
class HealthResponse(BaseModel):
    status: str
    neo4j: str
    llm: str


# Linked Entity
class LinkedEntity(BaseModel):
    mention: str
    node_id: str
    label: str
    score: float


# Triple
class Triple(BaseModel):
    h: str
    r: str
    t: str
    source_id: Optional[str] = None


# Stats
class SubgraphStats(BaseModel):
    triples: int
    nodes: int


# Subgraph Request
class SubgraphRequest(BaseModel):
    query: str
    hop: int = 2
    limit: int = 20


# Subgraph Response
class SubgraphResponse(BaseModel):
    query: str
    hop: int
    linked_entities: List[LinkedEntity]
    triples: List[Triple]
    cypher: str
    stats: SubgraphStats


# Ask Request
class AskRequest(BaseModel):
    question: str
    hop: int = 2
    limit: int = 20


# Citation
class Citation(BaseModel):
    triple: str
    source_id: Optional[str] = None


# Debug Info
class DebugInfo(BaseModel):
    linked_entities: List[Dict[str, Any]]
    cypher: str
    triples_used: int


# Ask Response
class AskResponse(BaseModel):
    answer: str
    citations: List[Citation]
    confidence: str
    debug: DebugInfo
