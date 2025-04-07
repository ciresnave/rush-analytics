import os
import unittest
from typing import Any
from unittest.mock import Mock, patch

from endpoints import RushAnalyticsAPI


class UnexpectedResponseError(Exception):
    """Custom exception for unexpected API responses."""

    def __init__(self, response: dict[str, Any]) -> None:
        message = f"Unexpected response from API: {response}"
        super().__init__(message)


class MissingKeyError(Exception):
    """Custom exception for missing keys in API responses."""

    def __init__(self, key: str) -> None:
        message = f"Expected '{key}' key in the response."
        super().__init__(message)


class TestRushAnalyticsAPI(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the API client for testing."""
        self.api_key: str = os.getenv("RUSH_ANALYTICS_API_KEY", "test_api_key")
        self.api_client: RushAnalyticsAPI = RushAnalyticsAPI(api_key=self.api_key)
        self.run_live_tests: bool = os.getenv("RUN_LIVE_API_TESTS") == "1"

    @patch("requests.get")
    def test_get_data_mocked(self, mock_get: Mock) -> None:
        """Test the get_data method with mocked requests."""
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        response: dict[str, Any] = self.api_client.get_data("test_endpoint", {"param": "value"})
        if response != {"success": True}:
            error_message: str = (
                f"Expected response to be {{'success': True}}, but got: {response}"
            )
            raise AssertionError(error_message)
        mock_get.assert_called_once_with(
            "https://rush-analytics.com/api/test_endpoint",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            params={"param": "value"},
            timeout=10,
        )
        key: str = "languages"
        if key not in response:
            raise MissingKeyError(key)

    def test_get_data_live(self) -> None:
        """Test the get_data method with live API requests."""
        if not self.run_live_tests:
            self.skipTest("Skipping live API test. Set RUN_LIVE_API_TESTS=1 to enable.")
        response: dict[str, Any] = self.api_client.get_data("apiLanguages.php")
        key: str = "languages"
        if key not in response:
            raise MissingKeyError(key)

    @patch("requests.post")
    def test_post_data_mocked(self, mock_post: Mock) -> None:
        """Test the post_data method with mocked requests."""
        mock_response: Mock = Mock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        response: dict[str, Any] = self.api_client.post_data("test_endpoint", {"key": "value"})
        if response != {"success": True}:
            error_message: str = (
                f"Expected response to be {{'success': True}}, but got: {response}"
            )
            raise AssertionError(error_message)
        mock_post.assert_called_once_with(
            "https://rush-analytics.com/api/test_endpoint",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"key": "value"},
            timeout=10,
        )

    def test_post_data_live(self) -> None:
        """Test the post_data method with live API requests."""
        if not self.run_live_tests:
            self.skipTest("Skipping live API test. Set RUN_LIVE_API_TESTS=1 to enable.")
        # Replace with a valid endpoint and payload for live testing
        response: dict[str, Any] = self.api_client.post_data("tasks", {"name": "Test Task"})
        if "task_id" not in response:
            error_message: str = "Expected 'task_id' in the response."
            raise ValueError(error_message)

    def test_invalid_api_key(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = InvalidAPIKeyError()
            with self.assertRaises(InvalidAPIKeyError):
                self.api_client.post_data("test_endpoint", {"key": "value"})

    def test_retry_logic(self):
        with patch("requests.post") as mock_post:
            mock_post.side_effect = RequestError("Temporary error", 500)
            with self.assertRaises(RequestError):
                retry_request(lambda: self.api_client.post_data("test_endpoint", {"key": "value"}), retries=2)

    @patch("requests.get")
    def test_invalid_api_key_error(self, mock_get: Mock) -> None:
        """Test that InvalidAPIKeyError is raised for a 403 response."""
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get.return_value = mock_response

        with self.assertRaises(InvalidAPIKeyError):
            self.api_client.get_data("test_endpoint")

    @patch("requests.get")
    def test_rate_limit_exceeded_error(self, mock_get: Mock) -> None:
        """Test that RateLimitExceededError is raised for a 429 response."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = requests.HTTPError()
        mock_get.return_value = mock_response

        with self.assertRaises(RateLimitExceededError):
            self.api_client.get_data("test_endpoint")

    def test_invalid_task_payload(self):
    with self.assertRaises(ValidationError):
        TaskPayload(name="Test", url="invalid_url")


if __name__ == "__main__":
    unittest.main()
