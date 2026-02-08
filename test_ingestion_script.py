from src.ingestion.processor import ScreenshotIngestor
from src.ingestion.layoutlm_analyzer import LayoutLMAnalyzer
import yaml

# Load config
with open('config/settings.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# Create ingestor
ingestor = ScreenshotIngestor(config)

# Process a specific screenshot
ingestor._process_screenshot('data/input_screenshots/FLASH.jpeg')