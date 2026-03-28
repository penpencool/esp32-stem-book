# 💡 LDR — ตัวต้านทานไวแสง

## LDR คืออะไร?

**LDR (Light Dependent Resistor)** คือตัวต้านทานที่ค่าเปลี่ยนตามแสง

```
LDR ทำงานยังไง:

แสงจ้า → ความต้านทานต่ำ → ค่า ADC สูง
มืด → ความต้านทานสูง → ค่า ADC ต่ำ
```

## ข้อมูลจำเพาะ

| Spec | ค่า |
|------|-----|
| ย่านแสง | 10-1000 Lux |
| ความต้านทาน (แสงจ้า) | 10-100Ω |
| ความต้านทาน (มืด) | 1MΩ |
| เวลาตอบสนอง | 20-30ms |

## การต่อวงจร (Voltage Divider)

```
    3.3V
      │
     [10kΩ]  (Resistor คงที่)
      │
      ├──────── GPIO 2 (ADC)
      │
     [LDR]   (ความต้านทานเปลี่ยนตามแสง)
      │
     GND

ค่าที่อ่านได้: 0-4095 (12-bit ADC)
```

## โค้ดพื้นฐาน

```cpp
#define LDR_PIN 2  // ADC pin

void setup() {
    Serial.begin(115200);
}

void loop() {
    int light = analogRead(LDR_PIN);  // 0-4095
    
    // แปลงเป็น %
    int percent = map(light, 0, 4095, 0, 100);
    
    Serial.print("แสง: ");
    Serial.print(percent);
    Serial.println("%");
    
    delay(500);
}
```

## โค้ด: เปิดไฟอัตโนมัติ

```cpp
#define LDR_PIN 2
#define LED_PIN 12

void setup() {
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    int light = analogRead(LDR_PIN);
    int percent = map(light, 0, 4095, 0, 100);
    
    // ถ้าแสงต่ำกว่า 20% ให้เปิดไฟ
    if (percent < 20) {
        digitalWrite(LED_PIN, HIGH);  // เปิดไฟ
    } else {
        digitalWrite(LED_PIN, LOW);   // ปิดไฟ
    }
}
```

## โค้ด: หรี่ไฟตามแสง (LED PWM)

```cpp
#define LDR_PIN 2
#define LED_PIN 12
#define LED_CHANNEL 0

void setup() {
    ledcSetup(LED_CHANNEL, 5000, 8);
    ledcAttachPin(LED_PIN, LED_CHANNEL);
}

void loop() {
    int light = analogRead(LDR_PIN);
    
    // แสงน้อย = ไฟสว่าง = duty สูง
    // แสงมาก = ไฟมืด = duty ต่ำ
    int brightness = map(light, 0, 4095, 255, 0);
    
    ledcWrite(LED_CHANNEL, brightness);
    delay(100);
}
```

## โค้ด: แสดงผลบน OLED

```cpp
#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define LDR_PIN 2
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
    Wire.begin(0, 1);
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
    int light = analogRead(LDR_PIN);
    int percent = map(light, 0, 4095, 0, 100);
    
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("Light: ");
    display.print(percent);
    display.print("%");
    
    // วาด progress bar
    int barWidth = map(percent, 0, 100, 0, 120);
    display.drawRect(4, 30, 120, 20, WHITE);
    display.fillRect(4, 30, barWidth, 20, WHITE);
    
    display.display();
    delay(200);
}
```

## การ Calibrate LDR

```cpp
// หาค่า Min/Max จริง
void loop() {
    int raw = analogRead(LDR_PIN);
    static int minVal = 4095;
    static int maxVal = 0;
    
    if (raw < minVal) minVal = raw;
    if (raw > maxVal) maxVal = raw;
    
    Serial.print("Min: "); Serial.print(minVal);
    Serial.print(" Max: "); Serial.println(maxVal);
}
```

## LDR vs Photodiode vs Phototransistor

| ชนิด | ข้อดี | ข้อเสีย |
|------|--------|----------|
| **LDR** | ราคาถูก, ง่าย | ช้า |
| Photodiode | เร็ว, แม่น | ต้องใช้วงจรเพิ่ม |
| Phototransistor | เร็ว, ไว | ต้องใช้วงจรเพิ่ม |

## การใช้ LDR ในโปรเจกต์

### Smart Street Light
```
แสงน้อย → เปิดไฟถนนอัตโนมัติ
```

### Night Light
```
มืด → เปิดไฟหัวใจเล็กๆ
```

### Sun Tracker
```
หมุน Servo ตามแสงอาทิตย์
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [DHT11 Sensor](./dht11-sensor.md)
- [HC-SR04 Ultrasonic](./hc-sr04-sensor.md)
- [OLED Display](./oled-display.md)
