from prometheus_client import start_http_server, Gauge, Counter, Summary
import time
import logging

logger = logging.getLogger(__name__)

# Define metrics
TESTS_TOTAL = Counter('camera_testgen_tests_total', 'Total number of tests executed')
TESTS_PASSED = Counter('camera_testgen_tests_passed', 'Total number of tests passed')
TESTS_FAILED = Counter('camera_testgen_tests_failed', 'Total number of tests failed')
TEST_DURATION = Summary('camera_testgen_test_duration_seconds', 'Duration of test execution in seconds')
TESTS_BY_FEATURE = Gauge('camera_testgen_tests_by_feature', 'Number of tests by feature', ['feature'])

class PrometheusExporter:
    def __init__(self, config: dict):
        self.config = config
        self.port = config["reporting"]["prometheus_port"]
        self.metrics = {}

    def start(self) -> None:
        """
        Start Prometheus metrics server.
        """
        start_http_server(self.port)
        logger.info(f"Prometheus metrics server started on port {self.port}")

    def record_test_result(self, feature: str, status: str, duration: float) -> None:
        """
        Record test result metrics.
        Args:
            feature (str): Feature name.
            status (str): Test status.
            duration (float): Test duration.
        """
        TESTS_TOTAL.inc()
        if status == "passed":
            TESTS_PASSED.inc()
        else:
            TESTS_FAILED.inc()

        TEST_DURATION.observe(duration)
        TESTS_BY_FEATURE.labels(feature=feature).inc()

    def get_metrics(self) -> dict:
        """
        Get current metrics.
        Returns:
            dict: Dictionary of current metrics.
        """
        return {
            "tests_total": TESTS_TOTAL._value.get(),
            "tests_passed": TESTS_PASSED._value.get(),
            "tests_failed": TESTS_FAILED._value.get(),
            "test_duration": TEST_DURATION._sum.get(),
            "tests_by_feature": {label: value for label, value in TESTS_BY_FEATURE._metrics.items()}
        }