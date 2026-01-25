---
description: Full feature implementation with checkpoints
---

# /create - Feature Build

$ARGUMENTS

---

## Purpose

Implement a complete feature with human checkpoints.

---

## Protocol

### 1. Check for Plan
Look for `docs/PLAN-*.md` matching the request.
- If exists → Follow the plan
- If not → Run `/plan` first

### 2. Execute Tasks
Follow plan tasks in order, using assigned agents.

### 3. Checkpoints

**After each phase:**
```markdown
🛑 **Checkpoint: [Phase Name]**

Completed:
- [x] Task 1
- [x] Task 2

Next: [Phase Name]

**Approve to continue?**
```

### 4. Verification
Run appropriate validation scripts.

---

## Workflow

```
/plan → Approve → /code (backend) → /code (frontend) → /test → /review → Approve
```

---

## Human-in-the-Loop

| Checkpoint | When |
|------------|------|
| After planning | Before coding starts |
| After backend | Before frontend |
| After tests | Before review |
| Before deploy | Final approval |

---

## Completion

```markdown
✅ **Feature complete:** [Feature Name]

Files created/modified:
- [list files]

Verification:
- [x] Tests pass
- [x] Lint clean

**Ready for `/deploy`?**
```
