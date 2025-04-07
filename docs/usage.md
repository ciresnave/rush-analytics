# Usage Examples

## Create a Task
```python
response = client.create_task(
    name="My Task",
    url="https://example.com",
    competitors=["competitor1.com"],
    data_collection_frequency=1,
    yandex_regions=[{"id": 1}],
    google_regions=[{"id": 2}],
    keywords=[{"keyword": "example"}]
)
print(response)
```

## Get Task Status
```python
status = client.get_task_status(task_id="12345")
print(status)
```

## Get Task Results
```python
results = client.get_task_results(task_id="12345")
print(results)
```

## List Supported Languages
```python
languages = client.list_languages()
print(languages)
```

## List Google Regions
```python
google_regions = client.list_google_regions()
print(google_regions)
```

## List Yandex Regions
```python
yandex_regions = client.list_yandex_regions()
print(yandex_regions)
```