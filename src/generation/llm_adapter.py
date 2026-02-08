import logging
import requests
from typing import Dict

logger = logging.getLogger(__name__)

class LLMAdapter:
    def __init__(self, config: dict):
        self.config = config
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = config["generation"]["llm_model"]
        self.temperature = config["generation"]["llm_temperature"]
        self.max_tokens = config["generation"]["llm_max_tokens"]

    def generate(self, metadata: Dict) -> str:
        """
        Generate Gherkin using Ollama LLM
        """
        prompt = self._build_prompt(metadata)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "stream": False
        }

        try:
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    def _build_prompt(self, metadata: Dict) -> str:
        """
        Build prompt using template from config
        """
        template = self.config["generation"]["prompt_template"]
        metadata_str = json.dumps(metadata, ensure_ascii=False, indent=2)
        return template.format(metadata=metadata_str)