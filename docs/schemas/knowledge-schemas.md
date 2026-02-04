# Knowledge Document Schemas

Canonical YAML frontmatter specifications for all MESO knowledge document types.
These schemas define the structured metadata that makes documents human-useful now
and machine-indexable for future RAG.

**Author:** Rowan Valle — Symbiont Systems LLC

---

## Common Fields

All knowledge documents require at minimum:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | yes | One of: `aar`, `decision`, `research`, `pattern` |
| `title` | string | yes | Human-readable title |
| `date` | date | yes | ISO 8601 (YYYY-MM-DD) |
| `domain` | string[] | yes | Domain tags: `web`, `gis`, `meso`, `business`, `ops`, `game`, `security` |
| `tags` | string[] | no | Free-form tags for indexing |

---

## AAR (After Action Report)

Filed to: `docs/knowledge/aars/YYYY-MM-DD-title.md`

```yaml
---
type: aar
title: "Brief descriptive title"
date: 2026-02-04
project: project-slug
domain: [web, gis, meso]
severity: minor | moderate | significant
scope: "One-line description of what was attempted"
tags: [tag1, tag2]
related-files:
  - path/to/file.md
supersedes:                          # optional: prior AAR this replaces
---
```

### AAR-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project` | string | yes | Project slug |
| `severity` | string | yes | `minor` / `moderate` / `significant` |
| `scope` | string | yes | What was attempted |
| `related-files` | string[] | no | Files involved |
| `supersedes` | string | no | Path to prior AAR this replaces |

### Severity Definitions

- **minor** — lessons learned, no rework required
- **moderate** — rework needed, no data loss or security impact
- **significant** — data loss, security issue, major rework, or systemic failure

### Body Structure

```
## AAR: [Title]
### What Happened
### What Went Well
### What Went Wrong
### Root Causes
### Lessons Learned
### Action Items
### Metrics
```

---

## Decision Log

Filed to: `docs/knowledge/decisions/YYYY-MM-DD-title.md`

```yaml
---
type: decision
title: "Short decision title"
date: 2026-02-04
project: project-slug
domain: [architecture, security]
status: proposed | accepted | deprecated | superseded
deciders: [valis]
tags: [tag1]
supersedes:                          # optional: prior decision this replaces
superseded-by:                       # optional: decision that replaced this one
related-files:
  - path/to/affected/file.md
---
```

### Decision-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project` | string | yes | Project slug |
| `status` | string | yes | `proposed` / `accepted` / `deprecated` / `superseded` |
| `deciders` | string[] | yes | Who made the decision |
| `supersedes` | string | no | Path to prior decision |
| `superseded-by` | string | no | Path to replacement decision |
| `related-files` | string[] | no | Files affected by this decision |

### Body Structure

```
## Context
## Decision
## Alternatives Considered
### Alternative A: [name]
### Alternative B: [name]
## Rationale
## Consequences
## Review Date
```

---

## Research Doc

Filed to: `docs/research-topic.md` (project docs root)

```yaml
---
type: research
title: "Research topic"
date: 2026-02-04
updated: 2026-02-04
project: project-slug
domain: [web, market]
status: draft | active | stale | archived
confidence: low | medium | high
sources:
  - url: "https://example.com"
    title: "Source title"
    accessed: 2026-02-04
tags: [tag1]
---
```

### Research-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project` | string | yes | Project slug |
| `updated` | date | yes | Last update date |
| `status` | string | yes | `draft` / `active` / `stale` / `archived` |
| `confidence` | string | yes | `low` / `medium` / `high` |
| `sources` | object[] | yes | At least one source with url, title, accessed |

### Status Definitions

- **draft** — research in progress, findings are preliminary
- **active** — research complete, findings are current
- **stale** — 90+ days without update, may contain outdated information
- **archived** — superseded or no longer relevant, kept for reference

### Body Structure

```
## Summary
## Findings
## Open Questions
## Sources
```

---

## Pattern / Recipe

Filed to: `docs/knowledge/patterns/descriptive-name.md`

```yaml
---
type: pattern
title: "Pattern name"
date: 2026-02-04
updated: 2026-02-04
domain: [orchestration, recovery]
applicability: universal | domain-specific
tags: [tag1]
derived-from:                        # optional: AARs or decisions that spawned this
  - aars/2026-02-03-title.md
prerequisites:                       # optional: conditions for applicability
  - "Tasks are independent with no shared file writes"
---
```

### Pattern-Specific Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `updated` | date | yes | Last update date |
| `applicability` | string | yes | `universal` / `domain-specific` |
| `derived-from` | string[] | no | Source AARs or decisions |
| `prerequisites` | string[] | no | Conditions that must be true |

### Body Structure

```
## Problem
## Solution
## Example
## Anti-Patterns
## When NOT to Use
```

---

## Filing Conventions

- **Dated documents** (AARs, decisions): `YYYY-MM-DD-kebab-case-title.md`
- **Named documents** (patterns, research): `descriptive-name.md`
- Every `docs/knowledge/` directory must have an `INDEX.md`
- Update the index when adding or archiving documents

---

*By Rowan Valle — Symbiont Systems LLC*
*Built with Claude Code*
