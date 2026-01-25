---
name: english-education
description: English education content generation - lessons, quizzes, curriculum
---

# English Education Skill

> Generate educational content for English language learning.

---

## Content Types

| Type | Description | Template |
|------|-------------|----------|
| Lesson Plan | Structured lesson | lesson-templates.md |
| Quiz | Assessment questions | quiz-templates.md |
| Vocabulary | Word lists with context | inline |
| Grammar | Rule explanations | inline |

---

## Lesson Plan Structure

```markdown
# Lesson: [Title]

## Overview
- **Level:** [A1-C2 / Beginner-Advanced]
- **Duration:** [minutes]
- **Topic:** [theme]
- **Objectives:** [what students will learn]

## Warm-up (5 min)
[Engaging activity]

## Presentation (15 min)
[New content introduction]

## Practice (20 min)
[Guided exercises]

## Production (15 min)
[Free practice / application]

## Wrap-up (5 min)
[Summary and homework]

## Materials
- [List of needed materials]
```

---

## Quiz Structure

```markdown
# Quiz: [Title]

## Metadata
- **Level:** [A1-C2]
- **Topics:** [covered topics]
- **Time:** [minutes]

## Questions

### Multiple Choice
1. [Question]
   - a) [option]
   - b) [option]
   - c) [option] ✓
   - d) [option]

### Fill in the Blank
2. She ___ (go) to school every day.
   **Answer:** goes

### Matching
3. Match the words with definitions:
   | Word | Definition |
   |------|------------|
   | 1. happy | a. feeling joy |
```

---

## CEFR Levels

| Level | Description |
|-------|-------------|
| A1 | Beginner |
| A2 | Elementary |
| B1 | Intermediate |
| B2 | Upper Intermediate |
| C1 | Advanced |
| C2 | Proficient |

---

## Content Guidelines

| ✅ Do | ❌ Don't |
|-------|---------|
| Age-appropriate language | Complex jargon |
| Clear instructions | Ambiguous tasks |
| Varied question types | Single format only |
| Progressive difficulty | Random difficulty |
| Cultural sensitivity | Offensive content |

---

## References

- `references/lesson-templates.md` - Lesson plan templates
- `references/quiz-templates.md` - Quiz templates
- `scripts/curriculum_validator.py` - Content validation
