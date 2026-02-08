import os
import logging
from pathlib import Path
from typing import List

from .layoutlm_analyzer import LayoutLMAnalyzer
from .metadata_builder import MetadataBuilder
from .kb_writer import KBWriter

logger = logging.getLogger(__name__)

class ScreenshotIngestor:
    def __init__(self, config: dict):
        self.config = config
        self.input_folder = Path(config["ingestion"]["input_folder"])
        self.supported_exts = set(config["ingestion"]["supported_extensions"])
        self.max_retries = config["ingestion"]["max_retries"]
        self.kb_writer = KBWriter(config)
        self.layoutlm = LayoutLMAnalyzer(config)
        self.metadata_builder = MetadataBuilder(config)

    def run(self):
        logger.info(f"Starting ingestion from {self.input_folder}")
        screenshots = self._get_screenshots()
        for screenshot in screenshots:
            self._process_screenshot(screenshot)
        logger.info("Ingestion completed.")

    def _get_screenshots(self) -> List[Path]:
        screenshots = []
        for file in self.input_folder.iterdir():
            if file.suffix.lower() in self.supported_exts:
                screenshots.append(file)
        logger.info(f"Found {len(screenshots)} screenshots.")
        return screenshots

    def _process_screenshot(self, screenshot_path: str):
        # Convert string to Path if needed
        if isinstance(screenshot_path, str):
            screenshot_path = Path(screenshot_path)
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"Processing {screenshot_path} (Attempt {attempt})")
                layout_data = self.layoutlm.analyze(screenshot_path)
                metadata = self.metadata_builder.build(screenshot_path, layout_data)
                self.kb_writer.write(metadata)
                logger.info(f"✅ {screenshot_path.name} ingested successfully.")
                break
            except Exception as e:
                logger.error(f"❌ Failed to process {screenshot_path} (Attempt {attempt}): {e}")
                if attempt == self.max_retries:
                    logger.critical(f"💥 Giving up on {screenshot_path.name} after {self.max_retries} attempts.")
