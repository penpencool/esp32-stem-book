# Skills & Tools สำหรับทำ PowerPoint/Presentation

> สรุปผลการค้นหาเมื่อ 2026-03-29

---

## 1. Skills ที่มีอยู่แล้วในระบบ (Local Skills)

### ✅ `felo-slides` (OpenClaw Skill)

| รายละเอียด | ข้อมูล |
|---|---|
| **สถานะ** | ✅ ติดตั้งแล้วใน `~/.openclaw/workspace/skills/felo-slides/` |
| **ราคา** | 💰 ต้องใช้ API Key จาก [felo.ai](https://felo.ai) (มี free tier) |
| **ทำอะไรได้** | สร้าง PPT/สไลด์จาก topic หรือ outline ด้วย Felo PPT Task API |
| **วิธีใช้** | ใช้คำสั่ง `/felo-slides` หรือ trigger keyword: slides, PPT, presentation deck |
| **Output** | ได้ลิงค์ PPT URL + Live Doc URL |
| **Theme** | รองรับการเลือก theme ด้วยคำสั่ง `felo ppt-themes` |
| **ตัวอย่าง** | `node felo-slides/scripts/run_ppt_task.mjs --query "เนื้อหาสไลด์" --interval 10 --max-wait 1800` |
| **ข้อจำกัด** | ต้องมี API key, ใช้ external API ไม่ใช่ local generation |

**📌 สรุป:** Skill หลักที่ใช้สร้าง PPT ได้เลย ติดตั้งแล้ว รอแค่ API Key

---

## 2. ค้นหาใน ClawhHub (clawhub.ai)

**ผลลัพธ์:** ❌ ไม่พบ skills ที่ตรงกับคำค้น `presentation`, `powerpoint`, `slides`, `pptx`

> หมายเหตุ: ClawhHub ใช้ JavaScript dynamic loading ทำให้ web fetch อ่านไม่ได้ทั้งหมด อาจมี skills ที่ยังไม่จัดทำ index ไว้

---

## 3. GitHub Projects & python-pptx Templates

### 🏆 McK PPT Design Skill (ดีที่สุด - AI Agent โดยเฉพาะ)

| รายละเอียด | ข้อมูล |
|---|---|
| **ชื่อ** | `likaku/Mck-ppt-design-skill` |
| **สถานะ** | ⭐ ดาว GitHub: สูงมาก, อัปเดตล่าสุด Mar 27, 2026 |
| **ราคา** | 🆓 ฟรี (Apache 2.0) |
| **ทำอะไรได้** | ระบบออกแบบ PPT สไตล์ Consulting Firm สำหรับ AI Agent — 70 layout patterns, BLOCK_ARC chart engine, icon library |
| **สถาปัตยกรรม 4 Tiers** | 1. SKILL.md (6,100 lines design specs) 2. mck_ppt/ Python engine 3. QA + Auto-fix pipeline 4. Post-processing (file corruption defense) |
| **จุดเด่น** | ลด output tokens 80%, ใช้ CPU deterministic execution แทน GPU inference สำหรับงานสร้าง chart |
| **ภาษา** | รองรับ CJK (Chinese, Japanese, Korean) อัตโนมัติ |
| **URL** | https://github.com/likaku/Mck-ppt-design-skill |

**📌 สรุป:** เป็น OpenClaw Skill ที่ใช้ได้โดยตรง! ออกแบบมาสำหรับ AI agents

---

### 💡 AI PPT Slide Generator (FastAPI + Gemini)

| รายละเอียด | ข้อมูล |
|---|---|
| **ชื่อ** | `ysskrishna/ai-ppt-slide-generator` |
| **ราคา** | 🆓 ฟรี (MIT) — ต้องมี Google Gemini API Key |
| **ทำอะไรได้** | FastAPI backend สร้าง PPT ด้วย Gemini AI, รองรับ custom layout, fonts, colors |
| **Endpoints** | `POST /api/v1/presentations/` สร้าง PPT, `GET .../download` ดาวน์โหลด |
| **Database** | PostgreSQL |
| **วิธีใช้** | Docker Compose หรือ run locally |
| **URL** | https://github.com/ysskrishna/ai-ppt-slide-generator |

---

### 📊 Automate PowerPoint (Supply Chain Reports)

| รายละเอียด | ข้อมูล |
|---|---|
| **ชื่อ** | `samirsaci/automate-powerpoint` |
| **ราคา** | 🆓 ฟรี |
| **ทำอะไรได้** | สร้าง PPT รายงานอัตโนมัติจากข้อมูล SQL, มี KPI + charts |
| **เหมาะกับ** | รายงาน operational reports, supply chain dashboards |
| **URL** | https://github.com/samirsaci/automate-powerpoint |

---

### 🛠️ python-pptx Template Tools

| ชื่อ | ราคา | คำอธิบาย |
|---|---|---|
| `kwlo/python-pptx-templater` | 🆓 ฟรี | สร้าง PPT จาก predefined layout template |
| `stellatechnologies/python-pptx-template` | 🆓 ฟรี | ใช้ Jinja2 tags สร้าง PPT (คล้าย docx-template) |
| `paradox-solver/PPTeXpress` | 🆓 ฟรี (MIT) | Web-based PPTX editor แก้ไข content ใน template โดยไม่ทำลาย design, มี versioning แบบ Git |
| `npogeant/deckflow` | 🆓 ฟรี (MIT) | Library สำหรับ extract/modify/update PPT content ผ่าน Python API |
| `bharath5673/python-pptx-tables` | 🆓 ฟรี | Helper สำหรับสร้างตารางใน PPT ง่ายขึ้น |
| `centipede13/PPT_Generation_with_Python-pptx` | 🆓 ฟรี | Script สร้าง PPT จาก text และ image |

---

## 4. สรุปตารางเปรียบเทียบ

| Tool | ประเภท | ราคา | AI-powered | ยากง่าย | เหมาะกับ |
|---|---|---|---|---|---|
| **felo-slides** (local skill) | OpenClaw Skill | 💰 API key | ✅ | ง่าย | สร้าง PPT จาก topic ทันที |
| **Mck-ppt-design-skill** | GitHub + Skill format | ฟรี | ✅ | ปานกลาง | AI agents สร้าง PPT สไตล์ consulting |
| **ai-ppt-slide-generator** | FastAPI backend | ฟรี + Gemini key | ✅ | ปานกลาง | สร้าง API service สำหรับ PPT |
| **automate-powerpoint** | Python script | ฟรี | ❌ | ยากกว่า | รายงานอัตโนมัติจาก data |
| **PPTeXpress** | Web app | ฟรี | ❌ | ง่าย | แก้ไข PPT template แบบ form-filling |
| **deckflow** | Python library | ฟรี | ❌ | ยากกว่า | Programmatic PPT manipulation |

---

## 5. คำแนะนำสำหรับโปรเจกต์ ESP32 STEM Book

### ทางเลือกที่แนะนำตามลำดับ:

1. **🥇 `felo-slides` (มีอยู่แล้ว!)** — ใช้ได้เลยหากมี API key จาก felo.ai
2. **🥈 McK-ppt-design-skill** — แปลงเป็น OpenClaw skill ได้ เหมาะกับงานที่ต้องการ PPT สวยๆ แบบ consulting
3. **🥉 PPTeXpress** — ใช้แก้ไข template PPT ที่มีอยู่แล้วโดยไม่ทำลาย design

### ขั้นตอนถัดไป:
- หากต้องการใช้ `felo-slides` → ขอ API key จาก [felo.ai](https://felo.ai) → Settings → API Keys
- หากต้องการ AI Agent ที่ฉลาดกว่า → clone `Mck-ppt-design-skill` และสร้าง OpenClaw skill wrapper
- หากต้องการแก้ไข template ที่มีอยู่ → ใช้ PPTeXpress

---

*รายงานนี้สร้างโดย subagent เมื่อ 2026-03-29 15:40 GMT+7*
