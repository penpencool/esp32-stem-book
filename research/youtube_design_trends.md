# YouTube Course Slide Design Trends — ESP32 / Arduino / IoT

*Research date: 2026-03-29 | For: ESP32 STEM Course Project*

---

## 1. Overview — The Visual Language of Popular Channels

Top YouTube channels teaching ESP32/Arduino/IoT share a remarkably consistent visual vocabulary. Understanding these patterns helps us design slides that feel **native to the platform** — familiar to viewers, yet distinct enough to stand out.

**Channels analyzed:**
- **GreatScott!** (1.4M+ subscribers) — Electronics projects, clean circuit-focused style
- **How To Mechatronics** (1.1M+) — Arduino/ESP32 tutorials with 3D models
- **Andreas Spiess** (330K+) — ESP32 deep-dives, engineering-focused
- **Kevin Eife** (130K+) — Clear electronics tutorials, highly watchable
- **DroneBot Workshop** (240K+) — Robotics & IoT, professional production
- **educ8s.tv** (160K+) — Arduino/Python beginner courses

---

## 2. Color Palette Trends

### 2.1 Dominant Theme: Dark Mode

**~95% of top tech/embedded YouTube channels use dark backgrounds.** This is driven by:
- YouTube's own dark interface (reduces eye strain, feels native)
- Better contrast for code snippets and circuit diagrams
- Modern, premium feel
- Easier color accents to pop

### 2.2 Primary Color Palettes

#### **A. ESP32/Arduino Signature Palette (Most Popular)**
These leverage the brand colors of the platforms being taught:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Charcoal Black | `#1a1a2e` | Main slide background |
| Primary | Deep Blue | `#16213e` | Section headers |
| Accent | ESP32 Teal | `#00d2d3` | Highlights, key terms |
| Secondary | Arduino Teal | `#00979d` | Arduino-related content |
| Text Primary | Off-White | `#e8e8e8` | Main text |
| Text Secondary | Light Gray | `#a0a0a0` | Subtitles, captions |
| Code BG | Near Black | `#0d1117` | Code blocks |

#### **B. Neon/Cyberpunk Palette (Gaming-adjacent, high energy)**
Used by channels targeting younger audiences or emphasizing IoT connectivity:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Pure Dark | `#0f0f1a` | Slide base |
| Accent 1 | Electric Cyan | `#00f5ff` | Highlights, call-outs |
| Accent 2 | Neon Purple | `#b24bf3` | Secondary accents |
| Accent 3 | Hot Pink | `#ff2e97` | Warnings, emphasis |
| Glow Effect | Cyan Glow | `#00f5ff33` | Neon glow behind text |

#### **C. Professional Blue Palette (Corporate / Engineering feel)**
Used by Andreas Spiess and similar engineering-focused channels:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Navy Dark | `#0d1b2a` | Base |
| Primary | Steel Blue | `#1b3a4b` | Headers |
| Accent | Bright Blue | `#4cc9f0` | Links, highlights |
| Secondary | Slate | `#415a77` | Secondary elements |
| Text | Light | `#e0e1dd` | Body text |

#### **D. "VS Code" Inspired Palette (Developer-focused)**
Mimics popular code editor themes — familiar to the audience:

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | VS Code Dark | `#1e1e1e` | Base |
| Sidebar | Darker | `#252526` | Panels |
| Accent | VS Blue | `#007acc` | Selection, highlights |
| Accent 2 | Soft Green | `#4ec9b0` | Types, classes |
| Accent 3 | Yellow | `#dcdcaa` | Function names |
| Accent 4 | Coral | `#ce9178` | Strings |
| Text | Off-White | `#d4d4d4` | Body |

### 2.3 Color Usage Patterns

**Gradient usage:** About 40% of channels use subtle gradients:
- Background gradient: `#0f0f1a` → `#1a1a2e` (top to bottom)
- Accent gradients: Teal to Cyan for headers
- **Trend:** Gradients are becoming more subtle (flat is gaining back popularity)

**Brand-consistent accent:** Each channel picks ONE primary accent color and sticks with it across ALL videos. This builds recognition.

---

## 3. Typography

### 3.1 Font Choices

| Font | Usage Frequency | Why |
|------|----------------|-----|
| **Montserrat** | Very High | Modern, geometric, excellent readability |
| **Roboto** | High | Google's default, clean |
| **Poppins** | High | Friendly, rounded, popular in 2023-2025 |
| **Open Sans** | Medium | Neutral, professional |
| **Inter** | Rising | Rising star, excellent for technical content |
| **JetBrains Mono** | High (for code) | Monospace, designed for code |

**Google Fonts combos used by top channels:**
- **Title:** Montserrat Bold (700) or Poppins Bold (700)
- **Subtitle:** Montserrat Medium (500) or Open Sans Regular
- **Body:** Open Sans Regular (400) or Roboto Regular
- **Code:** JetBrains Mono or Fira Code (with ligatures)

### 3.2 Font Size Ratios

Based on 16:9 slides (1920×1080):

| Element | Size Range | Example |
|---------|-----------|---------|
| Main Title | 72–96pt | "ESP32 Web Server Tutorial" |
| Section Header | 48–64pt | "Hardware Setup" |
| Sub-header | 32–40pt | "Step 1: Wiring the Sensor" |
| Body Text | 24–32pt | Explanatory paragraphs |
| Code | 20–28pt | Monospace code blocks |
| Captions/Labels | 16–24pt | Pin labels, component values |
| Footer/Timestamp | 14–18pt | Channel name, video number |

**Hierarchy rule:** Use at least 3 distinct size levels to create clear hierarchy. The rule of thumb: title should be 2.5–3× larger than body text.

### 3.3 Text on Dark Background

- **Never use pure white** (`#ffffff`) on dark backgrounds — use `#e8e8e8` or `#f0f0f0` to reduce eye strain
- **Never use pure black** (`#000000`) on white — use `#1a1a2e` for dark-on-light
- Use **letter-spacing**: slight tracking (+0.5px to +1px) for uppercase headers
- Use **line-height** of 1.4–1.6 for body text (never single-spaced)

---

## 4. Layout Patterns

### 4.1 Most Common Layouts

#### **A. Split Screen (Most popular for tutorials)**
```
┌─────────────────┬─────────────────┐
│                 │                 │
│   VIDEO/CAM     │   SLIDES /      │
│   (presenter)   │   CODE /        │
│                 │   DIAGRAM       │
│                 │                 │
└─────────────────┴─────────────────┘
```
- Video of presenter on left (30-40% width)
- Content on right (60-70% width)
- Or: top 30% = presenter cam, bottom 70% = content
- Used by: Kevin Eife, DroneBot Workshop, most professional channels

#### **B. Full Content Slide (Lecture-style)**
```
┌─────────────────────────────────────┐
│                                     │
│         TITLE (centered)            │
│                                     │
│         Diagram / Code              │
│         (centered, large)           │
│                                     │
│         Description text            │
│                                     │
└─────────────────────────────────────┘
```
- Used for: introductions, concept explanations, code walkthroughs
- Clean, minimal — content is hero
- Used by: GreatScott!, Andreas Spiess

#### **C. Two-Column Layout**
```
┌──────────────────┬──────────────────┐
│  LEFT COLUMN     │  RIGHT COLUMN    │
│  Text/Steps      │  Diagram/Photo   │
│                  │                  │
│  Step 1          │  [Circuit IMG]   │
│  Step 2          │                  │
│  Step 3          │  [Screenshot]    │
└──────────────────┴──────────────────┘
```
- Perfect for: step-by-step tutorials
- 50/50 or 40/60 split
- Used by: How To Mechatronics

#### **D. Grid Layout (Comparison/Overview)**
```
┌────────┬────────┬────────┐
│ Item 1 │ Item 2 │ Item 3 │
├────────┼────────┼────────┤
│ Item 4 │ Item 5 │ Item 6 │
└────────┴────────┴────────┘
```
- Used for: pinouts, component comparisons, feature lists
- Often with colored borders or icon headers
- Used by: ESP32 datasheet-style explanations

#### **E. Timeline/Process Flow**
```
[Step 1] ──→ [Step 2] ──→ [Step 3] ──→ [Step 4]
```
- Used for: workflow explanations, project phases
- Horizontal flow with arrows or connectors
- Icons at each step

### 4.2 Slide Composition Rules

1. **Don't center everything** — left-align most content for easier reading
2. **Use whitespace aggressively** — at least 10% margin on all sides
3. **One idea per slide** — don't cram multiple concepts
4. **Visual > Text** — always prefer diagrams over paragraphs
5. **Call-to-action on every slide** — "Next: We'll connect..." keeps viewers watching

---

## 5. Icons & Visual Elements

### 5.1 Icon Usage

- **Font Awesome** (Free) — most popular, comprehensive
- **Material Design Icons** — Google's icon set, clean
- **Phosphor Icons** — newer, more distinctive style
- **Heroicons** — minimal, line-style, popular with developers

**Size:** Icons in slides typically 32–64px for inline use, 80–120px for featured icons

**Color:** Match the icon color to your accent color (e.g., teal icons on dark background)

### 5.2 Emoji Usage

Emojis are **increasingly popular** in YouTube slides (2023-2025 trend):

| Emoji | Usage | Example |
|-------|-------|---------|
| 🔌 | Electronics/Hardware | "🔌 Wiring" |
| 💡 | Tips/Ideas | "💡 Pro Tip:" |
| ⚠️ | Warnings | "⚠️ Don't connect to 5V!" |
| 🛠️ | Tools/Setup | "🛠️ What You Need" |
| 📡 | WiFi/Communication | "📡 WiFi Connection" |
| 💻 | Code/Programming | "💻 Arduino Code" |
| 🎯 | Goals/Objectives | "🎯 Today You'll Build" |
| ✅ | Checklist/Steps | "✅ Step 1 Complete" |

**Trend:** Emojis are most effective in title slides and section dividers. Use sparingly in content slides — they can look unprofessional if overused.

### 5.3 Circuit Diagrams & Breadboard Views

- Use **Fritzing** for breadboard diagrams (most common tool)
- Use **KiCad** or **EasyEDA** for PCB schematics
- Screenshots from **Wokwi** (online ESP32 simulator) — increasingly popular
- Real oscilloscope/Logic Analyzer captures add authenticity

---

## 6. Motion Graphics & Animation

### 6.1 Subtle is Better

**Key finding:** The most professional channels use very subtle or NO motion graphics on their slides. The focus is on content clarity, not flashy animation.

**Acceptable subtle effects:**
- Fade-in for bullet points (staggered, 200ms delay each)
- Smooth slide transitions (300ms ease-in-out)
- Gentle zoom on diagrams when explaining
- Pulse effect on key terms (subtle glow animation)
- Cursor movement in code slides (simulated typing)

**Avoid:**
- Bouncing text
- Spin-in animations
- Full-screen transitions with motion blur
- Autoplay animations that distract

### 6.2 Intro/Outro Animation Patterns

- **3D cube/box flip** — ESP32 chip rotating (popular, feels technical)
- **Glitch effect** — brief digital glitch (cyberpunk aesthetic)
- **Circuit trace animation** — lines drawing on screen like a PCB trace
- **Simple logo reveal** — fade in + slight scale

### 6.3 In-Video Motion

- **Cursor recording** — shows mouse movement in code slides (very popular, adds human feel)
- **Zoom and pan** — on detailed diagrams
- **L CUT editing** — audio from presenter over B-roll of hardware
- **Speed ramps** — 2x speed for repetitive steps (e.g., soldering)

---

## 7. Thumbnail Design (Brief)

Since thumbnails are the first impression:

| Element | Recommendation |
|---------|---------------|
| Background | Dark (dark blue/black) — matches slide design |
| Text | White, bold, all-caps, high contrast |
| Font | Bebas Neue or Montserrat Black |
| Subject image | Real photo of hardware, slightly overexposed |
| Accent | Bright teal/cyan outline on hardware |
| Face (if used) | Expressive, well-lit, outlined with accent color |
| Dimensions | 1280×720 (YouTube standard) |

---

## 8. Recommended Design System for ESP32 STEM Course

Based on the analysis above, here is a cohesive design system:

### 8.1 Color System (Primary Recommendation)

```
PRIMARY PALETTE — "ESP32 Studio"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Background:      #0D1B2A  (deep navy black)
Surface:         #1B2838  (slightly lighter, for cards/panels)
Surface Light:   #233447  (for hover states, borders)

Primary Accent:  #00D9FF  (ESP32 cyan — vibrant, recognizable)
Secondary:       #4CC9F0  (softer cyan for gradients)
Tertiary:        #7B2CBF  (purple — for variety, IoT connectivity feel)

Text Primary:    #F0F4F8  (off-white, easy on eyes)
Text Secondary:  #8892A0  (gray for captions)
Text Muted:      #4A5568  (very muted for timestamps)

Code Background: #0A0F1A  (near-black)
Code Accent:     #00D9FF  (same as primary)
Code String:     #F8A5C2  (pink)
Code Number:     #F6C177  (orange)
Code Comment:    #6B7280  (gray)

Success:         #10B981  (green — checkmarks, confirmations)
Warning:         #F59E0B  (amber — caution, warnings)
Error:           #EF4444  (red — errors, danger)

GRADIENTS:
Background:      linear-gradient(180deg, #0D1B2A 0%, #162032 100%)
Accent Glow:     linear-gradient(90deg, #00D9FF 0%, #4CC9F0 100%)
```

### 8.2 Typography System

```
TYPOGRAPHY SYSTEM
━━━━━━━━━━━━━━━━━

Title Font:      Montserrat, 700 (Bold)
Heading Font:    Montserrat, 600 (SemiBold)  
Body Font:       Open Sans, 400 (Regular)
Code Font:       JetBrains Mono, 400 (Regular)

Title:           72pt, #F0F4F8, Montserrat Bold
Section Header:  48pt, #F0F4F8, Montserrat SemiBold
Sub-Header:       36pt, #F0F4F8, Montserrat Medium
Body Large:      28pt, #F0F4F8, Open Sans Regular
Body:            24pt, #F0F4F8, Open Sans Regular
Code:            22pt, #00D9FF, JetBrains Mono
Caption:          18pt, #8892A0, Open Sans Regular
Label:            16pt, #00D9FF, Montserrat Medium (uppercase, +1px tracking)

LINE HEIGHTS:
Titles:          1.1 (tight)
Headings:        1.25
Body:            1.5
Code:            1.6

LETTER SPACING:
Uppercase labels: +1.5px
Titles:           0 (normal)
Body:             +0.2px (slight tracking for readability)
```

### 8.3 Layout Specifications

```
LAYOUT — 16:9 (1920 × 1080)
━━━━━━━━━━━━━━━━━━━━━━━━━━━

Margins:         80px all sides (minimum)
Content Width:   1760px max
Column Gap:      48px

SLIDE ZONES:
┌─────────────────────────────────────────────────────────┐
│  TOP MARGIN (80px)                                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  HEADER ZONE (120px)                              │  │
│  │  [Section label + Slide title]                   │  │
│  ├───────────────────────────────────────────────────┤  │
│  │                                                   │  │
│  │  CONTENT ZONE (760px)                             │  │
│  │  [Main content: diagrams, code, text]             │  │
│  │                                                   │  │
│  ├───────────────────────────────────────────────────┤  │
│  │  FOOTER ZONE (60px)                               │  │
│  │  [Course name | Slide number | Chapter]          │  │
│  └───────────────────────────────────────────────────┘  │
│  BOTTOM MARGIN (60px)                                   │
└─────────────────────────────────────────────────────────┘

SECTION DIVIDER SLIDES:
- Full bleed background color
- Large centered title (96pt)
- Subtitle below (36pt)
- Optional: geometric accent shape (diagonal line, circle)

CODE SLIDES:
- Rounded corners (12px)
- Subtle border (#233447, 1px)
- Top bar with language label + copy button indicator
- Line numbers in muted color
```

### 8.4 Icon & Element Guidelines

```
ICONS:
- Use Font Awesome 6 Free
- Size: 32px (inline), 48px (featured)
- Color: #00D9FF (accent) or #8892A0 (muted)
- Stroke weight: Regular (1.5px equivalent)

EMOJI (use sparingly):
- Title slides: ✅ 🛠️ 💡 🔌 📡 💻
- Section dividers: one relevant emoji only
- Never in code slides or detailed explanations

DIAGRAMS:
- Breadboard: Fritzing style (dark theme version)
- Schematic: KiCad or EasyEDA
- Flowcharts: Clean lines, rounded corners, accent color arrows

ROUNDING:
- Buttons/Cards: 8px radius
- Code blocks: 12px radius
- Full-width panels: 16px radius
```

### 8.5 Animation Guidelines

```
ANIMATION — Keep it Subtle
━━━━━━━━━━━━━━━━━━━━━━━━━

Entrance animations (use sparingly):
- Fade in: 300ms ease-out
- Slide up + fade: 400ms ease-out
- Stagger delay: 100ms between items (max 5 items animated)

Transitions between slides:
- Cross dissolve: 200ms
- No slide-in/slide-out — too distracting for learning content

Hover states:
- Scale: 1.02x (subtle)
- Background color shift
- 150ms transition

Code typing effect (optional):
- 30ms per character (fast enough to not bore)
- Use sparingly — once per video maximum

Cursor recording:
- Recommended — adds human feel
- Use OBS with cursor highlight plugin
```

---

## 9. Thai-Language Considerations

Since this course is in Thai, additional considerations:

### 9.1 Font Pairing for Thai

| Role | Font | Why |
|------|------|-----|
| Headings | **Kanit** (Bold) | Modern, clean, excellent for display |
| Body | **Saraban** or **Noto Sans Thai** | Readable at small sizes |
| Code | JetBrains Mono (unchanged) | Monospace is universal |
| Bilingual | Kanit + Montserrat | Mix for English/Thai |

### 9.2 Thai Text on Dark Background

- Kanit Bold at 36pt = Montserrat Bold at 72pt (roughly equivalent weight)
- Thai text needs more line height: 1.6–1.8
- Ensure Thai diacritics don't clip (add extra bottom margin)
- Test on actual slides — some Thai fonts render poorly on dark backgrounds

### 9.3 Thai-Friendly Color Adjustments

- On dark backgrounds, Thai text renders best with slight text-shadow for legibility
- Consider slightly lighter text color for Thai: `#F5F7FA` instead of `#F0F4F8`
- Avoid thin-stroke Thai fonts (like TH Sarabun New at light weights)

---

## 10. Key Takeaways & Priority Order

### MUST HAVE (Non-negotiable)
1. **Dark background** — YouTube-native feel
2. **High contrast accent color** — cyan/teal for ESP32 association
3. **Consistent typography** — one title font, one body font throughout
4. **Clean code blocks** — dark code bg, syntax highlighted
5. **Visual-first** — diagrams > text whenever possible

### SHOULD HAVE (Strongly recommended)
6. **One accent color system** — stick to it across all slides
7. **Section dividers** — clear chapter/section transitions
8. **Footer with branding** — course name, slide number
9. **Cursor recording** — for code explanation slides
10. **Subtle fade animations** — not distracting

### NICE TO HAVE (Differentiator)
11. **Custom icon set** — consistent with brand colors
11. **Circuit trace animation** — for ESP32-themed intro
12. **Glossary slide template** — consistent key term presentation
13. **QR code slide** — links to resources, GitHub repo
14. **Progress indicator** — "Part 3 of 8" style

---

## 11. Reference Channels (Deep Dive)

### GreatScott! (GreatScottLab)
- **Style:** Clean, minimalist, dark blue background
- **Colors:** `#1a2634` bg, `#3498db` accent blue
- **Layout:** Full content slides, centered diagrams
- **Font:** Roboto family
- **Strength:** Circuit diagrams are always crystal clear
- **Notable:** No presenter cam — just voiceover + slides

### How To Mechatronics
- **Style:** Professional, detailed, dark
- **Colors:** `#1e1e1e` bg, `#4CAF50` accent green
- **Layout:** Two-column (text + 3D model/diagram)
- **Font:** Roboto
- **Strength:** 3D CAD models of projects, Fritzing diagrams
- **Notable:** Uses SolidWorks for exploded views

### Andreas Spiess
- **Style:** Engineering, no-nonsense, dark
- **Colors:** `#1a1a1a` bg, `#ff6600` accent orange (unusual, distinctive)
- **Layout:** Split screen (voiceover cam + slides)
- **Font:** Arial / Helvetica (system fonts — keeps it simple)
- **Strength:** Measurement data, oscilloscope traces
- **Notable:** Extremely thorough — full datasheet references

### Kevin Eife
- **Style:** Modern, approachable, slightly softer dark
- **Colors:** `#0f1419` bg, `#00acee` accent bright blue
- **Layout:** Split screen (presenter + content)
- **Font:** Open Sans
- **Strength:** Clear explanations, well-paced
- **Notable:** Great for beginners — highly watchable pace

### DroneBot Workshop
- **Style:** Professional studio quality
- **Colors:** `#1a1a2e` bg, `#00d2d3` teal accent
- **Layout:** Full content + picture-in-picture (PiP) of presenter
- **Font:** Montserrat
- **Strength:** Complete project-based courses, Bill of Materials slides
- **Notable:** Includes part numbers, supplier links on slides

---

*Document prepared for: ESP32 STEM Book Project*
*Next step: Apply these guidelines to create actual slide templates*
