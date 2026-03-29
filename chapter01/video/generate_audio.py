#!/usr/bin/env python3
"""
Chapter Audio Generator
- Generate audio from scripts using ElevenLabs
- Measure duration for each slide
- Create manifest for video production
"""

import os
import json
import subprocess
from pathlib import Path

# Configuration
CHAPTER_DIR = Path("/home/maxtic/esp32-stem-book/chapter01")
AUDIO_DIR = CHAPTER_DIR / "audio"
MANIFEST_FILE = CHAPTER_DIR / "video" / "slides_manifest.json"

# ElevenLabs API Key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "sk_36f107074348fed9b8a699a8d2e9622b13325778827da99e")

# Voice settings - using ElevenLabs API directly
# Alice - Clear, Engaging Educator (good for Thai with multilingual model)
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"  # Alice voice ID

def get_audio_duration(audio_file):
    """Get duration of audio file using MP3 duration estimation"""
    try:
        # Try using ffprobe first
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "json", str(audio_file)
        ], capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception:
        # Fallback: estimate from file size and bitrate
        # Most ElevenLabs audio is 128kbps MP3
        file_size = os.path.getsize(audio_file)
        # At 128kbps = 16000 bytes/sec
        estimated_duration = file_size / 16000
        print(f"   (estimated duration: {estimated_duration:.1f}s)")
        return estimated_duration

def generate_audio_elevenlabs(text, output_file, voice_id=None):
    """Generate audio using ElevenLabs API"""
    import requests
    
    # Use hardcoded Alice voice
    if voice_id is None:
        voice_id = VOICE_ID
    
    if voice_id is None:
        print("No voice found!")
        return False
    
    # Generate audio
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.85,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }
    
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

def load_scripts():
    """Load teaching scripts from file or create from chapter"""
    script_file = CHAPTER_DIR / "script" / "script_teaching.md"
    
    if script_file.exists():
        with open(script_file, "r", encoding="utf-8") as f:
            content = f.read()
        return parse_scripts_from_markdown(content)
    else:
        # Create scripts from chapter content
        return create_scripts_from_chapter()

def parse_scripts_from_markdown(content):
    """Parse scripts from markdown format"""
    scripts = []
    current_slide = None
    
    for line in content.split("\n"):
        if line.startswith("## Slide"):
            if current_slide:
                scripts.append(current_slide)
            current_slide = {"slide": len(scripts) + 1, "script": ""}
        elif current_slide and line.strip():
            current_slide["script"] += line + " "
    
    if current_slide:
        scripts.append(current_slide)
    
    return scripts

def create_scripts_from_chapter():
    """Create slide scripts from chapter content"""
    readme = CHAPTER_DIR / "README.md"
    
    if not readme.exists():
        print("No README.md found!")
        return []
    
    with open(readme, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Design 10 slides based on content structure
    slides = [
        {
            "slide": 1,
            "title": "บทที่ 1: AI คืออะไร?",
            "script": "สวัสดีครับ ยินดีต้อนรับสู่บทเรียนแรกของหนังสือ ESP32-C3 STEM AI Coding วันนี้เราจะมาเรียนรู้เรื่อง AI หรือปัญญาประดิษฐ์ ว่ามันคืออะไร และทำไมนักเขียนโค้ดอย่างเราควรรู้จักมัน"
        },
        {
            "slide": 2,
            "title": "AI คืออะไร?",
            "script": "AI หรือ Artificial Intelligence คือระบบคอมพิวเตอร์ที่ถูกออกแบบมาให้เรียนรู้ เข้าใจ และตัดสินใจได้เหมือนมนุษย์ ลองนึกภาพว่ามันเหมือนเพื่อนฉลาดที่รู้เรื่องเยอะมาก และช่วยเราได้ตลอด 24 ชั่วโมง"
        },
        {
            "slide": 3,
            "title": "AI อยู่รอบตัวเราแล้ว",
            "script": "รู้มั้ยว่าเราเจอ AI ในชีวิตประจำวันแทบทุกวัน เมื่อเราถาม Google ว่าอากาศเป็นยังไง เมื่อดู YouTube แล้วเห็นคำแนะนำวิดีโอที่ชอบ เมื่อถ่ายรูปแล้วมือถือตรวจจับใบหน้า ล้วนมี AI ช่วยทั้งนั้น"
        },
        {
            "slide": 4,
            "title": "Generative AI",
            "script": "AI ที่เราจะใช้กันเรียกว่า Generative AI หรือ AI ที่สร้างงานได้ มันไม่ได้แค่ตอบคำถาม แต่ยังเขียนข้อความ เขียนโค้ด วาดรูป และอธิบายเรื่องยากให้เข้าใจง่ายได้"
        },
        {
            "slide": 5,
            "title": "ChatGPT - ผู้ช่วย AI",
            "script": "ChatGPT พัฒนาโดย OpenAI เป็น AI ที่เราสามารถสนทนาด้วยได้ คล้ายกับการแชทกับเพื่อน แต่เพื่อนนี้รู้เรื่องเยอะมากและตอบได้ตลอด 24 ชั่วโมง สามารถตอบคำถาม เขียนบทความ และช่วยเขียนโค้ดได้"
        },
        {
            "slide": 6,
            "title": "GitHub Copilot",
            "script": "GitHub Copilot เป็น AI ที่ออกแบบมาเพื่อช่วยเขียนโค้ดโดยเฉพาะ มันจะเติมโค้ดให้เราอัตโนมัติขณะที่เรากำลังเขียน ช่วยเพิ่มความเร็วในการเขียนโปรแกรมได้มาก"
        },
        {
            "slide": 7,
            "title": "Prompt Engineering",
            "script": "Prompt คือคำถามหรือคำสั่งที่เราพิมพ์ให้ AI การเขียน Prompt ที่ดีจะช่วยให้ได้คำตอบที่ตรงใจมากขึ้น หลักการสำคัญคือ บอกให้ชัดว่าต้องการอะไร บอกบริบท และบอกรูปแบบที่ต้องการ"
        },
        {
            "slide": 8,
            "title": "ตัวอย่าง Prompt ที่ดี",
            "script": "ตัวอย่าง Prompt ที่ไม่ดีคือ ช่วยโค้ดหน่อย ส่วน Prompt ที่ดีคือ ช่วยเขียนโค้ด Arduino สำหรับ ESP32-C3 ให้ LED ต่อที่ GPIO 8 กระพริบเปิด-ปิดทุก 1 วินาที พร้อมอธิบายแต่ละบรรทัดเป็นภาษาไทย"
        },
        {
            "slide": 9,
            "title": "จริยธรรมในการใช้ AI",
            "script": "AI มีข้อจำกัด อย่าไว้ใจมากเกินไป AI อาจโกหกได้ เรียกว่า hallucination AI อาจให้ข้อมูลเก่า และอาจเขียนโค้ดผิดได้ ดังนั้นต้องตรวจสอบทุกครั้ง ใช้ AI เป็นผู้ช่วยไม่ใช่ผู้แทน และไม่ใช้ AI ในทางที่ผิด"
        },
        {
            "slide": 10,
            "title": "สรุปบทเรียน",
            "script": "สรุปวันนี้เราได้เรียนรู้ว่า AI คือปัญญาประดิษฐ์ที่ช่วยเราได้หลายอย่าง ChatGPT และ GitHub Copilot เป็นเครื่องมือที่จะช่วยในการเขียนโค้ด Prompt Engineering สำคัญมากในการได้คำตอบที่ดี และอย่าลืมใช้ AI อย่างมีความรับผิดชอบ บทต่อไปเราจะมาติดตั้งเครื่องมือเขียนโค้ดกัน"
        }
    ]
    
    return slides

def main():
    """Main function to generate audio for all slides"""
    print("🎙️ Chapter Audio Generator")
    print("=" * 50)
    
    # Create audio directory
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    
    # Load scripts
    print("\n📖 Loading scripts...")
    slides = load_scripts()
    print(f"Found {len(slides)} slides")
    
    # Generate audio for each slide
    manifest = {
        "chapter": 1,
        "total_slides": len(slides),
        "slides": []
    }
    
    print("\n🎙️ Generating audio...")
    for i, slide in enumerate(slides):
        slide_num = slide["slide"]
        script = slide["script"]
        title = slide.get("title", f"Slide {slide_num}")
        
        audio_file = AUDIO_DIR / f"slide_{slide_num:02d}.mp3"
        
        print(f"\n[{i+1}/{len(slides)}] Slide {slide_num}: {title}")
        print(f"   Script: {script[:50]}...")
        
        # Generate audio
        success = generate_audio_elevenlabs(script, audio_file)
        
        if success:
            # Get duration
            duration = get_audio_duration(audio_file)
            print(f"   ✅ Generated: {audio_file} ({duration:.1f}s)")
            
            manifest["slides"].append({
                "slide": slide_num,
                "title": title,
                "script": script,
                "audio_file": str(audio_file),
                "duration_sec": round(duration, 1) if duration else 0
            })
        else:
            print(f"   ❌ Failed to generate audio")
            manifest["slides"].append({
                "slide": slide_num,
                "title": title,
                "script": script,
                "audio_file": None,
                "duration_sec": 0
            })
    
    # Calculate total duration
    total_duration = sum(s["duration_sec"] for s in manifest["slides"])
    manifest["total_duration_sec"] = total_duration
    manifest["total_duration_formatted"] = f"{int(total_duration // 60)}:{int(total_duration % 60):02d}"
    
    # Save manifest
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 50)
    print(f"✅ Done! Total duration: {manifest['total_duration_formatted']}")
    print(f"📁 Manifest saved: {MANIFEST_FILE}")
    print(f"🎙️ Audio files: {AUDIO_DIR}")

if __name__ == "__main__":
    main()
