# 📊 Slide Design Outline สำหรับ Felo
## บทที่ 2: ติดตั้งเครื่องมือ พร้อมเขียนโค้ด!

---

## 🎯 แนวทาง Design

| หัวข้อ | ค่า |
|---------|-----|
| **Theme** | Dark Modern, Tech, ESP32 Style |
| **สีหลัก** | Navy #0D1B2A, Cyan #00D9FF |
| **สี Accent** | Pink #FF6B8A, Gold #FFD700 |
| **Font** | Bold, Clean, อ่านง่าย |
| **สไตล์** | Professional, Educational |

---

## 📋 Slide Structure (10 หน้า)

---

### 📱-slide 1: HOOK (หน้าแรก)

**หัวข้อ:** เคยเจอ Error ตอนติดตั้งแล้วท้อมั้ย?

**เนื้อหาหลัก:**
- ข้อความใหญ่: "ถ้าเคยเห็นหน้าจอ Error แล้วท้อ..."
- ข้อความเล็ก: "คุณไม่ได้แก่คนเดียว! แม้โปรแกรมเมอร์มืออาชีพก็ยังเจอ Error!"

**Visual:** หน้าจอ VS Code มี error สีแดง

**Style:** Bold text, Pink accent, Eye-catching

---

### 📱-slide 2: VS Code คืออะไร?

**หัวข้อ:** 💻 VS Code — โปรแกรมแก้ไขโค้ดยอดนิยม

**เนื้อหาหลัก:**
- คำอธิบาย: "Visual Studio Code — พัฒนาโดย Microsoft ฟรี!"
- ตารางเปรียบเทียบ:
  | วิธีเขียน | ข้อดี | ข้อเสีย |
  | เขียนด้วย Notepad | เขียนได้เลย | ไม่มีช่วยเหลือ |
  | เขียนด้วย VS Code | เติมโค้ดอัตโนมัติ | ต้องติดตั้งก่อน |

**Visual:** ภาพ VS Code Interface + Notepad

---

### 📱-slide 3: PlatformIO คืออะไร?

**หัวข้อ:** 🧩 PlatformIO — Extension ที่ทำให้ VS Code รองรับ ESP32

**เนื้อหาหลัก:**
- คำอธิบาย: "เหมือนติดแอปเพิ่มในมือถือ — ทำให้ VS Code ส่งโค้ดไปบอร์ดได้!"
- ตาราง 4 ความสามารถ:
  | ความสามารถ | ทำอะไรได้ |
  | 🔌 รองรับบอร์ดหลายตัว | ESP32, Arduino, STM32 |
  | 📦 จัดการ Library | ดาวน์โหลดอัตโนมัติ |
  | ⬆️ อัปโหลดโค้ด | กดปุ่มเดียว |
  | 🔍 Serial Monitor | ดูข้อความจากบอร์ด |

**Visual:** PlatformIO Logo + ภาพเปรียบเทียบมือถือ/แอป

---

### 📱-slide 4: วิธีติดตั้ง VS Code

**หัวข้อ:** 💻 วิธีติดตั้ง VS Code (4 ขั้นตอน)

**เนื้อหาหลัก:**
- ขั้นตอน:
  ```
  📌 ขั้นตอนที่ 1: ไปที่ code.visualstudio.com
  📌 ขั้นตอนที่ 2: กด "Download for Windows"
  📌 ขั้นตอนที่ 3: เปิดไฟล์ .exe ที่ดาวน์โหลดมา
  📌 ขั้นตอนที่ 4: ทำตามขั้นตอน — อย่าลืมเลือก "Add to PATH"!
  ```

**Visual:** ภาพ Step-by-step การติดตั้งบน Windows

---

### 📱-slide 5: วิธีติดตั้ง PlatformIO

**หัวข้อ:** 🛠️ วิธีติดตั้ง PlatformIO Extension

**เนื้อหาหลัก:**
- ขั้นตอน:
  ```
  📌 ขั้นตอนที่ 1: เปิด VS Code → คลิก Extensions (ไอคอน 4 ช่อง)
  📌 ขั้นตอนที่ 2: พิมพ์ "platformio ide"
  📌 ขั้นตอนที่ 3: กด Install ที่ "PlatformIO IDE"
  📌 ขั้นตอนที่ 4: รอ 5-10 นาที → Reload!
  ```

> 💡 **เคล็ดลับ:** ถ้าติดตั้งนาน อาจเป็นเพราะอินเทอร์เน็ตช้า รอได้เลย!

**Visual:** ภาพ Extensions Marketplace + ปุ่ม Install

---

### 📱-slide 6: สร้าง Project แรก

**หัวข้อ:** 🏗️ สร้าง Project ใหม่: HelloESP32

**เนื้อหาหลัก:**
- ขั้นตอน:
  ```
  📌 ขั้นตอนที่ 1: คลิกไอคอน "Ant" ของ PlatformIO
  📌 ขั้นตอนที่ 2: กด "PIO New Project"
  📌 ขั้นตอนที่ 3: ตั้งชื่อ "HelloESP32"
  📌 ขั้นตอนที่ 4: เลือก Board เป็น "ESP32-C3 Dev Module"
  📌 ขั้นตอนที่ 5: เลือก Framework เป็น "Arduino"
  📌 ขั้นตอนที่ 6: กด Finish!
  ```

**Visual:** ภาพ PlatformIO New Project Wizard

---

### 📱-slide 7: เขียนโค้ดแรก

**หัวข้อ:** 💻 โค้ด Hello ESP32!

**เนื้อหาหลัก:**
- โค้ด:
```cpp
void setup() {
  Serial.begin(115200);
  while(!Serial);
  Serial.println("Hello ESP32-C3!");
}

void loop() {
  Serial.println("บอร์ดกำลังทำงาน... ✅");
  delay(2000);
}
```

- ตารางอธิบาย:
  | คำสั่ง | ทำงานยังไง |
  | setup() | ทำงานแค่ครั้งเดียวตอนเริ่ม |
  | loop() | ทำงานซ้ำไปเรื่อยๆ |
  | delay(2000) | หยุดรอ 2 วินาที |

**Visual:** ภาพโค้ดบน VS Code พร้อมไฮไลท์

---

### 📱-slide 8: อัปโหลดโค้ด + Serial Monitor

**หัวข้อ:** ⬆️ อัปโหลดโค้ด + ดูผลลัพธ์

**เนื้อหาหลัก:**
- ขั้นตอนอัปโหลด:
  ```
  📌 เสียบสาย USB → เลือก Port → กดปุ่ม Upload → รอสำเร็จ!
  ```

- ผลลัพธ์บน Serial Monitor:
  ```
  ========================================
     Hello ESP32-C3! สวัสดีจากบอร์ดของเรา!
  ========================================
  บอร์ดกำลังทำงาน... ✅
  บอร์ดกำลังทำงาน... ✅
  ```

> ⚠️ **ปัญหาที่อาจเจอ:** "Failed to connect" → ลองกด BOOT + RESET

**Visual:** ภาพ Serial Monitor แสดงผล

---

### 📱-slide 9: ให้ AI ช่วยแก้ Error

**หัวข้อ:** 🤖 AI ช่วยแก้ Error — ลองฝึก!

**เนื้อหาหลัก:**
- โค้ดที่มี error:
```cpp
void setup() {
  Serial.begin(115200)       // ลืม ;
  digitlWrite(LED_PIN, HIGH);  // พิมพ์ผิด!
}
```

- วิธีถาม AI:
  ```
  "ช่วยดูโค้ด Arduino สำหรับ ESP32-C3 ให้หน่อย เจอ Error:
   [วางโค้ดที่นี่]
   Error: [วาง error message ที่นี่]"
  ```

> 💡 **เคล็ดลับ:** ยิ่งให้ข้อมูลมาก AI ยิ่งช่วยได้ดี!

**Visual:** ภาพ ChatGPT กำลังตอบคำถาม

---

### 📱-slide 10: สรุป

**หัวข้อ:** 📋 สรุปบทที่ 2

**เนื้อหาหลัก:**
- 💻 **VS Code** → โปรแกรมแก้ไขโค้ดยอดนิยม ฟรี
- 🧩 **PlatformIO** → Extension ที่รองรับ ESP32
- 🏗️ **สร้าง Project** → New Project → ตั้งชื่อ → เลือกบอร์ด
- ⚙️ **setup() vs loop()** → ทำงานครั้งเดียว vs ทำงานซ้ำ
- 🤖 **AI ช่วยแก้ Error** → ถาม AI พร้อมโค้ด + error message

> 🔮 **บทต่อไป:** ลงมือต่อวงจร LED ติด-ดับกัน!

---

## 📝 Prompt สำหรับ Felo

```
สร้าง PowerPoint 10 หน้า เรื่อง "ติดตั้งเครื่องมือ พร้อมเขียนโค้ด!"

Theme: Dark Modern, Tech, ESP32 Style
สีหลัก: Navy (#0D1B2A), Cyan (#00D9FF)
สี Accent: Pink (#FF6B8A), Gold (#FFD700)

Slide 1: HOOK - "เคยเจอ Error ตอนติดตั้งแล้วท้อมั้ย?"
Slide 2: VS Code คืออะไร - ตารางเปรียบเทียบ Notepad vs VS Code
Slide 3: PlatformIO คืออะไร - ตาราง 4 ความสามารถ
Slide 4: วิธีติดตั้ง VS Code - ขั้นตอน 4 ขั้น
Slide 5: วิธีติดตั้ง PlatformIO - ขั้นตอน 4 ขั้น
Slide 6: สร้าง Project แรก - HelloESP32 ขั้นตอน 6
Slide 7: เขียนโค้ดแรก - โค้ด Hello ESP32 + ตารางอธิบาย
Slide 8: อัปโหลดโค้ด + Serial Monitor - ผลลัพธ์ที่คาดหวัง
Slide 9: AI ช่วยแก้ Error - ตัวอย่างโค้ด error + วิธีถาม AI
Slide 10: สรุป - 5 ข้อสรุป + เตือนบทต่อไป

Style: Bold, Clean, Professional, Educational
```

---

## ⏱️ ระยะเวลา

| หน้า | เวลา |
|-------|-------|
| 1 (Hook) | 0:30 |
| 2 (VS Code) | 1:00 |
| 3 (PlatformIO) | 1:00 |
| 4 (ติดตั้ง VS Code) | 1:30 |
| 5 (ติดตั้ง PlatformIO) | 1:00 |
| 6 (สร้าง Project) | 1:30 |
| 7 (เขียนโค้ด) | 2:00 |
| 8 (อัปโหลด + Monitor) | 1:30 |
| 9 (AI แก้ Error) | 1:00 |
| 10 (สรุป) | 0:30 |
| **รวม** | **~12 นาที** |

---

> **หมายเหตุ:** Felo จะสร้าง PPT อัตโนมัติ พี่จะได้ไฟล์ PPT มาต่อจากนั้นจะต้อง:
> 1. เพิ่มเสียงบรรยาย (ElevenLabs)
> 2. ถ่าย INSERT footage (ติดตั้งจริง + อัปโหลดจริง)
> 3. ตัดต่อสุดท้าย
