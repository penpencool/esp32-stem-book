# 🔰 ESP32-C3 พื้นฐาน

## ESP32-C3 คืออะไร?

**ESP32-C3** คือไมโครคอนโทรลเลอร์ (MCU) ที่ผลิตโดย Espressif ตระกูลเดียวกับ ESP32

```
┌─────────────────────────────────┐
│         ESP32-C3                │
│  ┌───────────────────────────┐  │
│  │   CPU: RISC-V 32-bit      │  │
│  │   ความเร็ว: 160 MHz      │  │
│  │   WiFi: 802.11 b/g/n      │  │
│  │   Bluetooth: BLE 5.0       │  │
│  │   Flash: 4MB              │  │
│  │   RAM: 400 KB              │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## ทำไมต้องเลือก ESP32-C3?

| คุณสมบัติ | ESP32-C3 | Arduino UNO |
|-----------|----------|------------|
| WiFi | ✅ มี | ❌ ไม่มี |
| Bluetooth | ✅ มี | ❌ ไม่มี |
| ราคา | ~150฿ | ~250฿ |
| ความเร็ว | 160 MHz | 16 MHz |
| ADC | 12-bit (6 ch) | 10-bit (6 ch) |

## ขาต่างๆ ของ ESP32-C3

```
        ┌─────────────────────────┐
        │                         │
        │    ESP32-C3 DevKitM-1  │
        │                         │
   USB ─┤ ○                      │
        │                    LED ○ │  (GPIO 8)
        │                         │
        │  GND  5V  3V3  GPIO   │
        │  (เขียนหมายเลขขา)       │
        │                         │
        └─────────────────────────┘

GPIO พื้นฐานที่ใช้บ่อย:
- GPIO 0: สวิตช์ BOOT
- GPIO 1: TX (Serial)
- GPIO 2: ADC/LDR (ไม่ใช้ตอน boot)
- GPIO 3: RX (Serial)
- GPIO 4-5: Strapping pins (ระวัง!)
- GPIO 6-11: SPI Flash (หลีกเลี่ยง!)
- GPIO 12-21: ใช้งานทั่วไปได้ ✅
```

## GPIO ที่ควรใช้

### ✅ ใช้ได้ปลอดภัย

| GPIO | ฟังก์ชัน | ใช้ทำอะไร |
|------|----------|------------|
| 0 | ADC, Boot button | อ่านค่า Analog |
| 1 | TX Serial | Debug |
| 2 | ADC | LDR, วัดแสง |
| 3 | RX Serial | Debug |
| 12-21 | Digital I/O | ทั่วไป ✅ |

### ⚠️ ใช้ด้วยความระวัง

| GPIO | ข้อควรระวัง |
|------|-------------|
| 4-5 | Strapping pins - กำหนดโหมด boot |
| 6-11 | SPI Flash - หลีกเลี่ยงใช้เป็น GPIO |
| 21 | มี LED บิลต์อิน (บางรุ่น) |

## การติดตั้ง PlatformIO

### 1. ติดตั้ง VS Code

```
1. ดาวน์โหลด VS Code: https://code.visualstudio.com/
2. ติดตั้งตามปกติ
```

### 2. ติดตั้ง PlatformIO Extension

```
1. เปิด VS Code
2. กด Ctrl+Shift+X (Extensions)
3. พิมพ์ "PlatformIO IDE"
4. กด Install
5. รีสตาร์ท VS Code
```

### 3. สร้างโปรเจกต์แรก

```bash
# เปิด Terminal ใน VS Code (Ctrl+`)

# สร้างโปรเจกต์ใหม่
pio project init --board esp32-c3-devkitm-1

# หรือใช้ PIO Home
pio home  # แล้วกด "New Project"
```

## โครงสร้างโปรเจกต์ PlatformIO

```
myproject/
├── src/
│   └── main.cpp          ← โค้ดหลัก
├── lib/
│   └── README            ← ไลบรารีที่เพิ่มเอง
├── include/
│   └── README            ← Header files
├── test/
│   └── README            ← ทดสอบ
└── platformio.ini        ← การตั้งค่าโปรเจกต์
```

## ไฟล์ platformio.ini

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino

# เพิ่มไลบรารี
lib_deps =
    adafruit/Adafruit Unified Sensor
    adafruit/DHT sensor library
    adafruit/Adafruit SSD1306
    adafruit/Adafruit GFX Library

# ตั้งค่า Serial Monitor
monitor_speed = 115200
```

## โค้ดแรก: Hello ESP32

```cpp
// src/main.cpp
#include <Arduino.h>

void setup() {
    // เริ่ม Serial Monitor
    Serial.begin(115200);
    
    // พิมพ์ข้อความเมื่อเริ่ม
    Serial.println("Hello from ESP32-C3!");
}

void loop() {
    // พิมพ์ข้อความทุก 1 วินาที
    Serial.println("I'm running!");
    delay(1000);
}
```

## อัปโหลดโค้ด

```bash
# อัปโหลดไปยังบอร์ด
pio run --target upload

# หรือกดปุ่ม Upload ใน PIO Home
```

## ดู Serial Monitor

```bash
pio device monitor
```

## คำศัพท์ที่ควรรู้

| คำศัพท์ | ความหมาย |
|---------|----------|
| GPIO | General Purpose Input/Output - ขาทั่วไปสำหรับรับ-ส่งสัญญาณ |
| ADC | Analog-to-Digital Converter - แปลงสัญญาณ analog เป็น digital |
| PWM | Pulse Width Modulation - ส่งสัญญาณดิจิตอลแบบจำลอง analog |
| I2C | Inter-Integrated Circuit - มาตรฐานการสื่อสารอนุกรม |
| UART | Universal Asynchronous Receiver/Transmitter - สื่อสารกับคอมพิวเตอร์ |

## สิ่งที่ควรจำ

```
✅ ทำได้:
- ใช้ GPIO 12-21 ได้เลย
- ต่อ LED, สวิตช์, เซ็นเซอร์ได้
- ใช้ WiFi, Bluetooth ได้

❌ ทำไม่ได้:
- ต่อ GPIO 6-11 เป็นขา I/O ทั่วไป
- ใช้ analogWrite() กับทุกขา (บางขาเป็น input only)
```

---

## 📚 เรียนรู้เพิ่มเติม

- [GPIO Guide](./gpio-guide.md)
- [วงจรพื้นฐาน](./circuit-basics.md)
- [AI Prompt สำหรับ ESP32](../06-ai-prompts/basic-prompts.md)
