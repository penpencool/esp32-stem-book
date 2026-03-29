# Python Presentation Tools Research

> **Date:** 2026-03-29  
> **Purpose:** Survey Python libraries and design systems for creating beautiful PowerPoint presentations

---

## 1. Python Libraries

### ✅ python-pptx (RECOMMENDED - Primary Choice)

**Status:** ✅ Active, well-maintained  
**Version:** 1.0.2 (latest)  
**PyPI:** https://pypi.org/project/python-pptx/  
**GitHub:** https://github.com/scanny/python-pptx

**วิธีติดตั้ง:**
```bash
pip install python-pptx
# หรือใช้ uv (แนะนำสำหรับ Python 3.12+)
uv pip install python-pptx
```

**Features ที่ทดสอบแล้ว:**
- สร้าง Presentation ใหม่ทั้งหมด (programmatic)
- กำหนด slide size (widescreen 16:9, 4:3)
- 11 built-in slide layouts (Title Slide, Title & Content, Two Content, etc.)
- เพิ่ม/แก้ไข text พร้อม font formatting (size, bold, color)
- สร้างตาราง (tables)
- ใส่รูปภาพ
- วางรูปทรงต่างๆ (shapes)
- กำหนดสี background
- Rounded rectangle สำหรับ code blocks

**Limitations:**
- ไม่มี template engine ในตัว — ต้องสร้างทุกอย่างด้วย code
- ไม่มี built-in themes

**Code ตัวอย่าง (Basic):**
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.33)   # Widescreen 16:9
prs.slide_height = Inches(7.5)

# Title Slide
slide = prs.slides.add_slide(prs.slide_layouts[0])  # Title Slide
slide.shapes.title.text = "ESP32 Workshop"
slide.placeholders[1].text = "Build Interactive Projects"

# Text with formatting
txBox = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(11), Inches(1))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "Hello World"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = RGBColor(0, 100, 200)
p.alignment = PP_ALIGN.CENTER

# Table
slide2 = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
tbl = slide2.shapes.add_table(3, 3, Inches(1), Inches(2), Inches(11), Inches(3)).table
for i in range(3):
    for j in range(3):
        tbl.cell(i, j).text = f"R{i}C{j}"

prs.save("output.pptx")
```

**Code ตัวอย่าง (Advanced - STEM Workshop):**
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# --- Slide 1: Title with colored background ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid()
bg.fill.fore_color.rgb = RGBColor(25, 55, 95)
bg.line.fill.background()

title_box = slide1.shapes.add_textbox(Inches(1), Inches(2.5), Inches(11), Inches(1.5))
p = title_box.text_frame.paragraphs[0]
p.text = "ESP32 STEM Workshop"
p.font.size = Pt(54)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)
p.alignment = PP_ALIGN.CENTER

sub_box = slide1.shapes.add_textbox(Inches(1), Inches(4.2), Inches(11), Inches(0.8))
p2 = sub_box.text_frame.paragraphs[0]
p2.text = "Build Interactive Projects with MicroPython"
p2.font.size = Pt(28)
p2.font.color.rgb = RGBColor(100, 200, 255)
p2.alignment = PP_ALIGN.CENTER

# --- Slide 2: Bullet list ---
slide2 = prs.slides.add_slide(prs.slide_layouts[1])  # Title and Content
slide2.shapes.title.text = "What You'll Learn"
body = slide2.placeholders[1]
tf = body.text_frame
for i, item in enumerate(["MicroPython fundamentals", "GPIO & sensors", "WiFi web server"]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = item
    p.font.size = Pt(24)

# --- Slide 3: Code block ---
code_bg = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(1.5), Inches(12), Inches(5))
code_bg.fill.solid()
code_bg.fill.fore_color.rgb = RGBColor(30, 30, 40)
code_bg.line.color.rgb = RGBColor(60, 60, 80)

code_box = slide3.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(4.5))
tf = code_box.text_frame
tf.word_wrap = True
for i, line in enumerate(["from machine import Pin", "led = Pin(2, Pin.OUT)", "led.value(1)"]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.text = line
    p.font.name = "Courier New"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(100, 255, 150)

prs.save("esp32_workshop.pptx")
```

---

### ✅ pptx-template (m3dev)

**Status:** ✅ Available — ใช้งานได้ (GitHub version เท่านั้น สำหรับ Python 3.12+)  
**PyPI Version:** 0.2.9 (ล้าสมัย, ใช้ python-pptx 0.6.x ซึ่งไม่รองรับ Python 3.12)  
**GitHub Version:** 1.0.0 (รองรับ Python 3.10+, ใช้ python-pptx 1.0.2)  
**GitHub:** https://github.com/m3dev/pptx-template

**วิธีติดตั้ง (เวอร์ชันล่าสุด):**
```bash
# ต้องใช้ uv หรือ pip install จาก GitHub
uv pip install git+https://github.com/m3dev/pptx-template.git
```

**แนวคิด:** ใช้ template PPTX file ที่มี placeholder text เช่น `{variable_name}` แล้วแทนที่ด้วย JSON model

**Code ตัวอย่าง:**
```python
# 1. สร้าง template (ด้วย python-pptx) ใส่ text "{greeting}" และ "{product_name}"
# 2. ใช้ pptx-template แทนที่ค่า

from pptx import Presentation
from pptx_template.core import edit_slide

# สร้าง template
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[6])
txBox = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(11), Inches(1))
txBox.text_frame.paragraphs[0].text = "Hello {greeting}!"  # placeholder
prs.save('template.pptx')

# เปิด template และ fill ค่า
prs2 = Presentation('template.pptx')
model = {
    "greeting": "World",
    "product_name": "ESP32 DevKit",
}
edit_slide(prs2.slides[0], model)
prs2.save('output.pptx')
```

**หมายเหตุ:** PyPI version เป็นเวอร์ชันเก่ามาก (2019) ไม่แนะนำ — ใช้ GitHub version แทน

---

### ❌ python-pptx-templates

**Status:** ❌ ไม่มีใน PyPI — ไม่พบ package นี้

---

### ❌ markppt

**Status:** ❌ ไม่พบ package หรือ repository สาธารณะ  
**หมายเหตุ:** อาจเป็น package ส่วนตัวหรือเปลี่ยนชื่อแล้ว

---

### ❌ hoverboard-pptx

**Status:** ❌ ไม่พบ repository สาธารณะที่ชื่อนี้  
**หมายเหตุ:** อาจเป็น internal tool หรือเปลี่ยนชื่อแล้ว

---

## 2. Design Systems & Cloud APIs

### ✅ Google Slides API

**Status:** ✅ มี REST API ฟรี (ต้องมี Google Cloud account)  
**Pricing:** ฟรี up to 100 requests/user/second (quota มาพอสำหรับงานปกติ)  
**Docs:** https://developers.google.com/workspace/slides/api/reference/rest

**วิธีใช้ (Python):**
```bash
pip install google-api-python-client google-auth
```

```python
from googleapiclient.discovery import build
from google.oauth2 import service_account

# ต้องมี service account JSON key file
SCOPES = ['https://www.googleapis.com/auth/presentations']
creds = service_account.Credentials.from_service_account_file(
    'service-account.json', scopes=SCOPES)
slides_service = build('slides', 'v1', credentials=creds)

# สร้าง presentation ใหม่
presentation = slides_service.presentations().create(
    body={'title': 'My Presentation'}
).execute()
print(f"Created: {presentation.get('presentationId')}")

# เพิ่ม slide และ text
requests = [
    {
        'createSlide': {
            'slideLayoutReference': {'predefinedLayout': 'TITLE_ONLY'}
        }
    },
    {
        'insertText': {
            'objectId': '<object-id>',
            'text': 'Hello from API!'
        }
    }
]
slides_service.presentations().batchUpdate(
    body={'requests': requests},
    presentationId=presentation.get('presentationId')
).execute()
```

**ข้อจำกัด:** ต้องมี Google Cloud project + service account, ไม่สามารถใช้ template ที่มีอยู่ได้ง่ายนัก

---

### ❌ Canva API (Free Tier)

**Status:** ❌ Canva Connect API ต้องใช้ **Canva Teams subscription** ไม่มี free tier สำหรับ API  
**Docs:** https://www.canva.com/developers/docs/  
**หมายเหตุ:** มี Canva free tier สำหรับ design แต่ API ไม่ฟรี

---

### ❌ Gamma.app (Free Tier)

**Status:** ❌ ไม่มี public API สำหรับ Gamma  
**เว็บไซต์:** https://gamma.app  
**หมายเหตุ:** Gamma เป็น AI presentation generator แบบ web-only ไม่มี API, free tier จำกัดจำนวน presentations

---

## 3. Free PPTX Templates (GitHub)

### Recommended Free Template Repos:

| Repository | คำอธิบาย |
|---|---|
| [scanny/python-pptx](https://github.com/scanny/python-pptx) | มี example templates หลายแบบใน repo |
| [priyanka-nam/indeed_reports](https://github.com/priyanka-nam/indeed_reports) | มี sample PPTX templates |
| [AcademicJournals/PowerPoint-Templates](https://github.com/AcademicJournals/PowerPoint-Templates) | Academic-style templates |
| [free-powerpoint-templates](https://github.com/free-powerpoint-templates) | รวม free templates หลายชุด |

### Design Pattern จากศึกษา:

**Best Practices:**
1. **ใช้ Widescreen (16:9)** — `prs.slide_width = Inches(13.33), prs.slide_height = Inches(7.5)`
2. **สีหลักที่ใช้ได้ดี:**
   - Header bar: RGB(25, 55, 95) สีน้ำเงินเข้ม
   - Accent: RGB(100, 200, 255) สีฟ้าอ่อน
   - Code block bg: RGB(30, 30, 40)
   - Code text: RGB(100, 255, 150)
3. **ใช้ Blank layout** แล้วสร้างเองทุกอย่าง เพื่อควบคุม design ได้เต็มที่
4. **Rounded rectangle** สำหรับ code blocks
5. **Table styling** — bold header row, consistent font sizes

---

## 4. Summary: Recommended Toolchain

### 🎯 Best Free Solution: python-pptx (Programmatic)

```
✅ python-pptx 1.0.2 — สร้าง presentation เองด้วย code
   ✅ ฟรี, open source, active development
   ✅ รองรับทุก feature ของ PPTX (text, images, tables, shapes, charts)
   ✅ ใช้กับ Python 3.12+ ได้โดยตรง
   ❌ ต้องเขียน code ทุกอย่าง (ไม่มี template engine)

✅ pptx-template (GitHub) — ถ้าต้องการ template + data approach
   ✅ ง่ายสำหรับ report generation ที่มี pattern ตายตัว
   ✅ ต้องใช้ GitHub version เท่านั้น (PyPI version ล้าสมัย)

✅ Google Slides API — ถ้าต้อง integrate กับ Google Workspace
   ✅ มี quota ฟรีพอสมควร
   ❌ ต้องมี Google Cloud project
```

### ❌ Not Available / Not Recommended:
- `python-pptx-templates` — ไม่มีใน PyPI
- `markppt` — ไม่พบ
- `hoverboard-pptx` — ไม่พบ
- Canva API — ไม่มี free tier สำหรับ API
- Gamma.app — ไม่มี public API

### 📁 Sample Files Generated:
- `/tmp/test_basic.pptx` — Basic test (title + formatted text + table)
- `/tmp/esp32_demo.pptx` — Demo with 4 slides (title, content, 2-col, table)
- `/tmp/esp32_workshop.pptx` — Full STEM workshop style (dark title, bullets, code block)

---

## 5. Installation Guide

```bash
# Recommended: use uv (fast, handles Python 3.12+ well)
pip install uv
uv pip install python-pptx

# For pptx-template (GitHub version):
uv pip install git+https://github.com/m3dev/pptx-template.git

# For Google Slides API:
uv pip install google-api-python-client google-auth
```

**Note:** pip ปกติอาจมีปัญหากับ system Python 3.12 เรื่อง `pkg_resources` — ใช้ `uv` แทนได้เลย
