# Archipelag Python SDK

Official Python SDK for the [Archipelag.io](https://archipelag.io) distributed compute platform.

## Installation

```bash
pip install archipelag
```

## Quick Start

```python
from archipelag import Client

# Initialize the client
client = Client(api_key="ak_xxx")

# Chat completion
result = client.chat("Hello, how are you?")
print(result.content)

# Streaming chat
for event in client.chat_stream("Tell me a story"):
    if event.type == "token":
        print(event.content, end="", flush=True)

# Image generation
image = client.generate_image(
    prompt="a sunset over mountains",
    width=1024,
    height=1024
)
# image.image_data contains base64-encoded PNG
```

## Async Usage

```python
import asyncio
from archipelag import AsyncClient

async def main():
    async with AsyncClient(api_key="ak_xxx") as client:
        # Async chat
        result = await client.chat("Hello!")
        print(result.content)

        # Async streaming
        async for event in client.chat_stream("Tell me a story"):
            if event.type == "token":
                print(event.content, end="", flush=True)

asyncio.run(main())
```

## Features

- **Synchronous and Async clients**
- **Streaming support** via Server-Sent Events
- **Type hints** with Pydantic models
- **Automatic retries** and error handling
- **Workload helpers** for chat, image generation, and more

## API Reference

### Client

```python
client = Client(
    api_key="ak_xxx",           # Your API key
    base_url="https://...",     # Optional: custom API URL
    timeout=60.0,               # Optional: request timeout
)
```

### Chat

```python
# Simple chat
result = client.chat("Hello!")
print(result.content)
print(result.usage.total_tokens)

# With options
result = client.chat(
    prompt="Explain quantum computing",
    system_prompt="You are a physics professor",
    max_tokens=500,
    temperature=0.7,
)

# Streaming
for event in client.chat_stream("Tell me a joke"):
    if event.type == "token":
        print(event.content, end="")
    elif event.type == "done":
        print(f"\n[{event.usage.total_tokens} tokens]")
```

### Image Generation

```python
result = client.generate_image(
    prompt="a cat astronaut on mars",
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024,
    steps=30,
    guidance_scale=7.5,
    seed=42,  # For reproducibility
)

# Save image
import base64
with open("output.png", "wb") as f:
    f.write(base64.b64decode(result.image_data))
```

### Batch Processing

```python
# Create multiple jobs
jobs = client.batch([
    {"workload": "sdxl", "input": {"prompt": "a cat"}},
    {"workload": "sdxl", "input": {"prompt": "a dog"}},
    {"workload": "sdxl", "input": {"prompt": "a bird"}},
])

# Wait for all to complete
results = client.wait_all(jobs)
for job in results:
    print(f"Job {job.id}: {job.status}")
```

### Low-Level Job API

```python
# Create job manually
job = client.create_job(
    workload="llm-chat",
    input={"prompt": "Hello!"}
)

# Check status
job = client.get_job(job.id)
print(job.status)

# Wait for completion
job = client.wait_for_job(job.id, timeout=120)

# Stream output
for event in client.stream_job(job.id):
    print(event)

# Cancel job
client.cancel_job(job.id)

# List recent jobs
jobs = client.list_jobs(limit=10)
```

### Workloads

```python
# List available workloads
workloads = client.list_workloads()
for w in workloads:
    print(f"{w.slug}: {w.name} (${w.price_per_job} credits)")

# Get workload details
workload = client.get_workload("sdxl")
print(f"Requires {workload.required_vram_mb}MB VRAM")
```

### Account

```python
account = client.get_account()
print(f"Credits: {account.credits}")
```

## Error Handling

```python
from archipelag import (
    ArchipelagError,
    AuthenticationError,
    RateLimitError,
    InsufficientCreditsError,
    JobFailedError,
)

try:
    result = client.chat("Hello!")
except AuthenticationError:
    print("Invalid API key")
except InsufficientCreditsError as e:
    print(f"Not enough credits. Need {e.required}, have {e.available}")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except JobFailedError as e:
    print(f"Job {e.job_id} failed: {e.message}")
except ArchipelagError as e:
    print(f"API error: {e}")
```

## License

MIT
