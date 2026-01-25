---
description: Deploy to Azure DevOps with approval
---

# /deploy - Deployment

$ARGUMENTS

---

## Purpose

Trigger Azure DevOps deployment with human approval.

---

## Pre-Deployment Checklist

```markdown
## Deployment Checklist

### Code Quality
- [ ] All tests pass
- [ ] Code review approved
- [ ] No lint errors

### Security
- [ ] Security scan passed
- [ ] No exposed secrets
- [ ] Dependencies updated

### Documentation
- [ ] README updated
- [ ] API docs current
- [ ] Changelog updated
```

---

## Protocol

### 1. Verify Prerequisites
- Tests passing?
- Review approved?
- Branch up to date?

### 2. Select Environment

| Environment | Approval |
|-------------|----------|
| Dev | Auto |
| Staging | Auto |
| Production | **Required** |

### 3. Human Approval (Production)

```markdown
🚀 **Ready to deploy to PRODUCTION**

Changes:
- [List of changes]

Pre-flight:
- [x] Tests pass
- [x] Review approved
- [x] Security scan clean

**Approve deployment?**
```

### 4. Trigger Pipeline

```bash
# Azure DevOps CLI
az pipelines run --name "Deploy-Pipeline" --branch main
```

---

## Post-Deployment

```markdown
✅ **Deployed to [Environment]**

Pipeline: [link]
Status: Success

Verification:
- [ ] Health check passed
- [ ] Smoke tests passed
- [ ] Monitoring active
```

---

## Rollback

If issues detected:
```
az pipelines run --name "Rollback-Pipeline"
```
