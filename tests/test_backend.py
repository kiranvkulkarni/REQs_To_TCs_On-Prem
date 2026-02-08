import unittest
from fastapi.testclient import TestClient
from src.backend.main import app

client = TestClient(app)

class TestBackend(unittest.TestCase):
    def test_root(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_ingest(self):
        response = client.post("/api/v1/ingest")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_generate(self):
        response = client.post("/api/v1/generate")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_export(self):
        response = client.get("/api/v1/export")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

    def test_feedback(self):
        # Mock a screenshot ID
        response = client.post("/api/v1/feedback", json={
            "screenshot_id": 1,
            "status": "rejected",
            "rejection_reason": "Wrong gesture interpretation",
            "comment": "Swipe down should be tap"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())

if __name__ == "__main__":
    unittest.main()