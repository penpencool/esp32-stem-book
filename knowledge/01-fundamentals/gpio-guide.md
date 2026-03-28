# 🔌 GPIO Guide — การใช้ขา GPIO

## GPIO คืออะไร?

**GPIO (General Purpose Input/Output)** คือขาที่เราสามารถ:
- **Output** → ส่งสัญญาณออก (เช่น สั่ง LED ติด)
- **Input** → รับสัญญาณเข้า (เช่น อ่านสวิตช์กด)

```
┌──────────────────────────────────────┐
│           ESP32-C3 Chip               │
│                                      │
│   ┌────────┐                        │
│   │ GPIO 2 ├──────► LED ติด/ดับ   │  Output
│   └────────┘                        │
│                                      │
│   ┌────────┐                        │
│   │ GPIO 0 ├──────┤ สวิตช์ ───────┤  Input
│   └────────┘                        │
└──────────────────────────────────────┘
```

## โหมดการทำงานของ GPIO

### 1. Output Mode — ส่งสัญญาณออก

```cpp
// กำหนด GPIO 2 เป็น Output
pinMode(2, OUTPUT);

// สั่งให้ LED ติด (HIGH = 3.3V)
digitalWrite(2, HIGH);

// สั่งให้ LED ดับ (LOW = 0V)
digitalWrite(2, LOW);
```

### 2. Input Mode — รับสัญญาณเข้า

```cpp
// กำหนด GPIO 0 เป็น Input
pinMode(0, INPUT);

// อ่านค่าจากสวิตช์
int switchState = digitalRead(0);
// switchState = HIGH (1) = กด
// switchState = LOW (0) = ไม่กด
```

### 3. Input Pull-Up — มีตัวต้านทานภายใน

```cpp
// INPUT_PULLUP = ใช้ตัวต้านทานภายใน ในโหมด "ดึงขึ้น"
// ทำให้ไม่ต้องต่อ Resistor ภายนอก
pinMode(0, INPUT_PULLUP);

// วงจร:
// - กดสวิตช์ → ได้ค่า LOW (0)
// - ไม่กด → ได้ค่า HIGH (1)
```

## Analog vs Digital

### Digital Signal (0 หรือ 1)

```
        HIGH (3.3V)
          ─┐
          │ │
    LOW   │ │
   (0V)  │ │
    ─────┘ └──
          ▲
          │ 
       เวลา
       
รูปแบบ: สัญญาณไฟฟ้า 2 ระดับ = 0 หรือ 1
ใช้กับ: LED, สวิตช์, ปุ่มกด
```

### Analog Signal (0-1023 หรือ 0-4095)

```
     3.3V ─┐
           │  /
           │ /
     1.65V │/
           │ 
     0V ───┘
           ▲
           │ 
        เวลา
       
รูปแบบ: สัญญาณไฟฟ้าแบบต่อเนื่อง
ใช้กับ: LDR, Potentiometer, เซ็นเซอร์วัดค่าต่างๆ
```

## ADC — Analog to Digital Converter

ESP32-C3 มี ADC 12-bit ความละเอียด 4096 ระดับ

```cpp
// กำหนดขา GPIO 2 เป็น Input (ADC)
pinMode(2, INPUT);

// อ่านค่า Analog (0-4095)
int value = analogRead(2);

// ค่าที่ได้:
// 0 = 0V
// 2048 = 1.65V
// 4095 = 3.3V
```

### ESP32 vs ESP32-C3 ADC

| Spec | ESP32 | ESP32-C3 |
|-------|-------|----------|
| Resolution | 12-bit | 12-bit |
| Channels | 18 (ADC1 + ADC2) | 6 (ADC1) |
| Voltage | 0-3.3V | 0-3.3V |

> ⚠️ **ESP32-C3**: ADC2 ไม่สามารถใช้ขณะใช้ WiFi ได้

## PWM — Pulse Width Modulation

PWM ใช้ "ปิด-เปิด" สัญญาณเร็วๆ เพื่อจำลอง Analog

```
Duty Cycle = สัดส่วนที่สัญญาณเป็น HIGH

0%   (LED ดับสนิท)
████

25%  (LED สว่าง 25%)
██░░

50%  (LED สว่าง 50%)
█░░░

100% (LED ติดสว่างสุด)
░░░░
```

### การใช้ PWM กับ LED (LEDC)

```cpp
// กำหนด LED ที่ GPIO 2
#define LED_PIN 2
#define LED_CHANNEL 0

void setup() {
    // ตั้งค่า PWM
    ledcSetup(LED_CHANNEL, 5000, 8);  // 5kHz, 8-bit (0-255)
    ledcAttachPin(LED_PIN, LED_CHANNEL);
}

void loop() {
    // หรี่ไฟค่อยๆ (fade in)
    for (int brightness = 0; brightness <= 255; brightness++) {
        ledcWrite(LED_CHANNEL, brightness);  // 0-255
        delay(10);
    }
    
    // หรี่ไฟค่อยๆ (fade out)
    for (int brightness = 255; brightness >= 0; brightness--) {
        ledcWrite(LED_CHANNEL, brightness);
        delay(10);
    }
}
```

## I2C — การสื่อสารแบบอนุกรม

I2C ใช้ 2 สาย:
- **SDA** (Serial Data) — ข้อมูล
- **SCL** (Serial Clock) — สัญญาณนาฬิกา

```
ESP32-C3                          อุปกรณ์
┌─────────┐                      ┌─────────┐
│ GPIO 0  ├────── SDA ───────────┤ OLED    │
│ GPIO 1  ├────── SCL ───────────┤         │
└─────────┘                      └─────────┘
```

### การต่อ I2C

```cpp
// เริ่มใช้ I2C
#include <Wire.h>

void setup() {
    Wire.begin(0, 1);  // SDA=GPIO 0, SCL=GPIO 1
}
```

### I2C Address ที่ใช้บ่อย

| อุปกรณ์ | I2C Address |
|---------|-------------|
| OLED 0.96" (SSD1306) | 0x3C |
| OLED 0.96" (SSD1306) | 0x3D |
| DHT11 | 0x00 (ไม่ใช้ I2C) |

## สรุป GPIO ที่แนะนำ

```
✅ GPIO ที่ใช้บ่อย:

Digital I/O:  GPIO 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
ADC (Analog): GPIO 0, 2, 3, 4, 5
I2C:          GPIO 0 (SDA), GPIO 1 (SCL)

⚠️ GPIO ที่ควรหลีกเลี่ยง:

GPIO 6-11: SPI Flash (หลีกเลี่ยง!)
GPIO 4-5:  Strapping pins (ระวังตอน boot)
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [ESP32-C3 พื้นฐาน](./esp32c3-basics.md)
- [วงจรพื้นฐาน](./circuit-basics.md)
- [เซ็นเซอร์ LDR](../02-sensors/ldr-sensor.md)
- [เซ็นเซอร์ DHT11](../02-sensors/dht11-sensor.md)
