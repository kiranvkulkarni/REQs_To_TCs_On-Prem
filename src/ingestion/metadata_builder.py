import json
from pathlib import Path
from typing import Dict, List

class MetadataBuilder:
    def __init__(self, config: dict):
        self.config = config

    def build(self, screenshot_path: str, layout_data: dict) -> dict:
        """
        Build structured metadata from LayoutLM output
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

    def _extract_gestures(self, ui_elements: List[dict]) -> List[dict]:
        return [
            {
                "type": elem["subtype"],
                "target": elem["target"],
                "bbox": elem["bbox"],
                "confidence": elem["confidence"]
            }
            for elem in ui_elements
            if elem["type"] == "gesture"
        ]

    def _extract_conditions(self, ui_elements: List[dict]) -> List[str]:
        return [
            elem["name"]
            for elem in ui_elements
            if elem["type"] == "condition"
        ]

    def _extract_errors(self, ui_elements: List[dict]) -> List[str]:
        return [
            elem["message"]
            for elem in ui_elements
            if elem["type"] == "error"
        ]

    def _extract_languages(self, text: List[dict]) -> List[str]:
        return list(set([t["lang"] for t in text]))