---
description: Generate tests for existing code
---

# /test - Test Generation

$ARGUMENTS

---

## Purpose

Generate unit and integration tests for specified code.

---

## Protocol

### 1. Analyze Target
- What code needs testing?
- Frontend (Vitest) or Backend (xUnit)?
- Unit or integration tests?

### 2. Apply Testing Agent
Route to `@test-engineer` with appropriate skills.

### 3. Generate Tests

**Frontend (Vitest):**
```typescript
describe('ComponentName', () => {
  it('should render', () => {
    // Arrange, Act, Assert
  })
})
```

**Backend (xUnit):**
```csharp
[Fact]
public void Method_Scenario_Expected()
{
    // Arrange, Act, Assert
}
```

### 4. Run Tests

```bash
# Frontend
npm run test

# Backend
dotnet test
```

---

## Test Coverage

| Target | Minimum |
|--------|---------|
| Business logic | 90% |
| API endpoints | 80% |
| Components | 70% |

---

## Output

```markdown
✅ **Tests generated**

Files:
- `tests/UserService.test.ts`
- `tests/UserController.Tests.cs`

Results:
- 10 tests passed
- Coverage: 85%
```

---

## After Testing

```
Next: `/review` for code review
```
