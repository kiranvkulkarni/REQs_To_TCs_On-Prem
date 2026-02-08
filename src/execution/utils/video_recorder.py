import os
import subprocess
import time
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class VideoRecorder:
    def __init__(self, device, video_dir: Path, scenario_name: str):
        self.device = device
        self.video_dir = video_dir
        self.scenario_name = scenario_name
        self.video_path = None
        self.process = None

    def start(self) -> None:
        """
        Start video recording.
        """
        try:
            self.video_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{self.scenario_name}.mp4"
            self.video_path = self.video_dir / filename

            # Use ADB screenrecord
            cmd = [
                "adb", "shell", "screenrecord",
                "--bit-rate", "4000000",
                "--size", "1080x1920",
                str(self.video_path)
            ]

            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logger.info(f"🎥 Video recording started: {self.video_path}")
        except Exception as e:
            logger.error(f"Failed to start video recording: {e}")

    def stop(self) -> None:
        """
        Stop video recording.
        """
        if self.process:
            try:
                # Send Ctrl+C to stop screenrecord
                self.process.terminate()
                self.process.wait(timeout=5)
                logger.info(f"✅ Video recording stopped: {self.video_path}")
            except Exception as e:
                logger.error(f"Failed to stop video recording: {e}")