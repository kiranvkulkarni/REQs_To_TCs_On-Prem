import re
from pathlib import Path
from typing import Dict, List

class CucumberAdapter:
    def __init__(self, config: dict):
        self.config = config

    def parse(self, feature_file: Path) -> Dict:
        """
        Parse .feature file into structured data.
        Args:
            feature_file (Path): Path to the .feature file.
        Returns:
            Dict: Parsed feature structure.
        """
        content = feature_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        feature = {
            "name": "",
            "description": "",
            "scenarios": []
        }

        current_scenario = None
        in_scenario = False

        for line in lines:
            line = line.strip()
            if line.startswith("Feature:"):
                feature["name"] = line[8:].strip()
            elif line.startswith("#") and not in_scenario:
                feature["description"] += line[1:].strip() + "\n"
            elif line.startswith("Scenario:"):
                if current_scenario:
                    feature["scenarios"].append(current_scenario)
                current_scenario = {
                    "name": line[9:].strip(),
                    "steps": [],
                    "given": [],
                    "when": [],
                    "then": []
                }
                in_scenario = True
            elif line.startswith("Given ") and in_scenario:
                current_scenario["given"].append(line[6:].strip())
                current_scenario["steps"].append({"type": "given", "text": line[6:].strip()})
            elif line.startswith("When ") and in_scenario:
                current_scenario["when"].append(line[5:].strip())
                current_scenario["steps"].append({"type": "when", "text": line[5:].strip()})
            elif line.startswith("Then ") and in_scenario:
                current_scenario["then"].append(line[5:].strip())
                current_scenario["steps"].append({"type": "then", "text": line[5:].strip()})
            elif line.startswith("And ") and in_scenario:
                # Handle "And" as continuation of previous step type
                if current_scenario["steps"]:
                    last_type = current_scenario["steps"][-1]["type"]
                    current_scenario[last_type].append(line[4:].strip())
                    current_scenario["steps"].append({"type": last_type, "text": line[4:].strip()})

        if current_scenario:
            feature["scenarios"].append(current_scenario)

        return feature