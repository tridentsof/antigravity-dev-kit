---
description: Code review with security checks
---

# /review - Code Review

$ARGUMENTS

---

## Purpose

Review code for quality, security, and best practices.

---

## Protocol

### 1. Identify Scope
- Which files to review?
- Focus areas (security, performance, etc.)?

### 2. Apply Reviewers
- `@security-auditor` for security
- Domain specialist for patterns

### 3. Review Checklist

**Code Quality:**
- [ ] Clean code principles
- [ ] No code smells
- [ ] Proper naming
- [ ] No duplication

**Security:**
- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] Proper auth checks
- [ ] No SQL injection

**Performance:**
- [ ] No N+1 queries
- [ ] Proper async usage
- [ ] No memory leaks

**Testing:**
- [ ] Tests exist
- [ ] Edge cases covered
- [ ] Tests pass

---

## Output Format

```markdown
## Code Review: [Scope]

### ✅ Passed
- Clean code standards
- Security checks

### ⚠️ Suggestions
- [Improvement 1]
- [Improvement 2]

### ❌ Issues (Must Fix)
- [Critical issue]

**Approve for deployment?**
```

---

## Human Approval

Review requires explicit approval before `/deploy`.

---

## After Review

```
Approved: /deploy
Issues: Fix and re-review
```
