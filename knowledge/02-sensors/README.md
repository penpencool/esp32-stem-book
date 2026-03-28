# 🌡️ เซ็นเซอร์ต่างๆ

## ไฟล์ในหมวดนี้

| ไฟล์ | เซ็นเซอร์ | ฟังก์ชัน |
|------|----------|----------|
| [dht11-sensor.md](./dht11-sensor.md) | DHT11 | อุณหภูมิ + ความชื้น |
| [ldr-sensor.md](./ldr-sensor.md) | LDR | วัดความเข้มแสง |
| [hc-sr04-sensor.md](./hc-sr04-sensor.md) | HC-SR04 | วัดระยะทาง |
| [oled-display.md](./oled-display.md) | OLED 0.96" | จอแสดงผล |

## สรุปเซ็นเซอร์ในชุด

| เซ็นเซอร์ | ราคา | ย่านการวัด | การต่อ |
|----------|------|-----------|--------|
| **DHT11** | 25฿ | 0-50°C, 20-90%RH | GPIO (1-wire) |
| **LDR** | 15฿ | 0-1000 Lux | ADC |
| **HC-SR04** | 35฿ | 2-400 cm | GPIO (Trigger/Echo) |
| **OLED 0.96"** | 100฿ | 128x64 pixels | I2C |

## DHT11 — วัดอุณหภูมิ/ความชื้น

```cpp
#include <DHT.h>
#define DHT_PIN 0
#define DHT_TYPE DHT11

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
    dht.begin();
}

void loop() {
    float temp = dht.readTemperature();    // อุณหภูมิ (°C)
    float humidity = dht.readHumidity();      // ความชื้น (%)
    
    if (!isnan(temp) && !isnan(humidity)) {
        Serial.print("อุณหภูมิ: ");
        Serial.println(temp);
        Serial.print("ความชื้น: ");
        Serial.println(humidity);
    }
    delay(2000);
}
```

### วงจร DHT11

```
    ESP32-C3           DHT11
    ┌─────────┐       ┌─────────┐
    │ 3.3V   ├───────┤ VCC     │
    │ GPIO 0 ├───────┤ DATA    │──┤10kΩ├── 3.3V
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘
```

## LDR — วัดความเข้มแสง

```cpp
#define LDR_PIN 2  // ADC pin

void setup() {
    Serial.begin(115200);
}

void loop() {
    int light = analogRead(LDR_PIN);  // 0-4095
    int percent = map(light, 0, 4095, 0, 100);
    
    Serial.print("แสง: ");
    Serial.print(percent);
    Serial.println("%");
    delay(500);
}
```

### วงจร LDR (Voltage Divider)

```
    3.3V
      │
     [10kΩ]
      │
      ├─── GPIO 2 (ADC)
      │
     [LDR]
      │
     GND
```

## HC-SR04 — วัดระยะทาง

```cpp
#define TRIG_PIN 12
#define ECHO_PIN 13

void setup() {
    Serial.begin(115200);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
}

void loop() {
    // ส่ง ultrasonic
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // วัดระยะ
    long duration = pulseIn(ECHO_PIN, HIGH);
    float distance = duration * 0.034 / 2;  // cm
    
    Serial.print("ระยะ: ");
    Serial.print(distance);
    Serial.println(" cm");
    delay(500);
}
```

### วงจร HC-SR04 (ต้องมี Voltage Divider!)

```
    ESP32-C3           HC-SR04
    ┌─────────┐       ┌─────────┐
    │ 5V     ├───────┤ VCC     │
    │ GPIO 12├───────┤ TRIG    │
    │ GPIO 13├─┤1kΩ├──┤ ECHO   │──┤2kΩ├── GND
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘
```

> ⚠️ **สำคัญ:** HC-SR04 ให้ 5V ออกจาก ECHO ต้องลดเป็น 3.3V ก่อนเข้า ESP32

## OLED 0.96" — จอแสดงผล

```cpp
#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define OLED_ADDR 0x3C
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
    Wire.begin(0, 1);  // SDA, SCL
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
    display.clearDisplay();
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println("Hello!");
    display.display();
    delay(1000);
}
```

### วงจร OLED (I2C)

```
    ESP32-C3           OLED
    ┌─────────┐       ┌─────────┐
    │ 3.3V   ├───────┤ VCC     │
    │ GPIO 0 ├───────┤ SDA     │
    │ GPIO 1 ├───────┤ SCL     │
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘
```

## การเลือกใช้เซ็นเซอร์

| ต้องการวัด... | ใช้... | หมายเหตุ |
|--------------|--------|----------|
| อุณหภูมิ | DHT11 | ราคาถูก แต่ไม่แม่นมาก |
| ความชื้น | DHT11 | ±5% accuracy |
| แสง | LDR | วัดเป็น % ได้ |
| ระยะทาง | HC-SR04 | 2-400 cm |
| ความดันบรรยากาศ | BMP280 | ต้องซื้อเพิ่ม |
| ฝุ่น PM2.5 | PMS5003 | ต้องซื้อเพิ่ม |

## ขั้นตอนถัดไป

```
🌡️ DHT11 → [DHT11 Guide](./dht11-sensor.md)
   ↓
💡 LDR → [LDR Guide](./ldr-sensor.md)
   ↓
📏 HC-SR04 → [HC-SR04 Guide](./hc-sr04-sensor.md)
   ↓
🖥️ OLED → [OLED Guide](./oled-display.md)
```

---

**อัปเดตล่าสุด:** 28 มีนาคม 2569
