from fastapi import APIRouter, HTTPException
from typing import List, Dict

from src.backend.services.kb_service import KBService
from src.backend.services.export_service import ExportService
from src.backend.utils.retry import retry
import logging
import yaml

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/export", summary="Export accepted test cases to .feature files")
@retry(max_attempts=3, delay_seconds=2)
def export_feature_files():
    """
    Export all accepted test cases to .feature files
    Grouped by feature name (configurable)
    """
    try:
        # Load config from settings.yaml
        with open("config/settings.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        kb_service = KBService(config)
        export_service = ExportService(config)

        screenshots = kb_service.get_all_screenshots()
        accepted_screenshots = [s for s in screenshots if s.get("status") == "accepted"]

        if not accepted_screenshots:
            return {"message": "No accepted test cases to export"}

        if export_service.config["export"]["group_by"] == "feature":
            grouped = export_service.group_by_feature(accepted_screenshots)
            for feature_name, group in grouped.items():
                gherkin_content = ""
                for screenshot in group:
                    gherkin_content += screenshot["gherkin"] + "\n\n"
                filepath = export_service.export_feature_file(feature_name, gherkin_content,
version=group[0]["version"])
                logger.info(f"Exported {feature_name} to {filepath}")
        else:  # group_by == "screenshot"
            for screenshot in accepted_screenshots:
                filepath = export_service.export_feature_file(screenshot["feature_name"], screenshot["gherkin"],
version=screenshot["version"])
                logger.info(f"Exported {screenshot['filename']} to {filepath}")

        return {"message": "Export completed", "exported_files": len(accepted_screenshots)}
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))