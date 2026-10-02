# Changelog

## 0.1.1

Studio/content methods now send exactly the JSON fields the API reads. Every keyword
argument has the same name as its JSON key (and the JS SDK request type), and arguments
left as `None` are no longer sent, so the server applies its own defaults.

### Fixed
- `staging.stage` now posts to `/v1/studio/staging/stage` (was `/furnish`).
- `staging.restyle` sends `style` (was `target_style`, which the server ignored). Adds `retain_layout` and `custom_restyle_instructions`.
- `staging.replace_furniture` adds `target_location_notes` and `preserve_surroundings`. `staging.replace_material` adds `custom_finish_notes`.
- `staging.wall_colors` adds `custom_colors` and no longer always sends `palette_preset`. `staging.twilight` no longer sends `interior_lighting`.
- `custom.generate` sends `reference_image_urls` and adds `photo_url` and `aspect_ratio`.
- `render.architectural` sends `custom_instructions` and adds `render_type`, `lighting_environment`, `weather` and `season`.
- `video.walkthrough` now takes the Studio spec fields `photo_url`, `motion`, `duration_seconds` and `custom_motion_prompt`, plus `aspect_ratio`, `mls_id`, `photo_urls`, `voice_id` and `music_mood`.
- `video.transition` adds `transition_style` and `aspect_ratio`. `duration_seconds` now defaults to unset (the server uses 5); the old default of 3.0 was not a valid value.
- `video.tour` takes `ordered_photos` as `{"room_name", "photo_url", "highlight"?}` dicts and adds `duration_seconds`, `auto_script`, `shot_script`, `aspect_ratio` and `music_genre`.
- `creatives.generate`: `mls_id` is now optional, and the method adds `photo_url`, `photos`, `property_details`, `ad_type`, `custom_badge`, `custom_headline`, `highlights`, `open_house`, `include_carousel`, `agent_headshot_url` and `realtor_photo`. It raises `ValueError` if you pass none of `mls_id`, `photo_url` or `photos`.
- `social.publish` sends `destinations` as `{"platform", "target_type", ...}` dicts and adds `asset_type` and `webhook_url`.
- `staging.stage` adds the spec field `aspect_ratio`. `video.enhance` adds `mls_id`.
- Defaults that were always sent are now left unset: `stage` room_type, style and preserve_flooring; `restyle` style (was `"scandinavian"`, so the server default `"japandi"` now applies); `upscale` scale_factor and enhance_details; `floorplan` style and the boolean flags; `creatives` trigger, direction and placements (the server default is `["square"]`, not four placements); `video.enhance` features; `content.generate` outputs and tone.
- Result models now parse real server output and no longer raise `ValidationError`:
  - `RestyleResult` accepts the server's `retyped_photo_url` and exposes it as `restyled_photo_url`.
  - `ReplaceFurnitureResult` and `ReplaceMaterialResult` use `updated_room_photo_url`.
  - `HouseTourResult` uses `video_url`.
  - `CustomStudioResult` uses `image_url` and `prompt_applied`.
  - `SocialPublishResult.results` is a list.
  
  Every model also gains the other fields the server returns. Unknown fields are kept rather than dropped.
- `StudioJob` gains `type` (also read from `job_type`) and `estimated_completion_seconds`.
- The test environment's base URL was `https://api.mlsapi.dev`, which does not resolve. Both environments now use `https://mlsapi.dev`. The environment is sent as the `x-key-env` header, as in the JS SDK.
- `content.generate` URL-encodes `mls_id`.

### Added
- `TypedDict` request shapes: `WallColorSwatch`, `HouseTourRoomItem`, `SocialPublishDestination`, `CreativeBrandKit`, `CreativesPropertyDetails`, `OpenHouse`, `VideoEnhanceFeatures`, `SubtitleStyle` and `ContentPropertyDetails`.
- `pymlsapi.__version__` and the `User-Agent` header now come from one constant.

### Deprecated (still accepted; each emits `DeprecationWarning`)
- `staging.restyle(target_style=...)` → `style`
- `staging.twilight(interior_lighting=...)` is ignored
- `custom.generate(image_urls=...)` → `reference_image_urls`; `negative_prompt` is ignored
- `render.architectural(prompt=...)` → `custom_instructions`
- `video.walkthrough(photos=...)`, or a list passed as the first argument → `photo_urls`
- `video.tour(ordered_photos=["url", ...])` is converted to `{"room_name": "Room N", "photo_url": url}`. `music_mood` is ignored; use `music_genre`.
- `social.publish(destinations=["instagram", ...])` is converted to `{"platform", "target_type"}` dicts with a default target type for each platform. The top-level `caption` is copied into each destination that has no caption of its own.
- 0.1.0 result attribute names are still readable: `result_photo_url`, `target_furniture`, `surface_type`, `target_style`, `video_tour_url`, `output_url`, `prompt_used` and `transition_type`.

### Breaking (positional arguments only)
- New and deprecated parameters are keyword-only. A few rarely used optional parameters from 0.1.0 can no longer be passed by position:
  - `twilight`: `webhook_url`
  - `custom.generate`: `negative_prompt` and `webhook_url`
  - `social.publish`: `caption` and `schedule_time`
  - `video.tour`: `music_mood` and `webhook_url`
  
  Pass them by keyword.

## 0.1.0

- Initial release.
