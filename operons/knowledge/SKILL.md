---
name: knowledge
description: >
  This skill should be used when capturing knowledge, writing documentation,
  creating decision logs, writing AARs, recording research findings, extracting
  reusable patterns, filing knowledge documents, maintaining knowledge indexes,
  or preparing documents for RAG indexing.
  MESO operon (Rhopalia — Sensory Memory).
---

# Knowledge — Rhopalia (Sensory Memory)

Structured capture of what the colony learns. Every document must be
human-useful NOW and machine-indexable LATER.

## Document Types

| Type | When | Where | Naming |
|------|------|-------|--------|
| AAR | After significant sessions or incidents | `docs/knowledge/aars/` | `YYYY-MM-DD-title.md` |
| Decision | Architectural or technical choices | `docs/knowledge/decisions/` | `YYYY-MM-DD-title.md` |
| Research | Investigative findings | `docs/` (project root) | `descriptive-name.md` |
| Pattern | Reusable solution from experience | `docs/knowledge/patterns/` | `descriptive-name.md` |

## Frontmatter Rules

Every knowledge document MUST have YAML frontmatter with at minimum:
- `type`: one of `aar`, `decision`, `research`, `pattern`
- `title`: human-readable title
- `date`: ISO 8601 date
- `domain`: array of domain tags

Full schemas: `docs/schemas/knowledge-schemas.md` in techbiont-framework
or genome Part XI.

## Filing Convention

- Create `docs/knowledge/` and subdirectories on first use, not preemptively
- Every knowledge directory MUST have an `INDEX.md` listing contents
- Update the index when adding or archiving documents
- Use templates from `techbiont-framework/templates/knowledge/`

## Quality Criteria

### Good AAR
- Factual "What Happened" (no interpretation mixed in)
- Root causes identified, not just symptoms
- Actionable items with specific next steps
- Metrics quantified where possible

### Bad AAR
- "We should do better next time" (vague, no action)
- Skipping root causes (jumping straight to solutions)
- No metrics (how bad was it? unmeasured)

### Good Decision Log
- Records what was NOT chosen and why
- Includes the context that made this decision right NOW
- Has a review date for decisions that might age poorly
- Consequences section is honest about tradeoffs

### Bad Decision Log
- Only records what was chosen (no alternatives = no learning)
- Missing context (incomprehensible in 3 months)
- No consequences section (pretends there are no tradeoffs)

### Good Pattern
- Includes "When NOT to Use" (prevents over-application)
- Has a concrete example from real work
- Derived from experience (cites the AAR or session)
- Prerequisites stated explicitly

### Good Research Doc
- Sources with access dates (web content moves)
- Confidence level stated explicitly
- Status kept current (draft/active/stale/archived)
- Findings section leads with the key insight, not background

## RAG-Readiness Guidelines

For future indexing, write documents that are easy to retrieve:
- Use consistent terminology across documents
- Tags should use the same vocabulary as domain tags elsewhere
- Cross-reference related documents using relative paths
- Keep documents atomic: one decision per file, one pattern per file
- Put the core insight in the first paragraph, not buried in subsections
- Avoid ambiguous pronouns — name things explicitly

## Integration With Other Operons

| Operon | Integration |
|--------|-------------|
| **Evolution** | AARs are the primary input. When a lesson recurs 3+ times, extract a pattern. |
| **Auditing** | Session audit checks: were significant decisions logged? |
| **Scratchpad** | Drafts can stage in scratchpad before finalizing. |
| **Communication** | Research persistence rule: extensive research goes to docs/, not temp files. |
