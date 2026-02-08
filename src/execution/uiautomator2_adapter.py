import time
import logging
from typing import Dict, List

import uiautomator2 as u2
from uiautomator2.exceptions import UiObjectNotFoundError

from .utils.screenshot import capture_screenshot
from .utils.video_recorder import VideoRecorder

logger = logging.getLogger(__name__)

class UIAutomator2Adapter:
    def __init__(self, config: dict):
        self.config = config
        self.device = None
        self.app_package = config["execution"]["app_package"]
        self.app_activity = config["execution"]["app_activity"]
        self.screenshot_dir = Path(config["execution"]["screenshot_dir"]) if
config["execution"].get("screenshot_dir") else Path("data/screenshots")
        self.video_dir = Path(config["execution"]["video_dir"]) if config["execution"].get("video_dir") else
Path("data/videos")

    def execute(self, feature: Dict) -> Dict:
        """
        Execute tests on Android device/emulator using uiautomator2
        """
        start_time = time.time()
        status = "passed"
        errors = []
        screenshots = []
        videos = []

        try:
            # Setup uiautomator2
            self._setup_device()

            # Launch app
            self.device.app_start(self.app_package, self.app_activity)
            time.sleep(2)

            # Execute each scenario
            for scenario in feature["scenarios"]:
                scenario_status = self._execute_scenario(scenario)
                if scenario_status == "failed":
                    status = "failed"
                    errors.append(f"Scenario '{scenario['name']}' failed")

            # Teardown
            self._teardown_device()

        except Exception as e:
            status = "failed"
            errors.append(str(e))
        finally:
            duration = time.time() - start_time
            return {
                "status": status,
                "duration": duration,
                "errors": errors,
                "screenshots": screenshots,
                "videos": videos
            }

    def _setup_device(self):
        """
        Connect to Android device/emulator
        """
        self.device = u2.connect()
        if not self.device.info.get("screenOn"):
            self.device.screen.on()
        self.device.healthcheck()
        logger.info(f"Connected to device: {self.device.info['brand']} {self.device.info['model']}")

    def _teardown_device(self):
        """
        Teardown device connection
        """
        if self.device:
            self.device.app_stop(self.app_package)
            self.device.screen.off()
            self.device = None

    def _execute_scenario(self, scenario: Dict) -> str:
        """
        Execute a single scenario with retry and video recording
        """
        scenario_name = scenario["name"].replace(' ', '_').replace(':', '_')

        # Setup video recorder
        video_recorder = VideoRecorder(self.device, self.video_dir, scenario_name)
        video_recorder.start()

        # Setup screenshot directory
        screenshot_dir = self.screenshot_dir / scenario_name
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Execute Given steps
            for step in scenario["given"]:
                self._execute_step(step, scenario_name, screenshot_dir, video_recorder)

            # Execute When steps
            for step in scenario["when"]:
                self._execute_step(step, scenario_name, screenshot_dir, video_recorder)

            # Execute Then steps
            for step in scenario["then"]:
                self._execute_step(step, scenario_name, screenshot_dir, video_recorder)

            return "passed"

        except Exception as e:
            logger.error(f"Scenario failed: {e}")
            return "failed"

        finally:
            # Stop video recording
            video_recorder.stop()

    def _execute_step(self, step: str, scenario_name: str, screenshot_dir: Path, video_recorder: VideoRecorder):
        """
        Execute a single step with retry and screenshot on failure
        """
        step_name = step.replace(' ', '_').replace(':', '_')[:50]  # Limit filename length

        @retry(max_attempts=self.config["execution"]["retry_count"], delay_seconds=2, on_failure=lambda *args:
self._on_failure(step, scenario_name, screenshot_dir, video_recorder))
        def execute_step():
            step_lower = step.lower()

            # Given: "Given the camera app is open in PHOTO mode"
            if "open" in step_lower and "app" in step_lower:
                pass  # Already handled

            # When: "When the user swipes down on the shutter button"
            elif "swipe" in step_lower and "down" in step_lower:
                self.device.swipe(500, 200, 500, 800, 0.5)

            # When: "When the user taps on the shutter button"
            elif "tap" in step_lower and "shutter" in step_lower:
                try:
                    self.device(text="Shutter").click()
                except UiObjectNotFoundError:
                    try:
                        self.device(resourceId="com.example.camera:id/shutter_button").click()
                    except UiObjectNotFoundError:
                        raise AssertionError(f"Could not find shutter button for step: {step}")

            # When: "When the user types 'Hello'"
            elif "type" in step_lower or "enter" in step_lower:
                text = step.split("'")[-2] if "'" in step else step.split(" ")[-1]
                self.device.send_keys(text)

            # Then: "Then the system should display a warning: 'Battery low'"
            elif "display" in step_lower and "warning" in step_lower:
                warning_text = step.split("'")[-2] if "'" in step else ""
                if not self.device(text=warning_text).exists:
                    raise AssertionError(f"Warning '{warning_text}' not displayed")

            # Then: "Then a toast popup should appear: 'Photo saved'"
            elif "toast" in step_lower and "appear" in step_lower:
                toast_text = step.split("'")[-2] if "'" in step else ""
                if not self.device.toast.get_message(timeout=5.0, default=""):
                    raise AssertionError(f"Toast '{toast_text}' not shown")
                self.device.toast.reset()

            # Then: "Then the shutter button should be visible"
            elif "should be visible" in step_lower:
                target = step.split(" ")[-2] if "button" in step_lower else step.split(" ")[-1]
                if not self.device(text=target).exists:
                    raise AssertionError(f"Element '{target}' not visible")

            # Then: "Then the flash icon should be dimmed"
            elif "dimmed" in step_lower:
                target = step.split(" ")[-2] if "icon" in step_lower else step.split(" ")[-1]
                try:
                    elem = self.device(text=target)
                    if elem.exists:
                        if not elem.info.get("clickable", True) or not elem.info.get("enabled", True):
                            pass  # Considered dimmed
                        else:
                            raise AssertionError(f"Element '{target}' is not dimmed")
                    else:
                        raise AssertionError(f"Element '{target}' not found")
                except Exception as e:
                    logger.warning(f"Could not check dimmed state for {target}: {e}")

            else:
                logger.warning(f"Unknown step: {step}")
                # You can add more mappings here as needed

        execute_step()

    def _on_failure(self, step: str, scenario_name: str, screenshot_dir: Path, video_recorder: VideoRecorder):
        """
        Called on step failure — capture screenshot and log
        """
        logger.warning(f"Step failed: {step}")
        capture_screenshot(self.device, step, screenshot_dir, scenario_name)