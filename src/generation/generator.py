import logging
from typing import List, Dict

from .rule_engine import RuleEngine
from .llm_adapter import LLMAdapter
from .gherkin_formatter import GherkinFormatter

logger = logging.getLogger(__name__)

class GherkinGenerator:
    def __init__(self, config: dict):
        self.config = config
        self.rule_engine = RuleEngine(config)
        self.llm_adapter = LLMAdapter(config)
        self.gherkin_formatter = GherkinFormatter(config)

    def generate(self, metadata: Dict) -> str:
        """
        Generate Gherkin test cases from metadata.
        Priority: Rule-Based > LLM > Fallback to Rule-Based.
        Args:
            metadata (Dict): Screenshot metadata.
        Returns:
            str: Gherkin formatted test cases.
        """
        logger.info(f"Generating Gherkin for {metadata['filename']}")

        # Step 1: Try Rule-Based
        try:
            rule_based_scenarios = self.rule_engine.generate(metadata)
            if rule_based_scenarios:
                logger.info("✅ Rule-based generation successful.")
                return self.gherkin_formatter.format(metadata, rule_based_scenarios)
        except Exception as e:
            logger.warning(f"⚠️ Rule-based generation failed: {e}")

        # Step 2: Try LLM
        if not self.config["generation"]["rule_priority"]:
            try:
                llm_output = self.llm_adapter.generate(metadata)
                if llm_output:
                    logger.info("✅ LLM generation successful.")
                    return llm_output
            except Exception as e:
                logger.warning(f"⚠️ LLM generation failed: {e}")

        # Step 3: Fallback to Rule-Based (if enabled)
        if self.config["generation"]["fallback_to_rule_only"]:
            try:
                fallback_scenarios = self.rule_engine.generate(metadata, fallback=True)
                logger.info("✅ Fallback rule-based generation successful.")
                return self.gherkin_formatter.format(metadata, fallback_scenarios)
            except Exception as e:
                logger.error(f"💥 Generation failed for {metadata['filename']}: {e}")
                return ""

        logger.error(f"💥 No generation method succeeded for {metadata['filename']}")
        return ""