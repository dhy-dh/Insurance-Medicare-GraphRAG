from typing import Optional
import requests

from app.config import settings


class LLMClient:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.api_key = settings.LLM_API_KEY
        self.model = settings.LLM_MODEL

    async def generate(self, prompt: str) -> str:
        """Generate response from LLM"""
        if self.provider == "mock":
            return self._mock_generate(prompt)
        elif self.provider == "openai_compatible":
            return self._openai_compatible_generate(prompt)
        else:
            return self._mock_generate(prompt)

    def _mock_generate(self, prompt: str) -> str:
        """Mock LLM for testing"""
        # Return a simple template response for MVP
        return "根据提供的证据信息，无法明确判断。请补充更多相关证据。"

    def _openai_compatible_generate(self, prompt: str) -> str:
        """OpenAI compatible API call"""
        # This is a generic implementation - adjust based on actual API
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=30,
            )
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"


llm_client = LLMClient()
