from fastapi import APIRouter, HTTPException
from typing import List
import yaml

from src.ingestion.processor import ScreenshotIngestor
from src.backend.utils.retry import retry
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Load config
with open("config/settings.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

@router.post("/ingest", summary="Ingest screenshots from input folder")
@retry(max_attempts=3, delay_seconds=2)
def ingest_screenshots():
    """
    Scan input folder and ingest all screenshots into KB
    """
    try:
        logger.info(f"Config loaded: {config}")
        ingestor = ScreenshotIngestor(config)
        ingestor.run()
        return {"message": "Ingestion completed successfully"}
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
