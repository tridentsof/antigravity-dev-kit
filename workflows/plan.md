---
description: Create project plan with task breakdown. No code - planning only.
---

# /plan - Project Planning

$ARGUMENTS

---

## Purpose

Create a structured plan file with task breakdown. **NO CODE WRITING.**

---

## Protocol

### 1. Socratic Gate
Ask clarifying questions if request is vague.

### 2. Create Plan File
**Location:** `docs/PLAN-{slug}.md`

**Naming:** Extract 2-3 keywords, lowercase, hyphen-separated.

| Request | File |
|---------|------|
| E-commerce cart | PLAN-ecommerce-cart.md |
| User authentication | PLAN-user-auth.md |

### 3. Plan Structure

```markdown
# PLAN: [Feature Name]

## Overview
[Brief description]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Tasks

### Backend
- [ ] Task 1 [@backend-specialist]

### Frontend
- [ ] Task 2 [@frontend-specialist]

### Testing
- [ ] Task 3 [@test-engineer]

## Verification
- [ ] Run checklist.py
- [ ] Code review
```

---

## Rules

- ❌ NO code writing
- ✅ Assign agents to tasks
- ✅ Order by dependency
- ✅ Include verification

---

## After Planning

```markdown
✅ **Plan created:** docs/PLAN-{slug}.md

**Next steps:**
1. Review the plan
2. Run `/create` to implement
```
