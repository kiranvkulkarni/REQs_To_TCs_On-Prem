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


        import logging
        # Validate layout_data is a dict
        if not isinstance(layout_data, dict):
            logging.error("layout_data is not a dict. Returning minimal metadata.")
            return {
                "id": None,
                "filename": screenshot_path.name,
                "feature_name": self._extract_feature_name(screenshot_path.name),
                "gestures": [],
                "conditions": [],
                "errors": [],
                "languages": [],
                "text": [],
                "image_path": str(screenshot_path),
                "width": None,
                "height": None,
                "version": 1,
                "created_at": None,
                "embedding": None
            }

        # Try to extract UI elements from multiple possible keys
        ui_elements = layout_data.get("ui_elements")
        if ui_elements is None:
            # Try to extract from 'screens' or 'transitions' if present (Ollama output)
            if "screens" in layout_data and isinstance(layout_data["screens"], list):
                ui_elements = layout_data["screens"]
                logging.warning("layout_data missing 'ui_elements' key. Using 'screens' as fallback.")
            elif "transitions" in layout_data and isinstance(layout_data["transitions"], list):
                ui_elements = layout_data["transitions"]
                logging.warning("layout_data missing 'ui_elements' key. Using 'transitions' as fallback.")
            else:
                logging.warning("layout_data missing 'ui_elements', 'screens', and 'transitions' keys. Defaulting to empty list.")
                ui_elements = []

        text_elements = layout_data.get("text")
        if text_elements is None:
            # Try to extract from 'screens' if present (Ollama output)
            if "screens" in layout_data and isinstance(layout_data["screens"], list):
                text_elements = []
                for screen in layout_data["screens"]:
                    if "text_content" in screen:
                        for txt in screen["text_content"]:
                            text_elements.append({"text": txt, "lang": "en"})
                logging.warning("layout_data missing 'text' key. Extracted from 'screens' as fallback.")
            else:
                logging.warning("layout_data missing both 'text' and 'screens' keys. Defaulting to empty list.")
                text_elements = []

        # Validate width/height
        width = layout_data.get("width")
        height = layout_data.get("height")
        if width is None and "screens" in layout_data and isinstance(layout_data["screens"], list):
            # Try to extract from first screen
            first_screen = layout_data["screens"][0] if layout_data["screens"] else {}
            width = first_screen.get("width")
            height = first_screen.get("height")

        gestures = self._extract_gestures(ui_elements)
        conditions = self._extract_conditions(ui_elements)
        errors = self._extract_errors(ui_elements)
        languages = self._extract_languages(text_elements)

        metadata = {
            "id": None,  # Will be set by KBWriter
            "filename": screenshot_path.name,
            "feature_name": self._extract_feature_name(screenshot_path.name),
            "gestures": gestures,
            "conditions": conditions,
            "errors": errors,
            "languages": languages,
            "text": text_elements,
            "image_path": str(screenshot_path),
            "width": width,
            "height": height,
            "version": 1,
            "created_at": None,  # Set by KBWriter
            "embedding": None  # Set by KBWriter
        }

        return metadata

        metadata = {
            "id": None,  # Will be set by KBWriter
            "filename": filename,
            "feature_name": feature_name,
            "gestures": gestures,
            "conditions": conditions,
            "errors": errors,
            "languages": languages,
            "text": text_elements,
            "image_path": str(screenshot_path),
            "width": layout_data.get("width"),
            "height": layout_data.get("height"),
            "version": 1,
            "created_at": None,  # Set by KBWriter
            "embedding": None  # Set by KBWriter
        }

        return metadata

    def _extract_gestures(self, ui_elements: list) -> list:
        """
        Extract gestures from UI elements.
        Expected output: List of dicts with keys: type, target, bbox, confidence.
        """
        gestures = []
        for elem in ui_elements:
            if "gesture" in elem:
                gesture = elem["gesture"]
                gestures.append({
                    "type": gesture.get("type", "unknown"),
                    "target": gesture.get("target", elem.get("name", "unknown")),
                    "bbox": gesture.get("bbox", elem.get("bbox", [])),
                    "confidence": gesture.get("confidence", 1.0)
                })
        return gestures

    def _extract_conditions(self, ui_elements: list) -> list:
        """
        Extract conditions from UI elements.
        Expected output: List of strings.
        """
        conditions = []
        for elem in ui_elements:
            if "condition" in elem:
                cond = elem["condition"]
                if isinstance(cond, list):
                    conditions.extend(cond)
                else:
                    conditions.append(cond)
        return conditions

    def _extract_errors(self, ui_elements: list) -> list:
        """
        Extract errors from UI elements.
        Expected output: List of strings.
        """
        errors = []
        for elem in ui_elements:
            if "error" in elem:
                err = elem["error"]
                if isinstance(err, list):
                    errors.extend(err)
                else:
                    errors.append(err)
        return errors

    def _extract_languages(self, text_elements: list) -> list:
        """
        Extract languages from text elements.
        Expected output: List of language codes.
        """
        languages = set()
        for text in text_elements:
            lang = text.get("lang")
            if lang:
                languages.add(lang)
        return list(languages)

    def _extract_feature_name(self, filename: str) -> str:
        # Extract feature name from filename (e.g., "flash_mode.png" → "Flash Mode")
        name = filename.split(".")[0].replace("_", " ").title()
        return name