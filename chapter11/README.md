# บทที่ 11: Mini Project — รวมทุกอย่างเป็น "สมาร์ทฟาร์ม" 🌱

> 📝 **หมายเหตุ:** บทนี้เราจะได้รวมทุกอย่างที่เรียนรู้มาจากทุกบท สร้างเป็นโปรเจกต์จริงๆ ที่ใช้งานได้! ตั้งแต่วัดอุณหภูมิ วัดแสง รดน้ำอัตโนมัติ ไปจนถึงแจ้งเตือนบนจอ OLED เลย!

---

## 🎯 สิ่งที่จะเรียนรู้

ในบทนี้ เราจะได้เรียนรู้:

- [ ] สรุปอุปกรณ์ทั้งหมดที่ใช้ในบทนี้
- [ ] วางแผนโปรเจกต์ Smart Farm อย่างเป็นระบบ
- [ ] วัดอุณหภูมิ/ความชื้นด้วย DHT11
- [ ] วัดความเข้มแสงด้วย LDR
- [ ] รดน้ำอัตโนมัติด้วย Relay + ปั๊มน้ำ
- [ ] แจ้งเตือนด้วย Buzzer + แสดงผลบน OLED
- [ ] ใช้ AI ช่วยวางแผนโปรเจกต์ทั้งระบบ

---

## 📖 บทนำ

เคยเห็นสมาร์ทฟาร์ม (Smart Farm) ในข่าวมั้ย? เป็นฟาร์มที่ใช้หุ่นยนต์และ AI ดูแลพืชผลแทนคน วัดอุณหภูมิ วัดความชื้น รดน้ำอัตโนมัติ ทำให้ผลผลิตดีขึ้นและประหยัดแรงงาน!

วันนี้เราจะมาสร้าง **"สมาร์ทฟาร์มขนาดเล็ก"** กัน! 🌿

ไม่ว่าจะเป็นกระบอกเพาะผักบนระเบียง กล่องเพาะต้นอ่อน หรือสวนหย่อมในบ้าน — เราสามารถใช้ ESP32-C3 ควบคุมระบบทั้งหมดได้เลย!

> 💡 **ไอเดีย:** ลองนึกภาพว่าเราปลูกผักบุ้งในกระบอก ถ้าดินแห้งเกินไป → ปั๊มน้ำจะเปิดรดน้ำเอง! ถ้าแดดจัดเกินไป → รดน้ำเพิ่มความชื้น! ถ้าอุณหภูมิสูงเกิน → เสียงเตือนดัง! สุดยอดมั้ย? 😎

แต่ก่อนจะเริ่ม เรามาวางแผนให้ดีกันก่อนนะ!

---

## 🔧 อุปกรณ์ที่ใช้ในบทนี้

### 📋 รายการอุปกรณ์ทั้งหมด

| อุปกรณ์ | จำนวน | หมายเหตุ |
|---------|-------|---------|
| ESP32-C3 | 1 บอร์ด | บอร์ดหลัก ควบคุมทุกอย่าง |
| DHT11 | 1 อัน | วัดอุณหภูมิ + ความชื้น |
| LDR (Light Dependent Resistor) | 1 อัน | วัดความเข้มแสง |
| Relay Module 5V (1 Channel) | 1 อัน | ควบคุมปั๊มน้ำ |
| Active Buzzer 5V | 1 อัน | เสียงเตือน |
| OLED Display 0.96" (I2C) | 1 อัน | แสดงผลข้อมูล |
| ปั๊มน้ำ DC 5V-12V | 1 อัน | รดน้ำอัตโนมัติ |
| ตัวต้านทาน 10kΩ | 2 ตัว | Pull-up สำหรับ DHT11 และ LDR |
| สายจัมเปอร์ | หลายเส้น | ต่อวงจร |
| Breadboard | 1 อัน | ช่วยในการต่อวงจร |
| USB Cable | 1 เส้น | อัปโหลดโค้ด + จ่ายไฟ |
| กล่องพลาสติก/กระถาง | 1 อัน | ใส่ต้นไม้ + ดิน |

### 💰 ราคาโดยประมาณ

```
อุปกรณ์ทั้งหมด ≈ 600-900 บาท
(ถ้าซื้อแบบชุด Kit จะถูกกว่า)
```

### 📷 ภาพตัวอย่าง Smart Farm

```
┌─────────────────────────────────────────────────────┐
│                   Smart Farm ของเรา                │
│                                                     │
│      ┌─────────┐         ┌─────────┐               │
│      │  ESP32  │═════════│  OLED   │               │
│      │  -C3    │         │ 0.96"   │               │
│      └────┬────┘         └─────────┘               │
│           │                                         │
│      ┌────┴────┬──────────┬──────────┐            │
│      │         │          │          │            │
│      ↓         ↓          ↓          ↓            │
│   ┌─────┐  ┌─────┐   ┌─────┐   ┌─────┐            │
│   │DHT11│  │ LDR │   │Relay│   │Buzzer│           │
│   │ 🌡️  │  │ 💡  │   │ 💧  │   │ 🔔  │            │
│   └─────┘  └─────┘   └─────┘   └─────┘            │
│                              │                      │
│                              ↓                      │
│                        ┌─────────┐                  │
│                        │ ปั๊มน้ำ 💧 │                  │
│                        └─────────┘                  │
│                              ↓                      │
│                        ┌─────────┐                  │
│                        │ 🌱 ต้นไม้  │                  │
│                        └─────────┘                  │
└─────────────────────────────────────────────────────┘
```

---

## 💻 เนื้อหา

### 🔹 วางแผนโปรเจกต์ Smart Farm อย่างเป็นระบบ

#### 🗺️ แผนผังระบบ

ก่อนต่อสายหรือเขียนโค้ด เราต้องวางแผนก่อนเสมอ! มาดูกันว่าระบบ Smart Farm ของเราจะทำอะไรได้บ้าง:

```
┌─────────────────────────────────────────────────────────┐
│                  ESP32-C3 สมองกล                        │
│                      🧠                                  │
│    ┌─────────────────────────────────────────────┐     │
│    │                                             │     │
│    │   📊 อ่านค่าจาก Sensor ตลอดเวลา             │     │
│    │   📊 ประมวลผลตามเงื่อนไข                    │     │
│    │   📊 สั่งงาน Output ตามผลลัพธ์              │     │
│    │                                             │     │
│    └─────────────────────────────────────────────┘     │
│                         │                              │
│    ┌────────────────────┼────────────────────┐        │
│    │                    │                    │        │
│    ↓                    ↓                    ↓        │
│ ┌──────┐  💡         ┌──────┐  🌡️        ┌──────┐  │
│ │ LDR  │ แสง         │DHT11 │  อุณหภูมิ  │OLED  │  │
│ └──────┘             └──────┘  +ความชื้น  └──────┘  │
│                                                     │
│    ┌────────────────────┬────────────────────┐      │
│    │                    │                    │      │
│    ↓                    ↓                    ↓      │
│ ┌──────┐  💧         ┌──────┐  🔔         ข้อมูล  │
│ │Relay │ ปั๊มน้ำ      │Buzzer│ เสียงเตือน         │
│ └──────┘              └──────┘                 │
│                                                     │
└─────────────────────────────────────────────────────────┘
```

#### 📋 เงื่อนไขการทำงาน

เราจะตั้งเงื่อนไขการทำงานดังนี้:

| เงื่อนไข | การตอบสนอง |
|---------|-----------|
| ความชื้นในดิน < 30% | เปิดปั๊มน้ำรดน้ำ 5 วินาที |
| อุณหภูมิ > 38°C | เปิดเสียงเตือน + แสดง "ร้อนมาก!" บน OLED |
| แสงน้อยกว่า 30% (กลางคืน) | แสดงสถานะ "กลางคืน" บน OLED |
| ความชื้นในอากาศ < 40% | แจ้งเตือน "ดินแห้ง" บน OLED |
| ทุกอย่างปกติ | แสดงค่าปกติ + LED เขียว |

#### 💭 ใช้ AI วางแผนโปรเจกต์

> 💡 **เคล็ดลับจากเพื่อน:** ก่อนเขียนโค้ด เราสามารถใช้ ChatGPT หรือ AI ช่วยวางแผนได้!

**ตัวอย่าง Prompt ที่จะถาม AI:**

```
"ช่วยวางแผนโปรเจกต์ Smart Farm ด้วย ESP32-C3 หน่อย
 มี DHT11, LDR, Relay, Buzzer, OLED
 ต้องวัดอุณหภูมิ วัดแสง รดน้ำอัตโนมัติ
 ช่วยออกแบบเงื่อนไขและโค้ดให้หน่อย"
```

AI จะช่วย:
1. แนะนำว่าควรใช้อุปกรณ์อะไรเพิ่ม
2. ออกแบบเงื่อนไขการทำงาน
3. เขียนโค้ดตัวอย่างให้
4. ช่วยหาข้อผิดพลาดถ้ามี

เราจะมาลองใช้ AI ช่วยในแต่ละส่วนของบทนี้ด้วยนะ!

---

### 🔹 วัดอุณหภูมิ/ความชื้น → DHT11

เราได้เรียนรู้วิธีใช้ DHT11 ในบทก่อนแล้ว มาทบทวนกันสั้นๆ:

#### 🔌 วงจร DHT11

```
ESP32-C3          DHT11
────────          ─────
3V3           ──► VCC (ขา 1)
GPIO 10      ──► DATA (ขา 2)
GND           ──► GND (ขา 4)

* ขา DATA ต่อ Pull-up 10kΩ ไป 3V3
```

#### 💻 โค้ดทดสอบ DHT11

```cpp
#include <DHT.h>

#define DHT_PIN  10
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("ทดสอบ DHT11!");
}

void loop() {
  float temp = dht.readTemperature();    // อุณหภูมิ (°C)
  float humi = dht.readHumidity();        // ความชื้น (%)

  if (isnan(temp) || isnan(humi)) {
    Serial.println("❌ อ่านค่าไม่ได้!");
  } else {
    Serial.print("🌡️ อุณหภูมิ: ");
    Serial.print(temp);
    Serial.println("°C");
    
    Serial.print("💧 ความชื้น: ");
    Serial.print(humi);
    Serial.println("%");
  }
  delay(2000);
}
```

---

### 🔹 วัดแสง → LDR (Light Dependent Resistor)

#### 🤔 LDR คืออะไร?

**LDR** ย่อมาจาก **Light Dependent Resistor** หรือ "ตัวต้านทานที่ขึ้นกับแสง"

```
  แสงมาก ──────────────────→ ความต้านทานต่ำ (100-1kΩ) ──→ ไฟออก HIGH
  แสงน้อย ──────────────────→ ความต้านทานสูง (1MΩ+) ────→ ไฟออก LOW
```

**หลักการ:**
- LDR มีความต้านทานเปลี่ยนตามแสง
- แสงเยอะ → ความต้านทานลดลง → ไฟผ่านได้มาก → อ่านค่า ADC ได้สูง
- แสงน้อย → ความต้านทานเพิ่มขึ้น → ไฟผ่านได้น้อย → อ่านค่า ADC ได้ต่ำ

#### 📐 วงจร LDR — ใช้ Voltage Divider

เพื่อให้ ESP32 อ่านค่าเป็น "เปอร์เซ็นต์แสง" ได้ เราต้องต่อเป็น **Voltage Divider**:

```
VCC (3V3) ──►  LDR  ──►  GPIO (ADC)
                    │
                    └──►  R 10kΩ  ──►  GND
```

**สูตรคำนวณ:**
```
ค่า ADC ที่อ่านได้ ──► แปลงเป็นเปอร์เซ็นต์:
percent = (ADC_value / 4095) * 100
```

#### 🔧 ต่อวงจร LDR

```
ESP32-C3          LDR + R 10kΩ
────────          ─────────────
3V3            ──► LDR ขา 1
GPIO 6 (ADC)  ──► LDR ขา 2 + R 10kΩ ขา 1
GND            ──► R 10kΩ ขา 2
```

#### 💻 โค้ดทดสอบ LDR

```cpp
#define LDR_PIN  6    // GPIO 6 = ขา ADC

void setup() {
  Serial.begin(115200);
  Serial.println("ทดสอบ LDR!");
}

void loop() {
  int lightRaw = analogRead(LDR_PIN);     // ค่า ADC (0-4095)
  int lightPercent = map(lightRaw, 0, 4095, 0, 100);

  Serial.print("แสง: ");
  Serial.print(lightRaw);
  Serial.print(" (");
  Serial.print(lightPercent);
  Serial.println("%)");

  delay(500);
}
```

---

### 🔹 รดน้ำอัตโนมัติ → Relay + ปั๊มน้ำ

#### 🤔 หลักการทำงาน

เมื่อดินแห้น (ความชื้นต่ำ) → ESP32 สั่ง Relay ให้ทำงาน → ปั๊มน้ำเปิด → รดน้ำ → รอ 5 วินาที → ปั๊มน้ำปิด

**วงจร:**

```
Adapter 12V (หรือ 5V)    Relay        ปั๊มน้ำ
─────────────           ─────        ────────
(+) 12V           ──► COM (ขั้วกลาง)
(-) 12V           ──► ปั๊มน้ำ (-)
ปั๊มน้ำ (+)       ──► NO (ขั้วเปิด)
```

> ⚠️ **หมายเหตุ:** ปั๊มน้ำ DC บางตัวใช้ไฟ 5V ก็ได้ ถ้าใช้ USB จ่ายไฟเลย ลองดูสเปคที่ซื้อมานะ

#### 💻 โค้ดทดสอบปั๊มน้ำ

```cpp
#define RELAY_PIN   2
#define PUMP_TIME   5000  // รดน้ำ 5 วินาที

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // ปั๊มปิดตอนเริ่ม
  Serial.println("ทดสอบปั๊มน้ำ!");
}

void loop() {
  Serial.println("เปิดปั๊มน้ำ...");
  digitalWrite(RELAY_PIN, HIGH);  // Relay ON → ปั๊มทำงาน
  delay(PUMP_TIME);              // รอ 5 วินาที
  digitalWrite(RELAY_PIN, LOW);   // Relay OFF → ปั๊มหยุด
  Serial.println("ปั๊มหยุด รอ 10 วินาที...");
  delay(10000);                   // รอ 10 วินาที
}
```

---

### 🔹 แจ้งเตือน → Buzzer + OLED

เราได้เรียนรู้ Buzzer ในบทก่อนแล้ว มาดู OLED กันบ้าง!

#### 📺 OLED Display คืออะไร?

**OLED** ย่อมาจาก **Organic Light-Emitting Diode** คือหน้าจอที่แต่ละจุดเรืองแสงเอง ไม่ต้องมี backlight ทำให้บางมากและประหยัดไฟ!

จอ OLED ขนาด **0.96 นิ้ว** ที่เราใช้กันมากมี:
- ขนาด **128×64 พิกเซล**
- เชื่อมต่อแบบ **I2C** (ใช้สายแค่ 4 เส้น)
- ราคาถูก (60-120 บาท)

#### 🔌 วงจร OLED (I2C)

```
ESP32-C3          OLED 0.96" I2C
────────          ─────────────
3V3            ──► VCC
GND            ──► GND
GPIO 8 (SDA)   ──► SDA
GPIO 9 (SCL)   ──► SCL
```

#### 📚 ติดตั้ง Library SSD1306

1. **Sketch** → **Include Library** → **Manage Libraries...**
2. พิมพ์ **Adafruit SSD1306** ในช่องค้นหา
3. กด **Install** (อาจถูกถามว่าติดตั้ง Adafruit GFX Library ด้วยไหม → ตกลง)

#### 💻 โค้ดทดสอบ OLED

```cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH  128  // ความกว้างจอ (พิกเซล)
#define SCREEN_HEIGHT 64   // ความสูงจอ (พิกเซล)
#define OLED_RESET    -1   // ไม่มีขา reset (ใช้ -1)
#define OLED_ADDR     0x3C // ที่อยู่ I2C ของจอ (ส่วนใหญ่ 0x3C)

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);

  // เริ่ม OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("❌ หาจอ OLED ไม่เจอ!");
    while (true);  // หยุดทำงาน
  }

  // ล้างหน้าจอ
  display.clearDisplay();
  
  // ตั้งค่าข้อความ
  display.setTextSize(2);      // ขนาดตัวอักษร 2x
  display.setTextColor(SSD1306_WHITE);  // สีขาว

  // แสดงข้อความ
  display.setCursor(10, 20);   // ตำแหน่ง x, y
  display.println("Smart Farm");
  display.setCursor(10, 45);
  display.setTextSize(1);
  display.println("by ESP32-C3 🌱");
  
  display.display();  // แสดงผล!
  
  Serial.println("✅ OLED พร้อมใช้งาน!");
}

void loop() {
  // ทดสอบ: เปลี่ยนข้อความทุก 2 วินาที
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Test: 2 sec");
  display.display();
  delay(2000);
}
```

---

## 🔨 ปฏิบัติ — ต่อวงจร Smart Farm ทีละส่วน

### 🏗️ แผนการต่อวงจรแบบเต็ม

```
┌──────────────────────────────────────────────────────────────┐
│                        Smart Farm                            │
│                      ESP32-C3 🧠                             │
│                                                               │
│   GPIO 10 ────────── DHT11 DATA (Pull-up 10k → 3V3)         │
│   GPIO 6  ────────── LDR + R 10kΩ (Voltage Divider → GND)   │
│   GPIO 2  ────────── Relay IN                               │
│   GPIO 4  ────────── Buzzer (+)                              │
│   GPIO 8  ────────── OLED SDA                                │
│   GPIO 9  ────────── OLED SCL                               │
│   3V3     ────────── VCC ทั้งหมด (DHT, LDR pull-up, OLED)   │
│   GND     ────────── GND ทั้งหมด                            │
│                                                               │
│   Relay COM ──────── Adapter (+)                             │
│   Relay NO ──────── ปั๊มน้ำ (+)                              │
│   Adapter (-) ───── ปั๊มน้ำ (-)                             │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### 📋 ตาราง GPIO ที่ใช้

| GPIO | ฟังก์ชัน | อุปกรณ์ |
|------|---------|---------|
| GPIO 2 | Digital Output | Relay (ควบคุมปั๊มน้ำ) |
| GPIO 4 | Digital Output | Buzzer (เสียงเตือน) |
| GPIO 6 | ADC | LDR (วัดแสง) |
| GPIO 8 | I2C SDA | OLED |
| GPIO 9 | I2C SCL | OLED |
| GPIO 10 | Digital I/O | DHT11 (DATA) |

### 🟢 ขั้นตอนที่ 1: ต่อ DHT11

```
ESP32-C3          DHT11
────────          ─────
3V3           ──► VCC
GPIO 10     ──► DATA
GND           ──► GND

* Pull-up 10kΩ ระหว่าง DATA กับ 3V3
```

### 🟢 ขั้นตอนที่ 2: ต่อ LDR

```
ESP32-C3          Voltage Divider
────────          ───────────────
3V3           ──► LDR ขา 1
GPIO 6 (ADC) ──► LDR ขา 2 + R 10kΩ ขา 1
GND           ──► R 10kΩ ขา 2
```

### 🟢 ขั้นตอนที่ 3: ต่อ OLED

```
ESP32-C3          OLED
────────          ─────
3V3           ──► VCC
GND           ──► GND
GPIO 8       ──► SDA
GPIO 9       ──► SCL
```

### 🟢 ขั้นตอนที่ 4: ต่อ Relay + ปั๊มน้ำ

```
ESP32-C3          Relay
────────          ─────
3V3           ──► VCC
GND           ──► GND
GPIO 2       ──► IN

Adapter 12V      Relay        ปั๊มน้ำ
(+)          ──► COM
(-)          ──► ปั๊มน้ำ (-)
ปั๊มน้ำ (+)  ──► NO
```

### 🟢 ขั้นตอนที่ 5: ต่อ Buzzer

```
ESP32-C3          Active Buzzer
────────          ──────────────
GPIO 4        ──► (+) ขา +
GND           ──► (-) ขา -
```

> ⚠️ **ตรวจสอบก่อนจ่ายไฟ!**
> - สายไฟทุกเส้นแน่นหน็น? ✅
> - + กับ - ไม่สลับกัน? ✅
> - ไม่มีสายลัดวงจร (ชำรุด)? ✅

---

## 💻 เขียนโค้ด Smart Farm เต็มรูปแบบ

### 📝 โค้ดหลัก — Smart Farm

```cpp
// ========================================================
// บทที่ 11: Smart Farm - ระบบดูแลต้นไม้อัตโนมัติ
// ========================================================

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>

// ===== OLED Setup =====
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1
#define OLED_ADDR     0x3C
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_ADDR);

// ===== DHT Setup =====
#define DHT_PIN   10
#define DHT_TYPE  DHT11
DHT dht(DHT_PIN, DHT_TYPE);

// ===== Pin Setup =====
#define LDR_PIN      6    // ADC วัดแสง
#define RELAY_PIN    2    // ควบคุมปั๊มน้ำ
#define BUZZER_PIN   4    // เสียงเตือน

// ===== เงื่อนไขการทำงาน =====
#define SOIL_DRY_THRESHOLD  30   // ความชื้นดินต่ำกว่า 30% → รดน้ำ
#define TEMP_HIGH_THRESHOLD 38   // อุณหภูมิเกิน 38°C → เตือน
#define HUMI_AIR_LOW        40   // ความชื้นอากาศต่ำกว่า 40% → เตือน
#define LIGHT_LOW_THRESHOLD 30   // แสงต่ำกว่า 30% → กลางคืน

// ===== ตัวแปร Global =====
bool pumpRunning = false;        // ปั๊มกำลังทำงานหรือเปล่า?
bool alarmActive = false;        // เสียงเตือนดังอยู่หรือเปล่า?
unsigned long pumpStartTime = 0; // เวลาที่เริ่มรดน้ำ
unsigned long lastDisplayUpdate = 0;  // เวลาอัปเดตจอล่าสุด

// ===== ค่าที่อ่านได้ =====
float temperature = 0;
float humidityAir = 0;
int lightPercent = 0;
int soilMoisture = 0;  // จำลองจากความชื้นอากาศ (ควรใช้ Soil Sensor จริง)

// ========================================================
// ฟังก์ชัน: แสดงผลบน OLED
// ========================================================
void updateOLED() {
  // ล้างหน้าจอ
  display.clearDisplay();
  
  // ===== บรรทัดที่ 1: อุณหภูมิ =====
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.print("Temp: ");
  display.print(temperature, 1);
  display.print("C");
  
  // ===== บรรทัดที่ 2: ความชื้นอากาศ =====
  display.setCursor(0, 10);
  display.print("Air: ");
  display.print(humidityAir, 1);
  display.print("%");
  
  // ===== บรรทัดที่ 3: แสง =====
  display.setCursor(0, 20);
  display.print("Light: ");
  display.print(lightPercent);
  display.print("%");
  
  // ===== บรรทัดที่ 4: ความชื้นดิน =====
  display.setCursor(0, 30);
  display.print("Soil: ");
  display.print(soilMoisture);
  display.print("%");
  
  // ===== บรรทัดที่ 5: สถานะปั๊มน้ำ =====
  display.setCursor(0, 40);
  if (pumpRunning) {
    display.print("PUMP: ON  💧");
  } else {
    display.print("PUMP: OFF");
  }
  
  // ===== บรรทัดที่ 6: สถานะเตือนภัย =====
  display.setCursor(0, 50);
  if (alarmActive) {
    display.setTextColor(SSD1306_BLACK, SSD1306_WHITE);  // ตัวอักษรกลับสี
    display.print("ALERT! HOT! 🔥");
    display.setTextColor(SSD1306_WHITE);
  } else {
    display.print("Status: OK ✅");
  }
  
  // แสดงผล!
  display.display();
}

// ========================================================
// ฟังก์ชัน: เล่นเสียงเตือน
// ========================================================
void playAlertSound(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(150);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
}

// ========================================================
// ฟังก์ชัน: อ่านค่าเซ็นเซอร์ทั้งหมด
// ========================================================
void readSensors() {
  // อ่านอุณหภูมิ + ความชื้นอากาศ
  temperature = dht.readTemperature();
  humidityAir = dht.readHumidity();
  
  // อ่านค่าแสง (ADC)
  int lightRaw = analogRead(LDR_PIN);
  lightPercent = map(lightRaw, 0, 4095, 0, 100);
  
  // จำลองความชื้นดิน (ควรใช้ Soil Moisture Sensor จริง)
  // ถ้าความชื้นอากาศสูง → ดินน่าจะชื้นด้วย
  soilMoisture = constrain(humidityAir * 0.8, 0, 100);
}

// ========================================================
// ฟังก์ชัน: ตรวจสอบเงื่อนไขและสั่งงาน
// ========================================================
void checkAndAct() {
  
  // ===== เงื่อนไขที่ 1: ดินแห้ง → รดน้ำ =====
  if (soilMoisture < SOIL_DRY_THRESHOLD && !pumpRunning) {
    Serial.println("💧 ดินแห้ง! เปิดปั๊มน้ำรดน้ำ...");
    
    digitalWrite(RELAY_PIN, HIGH);  // เปิดปั๊ม
    pumpRunning = true;
    pumpStartTime = millis();       // จำเวลาเริ่ม
    
    playAlertSound(1);  // เสียงบี๊บ 1 ครั้งแจ้งเตือน
  }
  
  // ตรวจสอบว่าปั๊มทำงานนานพอหรือยัง (5 วินาที)
  if (pumpRunning && (millis() - pumpStartTime >= 5000)) {
    digitalWrite(RELAY_PIN, LOW);   // ปิดปั๊ม
    pumpRunning = false;
    Serial.println("✅ รดน้ำเสร็จแล้ว ปิดปั๊ม");
  }
  
  // ===== เงื่อนไขที่ 2: อุณหภูมิสูงเกิน → เตือนภัย =====
  if (temperature > TEMP_HIGH_THRESHOLD) {
    if (!alarmActive) {
      Serial.println("⚠️ อุณหภูมิสูงเกิน! เปิดเตือนภัย!");
      alarmActive = true;
    }
    // เสียงเตือนดังต่อเนื่อง (ทุก 3 วินาที)
    playAlertSound(3);
  } else {
    if (alarmActive) {
      Serial.println("✅ อุณหภูมิกลับมาปกติ ปิดเตือนภัย");
      alarmActive = false;
      digitalWrite(BUZZER_PIN, LOW);
    }
  }
  
  // ===== เงื่อนไขที่ 3: กลางคืน (แสงน้อย) =====
  if (lightPercent < LIGHT_LOW_THRESHOLD) {
    Serial.println("🌙 ตอนนี้เป็นกลางคืน (แสงน้อย)");
  }
}

// ========================================================
// SETUP
// ========================================================
void setup() {
  Serial.begin(115200);
  Serial.println("=================================");
  Serial.println("🌱 Smart Farm by ESP32-C3");
  Serial.println("=================================");
  
  // ตั้งค่า Output
  pinMode(RELAY_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  
  // เริ่มต้นทุกอย่างปิด
  digitalWrite(RELAY_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  
  // เริ่ม Sensor
  dht.begin();
  
  // เริ่ม OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("❌ หาจอ OLED ไม่เจอ!");
    while (true);
  }
  
  // แสดงหน้าจอเริ่มต้น
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 20);
  display.println("Smart Farm");
  display.setCursor(10, 45);
  display.setTextSize(1);
  display.println("Starting...");
  display.display();
  
  delay(2000);  // แสดงหน้าจอเริ่มต้น 2 วินาที
  
  Serial.println("✅ ระบบพร้อม!");
}

// ========================================================
// LOOP
// ========================================================
void loop() {
  // อ่านค่าเซ็นเซอร์
  readSensors();
  
  // แสดงค่าบน Serial Monitor
  Serial.print("🌡️ ");
  Serial.print(temperature, 1);
  Serial.print("C | 💧 ");
  Serial.print(humidityAir, 1);
  Serial.print("% | 💡 ");
  Serial.print(lightPercent);
  Serial.print("% | 🌱 ");
  Serial.print(soilMoisture);
  Serial.print("% | ");
  if (pumpRunning) Serial.println("💧 ปั๊ม: ON");
  else Serial.println("💧 ปั๊ม: OFF");
  
  // ตรวจสอบเงื่อนไขและสั่งงาน
  checkAndAct();
  
  // อัปเดตหน้าจอ OLED
  updateOLED();
  
  delay(1000);  // วนทุก 1 วินาที
}
```

### 📤 อัปโหลดและทดสอบ

1. **กดปุ่ม Upload**
2. **เปิด Serial Monitor** ที่ 115200 baud
3. **ดูผลลัพธ์บน Serial Monitor:**
```
=================================
🌱 Smart Farm by ESP32-C3
=================================
✅ ระบบพร้อม!
🌡️ 30.0C | 💧 55.0% | 💡 75% | 🌱 44% | 💧 ปั๊ม: OFF
🌡️ 29.5C | 💧 56.0% | 💡 70% | 🌱 45% | 💧 ปั๊ม: OFF
💧 ดินแห้ง! เปิดปั๊มน้ำรดน้ำ...
💧 ปั๊ม: ON
✅ รดน้ำเสร็จแล้ว ปิดปั๊ม
💧 ปั๊ม: OFF
```

4. **ดูผลลัพธ์บน OLED:** ควรเห็นข้อมูลทั้งหมดแสดงบนจอ

> 💡 **เคล็ดลับ:** ถ้าจอ OLED ไม่แสดงผล ลองกดปุ่ม Reset บนบอร์ด ESP32 ดูนะ

---

## 📝 แบบฝึก

### แบบฝึกที่ 1: ใช้ Soil Moisture Sensor จริง
ถ้ามี Soil Moisture Sensor (เซ็นเซอร์วัดความชื้นในดิน) ลองเปลี่ยนจากการจำลองเป็นค่าจริง:

```cpp
#include <Adafruit_Sensor.h>
#include <Adafruit_SoilSensor.h>

#define SOIL_SENSOR_PIN  7
Adafruit_SoilSensor soil = Adafruit_SoilSensor();

void readSensors() {
  // ... ค่าอื่นๆ เหมือนเดิม
  
  // อ่านค่าจริงจาก Soil Sensor
  soilMoisture = soil.getCapacitance();
  // หรือ map ค่าให้เป็น 0-100%
  soilMoisture = constrain(map(soilMoisture, 200, 500, 0, 100), 0, 100);
}
```

### แบบฝึกที่ 2: เพิ่มรดน้ำหลายรอบ
ถ้าดินแห้งมาก (ความชื้น < 20%) ให้รดน้ำ 2 รอบ:

```cpp
#define SOIL_VERY_DRY   20   // ความชื้นต่ำมาก

void checkAndAct() {
  if (soilMoisture < SOIL_DRY_THRESHOLD && !pumpRunning) {
    // เปิดปั๊ม
    digitalWrite(RELAY_PIN, HIGH);
    pumpRunning = true;
    pumpStartTime = millis();
    
    // ถ้าดินแห้งมาก → รดน้ำนานขึ้น
    if (soilMoisture < SOIL_VERY_DRY) {
      pumpStartTime -= 3000;  // ลดเวลาเริ่มลง = รดน้ำนานขึ้น 3 วินาที
      Serial.println("💧💧 ดินแห้งมาก! รดน้ำนานขึ้น!");
    }
  }
}
```

### แบบฝึกที่ 3: เพิ่ม LED แสดงสถานะ
เพิ่ม LED 2 ดวงแสดงสถานะ:

```cpp
#define LED_GREEN  3   // ปกติ
#define LED_YELLOW 5   // รดน้ำ
#define LED_RED    7   // เตือนภัย

void updateLEDs() {
  if (temperature > TEMP_HIGH_THRESHOLD) {
    digitalWrite(LED_RED, HIGH);
    digitalWrite(LED_GREEN, LOW);
    digitalWrite(LED_YELLOW, LOW);
  } else if (pumpRunning) {
    digitalWrite(LED_YELLOW, HIGH);
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_GREEN, LOW);
  } else {
    digitalWrite(LED_GREEN, HIGH);
    digitalWrite(LED_RED, LOW);
    digitalWrite(LED_YELLOW, LOW);
  }
}
```

### แบบฝึกที่ 4: ส่งข้อมูลขึ้น Cloud
ถ้ามี Wi-Fi ลองส่งข้อมูลขึ้น Cloud (จะเรียนรู้เพิ่มเติมในบท 12!):

```cpp
#include <WiFi.h>

const char* ssid = "ชื่อWiFi";
const char* password = "รหัสWiFi";

void setup() {
  // ... อื่นๆ
  WiFi.begin(ssid, password);
  Serial.print("เชื่อมต่อ Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("✅ เชื่อมต่อแล้ว!");
}

void sendToCloud() {
  // ส่งข้อมูลไปยัง API หรือ MQTT
  // เช่น ThingSpeak, Blynk, Firebase
}
```

---

## 🤔 คำถามท้ายบท

### คำถามที่ 1: ทำไมต้องใช้ Voltage Divider กับ LDR?
เพราะ LDR เป็นตัวต้านทาน ไม่ใช่เซ็นเซอร์ที่ส่งสัญญาณออกมาเอง การต่อแบบ Voltage Divider จะทำให้ค่าแรงดันที่อ่านได้เปลี่ยนตามความเข้มแสง และ ESP32 สามารถอ่านค่า ADC ได้ถูกต้อง

### คำถามที่ 2: LDR กับ Soil Moisture Sensor ต่างกันยังไง?
**LDR** วัด**แสง** — แสงเยอะ → ความต้านทานลด → ค่า ADC สูง  
**Soil Moisture Sensor** วัด**ความชื้นในดิน** — ดินเปียก → ความต้านทานลด → ค่า ADC สูง  
ทั้งสองใช้หลักการเดียวกัน (เปลี่ยนความต้านทานตามสิ่งแวดล้อม) แต่วัดคนละอย่าง!

### คำถามที่ 3: ทำไมต้องรดน้ำ 5 วินาทีแล้วหยุด?
เพราะถ้ารดน้ำต่อเนื่อง → น้ำจะท่วม → รากพืชเน่าเสีย! การรดเป็นจังหวะ (5 วินาที → รอ → 5 วินาที) ช่วยให้น้ำซึมเข้าดินทีละน้อย และระบบมีเวลาวัดความชื้นกลับมาอีก

### คำถามที่ 4 (เชิงลึก): ทำไมควรใช้ Soil Moisture Sensor แทนการจำลองจากความชื้นอากาศ?
เพราะความชื้นในดินกับความชื้นในอากาศไม่เหมือนกันเสมอไป! วันที่อากาศแห้ง ดินอาจยังชื้นอยู่ หรือวันที่ฝนตก ดินอาจเปียกแต่อากาศแห้ง การใช้เซ็นเซอร์วัดตรงที่ดินจะแม่นยำกว่า

---

## 📚 สรุป

ในบทนี้เราได้เรียนรู้ว่า:

✅ อุปกรณ์ทั้งหมดในบทนี้: DHT11, LDR, Relay, Buzzer, OLED, ปั๊มน้ำ  
✅ วางแผนโปรเจกต์ Smart Farm อย่างเป็นระบบก่อนเริ่มทำ  
✅ วัดอุณหภูมิ/ความชื้นด้วย DHT11  
✅ วัดความเข้มแสงด้วย LDR (ใช้ Voltage Divider)  
✅ รดน้ำอัตโนมัติด้วย Relay + ปั๊มน้ำ  
✅ แจ้งเตือนด้วย Buzzer + แสดงผลบน OLED  
✅ รวมทุกอย่างเป็นระบบ Smart Farm ที่ใช้งานได้จริง!  

> 🔮 **บทต่อไป:** ในบทถัดไปเราจะมาท้าทายกันด้วย **AI Coding Challenge** — โปรเจกต์ขั้นสูง 3 โปรเจกต์ ได้แก่ ระบบรักษาความปลอดภัยบ้าน, หุ่นยนต์หลบสิ่งกีดขวาง, และสถานีอากาศที่ส่งข้อมูลขึ้น Cloud! พร้อมเรียนรู้ Prompt Engineering ขั้นสูงและเครื่องมือ AI อื่นๆ ด้วย! 🚀

---

*📁 โค้ดตัวอย่าง: `/code/ch11_smart_farm/`*  
*🖼️ รูปประกอบ: `/images/ch11-*`*  
*🌱 Smart Farm สุดเจ๋งของเราพร้อมใช้งานแล้ว! อย่าลืมรดน้ำต้นไม้ด้วยนะ~*
