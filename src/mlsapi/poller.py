from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Optional, TypeVar

from mlsapi.errors import JobTimeoutError, StudioJobFailedError

T = TypeVar("T")


def poll_job_sync(
    fetch_fn: Callable[[], Any],
    is_done_fn: Callable[[Any], bool],
    is_failed_fn: Callable[[Any], bool],
    timeout_seconds: float = 90.0,
    initial_interval: float = 1.5,
    max_interval: float = 5.0,
    backoff_multiplier: float = 1.25,
    on_progress: Optional[Callable[[Any], None]] = None,
) -> Any:
    """Poll a job synchronously until it is finished, fails, or times out."""
    start_time = time.monotonic()
    current_interval = initial_interval

    while True:
        job = fetch_fn()

        if on_progress:
            try:
                on_progress(job)
            except Exception:
                pass

        if is_done_fn(job):
            return job

        if is_failed_fn(job):
            job_id = getattr(job, "job_id", getattr(job, "id", "unknown"))
            error_msg = getattr(job, "error", "Job processing failed on worker")
            raise StudioJobFailedError(
                job_id=str(job_id), message=str(error_msg), error_details=job
            )

        elapsed = time.monotonic() - start_time
        if elapsed >= timeout_seconds:
            job_id = getattr(job, "job_id", getattr(job, "id", "unknown"))
            raise JobTimeoutError(job_id=str(job_id), timeout_seconds=timeout_seconds)

        sleep_time = min(current_interval, timeout_seconds - elapsed)
        if sleep_time > 0:
            time.sleep(sleep_time)

        current_interval = min(current_interval * backoff_multiplier, max_interval)


async def poll_job_async(
    fetch_fn: Callable[[], Any],  # async function
    is_done_fn: Callable[[Any], bool],
    is_failed_fn: Callable[[Any], bool],
    timeout_seconds: float = 90.0,
    initial_interval: float = 1.5,
    max_interval: float = 5.0,
    backoff_multiplier: float = 1.25,
    on_progress: Optional[Callable[[Any], None]] = None,
) -> Any:
    """Poll a job asynchronously until it is finished, fails, or times out."""
    start_time = time.monotonic()
    current_interval = initial_interval

    while True:
        job = await fetch_fn()

        if on_progress:
            try:
                if asyncio.iscoroutinefunction(on_progress):
                    await on_progress(job)
                else:
                    on_progress(job)
            except Exception:
                pass

        if is_done_fn(job):
            return job

        if is_failed_fn(job):
            job_id = getattr(job, "job_id", getattr(job, "id", "unknown"))
            error_msg = getattr(job, "error", "Job processing failed on worker")
            raise StudioJobFailedError(
                job_id=str(job_id), message=str(error_msg), error_details=job
            )

        elapsed = time.monotonic() - start_time
        if elapsed >= timeout_seconds:
            job_id = getattr(job, "job_id", getattr(job, "id", "unknown"))
            raise JobTimeoutError(job_id=str(job_id), timeout_seconds=timeout_seconds)

        sleep_time = min(current_interval, timeout_seconds - elapsed)
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)

        current_interval = min(current_interval * backoff_multiplier, max_interval)
