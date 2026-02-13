from typing import List, Optional, Dict, Any
from neo4j import AsyncGraphDatabase, AsyncDriver

from app.config import settings


class Neo4jClient:
    def __init__(self):
        self.driver: Optional[AsyncDriver] = None

    async def connect(self):
        """Connect to Neo4j"""
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )

    async def close(self):
        """Close connection"""
        if self.driver:
            await self.driver.close()

    async def health_check(self) -> bool:
        """Check if Neo4j is reachable"""
        try:
            async with self.driver.session() as session:
                result = await session.run("RETURN 1 AS n")
                await result.single()
                return True
        except Exception:
            return False

    async def find_nodes_by_name_or_alias(
        self, mention: str, topk: int = 5
    ) -> List[Dict[str, Any]]:
        """Find nodes by name or alias"""
        if not self.driver:
            return []

        query = """
        MATCH (n)
        WHERE toLower(n.name) = toLower($name)
           OR (exists(n.aliases) AND any(a IN n.aliases WHERE toLower(a) = toLower($name)))
        RETURN n.node_id AS node_id,
               n.name AS name,
               labels(n)[0] AS label,
               1.0 AS score
        LIMIT $topk
        """

        async with self.driver.session() as session:
            result = await session.run(
                query, name=mention.strip(), topk=topk
            )
            records = await result.data()

        return records

    async def fetch_subgraph(
        self,
        node_ids: List[str],
        hop: int = 2,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Fetch subgraph around given nodes"""
        if not self.driver or not node_ids:
            return []

        # Simplified 1-hop query for MVP
        query = """
        MATCH (a)-[r]-(b)
        WHERE a.node_id IN $node_ids
        RETURN a.name AS head,
               type(r) AS relation,
               b.name AS tail,
               r.source_id AS source_id,
               a.node_id AS head_id,
               b.node_id AS tail_id
        LIMIT $limit
        """

        async with self.driver.session() as session:
            result = await session.run(query, node_ids=node_ids, limit=limit)
            records = await result.data()

        return records


neo4j_client = Neo4jClient()
