# 📖 บทที่ 5: DHT11 — เซ็นเซอร์วัดอุณหภูมิและความชื้น

> 💡 **หมายเหตุ:** DHT11 คือเซ็นเซอร์ราคาถูกที่วัดได้ทั้งอุณหภูมิและความชื้นในอากาศ ติดตั้งง่าย ใช้งานได้จริงในโปรเจกต์หลายๆ แบบ เหมาะมากสำหรับผู้เริ่มต้น!

---

## 🎯 สิ่งที่จะเรียนรู้

ในบทนี้ เราจะได้เรียนรู้:

- [ ] DHT11 ทำงานอย่างไร (อธิบายแบบเข้าใจง่าย)
- [ ] วิธีต่อ DHT11 กับ ESP32-C3 อย่างถูกต้อง
- [ ] เขียนโค้ดอ่านค่าอุณหภูมิและความชื้น
- [ ] แสดงผลข้อมูลบน Serial Monitor
- [ ] ปฏิบัติ: วัดอุณหภูมิ-ความชื้นห้องและบันทึกข้อมูล

---

## 📖 บทนำ

เคยสงสัยมั้ยครับ ว่าทำไมบางวันเรารู้สึกว่าอากาศ "จะปิด" หรือ "หนัก" แม้ว่าตามพยากรณ์อากาศจะบอกว่าอุณหภูมิไม่สูงมาก? นั่นแหละครับ! คือผลของ **ความชื้น** ในอากาศ ซึ่งมีผลต่อความรู้สึกสบายตัวของเรามาก

ความชื้น (Humidity) คือปริมาณไอน้ำที่อยู่ในอากาศ ถ้าความชื้นสูง เหงื่อระเหยช้า เราก็รู้สึกร้อนมากขึ้น ถ้าความชื้นต่ำ ผิวหนังเราก็แห้งตึง รู้สึกไม่สบายตัว

วันนี้เราจะมาเรียนรู้การใช้เซ็นเซอร์ **DHT11** ที่สามารถวัดได้ทั้ง **อุณหภูมิ** และ **ความชื้น** ในคราวเดียวกัน! 🌡️💧 พร้อมกับนำข้อมูลที่ได้ไปแสดงผลและบันทึกเก็บไว้ด้วย สนุกมากเลย!

---

## 🔧 อุปกรณ์ที่ใช้

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| DHT11 Sensor Module | 1 ตัว | พร้อมบอร์ด (มี Resistor ติดมาแล้ว) |
| สายจัมเปอร์ | 3 เส้น | ผู้หญิง-ผู้ชาย |
| สาย USB-C | 1 เส้น | สำหรับต่อกับคอมพิวเตอร์ |

---

## 💻 เนื้อหา

### 🔹 DHT11 ทำงานยังไง? (อธิบายแบบเข้าใจง่าย)

ก่อนจะใช้งานเซ็นเซอร์ตัวไหนก็ตาม สิ่งที่ดีมากๆ คือการเข้าใจว่ามันทำงานอย่างไร ไม่ต้องเข้าใจฟิสิกส์ขั้นสูงหรอกนะครับ แค่เข้าใจหลักการพื้นฐานก็เพียงพอแล้ว!

**DHT11 คืออะไร?**

DHT11 คือเซ็นเซอร์วัดอุณหภูมิและความชื้นแบบ Digital ขนาดเล็ก ราคาถูก (ประมาณ 30-50 บาท) แต่ทำงานได้ดีในระดับพื้นฐาน มันเป็นตัวเซ็นเซอร์ที่นิยมใช้กันมากในโปรเจกต์ DIY ต่างๆ

```
┌─────────────────────────┐
│       DHT11 Module      │
│                         │
│   [DHT11 Sensor Chip]   │
│                         │
│   VCC  OUT  GND        │
│    │    │    │         │
│    └───┴────┘          │
│     (Resistor ในตัว)   │
└─────────────────────────┘
```

**DHT11 มาใน 2 แบบ:**

```
แบบที่ 1: แยกชิ้นส่วน (Standalone)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- มี 4 ขา: VCC, Data, GND, NC (ไม่ได้ใช้)
- ต้องต่อ Resistor Pull-up เอง (4.7KΩ หรือ 10KΩ)
- ต้องต่อ Capacitor เพิ่ม (optional)

แบบที่ 2: พร้อม Module บอร์ด (เหมาะสำหรับเรามาก!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- มี 3 ขา: VCC, Data, GND
- มี Resistor Pull-up ติดมาบนบอร์ดแล้ว
- มี LED บอกสถานะ + Capacitor ในตัว
- ใช้งานง่าย ราคาไม่แพงมาก
```

> 💡 **เคล็ดลับ:** ซื้อแบบ Module (มีบอร์ดพร้อม) จะสะดวกกว่ามากสำหรับผู้เริ่มต้น! ถ้าซื้อแบบแยกชิ้นต้องต่อ Resistor Pull-up เพิ่มเอง

**หลักการทำงานของ DHT11:**

ภายใน DHT11 มีส่วนประกอบหลัก 2 ส่วน:

```
ส่วนที่ 1: วัดความชื้น (Humidity Sensor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ใช้แผ่นฟิล์มพอลิเมอร์ที่ดูดซับไอน้ำ
- เมื่อความชื้นมาก → แผ่นฟิล์มดูดไอน้ำมากขึ้น → ค่าความต้านทานเปลี่ยน
- เมื่อความชื้นน้อย → แผ่นฟิล์มแห้ง → ค่าความต้านทานเปลี่ยนเช่นกัน
- วัดได้: 20-90% RH (ความชื้นสัมพัทธ์)

ส่วนที่ 2: วัดอุณหภูมิ (Temperature Sensor)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- ใช้ Thermistor (ตัวต้านทานที่เปลี่ยนค่าตามอุณหภูมิ)
- อุณหภูมิสูงขึ้น → ความต้านทานลดลง
- อุณหภูมิต่ำลง → ความต้านทานเพิ่มขึ้น
- วัดได้: 0-50°C (ความแม่นยำ ±2°C)
```

**DHT11 สื่อสารกับ ESP32 ยังไง?**

DHT11 ใช้วิธีสื่อสารแบบ **Single-Wire Serial Interface** หรือเรียกว่า **DHT Protocol** ซึ่งเป็นโปรโตคอลที่ DHT สร้างขึ้นมาเอง มันส่งข้อมูลเป็น **40 bits** (5 bytes) ทุกครั้งที่ถูกอ่าน:

```
40 bits = 5 bytes = 16 bits humidity + 16 bits temperature + 8 bits checksum

[ Humidity High ] [ Humidity Low ] [ Temp High ] [ Temp Low ] [ Checksum ]
      8 bits          8 bits          8 bits        8 bits       8 bits
```

```
Checksum คืออะไร?
━━━━━━━━━━━━━━━
Checksum คือการตรวจสอบความถูกต้องของข้อมูล
มันคือผลรวมของ 4 bytes แรก (Humidity + Temperature)
ถ้าผลรวมไม่ตรงกับ Checksum → แปลว่าข้อมูลเสียหาย ต้องอ่านใหม่
```

**ขั้นตอนการอ่านข้อมูลจาก DHT11:**

```
1. ESP32 ส่งสัญญาณ START ไปที่ DHT11 (ลากสาย Data ลง LOW เป็นเวลา 18ms)
2. DHT11 ตอบกลับด้วยสัญญาณ LOW (80μs) + HIGH (80μs)
3. DHT11 เริ่มส่งข้อมูล 40 bits ทีละ bit
4. แต่ละ bit ประกอบด้วย:
   - LOW 50μs แล้วตามด้วย HIGH
   - ถ้า HIGH ยาว = 1, ถ้า HIGH สั้น = 0
5. ESP32 อ่านความยาวของ HIGH เพื่อรู้ว่า bit นั้นเป็น 0 หรือ 1
```

> 💡 **เคล็ดลับ:** ถ้าอ่านค่าไม่ได้ ลองเพิ่ม `delay(2000)` หลังจากเริ่มต้น DHT เพราะ DHT11 ต้องการเวลา "ตื่นตัว" ประมาณ 1-2 วินาทีหลังจากเปิดเครื่อง

---

### 🔹 วิธีต่อ DHT11 กับ ESP32-C3

ต่อวงจร DHT11 กับ ESP32-C3 ต้องทำอย่างระมัดระวังนะครับ! ผิดเพี้ยนไปนิดเดียวอาจทำให้อ่านค่าไม่ได้ หรือเซ็นเซอร์เสียหายได้

**การต่อสาย DHT11 Module กับ ESP32-C3:**

```
DHT11 Module                ESP32-C3
━━━━━━━━━━━━━               ━━━━━━━━━
  VCC (ขาแรก)  ──────────────  3.3V  (หรือ 5V ก็ได้)
  OUT (ขากลาง) ──────────────  GPIO 4
  GND (ขาสุดท้าย) ───────────  GND
```

**รายละเอียดแต่ละขา:**

```
DHT11 Module Pinout:
┌────────────────────────┐
│  DHT11 MODULE          │
│                        │
│  PIN 1: VCC  ●─────────●──→ 3.3V หรือ 5V
│  PIN 2: OUT  ●─────────●──→ GPIO 4 (หรือ GPIO อื่นก็ได้)
│  PIN 3: GND  ●─────────●──→ GND
│                        │
│  [LED สีแดงเล็กๆ บอกว่าต่อไฟแล้ว]
└────────────────────────┘
```

```
ESP32-C3 Pinout (ด้านบน):
┌──────────────────────────────────────┐
│                      USB-C           │
│  [USB]                    [RST]      │
│                                      │
│  3V3 ●────────────────●              │
│  GND ●────────────────●              │
│  2   ●────────────────●              │
│  3   ●────────────────●              │
│  4   ●────────────────●──→ DHT11 OUT │
│  5   ●────────────────●              │
│  ...                               │
│                                      │
│  BOOT ●────────────────●            │
│  (ปุ่มกดเล็กๆ)                        │
└──────────────────────────────────────┘
```

> ⚠️ **คำเตือน:** ตรวจสอบให้แน่ใจว่าต่อ VCC เข้ากับ 3.3V หรือ 5V (ขึ้นอยู่กับ Module) ถ้าต่อเข้าผิด (เช่น 5V เข้า 3.3V) อาจทำให้ DHT11 เสียหายได้!

> 💡 **เคล็ดลับ:** ถ้าใช้ DHT11 Module ที่มี Resistor Pull-up ติดมาแล้ว สามารถต่อได้เลยโดยไม่ต้องต่อ Resistor เพิ่ม แต่ถ้าเป็นแบบแยกชิ้น ต้องต่อ Resistor 10KΩ ระหว่าง Data กับ VCC ด้วย!

---

### 🔹 เขียนโค้ดอ่านค่าอุณหภูมิ

ต่อไปเรามาเขียนโค้ดกันนะครับ! ก่อนอื่นเราต้องติดตั้ง Library สำหรับ DHT11 ก่อน

**วิธีที่ 1: ติดตั้ง Library ผ่าน PlatformIO (แนะนำ)**

1. เปิดไฟล์ `platformio.ini` ในโปรเจกต์
2. เพิ่มบรรทัดนี้ใน `[env:...]`:

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino
monitor_speed = 115200

; เพิ่ม Library สำหรับ DHT11
lib_deps = 
    adafruit/Adafruit Unified Sensor@^1.1.9
    adafruit/DHT sensor library@^1.4.4
    adafruit/DHT stable@^1.0.3
```

3. กด **Save** แล้ว PlatformIO จะดาวน์โหลด Library อัตโนมัติ

**วิธีที่ 2: ติดตั้ง Library ผ่าน Arduino IDE**

1. ไปที่ **Sketch → Include Library → Manage Libraries**
2. พิมพ์ "DHT sensor library" ในช่องค้นหา
3. ติดตั้ง **DHT sensor library** จาก Adafruit
4. ติดตั้ง **Adafruit Unified Sensor** ด้วย

**โค้ดพื้นฐานสำหรับอ่านค่า DHT11:**

```cpp
// ch05_dht11_basic - อ่านค่าอุณหภูมิและความชื้นจาก DHT11
// ESP32-C3 STEM AI Coding

#include <Arduino.h>
#include <DHT.h>         // เรียกใช้ DHT Library

// กำหนดขาที่ต่อกับ DHT11
#define DHT_PIN  4       // GPIO 4 (เปลี่ยนได้ถ้าต่อขาอื่น)
#define DHT_TYPE DHT11   // ประเภทเซ็นเซอร์ (DHT11, DHT22, DHT21)

// สร้าง object สำหรับ DHT
DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  delay(1000);  // รอให้ Serial พร้อม

  Serial.println("╔══════════════════════════════════╗");
  Serial.println("║   DHT11 Temperature & Humidity   ║");
  Serial.println("╚══════════════════════════════════╝");

  dht.begin();  // เริ่มใช้งาน DHT11
  Serial.println("[DHT] Sensor initialized!");
  Serial.println("[DHT] Wait 2 seconds for first reading...\n");
  delay(2000);  // รอให้ DHT11 ตื่นตัว (ต้องรอ!)
}

void loop() {
  // อ่านค่าความชื้น (Humidity)
  float humidity = dht.readHumidity();

  // อ่านค่าอุณหภูมิเป็น Celsius (องศาเซลเซียส)
  float temperatureC = dht.readTemperature();

  // อ่านค่าอุณหภูมิเป็น Fahrenheit (องศาฟาเรนไฮต์)
  float temperatureF = dht.readTemperature(true);

  // เช็คว่าอ่านค่าได้มั้ย (ถ้ามี error จะได้ค่า NaN)
  if (isnan(humidity) || isnan(temperatureC) || isnan(temperatureF)) {
    Serial.println("[ERROR] Failed to read from DHT sensor!");
    delay(2000);  // รอ 2 วินาทีแล้วลองใหม่
    return;       // กลับไป loop ใหม่
  }

  // แสดงผลข้อมูลที่อ่านได้
  Serial.println("━━━ DHT11 Reading ━━━");
  Serial.printf("🌡️  Temperature: %.1f°C (%.1f°F)\n", temperatureC, temperatureF);
  Serial.printf("💧 Humidity:    %.1f%%\n", humidity);

  // คำนวณ Heat Index (อุณหภูมิที่รู้สึกจริง เมื่อรวมความชื้น)
  float heatIndex = dht.computeHeatIndex(temperatureC, humidity, false);
  Serial.printf("🌡️  Heat Index: %.1f°C\n", heatIndex);

  Serial.println("━━━━━━━━━━━━━━━━━━━━");
  Serial.println();  // ขึ้นบรรทัดใหม่

  delay(3000);  // อ่านทุก 3 วินาที
}
```

> 💡 **เคล็ดลับ:** ทำไมต้องใช้ `isnan()`? เพราะถ้า DHT11 อ่านค่าไม่ได้ (เช่น สายหลุด, ไฟไม่ถึง, หรือเซ็นเซอร์เสีย) มันจะคืนค่า `NaN` (Not a Number) ซึ่งเราต้องเช็คก่อนใช้งาน ไม่งั้นโปรแกรมจะทำงานผิดพลาด

---

### 🔹 แสดงผลบน Serial Monitor

Serial Monitor จะแสดงผลออกมาประมาณนี้:

```
╔══════════════════════════════════╗
║   DHT11 Temperature & Humidity   ║
╚══════════════════════════════════╝
[DHT] Sensor initialized!
[DHT] Wait 2 seconds for first reading...

━━━ DHT11 Reading ━━━
🌡️  Temperature: 28.5°C (83.3°F)
💧 Humidity:    75.0%
🌡️  Heat Index: 32.1°C
━━━━━━━━━━━━━━━━━━━━

━━━ DHT11 Reading ━━━
🌡️  Temperature: 28.7°C (83.7°F)
💧 Humidity:    74.5%
🌡️  Heat Index: 32.3°C
━━━━━━━━━━━━━━━━━━━━
```

> 💡 **เคล็ดลับ:** ค่า Heat Index (อุณหภูมิที่รู้สึก) คือค่าที่บอกว่าเรารู้สึกร้อนแค่ไหน เพราะเมื่อความชื้นสูง เหงื่อระเหยยาก ทำให้รู้สึกร้อนกว่าอุณหภูมิจริง! ถ้า Heat Index เกิน 32°C ควรระวังเรื่องสุขภาพด้วยนะครับ

**ปัญหาที่พบบ่อยและวิธีแก้ไข:**

```
❌ ปัญหา: อ่านค่าไม่ได้ตลอด บางครั้งขึ้น NaN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
สาเหตุ: สายยาวเกินไป หรือ สัญญาณรบกวน
แก้: 
  - ต่อสายให้สั้นที่สุด (ไม่เกิน 20 เมตร)
  - เพิ่ม Capacitor 0.1μF ระหว่าง VCC กับ GND
  - เพิ่ม delay ให้นานขึ้น

❌ ปัญหา: ค่าความชื้นไม่แม่นยำ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
สาเหตุ: DHT11 มีความแม่นยำ ±5% ซึ่งไม่สูงมาก
แก้:
  - ใช้ DHT22 แทน (แม่นยำกว่า ±2%)
  - ถ้าต้องการความแม่นยำสูง ใช้ BME280 แทน

❌ ปัญหา: ค่าอุณหภูมิผิดปกติ เช่น 0°C หรือ -1°C
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
สาเหตุ: มักเกิดจากการอ่านค่าผิดพลาด
แก้:
  - ใช้ค่าเฉลี่ยจากการอ่านหลายครั้ง
  - เช็ค `isnan()` ก่อนใช้ค่าทุกครั้ง
```

---

## 🔨 ปฏิบัติ: วัดอุณหภูมิ-ความชื้นห้อง + บันทึกข้อมูล

ในการปฏิบัตินี้เราจะสร้าง **Weather Logger** ที่วัดอุณหภูมิและความชื้นทุกๆ ช่วงเวลาที่กำหนด และบันทึกข้อมูลไว้ดูย้อนหลังได้ เหมือนเป็นสถานีตรวจอากาศเล็กๆ ในห้องเราเลย! 🌡️💧📊

### 📋 สิ่งที่ต้องเตรียม

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| DHT11 Module | 1 ตัว | พร้อม Module จะดีกว่า |
| LED สีเขียว | 1 หลอด | แสดงสถานะ |
| Resistor 220Ω | 1 ตัว | สำหรับ LED |
| Breadboard | 1 อัน | สำหรับต่อวงจร |
| สายจัมเปอร์ | จำนวนเท่าที่ต้องการ | ผู้หญิง-ผู้ชาย |

### 📋 ขั้นตอนที่ 1: ต่อวงจร

```
DHT11 Module:
  VCC  ────────────────  3.3V
  OUT  ────────────────  GPIO 4
  GND  ────────────────  GND

LED (สถานะ):
  ขาบวก (ยาว) ────────────  GPIO 3 (ผ่าน Resistor 220Ω)
  ขาลบ (สั้น) ────────────  GND
```

### 📋 ขั้นตอนที่ 2: สร้างโปรเจกต์ใหม่บน PlatformIO

1. สร้างโปรเจกต์ใหม่ชื่อ `ch05_weather_logger`
2. เพิ่ม Library ใน `platformio.ini`:

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino
monitor_speed = 115200

lib_deps = 
    adafruit/Adafruit Unified Sensor@^1.1.9
    adafruit/DHT sensor library@^1.4.4
    adafruit/DHT stable@^1.0.3
```

### 📋 ขั้นตอนที่ 3: เขียนโค้ด Weather Logger

สร้างไฟล์ใหม่ `src/dht_sensor.h`:

```cpp
// dht_sensor.h - DHT Sensor Module Header
// ESP32-C3 STEM AI Coding

#ifndef DHTSENSOR_H
#define DHTSENSOR_H

#include <Arduino.h>
#include <DHT.h>

// กำหนดขาและประเภทเซ็นเซอร์
#define DHT_DATA_PIN  4
#define DHT_SENSOR_TYPE DHT11

// ประกาศฟังก์ชัน
void dhtSensorInit();                        // เริ่มใช้งาน DHT
bool readDHT(float& temperature, float& humidity);  // อ่านค่า (คืน true/false)
String getComfortLevel(float temp, float hum);       // ระดับความสบาย
void printReading(float temp, float hum);             // แสดงผล Reading

#endif
```

สร้างไฟล์ `src/dht_sensor.cpp`:

```cpp
// dht_sensor.cpp - DHT Sensor Module Implementation
// ESP32-C3 STEM AI Coding

#include "dht_sensor.h"

// สร้าง DHT object
DHT dht(DHT_DATA_PIN, DHT_SENSOR_TYPE);

// ฟังก์ชันเริ่มใช้งาน DHT
void dhtSensorInit() {
  dht.begin();
  Serial.println("[DHT] Initialized - DHT11 Temperature & Humidity Sensor");
  Serial.println("[DHT] First reading in 2 seconds...\n");
  delay(2000);  // รอให้ DHT ตื่นตัว
}

// ฟังก์ชันอ่านค่า DHT (ส่งคืน true ถ้าสำเร็จ, false ถ้าล้มเหลว)
bool readDHT(float& temperature, float& humidity) {
  // อ่านค่าความชื้นและอุณหภูมิ
  humidity = dht.readHumidity();
  temperature = dht.readTemperature();

  // เช็คว่าอ่านได้มั้ย
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("[DHT] ERROR: Failed to read sensor!");
    return false;
  }

  return true;  // อ่านสำเร็จ
}

// ฟังก์ชันตรวจสอบระดับความสบาย
String getComfortLevel(float temp, float hum) {
  // คำนวณ Heat Index
  float heatIndex = dht.computeHeatIndex(temp, hum, false);

  // ตรวจสอบเงื่อนไขต่างๆ
  if (heatIndex >= 40) {
    return "⚠️  อันตราย! ร้อนมาก!";  // Heat index > 40°C
  } else if (heatIndex >= 32) {
    return "🔥 ร้อนมาก";  // Heat index 32-40°C
  } else if (heatIndex >= 27) {
    return "☀️  ค่อนข้างร้อน";  // Heat index 27-32°C
  } else if (hum >= 80) {
    return "💦 ชื้นมาก อากาศหนัก";  // Humidity > 80%
  } else if (hum >= 60) {
    return "😊 ค่อนข้างชื้น";  // Humidity 60-80%
  } else if (hum < 30) {
    return "🏜️ แห้งมาก";  // Humidity < 30%
  } else {
    return "🌤️  สบาย";  // Comfortable
  }
}

// ฟังก์ชันแสดงผล Reading สวยๆ
void printReading(float temp, float hum) {
  float fahrenheit = temp * 9.0 / 5.0 + 32.0;
  float heatIndex = dht.computeHeatIndex(temp, hum, false);
  String comfort = getComfortLevel(temp, hum);

  Serial.println("╔══════════════════════════════════════╗");
  Serial.println("║       🌡️  DHT11 WEATHER READING      ║");
  Serial.println("╠══════════════════════════════════════╣");
  Serial.printf  ("║  🌡️  Temperature:  %6.1f°C  (%5.1f°F) ║\n", temp, fahrenheit);
  Serial.printf  ("║  💧 Humidity:       %6.1f%%           ║\n", hum);
  Serial.printf  ("║  🌡️  Heat Index:    %6.1f°C           ║\n", heatIndex);
  Serial.printf  ("║  😊 Comfort:        %-18s ║\n", comfort.c_str());
  Serial.println("╚══════════════════════════════════════╝");
}
```

สร้างไฟล์ `src/main.cpp`:

```cpp
// main.cpp - Weather Logger with DHT11
// ESP32-C3 STEM AI Coding - Chapter 05
// วัดอุณหภูมิ ความชื้น และบันทึกข้อมูล

#include <Arduino.h>
#include "dht_sensor.h"

// กำหนดขา LED สถานะ
#define STATUS_LED 3

// กำหนดเวลาในการบันทึก (ทุก 10 วินาที)
#define LOG_INTERVAL 10000  // 10 วินาที
#define SERIAL_INTERVAL 3000  // แสดงผลทุก 3 วินาที

unsigned long lastLogTime = 0;    // เวลาบันทึกล่าสุด
unsigned long lastSerialTime = 0;  // เวลาแสดงผลล่าสุด
int readingCount = 0;             // จำนวนครั้งที่อ่าน

// ตัวแปรสำหรับค่าเฉลี่ย
float avgTemp = 0;
float avgHum = 0;
float sumTemp = 0;
float sumHum = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);

  // ตั้งค่า LED สถานะ
  pinMode(STATUS_LED, OUTPUT);
  digitalWrite(STATUS_LED, LOW);

  Serial.println("╔══════════════════════════════════════════╗");
  Serial.println("║   ESP32-C3 WEATHER LOGGER 🌡️💧            ║");
  Serial.println("║   DHT11 Temperature & Humidity Sensor     ║");
  Serial.println("╚══════════════════════════════════════════╝");

  // เริ่มใช้งาน DHT
  dhtSensorInit();

  // LED กระพริบบอกว่าเริ่มทำงานแล้ว
  blinkLED(3, 200);
}

void loop() {
  unsigned long currentTime = millis();  // อ่านเวลาปัจจุบัน (มิลลิวินาที)
  float temperature, humidity;

  // อ่านค่าจาก DHT
  if (readDHT(temperature, humidity)) {
    // อ่านสำเร็จ → LED ติด
    digitalWrite(STATUS_LED, HIGH);

    // บันทึกค่าเพื่อคำนวณเฉลี่ย
    sumTemp += temperature;
    sumHum += humidity;
    readingCount++;

    // แสดงผลที่ Serial Monitor
    if (currentTime - lastSerialTime >= SERIAL_INTERVAL) {
      printReading(temperature, humidity);
      lastSerialTime = currentTime;
    }

    // บันทึกข้อมูล (พร้อม timestamp)
    if (currentTime - lastLogTime >= LOG_INTERVAL) {
      int uptimeSeconds = currentTime / 1000;
      int uptimeMinutes = uptimeSeconds / 60;
      int uptimeHours = uptimeMinutes / 60;

      avgTemp = sumTemp / readingCount;
      avgHum = sumHum / readingCount;

      Serial.println("━━━ 📋 LOG RECORD ━━━");
      Serial.printf("⏱️  Uptime: %dh %dm %ds\n", 
                    uptimeHours, uptimeMinutes % 60, uptimeSeconds % 60);
      Serial.printf("📊 Reading #%d\n", readingCount);
      Serial.printf("🌡️  Current Temp: %.1f°C\n", temperature);
      Serial.printf("💧 Current Humidity: %.1f%%\n", humidity);
      Serial.printf("📈 Avg Temp (since start): %.1f°C\n", avgTemp);
      Serial.printf("📈 Avg Humidity (since start): %.1f%%\n", avgHum);
      Serial.println("━━━━━━━━━━━━━━━━━━━━━\n");

      lastLogTime = currentTime;
    }

    digitalWrite(STATUS_LED, LOW);

  } else {
    // อ่านไม่ได้ → LED ดับ และรอ
    digitalWrite(STATUS_LED, LOW);
    blinkLED(2, 100);  // กระพริบเร็วๆ บอกว่ามีปัญหา
  }

  delay(500);  // หน่วงเวลาเล็กน้อย
}

// ฟังก์ชันกระพริบ LED
void blinkLED(int times, int delayMs) {
  for (int i = 0; i < times; i++) {
    digitalWrite(STATUS_LED, HIGH);
    delay(delayMs);
    digitalWrite(STATUS_LED, LOW);
    delay(delayMs);
  }
}
```

### 📋 ขั้นตอนที่ 4: อัปโหลดและทดสอบ

1. ต่อ DHT11 เข้ากับ ESP32-C3 ตามวงจรที่วางไว้
2. กด `Ctrl + Alt + U` เพื่ออัปโหลด
3. เปิด Serial Monitor ที่ 115200 baud
4. ดูผลลัพธ์!

```
╔══════════════════════════════════════════╗
║   ESP32-C3 WEATHER LOGGER 🌡️💧            ║
║   DHT11 Temperature & Humidity Sensor     ║
╚══════════════════════════════════════════╝
[DHT] Initialized - DHT11 Temperature & Humidity Sensor
[DHT] First reading in 2 seconds...

╔══════════════════════════════════════╗
║       🌡️  DHT11 WEATHER READING      ║
╠══════════════════════════════════════╣
║  🌡️  Temperature:    28.5°C  ( 83.3°F) ║
║  💧 Humidity:           75.0%           ║
║  🌡️  Heat Index:        32.1°C          ║
║  😊 Comfort:        ☀️  ค่อนข้างร้อน   ║
╚══════════════════════════════════════╝

━━━ 📋 LOG RECORD ━━━
⏱️  Uptime: 0h 0m 10s
📊 Reading #3
🌡️  Current Temp: 28.5°C
💧 Current Humidity: 75.0%
📈 Avg Temp (since start): 28.5°C
📈 Avg Humidity (since start): 74.8%
━━━━━━━━━━━━━━━━━━━━━
```

> 💡 **เคล็ดลับ:** ลองเอาเซ็นเซอร์ไปวางในที่ต่างๆ เช่น ในห้องนอน ในห้องครัว หรือนอกบ้าน แล้วสังเกตดูว่าอุณหภูมิและความชื้นต่างกันมากน้อยแค่ไหน!

---

### 📋 ขั้นตอนที่ 5 (เพิ่มเติม): บันทึกข้อมูลลง SD Card

ถ้าอยากเก็บข้อมูลไว้ดูย้อนหลังนานๆ สามารถเพิ่ม SD Card Module ได้:

```cpp
// เพิ่มใน platformio.ini:
// lib_deps = ... (DHT libs ที่มีอยู่แล้ว)
//    greiman/SD@^2.1.0

// สร้างไฟล์ data_logger.h และ data_logger.cpp แยกต่างหาก
// หรือถาม AI ว่า "ช่วยสร้างโค้ดบันทึกข้อมูลลง SD Card สำหรับ ESP32-C3"
```

---

## 📝 แบบฝึก

### แบบฝึกที่ 1: เพิ่ม LED แสดงสถานะ
เพิ่ม LED 2 สีเพื่อแสดงสถานะ:
- LED เขียว: อุณหภูมิปกติ (20-30°C)
- LED แดง: อุณหภูมิสูงเกิน (>30°C) หรือต่ำเกิน (<20°C)

```cpp
// เพิ่มโค้ดตรวจสอบอุณหภูมิ
if (temperature > 30.0) {
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_GREEN, LOW);
  Serial.println("⚠️  อุณหภูมิสูง!");
} else if (temperature < 20.0) {
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_GREEN, LOW);
  Serial.println("⚠️  อุณหภูมิต่ำ!");
} else {
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED, LOW);
}
```

### แบบฝึกที่ 2: ใช้เซ็นเซอร์ 2 ตัว
ต่อ DHT11 2 ตัว (เช่น วัดในห้องและนอกบ้าน) แล้วแสดงผลเปรียบเทียบ:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด PlatformIO สำหรับ ESP32-C3 ที่ใช้ DHT11 2 ตัว
ตัวแรกต่อที่ GPIO4 ตัวที่สองต่อที่ GPIO5
แสดงผลเปรียบเทียบอุณหภูมิและความชื้นในห้อง vs นอกบ้าน
ใช้ modular code แยกเป็นไฟล์ dht_sensor.cpp"
```

### แบบฝึกที่ 3: แสดงผลบน OLED
เพิ่มจอ OLED 0.96" I2C เพื่อแสดงผลแบบไม่ต้องต่อคอมพิวเตอร์:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด PlatformIO สำหรับ ESP32-C3 ที่แสดงผลอุณหภูมิและความชื้น
บนจอ OLED 0.96 I2C (SDA=GPIO1, SCL=GPIO0) 
พร้อมแสดง icon อารมณ์ตามระดับความสบาย"
```

### แบบฝึกที่ 4: ส่งข้อมูลขึ้น Cloud
ส่งข้อมูลอุณหภูมิและความชื้นขึ้นเว็บไซต์ IoT Platform ฟรี เช่น ThingSpeak หรือ Blynk:

```
Prompt สำหรับ AI:
"ช่วยสร้างโค้ด ESP32-C3 ที่ส่งข้อมูลอุณหภูมิและความชื้นจาก DHT11 ขึ้น ThingSpeak
ใช้ WiFi ของบ้าน ทุก 30 วินาที"
```

### แบบฝึกที่ 5: เปลี่ยนเป็น DHT22
DHT22 แม่นยำกว่า DHT11 มาก (ความชื้น ±2%, อุณหภูมิ ±0.5°C) ลองเปลี่ยนไปใช้ดู!

```cpp
// เปลี่ยนแค่บรรทัดนี้:
#define DHT_TYPE DHT22   // แทน DHT11
// หรือ DHT22 พร้อมใช้เลย ต่อวงจรเหมือนเดิม!
```

---

## 🤔 คำถามท้ายบท

### คำถามที่ 1: DHT11 vs DHT22 vs DHT21
**ถาม:** DHT มีหลายรุ่น (11, 22, 21) ต่างกันยังไง และควรเลือกใช้ตัวไหน?

**ตอบ:** 
- **DHT11:** ราคาถูกที่สุด (±5% ความชื้น, ±2°C อุณหภูมิ, วัดได้ 0-50°C, 20-90% RH) — เหมาะสำหรับโปรเจกต์ง่ายๆ ไม่ต้องการความแม่นยำสูง
- **DHT22:** แม่นยำกว่ามาก (±2% ความชื้น, ±0.5°C อุณหภูมิ, วัดได้ -40~80°C, 0-100% RH) — เหมาะสำหรับงานที่ต้องการความแม่นยำ ราคาประมาณ 3-4 เท่าของ DHT11
- **DHT21:** อยู่ระหว่าง 11 กับ 22 (±3% ความชื้น, ±0.5°C อุณหภูมิ) — ไม่ค่อยนิยมใช้

สำหรับโปรเจกต์ STEM แนะนำ **DHT11** สำหรับเริ่มต้น เพราะราคาถูกและใช้งานง่าย เมื่อต้องการความแม่นยำขึ้นค่อยเปลี่ยนเป็น DHT22

---

### คำถามที่ 2: ทำไม DHT11 ถึงต้องรอ 2 วินาทีก่อนอ่านครั้งแรก?
**ถาม:** ทำไมต้องมี `delay(2000)` หลังจาก `dht.begin()`? ถ้าไม่รอจะเป็นยังไง?

**ตอบ:** DHT11 ใช้เวลาประมาณ 1-2 วินาทีในการ "ตื่นตัว" และเตรียมพร้อมวัดค่าหลังจากเปิดไฟฟ้า ถ้าเราอ่านค่าทันทีหลังจากเริ่มทำงาน ค่าที่ได้จะไม่ถูกต้อง หรืออาจได้ค่า NaN ก็ได้ นี่เป็นข้อจำกัดของตัวเซ็นเซอร์เอง ไม่ใช่ปัญหาจากโค้ดของเรา หลังจากอ่านครั้งแรกแล้ว ค่าถัดไปจะอ่านได้เร็วปกติ (ทุก 2-3 วินาทีก็พอ)

---

### คำถามที่ 3: Heat Index คืออะไร?
**ถาม:** Heat Index ที่โค้ดคำนวณให้นั้นคืออะไร? มันต่างจากอุณหภูมิจริงยังไง?

**ตอบ:** Heat Index หรือ "อุณหภูมิที่รู้สึก" คือค่าที่บอกว่าเรารู้สึกร้อนแค่ไหน เมื่อรวมผลของความชื้นเข้าไปด้วย ตัวอย่างเช่น ถ้าอุณหภูมิจริง 30°C แต่ความชื้นสูงมาก (80%) Heat Index อาจสูงถึง 36°C ทำให้เรารู้สึกร้อนกว่าที่เทอร์โมมิเตอร์บอกจริงๆ DHT library มีฟังก์ชัน `computeHeatIndex()` ที่คำนวณให้เราโดยอัตโนมัติ ซึ่งใช้สูตรคำนวณทางอุตุนิยมวิทยา เมื่อ Heat Index เกิน 32°C ถือว่า "ร้อนมาก" และควรดื่มน้ำบ่อยๆ หลีกเลี่ยงการออกกำลังกายกลางแจ้ง เกิน 40°C ถือว่า **อันตรายมาก** ครับ

---

## 📚 สรุป

ในบทนี้เราได้เรียนรู้ว่า:

✅ **DHT11** คือเซ็นเซอร์วัดอุณหภูมิและความชื้นที่ใช้งานง่าย ราคาถูก สื่อสารผ่าน Single-Wire Protocol ที่ส่งข้อมูล 40 bits ทุกครั้ง

✅ การต่อ DHT11 กับ ESP32-C3 ทำได้ง่ายมาก เพียงต่อ 3 สาย (VCC, Data, GND) และถ้าใช้ Module ที่มี Resistor ติดมาแล้วก็ไม่ต้องต่ออะไรเพิ่ม

✅ การใช้ DHT Library ทำให้การอ่านค่าง่ายมาก เพียงใช้ `dht.readTemperature()` และ `dht.readHumidity()` แต่ต้องเช็ค `isnan()` เพราะถ้าอ่านไม่ได้จะได้ค่า NaN

✅ **Serial Monitor** ช่วยให้เรา Debug และดูข้อมูลได้แบบ Real-time พร้อมกับคำนวณ Heat Index เพื่อรู้ว่ารู้สึกร้อนแค่ไหน

✅ สามารถต่อ DHT11 กับ PlatformIO แบบ Modular ได้โดยแยกเป็น `dht_sensor.h` และ `dht_sensor.cpp` ทำให้โค้ดอ่านง่ายและนำไปใช้ใหม่ได้สะดวก

> 🔮 **บทต่อไป:** ในบทถัดไปเราจะมาเรียนรู้เรื่อง **LDR + OLED** กัน! เราจะได้รู้จักกับ LDR (ตัวต้านทานไวแสง) ที่วัดความสว่างได้ และ OLED ที่เป็นจอแสดงผลขนาดเล็ก มาประกอบกันสร้าง **เครื่องวัดความสว่าง (Lux Meter)** ที่สวยงามกัน! 💡🖥️

---

*📁 โค้ดตัวอย่าง: `/code/ch05_dht11/`*  
*🖼️ รูปประกอบ: `/images/ch05-dht11-*.png`*
