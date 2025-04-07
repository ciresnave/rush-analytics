from typing import Any, Coroutine, override

import requests
import httpx
import time
import asyncio
import logging
from cachetools import TTLCache, cached

logger = logging.getLogger(__name__)

cache = TTLCache(maxsize=100, ttl=3600)


class RequestError(Exception):
    """Custom exception for request-related errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        if status_code is not None:
            message = f"{message} (HTTP {status_code})"
        super().__init__(message)


class InvalidAPIKeyError(RequestError):
    """Raised when an invalid API key is detected."""

    def __init__(self, message: str = "Invalid API key provided. Please check your API key.", status_code: int = 403) -> None:
        super().__init__(message, status_code)


class RateLimitExceededError(RequestError):
    """Raised when the API rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded. Please wait before making additional requests.", status_code: int = 429) -> None:
        super().__init__(message, status_code)


class NotFoundError(RequestError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found.", status_code: int = 404) -> None:
        super().__init__(message, status_code)


class InternalServerError(RequestError):
    """Raised when the server encounters an internal error."""

    def __init__(self, message: str = "Internal server error. Please try again later.", status_code: int = 500) -> None:
        super().__init__(message, status_code)


class RushAnalyticsAPI:
    BASE_URL = "https://rush-analytics.com/api"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(headers=self._get_headers(), timeout=10)

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @cached(cache)
    def get_data(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    def post_data(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        logger.info(f"POST request to {endpoint} with data: {data}")
        try:
            url = f"{self.BASE_URL}/{endpoint}"
            response = self.client.post(url, json=data)
            response.raise_for_status()
            logger.info(f"POST request to {endpoint} succeeded.")
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    def _handle_http_error(self, e: httpx.HTTPStatusError) -> None:
        status_code = e.response.status_code
        if status_code == 403:
            raise InvalidAPIKeyError() from e
        elif status_code == 429:
            raise RateLimitExceededError() from e
        elif status_code == 404:
            raise NotFoundError() from e
        elif status_code == 500:
            raise InternalServerError() from e
        else:
            raise RequestError(f"HTTP error occurred: {status_code}") from e

    def close(self) -> None:
        self.client.close()


class AsyncRushAnalyticsAPI(RushAnalyticsAPI):
    """Asynchronous version of RushAnalyticsAPI."""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = httpx.AsyncClient(headers=self._get_headers(), timeout=10)

    async def async_get_data(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Asynchronously fetch data from the specified API endpoint.

        Parameters
        ----------
        endpoint : str
            The API endpoint to fetch data from.
        params : dict[str, Any] | None, optional
            Query parameters to include in the request.

        Returns
        -------
        dict[str, Any]
            The JSON response as a dictionary.

        Raises
        ------
        RequestError
            If a request or HTTP error occurs, including rate limits, forbidden access, or other HTTP errors.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    async def async_post_data(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Perform an asynchronous POST request to the API.

        Args:
            endpoint (str): The API endpoint.
            data (dict[str, Any]): The JSON payload to send.

        Returns:
            dict[str, Any]: The JSON response from the API.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = await self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            self._handle_http_error(e)

    def _handle_http_error(self, e: httpx.HTTPStatusError) -> None:
        status_code = e.response.status_code
        if status_code == 403:
            raise InvalidAPIKeyError() from e
        elif status_code == 429:
            raise RateLimitExceededError() from e
        elif status_code == 404:
            raise NotFoundError() from e
        elif status_code == 500:
            raise InternalServerError() from e
        else:
            raise RequestError(f"HTTP error occurred: {status_code}") from e

    async def close(self) -> None:
        await self.client.aclose()


def retry_request(func, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            return func()
        except RequestError as e:
            if attempt < retries - 1:
                time.sleep(backoff ** attempt)
            else:
                raise e


async def async_retry_request(func, retries=3, backoff=2):
    for attempt in range(retries):
        try:
            return await func()
        except RequestError as e:
            if attempt < retries - 1:
                await asyncio.sleep(backoff ** attempt)
            else:
                raise e
