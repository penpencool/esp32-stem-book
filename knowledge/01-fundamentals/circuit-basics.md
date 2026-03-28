# ⚡ วงจรพื้นฐาน

## องค์ประกอบพื้นฐาน

### 1. LED (Light Emitting Diode)

```
ขั้วของ LED:
  ┌──┐
  │  │  ──── ขาเสี้ยวยาว = Anode (+)
  │  │  ──── ขาสั้น = Cathode (-)
  └──┘
     │
     └──── ฐานกลม
     
สัญลักษณ์:
    ──►┃  (แสดงทิศทางการไหล)
```

### 2. Resistor (ตัวต้านทาน)

Resistor ใช้จำกัดกระแสไม่ให้ LED พัง

```
สี Resistor (4 Band):
  น้ำตาล = 1
  แดง    = 2
  แดง    = 2
  น้ำตาล = ×10¹

  น้ำตาล-แดง-แดง-น้ำตาล = 1.2kΩ

ตารางสี Resistor:
  ┌────────┬───────┐
  │ สี      │ ค่า   │
  ├────────┼───────┤
  │ ดำ      │ 0     │
  │ น้ำตาล  │ 1     │
  │ แดง     │ 2     │
  │ ส้ม     │ 3     │
  │ เหลือง  │ 4     │
  │ เขียว   │ 5     │
  │ น้ำเงิน │ 6     │
  │ ม่วง    │ 7     │
  │ เทา     │ 8     │
  │ ขาว     │ 9     │
  │ ทอง     │ ×0.1  │
  │ ไม่มี   │ ±20%  │
  └────────┴───────┘
```

### 3. สวิตช์/ปุ่มกด

```
สวิตช์ 4 ขา (จริง):
   ┌──────────┐
   │  ○    ○  │
   │  ○    ○  │
   └──────────┘
   
   ขา A ──┬──┐
           │  ├─── ขา B (ต่อกันเมื่อกด)
   ขา C ──┴──┘
           │  ├─── ขา D (ต่อกันเมื่อกด)

วงจร:
   GPIO ──┤SW├─── GND
           │
      (INPUT_PULLUP)
```

## วงจร LED พื้นฐาน

### LED + Resistor (แบบ Basic)

```
    3.3V
      │
      ├──────┐
      │      │
     [R]    │   R = 220Ω - 1kΩ
      │      │
      └──────┼────── GPIO (Output)
             │
            LED
             │
            GND
```

### LED + ESP32-C3 (โค้ด)

```cpp
// ต่อ: 3.3V --- Resistor --- LED --- GPIO 2

#define LED_PIN 2

void setup() {
    pinMode(LED_PIN, OUTPUT);  // ตั้งค่าเป็น Output
}

void loop() {
    digitalWrite(LED_PIN, HIGH);  // LED ติด
    delay(1000);                   // รอ 1 วินาที
    digitalWrite(LED_PIN, LOW);   // LED ดับ
    delay(1000);                   // รอ 1 วินาที
}
```

## วงจรสวิตช์ Input

### สวิตช์กด (INPUT_PULLUP)

```
    ESP32-C3
    ┌─────────┐
    │  GPIO 0 ├────────┐
    │         │        │
    │         │    ┌───┴───┐
    │         │    │ SW    │  (ปุ่มกด)
    │         │    └───┬───┘
    │         │        │
    │     GND ├────────┘
    └─────────┘
    
    เมื่อกด: GPIO 0 = LOW (0V)
    เมื่อไม่กด: GPIO 0 = HIGH (3.3V จาก pull-up)
```

### โค้ดสวิตช์

```cpp
#define SW_PIN 0

void setup() {
    Serial.begin(115200);
    pinMode(SW_PIN, INPUT_PULLUP);  // ใช้ pull-up ภายใน
}

void loop() {
    int state = digitalRead(SW_PIN);
    
    if (state == LOW) {
        Serial.println("สวิตช์ถูกกด!");
    } else {
        Serial.println("สวิตช์ไม่ได้กด");
    }
    delay(100);
}
```

## วงจรอนุกรม vs วงจรขนาน

### วงจรอนุกรม (Series)

```
    3.3V
      │
     [R1]──┬──[LED1]──┬──[LED2]──┐
            │          │          │
            └──────────┴──────────┘
                      GND

กระแสไหลผ่านทุกอุปกรณ์เท่ากัน
ค่ารวม: R รวม = R1 + R2
```

### วงจรขนาน (Parallel)

```
    3.3V
      │
      ├──────[R1]──[LED1]──┬── GND
      │
      ├──────[R2]──[LED2]──┘
      │
      └──────[R3]──[LED3]──┘

กระแสแยกไหล แต่แรงดันเท่ากัน
ค่ารวม: 1/R รวม = 1/R1 + 1/R2 + 1/R3
```

## วงจร LDR (ตัวต้านทานไวแสง)

### Voltage Divider (แบ่งแรงดัน)

```
    3.3V
      │
     [R]  10kΩ (Resistor คงที่)
      │
      ├──────── GPIO (Analog Input)
      │
     [LDR]  (ความต้านทานเปลี่ยนตามแสง)
      │
      └──────── GND

ค่าที่อ่านได้:
- แสงจ้า: LDR มีค่าต่ำ → Vout สูง → ค่า ADC สูง
- มืด: LDR มีค่าสูง → Vout ต่ำ → ค่า ADC ต่ำ
```

### โค้ด LDR

```cpp
#define LDR_PIN 2  // ADC pin

void setup() {
    Serial.begin(115200);
    pinMode(LDR_PIN, INPUT);
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

## วงจร Relay

> ⚠️ **ความปลอดภัย**: ต่อ 220V ได้แค่ผ่าน Relay เท่านั้น!

### Relay Module 2 Channel

```
    ESP32-C3          Relay Module
    ┌─────────┐       ┌─────────┐
    │ GPIO 12 ├───────┤ IN1     │
    │ GPIO 13 ├───────┤ IN2     │
    │ 5V      ├───────┤ VCC     │
    │ GND     ├───────┤ GND     │
    └─────────┘       └─────────┘
                            │
                    ┌──────┴──────┐
                    │ COM    NO   │  (ช่อง NO = ต่อเมื่อ Relay ทำงาน)
                    │         NC   │  (ช่อง NC = ต่ออยู่ตลอด)
                    └──────┬──────┘
                           │
                      อุปกรณ์ไฟฟ้า
                      (พัดลม/หลอดไฟ)
                           │
                          220V
```

### โค้ด Relay

```cpp
#define RELAY1 12
#define RELAY2 13

void setup() {
    pinMode(RELAY1, OUTPUT);
    pinMode(RELAY2, OUTPUT);
    
    // เริ่มต้น: ปิด Relay ทั้ง 2 ช่อง
    digitalWrite(RELAY1, LOW);
    digitalWrite(RELAY2, LOW);
}

void loop() {
    // เปิด Relay 1
    digitalWrite(RELAY1, HIGH);
    delay(2000);
    
    // ปิด Relay 1
    digitalWrite(RELAY1, LOW);
    delay(2000);
}
```

## สรุปความปลอดภัย

```
⚠️ ข้อควรระวัง:

1. ห้ามต่อ 220V โดยตรงกับ ESP32!
2. ใช้ Relay เป็นตัวกลางเสมอ
3. ต่อวงจรขณะปิดไฟเสมอ
4. ตรวจสอบขั้ว + ก่อนจ่ายไฟ
5. มีผู้ใหญ่ดูแลเมื่อใช้ไฟสูง

✅ ทำได้เลย (ไม่ต้องใช้ Relay):

- LED (ผ่าน Resistor)
- สวิตช์/ปุ่มกด
- เซ็นเซอร์ (DHT11, LDR, HC-SR04)
- Servo Motor (12V หรือต่ำกว่า)
- OLED Display
- Buzzer
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [ESP32-C3 พื้นฐาน](./esp32c3-basics.md)
- [GPIO Guide](./gpio-guide.md)
- [Relay Module](../03-actuators/relay-module.md)
- [Servo Motor](../03-actuators/servo-motor.md)
