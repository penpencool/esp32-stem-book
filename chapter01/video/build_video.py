#!/usr/bin/env python3
"""
Video Builder - Combine PPTX with audio
- Extract slides from PPTX as images
- Combine with audio based on manifest timing
- Output final video
"""

import os
import json
import subprocess
from pathlib import Path
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE

# Configuration
CHAPTER_DIR = Path("/home/maxtic/esp32-stem-book/chapter01")
VIDEO_DIR = CHAPTER_DIR / "video"
AUDIO_DIR = CHAPTER_DIR / "audio"
MANIFEST_FILE = VIDEO_DIR / "slides_manifest.json"
PPTX_FILE = VIDEO_DIR / "chapter01.pptx"  # User needs to export from Felo

def extract_slides_from_pptx(pptx_path, output_dir):
    """Extract slides from PPTX as images using LibreOffice + ImageMagick"""
    if not pptx_path.exists():
        print(f"❌ PPTX file not found: {pptx_path}")
        print("   Please export from Felo and place here")
        return False
    
    print(f"📄 Extracting slides from {pptx_path}...")
    
    # Convert PPTX to PDF first
    pdf_path = output_dir / "slides.pdf"
    
    try:
        # Convert to PDF using LibreOffice
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", output_dir, str(pptx_path)
        ], check=True, capture_output=True)
        
        # Convert PDF to images
        print("🖼️ Converting PDF to images...")
        subprocess.run([
            "pdftoppm", "-png", "-r", "150",
            str(pdf_path), str(output_dir / "slide")
        ], check=True, capture_output=True)
        
        print(f"✅ Extracted slides to {output_dir}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Tool not found: {e}")
        return False

def create_video_from_manifest(manifest, slides_dir):
    """Create video by combining images with audio based on manifest"""
    print("\n🎬 Creating video...")
    
    # Build FFmpeg concat file
    concat_file = VIDEO_DIR / "concat.txt"
    
    with open(concat_file, "w") as f:
        for slide_info in manifest["slides"]:
            slide_num = slide_info["slide"]
            duration = slide_info["duration_sec"]
            audio_file = slide_info.get("audio_file")
            
            # Find the slide image
            slide_img = slides_dir / f"slide-{slide_num:03d}.png"
            if not slide_img.exists():
                slide_img = slides_dir / f"slide{slide_num:02d}.png"
            if not slide_img.exists():
                slide_img = slides_dir / f"slide_{slide_num:02d}.png"
            
            if not slide_img.exists():
                print(f"⚠️ Slide image not found for slide {slide_num}")
                continue
            
            # Write concat entry
            f.write(f"file '{slide_img}'\n")
            f.write(f"duration {duration}\n")
    
    # Get total duration
    total_duration = manifest.get("total_duration_sec", 0)
    
    # Build audio file list
    audio_files = []
    for slide_info in manifest["slides"]:
        audio_file = slide_info.get("audio_file")
        if audio_file and Path(audio_file).exists():
            audio_files.append(audio_file)
    
    # Create video using FFmpeg
    output_file = VIDEO_DIR / "chapter01.mp4"
    
    if audio_files:
        # Combine all audio files first
        audio_list_file = VIDEO_DIR / "audio_list.txt"
        with open(audio_list_file, "w") as f:
            for af in audio_files:
                f.write(f"file '{af}'\n")
        
        # Concatenate audio
        combined_audio = VIDEO_DIR / "combined_audio.mp3"
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(audio_list_file),
            "-c", "copy", str(combined_audio)
        ], check=True, capture_output=True)
        
        # Create video with audio
        print(f"🎙️ Combining video with audio...")
        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", "1,
            "-i", str(slides_dir / "slide-%03d.png"),
            "-i", str(combined_audio),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-shortest",
            str(output_file)
        ], check=True, capture_output=True)
    else:
        # Video without audio
        print("⚠️ No audio files, creating silent video")
        subprocess.run([
            "ffmpeg", "-y",
            "-framerate", "1",
            "-i", str(slides_dir / "slide-%03d.png"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", str(total_duration),
            str(output_file)
        ], check=True, capture_output=True)
    
    print(f"✅ Video saved: {output_file}")
    return output_file

def main():
    """Main function"""
    print("🎬 Video Builder")
    print("=" * 50)
    
    # Load manifest
    if not MANIFEST_FILE.exists():
        print(f"❌ Manifest not found: {MANIFEST_FILE}")
        print("   Run generate_audio.py first!")
        return
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    print(f"📋 Loaded manifest: {manifest['total_slides']} slides")
    print(f"⏱️ Total duration: {manifest.get('total_duration_formatted', 'N/A')}")
    
    # Extract slides from PPTX
    if not extract_slides_from_pptx(PPTX_FILE, VIDEO_DIR):
        print("\n📝 Manual steps required:")
        print(f"   1. Go to Felo: https://felo.ai/slides/BZVSoG4xyqViZpcix5Sf6y")
        print(f"   2. Export as PPTX")
        print(f"   3. Save to: {PPTX_FILE}")
        print(f"   4. Run this script again")
        return
    
    # Create video
    output = create_video_from_manifest(manifest, VIDEO_DIR)
    
    print("\n" + "=" * 50)
    print(f"✅ Complete! Video: {output}")

if __name__ == "__main__":
    main()
