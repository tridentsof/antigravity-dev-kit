# Design Systems Reference

> Color theory, typography, and visual hierarchy principles for Vue3 + Tailwind.

---

## Color Principles

### 60-30-10 Rule

```
60% → Primary/Background (calm, neutral base)
30% → Secondary (supporting areas)
10% → Accent (CTAs, highlights)
```

### Color Psychology

| Need | Consider | Avoid |
|------|----------|-------|
| Trust, calm | Blue family | Aggressive reds |
| Growth, nature | Green family | Industrial grays |
| Energy, urgency | Orange, red | Passive blues |
| Luxury | Deep Teal, Gold, Emerald | Cheap brights |
| Clean, minimal | Neutrals | Overwhelming color |

### ⛔ Colors to AVOID (AI Clichés)

| ❌ Avoid | Why | ✅ Try Instead |
|----------|-----|----------------|
| Purple/Violet | #1 AI default | Teal, Emerald, Coral |
| Fintech Blue | Safe harbor | Signal Orange, Deep Green |
| Pink gradients | Overused | Rich Gold, Warm Terracotta |
| Neon glow | Generic "tech" | Solid contrast, texture |

### Selection Process

1. **Industry?** → Narrows options
2. **Emotion?** → Picks primary
3. **Light/Dark mode?** → Sets foundation
4. **ASK USER** if not specified

---

## Tailwind Custom Palette

```javascript
// tailwind.config.js - UNIQUE colors
module.exports = {
  theme: {
    extend: {
      colors: {
        // Define brand-specific colors
        brand: {
          50: '#f0fdfa',
          500: '#14b8a6', // Primary - NOT purple
          900: '#134e4a',
        },
        accent: {
          DEFAULT: '#f59e0b', // Distinctive accent
          hover: '#d97706',
        }
      }
    }
  }
}
```

---

## Typography Principles

### Scale Ratios

| Content Type | Ratio | Feel |
|--------------|-------|------|
| Dense UI | 1.125-1.2 | Compact, efficient |
| General web | 1.25 | Balanced |
| Editorial | 1.333 | Readable, spacious |
| Hero/display | 1.5-1.618 | Dramatic |

### Font Pairing Concept

```
Contrast + Harmony:
├── DIFFERENT enough for hierarchy
├── SIMILAR enough for cohesion
└── Usually: display + neutral, or serif + sans
```

### ⛔ Fonts to AVOID (AI Defaults)

| ❌ Avoid | Why | ✅ Try Instead |
|----------|-----|----------------|
| Inter | Every AI uses it | Space Grotesk, DM Sans |
| Roboto | Generic | Outfit, General Sans |
| Poppins | Overused | Cabinet Grotesk, Clash Display |
| System fonts | Lazy | Research unique fonts |

### Unique Font Suggestions

| Purpose | Font Options |
|---------|--------------|
| Display/Hero | Clash Display, Cabinet Grotesk, Syne |
| Body | DM Sans, Outfit, General Sans |
| Mono/Code | JetBrains Mono, Fira Code |
| Elegant | Fraunces, Newsreader, Lora |

---

## Tailwind Typography Setup

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: {
        display: ['Clash Display', 'sans-serif'],
        body: ['DM Sans', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      fontSize: {
        'hero': ['4.5rem', { lineHeight: '1.1', letterSpacing: '-0.02em' }],
        'display': ['3rem', { lineHeight: '1.2' }],
      }
    }
  }
}
```

### Readability Rules

- **Line length:** 45-75 characters optimal
- **Line height:** 1.4-1.6 for body
- **Contrast:** WCAG AA minimum (4.5:1)
- **Base size:** 16px+ for web

---

## Visual Hierarchy

### Sizing Principles

| Element | Consideration |
|---------|---------------|
| **Touch targets** | Min 44×44px mobile |
| **Buttons** | Height by importance (48/40/36px) |
| **Inputs** | Match button height |
| **Cards** | Consistent padding |
| **Reading width** | max-w-prose (65ch) |

### 8-Point Grid

```css
/* All spacing in multiples of 8 */
.spacing {
  --space-1: 4px;   /* half-step */
  --space-2: 8px;
  --space-3: 16px;
  --space-4: 24px;
  --space-5: 32px;
  --space-6: 48px;
  --space-7: 64px;
  --space-8: 80px;
}
```

---

## Border Radius Strategy

**Don't default to `rounded-md`!**

| Style | Radius | Use Case |
|-------|--------|----------|
| **Sharp** | 0-2px | Tech, Luxury, Brutalist |
| **Subtle** | 4-6px | Professional, B2B |
| **Medium** | 8-12px | General, balanced |
| **Friendly** | 16-24px | Social, lifestyle |
| **Pill** | 9999px | Buttons, badges |

```javascript
// tailwind.config.js - COMMIT to a style
module.exports = {
  theme: {
    extend: {
      borderRadius: {
        'card': '2px',      // Sharp for tech
        'button': '9999px', // Pill buttons
      }
    }
  }
}
```

---

## Shadow Hierarchy

```css
/* Tailwind shadow scale */
.elevation-1 { @apply shadow-sm; }   /* Subtle lift */
.elevation-2 { @apply shadow-md; }   /* Cards */
.elevation-3 { @apply shadow-lg; }   /* Modals, dropdowns */
.elevation-4 { @apply shadow-xl; }   /* Popovers */
.elevation-5 { @apply shadow-2xl; }  /* Dialogs */

/* Custom dramatic shadow */
.shadow-dramatic {
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.25),
    0 0 0 1px rgba(0, 0, 0, 0.05);
}
```

---

## Quick Decision Checklist

- [ ] **Color** - NOT purple, justified choice
- [ ] **Typography** - NOT Inter/Roboto, unique fonts
- [ ] **Border radius** - Committed style (sharp OR rounded)
- [ ] **Shadows** - Elevation hierarchy defined
- [ ] **Spacing** - 8-point grid consistent
- [ ] **60-30-10** - Color ratio balanced

---

> **Remember:** Design systems create consistency. Define your tokens ONCE, use everywhere.
