import logging
import logging.config
from pathlib import Path

def setup_logger(config: dict):
    """
    Setup structured logging
    """
    Path(config["file"]).parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=config["level"],
        format=config["format"],
        handlers=[
            logging.FileHandler(config["file"], encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)