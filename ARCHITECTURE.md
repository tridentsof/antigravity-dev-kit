# Antigravity Kit Architecture

> Vue3 + ASP.NET + Azure Development Toolkit

---

## Overview

| Metric | Value |
|--------|-------|
| Agents | 12 |
| Skills | 20 |
| Workflows | 10 |
| Scripts | 2 master + skill-level |

---

## Directory Structure

```
.agent-antigravity/
├── ARCHITECTURE.md     # This file
├── README.md           # Usage guide
├── rules/GEMINI.md     # Global rules
├── agents/             # 12 Specialist Agents
├── skills/             # 20 Skill Modules
├── workflows/          # 10 Slash Commands
└── scripts/            # Validation Scripts
```

---

## Agents (12)

| Agent | Focus | Skills |
|-------|-------|--------|
| orchestrator | Multi-agent coordination | intelligent-routing, brainstorming |
| project-planner | Discovery, planning | brainstorming, plan-writing, architecture |
| frontend-specialist | Vue3, TypeScript, Pinia | vue3-patterns, vitest-testing |
| backend-specialist | ASP.NET Core, C# | aspnet-patterns, csharp-patterns, api-patterns |
| database-architect | SQL Server | sqlserver-design |
| devops-engineer | Azure DevOps, AKS, GitOps | azure-devops, azure-aks, gitops-patterns |
| security-auditor | KeyVault, OWASP | vulnerability-scanner, azure-keyvault |
| test-engineer | xUnit, Vitest, E2E | xunit-testing, vitest-testing |
| debugger | Root cause analysis | systematic-debugging |
| performance-optimizer | Grafana, metrics | grafana-logging |
| documentation-writer | API docs | documentation-templates |
| explorer-agent | Codebase analysis | - |

---

## Skills (20)

### Frontend & Vue3
| Skill | Description |
|-------|-------------|
| vue3-patterns | Composition API, Pinia, Vue Router |
| vitest-testing | Vue component testing |

### Backend & ASP.NET
| Skill | Description |
|-------|-------------|
| aspnet-patterns | Controllers, Services, Middleware |
| csharp-patterns | C# best practices, async/await |
| api-patterns | REST API design |

### Database
| Skill | Description |
|-------|-------------|
| sqlserver-design | Schema, stored procedures, optimization |

### Azure & DevOps
| Skill | Description |
|-------|-------------|
| azure-devops | CI/CD pipelines, YAML |
| azure-aks | Kubernetes, Helm charts |
| azure-keyvault | Secrets management |
| grafana-logging | Metrics, dashboards |
| gitops-patterns | ArgoCD, Flux |

### Testing
| Skill | Description |
|-------|-------------|
| xunit-testing | C# unit tests |
| testing-patterns | Test strategies |

### Core
| Skill | Description |
|-------|-------------|
| clean-code | Coding standards |
| architecture | System design patterns |
| brainstorming | Socratic discovery |
| plan-writing | Task breakdown |
| intelligent-routing | Agent selection |
| vulnerability-scanner | Security auditing |

### Industry
| Skill | Description |
|-------|-------------|
| english-education | Curriculum, lessons, quizzes |

---

## Workflows (10)

| Command | Description |
|---------|-------------|
| /brainstorm | Socratic discovery |
| /plan | Create PLAN-{slug}.md |
| /create | Full feature build |
| /code | Code generation |
| /test | Generate tests |
| /debug | Root cause analysis |
| /review | Code review |
| /deploy | Azure DevOps trigger |
| /status | Project health |
| /orchestrate | Multi-agent coordination |

---

## Skill Loading Protocol

```
User Request → Agent Selected → Load SKILL.md → Read references/
```

### Skill Structure
```
skill-name/
├── SKILL.md       # Required - metadata & rules
├── references/    # Optional - templates, docs
└── scripts/       # Optional - validation scripts
```

---

## Quick Reference

| Need | Agent | Skills |
|------|-------|--------|
| Vue3 Component | frontend-specialist | vue3-patterns |
| ASP.NET API | backend-specialist | aspnet-patterns, api-patterns |
| SQL Schema | database-architect | sqlserver-design |
| Deploy to AKS | devops-engineer | azure-aks, gitops-patterns |
| Security Audit | security-auditor | vulnerability-scanner |
| Tests | test-engineer | xunit-testing, vitest-testing |
| Debug | debugger | systematic-debugging |
| Plan | project-planner | brainstorming, plan-writing |
