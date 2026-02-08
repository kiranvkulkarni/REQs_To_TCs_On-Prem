import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def capture_screenshot(device, step_name: str, screenshot_dir: Path, scenario_name: str) -> str:
    """
    Capture screenshot on failure.
    Args:
        device: uiautomator2 device instance.
        step_name (str): Name of the step (for filename).
        screenshot_dir (Path): Directory to save screenshots.
        scenario_name (str): Name of the scenario (for folder).
    Returns:
        str: Path to the saved screenshot file, or None if failed.
    """
    try:
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{scenario_name}_{step_name.replace(' ', '_')}.png".replace(':', '_')
        filepath = screenshot_dir / filename
        device.screenshot(str(filepath))
        logger.info(f"📸 Screenshot captured: {filepath}")
        return str(filepath)
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return None