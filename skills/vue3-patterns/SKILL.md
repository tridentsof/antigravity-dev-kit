---
name: vue3-patterns
description: Vue3 Composition API, Pinia, Vue Router, and Tailwind CSS patterns
---

# Vue3 Patterns

> Modern Vue3 with Composition API, TypeScript, Pinia, and **Tailwind CSS**.

---

## Component Structure

```vue
<script setup lang="ts">
// 1. Imports
import { ref, computed, onMounted } from 'vue'

// 2. Props & Emits
const props = defineProps<{ title: string }>()
const emit = defineEmits<{ (e: 'update', value: string): void }>()

// 3. Reactive State
const count = ref(0)

// 4. Computed
const doubled = computed(() => count.value * 2)

// 5. Methods
const increment = () => count.value++

// 6. Lifecycle
onMounted(() => console.log('Mounted'))
</script>

<template>
  <div class="p-4 rounded-lg bg-white shadow-md">
    <h2 class="text-xl font-semibold">{{ title }}</h2>
    <p class="mt-2 text-gray-600">Count: {{ count }}</p>
  </div>
</template>
```

---

## Tailwind CSS with Vue3

### Styling Approach

| Approach | When to Use |
|----------|-------------|
| **Utility classes** | Default - inline in template |
| **@apply in scoped** | Complex repeated patterns |
| **CSS variables** | Dynamic theming |

### Button with Tailwind

```vue
<template>
  <button class="
    px-4 py-2 font-medium rounded-lg
    bg-primary text-white
    transition-all duration-200 ease-out
    hover:-translate-y-0.5 hover:shadow-lg
    active:scale-95
    focus:outline-none focus:ring-2 focus:ring-primary/50
    disabled:opacity-50 disabled:cursor-not-allowed
  ">
    <slot />
  </button>
</template>
```

### Dynamic Classes

```vue
<template>
  <div :class="[
    'p-4 rounded-lg transition-colors',
    isActive ? 'bg-primary text-white' : 'bg-gray-100',
    { 'opacity-50': disabled }
  ]">
    Content
  </div>
</template>
```

---

## Vue Transitions with Tailwind

```vue
<template>
  <Transition
    enter-active-class="transition-all duration-300 ease-out"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition-all duration-200 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div v-if="show" class="p-4 bg-white rounded-lg shadow">
      Animated content
    </div>
  </Transition>
</template>
```

---

## State Management

| Scope | Solution |
|-------|----------|
| Component | `ref()`, `reactive()` |
| Parent-child | Props + Emits |
| Global | Pinia store |

### Pinia Store

```typescript
export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const isLoggedIn = computed(() => !!user.value)
  
  async function login(credentials: Credentials) {
    user.value = await api.login(credentials)
  }
  
  return { user, isLoggedIn, login }
})
```

---

## Composables

```typescript
// composables/useCounter.ts
export function useCounter(initial = 0) {
  const count = ref(initial)
  const increment = () => count.value++
  const decrement = () => count.value--
  return { count, increment, decrement }
}
```

---

## Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0d9488',
        accent: '#f59e0b',
      },
      fontFamily: {
        sans: ['DM Sans', 'sans-serif'],
        display: ['Space Grotesk', 'sans-serif'],
      }
    }
  }
}
```

---

## TypeScript

| Pattern | Example |
|---------|---------|
| Props | `defineProps<{ id: number }>()` |
| Emits | `defineEmits<{ (e: 'click'): void }>()` |
| Ref typing | `const user = ref<User \| null>(null)` |

---

## Constants & Enums

```typescript
// ✅ Correct: constants/auth.ts
export enum UserRole {
  ADMIN = 'admin',
  USER = 'user'
}

export const API_ENDPOINTS = {
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout'
} as const;

// Usage
if (role === UserRole.ADMIN) { ... }
```

---

## Configuration Management

```bash
# ✅ Correct: .env
VITE_API_URL=https://api.example.com
VITE_ENABLE_ANALYTICS=true
```

```typescript
// src/config.ts
export const config = {
  apiUrl: import.meta.env.VITE_API_URL,
  enableAnalytics: import.meta.env.VITE_ENABLE_ANALYTICS === 'true'
} as const;
```

```

---

## Icons

> **CRITICAL:** Do NOT use emojis as icons. Use professional SVG libraries.

**Recommended Libraries:**
- [Lucide Vue](https://lucide.dev/guide/packages/lucide-vue-next) (Preferred)
- [Heroicons](https://heroicons.com/)
- [Phosphor Icons](https://phosphoricons.com/)

```vue
<!-- ❌ Wrong: Emoji -->
<button>🚀 Submit</button>

<!-- ✅ Correct: Lucide Icon -->
<script setup>
import { Rocket } from 'lucide-vue-next'
</script>

<template>
  <button class="flex items-center gap-2">
    <Rocket class="w-4 h-4" />
    <span>Submit</span>
  </button>
</template>
```

---

## DO / DON'T

| Do | Don't |
|-------|---------|
| Composition API | Options API |
| TypeScript strict | `any` type |
| Pinia for global state | Vuex |
| Tailwind utilities | Inline styles |
| Custom Tailwind config | Default colors only |
| Small components | Giant components |
| Constants/Enums for strings | Magic strings |
| Env files for config | Hardcoded config |
| SVG Icons (Lucide/Heroicons) | Emojis as icons |
