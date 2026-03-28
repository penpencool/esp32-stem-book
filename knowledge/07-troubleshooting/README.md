# 🔧 Troubleshooting — การแก้ปัญหาที่พบบ่อย

## ไฟล์ในหมวดนี้

| ไฟล์ | หัวข้อ |
|------|--------|
| [common-issues.md](./common-issues.md) | ปัญหาที่พบบ่อย + วิธีแก้ |

## สรุปปัญหายอดฮิต

### Compile Error

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|----------|
| `does not name a type` | ไม่ได้ include library | `#include <X.h>` |
| `was not declared` | ใช้ function ผิด | ดู documentation |
| `permission denied` | ไม่มีสิทธิ์ | รัน as admin |
| `library not found` | ยังไม่ติดตั้ง | ติดตั้งใน library manager |

### Upload Error

| Error | สาเหตุ | วิธีแก้ |
|-------|--------|----------|
| `Failed to connect` | บอร์ดไม่อยู่ในโหมด download | กด BOOT + RESET |
| `Device not found` | USB ไม่ตรง | ลอง USB อื่น |
| `timed out` | สายยาวเกิน/พอร์ตช้า | ลด speed หรือสายสั้นลง |

### Hardware Error

| ปัญหา | สาเหตุ | วิธีแก้ |
|--------|--------|----------|
| LED ไม่ติด | ขั้วผิด/Resistor ผิดค่า | สลับขา LED, เช็ค Resistor |
| สวิตช์อ่านค่าผิด | ใช้ mode ผิด | INPUT vs INPUT_PULLUP |
| OLED ไม่แสดง | I2C address ผิด | 0x3C หรือ 0x3D |
| DHT ได้ NaN | ต่อสายผิด/Resistor หลุด | เช็ควงจร |

## Quick Checklist

```
ก่อนถาม AI:

1. ✅ Hardware:
   - สายต่อถูกต้องมั้ย?
   - ขั้วถูกมั้ย?
   - VCC/GND ถูกมั้ย?

2. ✅ Software:
   - Library ติดตั้งครบมั้ย?
   - GPIO ตรงกับโค้ดมั้ย?

3. ✅ ลอง Basic:
   - เปลี่ยน GPIO อื่น
   - เปลี่ยนสาย/อุปกรณ์ใหม่

4. ✅ ดู Error:
   - Copy error มาถาม AI
```

## คำถามที่ถามบ่อยที่สุด

### Q: LED ไม่ติดเลย
```
A: ตรวจสอบ:
   1. LED ขั้วถูกมั้ย? (ขาเสี้ยวยาว = +)
   2. Resistor ใช้ค่าเท่าไหร่? (220Ω - 1kΩ)
   3. ลองสลับ LED ใหม่
```

### Q: Upload ไม่สำเร็จ
```
A: ลอง:
   1. กด BOOT ค้าง → กด RESET → ปล่อย BOOT
   2. ลองสาย USB ใหม่
   3. เช็คว่าเลือก Board ถูกมั้ย
```

### Q: Serial Monitor ไม่มีอะไรขึ้น
```
A: เช็ค:
   1. Baud Rate ตรงมั้ย? (115200)
   2. กด Reset บนบอร์ดหรือยัง?
   3. TX/RX ต่อถูกมั้ย?
```

### Q: DHT11 อ่านค่าได้ NaN
```
A: เช็ค:
   1. ต่อ Resistor 10kΩ ระหว่าง DATA กับ VCC หรือยัง?
   2. delay(2000) ก่อนอ่านค่าหรือยัง?
   3. ลองเปลี่ยน GPIO อื่น
```

### Q: OLED ไม่แสดงผล
```
A: ลอง:
   1. เปลี่ยน address เป็น 0x3D
   2. เพิ่ม delay หลัง display.begin()
   3. เช็คสาย SDA/SCL ถูกมั้ย
```

## หมายเหตุ

```
ปัญหาส่วนใหญ่เป็น:
- สาย/การต่อผิด (60%)
- Library ไม่ครบ (20%)
- GPIO ผิด (15%)
- อุปกรณ์เสีย (5%)
```

---

**อัปเดตล่าสุด:** 28 มีนาคม 2569
