import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def capture_screenshot(device, step_name: str, screenshot_dir: Path, scenario_name: str):
    """
    Capture screenshot on failure
    :param device: uiautomator2 device instance
    :param step_name: Name of the step (for filename)
    :param screenshot_dir: Directory to save screenshots
    :param scenario_name: Name of the scenario (for folder)
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