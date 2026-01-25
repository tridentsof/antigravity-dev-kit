# Animation Guidelines

> Animation principles and timing psychology. Learn to decide, not copy.

---

## Duration Principles

### What Affects Timing

```
Factors determining animation speed:
├── DISTANCE: Further travel = longer duration
├── SIZE: Larger elements = slower animations
├── IMPORTANCE: Critical actions = clear feedback
└── CONTEXT: Urgent = fast, luxurious = slow
```

### Duration Ranges

| Purpose | Range | Example |
|---------|-------|---------|
| Instant feedback | 50-100ms | Button press |
| Micro-interactions | 100-200ms | Hover effects |
| Standard transitions | 200-300ms | Tabs, toggles |
| Complex animations | 300-500ms | Modal open |
| Page transitions | 400-600ms | Route change |
| Premium/Wow effects | 800ms+ | Hero reveals |

---

## Easing Principles

| Easing | Best For | Feels Like |
|--------|----------|------------|
| **ease-out** | Elements entering | Arriving, settling |
| **ease-in** | Elements leaving | Departing, exiting |
| **ease-in-out** | Emphasis, loops | Smooth, deliberate |
| **linear** | Continuous motion | Mechanical |
| **spring/bounce** | Playful UI | Fun, energetic |

### The Pattern

```css
/* ENTERING = ease-out (decelerate) */
.enter { animation-timing-function: ease-out; }

/* LEAVING = ease-in (accelerate) */
.exit { animation-timing-function: ease-in; }

/* CONTINUOUS = ease-in-out */
.loop { animation-timing-function: ease-in-out; }
```

---

## Micro-Interactions

### Purpose

```
├── FEEDBACK: Confirm action happened
├── GUIDANCE: Show what's possible
├── STATUS: Indicate current state
└── DELIGHT: Small moments of joy
```

### Button States

| State | Effect | Tailwind Example |
|-------|--------|------------------|
| Hover | Lift + glow | `hover:-translate-y-1 hover:shadow-lg` |
| Active | Press down | `active:scale-95` |
| Focus | Ring indicator | `focus:ring-2 focus:ring-offset-2` |
| Loading | Spinner | `animate-spin` |

---

## Scroll Animations (Vue3 + Tailwind)

### Intersection Observer Pattern

```vue
<script setup lang="ts">
import { ref, onMounted } from 'vue'

const isVisible = ref(false)
const element = ref<HTMLElement>()

onMounted(() => {
  const observer = new IntersectionObserver(([entry]) => {
    isVisible.value = entry.isIntersecting
  }, { threshold: 0.1 })
  
  if (element.value) observer.observe(element.value)
})
</script>

<template>
  <div 
    ref="element"
    :class="[
      'transition-all duration-500 ease-out',
      isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
    ]"
  >
    Content reveals on scroll
  </div>
</template>
```

### Staggered Animation

```vue
<template>
  <div v-for="(item, i) in items" :key="i"
    :style="{ transitionDelay: `${i * 100}ms` }"
    :class="isVisible ? 'opacity-100' : 'opacity-0'"
  >
    {{ item }}
  </div>
</template>
```

---

## Vue Transition Components

```vue
<!-- Fade -->
<Transition name="fade">
  <div v-if="show">Content</div>
</Transition>

<style>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>

<!-- Slide Up -->
<Transition name="slide-up" appear>
  <div v-if="show">Content</div>
</Transition>

<style>
.slide-up-enter-active {
  transition: all 0.4s ease-out;
}
.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
</style>
```

---

## Performance Rules

### ✅ Animate ONLY

```css
/* GPU-accelerated (FAST) */
transform: translate(), scale(), rotate();
opacity: 0 to 1;
```

### ❌ NEVER Animate

```css
/* CPU-intensive (SLOW) */
width, height
top, left, right, bottom
margin, padding
border-radius
box-shadow
```

### Accessibility (MANDATORY)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Animation Checklist

Before adding animation:

- [ ] **Purpose** - Feedback, guidance, or delight?
- [ ] **Timing** - Appropriate duration?
- [ ] **Easing** - Correct for enter/exit/emphasis?
- [ ] **Performance** - transform/opacity only?
- [ ] **Reduced motion** - Accessibility respected?
- [ ] **Consistency** - Matches other animations?

### Anti-Patterns

- ❌ Same timing every project
- ❌ Animation without purpose
- ❌ Ignoring reduced-motion
- ❌ Animating expensive properties
- ❌ Too many things moving at once

---

> **Remember:** Animation is communication. Every motion should serve the user.
