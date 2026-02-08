import unittest
from pathlib import Path
from src.ingestion.processor import ScreenshotIngestor
from src.generation.generator import GherkinGenerator
import yaml

class TestIngestion(unittest.TestCase):
    def setUp(self):
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.ingestor = ScreenshotIngestor(self.config)
        self.generator = GherkinGenerator(self.config)

    def test_generate(self):
        # Mock metadata
        metadata = {
            "filename": "flash_mode.png",
            "feature_name": "Flash Mode",
            "gestures": [{"type": "swipe_down", "target": "shutter_button"}],
            "conditions": ["timer_enabled"],
            "errors": ["storage_full"],
            "languages": ["en", "ko"],
            "version": 1
        }

        gherkin = self.generator.generate(metadata)
        self.assertIn("Feature: Flash Mode", gherkin)
        self.assertIn("Scenario: User swipe_down on shutter_button", gherkin)
        self.assertIn("Given the camera app is open in PHOTO mode", gherkin)
        self.assertIn("When the user swipe_down on the shutter_button", gherkin)
        self.assertIn("Then the system should detect 'swipe_down' gesture", gherkin)
        self.assertIn("And 시스템은 'swipe_down' 제스처를 인식해야 합니다", gherkin)

    def test_get_screenshots(self):
        screenshots = self.ingestor._get_screenshots()
        self.assertGreaterEqual(len(screenshots), 0)

    def test_process_screenshot(self):
        # Create a temporary test screenshot
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            test_screenshot = Path(temp_file.name)
            # Write some dummy content to make it look like a valid PNG
            temp_file.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc`\x00\x00\x00\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82')
        
        try:
            self.ingestor._process_screenshot(test_screenshot)
            # Assert KB has data
            conn = sqlite3.connect(self.config["kb"]["sqlite_db_path"])
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM screenshots")
            count = cursor.fetchone()[0]
            self.assertGreater(count, 0)
            conn.close()
        finally:
            # Clean up the temporary file
            test_screenshot.unlink()

if __name__ == "__main__":
    unittest.main()