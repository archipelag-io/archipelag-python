# Python SDK Architecture

> Internal developer documentation for the Archipelag.io Python SDK.

## Overview

Lightweight Python client with sync and async support for submitting jobs and managing workloads.

## Package Structure

```
archipelag/
├── __init__.py       # Public exports
├── client.py         # Client and AsyncClient classes
├── models.py         # Pydantic data models
└── exceptions.py     # Exception hierarchy
```

## Client API

### Synchronous

```python
from archipelag import Client

client = Client(
    api_key="ak_xxx",
    base_url="https://api.archipelag.io",
    timeout=60.0,
)

# High-level methods
result = client.chat(prompt, system_prompt=None, max_tokens=None)
for event in client.chat_stream(prompt):
    print(event.content)
result = client.generate_image(prompt, width=1024, height=1024)

# Job management
job = client.create_job(workload, input)
job = client.get_job(job_id)
job = client.wait_for_job(job_id, poll_interval=1.0, timeout=None)
for event in client.stream_job(job_id):
    print(event)
client.cancel_job(job_id)

# Batch
jobs = client.batch([...])
results = client.wait_all(jobs)

client.close()
```

### Asynchronous

```python
from archipelag import AsyncClient

async with AsyncClient(api_key="ak_xxx") as client:
    result = await client.chat("Hello")

    async for event in client.chat_stream("Tell a story"):
        print(event.content)
```

## Data Models

### Job
```python
class Job:
    id: str
    status: JobStatus  # PENDING, QUEUED, RUNNING, COMPLETED, FAILED
    workload_id: int
    input: dict
    output: str | None
    error: str | None
    usage: Usage | None
```

### StreamEvent
```python
class StreamEvent:
    type: StreamEventType  # TOKEN, STATUS, PROGRESS, IMAGE, ERROR, DONE
    content: str | None
    step: int | None
    total: int | None
    image_data: str | None
    usage: Usage | None
```

## Exception Hierarchy

```python
ArchipelagError          # Base
├── AuthenticationError  # 401
├── InsufficientCreditsError  # 402 (has required, available)
├── NotFoundError        # 404
├── ValidationError      # 422 (has errors dict)
├── RateLimitError       # 429 (has retry_after)
├── JobFailedError       # Job execution failed
├── TimeoutError         # Request/job timeout
└── ConnectionError      # Network failure
```

## Building

```bash
# Setup
mise run setup

# Install
mise run install:dev

# Test
mise run test
mise run test:cov

# Lint
mise run lint
mise run lint:fix

# Format
mise run fmt

# Type check
mise run typecheck

# CI
mise run ci

# Build
mise run build

# Publish
mise run publish
```

## Dependencies

### Core
- `httpx` - HTTP client (sync + async)
- `pydantic` - Data validation
- `httpx-sse` - Server-Sent Events

### Development
- `pytest` + `pytest-asyncio` - Testing
- `ruff` - Linting and formatting
- `mypy` - Type checking
- `hatchling` - Build system
