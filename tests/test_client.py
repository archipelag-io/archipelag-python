"""
Tests for the Archipelag Python SDK client.
"""

import pytest
from archipelag import Client, AsyncClient
from archipelag.models import Job, JobStatus, Usage, StreamEvent, StreamEventType
from archipelag.exceptions import (
    AuthenticationError,
    NotFoundError,
    RateLimitError,
)


class TestModels:
    """Test Pydantic models."""

    def test_job_is_complete(self):
        """Test Job.is_complete property."""
        job = Job(
            id="job-123",
            workload_id=1,
            status=JobStatus.COMPLETED,
            input={"prompt": "test"},
            created_at="2024-01-01T00:00:00Z",
        )
        assert job.is_complete is True
        assert job.is_success is True

        job.status = JobStatus.RUNNING
        assert job.is_complete is False

        job.status = JobStatus.FAILED
        assert job.is_complete is True
        assert job.is_success is False

    def test_usage_model(self):
        """Test Usage model."""
        usage = Usage(
            prompt_tokens=10,
            completion_tokens=20,
            total_tokens=30,
            credits_used=0.5,
        )
        assert usage.total_tokens == 30

    def test_stream_event(self):
        """Test StreamEvent model."""
        event = StreamEvent(
            type=StreamEventType.TOKEN,
            content="Hello",
        )
        assert event.type == StreamEventType.TOKEN
        assert event.content == "Hello"


class TestClient:
    """Test synchronous client."""

    def test_client_init(self):
        """Test client initialization."""
        client = Client(api_key="ak_test")
        assert client.api_key == "ak_test"
        assert client.base_url == "https://api.archipelag.io"
        client.close()

    def test_client_custom_base_url(self):
        """Test client with custom base URL."""
        client = Client(
            api_key="ak_test",
            base_url="https://custom.api.com/",
        )
        assert client.base_url == "https://custom.api.com"
        client.close()

    def test_client_context_manager(self):
        """Test client as context manager."""
        with Client(api_key="ak_test") as client:
            assert client.api_key == "ak_test"


class TestAsyncClient:
    """Test async client."""

    def test_async_client_init(self):
        """Test async client initialization."""
        client = AsyncClient(api_key="ak_test")
        assert client.api_key == "ak_test"


class TestExceptions:
    """Test exception classes."""

    def test_authentication_error(self):
        """Test AuthenticationError."""
        err = AuthenticationError("Invalid API key", status_code=401)
        assert str(err) == "[401] Invalid API key"
        assert err.status_code == 401

    def test_rate_limit_error(self):
        """Test RateLimitError with retry_after."""
        err = RateLimitError("Too many requests", retry_after=60, status_code=429)
        assert err.retry_after == 60

    def test_not_found_error(self):
        """Test NotFoundError."""
        err = NotFoundError("Job not found", status_code=404)
        assert err.status_code == 404
