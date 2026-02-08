import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class RuleEngine:
    def __init__(self, config: dict):
        self.config = config

    def generate(self, metadata: Dict, fallback: bool = False) -> List[Dict]:
        """
        Generate Gherkin scenarios using rule-based logic.
        Args:
            metadata (Dict): Screenshot metadata.
            fallback (bool): If true, fallback to default scenario.
        Returns:
            List[Dict]: List of scenario dicts.
        """
        scenarios = []

        # Rule 1: If gesture exists → create scenario for it
        gestures = metadata.get("gestures", [])
        if isinstance(gestures, list):
            for gesture in gestures:
                scenario = self._generate_gesture_scenario(metadata, gesture)
                if scenario:
                    scenarios.append(scenario)

        # Rule 2: If conditions exist → create scenario for each
        conditions = metadata.get("conditions", [])
        if isinstance(conditions, list):
            for condition in conditions:
                scenario = self._generate_condition_scenario(metadata, condition)
                if scenario:
                    scenarios.append(scenario)

        # Rule 3: If errors exist → create scenario for each
        errors = metadata.get("errors", [])
        if isinstance(errors, list):
            for error in errors:
                scenario = self._generate_error_scenario(metadata, error)
                if scenario:
                    scenarios.append(scenario)

        # Rule 4: If no gestures/conditions/errors → create default scenario
        if not scenarios:
            scenario = self._generate_default_scenario(metadata)
            if scenario:
                scenarios.append(scenario)

        return scenarios

    def _generate_gesture_scenario(self, metadata: Dict, gesture: Dict) -> Dict:
        """
        Generate scenario for gesture (e.g., swipe down).
        Args:
            metadata (Dict): Screenshot metadata.
            gesture (Dict): Gesture dict.
        Returns:
            Dict: Scenario dict.
        """
        feature_name = metadata["feature_name"]
        gesture_type = gesture["type"]
        target = gesture["target"]

        # Build scenario steps
        given = f"Given the camera app is open in PHOTO mode"
        when = f"When the user {gesture_type} on the {target}"
        then = f"Then the system should detect '{gesture_type}' gesture"

        # Add language-specific then steps if needed
        if "ko" in metadata["languages"]:
            then_ko = f"그리고 시스템은 '{gesture_type}' 제스처를 인식해야 합니다"
            then = f"{then}\nAnd {then_ko}"

        return {
            "scenario": f"User {gesture_type} on {target}",
            "given": given,
            "when": when,
            "then": then
        }

    def _generate_condition_scenario(self, metadata: Dict, condition: str) -> Dict:
        """
        Generate scenario for condition (e.g., timer_enabled).
        Args:
            metadata (Dict): Screenshot metadata.
            condition (str): Condition name.
        Returns:
            Dict: Scenario dict.
        """
        feature_name = metadata["feature_name"]

        given = f"Given the {condition} is enabled"
        when = f"When the user performs the primary action"
        then = f"Then the system should display a warning: '{condition} is enabled'"

        if "ko" in metadata["languages"]:
            then_ko = f"그리고 시스템은 '{condition}이 활성화됨' 경고를 표시해야 합니다"
            then = f"{then}\nAnd {then_ko}"

        return {
            "scenario": f"Condition: {condition}",
            "given": given,
            "when": when,
            "then": then
        }

    def _generate_error_scenario(self, metadata: Dict, error: str) -> Dict:
        """
        Generate scenario for error (e.g., storage_full).
        Args:
            metadata (Dict): Screenshot metadata.
            error (str): Error message.
        Returns:
            Dict: Scenario dict.
        """
        feature_name = metadata["feature_name"]

        given = f"Given the {error} condition is met"
        when = f"When the user attempts to perform the action"
        then = f"Then a toast popup should appear: '{error}'"

        if "ko" in metadata["languages"]:
            then_ko = f"그리고 토스트 팝업이 '{error}' 메시지를 표시해야 합니다"
            then = f"{then}\nAnd {then_ko}"

        return {
            "scenario": f"Error: {error}",
            "given": given,
            "when": when,
            "then": then
        }

    def _generate_default_scenario(self, metadata: Dict) -> Dict:
        """
        Generate default scenario if no specific rules apply.
        Args:
            metadata (Dict): Screenshot metadata.
        Returns:
            Dict: Scenario dict.
        """
        feature_name = metadata["feature_name"]

        given = f"Given the camera app is open in PHOTO mode"
        when = f"When the user views the UI"
        then = f"Then all UI elements should be visible and functional"

        if "ko" in metadata["languages"]:
            then_ko = f"그리고 모든 UI 요소가 보이고 기능해야 합니다"
            then = f"{then}\nAnd {then_ko}"

        return {
            "scenario": "Default UI visibility",
            "given": given,
            "when": when,
            "then": then
        }