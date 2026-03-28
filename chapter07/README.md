# 🎯 สิ่งที่จะเรียนรู้

ในบทนี้ เราจะได้เรียนรู้:

- [ ] Servo Motor ทำงานยังไง และสัญญาณ PWM คืออะไร
- [ ] วิธีต่อ Servo SG90 กับ ESP32-C3 อย่างถูกต้อง (แยก Power)
- [ ] ควบคุมมุมหมุนของ Servo ตั้งแต่ 0° ถึง 180°
- [ ] ปฏิบัติ: ควบคุม Servo ด้วย Potentiometer
- [ ] ปฏิบัติ: ทำเข็มขั้นบันไดอัตโนมัติ

---

## 📖 บทนำ

> "เคยสงสัยมั้ยเล่า ทำไมหุ่นยนต์ตัวเล็กๆ ถึงขยับแขนได้อย่างเป็นจังหวะ? ทำไมประตูอัตโนมัติถึงเปิด-ปิดเองได้? คำตอบอยู่ที่อุปกรณ์ตัวหนึ่งที่เรียกว่า **Servo Motor** นี่แหละ! 🔩"
>
> "Servo ถูกใช้ทั่วไปเลย — ตั้งแต่เครื่องบินบังคับ, หุ่นยนต์, กล้องวงจรปิด, และแม้แต่เครื่องปริ้นท์ 3D! ในบทนี้เราจะมาทำความรู้จัก Servo SG90 กัน แล้วเอามาทำโปรเจกต์สุดเจ๋งอย่าง 'เข็มขั้นบันไดอัตโนมัติ' ที่สาขึ้นลงได้เองเลย!"

---

## 🔧 อุปกรณ์ที่ใช้

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| Servo Motor SG90 | 1 ตัว | มุมหมุน 0°-180° |
| Potentiometer 10kΩ | 1 ตัว | ใช้ควบคุมมุม |
| Power Supply 5V (USB หรือ Adapter) | 1 ชุด | จ่ายไฟให้ Servo |
| สายจัมเปอร์ | หลายเส้น | ผู้นิรภัยแนะนำใช้สายสีแยก |
| Breadboard | 1 อัน | สำหรับต่อวงจร |
| LED สีเขียว | 2 ตัว | สำหรับโปรเจกต์ขั้นบันได |
| LED สีแดง | 1 ตัว | แสดงสถานะเตือน |
| Resistor 220Ω | 3 ตัว | ป้องกัน LED ขาด |
| Buzzer | 1 ตัว | แสดงเสียงเตือน |
| IR Motion Sensor (PIR HC-SR501) | 1 ตัว | ตรวจจับการเคลื่อนไหว |

---

## 💻 เนื้อหา

### 🔹 Servo Motor ทำงานยังไง? 🤔

#### 🧩 Servo คืออะไร?

**Servo Motor** หรือเรียกสั้นๆ ว่า "Servo" เป็นมอเตอร์พิเศษที่สามารถ **ควบคุมตำแหน่งมุม** ได้แม่นยำ ไม่เหมือนมอเตอร์ DC ที่หมุนไปเรื่อยๆ เมื่อจ่ายไฟ Servo จะหมุนไปที่มุมที่เราต้องการแล้วหยุดอยู่ตรงนั้น!

Servo ประกอบด้วย 3 ส่วนหลัก:

1. **มอเตอร์ DC** — ตัวหมุนจริงๆ
2. **ชุดเกียร์ (Gear Box)** — ลดความเร็วรอบเพิ่มแรงบิด (Torque)
3. **วงจรควบคุม (Control Circuit)** — เปรียบเสมือน "สมอง" ที่รับคำสั่ง

```
📌 จุดสำคัญ:
- Servo หมุนได้แค่ 0° ถึง 180° (ไม่ใช่ 360° เหมือนมอเตอร์ DC)
- Servo รู้ตำแหน่งของตัวเอง (มี Feedback)
- ต้องใช้สัญญาณพิเศษที่เรียกว่า PWM ควบคุม
```

#### 🎛️ สัญญาณ PWM คืออะไร?

**PWM** ย่อมาจาก **Pulse Width Modulation** หรือ "การมอดูเลตความกว้างพัลส์" — เป็นเทคนิคที่ใช้ส่งสัญญาณดิจิทัลเพื่อควบคุมอุปกรณ์แบบอะนาล็อก

วิธีการทำงานของ PWM ง่ายมาก: เราปิด-เปิดสัญญาณไฟฟ้าเร็วมากๆ ด้วยความถี่คงที่ (ประมาณ 50 ครั้งต่อวินาที หรือ 50 Hz สำหรับ Servo) แล้วเปลี่ยนแค่ **ความกว้างของ "สัญญาณ ON"** (เรียกว่า Duty Cycle)

```
    ON  ────────        ความกว้างพัลส์มาก  = มุมมาก (เช่น 180°)
         OFF
    ON  ───            ความกว้างพัลส์กลาง  = มุมกลาง (เช่น 90°)
         OFF
    ON  ──              ความกว้างพัลส์น้อย  = มุมน้อย (เช่น 0°)
         OFF
    ───────────────────► เวลา (Period = 20ms สำหรับ Servo)
```

สำหรับ Servo SG90:
- **ความถี่:** 50 Hz (Period = 20ms)
- **Pulse Width สำหรับ 0°:** ประมาณ 0.5ms (1ms ก็มีใช้)
- **Pulse Width สำหรับ 90°:** ประมาณ 1.5ms
- **Pulse Width สำหรับ 180°:** ประมาณ 2.5ms (2.0ms ก็มีใช้)

> 💡 **เคล็ดลับ:** Pulse Width ที่แม่นยำจะทำให้ Servo หมุนได้ละเอียดขึ้น! ถ้า Pulse Width ไม่ตรง Servo อาจสั่นหรือเอียงไม่ถึงมุมที่ต้องการ

### 🔹 วิธีต่อ Servo กับ ESP32-C3 (แยก Power) ⚠️

#### ⚠️ ทำไมต้องแยก Power?

นี่คือจุดที่หลายคนเจ็บปวดมากที่สุดเวลาใช้ Servo! 😭

Servo SG90 ต้องการ **กระแสไฟฟ้าสูงพอสมควร** โดยเฉพาะตอนเริ่มหมุน (Stall Current สูงถึง 650mA!) ถ้าเราจ่ายไฟจาก ESP32-C3 ทาง USB หรือ Pin ไฟเลี้ยงเพียงอย่างเดียว:

- ❌ USB อาจจ่ายไฟได้ไม่พอ → Servo กระตุก
- ❌ ถ้า Servo ดึงกระแสมากเกิน → **ESP32-C3 อาจพังได้!**
- ❌ ไฟลง (Voltage Drop) → ESP32 รีเซ็ตเอง

ดังนั้นเราต้อง **แยก Power Supply** — ให้ Servo ได้ไฟจากแหล่งจ่ายไฟของตัวเอง (เช่น USB 5V หรือ Adapter 5V) และใช้สัญญาณ PWM จาก ESP32-C3 ควบคุมเท่านั้น

```
┌─────────────────┐         ┌─────────────────┐
│   ESP32-C3      │         │  USB/Adapter    │
│                 │         │     5V          │
│  GPIO 2 ────────┼─────────┤► Servo Signal   │
│  GND ───────────┼─────────┤► Servo GND      │
└─────────────────┘         │  (แยกจ่ายไฟ)    │
                             └─────────────────┘
```

#### 🔌 สายของ Servo SG90

Servo SG90 มีสาย 3 เส้น สีมาตรฐาน:

| สีสาย | หน้าที่ | เชื่อมต่อกับ |
|-------|--------|-------------|
| **น้ำตาล (Brown)** | GND (Ground) | GND ของ ESP32 + GND ของ Power Supply |
| **แดง (Red)** | VCC (+5V) | Power Supply 5V (แยกจาก ESP32) |
| **สีส้ม (Orange)** | Signal (PWM) | GPIO ของ ESP32-C3 |

```
⚠️ คำเตือนสำคัญ:
- สายสีแดง (VCC) ของ Servo ต้องต่อกับ Power Supply 5V เท่านั้น!
- ห้ามต่อสายสีแดงเข้ากับ Pin 3.3V ของ ESP32-C3 เด็ดขาด
- GND ของ ESP32 และ Power Supply ต้องต่อร่วมกัน (Common Ground)
```

#### 🔧 วิธีต่อวงจร Servo (พื้นฐาน)

ให้เราดูรูปนี้ประกอบ:

```
    ESP32-C3                    Servo SG90
    ┌─────────┐              ┌──────────┐
    │       3V3│─────────────│ (ไม่ต่อ!) │
    │       GND│─────────────┤○ สีน้ำตาล  │ ← GND ร่วม
    │    GPIO2├──────────────│○ สีส้ม    │ ← PWM Signal
    │       5V │              │○ สีแดง    │ ← 5V Power Supply
    └─────────┘              └──────────┘
         │                        ▲
         │                        │
    ┌────┴────┐              ┌─────┴────┐
    │  USB    │              │ 5V USB   │
    │ (จ่าย   │              │ Adapter  │
    │  5V)    │              │ (จ่ายไฟ) │
    └─────────┘              └──────────┘
```

### 🔹 ควบคุมมุม Servo (0°-180°) 💻

ใน Arduino IDE เราสามารถใช้ **Library มาตรฐาน** `Servo.h` ที่มาพร้อมกับ Arduino IDE ได้เลย ไม่ต้องติดตั้งเพิ่ม!

#### หลักการทำงานของ Servo Library

```cpp
#include <Servo.h>  // เรียกใช้ไลบรารี Servo

Servo myServo;      // สร้างอ็อบเจ็กต์ Servo

void setup() {
  myServo.attach(GPIO_PIN);  // บอกว่า Servo ต่อที่ขา GPIO ไหน
  myServo.write(90);         // สั่งให้หมุนไปที่ 90 องศา
}

void loop() {
  // หมุนช้าๆ จาก 0° ไป 180°
  for (int angle = 0; angle <= 180; angle += 1) {
    myServo.write(angle);   // ส่งมุมไปที่ Servo
    delay(15);               // รอให้ Servo หมุนไปถึง
  }
  // แล้วหมุนกลับจาก 180° ไป 0°
  for (int angle = 180; angle >= 0; angle -= 1) {
    myServo.write(angle);
    delay(15);
  }
}
```

#### ทำไมต้อง `delay(15)` ถึง `delay(30)`?

Servo ต้องการ **เวลาในการหมุนไปถึงมุมเป้าหมาย** ถ้าเราส่งสัญญาณเร็วเกินไป Servo จะตามไม่ทัน! ค่า `delay(15)` ถึง `delay(30)` คือการให้เวลาพอให้ Servo หมุนไปทีละองศา

```
📌 การตั้งค่า Pulse Width ที่แม่นยำ:
    myServo.attach(GPIO, 1000, 2000);
    
    - 1000 = Pulse Width ต่ำสุด (μs) สำหรับ 0°
    - 2000 = Pulse Width สูงสุด (μs) สำหรับ 180°
    
    ค่าเริ่มต้นของ ESP32 Arduino คือ 544μs - 2400μs
    สำหรับ SG90 ควรใช้ 1000μs - 2000μs จะแม่นยำกว่า
```

### 🔹 Servo กับ ESP32-C3: เรื่อง Voltage Level ⚠️

นี่คือเรื่องที่ต้องระวังเป็นพิเศษ!

ESP32-C3 ทำงานที่ **3.3V Logic Level** แต่ Servo SG90 ต้องการ **Signal ในระดับ 3.3V - 5V** ซึ่งโดยปกติ 3.3V ก็พอใช้งานได้กับ SG90 แต่ถ้า Servo ไม่ยอมทำงานหรือทำงานไม่เสถียร เราอาจต้องใช้วงจร **Level Shifter** หรือ **Logic Level Converter**

```
📌 วิธีแก้ปัญหา Servo ไม่ทำงานกับ ESP32-C3:
1. ลองใช้ก่อน — SG90 ส่วนใหญ่ใช้ 3.3V PWM ได้
2. ถ้าไม่ได้ ใช้ Logic Level Converter (3.3V → 5V)
3. หรือใช้ Servo รุ่นที่รองรับ 3.3V Logic โดยตรง
4. ตรวจสอบว่า Power Supply จ่ายไฟได้เพียงพอ (อย่างน้อย 5V 1A)
```

---

## 🔨 ปฏิบัติ (พร้อมโค้ด)

### 🛠️ ปฏิบัติที่ 1: ควบคุม Servo ด้วย Potentiometer 🎚️

โปรเจกต์นี้เราจะใช้ **Potentiometer** (ตัวต้านทานปรับค่าได้) หมุนเพื่อควบคุมมุมของ Servo เหมือนกับหมุน Volume ในเครื่องเสียง! 🔊

#### ขั้นตอนที่ 1: ต่อวงจร

```
    ESP32-C3                    Servo SG90
    ┌─────────┐              ┌──────────┐
    │       GND├─────────────┤○ น้ำตาล   │ ← GND ร่วม
    │    GPIO2├──────────────│○ สีส้ม    │ ← PWM Signal
    └─────────┘              │○ แดง     │ ← 5V USB Adapter
         │                   └──────────┘
         │                        ▲
    ┌────┴────┐              ┌─────┴────┐
    │ USB 5V  │              │ 5V 1A+  │
    └─────────┘              └──────────┘

    Potentiometer 10kΩ:
    ┌────────────┐
    │  ○  ซ้าย   │ ← 3V3
    │  ○  กลาง   │ ← GPIO 0 (Analog Signal)
    │  ○  ขวา   │ ← GND
    └────────────┘
```

**สรุปการต่อสาย:**

| Servo SG90 | ESP32-C3 / Power |
|------------|-----------------|
| สายน้ำตาล (GND) | GND ร่วม (ESP32 + Power Supply) |
| สายแดง (VCC) | Power Supply 5V (แยก) |
| สายส้ม (Signal) | GPIO 2 |
| Potentiometer ซ้าย | 3V3 |
| Potentiometer กลาง | GPIO 0 |
| Potentiometer ขวา | GND |

> ⚠️ **สำคัญ:** ตรวจสอบให้แน่ใจว่า GND ของ ESP32, Servo Power Supply, และ Potentiometer ต่อร่วมกันทั้งหมด!

#### ขั้นตอนที่ 2: เขียนโค้ด

เปิด Arduino IDE แล้วพิมพ์โค้ดนี้:

```cpp
// ============================================
// บทที่ 7: ควบคุม Servo ด้วย Potentiometer
// ============================================
// ใช้ Potentiometer หมุนเพื่อควบคุมมุม Servo

#include <Servo.h>  // เรียกใช้ไลบรารี Servo

// ==== กำหนดขา Pin ====
#define SERVO_PIN    2   // Servo Signal → GPIO 2
#define POT_PIN      0   // Potentiometer → GPIO 0 (Analog ADC)

// ==== สร้างอ็อบเจ็กต์ Servo ====
Servo myServo;

// ==== ตัวแปร ====
int potValue = 0;       // ค่าที่อ่านได้จาก Potentiometer (0-4095 บน ESP32-C3)
int angle = 0;          // มุมที่จะสั่ง Servo (0-180°)

void setup() {
  Serial.begin(115200);           // เปิด Serial Monitor
  Serial.println("=== Servo + Potentiometer ===");

  myServo.attach(SERVO_PIN);      // ต่อ Servo ที่ GPIO 2

  // ตั้งค่า Pulse Width ที่แม่นยำสำหรับ SG90
  // (1000μs = 0°, 2000μs = 180°) ปกติใช้ค่าเริ่มต้นก็ได้
  // myServo.attach(SERVO_PIN, 1000, 2000);
}

void loop() {
  // อ่านค่าจาก Potentiometer (ADC ของ ESP32-C3 มี 12-bit = 0-4095)
  potValue = analogRead(POT_PIN);

  // แปลงค่า 0-4095 เป็นมุม 0-180°
  angle = map(potValue, 0, 4095, 0, 180);

  // สั่ง Servo ไปที่มุมที่คำนวณได้
  myServo.write(angle);

  // แสดงผลใน Serial Monitor
  Serial.print("Pot: ");
  Serial.print(potValue);
  Serial.print("  →  Angle: ");
  Serial.print(angle);
  Serial.println("°");

  delay(15);  // รอให้ Servo หมุนไปถึง (15ms ต่อ 1° โดยประมาณ)
}
```

#### ขั้นตอนที่ 3: อัปโหลดและทดสอบ

1. **เลือกบอร์ด:** Tools → Board → ESP32C3 Dev Module
2. **เลือก Port:** ที่ถูกต้อง
3. **กด Upload** 🚀
4. **เปิด Serial Monitor** ที่ 115200 baud
5. **หมุน Potentiometer** ไปทางซ้าย-ขวา แล้วดู Servo หมุนตาม!

> 💡 **เคล็ดลับ:** ถ้า Servo สั่นหรือส่งเสียงแปลกๆ แสดงว่า PWM Signal อาจไม่เสถียร ลองเช็คการต่อสาย GND หรือลองเปลี่ยนค่า `delay()` ให้มากขึ้นเป็น `delay(20)`

**ผลลัพธ์ที่คาดหวัง:** 🎉
- หมุน Potentiometer ไปทางซ้ายสุด → Servo อยู่ที่ 0°
- หมุนตรงกลาง → Servo อยู่ที่ 90°
- หมุนไปทางขวาสุด → Servo อยู่ที่ 180°

---

### 🛠️ ปฏิบัติที่ 2: ทำเข็มขั้นบันไดอัตโนมัติ 🏠

โปรเจกต์นี้สุดเจ๋งมาก! เราจะทำ **"เข็มขั้นบันไดอัตโนมัติ"** ที่เมื่อมีคนเดินผ่าน มันจะยกขึ้นให้เดินขึ้น แล้วค่อยๆ ลดลงหลังจากนั้น เหมือนบันไดเลื่อนในห้างสรรพสินค้าเลย! 🛗

#### 💡 ไอเดียเบื้องหลัง

เราจะใช้ **PIR Sensor (HC-SR501)** ตรวจจับการเคลื่อนไหว (คนเดินผ่าน) เมื่อตรวจพบ → สั่งให้ Servo หมุนขึ้นไปที่ 90° (เปิดทาง) และ LED เขียวติด หลังจากรอ 3 วินาที → Servo ค่อยๆ หมุนกลับลงมาที่ 0° (ปิด) และเปิด LED แดงแสดงว่าพร้อมรับคนถัดไป

#### ขั้นตอนที่ 1: ต่อวงจร

```
    ESP32-C3
    ┌──────────────────────────────────────────┐
    │  GND ──┬──► GND ร่วมทุกอุปกรณ์             │
    │  3V3  ─┴──► PIR Sensor (VCC)              │
    │  GPIO 4 ──► PIR Signal OUT                │
    │  GPIO 2 ──► Servo Signal (ส้ม)            │
    │  GPIO 6 ──► LED เขียว (ผ่าน R 220Ω)       │
    │  GPIO 7 ──► LED แดง (ผ่าน R 220Ω)         │
    └──────────────────────────────────────────┘

    Servo SG90:
    - น้ำตาล (GND)  → GND ร่วม
    - แดง (VCC)    → Power Supply 5V (แยก!)
    - ส้ม (Signal)  → GPIO 2
```

**สรุปการต่อสาย:**

| อุปกรณ์ | Pin บน ESP32-C3 |
|--------|----------------|
| Servo Signal | GPIO 2 |
| LED เขียว (ไฟเปิด) | GPIO 6 |
| LED แดง (รอ) | GPIO 7 |
| PIR Signal OUT | GPIO 4 |
| PIR VCC | 3V3 |
| PIR GND | GND |
| Servo VCC | Power Supply 5V (แยก) |
| Servo GND | GND ร่วม |

```
💡 วิธีต่อ Servo Power Supply แยก:

    ┌──────────────┐
    │  USB 5V       │──────┐
    │  Adapter      │      │
    └──────────────┘      │
                         │──── สายแดง → Servo VCC (แดง)
                         │
    ┌──────────────┐      │
    │  ESP32-C3    │──────┤──── สายน้ำตาล → Servo GND
    │  GND          │      │     + PIR GND + LED GND ทั้งหมด
    └──────────────┘      │
                         │──── สายส้ม → GPIO 2 (Servo Signal)
                         │
    ┌──────────────┐     │
    │  Servo SG90   │◄────┘
    └──────────────┘
```

#### ขั้นตอนที่ 2: เขียนโค้ด

```cpp
// ============================================
// บทที่ 7: เข็มขั้นบันไดอัตโนมัติ
// ============================================
// ใช้ PIR Sensor ตรวจจับคนเดินผ่าน
// → Servo ยกขึ้น → รอ 3 วินาที → ค่อยๆ ลงมา

#include <Servo.h>

// ==== กำหนดขา Pin ====
#define SERVO_PIN      2   // Servo Signal → GPIO 2
#define PIR_PIN        4   // PIR Sensor OUT → GPIO 4
#define LED_GREEN_PIN  6   // LED เขียว (เปิด) → GPIO 6
#define LED_RED_PIN    7   // LED แดง (รอ) → GPIO 7

// ==== ค่าตั้งต้น ====
#define SERVO_OPEN     90  // มุมเปิด (องศา)
#define SERVO_CLOSED   0   // มุมปิด (องศา)
#define WAIT_TIME      3000  // รอ 3 วินาที (ms)

// ==== สร้างอ็อบเจ็กต์ Servo ====
Servo stairServo;

// ==== สถานะ ====
enum State {
  STANDBY,   // รอคน → LED แดง
  OPENING,  // กำลังเปิด → Servo หมุนขึ้น
  OPENED,    // เปิดอยู่ → LED เขียว
  CLOSING    // กำลังปิด → Servo หมุนลง
};

State currentState = STANDBY;
unsigned long stateStartTime = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("=== เข็มขั้นบันไดอัตโนมัติ ===");

  // ตั้งค่า Pin Mode
  pinMode(PIR_PIN, INPUT);         // PIR เป็นขาเข้า
  pinMode(LED_GREEN_PIN, OUTPUT);  // LED เขียวเป็นขาออก
  pinMode(LED_RED_PIN, OUTPUT);   // LED แดงเป็นขาออก

  // ต่อ Servo
  stairServo.attach(SERVO_PIN);
  stairServo.write(SERVO_CLOSED);  // เริ่มที่มุมปิด

  // เริ่มต้น LED
  digitalWrite(LED_RED_PIN, HIGH);   // LED แดงติด (รอ)
  digitalWrite(LED_GREEN_PIN, LOW);  // LED เขียวดับ

  Serial.println("พร้อมรับคนเดินผ่าน...");
}

void loop() {
  int pirValue = digitalRead(PIR_PIN);  // อ่านค่าจาก PIR Sensor

  switch (currentState) {

    // ===== สถานะ: รอคน =====
    case STANDBY:
      if (pirValue == HIGH) {
        // ตรวจพบคน! → เริ่มเปิด
        Serial.println("🚶 ตรวจพบคน → เปิดบันได!");
        currentState = OPENING;
        stateStartTime = millis();
      }
      break;

    // ===== สถานะ: กำลังเปิด =====
    case OPENING:
      // หมุน Servo ไปที่มุมเปิด (90°) อย่างค่อยเป็นค่อยไป
      for (int angle = SERVO_CLOSED; angle <= SERVO_OPEN; angle += 5) {
        stairServo.write(angle);
        delay(20);  // หมุนช้าๆ ให้นุ่มนวล
      }
      // เปลี่ยนเป็นสถานะ "เปิดอยู่"
      currentState = OPENED;
      stateStartTime = millis();
      digitalWrite(LED_RED_PIN, LOW);     // ดับ LED แดง
      digitalWrite(LED_GREEN_PIN, HIGH); // ติด LED เขียว
      Serial.println("✅ บันไดเปิดแล้ว!");
      break;

    // ===== สถานะ: เปิดอยู่ (รอเวลา) =====
    case OPENED:
      if (millis() - stateStartTime >= WAIT_TIME) {
        // ครบเวลาแล้ว → เริ่มปิด
        Serial.println("⏰ ครบเวลา → ปิดบันได");
        currentState = CLOSING;
      }
      break;

    // ===== สถานะ: กำลังปิด =====
    case CLOSING:
      // หมุน Servo กลับลงมาที่มุมปิด (0°) อย่างค่อยเป็นค่อยไป
      for (int angle = SERVO_OPEN; angle >= SERVO_CLOSED; angle -= 5) {
        stairServo.write(angle);
        delay(20);
      }
      // กลับไปสถานะรอ
      currentState = STANDBY;
      digitalWrite(LED_RED_PIN, HIGH);    // ติด LED แดง
      digitalWrite(LED_GREEN_PIN, LOW);   // ดับ LED เขียว
      Serial.println("🔴 รอคนถัดไป...");
      break;
  }

  delay(50);  // หน่วงเวลาเล็กน้อย
}
```

#### ขั้นตอนที่ 3: อัปโหลดและทดสอบ

1. **เลือกบอร์ด:** ESP32C3 Dev Module
2. **เลือก Port** ที่ถูกต้อง
3. **กด Upload** 🚀
4. **เปิด Serial Monitor** ที่ 115200 baud

**วิธีทดสอบ:**
1. รอสักครู่ให้ PIR Sensor พร้อม (ประมาณ 10-20 วินาที หลังเปิด)
2. **โบกมือ** หน้า PIR Sensor หรือเดินผ่าน
3. ดูว่า Servo หมุนขึ้น → LED เขียวติด
4. รอ 3 วินาที → Servo ค่อยๆ หมุนลง → LED แดงติด

> 💡 **เคล็ดลับ:** ถ้า PIR ตรวจไม่เจอ ให้ลองเดินช้าๆ หรือยืนนิ่งๆ แล้วค่อยขยับ หรือปรับ Sensitivity ที่ตัว PIR (มีสกรูหมุนได้)

**ผลลัพธ์ที่คาดหวัง:** 🎉
- LED แดงติด = รอคน (สถานะ STANDBY)
- มีคนผ่าน → Servo หมุนขึ้น 90° + LED เขียวติด
- รอ 3 วินาที → Servo ค่อยๆ หมุนลง + LED แดงติดกลับ
- วนซ้ำ!

---

## 🔬 เรื่องพิเศษ: Servo กับ Interrupt ⚡

ถ้าเราต้องการให้ Servo หยุดทำงานทันทีเมื่อกดปุ่มฉุกเฉิน เราสามารถใช้ **Interrupt** ช่วยได้!

**Interrupt** คือกลไกที่ทำให้ ESP32 หยุดทำอะไรอยู่ก็ตามที เพื่อไปทำอีกเรื่องที่สำคัญกว่าทันที

```cpp
// ==== กำหนดขา ====
#define SERVO_PIN   2
#define BUTTON_PIN  3   // ปุ่มฉุกเฉิน → GPIO 3

// ==== สร้างอ็อบเจ็กต์ ====
Servo myServo;

// ==== ฟังก์ชันที่จะทำเมื่อกดปุ่ม ====
void IRAM_ATTR emergencyStop() {
  myServo.write(0);   // หมุนกลับมุม 0°
  digitalWrite(LED_BUILTIN, LOW);  // ดับ LED ทุกตัว
}

void setup() {
  myServo.attach(SERVO_PIN);

  // ตั้งค่า Interrupt
  // RISING = ตรวจจับเมื่อสัญญาณเปลี่ยนจาก LOW เป็น HIGH
  attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), emergencyStop, RISING);

  Serial.println("พร้อมใช้งาน (กดปุ่มเพื่อหยุดฉุกเฉิน)");
}

void loop() {
  // หมุนไปมา
  myServo.write(90);
  delay(1000);
  myServo.write(0);
  delay(1000);
}
```

> 💡 **เคล็ดลับ:** `IRAM_ATTR` บอกว่าให้เก็บฟังก์ชันนี้ไว้ใน RAM (เร็วกว่าอ่านจาก Flash) ซึ่งจำเป็นสำหรับ Interrupt Handler

---

## 📝 แบบฝึก

### แบบฝึกที่ 1: ปรับความเร็ว Servo
ลองเปลี่ยนค่า `delay(15)` ให้ Servo หมุนเร็วขึ้นหรือช้าลง ดูว่า `delay()` ที่เหมาะสมสำหรับ SG90 คือเท่าไหร่?

```cpp
// ลองเปลี่ยนค่านี้ใน loop():
delay(5);   // หมุนเร็วมาก (อาจกระตุก)
delay(30);  // หมุนช้านุ่มนวล
delay(100); // หมุนช้ามาก
```

### แบบฝึกที่ 2: Servo Sweep อัตโนมัติ
เขียนโค้ดให้ Servo หมุนจาก 0° → 180° → 0° วนซ้ำไปเรื่อยๆ โดยใช้ `for` loop และไม่ใช้ Library

```cpp
// คำใบ้: ใช้ฟังก์ชัน ledcWrite() สำหรับ ESP32
// หรือใช้ delayMicroseconds() สำหรับสัญญาณ PWM ดิบ
```

### แบบฝึกที่ 3: ควบคุม Servo หลายตัว
ลองต่อ Servo 2 ตัว แล้วเขียนโค้ดให้เคลื่อนไหวเป็นจังหวะ (เช่น หุ่นยนต์เต้น)

```cpp
Servo servo1;
Servo servo2;
// servo1 หมุน 0° → servo2 หมุน 90° → สลับกัน
```

### แบบฝึกที่ 4: เพิ่มเสียง Buzzer แจ้งเตือน
เพิ่ม Buzzer ให้เสียงเมื่อ Servo หมุนขึ้นหรือลง ใช้ในโปรเจกต์ขั้นบันได

### แบบฝึกที่ 5: Servo + LDR (ตัวต้านทานไวแสง)
ใช้ LDR แทน Potentiometer เพื่อให้ Servo หมุนตามแสง เช่น ทำแขนหุ่นยนต์หันไปหาแสง

---

## 🤔 คำถามท้ายบท

1. **"ทำไม Servo ถึงต้องใช้ PWM Signal ในการควบคุมมุม?"** — อธิบายว่า PWM ทำงานยังไง และทำไมไม่ใช้สัญญาณอื่น เช่น ON/OFF ธรรมดา

2. **"ทำไมเราต้องแยก Power Supply ให้ Servo?"** — ถ้าเราจ่ายไฟ Servo จาก Pin 3.3V ของ ESP32-C3 โดยตรงจะเกิดอะไรขึ้น?

3. **"ถ้าเราต้องการให้ Servo หมุน 360° แทนที่จะเป็น 180° เราต้องใช้อุปกรณ์อะไรแทน?"**

4. **(เชิงลึก)** "จะเกิดอะไรขึ้นถ้าเราต่อ Servo หลายตัว (เช่น 4 ตัว) แล้วให้ทุกตัวหมุนพร้อมกัน? Power Supply USB จะรับได้ไหม? ถ้าไม่ได้ต้องใช้อะไร?"

---

## 📚 สรุป

ในบทนี้เราได้เรียนรู้ว่า:

✅ **Servo Motor ทำงานด้วยสัญญาณ PWM** — ยิ่ง Pulse Width กว้าง มุมยิ่งมาก (0° = ~1ms, 180° = ~2ms)  
✅ **ต้องแยก Power Supply ให้ Servo** — เพราะ Servo ดึงกระแสสูงมาก อาจทำให้ ESP32-C3 พังได้ถ้าใช้ไฟจากบอร์ดเพียงอย่างเดียว  
✅ **ใช้ Library `Servo.h`** สำหรับ Arduino IDE ควบคุม Servo ได้ง่ายมากเพียง `servo.write(angle)`  
✅ **Potentiometer ใช้ควบคุมมุม Servo** ได้โดยอ่านค่า ADC แล้วแปลงเป็นมุม 0°-180°  
✅ **สามารถสร้างโปรเจกต์เข็มขั้นบันไดอัตโนมัติ** โดยใช้ PIR Sensor + Servo + LED ร่วมกัน

> 🔮 **บทต่อไป:** ในบทถัดไปเราจะมาเรียนรู้เรื่อง **IR Remote** กัน! เราจะได้รู้ว่าทำไมกดรีโมททีวีแล้วทีวีถึงรู้ว่าเรากดปุ่มอะไร และจะเอามาควบคุม ESP32-C3 ได้ยังไง! 📺➡️🔌

---

*📁 โค้ดตัวอย่าง: `/code/ch07_servo/`*  
*🖼️ รูปประกอบ: `/images/ch07-*`*
