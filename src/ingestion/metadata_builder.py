import json
from pathlib import Path
from typing import Dict, List

class MetadataBuilder:
    def __init__(self, config: dict):
        self.config = config

    def build(self, screenshot_path: str, layout_data: dict) -> dict:
        """
        Build structured metadata from Ollama output.
        Args:
            screenshot_path (str): Path to the screenshot file.
            layout_data (dict): Parsed output from Ollama vision model.
        Returns:
            dict: Structured metadata for KBWriter.
        """
        # Convert string to Path if needed
        if isinstance(screenshot_path, str):
            screenshot_path = Path(screenshot_path)
        filename = screenshot_path.name
        feature_name = self._extract_feature_name(filename)

        gestures = self._extract_gestures(layout_data["ui_elements"])
        conditions = self._extract_conditions(layout_data["ui_elements"])
        errors = self._extract_errors(layout_data["ui_elements"])
        languages = self._extract_languages(layout_data["text"])

        metadata = {
            "id": None,  # Will be set by KBWriter
            "filename": filename,
            "feature_name": feature_name,
            "gestures": gestures,
            "conditions": conditions,
            "errors": errors,
            "languages": languages,
            "text": layout_data["text"],
            "image_path": str(screenshot_path),
            "width": layout_data["width"],
            "height": layout_data["height"],
            "version": 1,
            "created_at": None,  # Set by KBWriter
            "embedding": None  # Set by KBWriter
        }

        return metadata

    def _extract_feature_name(self, filename: str) -> str:
        # Extract feature name from filename (e.g., "flash_mode.png" → "Flash Mode")
        name = filename.split(".")[0].replace("_", " ").title()
        return name