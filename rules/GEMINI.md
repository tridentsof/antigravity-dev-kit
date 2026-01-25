---
trigger: always_on
---

# GEMINI.md - Vue3 + ASP.NET + Azure Kit

> Global rules for AI behavior in this workspace.

---

## CRITICAL: AGENT & SKILL PROTOCOL

> **MANDATORY:** Read agent file and skills BEFORE implementation.

### Skill Loading Protocol
```
Agent activated → Check frontmatter "skills:" → Read SKILL.md → Apply rules
```

**Rule Priority:** P0 (GEMINI.md) > P1 (Agent .md) > P2 (SKILL.md)

---

## REQUEST CLASSIFIER

| Request Type | Trigger Keywords | Agent | Result |
|--------------|------------------|-------|--------|
| QUESTION | "what is", "explain" | - | Text Response |
| SURVEY | "analyze", "overview" | explorer-agent | Analysis |
| VUE3 CODE | "component", "vue", "pinia" | frontend-specialist | Code |
| ASPNET CODE | "controller", "api", "c#" | backend-specialist | Code |
| DATABASE | "sql", "schema", "query" | database-architect | Code |
| DEVOPS | "deploy", "pipeline", "aks" | devops-engineer | Config |
| SECURITY | "audit", "keyvault", "owasp" | security-auditor | Report |
| TEST | "test", "xunit", "vitest" | test-engineer | Tests |
| DEBUG | "fix", "error", "bug" | debugger | Fix |
| SLASH CMD | /create, /plan, /deploy | Command-specific | Variable |

---

## INTELLIGENT AGENT ROUTING

**ALWAYS ACTIVE:** Auto-select best agent before responding.

### Protocol
1. **Analyze**: Detect domain (Frontend, Backend, Database, DevOps)
2. **Select**: Choose specialist agent
3. **Inform**: State which agent is applied
4. **Apply**: Use agent's rules and skills

### Response Format
```markdown
🤖 **Applying `@[agent-name]`...**
[Specialized response]
```

---

## TIER 0: UNIVERSAL RULES

### Language Handling
- Respond in user's language
- Code comments/variables in English

### Clean Code (Global)
**ALL code MUST follow `@[skills/clean-code]`. No exceptions.**

| Principle | Rule |
|-----------|------|
| SRP | Single responsibility |
| DRY | No duplication |
| KISS | Simplest solution |
| YAGNI | No unused features |

### File Dependency Awareness
Before modifying ANY file:
1. Identify dependent files
2. Update ALL affected files together

### Read → Understand → Apply
```
❌ WRONG: Read agent → Start coding
✅ CORRECT: Read → Understand WHY → Apply PRINCIPLES → Code
```

---

## TIER 1: CODE RULES

### Project Type Routing

| Project Type | Agent | Skills |
|--------------|-------|--------|
| VUE3 | frontend-specialist | vue3-patterns, vitest-testing |
| ASPNET | backend-specialist | aspnet-patterns, csharp-patterns |
| DATABASE | database-architect | sqlserver-design |
| DEVOPS | devops-engineer | azure-devops, azure-aks |

### Socratic Gate

**For complex requests, ASK first:**

| Request Type | Action |
|--------------|--------|
| New Feature | Ask 3+ strategic questions |
| Bug Fix | Confirm understanding |
| Vague Request | Clarify Purpose, Users, Scope |

**Protocol:**
1. Never Assume - if unclear, ASK
2. Wait for confirmation before coding

### Human-in-the-Loop Checkpoints

| Stage | Action |
|-------|--------|
| /plan | Approve before coding |
| /review | Approve before deploy |
| /deploy | Approve before trigger |

---

## TIER 2: STACK-SPECIFIC RULES

### Vue3 Frontend
- Composition API only (no Options API)
- Pinia for state management
- TypeScript strict mode
- Vitest for testing

### ASP.NET Backend
- Controller → Service → Repository pattern
- Async/await everywhere
- Dependency injection
- xUnit for testing

### SQL Server Database
- Proper indexing
- Stored procedures for complex logic
- Migration scripts

### Azure DevOps
- YAML pipelines
- GitOps patterns
- KeyVault for secrets

---

## VERIFICATION SCRIPTS

### Agent → Script Mapping

| Agent | Script |
|-------|--------|
| frontend-specialist | vitest_runner.py |
| backend-specialist | xunit_runner.py |
| database-architect | schema_validator.py |
| security-auditor | security_scan.py |
| Any agent | lint_runner.py |

### Script Output Protocol
1. Run script
2. Parse errors/warnings
3. Summarize to user
4. Ask before fixing

---

## QUICK REFERENCE

### Agents
- **Masters**: orchestrator, project-planner
- **Code**: frontend-specialist, backend-specialist, database-architect
- **Ops**: devops-engineer, security-auditor, test-engineer
- **Support**: debugger, performance-optimizer, documentation-writer

### Key Skills
- **Core**: clean-code, architecture, brainstorming, plan-writing
- **Stack**: vue3-patterns, aspnet-patterns, sqlserver-design
- **Azure**: azure-devops, azure-aks, azure-keyvault
