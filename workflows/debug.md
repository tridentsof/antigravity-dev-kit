---
description: Debug issues and fix bugs
---

# /debug - Bug Fixing

$ARGUMENTS

---

## Purpose

Systematically find and fix the root cause of issues.

---

## Protocol

### 1. Gather Information
- What is the error message?
- What are the reproduction steps?
- What's expected vs actual?

### 2. Apply Debugger Agent
Route to `@debugger` with systematic-debugging skill.

### 3. Investigation Flow

```
REPRODUCE → ISOLATE → IDENTIFY → FIX → VERIFY
```

### 4. Root Cause Analysis

| Step | Question |
|------|----------|
| Reproduce | Can we trigger it? |
| Isolate | Where does it fail? |
| Identify | What's the root cause? |
| Fix | Minimal change |
| Verify | Does it work? |

---

## Fix Approach

- ✅ Minimal change
- ✅ Add regression test
- ✅ No side effects
- ❌ Guess and patch
- ❌ Multiple unrelated changes

---

## Human Checkpoint

```markdown
🔍 **Root cause identified:**

Issue: [description]
Cause: [root cause]
Fix: [proposed solution]

**Approve fix?**
```

---

## Output

```markdown
✅ **Bug fixed**

Root cause: [description]
Fix: [what was changed]

Files modified:
- `path/to/file`

Tests:
- [x] Regression test added
- [x] All tests pass
```
