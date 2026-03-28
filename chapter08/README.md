# 🎯 สิ่งที่จะเรียนรู้

ในบทนี้ เราจะได้เรียนรู้:

- [ ] Infrared (IR) คืออะไร — แสงที่ตาไม่เห็น
- [ ] โปรโตคอล NEC IR คืออะไร และทำงานยังไง
- [ ] วิธีต่อ IR Receiver กับ ESP32-C3
- [ ] ถอดรหัสรีโมททีวี — อ่านค่า Hex จากรีโมทจริง
- [ ] ปฏิบัติ: สั่งเปิด-ปิด LED ด้วยรีโมท
- [ ] ปฏิบัติ: สร้างรีโมทคอนโทรลเซ็นเซอร์หลายตัว

---

## 📖 บทนำ

> "เคยสงสัยมั้ยเล่า ทำไมรีโมททีวีถึงสื่อสารกับทีวีได้โดยไม่ต้องเชื่อมสาย? ทำไมเปิดปิดไฟด้วยรีโมทถึงส่งสัญญาณไปถึงเพียงมุมห้องเดียว? และทำไมรีโมทไม่ทำงานเมื่อแบตเตอรี่อ่อน? 🤔"
>
> "คำตอบทั้งหมดอยู่ที่ **แสง Infrared หรือ IR** — แสงที่ตามนุษย์ไม่เห็น แต่อุปกรณ์อิเล็กทรอนิกส์สามารถ 'มองเห็น' ได้! ในบทนี้เราจะมาจับสัญญาณ IR จากรีโมททีวีที่บ้าน แล้วเอามาควบคุม ESP32-C3 กัน!"

---

## 🔧 อุปกรณ์ที่ใช้

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก |
| IR Receiver (VS1838B หรือ IRM-5638) | 1 ตัว | รับสัญญาณ IR |
| LED สีแดง | 2 ตัว | แสดงสถานะ |
| LED สีเขียว | 2 ตัว | แสดงสถานะ |
| Resistor 220Ω | 4 ตัว | ป้องกัน LED ขาด |
| DHT11 (Temperature & Humidity Sensor) | 1 ตัว | วัดอุณหภูมิ/ความชื้น |
| Servo Motor SG90 | 1 ตัว | สำหรับโปรเจกต์ที่ 2 |
| สายจัมเปอร์ | หลายเส้น | |
| Breadboard | 1 อัน | สำหรับต่อวงจร |
| รีโมททีวีหรือรีโมทอะไรก็ได้ | 1 อัน | สำหรับส่งสัญญาณ IR |
| Power Supply 5V | 1 ชุด | จ่ายไฟให้ Servo (ถ้าใช้) |

---

## 💻 เนื้อหา

### 🔹 Infrared (IR) คืออะไร? — แสงที่ตาไม่เห็น 👁️

#### 🌀 IR คือแสงที่อยู่นอกสเปกตรัมที่ตามองเห็น

แสงที่ตามนุษย์เห็นได้ มีความยาวคลื่นอยู่ในช่วงประมาณ **400-700 นาโนเมตร (nm)** ซึ่งรวมถึงสีม่วง คราม น้ำเงิน เขียว เหลือง ส้ม แดง (VIBGYOR) แต่ **Infrared (IR)** มีความยาวคลื่น **ยาวกว่าแสงแดง** อยู่ที่ประมาณ **700nm - 1,000,000nm (1mm)** ทำให้ตามนุษย์ไม่เห็น แต่เซมิคอนดักเตอร์สามารถตรวจจับได้!

```
    ความยาวคลื่น: สั้น ◄────────────────────────────────► ยาว

    ▼▼▼▼▼▼▼  ▼▼▼▼▼▼▼  ▼▼▼▼▼▼▼▼▼  ▼▼▼▼▼▼▼▼▼▼▼▼  ████████
    ม่วง      แดง       IR-A       IR-B         IR-C
    400nm    700nm     1400nm      3000nm       1000000nm

    ◄──────── ตามองเห็น ────────►   ◄────  Infrared  ────►
```

> 💡 **รู้มั้ย?** ความร้อนที่เรารู้สึกจากไฟ หรือแสงอาทิตย์ ก็มี Infrared เป็นส่วนประกอบ! ทุกสิ่งที่มีความร้อนจะปล่อยรังสี IR ออกมา

#### 📡 วิธีการส่งสัญญาณ IR

ในรีโมทจะมี **IR LED** (Light Emitting Diode) ที่เมื่อเรากดปุ่ม จะส่งแสง IR ออกไปเป็น **พัลส์ (Pulse)** ติดๆ ดับๆ ด้วยความถี่ประมาณ **38kHz - 40kHz** (ความถี่นี้เรียกว่า Carrier Frequency)

ทำไมต้องเป็นพัลส์? เพราะว่า:
1. **แยกแยะได้** — ถ้าส่งต่อเนื่องจะตรวจไม่ได้ว่าคือสัญญาณจริงหรือแค่แสงแวดล้อม
2. **ประหยัดพลังงาน** — LED ติดแค่บางส่วน แบตเตอรี่ใช้ได้นานขึ้น
3. **ต้านทานสัญญาณรบกวน** — ระบบเลือกรับเฉพาะความถี่ 38kHz พอดี

```
📌 จุดสำคัญ:
- IR LED ส่งสัญญาณเป็นพัลส์ที่ความถี่ 38kHz
- IR Receiver รับและถอดรหัสสัญญาณที่ความถี่ 38kHz
- IR ส่งได้ไกลสุดประมาณ 10-15 เมตร (ตรงไปตรงมา)
```

#### 🔍 IR Receiver (ตัวรับ)

IR Receiver ที่เราจะใช้เป็นแบบ **38kHz Carrier demodulating** ซึ่งจะ:
- รับสัญญาณ IR ที่ความถี่ 38kHz
- ถอด Carrier ออก เหลือแค่ข้อมูลดิจิทัล (0 กับ 1)
- ส่งออกเป็นสัญญาณดิจิทัลที่ GPIO Pin

IR Receiver มี 3 ขา:
| ขา | หน้าที่ | สีสายทั่วไป |
|----|--------|------------|
| VCC (+5V หรือ +3.3V) | ไฟเลี้ยง | แดง |
| GND | กราวด์ | ดำ/น้ำตาล |
| OUT (Signal) | สัญญาณออก | ขาว/เหลือง |

```
⚠️ คำเตือน:
- IR Receiver บางรุ่นใช้ไฟ 5V บางรุ่นใช้ 3.3V
- VS1838B ใช้ได้ทั้ง 3.3V และ 5V (เหมาะกับ ESP32-C3!)
- อย่าสับสนระหว่าง IR Receiver กับ IR Transmitter (LED)
```

### 🔹 โปรโตคอล NEC IR 📜

NEC เป็น **โปรโตคอล IR** ที่นิยมใช้มากที่สุดในรีโมททีวีและเครื่องใช้ไฟฟ้าต่างๆ พัฒนาโดยบริษัท NEC Corporation ของญี่ปุ่น

#### โครงสร้างสัญญาณ NEC

สัญญาณ NEC แต่ละครั้งที่ส่ง จะประกอบด้วย:

```
1. Leader Code (สัญญาณนำ)     =  9ms ON + 4.5ms OFF
2. Address (8 bits)            =  รหัสอุปกรณ์ (Device ID)
3. Command (8 bits)            =  รหัสคำสั่ง (ปุ่มที่กด)
4. Command inverted (8 bits)  =  รหัสผกผัน (ตรวจสอบความถูกต้อง)
```

**ตัวอย่าง:** ถ้าเรากดปุ่ม "1" บนรีโมท NEC จะส่ง:
- Address: `0x00` (ทีวียี่ห้อนั้น)
- Command: `0x01` (ปุ่ม 1)

และส่ง **2 ครั้ง** ซ้ำกันในการกด 1 ครั้ง (ครั้งแรกเป็นคำสั่งจริง ครั้งที่สองเป็น Repeat Code)

```
    ┌─────────────────────────┐
    │ Leader: 9ms ON 4.5ms OFF│
    ├─────────────────────────┤
    │ Address: 8 bits         │
    ├─────────────────────────┤
    │ Command: 8 bits         │
    ├─────────────────────────┤
    │ Command inverted: 8 bits │
    └─────────────────────────┘
```

#### วิธีเข้ารหัส Bit (Encoding)

NEC ใช้ **Pulse Distance Encoding** หมายความว่า ระยะห่างระหว่างพัลส์ จะบอกว่าเป็น bit 0 หรือ bit 1

```
    Bit "0":  560μs ON  +  560μs OFF  =  1120μs รวม
    Bit "1":  560μs ON  + 1690μs OFF  =  2250μs รวม
```

```
    Bit 0:   ████        ████
             ───┐  560μs ┌───  560μs ────┐
                 └───────┘                └────────

    Bit 1:   ████                              ████
             ───┐  560μs ┌──────────────────┐  1690μs
                 └───────┘                  └────────
```

```
📌 จุดสำคัญ:
- Leader Code = บอกว่าเริ่มส่งแล้วนะ
- Address = บอกว่าสัญญาณนี้สำหรับอุปกรณ์ไหน (เช่น ทีวี, แอร์, กล่องดิจิทัล)
- Command = บอกว่ากดปุ่มอะไร (เช่น 1, 2, VOL+, CH-)
- Inverted Command = ตรวจสอบว่าสัญญาณไม่ผิดพลาด
```

### 🔹 วิธีต่อ IR Receiver กับ ESP32-C3 🔌

การต่อ IR Receiver กับ ESP32-C3 ง่ายมาก! เราต่อแค่ 3 สายเท่านั้น

```
    ESP32-C3                 IR Receiver
    ┌─────────┐            ┌───────────┐
    │      3V3├────────────│○ VCC      │
    │      GND├────────────│○ GND     │
    │   GPIO5 ├────────────│○ OUT     │
    └─────────┘            └───────────┘
```

**สรุปการต่อสาย:**

| IR Receiver | ESP32-C3 |
|------------|---------|
| VCC | 3V3 |
| GND | GND |
| OUT (Signal) | GPIO 5 |

> 💡 **เคล็ดลับ:** IR Receiver ส่วนใหญ่มีขาสัญญาณอยู่ตรงกลาง เวลามองด้านหน้า (มี lens โปร่ง) ขาซ้าย = VCC, ขากลาง = GND, ขาขวา = OUT

```
⚠️ ตรวจสอบขาของ IR Receiver ให้ถูกต้อง!
IR Receiver บางรุ่นมีลำดับขาไม่เหมือนกัน ควรตรวจสอบจาก Datasheet
หรือใช้มัลติมิเตอร์วัดหาขา VCC-GND (จะมีค่าความต้านทานประมาณ 100kΩ ระหว่าง VCC กับ GND)
```

### 🔹 ถอดรหัสรีโมททีวี — อ่านค่า Hex 🔎

ก่อนจะเขียนโค้ดควบคุมอะไร เราต้องรู้ก่อนว่าแต่ละปุ่มบนรีโมทส่งค่าอะไรออกมา ใน Arduino IDE มี **ตัวอย่างโค้ด IRrecvDumpV2** ที่จะช่วยถอดรหัสให้เรา!

#### ขั้นตอนที่ 1: ติดตั้ง Library

1. เปิด Arduino IDE
2. ไปที่ **Sketch → Include Library → Manage Libraries**
3. พิมพ์ **"IRremote"** ในช่องค้นหา
4. เลือก **IRremote** โดย shirriff (เป็น library ที่รองรับ ESP32 รวมถึง ESP32-C3)
5. กด **Install**

> ⚠️ **หมายเหตุสำคัญ:** ห้ามใช้ Library "IRremoteESP8266" กับ ESP32-C3 เด็ดขาด! ❌
> 
> Library `IRremoteESP8266` ออกแบบมาสำหรับ **ESP8266** เท่านั้น ไม่รองรับ ESP32-C3
> 
> สำหรับ ESP32-C3 ให้ใช้ Library `IRremote` (ไม่มี ESP8266 ต่อท้าย) ✅

#### ขั้นตอนที่ 2: อัปโหลดโค้ดถอดรหัส

ไปที่ **File → Examples → IRremote → IRrecvDumpV2**

```cpp
// ============================================
// บทที่ 8: ถอดรหัส IR Remote
// ============================================

#include <Arduino.h>
#include <IRrecv.h>
#include <IRremote.h>
#include <IRac.h>
#include <IRtext.h>

// ==== กำหนดขา ====
#define IR_PIN    5   // IR Receiver OUT → GPIO 5

// ==== สร้างอ็อบเจ็กต์ IR Receiver ====
// Buffer ขนาด 100 จะเก็บสัญญาณได้ 100 ครั้ง
IRrecv irrecv(IR_PIN, 100, 38, true);

decode_results results;  // ตัวแปรเก็บผลถอดรหัส

void setup() {
  Serial.begin(115200);
  Serial.println();
  Serial.println("=== IR Remote Decoder ===");
  Serial.println("กดปุ่มรีโมทแล้วดูค่าใน Serial Monitor");
  Serial.println();

  // เริ่มรับสัญญาณ IR
  irrecv.enableIRIn();
}

void loop() {
  // ถ้ามีสัญญาณ IR เข้ามา
  if (irrecv.decode(&results)) {

    // แสดงข้อมูลพื้นฐาน
    Serial.print("Protocol: ");
    Serial.println(results.protocolname);  // เช่น NEC, SONY, RC5

    Serial.print("Value:    0x");
    Serial.println(results.value, HEX);     // ค่า Hex หลัก

    Serial.print("Address:  0x");
    Serial.println(results.address, HEX);  // รหัสอุปกรณ์

    Serial.print("Command: 0x");
    Serial.println(results.command, HEX);   // รหัสปุ่ม

    Serial.print("Raw: (");
    Serial.print(results.rawlen - 1);       // จำนวนข้อมูลดิบ
    Serial.println(" ticks)");

    // ถ้าเป็น NEC Protocol
    if (results.decode_type == NEC) {
      Serial.println("✅ เป็นโปรโตคอล NEC!");
    }

    Serial.println("----------------------------");
    Serial.println();

    // รับสัญญาณต่อไป
    irrecv.resume();
  }

  delay(100);
}
```

#### ขั้นตอนที่ 3: ทดสอบถอดรหัส

1. **อัปโหลดโค้ด** ไปที่ ESP32-C3
2. **เปิด Serial Monitor** ที่ 115200 baud
3. **กดปุ่มต่างๆ** บนรีโมททีวี หันรีโมทเข้าหา IR Receiver
4. **บันทึกค่า Hex** ของแต่ละปุ่มที่เราต้องการใช้

**ตัวอย่างผลลัพธ์ที่ได้:**

```
=== IR Remote Decoder ===
Protocol: NEC
Value:    0x20DF10EF
Address:  0x101
Command: 0x10
✅ เป็นโปรโตคอล NEC!
----------------------------

Protocol: NEC
Value:    0x20DF807F
Address:  0x101
Command: 0x7F
----------------------------
```

> 💡 **เคล็ดลับ:** ค่า `Value` ที่ได้มาจะมี 32 bits (8 ตัวอักษร Hex) สำหรับ NEC แบบเต็ม ถ้าเป็น Repeat Code ค่าจะเป็น `0xFFFFFFFF`

```
📌 ตารางบันทึกค่ารีโมท:

ปุ่ม          | Address  | Command | ค่า Value ที่อ่านได้
-------------|----------|---------|------------------
Power        | 0x101    | 0x10    | 0x20DF10EF
Volume +     | 0x101    | 0x08    | 0x20DF807F
Volume -     | 0x101    | 0x88    | 0x20DF40BF
Channel +    | 0x101    | 0x00    | 0x20DF807F
Channel -    | 0x101    | 0x01    | 0x20DF40BF
(บันทึกค่าจริงของรีโมทที่ใช้จริง!)
```

---

## 🔨 ปฏิบัติ (พร้อมโค้ด)

### 🛠️ ปฏิบัติที่ 1: สั่งเปิด-ปิด LED ด้วยรีโมท 💡

โปรเจกต์แรกง่ายๆ: กดปุ่ม Power → LED ติด กดอีกครั้ง → LED ดับ เหมือนเปิด-ปิดไฟบ้านเลย! 🔌

#### ขั้นตอนที่ 1: ต่อวงจร

```
    ESP32-C3
    ┌────────────────────────────────────────┐
    │  3V3  ──┬──► IR Receiver VCC            │
    │  GND  ──┴──► IR Receiver GND            │
    │  GPIO5 ──────► IR Receiver OUT          │
    │  GPIO18 ─────► LED1 เขียว (ผ่าน R220Ω)   │
    │  GPIO19 ─────► LED2 แดง (ผ่าน R220Ω)    │
    └────────────────────────────────────────┘
```

#### ขั้นตอนที่ 2: เขียนโค้ด

```cpp
// ============================================
// บทที่ 8: สั่งเปิด-ปิด LED ด้วยรีโมท
// ============================================

#include <Arduino.h>
#include <IRrecv.h>
#include <IRremote.h>
#include <IRac.h>
#include <IRtext.h>

// ==== กำหนดขา ====
#define IR_PIN        5   // IR Receiver OUT → GPIO 5
#define LED_GREEN_PIN 18  // LED เขียว → GPIO 18
#define LED_RED_PIN   19  // LED แดง → GPIO 19

// ==== กำหนดค่า Hex ของรีโมท (แก้ตามค่าจริงที่ถอดรหัสได้!) ====
// ค่าตัวอย่างจากรีโมททีวี (เปลี่ยนตามรีโมทจริงที่ใช้)
#define IR_POWER    0x20DF10EF  // ปุ่ม Power
#define IR_VOL_UP   0x20DF807F  // ปุ่ม Volume +
#define IR_VOL_DOWN 0x20DF40BF  // ปุ่ม Volume -

// ==== สร้างอ็อบเจ็กต์ ====
IRrecv irrecv(IR_PIN, 100, 38, true);
decode_results results;

// ==== สถานะ ====
bool ledState = false;  // false = ปิด, true = ติด

void setup() {
  Serial.begin(115200);
  Serial.println("=== IR Remote: LED Control ===");

  // ตั้งค่า LED
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);
  digitalWrite(LED_GREEN_PIN, LOW);   // เริ่มติด
  digitalWrite(LED_RED_PIN, HIGH);    // LED แดงดับ

  // เริ่มรับ IR
  irrecv.enableIRIn();

  Serial.println("พร้อมรับคำสั่งจากรีโมท (กดปุ่ม Power)");
}

void loop() {
  // ถ้ามีสัญญาณ IR เข้ามา
  if (irrecv.decode(&results)) {

    // แสดงค่าที่รับได้ (ดีบัก)
    Serial.print("รับค่า: 0x");
    Serial.println(results.value, HEX);

    // ตรวจสอบว่าเป็นค่าที่เราสนใจหรือไม่
    switch (results.value) {

      // ===== ปุ่ม Power → สลับเปิด/ปิด =====
      case IR_POWER:
        ledState = !ledState;  // สลับสถานะ

        if (ledState) {
          digitalWrite(LED_GREEN_PIN, HIGH);  // เปิดไฟเขียว
          digitalWrite(LED_RED_PIN, LOW);     // ดับไฟแดง
          Serial.println("💡 เปิดไฟ!");
        } else {
          digitalWrite(LED_GREEN_PIN, LOW);    // ดับไฟเขียว
          digitalWrite(LED_RED_PIN, HIGH);     // เปิดไฟแดง
          Serial.println("💡 ปิดไฟ!");
        }
        break;

      // ===== ปุ่ม Volume+ → ไฟเขียวกระพริบ =====
      case IR_VOL_UP:
        Serial.println("🔊 Volume UP!");
        for (int i = 0; i < 3; i++) {
          digitalWrite(LED_GREEN_PIN, HIGH);
          delay(100);
          digitalWrite(LED_GREEN_PIN, LOW);
          delay(100);
        }
        break;

      // ===== ปุ่ม Volume- → ไฟแดงกระพริบ =====
      case IR_VOL_DOWN:
        Serial.println("🔉 Volume DOWN!");
        for (int i = 0; i < 3; i++) {
          digitalWrite(LED_RED_PIN, HIGH);
          delay(100);
          digitalWrite(LED_RED_PIN, LOW);
          delay(100);
        }
        break;
    }

    // รับสัญญาณต่อไป
    irrecv.resume();
  }

  delay(100);
}
```

#### ขั้นตอนที่ 3: ทดสอบ

1. **อัปโหลดโค้ด** ไปที่ ESP32-C3
2. **เปิด Serial Monitor**
3. **หันรีโมทเข้าหา IR Receiver**
4. **กดปุ่ม Power** → LED เขียวติด/ดับ สลับกัน
5. **กดปุ่ม Volume +/-** → LED กระพริบ

> ⚠️ **สำคัญ:** อย่าลืมเปลี่ยนค่า `IR_POWER`, `IR_VOL_UP`, `IR_VOL_DOWN` เป็นค่าจริงที่ถอดรหัสได้จากรีโมทที่ใช้!

---

### 🛠️ ปฏิบัติที่ 2: รีโมทคอนโทรลเซ็นเซอร์หลายตัว 🌡️

โปรเจกต์นี้จะเจ๋งกว่าเดิม! เราจะใช้รีโมทควบคุม:
- ปุ่ม **1** → อ่านอุณหภูมิ/ความชื้นจาก DHT11 แล้วแสดงผล
- ปุ่ม **2** → หมุน Servo ไป 0°
- ปุ่ม **3** → หมุน Servo ไป 90°
- ปุ่ม **4** → หมุน Servo ไป 180°
- ปุ่ม **Power** → สั่ง Servo Sweep อัตโนมัติ

#### ขั้นตอนที่ 1: ต่อวงจร

```
    ESP32-C3
    ┌─────────────────────────────────────────────────────┐
    │  3V3  ──┬──► IR Receiver VCC                         │
    │  GND  ──┴──► IR Receiver GND                         │
    │  GPIO5 ──────► IR Receiver OUT                       │
    │  GPIO0 ──────► DHT11 DATA                            │
    │  GPIO10 ─────► Servo Signal                          │
    │  GPIO18 ─────► LED เขียว (ผ่าน R 220Ω)                │
    │  GPIO19 ─────► LED แดง (ผ่าน R 220Ω)                  │
    └─────────────────────────────────────────────────────┘
```

#### ขั้นตอนที่ 2: ติดตั้ง Library DHT

1. **Sketch → Include Library → Manage Libraries**
2. พิมพ์ **"DHT sensor library"**
3. กด **Install** (ไลบรารีโดย Adafruit)

#### ขั้นตอนที่ 3: เขียนโค้ด

```cpp
// ============================================
// บทที่ 8: รีโมทคอนโทรลเซ็นเซอร์หลายตัว
// ============================================
// ปุ่ม 1: อ่านค่า DHT11 (อุณหภูมิ/ความชื้น)
// ปุ่ม 2-4: หมุน Servo
// ปุ่ม Power: Servo Sweep

#include <Arduino.h>
#include <IRrecv.h>
#include <IRremote.h>
#include <IRac.h>
#include <IRtext.h>
#include <Servo.h>
#include <DHT.h>

// ==== กำหนดขา ====
#define IR_PIN        5
#define LED_GREEN_PIN 18  // LED เขียว → GPIO 18
#define LED_RED_PIN   19  // LED แดง → GPIO 19
#define SERVO_PIN     10  // Servo → GPIO 10 (GPIO 2 เป็น Strapping Pin)
#define DHT_PIN       0

// ==== กำหนดค่า Hex ของรีโมท (เปลี่ยนตามรีโมทจริง!) ====
// ใช้ค่าตัวอย่าง — ถอดรหัสจริงจาก Serial Monitor
#define IR_1        0x20DF8877  // ปุ่ม 1
#define IR_2        0x20DF48B7  // ปุ่ม 2
#define IR_3        0x20DFC837  // ปุ่ม 3
#define IR_4        0x20DF28D7  // ปุ่ม 4
#define IR_POWER    0x20DF10EF  // ปุ่ม Power

// ==== สร้างอ็อบเจ็กต์ ====
IRrecv irrecv(IR_PIN, 100, 38, true);
decode_results results;
Servo myServo;
DHT dht(DHT_PIN, DHT11);

// ==== สถานะ ====
bool sweepMode = false;  // false = ปิด, true = Sweep

void setup() {
  Serial.begin(115200);
  Serial.println("=== IR Remote: Multi-Sensor Control ===");

  // ตั้งค่า LED
  pinMode(LED_GREEN_PIN, OUTPUT);
  pinMode(LED_RED_PIN, OUTPUT);

  // ตั้งค่า Servo
  myServo.attach(SERVO_PIN);
  myServo.write(0);  // เริ่มที่ 0°

  // ตั้งค่า DHT
  dht.begin();

  // เริ่มรับ IR
  irrecv.enableIRIn();

  // ไฟเริ่มต้น
  digitalWrite(LED_RED_PIN, HIGH);   // LED แดงติด = พร้อม
  digitalWrite(LED_GREEN_PIN, LOW);

  Serial.println("พร้อม! กดปุ่มรีโมท:");
  Serial.println(" [1] อ่านอุณหภูมิ/ความชื้น");
  Serial.println(" [2] Servo → 0°");
  Serial.println(" [3] Servo → 90°");
  Serial.println(" [4] Servo → 180°");
  Serial.println(" [Power] Servo Sweep");
}

void loop() {
  // ===== Servo Sweep อัตโนมัติ =====
  if (sweepMode) {
    // หมุนขึ้น 0 → 180
    for (int angle = 0; angle <= 180; angle += 5) {
      myServo.write(angle);
      delay(20);

      // ถ้ามีปุ่มอื่นกด → ออกจาก Sweep Mode
      if (irrecv.decode(&results)) {
        if (results.value != 0xFFFFFFFF) {  // ไม่ใช่ Repeat Code
          sweepMode = false;
          digitalWrite(LED_GREEN_PIN, LOW);
          digitalWrite(LED_RED_PIN, HIGH);
        }
        irrecv.resume();
        if (!sweepMode) break;
      }
    }

    if (!sweepMode) return;

    // หมุนลง 180 → 0
    for (int angle = 180; angle >= 0; angle -= 5) {
      myServo.write(angle);
      delay(20);

      if (irrecv.decode(&results)) {
        if (results.value != 0xFFFFFFFF) {
          sweepMode = false;
          digitalWrite(LED_GREEN_PIN, LOW);
          digitalWrite(LED_RED_PIN, HIGH);
        }
        irrecv.resume();
        if (!sweepMode) break;
      }
    }
  }

  // ===== รอรับคำสั่ง IR =====
  if (irrecv.decode(&results)) {

    // ข้าม Repeat Code (0xFFFFFFFF) ที่เกิดจากกดค้าง
    if (results.value != 0xFFFFFFFF) {

      Serial.print("รับค่า: 0x");
      Serial.println(results.value, HEX);

      switch (results.value) {

        // ===== ปุ่ม 1: อ่านอุณหภูมิ/ความชื้น =====
        case IR_1:
          Serial.println("🌡️  อ่านค่า DHT11...");
          readDHT();
          // ไฟกระพริบแจ้ง
          for (int i = 0; i < 2; i++) {
            digitalWrite(LED_GREEN_PIN, HIGH);
            delay(100);
            digitalWrite(LED_GREEN_PIN, LOW);
            delay(100);
          }
          break;

        // ===== ปุ่ม 2: Servo → 0° =====
        case IR_2:
          Serial.println("🔽 Servo → 0°");
          myServo.write(0);
          digitalWrite(LED_GREEN_PIN, HIGH);
          digitalWrite(LED_RED_PIN, LOW);
          break;

        // ===== ปุ่ม 3: Servo → 90° =====
        case IR_3:
          Serial.println("🔽🔼 Servo → 90°");
          myServo.write(90);
          digitalWrite(LED_GREEN_PIN, HIGH);
          digitalWrite(LED_RED_PIN, LOW);
          break;

        // ===== ปุ่ม 4: Servo → 180° =====
        case IR_4:
          Serial.println("🔼 Servo → 180°");
          myServo.write(180);
          digitalWrite(LED_GREEN_PIN, HIGH);
          digitalWrite(LED_RED_PIN, LOW);
          break;

        // ===== ปุ่ม Power: เปิด/ปิด Sweep Mode =====
        case IR_POWER:
          sweepMode = !sweepMode;
          if (sweepMode) {
            Serial.println("🔄 Sweep Mode เปิด!");
            digitalWrite(LED_GREEN_PIN, HIGH);
            digitalWrite(LED_RED_PIN, LOW);
          } else {
            Serial.println("⏹️  Sweep Mode ปิด!");
            digitalWrite(LED_GREEN_PIN, LOW);
            digitalWrite(LED_RED_PIN, HIGH);
          }
          break;
      }
    }

    irrecv.resume();
  }

  delay(50);
}

// ===== ฟังก์ชันอ่านค่า DHT11 =====
void readDHT() {
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  // ตรวจสอบว่าอ่านค่าได้ไหม
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("❌ อ่านค่า DHT11 ไม่ได้! ตรวจสอบการต่อสาย");
    return;
  }

  Serial.print("💧 ความชื้น: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("🌡️  อุณหภูมิ: ");
  Serial.print(temperature);
  Serial.println(" °C");

  // แจ้งเตือนถ้าร้อนเกินไป
  if (temperature > 35) {
    Serial.println("⚠️  ร้อนมาก! เปิดพัดลมหรือแอร์ด่วน!");
  }
}
```

#### ขั้นตอนที่ 4: ทดสอบ

1. **อัปโหลดโค้ด** ไปที่ ESP32-C3
2. **ถอดรหัสปุ่ม 1-4 จริง** จาก Serial Monitor
3. **แก้ค่า Hex** ในโค้ดให้ตรงกับรีโมทจริง
4. **ทดสอบทีละปุ่ม**

**ผลลัพธ์ที่คาดหวัง:** 🎉
- กด **1** → Serial Monitor แสดงอุณหภูมิและความชื้น
- กด **2** → Servo หมุนไป 0°
- กด **3** → Servo หมุนไป 90°
- กด **4** → Servo หมุนไป 180°
- กด **Power** → Servo หมุนไป-มา 0°-180° วนซ้ำ
- กดปุ่มอื่นระหว่าง Sweep → หยุด Sweep

---

## 🔬 เรื่องพิเศษ: IR กับโปรโตคอลอื่นๆ 🌐

NEC เป็นแค่หนึ่งในหลายโปรโตคอล IR ที่มีอยู่ โปรโตคอลอื่นๆ ที่นิยมใช้:

| โปรโตคอล | ใช้ใน | ลักษณะเด่น |
|---------|-------|----------|
| **NEC** | ทีวี, เครื่องเสียง, แอร์ส่วนใหญ่ | 32 bits, มี Address + Command |
| **Sony SIRC** | รีโมท Sony | 12/15/20 bits, มี 3 bytes |
| **RC5** | รีโมท Philips | 14 bits, Manchester Encoding |
| **Sharp** | เครื่อง Sharp | มี Address + Command + Parity |

```
📌 วิธีตรวจสอบโปรโตคอล:
- ใช้โค้ด IRrecvDumpV2 ดูที่ Protocol ใน Serial Monitor
- ถ้าขึ้น UNKNOWN = ต้องศึกษาเพิ่มเติมจาก Datasheet
```

---

## 📝 แบบฝึก

### แบบฝึกที่ 1: รีโมทควบคุม LED หลายดวง
ต่อ LED 4 ดวง แล้วเขียนโค้ดให้กดปุ่ม 1-4 ติดดวงละ 1 ดวงตามลำดับ

### แบบฝึกที่ 2: ปิดเครื่องปรับอากาศอัตโนมัติ
ใช้ IR LED (ส่งสัญญาณออก) ส่งคำสั่งปิดแอร์เมื่ออุณหภูมิสูงเกิน 30°C โดยอัตโนมัติ

```cpp
// ต้องใช้ IRsend library สำหรับส่งสัญญาณ IR
#include <IRsend.h>
IRsend irsend(4);  // IR LED → GPIO 4

// ส่งคำสั่งปิดแอร์ (ต้องหาค่า NEC ของปุ่มปิดแอร์จริงๆ)
irsend.sendNEC(0xXXXXXXXX);
```

### แบบฝึกที่ 3: รีโมทเปลี่ยนสี LED RGB
ใช้ปุ่ม R, G, B บนรีโมทควบคุมให้ LED RGB แสดงสีแดง เขียว น้ำเงิน

### แบบฝึกที่ 4: สร้างระบบ "กดปุ่ม + ยืนยัน"
ถ้ากดปุ่ม Power 1 ครั้ง → ไฟกระพริบรอยืนยัน → กดอีกครั้งภายใน 2 วินาที → ถึงจะทำงานจริง (ป้องกันกดผิด)

### แบบฝึกที่ 5: รีโมท + OLED Display
แสดงข้อความบน OLED ว่ากดปุ่มอะไร เช่น "Volume UP!" หรือ "Power OFF"

---

## 🤔 คำถามท้ายบท

1. **"ทำไม IR Receiver ถึงต้องใช้ความถี่ 38kHz ในการรับสัญญาณ?"** — อธิบายว่าถ้าใช้ความถี่อื่นจะเกิดปัญหาอะไร

2. **"ทำไมรีโมทต้องส่ง Address ด้วย?"** — ถ้าไม่มี Address จะเกิดปัญหาอะไรถ้ามีรีโมท 2 อันในห้องเดียวกัน?

3. **"Repeat Code (0xFFFFFFFF) คืออะไร? ทำไมรีโมทถึงส่งค่านี้เมื่อกดค้าง?"**

4. **(เชิงลึก)** "IR มีข้อจำกัดอะไรบ้าง? ถ้าเราต้องการควบคุมระยะไกลเกิน 10 เมตร หรือต้องควบคุมผ่านผนัง ควรใช้เทคโนโลยีอะไรแทน?"

---

## 📚 สรุป

ในบทนี้เราได้เรียนรู้ว่า:

✅ **Infrared (IR) คือแสงที่ตามนุษย์ไม่เห็น** แต่เซมิคอนดักเตอร์สามารถตรวจจับได้ อยู่ที่ความยาวคลื่น 700nm-1mm  
✅ **โปรโตคอล NEC ใช้กันแพร่หลาย** ประกอบด้วย Leader Code + Address (8 bits) + Command (8 bits) + Inverted Command  
✅ **IR Receiver รับสัญญาณ 38kHz** และถอด Carrier ออกให้เหลือข้อมูลดิจิทัล  
✅ **ใช้ Library IRremote** (สำหรับ ESP32) ถอดรหัสและใช้งาน IR ได้ง่ายมาก  
✅ **สามารถสร้างรีโมทคอนโทรลเซ็นเซอร์หลายตัว** ได้โดยกดปุ่มต่างกันให้ทำงานต่างกัน  

> 🔮 **บทต่อไป:** ในบทถัดไปเราจะมาเรียนรู้เรื่อง **HC-SR04 Ultrasonic Sensor** กัน! เราจะได้รู้ว่าทำไมค้างคาวถึงบินในความมืดได้ และจะเอาหลักการเดียวกันมาวัดระยะทางด้วยเสียงกัน! 🦇➡️📏

---

*📁 โค้ดตัวอย่าง: `/code/ch08_ir_remote/`*  
*🖼️ รูปประกอบ: `/images/ch08-*`*
