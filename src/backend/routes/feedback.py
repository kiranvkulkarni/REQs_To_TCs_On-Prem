from fastapi import APIRouter, HTTPException
from typing import List, Dict

from src.backend.services.kb_service import KBService
from src.backend.utils.retry import retry
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/feedback", summary="Log user feedback for rejected test cases")
@retry(max_attempts=3, delay_seconds=2)
def log_feedback(
    screenshot_id: int,
    status: str,  # "accepted" or "rejected"
    rejection_reason: str = None,
    comment: str = None
):
    """
    Log user feedback for a test case
    """
    try:
        kb_service = KBService({})

        updates = {"status": status}
        if status == "rejected":
            updates["rejection_reason"] = rejection_reason
            updates["comment"] = comment
            updates["version"] = updates.get("version", 1) + 1  # Version bump on rejection

        kb_service.update_screenshot(screenshot_id, updates)
        return {"message": "Feedback logged successfully", "screenshot_id": screenshot_id, "status": status}
    except Exception as e:
        logger.error(f"Feedback logging failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))