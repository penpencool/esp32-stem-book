# 🌡️ DHT11 — เซ็นเซอร์วัดอุณหภูมิและความชื้น

## DHT11 คืออะไร?

**DHT11** คือเซ็นเซอร์ที่วัดได้ 2 ค่า:
- **อุณหภูมิ** (Temperature)
- **ความชื้นสัมพัทธ์** (Humidity)

```
┌─────────────────┐
│                  │
│    DHT11        │
│                  │
│  ○ VCC (ขา1)   │  → เสียบ 3.3V หรือ 5V
│  ○ DATA (ขา2)  │  → ต่อกับ GPIO
│  ○ NC (ขา3)    │  → ไม่ต่อ
│  ○ GND (ขา4)   │  → ต่อ GND
│                  │
└─────────────────┘
```

## ข้อมูลจำเพาะ

| Spec | DHT11 |
|------|-------|
| ย่านอุณหภูมิ | 0-50°C |
| ความแม่นยำอุณหภูมิ | ±2°C |
| ย่านความชื้น | 20-90% RH |
| ความแม่นยำความชื้น | ±5% RH |
| แรงดัน | 3.3V - 5V |
| กระแส | 0.5-2.5mA |

## การต่อวงจร

```
    ESP32-C3           DHT11
    ┌─────────┐       ┌─────────┐
    │ 3.3V   ├───────┤ VCC     │
    │ GPIO 0 ├───────┤ DATA    │
    │         │       │ NC      │
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘
    
    ⚠️ ต้องมี Resistor 10kΩ ระหว่าง DATA กับ VCC
```

### วงจรเต็ม

```
    3.3V
      │
     [10kΩ]
      │
      ├──────── DATA (GPIO 0)
      │
     [DHT11]
      │
      └──────── GND
```

## การติดตั้ง Library

### PlatformIO (platformio.ini)

```ini
[env:esp32-c3-devkitm-1]
platform = espressif32
board = esp32-c3-devkitm-1
framework = arduino

lib_deps =
    adafruit/DHT sensor library
    adafruit/Adafruit Unified Sensor
```

### Arduino IDE

```
1. เปิด Arduino IDE
2. Sketch → Include Library → Manage Libraries
3. ค้นหา "DHT sensor library"
4. ติดตั้งโดย Adafruit
```

## โค้ดพื้นฐาน

### โค้ดที่ 1: อ่านค่าง่ายๆ

```cpp
#include <DHT.h>

#define DHT_PIN 0        // DATA pin
#define DHT_TYPE DHT11   // DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    
    Serial.println("DHT11 Ready!");
}

void loop() {
    // รออ่านค่า (ใช้เวลา ~250ms)
    delay(2000);
    
    // อ่านค่าอุณหภูมิ (Celsius)
    float temp = dht.readTemperature();
    
    // อ่านค่าความชื้น (Percent)
    float humidity = dht.readHumidity();
    
    // ตรวจสอบว่าอ่านได้มั้ย
    if (isnan(temp) || isnan(humidity)) {
        Serial.println("อ่านค่าผิดพลาด!");
        return;
    }
    
    // แสดงผล
    Serial.print("อุณหภูมิ: ");
    Serial.print(temp);
    Serial.println("°C");
    
    Serial.print("ความชื้น: ");
    Serial.print(humidity);
    Serial.println("%");
}
```

### โค้ดที่ 2: แสดงผลบน OLED

```cpp
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define DHT_PIN 0
#define DHT_TYPE DHT11

#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(128, 64, &Wire, -1);

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
    
    // เริ่ม OLED
    Wire.begin(0, 1);  // SDA, SCL
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
    delay(2000);
    
    float temp = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if (isnan(temp) || isnan(humidity)) {
        return;
    }
    
    // ล้างหน้าจอ
    display.clearDisplay();
    
    // ตั้งขนาดตัวอักษร
    display.setTextSize(2);
    display.setTextColor(WHITE);
    
    // พิมพ์อุณหภูมิ
    display.setCursor(0, 0);
    display.print("Temp: ");
    display.print(temp);
    display.println("C");
    
    // พิมพ์ความชื้น
    display.setCursor(0, 24);
    display.print("Humi: ");
    display.print(humidity);
    display.println("%");
    
    // แสดงผล
    display.display();
}
```

## การคำนวณ Heat Index

**Heat Index** คือ "อุณหภูมิที่รู้สึก" — รวมผลของความชื้นเข้าด้วย

```cpp
#include <DHT.h>

#define DHT_PIN 0
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    Serial.begin(115200);
    dht.begin();
}

void loop() {
    delay(2000);
    
    float tempC = dht.readTemperature();
    float humidity = dht.readHumidity();
    
    if (isnan(tempC) || isnan(humidity)) {
        return;
    }
    
    // อ่านเป็น Fahrenheit ก่อน (library ต้องการ)
    float tempF = dht.readTemperature(true);
    
    // คำนวณ Heat Index
    float heatIndex = dht.computeHeatIndex(tempF, humidity);
    
    // แปลงกลับเป็น Celsius
    float heatIndexC = (heatIndex - 32) * 5 / 9;
    
    Serial.print("อุณหภูมิจริง: ");
    Serial.print(tempC);
    Serial.println("C");
    
    Serial.print("รู้สึกเหมือน: ");
    Serial.print(heatIndexC);
    Serial.println("C");
}
```

## Heat Index Table

| °C | ความหมาย |
|----|----------|
| 27-32 | รู้สึกร้อนเล็กน้อย |
| 32-41 | ระวัง! อาจเหนื่อยมาก |
| 41-54 | **อันตราย!** ความร้อนจัด |
| >54 | **อันตรายสูง!** |

## การแก้ปัญหาที่พบบ่อย

### ปัญหา: อ่านค่าได้ NaN

```cpp
// ✅ วิธีตรวจสอบ
if (isnan(temp)) {
    Serial.println("Error: อ่านค่าผิดพลาด!");
    return;
}

// ❌ ไม่ควรทำ
Serial.println(temp);  // พิมพ์ NaN ออกมา
```

### ปัญหา: ค่าเพี้ยน

```
สาเหตุ:
1. ต่อสายไกลเกินไป (>20m)
2. แหล่งจ่ายไฟไม่ stable
3. ตัว DHT11 เก่า/เสีย

วิธีแก้:
1. เพิ่ม Capacitor 100µF ที่ VCC
2. ใช้ DHT22 แทน (แม่นยำกว่า)
3. เปลี่ยนตัวใหม่
```

## DHT11 vs DHT22

| Spec | DHT11 | DHT22 |
|------|--------|-------|
| ราคา | ~25฿ | ~100฿ |
| ย่านอุณหภูมิ | 0-50°C | -40-80°C |
| ความแม่นยำอุณหภูมิ | ±2°C | ±0.5°C |
| ย่านความชื้น | 20-90% | 0-100% |
| ความแม่นยำความชื้น | ±5% | ±2% |

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [OLED Display](../02-sensors/oled-display.md)
- [LDR Sensor](./ldr-sensor.md)
- [HC-SR04 Ultrasonic](./hc-sr04-sensor.md)
- [AI Prompt สำหรับเซ็นเซอร์](../06-ai-prompts/sensor-prompts.md)
