# 🔰 พื้นฐาน ESP32-C3

## ไฟล์ในหมวดนี้

| ไฟล์ | หัวข้อ | ระดับ |
|------|--------|-------|
| [esp32c3-basics.md](./esp32c3-basics.md) | รู้จัก ESP32-C3 + การติดตั้ง | 🔰 ผู้เริ่มต้น |
| [gpio-guide.md](./gpio-guide.md) | GPIO, ADC, PWM, I2C | 🔰 ผู้เริ่มต้น |
| [circuit-basics.md](./circuit-basics.md) | วงจร LED, สวิตช์, LDR, Relay | 🔰 ผู้เริ่มต้น |

## เนื้อหาสรุป

### ESP32-C3 คืออะไร?

**ESP32-C3** คือไมโครคอนโทรลเลอร์ที่มี:
- ✅ WiFi ในตัว
- ✅ Bluetooth ในตัว
- ✅ ราคาถูก (~150฿)
- ✅ ขนาดเล็ก

### ทำไมต้องเลือก ESP32-C3?

| คุณสมบัติ | ESP32-C3 | Arduino UNO |
|-----------|---------|-------------|
| WiFi | ✅ มี | ❌ ไม่มี |
| Bluetooth | ✅ มี | ❌ ไม่มี |
| ราคา | ~150฿ | ~250฿ |
| ความเร็ว | 160 MHz | 16 MHz |

### GPIO ที่ใช้บ่อย

```
✅ ใช้ได้ปลอดภัย: GPIO 0, 1, 2, 3, 12-21
⚠️ ระวัง: GPIO 4, 5 (strapping pins)
❌ หลีกเลี่ยง: GPIO 6-11 (SPI Flash)
```

### การติดตั้ง PlatformIO

```bash
# 1. ติดตั้ง PlatformIO ใน VS Code
# Ctrl+Shift+X → ค้นหา "PlatformIO IDE" → Install

# 2. สร้างโปรเจกต์ใหม่
pio project init --board esp32-c3-devkitm-1

# 3. เพิ่ม library ใน platformio.ini
lib_deps =
    adafruit/DHT sensor library
    adafruit/Adafruit SSD1306
```

### โค้ดแรก: Hello ESP32

```cpp
#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    Serial.println("Hello from ESP32-C3!");
}

void loop() {
    Serial.println("I'm running!");
    delay(1000);
}
```

### วงจร LED พื้นฐาน

```
    3.3V
      │
     [R]  220Ω - 1kΩ
      │
      ├────── GPIO 2
      │
     [LED]
      │
     GND
```

### วงจรสวิตช์ Input

```
    GPIO 0 ──┤SW├── GND
    
    ใช้ INPUT_PULLUP ในโค้ด:
    pinMode(0, INPUT_PULLUP);
```

## คำศัพท์สำคัญ

| คำศัพท์ | ความหมาย |
|---------|----------|
| GPIO | ขาทั่วไปสำหรับ Input/Output |
| ADC | แปลงสัญญาณ Analog เป็น Digital |
| PWM | จำลอง Analog ด้วย Digital |
| I2C | มาตรฐานการสื่อสารอนุกรม |
| UART | สื่อสารกับคอมพิวเตอร์ |
| SPI | มาตรฐานการสื่อสารแบบอนุกรมเร็ว |

## ขั้นตอนถัดไป

```
🔰 ผู้เริ่มต้น → [GPIO Guide](./gpio-guide.md)
   ↓
🔰 วงจรพื้นฐาน → [Circuit Basics](./circuit-basics.md)
   ↓
🌡️ เซ็นเซอร์ → [DHT11](../02-sensors/dht11-sensor.md)
```

---

**อัปเดตล่าสุด:** 28 มีนาคม 2569
