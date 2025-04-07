import os
import unittest
from typing import Any
from unittest.mock import Mock, patch

from __init__ import Endpoints, RushAnalyticsAPI


class InvalidResponseError(AssertionError):
    """Custom exception for invalid API responses."""

    def __init__(self, expected: dict[str, Any], actual: dict[str, Any]) -> None:
        message: str = f"Expected response to be {expected}, but got {actual}"
        super().__init__(message)


class TestRushAnalyticsAPI(unittest.TestCase):
    def setUp(self) -> None:
        """Set up the API client for testing."""
        self.api_key: str = os.getenv("RUSH_ANALYTICS_API_KEY", "test_api_key")
        self.api_client: RushAnalyticsAPI = RushAnalyticsAPI(api_key=self.api_key)

    @patch("endpoints.RushAnalyticsAPI.post_data")
    def test_create_task(self, mock_post_data: Mock) -> None:
        """Test the create_task method."""
        mock_post_data.return_value = {"task_id": "12345"}

        response: dict[str, Any] = self.api_client.create_task(
            name="Test Task",
            url="https://example.com",
            competitors=["competitor1.com"],
            data_collection_frequency=1,
            yandex_regions=[{"id": 1}],
            google_regions=[{"id": 2}],
            keywords=[{"keyword": "test"}],
        )
        expected_response: dict[str, Any] = {"task_id": "12345"}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_post_data.assert_called_once_with(
            Endpoints.CREATE_TASK.value,
            {
                "apikey": "test_api_key",
                "name": "Test Task",
                "url": "https://example.com",
                "competitors": ["competitor1.com"],
                "dataCollectionFrequency": 1,
                "yandexRegions": [{"id": 1}],
                "googleRegions": [{"id": 2}],
                "keywords": [{"keyword": "test"}],
            },
        )

    @patch("endpoints.RushAnalyticsAPI.get_data")
    def test_get_task_status(self, mock_get_data: Mock) -> None:
        """Test the get_task_status method."""
        mock_get_data.return_value = {"status": "completed"}

        response: dict[str, Any] = self.api_client.get_task_status(task_id="12345")
        expected_response: dict[str, Any] = {"status": "completed"}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_get_data.assert_called_once_with(
            Endpoints.TASK_STATUS.value.format(task_id="12345"),
            {"apikey": "test_api_key"},
        )

    @patch("endpoints.RushAnalyticsAPI.get_data")
    def test_get_task_results(self, mock_get_data: Mock) -> None:
        """Test the get_task_results method."""
        mock_get_data.return_value = {"results": []}

        response: dict[str, Any] = self.api_client.get_task_results(task_id="12345")
        expected_response: dict[str, Any] = {"results": []}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_get_data.assert_called_once_with(
            Endpoints.TASK_RESULTS.value.format(task_id="12345"),
            {"apikey": "test_api_key"},
        )

    @patch("endpoints.RushAnalyticsAPI.get_data")
    def test_list_languages(self, mock_get_data: Mock) -> None:
        """Test the list_languages method."""
        mock_get_data.return_value = {"languages": ["en", "ru"]}

        response: dict[str, Any] = self.api_client.list_languages()
        expected_response: dict[str, Any] = {"languages": ["en", "ru"]}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_get_data.assert_called_once_with(
            Endpoints.LIST_LANGUAGES.value,
            {"apikey": "test_api_key"},
        )

    @patch("endpoints.RushAnalyticsAPI.get_data")
    def test_list_google_regions(self, mock_get_data: Mock) -> None:
        """Test the list_google_regions method."""
        mock_get_data.return_value = {"regions": ["US", "CA"]}

        response: dict[str, Any] = self.api_client.list_google_regions()
        expected_response: dict[str, Any] = {"regions": ["US", "CA"]}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_get_data.assert_called_once_with(
            Endpoints.LIST_GOOGLE_REGIONS.value,
            {"apikey": "test_api_key"},
        )

    @patch("endpoints.RushAnalyticsAPI.get_data")
    def test_list_yandex_regions(self, mock_get_data: Mock) -> None:
        """Test the list_yandex_regions method."""
        mock_get_data.return_value = {"regions": ["RU", "BY"]}

        response: dict[str, Any] = self.api_client.list_yandex_regions()
        expected_response: dict[str, Any] = {"regions": ["RU", "BY"]}
        if response != expected_response:
            raise InvalidResponseError(expected_response, response)
        mock_get_data.assert_called_once_with(
            Endpoints.LIST_YANDEX_REGIONS.value,
            {"apikey": "test_api_key"},
        )


if __name__ == "__main__":
    unittest.main()
