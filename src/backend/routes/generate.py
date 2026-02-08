from fastapi import APIRouter, HTTPException
from typing import List, Dict

from src.backend.services.kb_service import KBService
from src.backend.services.generation_service import GenerationService
from src.backend.utils.retry import retry
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", summary="Generate Gherkin test cases for all screenshots")
@retry(max_attempts=3, delay_seconds=2)
def generate_gherkin():
    """
    Generate Gherkin test cases for all screenshots in KB
    """
    try:
        from src.backend.main import app
        kb_service = KBService(app.state.config)
        generation_service = GenerationService(app.state.config)

        screenshots = kb_service.get_all_screenshots()
        results = []

        for screenshot in screenshots:
            gherkin = generation_service.generate_gherkin(screenshot)
            screenshot["gherkin"] = gherkin
            screenshot["status"] = "generated"
            kb_service.update_screenshot(screenshot["id"], {"gherkin": gherkin, "status": "generated"})
            results.append({
                "id": screenshot["id"],
                "filename": screenshot["filename"],
                "feature_name": screenshot["feature_name"],
                "status": "generated"
            })

        return {"message": "Generation completed", "results": results}
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))