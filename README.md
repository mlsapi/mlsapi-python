# mlsapi

The official Python client library for **[mlsapi.dev](https://mlsapi.dev)**.

Access real-time MLS listing data, property intelligence, CapEx lifecycle analysis, AI-generated marketing copy, and the complete suite of **Studio Visual AI** generative tools (virtual staging, twilight conversion, decluttering, 3D dollhouse floor plans, 4K upscaling, ad creatives, and video generation).

[![PyPI version](https://img.shields.io/pypi/v/pymlsapi.svg?style=flat-square)](https://pypi.org/project/pymlsapi/)
[![Python versions](https://img.shields.io/pypi/pyversions/mlsapi.svg?style=flat-square)](https://pypi.org/project/pymlsapi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Synchronous Example](#synchronous-example)
  - [Asynchronous (asyncio) Example](#asynchronous-asyncio-example)
- [Configuration & Authentication](#configuration--authentication)
- [Core Features & Code Examples](#core-features--code-examples)
  - [1. Real-Time MLS Listing Lookup & Ingestion](#1-real-time-mls-listing-lookup--ingestion)
  - [2. Property Intelligence & CapEx Analysis](#2-property-intelligence--capex-analysis)
  - [3. Marketing Content Generation](#3-marketing-content-generation)
  - [4. Media Upload to Global CDN](#4-media-upload-to-global-cdn)
  - [5. Virtual Room Staging (29 Architectural Styles)](#5-virtual-room-staging-29-architectural-styles)
  - [6. Day-to-Dusk Twilight & Exterior Enhancement](#6-day-to-dusk-twilight--exterior-enhancement)
  - [7. Declutter & Clean Space](#7-declutter--clean-space)
  - [8. De-Staging (Empty Room) & Floor Restoration](#8-de-staging-empty-room--floor-restoration)
  - [9. Furniture & Surface Material Replacement](#9-furniture--surface-material-replacement)
  - [10. 3x3 Designer Wall Paint Swatches](#10-3x3-designer-wall-paint-swatches)
  - [11. 2D Blueprint to 3D Isometric Dollhouse](#11-2d-blueprint-to-3d-isometric-dollhouse)
  - [12. 4K Super-Resolution Upscaling](#12-4k-super-resolution-upscaling)
  - [13. Branded Multi-Placement Ad Creatives](#13-branded-multi-placement-ad-creatives)
  - [14. AI Video Walkthroughs & Voice/Subtitle Polish](#14-ai-video-walkthroughs--voicesubtitle-polish)
  - [15. Restyle a Furnished Room](#15-restyle-a-furnished-room)
  - [16. Architectural Rendering (CAD / Sketch to Photoreal)](#16-architectural-rendering-cad--sketch-to-photoreal)
  - [17. Photo-to-Video: Walkthrough, Transition & House Tour](#17-photo-to-video-walkthrough-transition--house-tour)
  - [18. Custom Generative Prompt](#18-custom-generative-prompt)
  - [19. Social Publishing](#19-social-publishing)
- [Asynchronous Jobs & Progress Callbacks](#asynchronous-jobs--progress-callbacks)
- [Error Handling](#error-handling)
- [Supported Presets Reference](#supported-presets-reference)
- [License](#license)

---

## Features

- **Dual Sync & Async Interfaces:** Native synchronous `MlsApiClient` and async `AsyncMlsApiClient` for high-throughput `asyncio` applications.
- **Deep Type Safety:** Pydantic v2 domain models with full IDE autocompletion, type hinting, and runtime validation.
- **Smart Asynchronous Polling:** Auto-waiting helper methods (`*_and_wait(...)`) with exponential backoff, jitter, and real-time progress callbacks.
- **Resilient Networking:** Built on `httpx` with automatic connection pooling and smart retries on HTTP 429 rate limits and 5xx server errors.
- **Complete Studio Coverage:** First-class access to all 21+ Studio generative visual endpoints.

---

## Installation

Install via pip, uv, or poetry:

```bash
# pip
pip install pymlsapi

# uv
uv add pymlsapi

# poetry
poetry add pymlsapi
```

Requires **Python 3.9+**.

---

## Quick Start

### Synchronous Example

```python
import os
from pymlsapi import MlsApiClient

# Initialize the client with your API key
mls = MlsApiClient(api_key=os.environ.get("MLSAPI_KEY"))

# 1. Fetch normalized MLS listing data
listing = mls.listings.get_and_wait("A12079565")
print(f"Property: {listing.address.formatted} - ${listing.price:,.2f}")
print(f"Downloaded {listing.photo_count} photos: {listing.photos[0]}")

# 2. Perform AI Virtual Staging on an empty room photo
staged = mls.studio.staging.stage_and_wait(
    photo_url=listing.photos[0],
    room_type="living_room",
    style="scandinavian",
    custom_staging_instructions="Oak dining table, bouclé accent chairs, fiddle-leaf fig tree",
)

print(f"Staged photo ready: {staged.staged_photo_url}")
print(f"Before/after comparison: {staged.before_after_comparison_url}")
```

### Asynchronous (asyncio) Example

```python
import asyncio
import os
from pymlsapi import AsyncMlsApiClient

async def main():
    async with AsyncMlsApiClient(api_key=os.environ.get("MLSAPI_KEY")) as mls:
        # Ingest listing and synthesize intelligence concurrently
        listing_task = mls.listings.get_and_wait("A12079565")
        intel_task = mls.intelligence.get("A12079565", investor_mode=True)

        listing, intel = await asyncio.gather(listing_task, intel_task)

        print(f"Listing: {listing.address.city}, {listing.address.state}")
        print(f"Gross Yield: {intel.llm_derived_intelligence.investor_insights.estimated_gross_yield_pct}%")

asyncio.run(main())
```

---

## Configuration & Authentication

Obtain your API key from the **[mlsapi.dev Dashboard](https://mlsapi.dev)**.

```python
from pymlsapi import MlsApiClient

mls = MlsApiClient(
    api_key="sk_live_...",              # Secret API key (or MLSAPI_KEY env var)
    environment="live",                # "live" (production) or "test" (sandbox)
    base_url="https://mlsapi.dev",      # Optional; both environments use https://mlsapi.dev
    timeout_seconds=60.0,              # HTTP request timeout (default: 60s)
    max_retries=3,                     # Automatic retries on rate limits (429) & 5xx errors
)
```

The `environment` is sent on every request as the `x-key-env` header, the same way the JS SDK does it.

> **Parameter names = JSON keys.** Every Studio and content method takes keyword arguments
> named exactly like the JSON body fields the API reads (identical to the JS SDK request
> types). Arguments you leave as `None` are not sent, so the server applies its own defaults.

---

## Core Features & Code Examples

### 1. Real-Time MLS Listing Lookup & Ingestion

Ingest property records by MLS number. If the property is not cached, the engine enqueues live scraping and photo downloading.

```python
# Auto-wait until scraping completes (recommended)
listing = mls.listings.get_and_wait(
    "A12079565",
    timeout_seconds=45.0,
    on_progress=lambda job: print(f"Ingestion step: {job.step}"),
)

print(listing.address.city, listing.specifications.beds, listing.specifications.baths_full)
print(f"Downloaded {listing.photo_count} high-res photos: {listing.photos}")

# Or handle the asynchronous job tracker manually
response = mls.listings.get("A12079565")
if hasattr(response, "status") and response.status == "processing":
    print(f"Ingestion job queued with tracker ID: {response.job_id}")
```

---

### 2. Property Intelligence & CapEx Analysis

Synthesize public tax records, historical ownership, school zoning, replacement horizons for major structural systems (roof, HVAC, water heater, impact windows), and investor yields.

```python
intel = mls.intelligence.get(
    "A12079565",
    include_llm=True,     # Deep AI analysis of remarks and conditions
    investor_mode=True,   # Include estimated rent, gross yield, and HOA flags
)

insights = intel.llm_derived_intelligence.investor_insights
capex = intel.llm_derived_intelligence.systems_and_capex

print(f"Estimated Monthly Rent: ${insights.estimated_monthly_rent.median:,.2f}")
print(f"Gross Yield: {insights.estimated_gross_yield_pct}%")
print(f"Roof Age & Condition: {capex.roof.age_years} years - {capex.roof.condition}")
print(f"Impact windows detected: {capex.storm_protection.has_impact_windows}")
```

---

### 3. Marketing Content Generation

Generate multi-channel marketing campaigns tailored by tone, target audience, and channel format.

```python
copy = mls.content.generate(
    "A12079565",
    outputs=["social", "email_blast", "video_script", "flyer_bullets", "mls_remarks"],
    social_platforms=["instagram", "linkedin", "facebook", "tiktok"],
    tone="luxury",
    target_audience="High-net-worth buyers relocating to South Florida",
)

# Access typed content
print("Instagram Caption:\n", copy.content.social.instagram.caption)
print("Instagram Hashtags:\n", copy.content.social.instagram.hashtags)
print("Video Script Hook:\n", copy.content.video_script.hook)
print("Optimized MLS Remarks:\n", copy.content.mls_remarks)
```

---

### 4. Media Upload to Global CDN

Upload local image files, binary bytes, or open file objects directly to the `mlsapi.dev` CDN to use as inputs for any Studio operation.

```python
from pathlib import Path

# 1. Upload from a local filesystem path
upload1 = mls.studio.upload(Path("./photos/vacant_living_room.jpg"))
print("CDN URL:", upload1.url)

# 2. Upload from raw bytes
with open("./photos/blueprint.png", "rb") as f:
    upload2 = mls.studio.upload(
        f.read(),
        filename="blueprint.png",
        content_type="image/png",
    )
print("Uploaded blueprint:", upload2.url)
```

---

### 5. Virtual Room Staging (29 Architectural Styles)

Furnish vacant room photos with photorealistic staging adhering to real estate staging standards.

```python
staged = mls.studio.staging.stage_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/vacant_living_room.jpg",
    room_type="living_room",
    style="luxury",             # Choose from 29 styles (e.g. 'modern', 'japandi', 'coastal')
    preserve_flooring=True,     # Keep original hardwood/tile flooring
    custom_staging_instructions="White boucle sectional, travertine coffee table, minimalist wall art",
)

print("Staged image:", staged.staged_photo_url)
print("Before/after slider:", staged.before_after_comparison_url)
print("Staging manifest:", staged.staging_manifest)
```

---

### 6. Day-to-Dusk Twilight & Exterior Enhancement

Transform daytime exterior photos into dramatic golden-hour twilight scenes with warm interior illumination, or enhance sunny curb appeal.

```python
# 1. Twilight Day-to-Dusk conversion
twilight = mls.studio.staging.twilight_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/exterior_day.jpg",
    mode="day_to_dusk",        # Or 'blue_sky_replace'
)
print("Twilight exterior:", twilight.enhanced_photo_url)

# 2. Exterior enhancements (blue sky, green lawn, pool cleaning)
enhanced = mls.studio.enhance.exterior_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/exterior_overcast.jpg",
    enhancements=["blue_sky", "green_grass", "clean_pool", "tidy_garden"],
)
print("Enhanced curb appeal:", enhanced.enhanced_photo_url)
```

---

### 7. Declutter & Clean Space

Remove tenant clutter, wires, boxes, children's toys, and moving messes while strictly keeping walls, floors, and primary structural architecture intact.

```python
clean = mls.studio.staging.declutter_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/cluttered_kitchen.jpg",
    room_type="kitchen",
    removal_targets=["dishes", "refrigerator magnets", "trash cans", "countertop appliances"],
)

print("Clean photo:", clean.decluttered_photo_url)
print("Items removed:", clean.items_removed)
```

---

### 8. De-Staging (Empty Room) & Floor Restoration

Strip out outdated furniture to present prospective buyers with a clean architectural canvas, with optional floor restoration.

```python
emptied = mls.studio.staging.empty_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/dated_bedroom.jpg",
    room_type="bedroom",
    restore_flooring="hardwood",  # 'hardwood' | 'tile' | 'carpet' | 'polished_concrete'
)

print("Empty room canvas:", emptied.empty_photo_url)
```

---

### 9. Furniture & Surface Material Replacement

Replace outdated furniture items with modern pieces or resurface materials like kitchen countertops and flooring.

```python
# 1. Precision furniture swap
new_sofa = mls.studio.staging.replace_furniture_and_wait(
    room_photo_url="https://cdn.mlsapi.dev/uploads/living.jpg",
    target_furniture="sofa",
    product_description="Low-profile minimalist Italian cream leather sofa",
    # Or pass an exact product catalog photo:
    # reference_product_image_url="https://example.com/catalog-sofa.jpg",
    target_location_notes="Replace the gray 3-seat sofa under the window",
    preserve_surroundings=True,
)
print("Updated sofa photo:", new_sofa.updated_room_photo_url)

# 2. Surface material replacement
new_kitchen = mls.studio.staging.replace_material_and_wait(
    room_photo_url="https://cdn.mlsapi.dev/uploads/kitchen.jpg",
    surface_type="countertops",
    material_preset="Calacatta Gold Italian Marble with subtle grey and gold veining",
    custom_finish_notes="Honed finish, soft reflections",
)
print("Updated kitchen countertops:", new_kitchen.updated_room_photo_url)
```

---

### 10. 3x3 Designer Wall Paint Swatches

Test curated designer paint colors on room walls with an instant 3x3 comparison grid.

```python
swatches = mls.studio.staging.wall_colors_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/living_room.jpg",
    palette_preset="popular_neutrals",  # 'popular_neutrals' | 'modern_earth' | 'coastal_breeze' | 'moody_darks'
    # Or test your own colors:
    # custom_colors=[{"name": "Hale Navy", "hex": "#303A45"}, {"name": "Sage Green", "hex": "#9BA896"}],
)

print("3x3 comparison grid:", swatches.comparison_grid_3x3_url)
for swatch in swatches.swatch_results:
    print(f"Color: {swatch.color_name} ({swatch.hex}) -> {swatch.image_url}")
```

---

### 11. 2D Blueprint to 3D Isometric Dollhouse

Convert 2D floor plans, architectural blueprints, or hand sketches into 3D isometric cutaway dollhouse renders.

```python
# Step 1: Analyze floor plan structural geometry
analysis = mls.studio.floorplan.analyze(
    floorplan_image_url="https://cdn.mlsapi.dev/uploads/floorplan.png",
    style="modern",
)
print(f"Rooms detected: {analysis.spatial_summary.total_rooms_detected}")

# Step 2: Render 3D isometric dollhouse view
dollhouse = mls.studio.floorplan.render_3d_and_wait(
    floorplan_image_url="https://cdn.mlsapi.dev/uploads/floorplan.png",
    style="modern",
    include_room_closeups=True,
)

print("3D Dollhouse Render:", dollhouse.isometric_3d_dollhouse_url)
for closeup in dollhouse.room_renders:
    print(f"Room {closeup.room_name}: {closeup.image_url}")
```

---

### 12. 4K Super-Resolution Upscaling

Upscale low-resolution or compressed MLS photos up to 4K resolution with AI detail reconstruction.

```python
upscaled = mls.studio.enhance.upscale_and_wait(
    image_url="https://cdn.mlsapi.dev/uploads/lowres_photo.jpg",
    scale_factor=4,           # 2 or 4
    enhance_details=True,
)

print("4K Upscaled image:", upscaled.upscaled_image_url)
print("Target resolution:", upscaled.target_resolution)
```

---

### 13. Branded Multi-Placement Ad Creatives

Generate compliant real estate ad creatives with agent branding kits, MLS property badges, and typography across all social and print dimensions.

```python
ads = mls.studio.creatives.generate_and_wait(
    mls_id="A12079565",      # Or pass photo_url=/photos= plus property_details={...} for any property
    trigger="just_listed",   # 'just_listed' | 'open_house' | 'price_improved' | 'just_sold'
    direction="magazine",    # 'magazine' | 'bold' | 'warm'
    placements=["feed_portrait", "square", "link", "flyer"],
    brand_kit={
        "agent_name": "Sarah Connor",
        "brokerage_name": "Compass Beverly Hills",
        "phone": "(310) 555-0199",
        "primary_brand_color": "#0F172A",
        "agent_headshot_url": "https://cdn.example.com/sarah-headshot.jpg",
    },
)

print("1:1 Square Feed Ad:", ads.creatives.get("square").image_url)
print("4:5 Portrait Feed Ad:", ads.creatives.get("feed_portrait").image_url)
print("Fair Housing compliance passed:", ads.compliance.fair_housing_passed)
```

---

### 14. AI Video Walkthroughs & Voice/Subtitle Polish

Polish realtor walkthrough videos with studio voice leveling, Hormozi-style animated captions, and automatic vertical 9:16 re-framing.

```python
polished_video = mls.studio.video.enhance_and_wait(
    video_url="https://cdn.mlsapi.dev/uploads/raw_walkthrough.mp4",
    features={
        "studio_voice": True,        # Wind/echo cleanup & voice mastering
        "animated_subtitles": True,  # Word-by-word dynamic animated subtitles
        "smart_reframe": True,       # Auto-track agent and reframe to 9:16
    },
    subtitle_style={
        "font_theme": "hormozi_bold",
        "primary_color": "#FFFFFF",
        "highlight_color": "#FFDE59",
    },
    export_aspect_ratios=["9:16", "16:9"],
)

print("Reels / TikTok Video:", polished_video.mastered_videos[0].url)
```

---

### 15. Restyle a Furnished Room

```python
restyled = mls.studio.staging.restyle_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/dated_living_room.jpg",
    style="japandi",
    room_type="living_room",
    retain_layout=True,
    custom_restyle_instructions="Low ash-wood furniture, boucle cushions, paper lantern lighting",
)
print("Restyled photo:", restyled.restyled_photo_url)
```

---

### 16. Architectural Rendering (CAD / Sketch to Photoreal)

```python
render = mls.studio.render.architectural_and_wait(
    source_image_url="https://cdn.mlsapi.dev/uploads/sketchup_viewport.png",
    render_type="interior",            # 'interior' | 'exterior'
    style="modern_luxury",
    lighting_environment="golden_hour",  # 'daylight' | 'golden_hour' | 'twilight' | 'overcast' | 'night'
    weather="clear_sunny",
    season="summer",
    custom_instructions="Travertine fireplace wall, wide-plank oak flooring",
)
print("Rendered image:", render.rendered_image_url)
```

---

### 17. Photo-to-Video: Walkthrough, Transition & House Tour

```python
# Animate a single photo into a 5s/10s camera move
clip = mls.studio.video.walkthrough_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/living_room.jpg",
    motion="slow_zoom_in",       # 'orbit_left' | 'orbit_right' | 'pan_left' | 'pan_right' | 'slow_zoom_in' | 'dolly_out' | ...
    duration_seconds=5,          # 5 or 10
    custom_motion_prompt="Slow push toward the fireplace",
    aspect_ratio="9:16",
)
print("Walkthrough clip:", clip.video_url)

# Before/after morph between two images
morph = mls.studio.video.transition_and_wait(
    start_image_url="https://cdn.mlsapi.dev/uploads/empty_living_room.jpg",
    end_image_url=restyled.restyled_photo_url,
    duration_seconds=5,          # 5 or 10
    transition_style="furnishing_timelapse",
    aspect_ratio="9:16",
)
print("Transition video:", morph.video_url)

# Multi-room house tour
tour = mls.studio.video.tour_and_wait(
    ordered_photos=[
        {"room_name": "Exterior Front", "photo_url": "https://cdn.mlsapi.dev/uploads/front.jpg", "highlight": "Double-door entry"},
        {"room_name": "Chef Kitchen", "photo_url": "https://cdn.mlsapi.dev/uploads/kitchen.jpg", "highlight": "Waterfall island"},
        {"room_name": "Primary Suite", "photo_url": "https://cdn.mlsapi.dev/uploads/primary.jpg"},
    ],
    duration_seconds=15,         # 12 | 15 | 30
    auto_script=True,
    aspect_ratio="9:16",
    music_genre="ambient_luxury",
)
print("House tour:", tour.video_url, f"({tour.shots_count} shots)")
```

---

### 18. Custom Generative Prompt

```python
custom = mls.studio.custom.generate_and_wait(
    prompt="Turn this living room into a sunken mid-century conversation pit with terrazzo floors",
    reference_image_urls=["https://cdn.mlsapi.dev/uploads/room.jpg"],
    aspect_ratio="16:9",         # '1:1' | '3:4' | '4:3' | '16:9' | '9:16'
)
print("Generated image:", custom.image_url)
```

---

### 19. Social Publishing

```python
published = mls.studio.social.publish(
    asset_url=tour.video_url,
    asset_type="video",
    destinations=[
        {"platform": "instagram", "target_type": "reels", "caption": "Just listed in Coral Gables!"},
        {"platform": "youtube", "target_type": "shorts", "title": "Coral Gables house tour"},
    ],
    schedule_time="immediate",
)
for item in published.results:
    print(item.platform, item.status, item.post_url)
```

---

## Asynchronous Jobs & Progress Callbacks

Every Studio operation returns immediately with an HTTP 202 `StudioJob` when using the standard method (e.g. `stage(...)`), or polls until completion when using the `*_and_wait(...)` companion method.

### Custom Polling Options & Progress Hook

```python
def on_progress(job):
    print(f"[{job.progress_percentage}%] Step: {job.current_step}")

result = mls.studio.staging.stage_and_wait(
    photo_url="https://cdn.mlsapi.dev/uploads/room.jpg",
    style="japandi",
    poll_interval=2.0,       # Poll every 2.0 seconds (default: 2.0s)
    timeout_seconds=120.0,   # Maximum wait time (default: 90.0s)
    on_progress=on_progress, # Optional progress callback
)
```

### Manual Job Tracking

```python
# Dispatch without waiting
job = mls.studio.staging.stage(photo_url="https://cdn.mlsapi.dev/uploads/room.jpg")
print(f"Track job later: {job.job_id}")

# Check status later
current_status = mls.studio.jobs.get(job.job_id)
print(f"Status: {current_status.status}, progress: {current_status.progress_percentage}%")

# Or wait for it when ready
completed_job = mls.studio.jobs.wait_for(job.job_id, timeout_seconds=90.0)
print("Result URL:", completed_job.result.staged_photo_url)
```

---

## Error Handling

All API errors inherit from `MlsApiError` and expose the HTTP status code, error code, and server message.

```python
from pymlsapi.errors import (
    MlsApiError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    InsufficientCreditsError,
    JobTimeoutError,
)

try:
    listing = mls.listings.get_and_wait("INVALID_ID")
except AuthenticationError as e:
    print("Invalid API Key:", e.message)
except NotFoundError as e:
    print("Listing or resource not found:", e.message)
except RateLimitError as e:
    print(f"Rate limited. Quota resets in {e.retry_after_seconds}s")
except InsufficientCreditsError as e:
    print("Insufficient credits in workspace balance. Top up at https://mlsapi.dev/billing")
except JobTimeoutError as e:
    print(f"Job polling timed out after {e.timeout_seconds}s")
except MlsApiError as e:
    print(f"API Error [{e.code}]: {e.message}")
```

---

## Supported Presets Reference

### Interior Design Styles (29 Presets)

| | | |
|---|---|---|
| `modern` | `luxury` | `scandinavian` |
| `japandi` | `industrial` | `bohemian` |
| `minimalist` | `coastal` | `mid_century_modern` |
| `art_deco` | `farmhouse` | `mediterranean` |
| `contemporary` | `rustic` | `transitional` |
| `french_country` | `hollywood_regency` | `eclectic` |
| `zen` | `bauhaus` | `victorian` |
| `tropical` | `modern_craftsman` | `southwestern` |
| `wabi_sabi` | `shabby_chic` | `chalet` |
| `urban_loft` | `custom` | |

### Architectural Room Types (12 Types)

`living_room`, `bedroom`, `primary_bedroom`, `dining_room`, `kitchen`, `bathroom`, `patio`, `outdoor_patio`, `home_office`, `entryway`, `basement`, `commercial_lobby`.

---

## License

MIT © [mlsapi.dev](https://mlsapi.dev)
