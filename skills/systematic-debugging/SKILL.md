---
name: systematic-debugging
description: Root cause analysis and debugging methodology
---

# Systematic Debugging

> Find root causes, not just symptoms.

---

## Debugging Flow

```
1. REPRODUCE → Can you trigger the bug?
2. ISOLATE   → Where exactly does it fail?
3. IDENTIFY  → What is the root cause?
4. FIX       → Minimal change to solve it
5. VERIFY    → Does it work? Any regressions?
```

---

## Questions to Ask

### Reproduce
- What are the exact steps?
- What's expected vs actual?
- Is it consistent or intermittent?

### Isolate
- Which file/function fails?
- What changed recently?
- What are the inputs?

### Identify
- Is this the root cause or symptom?
- Why does this happen?
- Are there similar issues?

---

## Error Pattern Analysis

| Symptom | Check |
|---------|-------|
| 500 error | Logs, exception details |
| 404 error | Routes, URLs |
| Null reference | Data flow, null checks |
| Type error | Types, casting |
| Works locally | Environment config |
| Intermittent | Race conditions, timing |

---

## Logging Strategy

```csharp
// C# - structured logging
_logger.LogError(ex, "Failed to process order {OrderId}", orderId);
```

```typescript
// TypeScript
console.error('Failed to fetch user:', { userId, error });
```

---

## Fix Principles

| Principle | Description |
|-----------|-------------|
| Minimal | Smallest change that works |
| Focused | Only fix the bug |
| Tested | Add regression test |
| Documented | Comment if complex |

---

## Post-Fix Checklist

- [ ] Root cause confirmed
- [ ] Minimal fix applied
- [ ] Regression test added
- [ ] No side effects
- [ ] Documentation updated

---

## DO / DON'T

| ✅ Do | ❌ Don't |
|-------|---------|
| Find root cause | Patch symptoms |
| Minimal changes | Multiple fixes |
| Add tests | Skip verification |
| Check side effects | Assume it works |
