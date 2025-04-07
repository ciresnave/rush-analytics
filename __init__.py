import logging
from enum import Enum
from typing import Any

from pydantic import BaseModel, HttpUrl, ValidationError

from .endpoints import RushAnalyticsAPI as BaseAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Endpoints(Enum):
    """Define API endpoints for Rush Analytics."""
    CREATE_TASK = "tasks"
    TASK_STATUS = "tasks/{task_id}"
    TASK_RESULTS = "tasks/{task_id}/results"
    LIST_LANGUAGES = "apiLanguages.php"
    LIST_GOOGLE_REGIONS = "apiRegionsGoogle.php"
    LIST_YANDEX_REGIONS = "apiRegionsYandex.php"

class TaskPayload(BaseModel):
    name: str
    url: HttpUrl
    competitors: list[str] = []
    data_collection_frequency: int = 0
    yandex_regions: list[dict[str, Any]] = []
    google_regions: list[dict[str, Any]] = []
    keywords: list[dict[str, str]] = []

def build_task_payload(**kwargs) -> TaskPayload:
    try:
        return TaskPayload(**kwargs)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        raise

class RushAnalyticsAPI(BaseAPI):
    """Interact with the Rush Analytics API."""

    def create_task(self, **kwargs) -> dict[str, Any]:
        try:
            payload = TaskPayload(**kwargs).dict()
            endpoint = Endpoints.CREATE_TASK.value
            return self.post_data(endpoint, payload)
        except ValidationError as e:
            logger.error(f"Validation error while creating task: {e}")
            raise

    def get_task_status(self, task_id: str) -> dict[str, Any]:
        """Retrieve the status of a specific task.

        Args:
            task_id (str): The ID of the task.

        Returns:
            Dict[str, Any]: The API response containing the task status.

        """
        endpoint = Endpoints.TASK_STATUS.value.format(task_id=task_id)
        params = {"apikey": self.api_key}
        return self.get_data(endpoint, params)

    def get_task_results(self, task_id: str) -> dict[str, Any]:
        """Fetch the results of a completed task.

        Args:
            task_id (str): The ID of the task.

        Returns:
            Dict[str, Any]: The API response containing the task results.

        """
        endpoint = Endpoints.TASK_RESULTS.value.format(task_id=task_id)
        params = {"apikey": self.api_key}
        return self.get_data(endpoint, params)

    @cached(cache)
    def list_languages(self) -> dict[str, Any]:
        logger.info("Fetching supported languages from API.")
        endpoint = Endpoints.LIST_LANGUAGES.value
        params = {"apikey": self.api_key}
        return self.get_data(endpoint, params)

    def list_google_regions(self) -> dict[str, Any]:
        """Fetch the list of supported Google regions from the API.

        Returns:
            dict[str, Any]: The API response containing the list of Google regions.

        """
        endpoint = Endpoints.LIST_GOOGLE_REGIONS.value
        params = {"apikey": self.api_key}
        return self.get_data(endpoint, params)

    def list_yandex_regions(self) -> dict[str, Any]:
        """Fetch the list of supported Yandex regions from the API.

        Returns:
            dict[str, Any]: The API response containing the list of Yandex regions.

        """
        endpoint = Endpoints.LIST_YANDEX_REGIONS.value
        params = {"apikey": self.api_key}
        return self.get_data(endpoint, params)

class AsyncRushAnalyticsAPI(RushAnalyticsAPI):
    """Asynchronous version of RushAnalyticsAPI."""

    async def create_task(
        self,
        name: str,
        url: str,
        competitors: list[str] | None = None,
        data_collection_frequency: int = 0,
        yandex_regions: list[dict[str, Any]] | None = None,
        google_regions: list[dict[str, Any]] | None = None,
        keywords: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        endpoint = Endpoints.CREATE_TASK.value
        payload = {
            "apikey": self.api_key,
            "name": name,
            "url": url,
            "competitors": competitors or [],
            "dataCollectionFrequency": data_collection_frequency,
            "yandexRegions": yandex_regions or [],
            "googleRegions": google_regions or [],
            "keywords": keywords or [],
        }
        return await self.post_data(endpoint, payload)

    async def async_get_task_status(self, task_id: str) -> dict[str, Any]:
        endpoint = Endpoints.TASK_STATUS.value.format(task_id=task_id)
        params = {"apikey": self.api_key}
        return await self.get_data(endpoint, params)

    async def async_get_task_results(self, task_id: str) -> dict[str, Any]:
        endpoint = Endpoints.TASK_RESULTS.value.format(task_id=task_id)
        params = {"apikey": self.api_key}
        return await self.get_data(endpoint, params)

    async def async_list_languages(self) -> dict[str, Any]:
        endpoint = Endpoints.LIST_LANGUAGES.value
        params = {"apikey": self.api_key}
        return await self.get_data(endpoint, params)

    async def async_list_google_regions(self) -> dict[str, Any]:
        endpoint = Endpoints.LIST_GOOGLE_REGIONS.value
        params = {"apikey": self.api_key}
        return await self.get_data(endpoint, params)

    async def async_list_yandex_regions(self) -> dict[str, Any]:
        endpoint = Endpoints.LIST_YANDEX_REGIONS.value
        params = {"apikey": self.api_key}
        return await self.get_data(endpoint, params)
