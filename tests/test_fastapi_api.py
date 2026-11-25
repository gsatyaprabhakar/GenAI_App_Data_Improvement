import sys
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.api.fastapi_api import app


class FastApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_home_endpoint(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Welcome To Data Improvement API"},
        )

    def test_blank_request_is_rejected(self):
        response = self.client.post("/improve", json={"request": "          "})

        self.assertEqual(response.status_code, 422)

    def test_missing_api_key_returns_service_unavailable(self):
        import os

        previous_key = os.environ.pop("GOOGLE_API_KEY", None)
        try:
            response = self.client.post(
                "/improve",
                json={"request": "Improve this text"},
            )
        finally:
            if previous_key is not None:
                os.environ["GOOGLE_API_KEY"] = previous_key

        self.assertEqual(response.status_code, 503)


if __name__ == "__main__":
    unittest.main()
