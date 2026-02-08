import json
from typing import List, Dict

class GherkinFormatter:
    def __init__(self, config: dict):
        self.config = config

    def format(self, metadata: Dict, scenarios: List[Dict]) -> str:
        """
        Format scenarios into Gherkin syntax.
        Args:
            metadata (Dict): Screenshot metadata.
            scenarios (List[Dict]): List of scenario dicts.
        Returns:
            str: Gherkin formatted string.
        """
        feature_name = metadata["feature_name"]
        filename = metadata["filename"]
        version = metadata.get("version", 1)

        # Build Feature header
        feature = f"Feature: {feature_name}\n\n"

        # Build Scenarios
        scenario_blocks = []
        for i, scenario in enumerate(scenarios, 1):
            scenario_header = f"Scenario: {scenario['scenario']}\n"
            given = f"  Given {scenario['given']}\n"
            when = f"  When {scenario['when']}\n"
            then = f"  Then {scenario['then']}\n"
            scenario_blocks.append(f"{scenario_header}{given}{when}{then}\n")

        # Combine
        gherkin = feature + "".join(scenario_blocks)

        # Add version if configured
        if self.config["export"]["include_version"]:
            gherkin = f"# Generated from {filename} (v{version})\n\n" + gherkin

        return gherkin