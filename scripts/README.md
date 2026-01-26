# Verification Scripts

Automated validation scripts used by agents to ensure code quality, security, and correctness.

---

## Agent → Script Mapping

| Agent | Script | Purpose |
|-------|--------|---------|
| `frontend-specialist` | `vitest_runner.py` | Run Vue3/TypeScript tests with Vitest |
| `backend-specialist` | `xunit_runner.py` | Run ASP.NET/C# tests with xUnit |
| `database-architect` | `schema_validator.py` | Validate SQL schemas and migrations |
| `security-auditor` | `security_scan.py` | Scan for security vulnerabilities |
| **Any agent** | `lint_runner.py` | Universal code quality checker |
| **Any agent** | `checklist.py` | Quick validation checklist |
| **Any agent** | `verify_all.py` | Comprehensive validation suite |

---

## Script Output Protocol

When agents use these scripts, they follow this protocol:

1. **Run script** - Execute the appropriate validation script
2. **Parse errors/warnings** - Extract and categorize issues
3. **Summarize to user** - Present findings in readable format
4. **Ask before fixing** - Request approval before making changes

---

## Individual Script Usage

### 🧪 `vitest_runner.py` - Frontend Test Runner

**Purpose**: Execute and validate Vue3/TypeScript tests using Vitest

**Usage**:
```bash
# Run tests
python scripts/vitest_runner.py .

# Run with coverage
python scripts/vitest_runner.py . --coverage

# Watch mode
python scripts/vitest_runner.py . --watch
```

**Requirements**: Node.js, Vitest installed in project

**Output**: Test results, pass/fail counts, coverage metrics

---

### 🧪 `xunit_runner.py` - Backend Test Runner

**Purpose**: Execute and validate ASP.NET/C# tests using xUnit

**Usage**:
```bash
# Run all tests
python scripts/xunit_runner.py .

# Run with coverage
python scripts/xunit_runner.py . --coverage

# Filter specific tests
python scripts/xunit_runner.py . --filter "UserServiceTests"
```

**Requirements**: .NET SDK, xUnit test projects

**Output**: Test results, pass/fail counts, duration

---

### 🗄️ `schema_validator.py` - Database Schema Validator

**Purpose**: Validate SQL Server schemas, migrations, and stored procedures

**Usage**:
```bash
# Validate schemas
python scripts/schema_validator.py .

# With connection string (for live validation)
python scripts/schema_validator.py . --connection-string "Server=..."
```

**Checks**:
- SQL syntax errors
- Missing primary keys
- Naming conventions
- Migration file naming
- SQL injection risks
- Transaction handling

**Output**: Schema quality report, syntax issues, recommendations

---

### 🔒 `security_scan.py` - Security Scanner

**Purpose**: Comprehensive security vulnerability detection

**Usage**:
```bash
# Full security scan
python scripts/security_scan.py .

# Filter by severity
python scripts/security_scan.py . --severity high
```

**Scans For**:
- Hardcoded secrets (passwords, API keys, tokens)
- npm package vulnerabilities
- NuGet package vulnerabilities
- SQL injection patterns
- XSS vulnerabilities
- Weak cryptography (MD5, SHA1)
- eval() usage
- HTTP vs HTTPS
- Missing security headers (HSTS, HTTPS redirect)

**Output**: Security findings grouped by severity (HIGH/MEDIUM/LOW)

---

### 🔍 `lint_runner.py` - Universal Linter

**Purpose**: Code quality and style validation for both frontend and backend

**Usage**:
```bash
# Lint entire project
python scripts/lint_runner.py .

# Auto-fix issues
python scripts/lint_runner.py . --fix

# Frontend only
python scripts/lint_runner.py . --frontend-only

# Backend only
python scripts/lint_runner.py . --backend-only
```

**Frontend Checks**:
- ESLint (JavaScript/TypeScript)
- Prettier (code formatting)
- TypeScript type checking

**Backend Checks**:
- dotnet format (C# formatting)
- dotnet build with warnings as errors

**Output**: Code quality report with pass/fail status

---

### ✅ `checklist.py` - Quick Validation

**Purpose**: Fast validation checklist for development and pre-commit

**Usage**:
```bash
# Run checklist
python scripts/checklist.py .

# With URL for integration tests
python scripts/checklist.py . --url http://localhost:3000
```

**Checks**:
- Security (secrets, vulnerabilities)
- Frontend lint
- Frontend types
- Frontend tests
- Backend build
- Backend tests

**Output**: Pass/fail summary for each check

---

### 🎯 `verify_all.py` - Comprehensive Validation

**Purpose**: Complete validation suite before deployment

**Usage**:
```bash
# Full verification
python scripts/verify_all.py .

# With application URL
python scripts/verify_all.py . --url http://localhost:3000
```

**Runs All Checks**:
- All checklist items
- Additional deployment validations
- Integration tests (if URL provided)

**Output**: Comprehensive validation report

---

## When to Use Each Script

| Scenario | Script | Why |
|----------|--------|-----|
| Writing Vue components | `vitest_runner.py` | Validate component tests |
| Writing API endpoints | `xunit_runner.py` | Validate backend tests |
| Creating migrations | `schema_validator.py` | Ensure schema quality |
| Before commit | `checklist.py` | Quick validation |
| Before PR | `lint_runner.py` | Code quality check |
| Security review | `security_scan.py` | Find vulnerabilities |
| Before deployment | `verify_all.py` | Complete validation |

---

## Exit Codes

All scripts follow standard exit code conventions:

- **0** - Success (all checks passed)
- **1** - Failure (issues found)

This allows scripts to be used in CI/CD pipelines:

```bash
python scripts/checklist.py . && echo "Ready to commit" || echo "Fix issues first"
```

---

## Integration with Agents

Agents automatically use these scripts when appropriate:

```
User: "Test my Vue components"
  ↓
@test-engineer activates
  ↓
Runs: python scripts/vitest_runner.py .
  ↓
Parses output and reports to user
  ↓
Asks: "Found 2 failing tests. Should I help fix them?"
```

---

## Requirements

### Python
- Python 3.7+
- No external dependencies (uses stdlib only)

### Project Dependencies
- **Frontend**: Node.js, npm, Vitest (for vitest_runner.py)
- **Backend**: .NET SDK (for xunit_runner.py)
- **Database**: SQL files in project (for schema_validator.py)

---

## Adding Custom Validations

To add project-specific validations:

1. Create a new script following the same pattern
2. Add to the agent's skill or workflow
3. Update this README with usage instructions

**Example**:
```python
#!/usr/bin/env python3
"""
Custom Validator - Your specific validation
"""

def main():
    # Your validation logic
    pass

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

### "Command not found"
- Ensure required tools are installed (npm, dotnet, etc.)
- Check PATH environment variable

### "Permission denied"
- Make scripts executable: `chmod +x scripts/*.py`

### "Timeout"
- Scripts timeout after 5 minutes
- For large projects, consider running specific checks

---

## Contributing

When modifying scripts:

1. Keep exit codes consistent (0 = success, 1 = failure)
2. Follow the output protocol (run → parse → summarize → ask)
3. Add timeout handling for long-running commands
4. Update this README with changes
