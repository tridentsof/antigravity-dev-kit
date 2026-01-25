---
description: Multi-agent coordination for complex tasks
---

# /orchestrate - Multi-Agent Task

$ARGUMENTS

---

## Purpose

Coordinate multiple specialist agents for complex, multi-domain tasks.

---

## Protocol

### 1. Analyze Request
Identify all domains involved:
- Frontend (Vue3)?
- Backend (ASP.NET)?
- Database (SQL Server)?
- DevOps (Azure)?

### 2. Create Orchestration Plan

```markdown
## Orchestration Plan: [Task]

### Agents Required
- @backend-specialist
- @frontend-specialist
- @database-architect

### Phases
1. Database schema [@database-architect]
2. API endpoints [@backend-specialist]
3. UI components [@frontend-specialist]
4. Integration tests [@test-engineer]

### Checkpoints
- After Phase 2 (backend complete)
- After Phase 4 (all complete)
```

### 3. Execute with Checkpoints

After each phase:
```markdown
🛑 **Checkpoint: Phase [N] Complete**

Completed:
- [x] Task 1
- [x] Task 2

Next: Phase [N+1]

**Continue?**
```

### 4. Final Verification

```markdown
✅ **Orchestration Complete**

All phases:
- [x] Phase 1: Database
- [x] Phase 2: Backend
- [x] Phase 3: Frontend
- [x] Phase 4: Testing

Verification:
- [x] All tests pass
- [x] Integration verified
```

---

## When to Orchestrate

| Scenario | Action |
|----------|--------|
| Single domain | Direct to specialist |
| Multi-domain | Orchestrate |
| Full feature | Orchestrate |
