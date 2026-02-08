import os
import logging
from pathlib import Path
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .cucumber_adapter import CucumberAdapter
from .uiautomator2_adapter import UIAutomator2Adapter
from .report_generator import ReportGenerator

logger = logging.getLogger(__name__)

class TestExecutor:
    def __init__(self, config: dict):
        self.config = config
        self.test_dir = Path(config["execution"]["test_dir"])
        self.report_dir = Path(config["execution"]["report_dir"])
        self.cucumber = CucumberAdapter(config)
        self.reporter = ReportGenerator(config)
        self.parallel = config["execution"]["parallel"]
        self.device_serials = config["execution"].get("device_serials", [])  # List of device serials

    def run(self):
        logger.info("Starting test execution...")
        feature_files = self._get_feature_files()
        results = []

        if self.parallel and self.device_serials:
            # Parallel execution on multiple devices
            with ThreadPoolExecutor(max_workers=len(self.device_serials)) as executor:
                futures = []
                for i, feature_file in enumerate(feature_files):
                    device_serial = self.device_serials[i % len(self.device_serials)]
                    futures.append(executor.submit(self._execute_feature, feature_file, device_serial))
                for future in as_completed(futures):
                    results.append(future.result())
        else:
            # Sequential execution
            for feature_file in feature_files:
                result = self._execute_feature(feature_file)
                results.append(result)

        logger.info("Test execution completed.")
        return results

    def _execute_feature(self, feature_file: Path, device_serial: str = None) -> Dict:
        """
        Execute a single feature file
        """
        logger.info(f"Executing {feature_file.name} on device {device_serial or 'default'}")
        try:
            feature = self.cucumber.parse(feature_file)

            # Create adapter with device serial
            adapter_config = self.config.copy()
            if device_serial:
                adapter_config["execution"]["device_serial"] = device_serial
            adapter = UIAutomator2Adapter(adapter_config)

            execution_result = adapter.execute(feature)
            report_path = self.reporter.generate(feature, execution_result)

            return {
                "feature": feature_file.name,
                "status": execution_result["status"],
                "report": str(report_path),
                "duration": execution_result["duration"],
                "screenshots": execution_result.get("screenshots", []),
                "videos": execution_result.get("videos", [])
            }

        except Exception as e:
            logger.error(f"❌ Failed to execute {feature_file.name}: {e}")
            return {
                "feature": feature_file.name,
                "status": "failed",
                "report": None,
                "duration": 0,
                "screenshots": [],
                "videos": []
            }

    def _get_feature_files(self) -> List[Path]:
        feature_files = []
        for file in self.test_dir.iterdir():
            if file.suffix == ".feature":
                feature_files.append(file)
        logger.info(f"Found {len(feature_files)} .feature files.")
        return feature_files