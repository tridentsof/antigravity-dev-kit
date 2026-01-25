---
name: frontend-design
description: UI/UX design thinking and decision-making. Use when designing layouts, color schemes, typography, or visual interfaces. Teaches principles, not fixed values.
---

# Frontend Design System

> **Philosophy:** Every pixel has purpose. Restraint is luxury. User psychology drives decisions.
> **Core Principle:** THINK, don't memorize. ASK, don't assume.

---

## 📑 Reference Files

| File | When to Read |
|------|--------------|
| [ux-psychology.md](ux-psychology.md) | 🔴 **ALWAYS** - Core UX laws |
| [animation-guide.md](animation-guide.md) | When animations needed |
| [design-systems.md](design-systems.md) | Color/typography decisions |

---

## ⛔ ANTI-AI-SLOP RULES (CRITICAL)

**Your training data makes you converge to generic designs. BREAK THIS!**

| AI Default Tendency | Why It's Bad | Think Instead |
|---------------------|--------------|---------------|
| **Purple/Violet gradients** | #1 AI cliché | Try Teal, Emerald, Signal Orange |
| **Inter/Roboto fonts** | Every AI uses these | Research unique fonts for context |
| **Bento Grids** | Overused layout | Try asymmetric, staggered, overlap |
| **Hero Split (Left/Right)** | Predictable | Massive typography, vertical flow |
| **Mesh/Aurora Gradients** | Lazy background | Solid contrast, textures, patterns |
| **Glassmorphism everywhere** | AI "premium" idea | Raw borders, high-contrast flat |
| **Dark + neon glow** | Generic "tech" look | What does the BRAND need? |
| **rounded-md on everything** | Safe/boring | Go extreme: 0px OR 24px+ |

> 🔴 **"If it looks like a Tailwind template, you have FAILED."**

---

## 🧠 DEEP DESIGN THINKING (MANDATORY)

**Before ANY design, answer internally:**

```
🔍 CONTEXT ANALYSIS:
├── What sector? → What emotions should it evoke?
├── Who is the audience? → Age, expectations, tech-savviness?
├── What do competitors look like? → What should I NOT do?
└── What is the soul of this app? → In one word?

🎨 DESIGN IDENTITY:
├── What will make this UNFORGETTABLE?
├── What unexpected element can I use?
├── 🚫 CLICHÉ CHECK: Am I defaulting to AI patterns?
└── Will I remember this design in a year?

📐 LAYOUT HYPOTHESIS:
├── How can the Hero be DIFFERENT?
├── Where can I break the grid?
└── Can navigation be unconventional?
```

---

## 🎨 DESIGN COMMITMENT (REQUIRED OUTPUT)

**Present this block to user BEFORE coding:**

```markdown
🎨 DESIGN COMMITMENT:

- **Style Choice:** [Brutalist / Neo-Retro / Swiss Punk / Minimal Luxury]
- **Primary Color:** [NOT purple/blue - justify choice]
- **Typography:** [Specific fonts, not Inter/Roboto]
- **Layout Risk:** [What unconventional decision did I take?]
- **Cliché Avoided:** [Which AI default did I explicitly kill?]
```

---

## ⚠️ ASK BEFORE ASSUMING

**If user request is vague, ASK:**

| Unspecified | Ask This |
|-------------|----------|
| Color | "What palette? (warm/cool/bold/minimal)" |
| Style | "What vibe? (professional/playful/luxurious)" |
| Layout | "Any preference? (spacious/dense/asymmetric)" |
| Audience | "Who is this for? (age/tech-savviness)" |

---

## 📐 LAYOUT PRINCIPLES

### Layout Alternatives (NOT Split Screen)

| Layout | When to Use |
|--------|-------------|
| **Massive Typography** | Hero with 80px+ text as visual |
| **Staggered Grid** | Cards at different alignments |
| **Overlapping Elements** | Depth through z-layers |
| **Extreme Asymmetry** | 90/10 split for tension |
| **Vertical Flow** | No "above the fold" hero |

### 8-Point Grid

```
All spacing in multiples of 8:
├── Tight: 4px, 8px
├── Medium: 16px, 24px
├── Large: 32px, 48px
└── XL: 64px, 80px
```

---

## ✨ MANDATORY VISUAL POLISH

### Animation Requirements

- [ ] **Scroll reveals** - Staggered entrance animations
- [ ] **Micro-interactions** - Hover/click feedback on all interactive elements
- [ ] **Spring physics** - Natural, not linear easing
- [ ] **prefers-reduced-motion** - MUST respect accessibility

### Depth & Texture

- [ ] **Layering** - Overlapping elements, parallax
- [ ] **Shadows** - Meaningful elevation hierarchy
- [ ] **Texture** - Grain, patterns, not flat colors only

---

## 🧐 REALITY CHECK (ANTI-SELF-DECEPTION)

Before delivering, verify HONESTLY:

| Question | FAIL | PASS |
|----------|------|------|
| "Could this be a template?" | "It's clean..." | "No way, this is unique" |
| "Would I scroll past on Dribbble?" | "It's professional" | "I'd stop and look" |
| "Can I describe without 'clean'?" | "Clean minimal" | "Brutalist with aurora accents" |

### Self-Deception Patterns

- ❌ "I used custom color" → But it's still blue+white
- ❌ "I have hover effects" → But just `opacity: 0.8`
- ❌ "Layout is varied" → But 3-column equal grid

> 🔴 **If it looks generic, you have FAILED. No exceptions.**

---

## Vue3 + Tailwind Implementation

### Component Animation (Vue)

```vue
<template>
  <Transition name="slide-up" appear>
    <div v-if="show" class="card">...</div>
  </Transition>
</template>

<style>
.slide-up-enter-active { transition: all 0.4s ease-out; }
.slide-up-enter-from { opacity: 0; transform: translateY(20px); }
</style>
```

### Tailwind Custom Theme

```javascript
// tailwind.config.js - CUSTOMIZE, don't use defaults
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#0d9488', // NOT default purple
        accent: '#f59e0b',  // Distinctive accent
      },
      fontFamily: {
        display: ['Space Grotesk', 'sans-serif'], // Unique font
        body: ['DM Sans', 'sans-serif'],
      },
      borderRadius: {
        'card': '2px', // Sharp, not rounded-md
      }
    }
  }
}
```

---

> **Remember:** Design is THINKING, not copying. Avoid the "Modern SaaS Safe Harbor"!
