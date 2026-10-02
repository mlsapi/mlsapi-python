import pytest

from pymlsapi.errors import JobTimeoutError, StudioJobFailedError
from pymlsapi.models import StudioJob
from pymlsapi.poller import poll_job_async, poll_job_sync


def test_poll_job_sync_success():
    call_count = 0

    def fetch():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            return StudioJob(
                job_id="test_1", status="processing", progress_percentage=call_count * 30
            )
        return StudioJob(job_id="test_1", status="completed", progress_percentage=100)

    progress_log = []
    job = poll_job_sync(
        fetch_fn=fetch,
        is_done_fn=lambda j: j.status == "completed",
        is_failed_fn=lambda j: j.status == "failed",
        timeout_seconds=5.0,
        initial_interval=0.01,
        on_progress=lambda j: progress_log.append(j.progress_percentage),
    )
    assert job.status == "completed"
    assert call_count == 3
    assert progress_log == [30, 60, 100]


def test_poll_job_sync_failed():
    def fetch():
        return StudioJob(job_id="test_err", status="failed", error="GPU out of memory")

    with pytest.raises(StudioJobFailedError, match="GPU out of memory"):
        poll_job_sync(
            fetch_fn=fetch,
            is_done_fn=lambda j: j.status == "completed",
            is_failed_fn=lambda j: j.status == "failed",
            timeout_seconds=5.0,
            initial_interval=0.01,
        )


def test_poll_job_sync_timeout():
    def fetch():
        return StudioJob(job_id="test_timeout", status="processing")

    with pytest.raises(JobTimeoutError):
        poll_job_sync(
            fetch_fn=fetch,
            is_done_fn=lambda j: j.status == "completed",
            is_failed_fn=lambda j: j.status == "failed",
            timeout_seconds=0.05,
            initial_interval=0.02,
        )


@pytest.mark.asyncio
async def test_poll_job_async_success():
    call_count = 0

    async def fetch():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            return StudioJob(job_id="async_1", status="processing", progress_percentage=50)
        return StudioJob(job_id="async_1", status="completed", progress_percentage=100)

    job = await poll_job_async(
        fetch_fn=fetch,
        is_done_fn=lambda j: j.status == "completed",
        is_failed_fn=lambda j: j.status == "failed",
        timeout_seconds=5.0,
        initial_interval=0.01,
    )
    assert job.status == "completed"
    assert call_count == 2
