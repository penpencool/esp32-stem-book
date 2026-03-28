# 📖 บทที่ 6: LDR + OLED — วัดแสงและแสดงผลบนจอ

> 💡 **หมายเหตุ:** LDR (Light Dependent Resistor) คือตัวต้านทานที่เปลี่ยนค่าตามแสง ส่วน OLED คือจอแสดงผลขนาดเล็กที่ใช้พลังงานน้อยมาก การรวมกันของทั้งสองจะทำให้เราสร้าง "เครื่องวัดความสว่าง" ได้ในราคาไม่ถึง 100 บาท!

---

## 🎯 สิ่งที่จะเรียนรู้

ในบทนี้ เราจะได้เรียนรู้:

- [ ] LDR (Light Dependent Resistor) คืออะไร และทำงานอย่างไร
- [ ] ความแตกต่างระหว่าง Analog และ Digital
- [ ] OLED 0.96" I2C คืออะไร และใช้งานยังไง
- [ ] วิธีต่อ LDR และ OLED กับ ESP32-C3
- [ ] วิธีใช้ AI สร้าง UI บน OLED
- [ ] ปฏิบัติ: ทำเครื่องวัดความสว่าง (Lux Meter)

---

## 📖 บทนำ

เคยสังเกตมั้ยครับว่า เมื่อเราเดินเข้าห้องมืดๆ จากที่แจ่มจ้า เราจะรู้สึกว่าตาเราต้องปรับตัวสักพักก่อนจึงจะมองเห็นได้ชัด? นั่นเป็นเพราะตาของเราก็เป็นเหมือน "เซ็นเซอร์วัดแสง" ที่ปรับความไวอัตโนมัตินั่นเอง! 👁️✨

วันนี้เราจะมาสร้างอุปกรณ์ที่คล้ายกัน — **เครื่องวัดความสว่าง (Lux Meter)** ที่วัดได้ว่าแสงรอบข้างเรามีความสว่างมากน้อยแค่ไหน พร้อมแสดงผลบนจอ OLED สีสันสดใส ให้เราเห็นค่าได้ทันทีโดยไม่ต้องเสียบสาย USB ตลอดเวลา!

ไม่ว่าจะเป็นการวัดแสงในห้องเรียน วัดแสงสปอร์ตไลท์ เช็คว่าต้นไม้ได้รับแสงพอมั้ย หรือแม้แต่ทำ Smart Lighting ที่ปรับไฟตามแสงธรรมชาติ เครื่องมือนี้ก็ทำได้หมดเลย! 🌟

---

## 🔧 อุปกรณ์ที่ใช้

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| LDR (GL5528 หรือเทียบเท่า) | 1 ตัว | ตัวต้านทานไวแสง |
| Resistor 10KΩ | 1 ตัว | ตัวต้านทาน Pull-down |
| OLED 0.96" I2C | 1 จอ | จอ SSD1306 สีฟ้า/เหลือง |
| Breadboard | 1 อัน | สำหรับต่อวงจร |
| สายจัมเปอร์ | จำนวนเท่าที่ต้องการ | ผู้หญิง-ผู้ชาย |

---

## 💻 เนื้อหา

### 🔹 LDR (Light Dependent Resistor) คืออะไร?

LDR หรือ **Light Dependent Resistor** คือตัวต้านทานที่ค่าความต้านทานเปลี่ยนไปตามความเข้มแสงที่ตกกระทบ มันเป็นอุปกรณ์ที่เรียบง่ายมากแต่มีประโยชน์มหาศาล!

**LDR หน้าตายังไง?**

```
LDR ภายนอก (Top View):
┌─────────────────┐
│  ╭───────────╮  │
│  │  ░░░░░░░░ │  │  ← หน้ากากรับแสง (สีเทา/เงิน)
│  │  ░░ LDR ░ │  │
│  │  ░░░░░░░░ │  │
│  ╰───────────╯  │
│  │  │      │  │  ← ขาออก 2 ขา
└──┴──────────┴──┘

LDR ภาพข้าง (Side View):
     ┌──────┐
   ──┤      ├───  ขาทั้งสองข้าง
     │ ░░░░ │
     │ LDR  │
     │ ░░░░ │
     └──────┘
        ↓
   ตัวต้านทานแบบไวแสง
```

**LDR มีขากี่ขา?**
LDR มีขา 2 ขาเหมือน Resistor ธรรมดา ไม่มีขา + และ - (ไม่ต้องสนใจขั้ว) สามารถพลิกข้างใช้ได้เลย!

**หลักการทำงานของ LDR:**

```
เมื่อแสงสว่างมาก (เช่น แดดจ้า)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
ค่าความต้านทาน: ต่ำมาก (~100-1KΩ)
กระแสไฟฟ้า: ไหลได้มาก
→ ESP32 อ่านค่าได้สูง (ใกล้ 4095)

เมื่อแสงมืด (ห้องมืด/มีเงา)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
ค่าความต้านทาน: สูงมาก (~1-10MΩ)
กระแสไฟฟ้า: ไหลได้น้อย
→ ESP32 อ่านค่าได้ต่ำ (ใกล้ 0)
```

> 💡 **เคล็ดลับ:** LDR ยอดนิยมคือ GL5528 ซึ่งมีค่าความต้านทานต่างกันมากระหว่างมืด-สว่าง ทำให้วัดแสงได้ไกลมาก!

**LDR ข้อมูลสำคัญ:**

| คุณสมบัติ | ค่า |
|-----------|-----|
| ชื่อรุ่น | GL5528 (ที่นิยมใช้) |
| ความต้านทานตอนมืด | 1-10 MΩ |
| ความต้านทานตอนสว่าง | 100-500 Ω |
| Peak Sensitivity Wavelength | 540 nm (เขียว) |
| Power Rating | 100 mW |
| ราคา | 3-10 บาท |

---

### 🔹 Analog vs Digital — อ่านค่ายังไง

นี่คือความรู้พื้นฐานที่สำคัญมากๆ เลยครับ! Analog และ Digital เป็น 2 วิธีหลักในการอ่านค่าจากโลกจริงเข้าสู่ Microcontroller

**Digital Signal (สัญญาณดิจิทัล):**

ลองนึกภาพสวิตช์ไฟในบ้านนะครับ มันมีได้แค่ 2 สถานะ: เปิด หรือ ปิด ไม่มีตรงกลาง!

```
Digital Signal:
        HIGH (1)
        3.3V ───┐
                │
                │
        LOW (0) │
        0V ────┘
        ───────────────→ เวลา

สถานะ:  0  0  0  1  1  1  0  0  1  1
ข้อมูล:  ปิด ปิด ปิด เปิด เปิด เปิด ปิด ปิด เปิด เปิด
```

Digital มีค่าได้แค่ 2 ค่า: **0 (LOW/ปิด)** หรือ **1 (HIGH/เปิด)** เหมาะกับอ่านสถานะที่เป็น "มี/ไม่มี" เช่น ปุ่มกด, สวิตช์, LED เปิด/ปิด

**Analog Signal (สัญญาณอะนาล็อก):**

ลองนึกภาพหลอดไฟที่หรี่ได้นะครับ ไม่ใช่แค่เปิด-ปิด แต่สามารถเปิด 10%, 50%, 75% ได้ มันมีค่าได้หลายระดับมาก!

```
Analog Signal:
        3.3V ────────────────────────────
        3.0V ───────────┐
        2.5V ─────┐     │
        2.0V ─┐  │     │    ┌──
        1.5V ─┼──┼──┐  │    │  ┌─
        1.0V ─┼──┼──┼──┐ │ ┌──┼──┼──
        0.5V ─┼──┼──┼──┼─┤──┼──┼──┼──
        0.0V ─┴──┴──┴──┴─┴──┴──┴──┴────
        ─────────────────────────────────→ เวลา

ค่า:    0   100  500  1000  2500  3500  4095
```

ESP32-C3 มี **ADC (Analog-to-Digital Converter)** ที่สามารถแปลงสัญญาณอะนาล็อก (0-3.3V) ให้เป็นค่าดิจิทัล (0-4095) ได้เลย!

> 💡 **เคล็ดลับ:** ESP32 มี ADC ความละเอียด 12 bits ซึ่งแปลงได้ 2^12 = 4096 ระดับ (0-4095) ยิ่งค่าสูง = ยิ่งแรงดันสูง = ยิ่งแสงสว่าง!

**วิธีอ่านค่า Analog จาก LDR:**

เนื่องจาก LDR เปลี่ยนค่าความต้านทานต่อเนื่อง (ไม่ใช่แค่ 0/1) เราจึงต้องอ่านค่าแบบ Analog:

```cpp
// อ่านค่า Analog จาก GPIO 0
int lightValue = analogRead(GPIO_NUM_0);  // ค่า 0-4095

// แปลงค่าเป็นเปอร์เซ็นต์
int percent = map(lightValue, 0, 4095, 0, 100);
```

**วงจร Voltage Divider (สำคัญมาก!):**

ถ้าเราต่อ LDR ตรงๆ เข้ากับ ESP32 ไม่ได้นะครับ เพราะ ESP32 อ่านแรงดันไฟฟ้า (Voltage) ไม่ใช่ความต้านทาน เราต้องแปลงค่าความต้านทานให้เป็นแรงดันก่อน โดยใช้วงจรที่เรียกว่า **Voltage Divider**:

```
Voltage Divider Circuit:
         3.3V
           │
         ┌─┴─┐
    LDR  │   │  10KΩ Resistor
         │   │
         └───┼───┐
             │   │
             │   │  (ไป GPIO 0 - Analog Input)
             │   │
            ───┴───
             GND
```

**สูตร Voltage Divider:**
```
Vout = Vin × (R2 / (R1 + R2))

โดยที่:
- Vin = 3.3V (ไฟเลี้ยง)
- R1 = ค่า LDR (เปลี่ยนตามแสง)
- R2 = 10KΩ Resistor (คงที่)
- Vout = แรงดันที่ไป Analog Input
```

```
เมื่อแสงสว่าง (LDR = 1KΩ):
Vout = 3.3 × (10000 / (1000 + 10000)) = 3.0V → ADC อ่านได้ ~3727

เมื่อแสงมืด (LDR = 1MΩ):
Vout = 3.3 × (10000 / (1000000 + 10000)) ≈ 0.03V → ADC อ่านได้ ~30
```

> ⚠️ **คำเตือน:** ใช้ Resistor 10KΩ เสมอนะครับ! ถ้าใช้ค่าต่ำเกิน (เช่น 100Ω) จะมีกระแสไหลมากเกินไป ทำให้ LDR ร้อนและเสียหาย ถ้าใช้ค่าสูงเกินไป (เช่น 1MΩ) สัญญาณจะอ่อนมากจนอ่านค่าไม่ได้

---

### 🔹 OLED 0.96" I2C คืออะไร?

OLED ย่อมาจาก **Organic Light-Emitting Diode** ซึ่งเป็นจอแสดงผลที่แต่ละจุด (pixel) สามารถเปล่งแสงได้เอง ไม่ต้องมี backlight ทำให้จอมีความคมชัดสูง สีดำจะดำสนิท (เพราะปิด pixel เลย) และใช้พลังงานน้อยมาก!

**OLED 0.96" มีขนาดเท่าไหร่?**

จอ 0.96 นิ้วนั้นมีขนาดประมาณ 2.5 × 1.4 เซนติเมตร มีพิกเซลทั้งหมด **128 × 64 = 8,192 จุด** ซึ่งเยอะพอสำหรับแสดงตัวอักษร กราฟ และรูปภาพง่ายๆ ได้เลย!

```
OLED 0.96" I2C Pinout:
┌─────────────────────────┐
│      OLED 0.96"         │
│  ┌───────────────────┐  │
│  │                   │  │
│  │   128 x 64 pixels │  │  ← จอสีฟ้าหรือเหลือง-ฟ้า
│  │                   │  │
│  │                   │  │
│  └───────────────────┘  │
│                         │
│  VCC  GND  SCL  SDA    │
│   │    │    │    │      │
└───┴────┴────┴────┴──────┘
```

**OLED กับ I2C Protocol:**

OLED 0.96" ที่นิยมใช้สื่อสารผ่าน **I2C (Inter-Integrated Circuit)** ซึ่งเป็น protocol ที่ใช้สายเพียง 2 เส้น!

```
I2C สื่อสารด้วย 2 สาย:
━━━━━━━━━━━━━━━

SCL (Serial Clock):
▀▀▀_▀▀▀_▀▀▀_▀▀▀_▀▀▀_▀▀▀_▀▀▀_▀▀▀  → ส่งสัญญาณนาฬิกา
SDA (Serial Data):
▀▀▀▄▄▄▀▀▀▄▄▄▄▀▀▀▄▄▀▀▄▄▄▄▀▀▀  → ส่งข้อมูลจริง

จุดเด่นของ I2C:
✅ ใช้สายเพียง 2 เส้น (SDA + SCL)
✅ ต่ออุปกรณ์ได้หลายตัวบนสายเดียวกัน
✅ มี Address กำหนดแต่ละอุปกรณ์
✅ ใช้งานง่าย มี Library พร้อม
```

> 💡 **เคล็ดลับ:** OLED 0.96" I2C ส่วนใหญ่มี Address เป็น `0x3C` (ฐานสิบหก) ซึ่งเป็นค่าเริ่มต้น แต่บางตัวอาจเป็น `0x3D` ถ้าใช้ไม่ได้ลองเปลี่ยนดูนะครับ

**OLED vs LCD — ต่างกันยังไง?**

| คุณสมบัติ | OLED | LCD |
|-----------|------|-----|
| การแสดงสีดำ | ดำสนิท (ปิด pixel) | มีแสง backlight รั่ว |
| ความสว่าง | สูงกว่า | ต่ำกว่า |
| การใช้พลังงาน | ต่ำมาก (ยิ่งดำยิ่งประหยัด) | คงที่ (backlight ติดเสมอ) |
| ราคา | ถูกกว่า | แพงกว่า |
| ขนาดพิกเซล | 128×64 สำหรับ 0.96" | หลากหลาย |
| สี | มักเป็นฟ้าหรือเหลือง-ฟ้า | หลากหลาย |

---

### 🔹 วิธีต่อ LDR + OLED กับ ESP32-C3

มาถึงขั้นตอนที่สำคัญที่สุดแล้ว — การต่อวงจร! ต้องทำอย่างระมัดระวังนะครับ

**วงจรที่ 1: LDR (Voltage Divider)**

```
LDR Circuit:
       3.3V (ESP32)
          │
      ┌───┴───┐
      │  LDR  │  ← ขา 1
      │       │
      └───┬───┘
          │  ← จุดต่อกลาง (ไป GPIO 0)
      ┌───┴───┐
      │ 10KΩ  │  ← Resistor Pull-down
      │       │
      └───┬───┘
          │
         GND
```

**วงจรที่ 2: OLED I2C**

```
OLED I2C Circuit:
       ESP32-C3          OLED 0.96" I2C
       ━━━━━━━━━          ━━━━━━━━━━━━━━
       GPIO 0 (SDA) ──── SDA
       GPIO 1 (SCL) ──── SCL
       3.3V          ──── VCC
       GND           ──── GND
```

**รายละเอียดการต่อทุกขา:**

```
ESP32-C3                    LDR + OLED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3.3V   ──────────────────── OLED VCC
GND    ──────────────────── OLED GND
        ──────────────────── LDR → 10KΩ → GND
GPIO 2 (ADC) ──────────────── LDR Junction
GPIO 0 (SDA) ──────────────── OLED SDA
GPIO 1 (SCL) ──────────────── OLED SCL
```

> ⚠️ **หมายเหตุด้าน GPIO:** บน ESP32-C3 มี GPIO บางตัวที่ใช้สำหรับ SPI Flash ภายใน (GPIO 6-11) และ GPIO 0 (BOOT button) ควรหลีกเลี่ยงใช้ GPIO เหล่านี้สำหรับ I/O ทั่วไป! บทนี้ใช้ GPIO 0 (SDA), GPIO 1 (SCL), GPIO 2 (ADC) ซึ่งปลอดภัยบน ESP32-C3 ทั่วไป

> ⚠️ **คำเตือน:** 
> 1. OLED ต้องต่อไฟ 3.3V หรือ 5V (ดูที่ตัวจอ) ถ้าต่อผิดอาจเสียหาย!
> 2. I2C ต้องต่อ SDA และ SCL ให้ถูกขา ถ้าผิดจอจะไม่แสดงผล!
> 3. ตรวจสอบ Address ของ OLED ก่อนใช้ (มักเป็น 0x3C)

---

### 🔹 ใช้ AI สร้าง UI บน OLED

ต่อไปเราจะมาสร้าง UI สวยๆ บนจอ OLED กันนะครับ โดยใช้ความช่วยเหลือของ AI! ยิ่งถ้าเราบอก AI อย่างชัดเจนว่าต้องการอะไร AI ก็จะสร้างโค้ดให้เราได้อย่างรวดเร็ว

**ก่อนอื่น — ติดตั้ง Library สำหรับ OLED:**

เพิ่มใน `platformio.ini`:

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino
monitor_speed = 115200

lib_deps = 
    adafruit/Adafruit GFX Library@^1.11.9
    adafruit/Adafruit SSD1306@^2.5.9
```

**สร้างไฟล์ UI Module — `ui.h`:**

```cpp
// ui.h - OLED UI Module Header
// ESP32-C3 STEM AI Coding

#ifndef UI_H
#define UI_H

#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// กำหนดขนาดจอ OLED
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT  64

// กำหนดขา I2C
#define OLED_SDA  0    // GPIO 0
#define OLED_SCL  1    // GPIO 1

// ฟังก์ชันสำหรับ UI ต่างๆ
void uiInit();                                          // เริ่มใช้งานจอ OLED
void uiClear();                                        // ล้างจอ
void uiDisplayLux(int luxValue, int rawValue);         // แสดงค่า Lux
void uiDisplayProgressBar(int percent);                // แสดง Progress Bar
void uiDisplayWelcome();                                // หน้าจอ Welcome
void uiDisplayStatus(String status);                    // แสดงสถานะ
void uiDisplayGraph(int history[], int size);          // แสดงกราฟประวัติ

// Helper functions
void drawSunIcon(int x, int y, int size);               // วาดรูปพระอาทิตย์
void drawLightLevel(int level);                         // แสดงระดับแสงเป็นภาพ
String getLightDescription(int lux);                   // อธิบายระดับแสง

#endif
```

**สร้างไฟล์ UI Module — `ui.cpp`:**

```cpp
// ui.cpp - OLED UI Module Implementation
// ESP32-C3 STEM AI Coding

#include "ui.h"

// สร้าง object สำหรับจอ OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// ฟังก์ชันเริ่มใช้งานจอ OLED
void uiInit() {
  Wire.begin(OLED_SDA, OLED_SCL);  // เริ่มใช้ I2C

  // ตรวจสอบว่าจอเชื่อมต่อได้มั้ย
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("[OLED] ERROR: SSD1306 allocation failed!");
    while(1);  // ถ้าไม่ได้ ให้หยุดทำงาน
  }

  display.clearDisplay();  // ล้างจอ
  display.setTextSize(1);   // ตั้งขนาดตัวอักษร
  display.setTextColor(SSD1306_WHITE);  // ตั้งสีขาว
  display.display();        // แสดงผล

  Serial.println("[OLED] Initialized successfully!");
  delay(500);
}

// ฟังก์ชันล้างจอ
void uiClear() {
  display.clearDisplay();
}

// ฟังก์ชันแสดงค่า Lux หลัก
void uiDisplayLux(int luxValue, int rawValue) {
  display.clearDisplay();

  // หัวข้อ
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("=== LUX METER ===");

  // แบ่งหน้าจอเป็น 2 ส่วน
  // ส่วนบน: ค่า Lux ขนาดใหญ่
  display.setTextSize(2);
  display.setCursor(0, 12);
  display.printf(" %d", luxValue);
  display.setTextSize(1);
  display.println(" lux");

  // ส่วนกลาง: Progress Bar
  int barX = 0;
  int barY = 32;
  int barWidth = 128;
  int barHeight = 8;
  
  // วาดกรอบ Progress Bar
  display.drawRect(barX, barY, barWidth, barHeight, SSD1306_WHITE);
  
  // วาด Progress (แปลง Lux เป็น % สำหรับแสง 0-1000 lux)
  int percent = constrain(map(luxValue, 0, 1000, 0, barWidth - 2), 0, barWidth - 2);
  display.fillRect(barX + 1, barY + 1, percent, barHeight - 2, SSD1306_WHITE);

  // ส่วนล่าง: ระดับแสง + Raw Value
  display.setTextSize(1);
  display.setCursor(0, 45);
  String desc = getLightDescription(luxValue);
  display.println(desc.c_str());

  display.setCursor(0, 55);
  display.printf("Raw: %d/4095", rawValue);

  display.display();
}

// ฟังก์ชันแสดง Welcome Screen
void uiDisplayWelcome() {
  display.clearDisplay();

  // วาดกรอบ
  display.drawRect(0, 0, 128, 64, SSD1306_WHITE);

  // ข้อความ Welcome
  display.setTextSize(1);
  display.setCursor(15, 10);
  display.println("ESP32-C3");

  display.setTextSize(2);
  display.setCursor(10, 25);
  display.println("LUX METER");

  display.setTextSize(1);
  display.setCursor(20, 48);
  display.println("by STEM AI");

  display.display();
  delay(2000);
}

// ฟังก์ชันแสดงสถานะ
void uiDisplayStatus(String status) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 28);
  display.println(status);
  display.display();
}

// ฟังก์ชันอธิบายระดับแสง
String getLightDescription(int lux) {
  if (lux < 10) return "🌙 มืดสนิท";
  else if (lux < 50) return "🪟 ห้องมืด";
  else if (lux < 200) return "🏠 แสงในห้อง";
  else if (lux < 500) return "💡 แสงสว่าง";
  else if (lux < 1000) return "☀️ แสงแดดจ้า";
  else if (lux < 5000) return "🌤️  แสงกลางวัน";
  else if (lux < 10000) return "🌞 แดดจัด";
  else return "⚡ แดดแรงสุด!";
}

// ฟังก์ชันแสดงกราฟประวัติ
void uiDisplayGraph(int history[], int size) {
  int graphX = 0;
  int graphY = 20;
  int graphW = 128;
  int graphH = 40;

  display.clearDisplay();
  
  // วาดกรอบกราฟ
  display.drawRect(graphX, graphY, graphW, graphH, SSD1306_WHITE);

  // หาค่าสูงสุด
  int maxVal = 0;
  for (int i = 0; i < size; i++) {
    if (history[i] > maxVal) maxVal = history[i];
  }
  if (maxVal == 0) maxVal = 1;  // ป้องกันหาร 0

  // วาดเส้นกราฟ
  for (int i = 0; i < size - 1; i++) {
    int x1 = map(i, 0, size - 1, graphX + 1, graphX + graphW - 1);
    int y1 = graphY + graphH - 1 - map(history[i], 0, maxVal, 1, graphH - 1);
    int x2 = map(i + 1, 0, size - 1, graphX + 1, graphX + graphW - 1);
    int y2 = graphY + graphH - 1 - map(history[i + 1], 0, maxVal, 1, graphH - 1);
    display.drawLine(x1, y1, x2, y2, SSD1306_WHITE);
  }

  display.display();
}
```

**สร้างไฟล์ LDR Module — `ldr.h` และ `ldr.cpp`:**

```cpp
// ldr.h - LDR Sensor Module Header
// ESP32-C3 STEM AI Coding

#ifndef LDR_H
#define LDR_H

#include <Arduino.h>

#define LDR_PIN 2  // GPIO 2 สำหรับ LDR (Analog Input)

// ฟังก์ชัน
void ldrInit();                              // เริ่มใช้งาน LDR
int ldrReadRaw();                            // อ่านค่าดิบ (0-4095)
float ldrReadVoltage();                      // อ่านค่าแรงดัน (0.0-3.3V)
float ldrReadLux();                         // อ่านค่า Lux (ความสว่าง)
float ldrReadPercent();                      // อ่านค่าเปอร์เซ็นต์

#endif
```

```cpp
// ldr.cpp - LDR Sensor Module Implementation
// ESP32-C3 STEM AI Coding

#include "ldr.h"

// ค่าคงที่สำหรับ LDR
#define LDR_RESISTOR 10000.0  // 10KΩ Resistor (Pull-down)

// ฟังก์ชันเริ่มใช้งาน LDR
void ldrInit() {
  pinMode(LDR_PIN, INPUT);  // ตั้งค่า GPIO เป็น Input
  Serial.println("[LDR] Initialized - Light Dependent Resistor");
}

// อ่านค่าดิบจาก ADC (0-4095)
int ldrReadRaw() {
  return analogRead(LDR_PIN);
}

// อ่านค่าแรงดัน (0.0 - 3.3V)
float ldrReadVoltage() {
  int raw = ldrReadRaw();
  return (raw / 4095.0) * 3.3;
}

// อ่านค่า Lux โดยประมาณ
// สูตรคำนวณจากค่า ADC ผ่าน Voltage Divider
float ldrReadLux() {
  int raw = ldrReadRaw();

  // แปลงค่า ADC เป็นความต้านทานของ LDR
  // Vout = Vin × (R2 / (R1 + R2))
  // แก้สมการหา R1 (LDR):
  // R1 = R2 × (Vin - Vout) / Vout
  float voltageOut = (raw / 4095.0) * 3.3;
  float ldrResistance;

  if (voltageOut < 0.01) {
    ldrResistance = 10000000.0;  // 10MΩ (มืดมาก)
  } else {
    ldrResistance = LDR_RESISTOR * (3.3 - voltageOut) / voltageOut;
  }

  // แปลงค่าความต้านทานเป็น Lux (โดยประมาณ)
  // ใช้สูตร log: Lux = 500 / (R_LDR / 1000)
  // (ค่านี้เป็นค่าประมาณ ไม่ใช่ค่าที่แม่นยำ 100%)
  float lux = 500.0 / (ldrResistance / 1000.0);
  
  return constrain(lux, 0, 10000);  // จำกัดค่า 0-10000 Lux
}

// อ่านค่าเป็นเปอร์เซ็นต์ (0-100%)
float ldrReadPercent() {
  int raw = ldrReadRaw();
  return (raw / 4095.0) * 100.0;
}
```

**ไฟล์หลัก `src/main.cpp`:**

```cpp
// main.cpp - Lux Meter with LDR + OLED
// ESP32-C3 STEM AI Coding - Chapter 06
// เครื่องวัดความสว่างด้วย LDR และแสดงผลบนจอ OLED

#include <Arduino.h>
#include "ldr.h"
#include "ui.h"

#define UPDATE_INTERVAL 500  // อัปเดตทุก 500ms

// ประวัติการอ่านค่า (สำหรับกราฟ)
const int HISTORY_SIZE = 20;
int luxHistory[HISTORY_SIZE] = {0};
int historyIndex = 0;
int historyCount = 0;

unsigned long lastUpdate = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("╔════════════════════════════════════════╗");
  Serial.println("║    ESP32-C3 LUX METER 🌟               ║");
  Serial.println("║    LDR + OLED 0.96\" I2C               ║");
  Serial.println("╚════════════════════════════════════════╝");

  // เริ่มใช้งาน LDR และ OLED
  ldrInit();
  uiInit();

  // แสดง Welcome Screen
  uiDisplayWelcome();

  Serial.println("[MAIN] Lux Meter Ready!");
}

void loop() {
  unsigned long currentTime = millis();

  // อัปเดตทุก UPDATE_INTERVAL ms
  if (currentTime - lastUpdate >= UPDATE_INTERVAL) {
    // อ่านค่าจาก LDR
    int rawValue = ldrReadRaw();
    float voltage = ldrReadVoltage();
    float lux = ldrReadLux();
    float percent = ldrReadPercent();

    // เก็บประวัติ
    luxHistory[historyIndex] = (int)lux;
    historyIndex = (historyIndex + 1) % HISTORY_SIZE;
    if (historyCount < HISTORY_SIZE) historyCount++;

    // แสดงผลบน OLED
    uiDisplayLux((int)lux, rawValue);

    // Debug ผ่าน Serial
    Serial.printf("[LUX] Raw: %d | Voltage: %.2fV | Lux: %.1f | Percent: %.1f%%\n",
                  rawValue, voltage, lux, percent);
    Serial.printf("[LUX] Description: %s\n", getLightDescription((int)lux).c_str());

    lastUpdate = currentTime;
  }

  // กดปุ่ม BOOT เพื่อแสดงกราฟ (ถ้าต้องการ)
  // หรือเพิ่มฟังก์ชันอื่นๆ ตามต้องการ
}
```

---

## 🔨 ปฏิบัติ: ทำเครื่องวัดความสว่าง (Lux Meter)

ในการปฏิบัตินี้เราจะสร้าง **Lux Meter สมบูรณ์แบบ** ที่วัดความสว่างได้จริงและแสดงผลบนจอ OLED พร้อมฟีเจอร์เพิ่มเติมมากมาย! 🌟🖥️

### 📋 สิ่งที่ต้องเตรียม

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| LDR (GL5528) | 1 ตัว | ตัวต้านทานไวแสง |
| Resistor 10KΩ | 1 ตัว | ตัวต้านทาน Pull-down |
| OLED 0.96" I2C | 1 จอ | จอ SSD1306 |
| LED สีเขียว | 1 หลอด | แสดงสถานะ |
| Resistor 220Ω | 1 ตัว | สำหรับ LED สถานะ |
| Breadboard | 1 อัน | สำหรับต่อวงจร |
| สายจัมเปอร์ | จำนวนเท่าที่ต้องการ | ผู้หญิง-ผู้ชาย |

### 📋 ขั้นตอนที่ 1: ต่อวงจร

```
วงจรที่ 1: LDR Voltage Divider
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3.3V ──┬── LDR ──┬── GPIO 2 (ADC)
       │         │
       └── 10KΩ ─┴── GND

วงจรที่ 2: OLED I2C
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3.3V ──── VCC (OLED)
GND  ──── GND (OLED)
GPIO 0 ──── SDA (OLED)
GPIO 1 ──── SCL (OLED)

วงจรที่ 3: Status LED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GPIO 3 ──── 220Ω ──── LED (+) ──── GND
```

> ⚠️ **คำเตือน:** ตรวจสอบว่าจอ OLED รองรับ 3.3V หรือต้องใช้ 5V ถ้าใช้ 3.3V ต่อเข้า 3.3V ถ้าใช้ 5V ต่อเข้า 5V และต้องใช้ Level Shifter ถ้าจอต้องการ 5V I2C แต่ ESP32 ใช้ 3.3V!

### 📋 ขั้นตอนที่ 2: สร้างโปรเจกต์ใหม่บน PlatformIO

1. สร้างโปรเจกต์ใหม่ชื่อ `ch06_lux_meter`
2. เพิ่ม Library ใน `platformio.ini`:

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino
monitor_speed = 115200

lib_deps = 
    adafruit/Adafruit GFX Library@^1.11.9
    adafruit/Adafruit SSD1306@^2.5.9
```

### 📋 ขั้นตอนที่ 3: อัปโหลดโค้ด

1. สร้างไฟล์ `src/ldr.h`, `src/ldr.cpp`, `src/ui.h`, `src/ui.cpp` ตามที่เขียนไว้ข้างบน
2. แก้ไข `src/main.cpp` ตามที่เขียนไว้
3. กด `Ctrl + Alt + U` เพื่ออัปโหลด
4. เปิด Serial Monitor ที่ 115200 baud

### 📋 ขั้นตอนที่ 4: ทดสอบ

1. เมื่ออัปโหลดเสร็จ จอ OLED จะแสดง Welcome Screen 2 วินาที
2. จากนั้นจะแสดงค่า Lux ปัจจุบัน พร้อม Progress Bar
3. ลองเปลี่ยนแสงรอบ LDR โดย:
   - ฉายไฟฉายเข้าใกล้ LDR → ค่า Lux จะเพิ่มขึ้น
   - ปิดไฟห้องให้มืด → ค่า Lux จะลดลง
   - คลุม LDR ด้วยมือ → ค่า Lux จะต่ำมาก

```
Serial Monitor Output:
[LUX] Raw: 2048 | Voltage: 1.65V | Lux: 250.0 | Percent: 50.0%
[LUX] Description: 💡 แสงสว่าง

[LUX] Raw: 3500 | Voltage: 2.82V | Lux: 850.0 | Percent: 85.5%
[LUX] Description: ☀️ แสงแดดจ้า
```

### 📋 ขั้นตอนที่ 5: ปรับแต่งเพิ่มเติม

ลองให้ AI ช่วยปรับแต่ง Lux Meter ให้ดียิ่งขึ้น!

```
Prompt สำหรับ AI:
"ช่วยปรับปรุงโค้ด Lux Meter ให้มีฟีเจอร์เพิ่มเติม:
1. เพิ่มกราฟแสดงประวัติความสว่างย้อนหลัง 20 ค่า
2. เพิ่ม LED แสดงสถานะ (เขียว=แสงปกติ, แดง=แสงมากเกินไป)
3. เพิ่มปุ่มกดเพื่อเปลี่ยนโหมด (แสดง Lux / แสดง % / แสดงกราฟ)
4. บันทึกค่าต่ำสุด-สูงสุดไว้ดู
ใช้ PlatformIO Arduino Framework สำหรับ ESP32-C3"
```

---

## 📝 แบบฝึก

### แบบฝึกที่ 1: สร้าง Smart Light Controller
ใช้ LDR ควบคุม LED ให้ติดเมื่อแสงน้อย (เหมือนไฟกลางคืน):

```cpp
// เพิ่มใน loop():
if (lux < 50) {
  digitalWrite(LED_STATUS, HIGH);  // LED ติดเมื่อมืด
} else {
  digitalWrite(LED_STATUS, LOW);   // LED ดับเมื่อสว่าง
}
```

### แบบฝึกที่ 2: วัดแสงหลายจุด
ต่อ LDR หลายตัววัดแสงในห้องหลายจุด แล้วเปรียบเทียบ:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด PlatformIO ESP32-C3 ที่วัดแสงจาก LDR 4 ตัว
ต่อที่ GPIO 0, 1, 2, 3
แสดงผลเปรียบเทียบ 4 จุดบน OLED 128x64"
```

### แบบฝึกที่ 3: เปลี่ยนเป็น VEML7700
VEML7700 คือเซ็นเซอร์วัดแสงแบบ Digital (I2C) ที่แม่นยำกว่า LDR มาก:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด PlatformIO สำหรับ ESP32-C3 ที่ใช้ VEML7700
แทน LDR สำหรับวัดความสว่าง (Lux) ผ่าน I2C
แสดงผลบน OLED 0.96 I2C
ต่อ SDA=GPIO0, SCL=GPIO1"
```

### แบบฝึกที่ 4: ส่งข้อมูลขึ้น Cloud
ส่งค่า Lux ขึ้น IoT Platform เช่น Blynk หรือ ThingSpeak:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด ESP32-C3 ที่วัดค่า Lux จาก LDR
และส่งข้อมูลขึ้น Blynk ทุก 10 วินาที
ใช้ WiFi บ้าน พร้อมแสดง Virtual Pin V0"
```

### แบบฝึกที่ 5: ทำ Solar Tracker
ใช้ LDR 2 ตัวเพื่อหาทิศทางที่แดดจัดที่สุด แล้วหมุน Servo Motor ไปทางนั้น:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด ESP32-C3 Solar Tracker ที่:
- ใช้ LDR 2 ตัวเปรียบเทียบแสงซ้าย-ขวา
- หมุน Servo Motor ไปทางที่แดดจัดที่สุด
- แสดงทิศทางและค่า Lux บน OLED"
```

---

## 🤔 คำถามท้ายบท

### คำถามที่ 1: ทำไมต้องใช้ Voltage Divider?
**ถาม:** ทำไมไม่ต่อ LDR ตรงๆ เข้ากับ ESP32 เลย? ทำไมต้องมี Resistor 10KΩ ด้วย?

**ตอบ:** เพราะ ESP32 อ่านค่าเป็น **แรงดันไฟฟ้า (Voltage)** ไม่ใช่ค่าความต้านทาน LDR เปลี่ยนค่าความต้านทาน (R) ได้ แต่เราต้องแปลงให้เป็นแรงดันก่อน วงจร Voltage Divider จึงทำหน้าที่ "แปลง" ค่าความต้านทานที่เปลี่ยนแปลงได้ตลอดเวลาให้เป็นแรงดันที่เปลี่ยนแปลงตาม ยิ่ง LDR มีความต้านทานต่ำ (แสงเยอะ) ยิ่ง Vout สูง ยิ่ง LDR มีความต้านทานสูง (มืด) ยิ่ง Vout ต่ำ ถ้าไม่มี Resistor จะเกิดปัญหา "ลัดวงจร" และอาจทำให้ ESP32 เสียหายได้ครับ

---

### คำถามที่ 2: I2C คืออะไร ทำไมต้องใช้?
**ถาม:** I2C ต่างจากการต่อสายธรรมดายังไง? ทำไมไม่ต่อแบบ Digital หรือ Analog ธรรมดา?

**ตอบ:** I2C (Inter-Integrated Circuit) เป็น **protocol การสื่อสาร** ที่ใช้สายเพียง 2 เส้น (SDA สำหรับข้อมูล และ SCL สำหรับสัญญาณนาฬิกา) สามารถต่ออุปกรณ์ได้หลายตัวบนสายเดียวกัน (แต่ละตัวมี Address ต่างกัน) ซึ่งประหยัดขา GPIO มาก ถ้าเทียบกับ SPI ที่ต้องใช้ 4 เส้น หรือ Serial ที่ต้องต่อ TX/RX สำหรับ OLED ที่ต้องส่งข้อมูลจำนวนมาก (พิกเซล 128×64 = 8,192 จุด) I2C เป็นทางเลือกที่ดีเพราะใช้สายน้อยและมี Library พร้อมใช้ง่าย

---

### คำถามที่ 3: Lux คืออะไร?
**ถาม:** หน่วย Lux ที่วัดได้นั้นคืออะไร? มันต่างจาก Watt หรือ Lumen ยังไง?

**ตอบ:** **Lux (lx)** คือหน่วยวัด **ความสว่างที่ตกกระทบพื้นที่** หรือ Illuminance โดย 1 Lux = 1 Lumen ต่อตารางเมตร ส่วน **Lumen (lm)** คือหน่วยวัด **ปริมาณแสงทั้งหมดที่แหล่งกำเนิดปล่อยออกมา** ส่วน **Watt (W)** คือหน่วยวัด **กำลังไฟฟ้า** ไม่เกี่ยวกับความสว่างโดยตรง

ตัวอย่างความสว่างเป็น Lux:
- พระอาทิตย์เที่ยงคืน: 0.0001 lux
- แสงดาวในคืนไม่มีพระจันทร์: 0.002 lux
- แสงพระจันทร์เต็มดวง: 0.27 lux
- แสงในห้องนั่งเล่น: 50-100 lux
- แสงในสำนักงาน: 300-500 lux
- แสงแดดจ้า: 10,000-100,000 lux

> 💡 **เคล็ดลับ:** ค่า Lux ที่ LDR วัดได้ในโค้ดของเราเป็นค่าประมาณ (approximate) เพราะใช้สูตรง่ายๆ ไม่ใช่ค่าที่แม่นยำ 100% ถ้าต้องการความแม่นยำสูง ควรใช้เซ็นเซอร์วัดแสงแบบ Digital เช่น BH1750 หรือ VEML7700 ที่ให้ค่า Lux ที่แม่นยำกว่า

---

## 📚 สรุป

ในบทนี้เราได้เรียนรู้ว่า:

✅ **LDR (Light Dependent Resistor)** คือตัวต้านทานที่ค่าเปลี่ยนตามแสง เมื่อแสงมากความต้านทานต่ำ เมื่อแสงน้อยความต้านทานสูง ต้องใช้ Voltage Divider เพื่อแปลงค่าให้เป็นแรงดันก่อนอ่านด้วย ADC

✅ **Analog vs Digital** — Analog อ่านค่าได้หลายระดับ (0-4095) เหมาะกับเซ็นเซอร์ที่ให้ค่าต่อเนื่อง ส่วน Digital อ่านได้แค่ 0/1 เหมาะกับสถานะที่เป็น "มี/ไม่มี"

✅ **OLED 0.96" I2C** คือจอแสดงผลขนาดเล็กที่ใช้พลังงานน้อย สื่อสารผ่าน I2C protocol ด้วยสายเพียง 2 เส้น (SDA + SCL) มี Address ปกติคือ `0x3C`

✅ การต่อ LDR ต้องใช้ **Voltage Divider** กับ Resistor 10KΩ และต่อเข้ากับ GPIO ที่เป็น Analog (GPIO 0-5 บน ESP32-C3)

✅ **AI สามารถช่วยสร้าง UI บน OLED** ได้ โดยใช้ Adafruit GFX Library ซึ่งรองรับการวาดรูป ตัวอักษร กราฟ และสิ่งต่างๆ ได้หลากหลาย

✅ สามารถสร้าง **Lux Meter** ที่ใช้งานได้จริงโดยใช้ LDR และ OLED ร่วมกัน เหมาะสำหรับวัดแสงในห้องเรียน สวน หรือที่ต่างๆ ได้

> 🔮 **บทต่อไป:** ในบทถัดไปเราจะมาเรียนรู้เรื่อง **Wi-Fi + Blynk** กัน! เราจะนำความรู้ที่เรียนมาทั้งหมด (DHT11, LDR, OLED) มาต่อ Wi-Fi และส่งข้อมูลขึ้น Internet ผ่าน Blynk เพื่อดูข้อมูลจากที่ไหนก็ได้ในโลก! 🌐📱

---

*📁 โค้ดตัวอย่าง: `/code/ch06_lux_meter/`*  
*🖼️ รูปประกอบ: `/images/ch06-ldr-oled-*.png`*
