# 🖥️ OLED 0.96" — จอแสดงผล

## OLED คืออะไร?

**OLED (Organic Light-Emitting Diode)** จอแสดงผลขนาดเล็กที่ใช้พลังงานต่ำ

```
规格 OLED 0.96":
- ขนาด: 0.96 นิ้ว
- ความละเอียด: 128×64 pixels
- โปรโตคอล: I2C
- Driver: SSD1306
- แรงดัน: 3.3V
```

## การต่อวงจร (I2C)

```
    ESP32-C3           OLED
    ┌─────────┐       ┌─────────┐
    │ 3.3V   ├───────┤ VCC     │
    │ GPIO 0 ├───────┤ SDA     │
    │ GPIO 1 ├───────┤ SCL     │
    │ GND    ├───────┤ GND     │
    └─────────┘       └─────────┘

I2C Address มาตรฐาน: 0x3C หรือ 0x3D
```

## การติดตั้ง Library

### PlatformIO (platformio.ini)

```ini
lib_deps =
    adafruit/Adafruit SSD1306
    adafruit/Adafruit GFX Library
    adafruit/Adafruit BusIO
```

### Arduino IDE

```
1. Sketch → Include Library → Manage Libraries
2. ค้นหา "Adafruit SSD1306"
3. ติดตั้งทั้ง SSD1306, GFX Library, และ BusIO
```

## โค้ดพื้นฐาน

```cpp
#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define OLED_ADDR 0x3C
#define OLED_WIDTH 128
#define OLED_HEIGHT 64

Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

void setup() {
    Wire.begin(0, 1);  // SDA, SCL
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
}

void loop() {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("Hello!");
    display.display();
    delay(1000);
}
```

## โค้ด: แสดงข้อความ + ตัวเลข

```cpp
void loop() {
    display.clearDisplay();
    
    // ข้อความใหญ่
    display.setTextSize(2);
    display.setCursor(0, 0);
    display.println("Temp:");
    display.print(25.5);
    display.println(" C");
    
    // ข้อความเล็ก
    display.setTextSize(1);
    display.setCursor(0, 40);
    display.println("Humidity: 65%");
    
    display.display();
    delay(500);
}
```

## โค้ด: Progress Bar

```cpp
void drawProgressBar(int percent) {
    int barWidth = 120;
    int barMaxWidth = 120;
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print("Loading: ");
    display.print(percent);
    display.println("%");
    
    // วาดกรอบ
    display.drawRect(4, 20, barMaxWidth, 20, SSD1306_WHITE);
    
    // วาดเติม
    int fillWidth = map(percent, 0, 100, 0, barMaxWidth);
    display.fillRect(4, 20, fillWidth, 20, SSD1306_WHITE);
    
    display.display();
}
```

## โค้ด: วาดรูป

```cpp
void drawHeart() {
    display.clearDisplay();
    
    // วาดหัวใจด้วย pixel
    int x = 50;
    int y = 20;
    
    display.drawPixel(x+3, y+1, SSD1306_WHITE);
    display.drawPixel(x+5, y+1, SSD1306_WHITE);
    display.drawLine(x, y+2, x+8, y+2, SSD1306_WHITE);
    display.drawLine(x, y+3, x+8, y+3, SSD1306_WHITE);
    display.drawLine(x, y+4, x+8, y+4, SSD1306_WHITE);
    display.drawLine(x+1, y+5, x+7, y+5, SSD1306_WHITE);
    display.drawLine(x+2, y+6, x+6, y+6, SSD1306_WHITE);
    display.drawLine(x+3, y+7, x+5, y+7, SSD1306_WHITE);
    display.drawPixel(x+4, y+8, SSD1306_WHITE);
    
    display.display();
}
```

## โค้ด: แสดงค่าจากหลายเซ็นเซอร์

```cpp
void displaySensorData(float temp, float humidity, int light) {
    display.clearDisplay();
    
    // แถวที่ 1: อุณหภูมิ
    display.setTextSize(1);
    display.setCursor(0, 0);
    display.print("Temp: ");
    display.print(temp, 1);
    display.println(" C");
    
    // แถวที่ 2: ความชื้น
    display.setCursor(0, 10);
    display.print("Humidity: ");
    display.print(humidity, 0);
    display.println("%");
    
    // แถวที่ 3: แสง
    display.setCursor(0, 20);
    display.print("Light: ");
    display.print(light);
    display.println("%");
    
    // แถวที่ 4: Progress bar แสง
    display.drawRect(0, 30, 128, 10, SSD1306_WHITE);
    display.fillRect(0, 30, map(light, 0, 100, 0, 128), 10, SSD1306_WHITE);
    
    display.display();
}
```

## โค้ด: หน้าจอ Splash

```cpp
void showSplash() {
    display.clearDisplay();
    
    // ชื่อโปรเจกต์
    display.setTextSize(2);
    display.setCursor(20, 20);
    display.println("SmartFarm");
    
    // เวอร์ชัน
    display.setTextSize(1);
    display.setCursor(40, 45);
    display.println("Version 1.0");
    
    display.display();
    delay(2000);
}
```

## I2C Scanner (หา Address OLED)

```cpp
#include <Wire.h>

void setup() {
    Serial.begin(115200);
    Wire.begin(0, 1);
    
    Serial.println("I2C Scanner...");
    
    for (byte address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        if (Wire.endTransmission() == 0) {
            Serial.print("Found: 0x");
            Serial.println(address, HEX);
        }
    }
}

void loop() {}
```

## การแก้ปัญหา

### OLED ไม่แสดงผล

```
1. เช็คการต่อสาย I2C (SDA, SCL, VCC, GND)
2. ลองเปลี่ยน Address:
   - 0x3C (มาตรฐาน)
   - 0x3D (อีกรุ่น)
3. เพิ่ม delay(100) หลัง display.begin()
4. ลอง I2C Scanner ดูว่าเจอมั้ย
```

### ภาพเพี้ยน/ไม่ชัด

```
1. ลดความเร็ว I2C:
   Wire.setClock(100000);  // 100kHz
   
2. เพิ่ม Capacitor 10µF ที่ VCC
```

---

## 📚 หัวข้อที่เกี่ยวข้อง

- [DHT11 Sensor](./dht11-sensor.md)
- [LDR Sensor](./ldr-sensor.md)
- [HC-SR04 Ultrasonic](./hc-sr04-sensor.md)
