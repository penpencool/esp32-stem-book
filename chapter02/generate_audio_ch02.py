#!/usr/bin/env python3
"""
Script สร้างเสียง TTS สำหรับ Chapter 2
ใช้ ElevenLabs API พร้อม Voice Settings
"""

import requests
import os
import time

# ========== CONFIG ==========
ELEVENLABS_API_KEY = "sk_36f107074348fed9b8a699a8d2e9622b13325778827da99e"
VOICE_ID = "Xb7hH8MSUJpSbSDYk0k2"  # Alice voice

# 🎯 Voice Settings
VOICE_SETTINGS = {
    "stability": 0.75,
    "similarity_boost": 0.85,
    "style": 0.30,
    "use_speaker_boost": True
}

# ========== FUNCTIONS ==========
def generate_audio(text, output_path):
    """สร้างเสียง TTS จาก ElevenLabs"""
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": "eleven_v3",
        "voice_settings": VOICE_SETTINGS
    }
    
    print(f"🎙️ กำลังสร้างเสียง: {output_path}")
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=60)
        
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"✅ สำเร็จ: {output_path}")
            return True
        else:
            error = response.json()
            print(f"❌ ผิดพลาด: {error.get('message', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

# ========== CHAPTER 2 SCRIPTS ==========
CHAPTER_2_SCRIPTS = [
    # Slide 1: HOOK
    """เฮ้! ก่อนจะดูต่อ — ถ้าเคยเห็นหน้าจอ Error แล้วรู้สึกท้อ... บอกเลย — คุณไม่ได้แก่คนเดียว! แม้แต่โปรแกรมเมอร์มืออาชีพก็ยังเจอ Error ตอนติดตั้งเยอะมาก! แต่วันนี้เราจะมาทำให้มันง่ายที่สุด...""",
    
    # Slide 2: VS Code คืออะไร?
    """สวัสดีครับทุกคน! ยินดีต้อนรับกลับมาสู่บทที่ 2! ในบทนี้เราจะมาเตรียมครัวให้พร้อมสำหรับการเขียนโค้ดกัน! ถ้าเปรียบการเขียนโค้ดเป็นการทำอาหาร VS Code กับ PlatformIO ก็เหมือนเตาและอุปกรณ์ที่ดี มีแล้วการทำอาหารจะง่ายขึ้นเยอะ!""",
    
    # Slide 3: PlatformIO คืออะไร?
    """PlatformIO คือ Extension หรือส่วนขยายที่ติดตั้งเพิ่มใน VS Code มันเหมือนกับการติดตั้งแอปเพิ่มในมือถือ ถ้าอินเทอร์เน็ตคือมือถือ PlatformIO ก็เหมือนแอปที่ทำให้มือถือโทรหาทุกคนได้ เพราะ PlatformIO จะทำให้ VS Code สามารถส่งโค้ดไปบอร์ด ESP32 ได้เลย!""",
    
    # Slide 4: วิธีติดตั้ง VS Code
    """มาเริ่มติดตั้ง VS Code กันเลย! ขั้นตอนง่ายๆ สี่ขั้นตอน ขั้นตอนที่หนึ่ง ไปที่ code.visualstudio.com ขั้นตอนที่สอง กดปุ่ม Download for Windows ขั้นตอนที่สาม เปิดไฟล์ .exe ที่ดาวน์โหลดมา ขั้นตอนที่สี่ ทำตามขั้นตอน อย่าลืมเลือก Add to PATH ด้วย!""",
    
    # Slide 5: วิธีติดตั้ง PlatformIO
    """เมื่อติดตั้ง VS Code เสร็จแล้ว ต่อไปคือติดตั้ง PlatformIO ขั้นตอนที่หนึ่ง เปิด VS Code ขึ้นมา ขั้นตอนที่สอง คลิกไอคอนรูปสี่เหลี่ยมสี่ช่องด้านซ้าย ขั้นตอนที่สาม พิมพ์ platformio ide ในช่องค้นหา ขั้นตอนที่สี่ กด Install ที่ PlatformIO IDE รอประมาณห้าถึงสิบนาทีแล้ว reload!""",
    
    # Slide 6: สร้าง Project แรก
    """ตอนนี้เรามีเครื่องมือพร้อมแล้ว! มาสร้าง Project แรกกัน ขั้นตอนที่หนึ่ง คลิกไอคอน Ant ของ PlatformIO ขั้นตอนที่สอง กด PIO New Project ขั้นตอนที่สาม ตั้งชื่อว่า HelloESP32 ขั้นตอนที่สี่ เลือก Board เป็น ESP32-C3 Dev Module ขั้นตอนที่ห้า เลือก Framework เป็น Arduino ขั้นตอนที่หก กด Finish!""",
    
    # Slide 7: เขียนโค้ดแรก
    """มาเขียนโค้ดแรกกัน! ลบโค้ดเดิมใน main.cpp แล้วพิมพ์ตามนี้ ในฟังก์ชัน setup เราจะเริ่มคุยกับคอมพิวเตอร์ที่ความเร็ว 115200 รอจนเชื่อมต่อ แล้วพิมพ์ข้อความทักทาย ในฟังก์ชัน loop เราจะพิมพ์ข้อความบอกว่าบอร์ดกำลังทำงาน แล้วรอสองวินาทีแล้วทำซ้ำไปเรื่อยๆ""",
    
    # Slide 8: อัปโหลดโค้ด + Serial Monitor
    """ถ้ามีบอร์ด ESP32-C3 อยู่ ลองอัปโหลดโค้ดไปได้เลย! เสียบสาย USB เข้าบอร์ด เลือก Port ใน Status Bar กดปุ่ม Upload รอจนเห็น Hard resetting via RTS pin สำเร็จแล้ว! ต่อไปมาเปิด Serial Monitor ดูผลลัพธ์กัน กดปุ่ม Plug icon หรือกด Ctrl Shift M เลือก Baud Rate เป็น 115200 แล้วจะเห็นข้อความ Hello ESP32-C3! พิมพ์ขึ้นมาเรื่อยๆ!""",
    
    # Slide 9: AI ช่วยแก้ Error
    """มาฝึกใช้ AI ช่วยแก้ Error กัน! ลองเขียนโค้ดที่มี Error จงใจ กด Build ดู Error แล้ว Copy Error Message ไปถาม ChatGPT ว่าช่วยดูโค้ด Arduino สำหรับ ESP32-C3 ให้หน่อย เจอ Error แล้ววางโค้ดและ Error Message ลงไป AI จะบอกว่าผิดตรงไหนและแก้ให้เลย! ยิ่งให้ข้อมูลมาก AI ยิ่งช่วยได้ดี!""",
    
    # Slide 10: CTA + สรุป
    """ก่อนจบบทนี้ ถามเพื่อนๆ หน่อย ติดตั้ง VS Code กับ PlatformIO สำเร็จมั้ย? ถ้าเจอ Error อะไร บอกในคอมเมนต์มาเลย! ถ้าชอบบทเรียนนี้ กด Like และ Subscribe ด้วยนะ! บทต่อไปเราจะมาลงมือต่อวงจร LED จริงๆ เลย! สรุปบทที่สองวันนี้ เราได้เรียนรู้เรื่อง VS Code โปรแกรมแก้ไขโค้ดยอดนิยม PlatformIO Extension ที่รองรับ ESP32 การสร้าง Project และความแตกต่างระหว่าง setup กับ loop พร้อมทั้งการใช้ AI ช่วยแก้ Error! บางครั้ง!""",
]

# ========== MAIN ==========
if __name__ == "__main__":
    print("=" * 50)
    print("🎙️ สร้างเสียง Chapter 2: ติดตั้งเครื่องมือ พร้อมเขียนโค้ด!")
    print("=" * 50)
    
    output_dir = "/mnt/mimi/esp32-tutor/chapter02/audio"
    os.makedirs(output_dir, exist_ok=True)
    
    print("\n📝 Voice Settings:")
    print(f"   Stability: {VOICE_SETTINGS['stability']}")
    print(f"   Similarity Boost: {VOICE_SETTINGS['similarity_boost']}")
    print(f"   Style: {VOICE_SETTINGS['style']}")
    print(f"   Speaker Boost: {VOICE_SETTINGS['use_speaker_boost']}")
    print()
    
    success_count = 0
    for i, script in enumerate(CHAPTER_2_SCRIPTS, 1):
        filename = f"ch02_{i:02d}.mp3"
        output_path = os.path.join(output_dir, filename)
        
        if generate_audio(script, output_path):
            success_count += 1
        
        if i < len(CHAPTER_2_SCRIPTS):
            time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print(f"📊 สรุปผล: สำเร็จ {success_count}/{len(CHAPTER_2_SCRIPTS)}")
    print("=" * 50)
