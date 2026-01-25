"""
Archipelag.io Python SDK

Official Python client for the Archipelag.io distributed compute platform.

Example usage:
    from archipelag import Client

    client = Client(api_key="ak_xxx")

    # Synchronous
    result = client.chat("Hello, how are you?")
    print(result.content)

    # Streaming
    for event in client.chat_stream("Tell me a story"):
        if event.type == "token":
            print(event.content, end="", flush=True)
"""

from archipelag.client import Client, AsyncClient
from archipelag.models import (
    Job,
    JobStatus,
    JobOutput,
    ChatResult,
    ImageResult,
    StreamEvent,
    Usage,
    Workload,
    ApiKey,
)
from archipelag.exceptions import (
    ArchipelagError,
    AuthenticationError,
    RateLimitError,
    InsufficientCreditsError,
    JobFailedError,
    NotFoundError,
    ValidationError,
)

__version__ = "0.1.0"
__all__ = [
    # Clients
    "Client",
    "AsyncClient",
    # Models
    "Job",
    "JobStatus",
    "JobOutput",
    "ChatResult",
    "ImageResult",
    "StreamEvent",
    "Usage",
    "Workload",
    "ApiKey",
    # Exceptions
    "ArchipelagError",
    "AuthenticationError",
    "RateLimitError",
    "InsufficientCreditsError",
    "JobFailedError",
    "NotFoundError",
    "ValidationError",
]
