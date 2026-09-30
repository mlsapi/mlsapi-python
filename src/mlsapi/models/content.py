from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class InstagramContent(BaseModel):
    hook_above_fold: Optional[str] = None
    caption: str
    carousel_prompt: Optional[str] = None
    call_to_action: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    character_count: Optional[int] = None


class FacebookContent(BaseModel):
    headline: Optional[str] = None
    post_copy: str
    link_preview: Optional[Dict[str, str]] = None
    hashtags: List[str] = Field(default_factory=list)


class LinkedInContent(BaseModel):
    post_copy: str
    hashtags: List[str] = Field(default_factory=list)


class XTwitterContent(BaseModel):
    single_tweet: Optional[str] = None
    thread: List[str] = Field(default_factory=list)


class TikTokContent(BaseModel):
    caption: str
    on_screen_hook_text: Optional[str] = None
    call_to_action_cue: Optional[str] = None
    sound_recommendation: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)


class YouTubeContent(BaseModel):
    video_title_options: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    shorts: Optional[Dict[str, str]] = None


class SocialPlatformBundle(BaseModel):
    instagram: Optional[InstagramContent] = None
    facebook: Optional[FacebookContent] = None
    linkedin: Optional[LinkedInContent] = None
    x_twitter: Optional[XTwitterContent] = None
    tiktok: Optional[TikTokContent] = None
    youtube: Optional[YouTubeContent] = None


class VideoScriptScene(BaseModel):
    second_range: str
    visual: str
    voiceover: str


class VideoScriptContent(BaseModel):
    duration_seconds: int = 30
    format: str = "vertical_9_16"
    hook: str
    scenes: List[VideoScriptScene] = Field(default_factory=list)


class EmailBlastContent(BaseModel):
    subject_lines: List[str] = Field(default_factory=list)
    preview_text: Optional[str] = None
    body_html: Optional[str] = None
    body_markdown: Optional[str] = None


class GeneratedContentBundle(BaseModel):
    social: Optional[SocialPlatformBundle] = None
    email_blast: Optional[EmailBlastContent] = None
    video_script: Optional[VideoScriptContent] = None
    flyer_bullets: Optional[List[str]] = None
    mls_remarks: Optional[str] = None
    investor_pitch: Optional[Dict[str, Any]] = None


class ContentGenerationResponse(BaseModel):
    mls_id: str
    tone: str
    target_audience: Optional[str] = None
    generated_at: Optional[str] = None
    content: GeneratedContentBundle = Field(default_factory=GeneratedContentBundle)
