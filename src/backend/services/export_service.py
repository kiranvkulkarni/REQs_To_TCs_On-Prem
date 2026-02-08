import os
from pathlib import Path
from typing import List, Dict

class ExportService:
    def __init__(self, config: dict):
        self.config = config
        self.output_dir = Path(config["export"]["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_feature_file(self, feature_name: str, gherkin_content: str, version: int = 1):
        """
        Export Gherkin to .feature file
        """
        filename = f"{feature_name.replace(' ', '_')}"
        if self.config["export"]["include_version"]:
            filename = f"{filename}_v{version}"
        filename = f"{filename}{self.config['export']['file_extension']}"

        filepath = self.output_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(gherkin_content)

        return str(filepath)

    def group_by_feature(self, screenshots: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Group screenshots by feature name
        """
        grouped = {}
        for screenshot in screenshots:
            feature_name = screenshot["feature_name"]
            if feature_name not in grouped:
                grouped[feature_name] = []
            grouped[feature_name].append(screenshot)
        return grouped