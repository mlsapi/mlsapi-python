from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Union

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.models.studio import UploadResult


class UploadResource:
    """Synchronous file upload utility to mlsapi global CDN."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def upload(
        self,
        file: Union[str, Path, bytes, BinaryIO],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> UploadResult:
        """Upload an image or video file to mlsapi CDN."""
        if isinstance(file, (str, Path)):
            path = Path(file)
            filename = filename or path.name
            with open(path, "rb") as f:
                file_bytes = f.read()
        elif isinstance(file, bytes):
            file_bytes = file
            filename = filename or "upload.jpg"
        elif hasattr(file, "read"):
            file_bytes = file.read()
            filename = filename or getattr(file, "name", "upload.jpg")
        else:
            raise ValueError(
                "Unsupported file type. Pass a Path, filepath string, bytes, or file object."
            )

        content_type = content_type or "image/jpeg"
        files = {"file": (filename, file_bytes, content_type)}

        data = self._http.post("/v1/studio/upload", files=files)
        # Server may return { url: "..." } or { data: { url: "..." } }
        url = data.get("url") or (data.get("data", {}).get("url", ""))
        return UploadResult(
            url=url,
            filename=filename,
            content_type=content_type,
            bytes=len(file_bytes),
            storage_key=data.get("storageKey") or (data.get("data", {}).get("storageKey")),
        )


class AsyncUploadResource:
    """Asynchronous file upload utility to mlsapi global CDN."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def upload(
        self,
        file: Union[str, Path, bytes, BinaryIO],
        filename: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> UploadResult:
        """Upload an image or video file to mlsapi CDN."""
        if isinstance(file, (str, Path)):
            path = Path(file)
            filename = filename or path.name
            with open(path, "rb") as f:
                file_bytes = f.read()
        elif isinstance(file, bytes):
            file_bytes = file
            filename = filename or "upload.jpg"
        elif hasattr(file, "read"):
            file_bytes = file.read()
            filename = filename or getattr(file, "name", "upload.jpg")
        else:
            raise ValueError(
                "Unsupported file type. Pass a Path, filepath string, bytes, or file object."
            )

        content_type = content_type or "image/jpeg"
        files = {"file": (filename, file_bytes, content_type)}

        data = await self._http.post("/v1/studio/upload", files=files)
        url = data.get("url") or (data.get("data", {}).get("url", ""))
        return UploadResult(
            url=url,
            filename=filename,
            content_type=content_type,
            bytes=len(file_bytes),
            storage_key=data.get("storageKey") or (data.get("data", {}).get("storageKey")),
        )
