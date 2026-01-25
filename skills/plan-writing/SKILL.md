---
name: plan-writing
description: Task breakdown and project planning
---

# Plan Writing

> Structure tasks for clear execution.

---

## Plan File Format

**Location:** `docs/PLAN-{slug}.md`

```markdown
# PLAN: [Feature Name]

## Overview
Brief description of what we're building.

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Tasks

### Phase 1: Backend
- [ ] Task 1 [@backend-specialist]
- [ ] Task 2 [@database-architect]

### Phase 2: Frontend
- [ ] Task 3 [@frontend-specialist]

### Phase 3: Testing
- [ ] Task 4 [@test-engineer]

## Verification
- [ ] Run checklist.py
- [ ] Manual testing
- [ ] Code review
```

---

## Task Breakdown Rules

| Rule | Description |
|------|-------------|
| Specific | Clear deliverable |
| Atomic | Single responsibility |
| Assigned | Agent specified |
| Ordered | Dependencies clear |

---

## Naming Convention

| Request | Slug |
|---------|------|
| E-commerce cart | ecommerce-cart |
| User authentication | user-auth |
| Dashboard analytics | dashboard-analytics |

---

## Task Sizing

| Size | Description | Time |
|------|-------------|------|
| S | Single file change | < 30 min |
| M | Few files, one domain | 1-2 hours |
| L | Multiple domains | 2-4 hours |
| XL | Break into sub-tasks | - |

---

## Dependencies

```markdown
## Tasks
- [ ] 1. Create database schema [@database-architect]
- [ ] 2. Create API endpoints [@backend-specialist] (depends: 1)
- [ ] 3. Create UI components [@frontend-specialist] (depends: 2)
```

---

## DO / DON'T

| ✅ Do | ❌ Don't |
|-------|---------|
| Assign agents | Leave unassigned |
| Order by dependency | Random order |
| Include verification | Skip testing tasks |
| Break large tasks | Massive single tasks |
