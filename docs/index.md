# Rush Analytics Python Client Documentation

Welcome to the documentation for the Rush Analytics Python Client. This library provides a simple interface for interacting with the Rush Analytics API.

## Features

- Easy-to-use methods for accessing various API endpoints.
- Built-in error handling and response parsing.
- Unit tests to ensure functionality and reliability.

## Installation

To install the Rush Analytics client, use the following command:

```bash
pip install rush-analytics
```

## Usage

Here is an example of how to use the Rush Analytics client:

```python
from rush_analytics import RushAnalyticsAPI

# Initialize the API client
api_key = "your_api_key"
client = RushAnalyticsAPI(api_key=api_key)

# Example: Create a new task
response = client.create_task(
    name="My Task",
    url="https://example.com",
    competitors=["competitor1.com", "competitor2.com"],
    data_collection_frequency=1,
    yandex_regions=[{"id": 1, "name": "Region 1"}],
    google_regions=[{"id": 2, "name": "Region 2"}],
    keywords=[{"keyword": "example keyword"}]
)
print(response)
```

## Project Layout

The project is organized as follows:

```
rush-analytics/
├── __init__.py          # Main library file
├── endpoints.py         # Base API client implementation
├── README.md            # Project overview and usage examples
├── setup.py             # Packaging configuration
├── pyproject.toml       # Project metadata and dependencies
├── docs/                # Documentation files
│   └── index.md         # Documentation homepage
├── tests/               # Unit tests
│   ├── test_endpoints.py
│   ├── test_rush_analytics_api.py
└── utils/               # Utility functions
    └── helpers.py
```

## Asynchronous Usage

The library now supports asynchronous workflows. To use the asynchronous API, import and initialize the `AsyncRushAnalyticsAPI` class as shown below:

```python
from rush_analytics import AsyncRushAnalyticsAPI

# Initialize the async API client
api_key = "your_api_key"
client = AsyncRushAnalyticsAPI(api_key=api_key)

# Example: Create a new task asynchronously
import asyncio

async def main():
    response = await client.create_task(
        name="My Async Task",
        url="https://example.com",
        competitors=["competitor1.com", "competitor2.com"],
        data_collection_frequency=1,
        yandex_regions=[{"id": 1, "name": "Region 1"}],
        google_regions=[{"id": 2, "name": "Region 2"}],
        keywords=[{"keyword": "example keyword"}]
    )
    print(response)

asyncio.run(main())
```

### Note
Both synchronous and asynchronous APIs are available. Use the synchronous `RushAnalyticsAPI` class for simpler workflows or the asynchronous `AsyncRushAnalyticsAPI` class for async workflows.

## API Reference

The `RushAnalyticsAPI` class provides the following methods:

- `create_task`: Create a new task in the Rush Analytics system.
- `get_task_status`: Retrieve the status of a specific task.
- `get_task_results`: Fetch the results of a completed task.
- `list_languages`: Fetch the list of supported languages.
- `list_google_regions`: Fetch the list of supported Google regions.
- `list_yandex_regions`: Fetch the list of supported Yandex regions.

For detailed information about each method, refer to the [API Reference](endpoints.md).

## Running Tests

To run the unit tests for the Rush Analytics client, use the following command:

```bash
python -m unittest discover tests
```

### Code Quality Tools

1. **flake8**: Run `flake8` to check for linting issues.
2. **mypy**: Use `mypy` to validate type hints.
3. **black**: Format code using `black` to ensure consistency.

#### Example Commands

```bash
# Run flake8
flake8 src/ tests/

# Run mypy
typing mypy src/

# Format code with black
black src/ tests/
```

## Troubleshooting

### Common Errors

#### `InvalidAPIKeyError`
- **Cause**: The API key provided is invalid.
- **Solution**: Verify your API key and ensure it is correctly set in your environment variables.

#### `RateLimitExceededError`
- **Cause**: Too many requests were made in a short period.
- **Solution**: Wait for the rate limit to reset before making additional requests.

#### `ValidationError`
- **Cause**: Invalid input data was provided.
- **Solution**: Check the input data and ensure it meets the required format.

## Error Codes and Exceptions

| HTTP Status Code | Exception               | Description                                   |
|------------------|-------------------------|-----------------------------------------------|
| 403              | `InvalidAPIKeyError`   | Invalid API key provided.                    |
| 429              | `RateLimitExceededError` | Too many requests; rate limit exceeded.      |
| 404              | `NotFoundError`        | Resource not found.                          |
| 500              | `InternalServerError`  | Internal server error.                       |
| Other            | `RequestError`         | General request error for other status codes.|

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
