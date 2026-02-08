from src.generation.generator import GherkinGenerator
from typing import Dict

class GenerationService:
    def __init__(self, config: dict):
        self.config = config
        self.generator = GherkinGenerator(config)

    def generate_gherkin(self, metadata: Dict) -> str:
        """
        Generate Gherkin test cases from metadata
        """
        return self.generator.generate(metadata)