#!/usr/bin/env python3
"""Test McK PPT Design Skill with ESP32 content"""

import sys, os
sys.path.insert(0, os.path.expanduser('~/.openclaw/workspace/skills/Mck-ppt-design-skill'))
from mck_ppt import MckEngine

# Create engine
eng = MckEngine(total_slides=10)

# Slide 1: Cover
eng.cover(
    title="ESP32-C3 Workshop",
    subtitle="เรียนรู้ IoT สไตล์ Maker",
    author="mimiClaw"
)

# Slide 2: TOC
eng.toc(items=[
    ("1", "ESP32 คืออะไร?", "บอร์ด IoT ยอดนิยม"),
    ("2", "การติดตั้ง", "Arduino IDE + ESP32"),
    ("3", "โค้ดตัวอย่าง", "Hello World LED")
])

# Slide 3: Two column text
eng.two_column_text(
    title="ESP32 คืออะไร?",
    columns=[
        ("A", "คุณสมบัติหลัก", [
            "ไมโครคอนโทรลเลอร์ทรงพลัง",
            "มี WiFi + Bluetooth ในตัว", 
            "ราคาถูกมาก",
            "ใช้งานง่าย"
        ]),
        ("B", "การใช้งาน", [
            "Smart Home",
            "IoT Sensors",
            "Robotics",
            "Automation"
        ])
    ]
)

# Slide 4: Process Chevron
eng.process_chevron(
    title="เริ่มต้นใน 4 ขั้นตอน",
    steps=[
        ("1", "ติดตั้ง", "Arduino IDE"),
        ("2", "เพิ่ม ESP32", "Board Manager"),
        ("3", "เขียนโค้ด", "Hello World"),
        ("4", "อัปโหลด", "ไปยังบอร์ด")
    ]
)

# Slide 5: Closing
eng.closing(
    title="พร้อมเริ่มต้นแล้ว!",
    message="มาเรียนรู้ ESP32 กันเถอะ 🚀"
)

# Save
output = "/home/maxtic/esp32-stem-book/esp32_mck.pptx"
eng.save(output)
print(f"✅ Created: {output}")
print(f"📊 Total slides: {eng.total()}")
