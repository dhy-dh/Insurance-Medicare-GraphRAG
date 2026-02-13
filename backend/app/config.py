from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "neo4j_password"

    # LLM
    LLM_PROVIDER: str = "mock"
    LLM_API_KEY: str = "mock_key"
    LLM_MODEL: str = "mock-model"

    # Application
    LOG_DIR: str = "./data/logs"
    SUBGRAPH_DEFAULT_HOP: int = 2
    SUBGRAPH_DEFAULT_LIMIT: int = 20


settings = Settings()
