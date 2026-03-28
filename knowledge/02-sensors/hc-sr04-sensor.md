# 📏 HC-SR04 — เซ็นเซอร์วัดระยะด้วย Ultrasonic

## HC-SR04 คืออะไร?

**HC-SR04** ใช้คลื่นเสียง (ultrasonic) วัดระยะทาง

```
หลักการทำงาน:

1. ส่งคลื่นเสียงออกไป (TRIG)
2. คลื่นสะท้อนกลับจากวัตถุ
3. รับคลื่นที่สะท้อนกลับ (ECHO)
4. คำนวณระยะจากเวลา

เสียงเดินทาง ~343 เมตร/วินาที
```

## ข้อมูลจำเพาะ

| Spec | ค่า |
|------|-----|
| ย่านวัด | 2-400 cm |
| ความแม่นยำ | ±3mm |
| มุมวัด | 15° |
| แรงดัน | 5V DC |

## ⚠️ สำคัญ: HC-SR04 ต้องใช้ 5V!

```
HC-SR04 ให้ ECHO ออก 5V
แต่ ESP32-C3 รับได้แค่ 3.3V

⚠️ ต้องมี Voltage Divider!
```

## วงจร (พร้อม Voltage Divider)

```
    ESP32-C3           HC-SR04
    ┌─────────┐       ┌─────────┐
    │ 5V     ├───────┤ VCC     │
    │ GPIO 12├───────┤ TRIG    │
    │ GPIO 13├─┤1kΩ├──┤ ECHO   │──┤2kΩ├── GND
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘

Voltage Divider ลด 5V → 3.3V:
  Vout = 5V × (2kΩ / (1kΩ + 2kΩ)) = 3.33V ✓
```

## โค้ดพื้นฐาน

```cpp
#define TRIG_PIN 12
#define ECHO_PIN 13

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    // 1. ส่งคลื่น
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // 2. วัดเวลาที่คลื่นกลับมา
    long duration = pulseIn(ECHO_PIN, HIGH);
    
    // 3. คำนวณระยะ
    float distance = duration * 0.034 / 2;  // cm
    
    Serial.print("ระยะ: ");
    Serial.print(distance);
    Serial.println(" cm");
    
    delay(500);
}
```

## โค้ด: Parking Sensor (LED 4 สี)

```cpp
#define TRIG_PIN 12
#define ECHO_PIN 13
#define LED_GREEN  18
#define LED_YELLOW 19
#define LED_ORANGE  2
#define LED_RED     3

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_YELLOW, OUTPUT);
    pinMode(LED_ORANGE, OUTPUT);
    pinMode(LED_RED, OUTPUT);
}

void loop() {
    // วัดระยะ
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = duration * 0.034 / 2;
    
    // ปิด LED ทั้งหมดก่อน
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
    digitalWrite(LED_ORANGE, LOW);
    digitalWrite(LED_RED, LOW);
    
    // เปิด LED ตามระยะ
    if (distance < 10) {
        digitalWrite(LED_RED, HIGH);    // < 10cm = แดง อันตราย!
    } else if (distance < 25) {
        digitalWrite(LED_ORANGE, HIGH); // 10-25cm = ส้ม ใกล้มาก
    } else if (distance < 50) {
        digitalWrite(LED_YELLOW, HIGH);  // 25-50cm = เหลือง ระวัง
    } else if (distance < 100) {
        digitalWrite(LED_GREEN, HIGH);  // 50-100cm = เขียว ปลอดภัย
    }
    
    delay(100);
}
```

## โค้ด: แสดงผลบน OLED

```cpp
#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define TRIG_PIN 12
#define ECHO_PIN 13
#define OLED_ADDR 0x3C

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
    Wire.begin(0, 1);
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = duration * 0.034 / 2;
    
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.print("Distance:");
    display.setTextSize(3);
    display.setCursor(0, 30);
    display.print(distance);
    display.setTextSize(1);
    display.print(" cm");
    display.display();
    delay(200);
}
```

## สูตรคำนวณ

```
ระยะ = (ความเร็วเสียง × เวลา) / 2

โดย:
- ความเร็วเสียง = 0.034 cm/μs (ที่อุณหภูมิห้อง)
- เวลา = pulseIn() ได้เป็น μ�รวินาที
- หาร 2 = เพราะคลื่นไปและกลับ

หรือ:
ระยะ (cm) = duration / 58
```

## HC-SR04 vs HC-SR05 vs VL53L0X

| รุ่น | ย่านวัด | ความแม่นยำ | ราคา |
|------|---------|------------|------|
| **HC-SR04** | 2-400cm | ±3mm | ~35฿ |
| HC-SR05 | 2-300cm | ±3mm | ~50฿ |
| VL53L0X | 2-200cm | ±3mm | ~150฿ |

## การแก้ปัญหา

### ปัญหา: ค่า = 0 ตลอด

```
สาเหตุ: TRIG หรือ ECHO ต่อผิด

วิธีแก้:
1. เช็คว่าต่อ TRIG → GPIO Output
2. เช็คว่า ECHO → GPIO Input
3. เช็ค Voltage Divider ต่อถูกมั้ย?
```

### ปัญหา: ค่าผันผวนมาก

```
สาเหตุ: วัดวัตถุที่ไกลหรือดูดซับเสียง

วิธีแก้:
1. ใช้วัสดุที่สะท้อนเสียงได้ดี
2. เพิ่ม delay ระหว่างการวัด
3. หาค่าเฉลี่ยหลายครั้ง
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [DHT11 Sensor](./dht11-sensor.md)
- [LDR Sensor](./ldr-sensor.md)
- [OLED Display](./oled-display.md)
