"""
Archipelag SDK Models

Pydantic models for API requests and responses.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job execution status."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class RuntimeType(str, Enum):
    """Workload runtime type."""

    CONTAINER = "container"
    WASM = "wasm"


class Usage(BaseModel):
    """Token/resource usage information."""

    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    credits_used: float = 0.0


class Job(BaseModel):
    """Job information."""

    id: str
    workload_id: int
    workload_slug: Optional[str] = None
    status: JobStatus
    input: dict[str, Any]
    output: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    usage: Optional[Usage] = None

    @property
    def is_complete(self) -> bool:
        """Check if job is in a terminal state."""
        return self.status in (
            JobStatus.COMPLETED,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
            JobStatus.TIMEOUT,
        )

    @property
    def is_success(self) -> bool:
        """Check if job completed successfully."""
        return self.status == JobStatus.COMPLETED


class JobOutput(BaseModel):
    """Job output chunk for streaming."""

    job_id: str
    seq: int
    chunk: str
    is_final: bool = False


class StreamEventType(str, Enum):
    """Types of streaming events."""

    TOKEN = "token"
    STATUS = "status"
    PROGRESS = "progress"
    IMAGE = "image"
    ERROR = "error"
    DONE = "done"


class StreamEvent(BaseModel):
    """A streaming event from a job."""

    type: StreamEventType
    content: Optional[str] = None
    step: Optional[int] = None
    total: Optional[int] = None
    image_data: Optional[str] = None
    image_format: Optional[str] = None
    error: Optional[str] = None
    usage: Optional[Usage] = None


class ChatResult(BaseModel):
    """Result from a chat completion."""

    content: str
    job_id: str
    usage: Usage
    model: Optional[str] = None
    finish_reason: Optional[str] = None


class ImageResult(BaseModel):
    """Result from image generation."""

    image_data: str  # Base64 encoded
    image_format: str  # png, jpeg, etc.
    width: int
    height: int
    seed: Optional[int] = None
    job_id: str
    usage: Usage


class Workload(BaseModel):
    """Workload information."""

    id: int
    name: str
    slug: str
    description: Optional[str] = None
    runtime_type: RuntimeType
    required_vram_mb: Optional[int] = None
    required_ram_mb: Optional[int] = None
    price_per_job: float
    is_enabled: bool = True


class ApiKey(BaseModel):
    """API key information."""

    id: str
    name: str
    prefix: str  # First 8 chars of key
    created_at: datetime
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class Account(BaseModel):
    """User account information."""

    id: str
    email: str
    credits: float
    created_at: datetime


# Request models


class ChatRequest(BaseModel):
    """Request for chat completion."""

    prompt: str
    system_prompt: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    workload: str = "llm-chat"


class ImageRequest(BaseModel):
    """Request for image generation."""

    prompt: str
    negative_prompt: Optional[str] = None
    width: int = 1024
    height: int = 1024
    steps: int = 30
    guidance_scale: float = 7.5
    seed: Optional[int] = None
    scheduler: Optional[str] = None
    workload: str = "sdxl"


class JobCreateRequest(BaseModel):
    """Generic job creation request."""

    workload: str
    input: dict[str, Any]


# =========================================================================
# Batch models
# =========================================================================


class BatchChild(BaseModel):
    """A child job in a batch."""

    id: str
    batch_index: int
    state: str
    error: Optional[str] = None
    host_id: Optional[str] = None


class BatchConfig(BaseModel):
    """Batch configuration and progress."""

    chunk_count: int
    merge_strategy: str = "concat"
    fail_mode: str = "best_effort"
    completed: int = 0
    failed: int = 0


class BatchJob(BaseModel):
    """A batch job (parent) with its children."""

    id: str
    state: str
    workload: str
    batch: BatchConfig
    children: list[BatchChild] = []
    created_at: datetime

    @property
    def is_complete(self) -> bool:
        return self.state in ("succeeded", "failed", "cancelled")

    @property
    def progress(self) -> float:
        if self.batch.chunk_count == 0:
            return 0.0
        return (self.batch.completed + self.batch.failed) / self.batch.chunk_count


class BatchProgress(BaseModel):
    """Detailed batch progress."""

    parent_id: str
    parent_state: str
    chunk_count: int
    merge_strategy: str
    fail_mode: str
    child_states: dict[str, int] = {}
    children: list[BatchChild] = []
