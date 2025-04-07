import unittest
from unittest.mock import AsyncMock, patch

from endpoints import AsyncRushAnalyticsAPI


@patch("httpx.AsyncClient.get")
async def test_async_get_data(mock_get: AsyncMock):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = AsyncMock()
    mock_get.return_value = mock_response

    api_client = AsyncRushAnalyticsAPI(api_key="test_api_key")
    response = await api_client.get_data("test_endpoint", {"param": "value"})

    assert response == {"success": True}
    mock_get.assert_called_once_with(
        "https://rush-analytics.com/api/test_endpoint",
        headers={
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json",
        },
        params={"param": "value"},
        timeout=10,
    )

@patch("httpx.AsyncClient.post")
async def test_async_post_data(mock_post: AsyncMock):
    mock_response = AsyncMock()
    mock_response.json.return_value = {"success": True}
    mock_response.raise_for_status = AsyncMock()
    mock_post.return_value = mock_response

    api_client = AsyncRushAnalyticsAPI(api_key="test_api_key")
    response = await api_client.async_post_data("test_endpoint", {"key": "value"})

    assert response == {"success": True}
    mock_post.assert_called_once_with(
        "https://rush-analytics.com/api/test_endpoint",
        headers={
            "Authorization": "Bearer test_api_key",
            "Content-Type": "application/json",
        },
        json={"key": "value"},
        timeout=10,
    )

@patch("httpx.AsyncClient.get")
async def test_async_invalid_api_key_error(mock_get: AsyncMock):
    """Test that InvalidAPIKeyError is raised for a 403 response in async_get_data."""
    mock_response = AsyncMock()
    mock_response.status_code = 403
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Forbidden", request=None, response=mock_response)
    mock_get.return_value = mock_response

    api_client = AsyncRushAnalyticsAPI(api_key="test_api_key")
    with pytest.raises(InvalidAPIKeyError):
        await api_client.async_get_data("test_endpoint")

@patch("httpx.AsyncClient.get")
async def test_async_rate_limit_exceeded_error(mock_get: AsyncMock):
    """Test that RateLimitExceededError is raised for a 429 response in async_get_data."""
    mock_response = AsyncMock()
    mock_response.status_code = 429
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError("Rate Limit Exceeded", request=None, response=mock_response)
    mock_get.return_value = mock_response

    api_client = AsyncRushAnalyticsAPI(api_key="test_api_key")
    with pytest.raises(RateLimitExceededError):
        await api_client.async_get_data("test_endpoint")
