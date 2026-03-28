# 🔧 Troubleshooting — การแก้ปัญหาที่พบบ่อย

## ปัญหาการติดตั้ง

### 1. PlatformIO ไม่ติดตั้งได้

```
อาการ: PlatformIO IDE ไม่ขึ้นใน VS Code

วิธีแก้:
1. อัปเดต VS Code เป็นเวอร์ชันล่าสุด
2. รีสตาร์ท VS Code
3. ลองติดตั้ง PlatformIO ใหม่
4. ตรวจสอบว่า Internet ทำงานได้
```

### 2. เลือก Board ไม่เจอ

```
อาการ: ไม่มี ESP32-C3 ใน Board List

วิธีแก้:
1. ไปที่ PIO Home → Platforms
2. พิมพ์ "esp32"
3. ติดตั้ง "Espressif 32"
4. รีสตาร์ท VS Code
```

### 3. Library ติดตั้งไม่ได้

```
อาการ: โหลด Library นานมาก หรือ ติดตั้งไม่สำเร็จ

วิธีแก้ (PlatformIO):
1. เช็ค Internet ว่าเสถียรมั้ย
2. ลองเปลี่ยน Platform Version ใน platformio.ini

วิธีแก้ (Arduino IDE):
1. Sketch → Include Library → Manage Libraries
2. ลองค้นหาอีกครั้ง
3. ติดตั้งเวอร์ชันที่แนะนำ
```

---

## ปัญหา Compile

### 1. Error: 'DHT' does not name a type

```
Error: 'DHT' does not name a type

สาเหตุ: ไม่ได้ include library ถูกต้อง

วิธีแก้:
1. เช็คว่าติดตั้ง Library แล้ว
2. ใส่ include ให้ถูกต้อง:
   #include <DHT.h>
3. เช็คว่า lib_deps ใน platformio.ini ถูกต้อง:
   lib_deps = adafruit/DHT sensor library
```

### 2. Error: 'Wire' does not name a type

```
Error: 'Wire' does not name a type

สาเหตุ: ไม่ได้ include Wire library

วิธีแก้:
#include <Wire.h>

// และเริ่มต้น I2C
Wire.begin(SDA, SCL);  // กำหนดขา SDA, SCL
```

### 3. Error: 'SSD1306' does not name a type

```
Error: 'SSD1306' does not name a type

สาเหตุ: Library ไม่ครบ

วิธีแก้ (platformio.ini):
lib_deps =
    adafruit/Adafruit SSD1306
    adafruit/Adafruit GFX Library
    adafruit/Adafruit BusIO
```

### 4. Error: 'ledcSetup' was not declared

```
Error: 'ledcSetup' was not declared in this scope

สาเหตุ: ใช้ ESP32-C3 ซึ่งต้องใช้ LEDC API

วิธีแก้:
ใช้ analogWrite() แทน ledcSetup()
หรือใช้ LEDC API ที่ถูกต้องสำหรับ ESP32-C3:
ledcSetup(channel, frequency, resolution);
ledcAttachPin(pin, channel);
ledcWrite(channel, duty);
```

### 5. Warning: GPIO 6-11 are used for SPI Flash

```
Warning: GPIO6-11 are used for SPI flash

สาเหตุ: ESP32-C3 ใช้ GPIO 6-11 สำหรับ SPI Flash ภายใน

วิธีแก้:
- หลีกเลี่ยงใช้ GPIO 6, 7, 8, 9, 10, 11
- ใช้ GPIO อื่นแทน
```

---

## ปัญหา Upload

### 1. Upload สำเร็จแต่ Serial ไม่มีอะไรขึ้น

```
อาการ: "Successfully uploaded" แต่ Serial Monitor ว่าง

วิธีแก้:
1. เช็ค Baud Rate ตรงกันมั้ย?
   - ตั้ง 115200 ใน Serial Monitor
2. เช็คว่าเสียบสาย USB แน่นมั้ย?
3. ลองกดปุ่ม EN (Reset) บนบอร์ด
4. เช็คว่า TX/RX ต่อถูกต้อง?
```

### 2. Upload Failed - Device not found

```
Error: Failed to connect to ESP32-C3

สาเหตุ: บอร์ดไม่อยู่ในโหมด Download

วิธีแก้:
1. กดปุ่ม BOOT ค้างไว้
2. กดปุ่ม RESET (EN) 1 ครั้ง
3. ปล่อยปุ่ม BOOT
4. ลอง Upload ใหม่
```

### 3. Upload นานมาก

```
อาการ: Upload ใช้เวลานานเกินไป

วิธีแก้:
1. ลด upload speed:
   monitor_speed = 115200
   
2. ใช้สาย USB ที่สั้นลง
3. เช็คว่า USB Port พอรับ High Speed ได้มั้ย
```

---

## ปัญหา Hardware

### 1. LED ไม่ติด

```
ตรวจสอบทีละจุด:

1. LED ต่อถูกขั้วมั้ย?
   - ขาเสี้ยวยาว = + (Anode)
   - ขาสั้น = - (Cathode)
   
2. Resistor ใช้ค่าเท่าไหร่?
   - ค่าแนะนำ: 220Ω - 1kΩ
   
3. ลองสลับ LED ใหม่ (อาจเสีย)

4. ลองใช้ GPIO อื่น
```

### 2. สวิตช์อ่านค่าได้ไม่ตรง

```
อาการ: กดสวิตช์แล้วค่าเปลี่ยน แต่ไม่ตรงความคาดหวัง

วิธีแก้:
1. เช็คว่าใช้ INPUT_PULLUP หรือ INPUT_PULLDOWN?
2. ดู logic ที่ถูกต้อง:
   - INPUT_PULLUP: กด=LOW, ไม่กด=HIGH
   - INPUT_PULLDOWN: กด=HIGH, ไม่กด=LOW
3. เช็ควงจรว่าต่อ GND หรือ VCC ถูกต้อง
```

### 3. OLED ไม่แสดงผล

```
ตรวจสอบทีละจุด:

1. เช็คการต่อสาย I2C:
   - SDA → GPIO 0
   - SCL → GPIO 1
   - VCC → 3.3V
   - GND → GND

2. เช็ค I2C Address:
   - ค่ามาตรฐาน: 0x3C หรือ 0x3D

3. ลองเพิ่มความเร็ว I2C:
   Wire.begin(0, 1);
   Wire.setClock(400000); // 400kHz

4. ลองกด Reset บน OLED (ถ้ามี)
```

### 4. DHT11 อ่านค่าได้ NaN

```
อาการ: ค่าที่ได้เป็น NaN ตลอด

วิธีแก้:
1. เช็คการต่อสาย:
   - VCC → 3.3V
   - DATA → GPIO (กำหนดในโค้ด)
   - GND → GND
   
2. เช็ค Resistor 10kΩ:
   - ต้องต่อระหว่าง DATA กับ VCC

3. เพิ่ม delay หลัง dht.begin():
   dht.begin();
   delay(1000);  // รอให้ sensor พร้อม

4. ลองเปลี่ยน GPIO อื่น
```

### 5. HC-SR04 อ่านค่าได้ไม่ถูกต้อง

```
อาการ: ค่าระยะไม่ตรง หรือ 0 ตลอด

วิธีแก้:
1. เช็คการต่อ:
   - VCC → 5V (ต้องใช้ 5V สำหรับ HC-SR04)
   - TRIG → GPIO Output
   - ECHO → GPIO Input
   - GND → GND

2. เช็ค Voltage Divider (ต้องมี!):
   - ECHO ให้ 5V ออกมา
   - ต้องลดเป็น 3.3V ก่อนเข้า ESP32
   - ใช้ R1=1kΩ + R2=2kΩ

3. ลองใช้โค้ดทดสอบง่ายๆ:
   digitalWrite(TRIG, HIGH);
   delayMicroseconds(10);
   digitalWrite(TRIG, LOW);
   duration = pulseIn(ECHO, HIGH);
```

---

## ปัญหา WiFi

### 1. เชื่อมต่อ WiFi ไม่ได้

```
วิธีแก้:
1. เช็ค SSID และ Password ถูกต้องมั้ย?
2. บอร์ดอยู่ใกล้ Router พอมั้ย?
3. WiFi 2.4GHz หรือ 5GHz?
   - ESP32 รองรับแค่ 2.4GHz
4. ลองเปลี่ยน WiFi Channel

5. เพิ่ม debug:
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
     delay(500);
     Serial.print(".");
   }
```

### 2. WiFi ตัดบ่อย

```
สาเหตุ: สัญญาณไม่เสถียร

วิธีแก้:
1. เพิ่ม auto-reconnect:
   WiFi.reconnect();
   
2. เพิ่ม watchdog:
   if (WiFi.status() != WL_CONNECTED) {
     WiFi.reconnect();
   }

3. ตรวจสอบ RSSI:
   Serial.println(WiFi.RSSI());
```

---

## สรุป: Debug Checklist

```
ก่อนถาม AI:

1. ✅ ตรวจสอบ Hardware:
   - สายต่อถูกต้องมั้ย?
   - ขั้วถูกมั้ย?
   - VCC/GND ถูกมั้ย?

2. ✅ ตรวจสอบ Software:
   - Library ติดตั้งครบมั้ย?
   - GPIO ตรงกับโค้ดมั้ย?
   - Baud Rate ถูกมั้ย?

3. ✅ ลอง Basic Test:
   - เปลี่ยน GPIO อื่นดู
   - เปลี่ยนสาย/อุปกรณ์ใหม่

4. ✅ ดู Error Message:
   - Copy error มาถาม AI
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [GPIO Guide](../01-fundamentals/gpio-guide.md)
- [DHT11 Sensor](../02-sensors/dht11-sensor.md)
- [HC-SR04 Sensor](../02-sensors/hc-sr04-sensor.md)
- [AI Prompts](../06-ai-prompts/basic-prompts.md)
