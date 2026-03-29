#!/usr/bin/env python3
"""
Script สร้างเสียง TTS สำหรับ Chapter 1
ใช้ ElevenLabs API พร้อม Voice Settings ที่ตั้งค่าไว้
"""

import requests
import os
import json
import time

# ========== CONFIG ==========
ELEVENLABS_API_KEY = "sk_36f107074348fed9b8a699a8d2e9622b13325778827da99e"
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"  # Alice voice

# 🎯 Voice Settings (ตั้งค่าตามรูป)
# - Stability: 0.75 (75-80%)
# - Similarity Boost: 0.85
# - Style: 0.30
# - use_speaker_boost: True
VOICE_SETTINGS = {
    "stability": 0.75,
    "similarity_boost": 0.85,
    "style": 0.30,
    "use_speaker_boost": True
}

# ========== FUNCTIONS ==========
def generate_audio(text, output_path, voice_id=VOICE_ID, model="eleven_v3"):
    """สร้างเสียง TTS จาก ElevenLabs"""
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": model,
        "voice_settings": VOICE_SETTINGS
    }
    
    print(f"🎙️ กำลังสร้างเสียง: {output_path}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ สร้างเสียงสำเร็จ: {output_path}")
            return True
        else:
            error = response.json()
            print(f"❌ ผิดพลาด: {error.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def generate_audio_batch(texts, output_dir, prefix="audio"):
    """สร้างเสียงหลายไฟล์พร้อมกัน"""
    
    os.makedirs(output_dir, exist_ok=True)
    
    results = []
    for i, text in enumerate(texts, 1):
        filename = f"{prefix}_{i:02d}.mp3"
        output_path = os.path.join(output_dir, filename)
        
        success = generate_audio(text, output_path)
        results.append({"file": filename, "success": success})
        
        # Delay ระหว่าง requests
        if i < len(texts):
            time.sleep(0.5)
    
    return results

# ========== CHAPTER 1 SCRIPTS ==========
# แบ่งเป็นส่วนๆ ตาม slide
CHAPTER_1_SCRIPTS = [
    # Slide 1: HOOK
    """เฮ้! ก่อนจะดูต่อ — ถ้าคุณเคยพิมพ์คำถามลงไปที่ ChatGPT แล้วมันตอบมางงๆ ไม่ตรงประเด็น... บอกเลย — มันอาจไม่ใช่ความผิดของ AI นะ แต่เป็นเพราะเราถามผิดวิธีต่างหาก!""",
    
    # Slide 2: AI อยู่รอบตัว
    """สวัสดีครับทุกคน! ยินดีต้อนรับสู่คอร์ส ESP32-C3 ของเรา ก่อนจะลงมือต่อวงจรจริง บทแรกนี้เราจะมารู้จัก AI กันก่อน เพราะ AI จะเป็นเพื่อนร่วมทีมที่ช่วยเราตลอดทาง""",
    
    # Slide 3: AI คืออะไร
    """AI หรือ Artificial Intelligence — ปัญญาประดิษฐ์ มันคือโปรแกรมคอมพิวเตอร์ที่ถูกสอนให้คิดและเข้าใจได้เหมือนมนุษย์ แต่เร็วกว่าเยอะ! AI มี 4 ความสามารถหลัก: เรียนรู้จากข้อมูล เข้าใจภาษามนุษย์ ตัดสินใจจากข้อมูล และสร้างผลลัพธ์ใหม่""",
    
    # Slide 4: AI ทำงานยังไง
    """ลองนึกภาพว่า AI คือคนที่อ่านหนังสือมาทั้งห้องสมุด เมื่อเราถามคำถาม AI จะรับคำถาม ค้นหาข้อมูลที่เกี่ยวข้อง ประมวลผล และตอบกลับ สิ่งสำคัญคือ AI ไม่ได้คิดเหมือนมนุษย์ — มันเป็นโปรแกรมที่ทำนายคำตอบที่น่าจะถูกต้อง""",
    
    # Slide 5: Generative AI
    """AI ที่เราจะใช้กันเรียกว่า Generative AI หรือ AI ที่สร้างงานได้ มันไม่ได้แค่ตอบคำถาม แต่ยังสามารถเขียนข้อความ เขียนโค้ด วาดรูป และอธิบายเรื่องยากให้เข้าใจง่าย""",
    
    # Slide 6: AI ช่วยเขียนโค้ด
    """สำหรับการเขียนโค้ด AI สามารถช่วยเราได้หลายอย่าง ถามว่าโค้ดนี้ทำงานยังไง หรือขอให้เขียนโค้ดใหม่ ช่วยแก้ไขโค้ดที่ผิด หรือเพิ่มเติมฟังก์ชันใหม่ๆ AI จึงเป็นเพื่อนฉลาดที่ช่วยเราสร้างโปรเจกต์ได้เร็วขึ้นมาก!""",
    
    # Slide 7: เครื่องมือที่ใช้
    """ในคอร์สนี้เราจะใช้เครื่องมือ AI สองตัวหลักๆ คือ ChatGPT สำหรับถามตอบทุกเรื่องและเขียนโค้ด และ GitHub Copilot สำหรับเขียนโค้ดแบบ auto-complete ทั้งสองฟรี!""",
    
    # Slide 8: CTA
    """ก่อนจบบทนี้ ถามเพื่อนๆ หน่อย พี่เคยใช้ AI ช่วยเขียนโค้ดมั้ย? บอกในคอมเมนต์มาเลย! แล้วก็ Follow ก่อนนะ เดี๋ยวบทต่อไปสนุกกว่านี้!""",
]

# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🎙️ สร้างเสียง Chapter 1: AI คืออะไร?")
    print("=" * 50)
    
    # สร้างโฟลเดอร์
    output_dir = "/home/maxtic/esp32-stem-book/chapter01/audio"
    os.makedirs(output_dir, exist_ok=True)
    
    # สร้างเสียงทั้งหมด
    print("\n📝 Voice Settings ที่ใช้:")
    print(f"   Stability: {VOICE_SETTINGS['stability']}")
    print(f"   Similarity Boost: {VOICE_SETTINGS['similarity_boost']}")
    print(f"   Style: {VOICE_SETTINGS['style']}")
    print(f"   Speaker Boost: {VOICE_SETTINGS['use_speaker_boost']}")
    print()
    
    results = generate_audio_batch(
        CHAPTER_1_SCRIPTS,
        output_dir,
        prefix="ch01"
    )
    
    # สรุปผล
    print("\n" + "=" * 50)
    print("📊 สรุปผล:")
    success_count = sum(1 for r in results if r["success"])
    print(f"   สำเร็จ: {success_count}/{len(results)}")
    print("=" * 50)
