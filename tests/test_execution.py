import unittest
from src.execution.executor import TestExecutor
import yaml

class TestExecution(unittest.TestCase):
    def setUp(self):
        with open("config/settings.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        self.executor = TestExecutor(self.config)

    def test_get_feature_files(self):
        feature_files = self.executor._get_feature_files()
        self.assertGreaterEqual(len(feature_files), 0)

    def test_execute(self):
        # Mock a feature file
        test_feature = "data/exports/Flash_Mode_v1.feature"
        if not Path(test_feature).exists():
            with open(test_feature, "w", encoding="utf-8") as f:
                f.write("Feature: Flash Mode\n\nScenario: User swipes down on shutter button\n  Given the camera app is open in PHOTO mode\n  When the user swipes down on the shutter_button\n  Then the system should detect 'swipe_down' gesture")
        results = self.executor.run()
        self.assertGreaterEqual(len(results), 1)

if __name__ == "__main__":
    unittest.main()