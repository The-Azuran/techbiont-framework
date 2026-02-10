# RAG-Based Session Continuity Protocol

**Status**: Active (Phase 2)
**Replaces**: Manual handoff.md files
**Date**: 2026-02-09

---

## Overview

MESO v2 uses RAG (Retrieval-Augmented Generation) for session continuity instead of manual handoff notes. The RAG MCP provides semantic search over indexed knowledge, enabling natural session resumption.

**Philosophy**: Knowledge persists in searchable collections, not linear handoff documents.

---

## RAG Collections

### knowledge_base
**Purpose**: STANDING-ORDERS.md, domain docs, research, operational knowledge
**Current**: 32 chunks indexed
**Use for**:
- General MESO knowledge
- Technical documentation
- Research findings
- Operational procedures

**Example searches**:
```
"git commit workflows"
"MESO v2 architecture"
"orchestration patterns"
```

### aar_archive
**Purpose**: After Action Reports and lessons learned
**Current**: 10 chunks indexed
**Metadata**: date, severity, domain
**Use for**:
- Learning from past sessions
- Understanding what worked/failed
- Finding high-severity lessons

**Example searches**:
```
severity="high" query="radical simplification"
domain="meso" query="validation gates"
query="lessons learned planning"
```

### decisions
**Purpose**: Decision docs with YAML frontmatter
**Current**: 0 chunks (not yet used)
**Metadata**: date, domain, status
**Use for**:
- Recording architectural decisions
- Tracking decision outcomes
- Understanding why choices were made

---

## Session Start Protocol

Instead of reading handoff.md, start sessions with RAG queries:

### 1. Check Recent Work
```
Search aar_archive for recent lessons (last 7 days)
Search knowledge_base for "in progress" or "pending"
```

### 2. Understand Context
```
Search knowledge_base for current project/topic
Search decisions for related architectural choices
```

### 3. Resume Tasks
Use TaskList tool to see pending work (tasks persist across sessions)

---

## Session End Protocol

### 1. Index Session Summary
If session produced significant work or lessons:

```bash
# Create summary document
cat > /tmp/session-summary.md <<EOF
# Session: [Brief Description]
**Date**: $(date +%Y-%m-%d)
**Topic**: [Main topic]
**Outcome**: [What was accomplished]

## Key Points
- [Point 1]
- [Point 2]

## Decisions Made
- [Decision 1]
- [Decision 2]

## Next Steps
- [Step 1]
- [Step 2]
EOF

# Index to knowledge_base
mcp__rag__index_document \
  file_path="/tmp/session-summary.md" \
  collection="knowledge_base" \
  doc_type="session_summary" \
  metadata='{"date": "2026-02-09", "domain": "meso"}'
```

### 2. Write AAR (If Needed)
For sessions with significant lessons learned, create AAR and index to aar_archive:

```bash
# Create AAR (use AAR template from genome)
# Index to aar_archive
mcp__rag__index_document \
  file_path="/path/to/aar.md" \
  collection="aar_archive" \
  doc_type="aar" \
  metadata='{"date": "2026-02-09", "severity": "high", "domain": "meso"}'
```

### 3. Record Decisions
For architectural or strategic decisions:

```bash
# Create decision doc with YAML frontmatter
cat > decision-001.md <<EOF
---
date: 2026-02-09
domain: meso
status: accepted
---

# Decision: [Title]

## Context
[Why this decision was needed]

## Options Considered
1. [Option 1]
2. [Option 2]

## Decision
[What was decided]

## Rationale
[Why this was chosen]

## Consequences
[Implications of this decision]
EOF

# Index to decisions collection
mcp__rag__index_document \
  file_path="decision-001.md" \
  collection="decisions" \
  doc_type="decision" \
  metadata='{"date": "2026-02-09", "domain": "meso", "status": "accepted"}'
```

---

## Searching the RAG

### Basic Search
```
mcp__rag__semantic_search \
  query="your search query" \
  collection="knowledge_base" \
  top_k=5
```

### Filtered Search (AAR)
```
mcp__rag__semantic_search \
  query="lessons about planning" \
  collection="aar_archive" \
  severity="high" \
  top_k=5
```

### List Indexed Documents
```
mcp__rag__list_documents \
  collection="knowledge_base"
```

### List All Collections
```
mcp__rag__list_collections
```

---

## When to Use Manual Handoffs

RAG is for **knowledge** that should persist long-term. Use manual handoff notes for:

- **Ephemeral context**: Temporary state that won't matter in a week
- **Work-in-progress**: Unfinished tasks (use TaskList instead if possible)
- **Session-specific details**: Won't be useful to search for later

**Rule of thumb**: If you'd want to search for it later, index it to RAG. If it's only useful for the next session, use handoff note.

---

## Migration from Old Handoffs

Existing handoff files in `/home/Valis/.claude/handoff/` are preserved as historical record. They document Phase 1 validation and early MESO v2 work.

**Action**: Review old handoffs for knowledge worth indexing to RAG, then leave them as archive.

---

## Advantages Over Manual Handoffs

| Manual Handoff | RAG-Based |
|----------------|-----------|
| Linear (hard to find old info) | Semantic search (find by meaning) |
| One file per session (fragmented) | All knowledge in queryable collections |
| Manual reading on resume | Query for exactly what you need |
| No metadata/filtering | Filter by date, severity, domain, etc. |
| Grows indefinitely | Automatically deduplicated chunks |

---

## Best Practices

### DO
- Index significant session outcomes to knowledge_base
- Write AARs for lessons learned (index to aar_archive)
- Record decisions with context (index to decisions)
- Search RAG at session start to restore context
- Use semantic queries (describe what you're looking for)

### DON'T
- Index trivial session notes (noise in search results)
- Duplicate information already in genome/zooids
- Index ephemeral state (use TaskList or scratchpad)
- Rely only on RAG (still use TaskList for active work)
- Forget to add metadata (makes filtering impossible)

---

## Implementation Status

**Phase 2**: ✅ ACTIVE (2026-02-09)
- RAG MCP validated and operational
- Backend: Qdrant (localhost:6333) running
- Embedding model: Ollama (localhost:11435) running
- 3 collections defined and indexed
- Semantic search proven in production use

**Validation**: Exceeded 3+ uses requirement (Phase 2 gate passed)

---

## Tools Reference

| Tool | Purpose |
|------|---------|
| `mcp__rag__semantic_search` | Search collections by meaning |
| `mcp__rag__index_document` | Add document to collection |
| `mcp__rag__list_collections` | Show all collections with stats |
| `mcp__rag__list_documents` | Show indexed docs in collection |

---

**Authored by**: Rowan Valle
**Executed by**: Claude Code (Sonnet 4.5)
**Status**: Production protocol for MESO v2 Phase 2
