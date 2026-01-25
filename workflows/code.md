---
description: Generate code for a specific task
---

# /code - Code Generation

$ARGUMENTS

---

## Purpose

Generate code for a specific task with appropriate specialist.

---

## Protocol

### 1. Route to Agent
Analyze request and select specialist:

| Keywords | Agent |
|----------|-------|
| vue, component, pinia | frontend-specialist |
| api, controller, c# | backend-specialist |
| sql, schema | database-architect |

### 2. Apply Agent Rules
Load agent's skills and follow their patterns.

### 3. Generate Code
Write clean, tested code following standards.

### 4. Verify

```bash
# Frontend
npm run lint && npm run type-check

# Backend
dotnet build && dotnet test
```

---

## Output Format

```markdown
🤖 **Applying `@[agent-name]`...**

Created/Modified:
- `path/to/file.ts`
- `path/to/file.cs`

```[language]
// Code snippet
```

**Verification:**
- [x] Lint passed
- [x] Types checked
```

---

## Rules

- ✅ Follow clean-code standards
- ✅ Include TypeScript types
- ✅ Add comments for complex logic
- ❌ No `any` types
- ❌ No hardcoded secrets

---

## After Coding

```markdown
✅ **Code complete**

Next: `/test` to generate tests
```
