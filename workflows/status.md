---
description: Check project health and status
---

# /status - Project Health

$ARGUMENTS

---

## Purpose

Quick overview of project health and status.

---

## Protocol

### 1. Gather Metrics

**Code Quality:**
- Lint errors
- Type errors
- Test coverage

**Dependencies:**
- Outdated packages
- Security vulnerabilities

**Build:**
- Last build status
- Build time

---

## Status Report

```markdown
## Project Status: [Project Name]

### Code Quality
| Metric | Status |
|--------|--------|
| Lint | ✅ Clean |
| Types | ✅ No errors |
| Coverage | 85% |

### Dependencies
| Check | Status |
|-------|--------|
| Outdated | ⚠️ 3 packages |
| Vulnerable | ✅ None |

### Build
| Metric | Value |
|--------|-------|
| Last build | ✅ Passed |
| Duration | 2m 30s |

### Recommendations
1. Update outdated packages
2. Add tests for new features
```

---

## Commands Used

```bash
# Lint check
npm run lint

# Type check
npm run type-check

# Test coverage
npm run test -- --coverage

# Outdated packages
npm outdated

# Vulnerabilities
npm audit
```

---

## No Approval Required

Status check is read-only, no human approval needed.
