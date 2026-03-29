#!/usr/bin/env python3
"""
Combine slides images with audio to create video
Uses moviepy which bundles ffmpeg
"""

import os
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
from pathlib import Path
import json

# Configuration
SLIDES_DIR = Path("/home/maxtic/esp32-stem-book/chapter01/video/slides")
AUDIO_DIR = Path("/home/maxtic/esp32-stem-book/chapter01/audio")
OUTPUT_FILE = Path("/home/maxtic/esp32-stem-book/chapter01/video/chapter01.mp4")
MANIFEST_FILE = Path("/home/maxtic/esp32-stem-book/chapter01/video/slides_manifest.json")

print("🎬 Video Combiner - Chapter 01")
print("=" * 50)

# Load manifest
with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"📋 {manifest['total_slides']} slides, total: {manifest['total_duration_formatted']}")

# Create video clips with audio
clips = []
total_duration = 0

for i, slide_info in enumerate(manifest["slides"]):
    slide_num = slide_info["slide"]
    audio_file = slide_info.get("audio_file")
    
    # Image file
    img_file = SLIDES_DIR / f"slide-{slide_num:02d}.png"
    if not img_file.exists():
        img_file = SLIDES_DIR / f"slide-{slide_num:03d}.png"
    
    if img_file.exists() and audio_file and Path(audio_file).exists():
        # Load audio to get actual duration
        audio = AudioFileClip(audio_file)
        actual_duration = audio.duration
        
        print(f"\n[{i+1}/10] Slide {slide_num}: {slide_info['title']}")
        print(f"   Audio duration: {actual_duration:.2f}s")
        
        # Create clip with image and audio
        # Use actual audio duration, not the manifest value
        clip = ImageClip(str(img_file)).with_duration(actual_duration).with_audio(audio)
        clips.append(clip)
        total_duration += actual_duration
        print(f"   ✅ Combined ({actual_duration:.1f}s)")
    elif img_file.exists():
        duration = slide_info["duration_sec"]
        clip = ImageClip(str(img_file)).with_duration(duration)
        clips.append(clip)
        total_duration += duration
        print(f"   ⚠️ Image only - {duration}s")
    else:
        print(f"   ❌ Not found!")

# Concatenate all clips
print(f"\n🔗 Concatenating {len(clips)} clips...")
final_video = concatenate_videoclips(clips, method="compose")

# Write output
print(f"\n💾 Writing video...")
final_video.write_videofile(
    str(OUTPUT_FILE),
    fps=1,
    codec='libx264',
    audio_codec='aac',
    audio_bitrate='128k'
)

duration = final_video.duration
print(f"\n✅ Done!")
print(f"   📁 {OUTPUT_FILE}")
print(f"   ⏱️ Duration: {int(duration//60)}:{int(duration%60):02d}")
