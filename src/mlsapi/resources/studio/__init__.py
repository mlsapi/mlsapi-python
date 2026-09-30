from __future__ import annotations

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient
from mlsapi.resources.studio.creatives import AsyncCreativesResource, CreativesResource
from mlsapi.resources.studio.custom import AsyncCustomResource, CustomResource
from mlsapi.resources.studio.enhance import AsyncEnhanceResource, EnhanceResource
from mlsapi.resources.studio.floorplan import AsyncFloorPlanResource, FloorPlanResource
from mlsapi.resources.studio.jobs import AsyncStudioJobsResource, StudioJobsResource
from mlsapi.resources.studio.render import AsyncRenderResource, RenderResource
from mlsapi.resources.studio.social import AsyncSocialResource, SocialResource
from mlsapi.resources.studio.staging import AsyncStagingResource, StagingResource
from mlsapi.resources.studio.upload import AsyncUploadResource, UploadResource
from mlsapi.resources.studio.video import AsyncVideoResource, VideoResource


class StudioResource:
    """Aggregated Studio Visual AI namespace."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self.jobs = StudioJobsResource(http)
        self.staging = StagingResource(http, self.jobs)
        self.enhance = EnhanceResource(http, self.jobs)
        self.floorplan = FloorPlanResource(http, self.jobs)
        self.render = RenderResource(http, self.jobs)
        self.creatives = CreativesResource(http, self.jobs)
        self.social = SocialResource(http)
        self.video = VideoResource(http, self.jobs)
        self.custom = CustomResource(http, self.jobs)
        self._upload = UploadResource(http)

    def upload(self, *args, **kwargs):
        """Upload image or video file directly to mlsapi CDN."""
        return self._upload.upload(*args, **kwargs)


class AsyncStudioResource:
    """Aggregated Asynchronous Studio Visual AI namespace."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http
        self.jobs = AsyncStudioJobsResource(http)
        self.staging = AsyncStagingResource(http, self.jobs)
        self.enhance = AsyncEnhanceResource(http, self.jobs)
        self.floorplan = AsyncFloorPlanResource(http, self.jobs)
        self.render = AsyncRenderResource(http, self.jobs)
        self.creatives = AsyncCreativesResource(http, self.jobs)
        self.social = AsyncSocialResource(http)
        self.video = AsyncVideoResource(http, self.jobs)
        self.custom = AsyncCustomResource(http, self.jobs)
        self._upload = AsyncUploadResource(http)

    async def upload(self, *args, **kwargs):
        """Upload image or video file directly to mlsapi CDN."""
        return await self._upload.upload(*args, **kwargs)
