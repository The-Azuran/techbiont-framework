---
name: retrieval
description: >
  This skill should be used when searching the knowledge base, finding past
  decisions, retrieving relevant context, searching for patterns or solutions,
  finding similar documents, querying workspace artifacts, or performing
  semantic search across MESO's memory.
  MESO operon (Neurozooid — Sensory Integration & Retrieval).
---

# Retrieval — Neurozooid (Sensory Integration & Retrieval)

Semantic search and knowledge retrieval across MESO's memory using local-first
RAG (Ollama embeddings + Qdrant vector store).

## Problem

MESO accumulates knowledge (AARs, decisions, research, patterns) but lacks
semantic search. Manual navigation through directories and keyword search
(SQLite FTS) miss conceptually related content.

**Example**: Searching "docker compose pattern" should find documents about
"container orchestration templates" even without exact keyword matches.

## Principles

1. **Local-first**: All retrieval runs on-device (no cloud APIs)
2. **Semantic search**: Find documents by meaning, not just keywords
3. **Metadata-aware**: Filter by type, domain, tags, severity, dates
4. **Hybrid approach**: Combine semantic (concepts) + keyword (exact matches)
5. **Cross-collection**: Search both knowledge base and workspace artifacts
6. **Non-destructive**: Never modify source documents during retrieval

## Architecture

```
Query
  ↓
Embedding (Ollama nomic-embed-text 768-dim)
  ↓
Vector Search (Qdrant cosine similarity)
  ↓
Metadata Filtering (type, domain, tags, dates)
  ↓
Ranking (relevance score 0-1)
  ↓
Top-K Results
```

**Collections**:
- `knowledge_base`: docs/knowledge/ (~200 chunks from 40+ docs)
- `workspace_artifacts`: ~/.claude/workspace/artifacts/ (~100 chunks from 20+ artifacts)

**Index location**: `/home/Valis/code/github.com/the-azuran/unified-ai/data/qdrant_db/`

## Commands

### Search Knowledge Base

```bash
# Basic semantic search
/retrieval search "docker compose pattern for FastAPI"

# With metadata filters
/retrieval search "authentication patterns" --type decision --domain web

# Date-based filtering (Phase 3)
/retrieval search "context window" --type aar --after 2026-01-01

# Tag filtering
/retrieval search "RAG integration" --tags rag,retrieval

# Search workspace artifacts
/retrieval search "database migration script" --collection workspace

# Cross-collection search (default)
/retrieval search "API endpoint design"
```

**Filters**:
- `--type`: Document type (`aar`, `decision`, `research`, `pattern`)
- `--domain`: Domain tags (comma-separated)
- `--tags`: Tags (comma-separated)
- `--severity`: AAR severity (`minor`, `moderate`, `significant`)
- `--after`: Minimum date (ISO 8601: `2026-01-01`)
- `--before`: Maximum date (ISO 8601: `2026-12-31`)
- `--collection`: Collection name (`knowledge_base`, `workspace_artifacts`, or `all`)
- `--top-k`: Number of results (default: 5)

**Output**:
```
Found 3 results:

1. Score: 0.701
   File: docs/knowledge/aars/2026-02-06-rag-capability-analysis.md
   Type: aar
   Heading: Root Causes
   Preview: RAG readiness is high — 80% of infrastructure exists...

2. Score: 0.613
   File: docs/knowledge/decisions/2026-02-04-knowledge-document-format.md
   Type: decision
   Heading: Decision
   Preview: Use YAML frontmatter for structured metadata...

3. Score: 0.587
   File: ~/.claude/workspace/artifacts/fastapi-template.py
   Type: code
   Tags: template, api, python
   Preview: from fastapi import FastAPI, HTTPException...
```

### Find Similar Documents

```bash
# Find documents similar to a specific file
/retrieval similar docs/knowledge/aars/2026-02-06-rag-capability-analysis.md

# With filters
/retrieval similar docs/knowledge/decisions/2026-02-04-example.md --type decision
```

**Use cases**:
- Find related AARs when writing a new one
- Discover similar decisions before making a new one
- Find patterns that apply to current problem

### Index New Documents

```bash
# Index entire knowledge base
/retrieval index docs/knowledge/

# Index specific directory
/retrieval index docs/knowledge/aars/

# Index single document
/retrieval index docs/knowledge/aars/2026-02-06-example.md

# Index workspace artifacts
/retrieval index ~/.claude/workspace/artifacts/

# Re-index everything (if schema changes)
/retrieval index --all
```

**When to index**:
- After filing a new knowledge document
- After workspace artifact promotion
- After bulk document updates
- If search results seem stale

**Automatic indexing** (Phase 4):
File watcher on `docs/knowledge/` auto-triggers indexing on file creation/modification.

### Check Index Status

```bash
/retrieval status

# Output:
Collections:
  knowledge_base: 203 chunks, 42 documents
  workspace_artifacts: 89 chunks, 18 artifacts
Last indexed: 2026-02-06 14:32
Qdrant location: /home/Valis/code/github.com/the-azuran/unified-ai/data/qdrant_db/
Embedding model: nomic-embed-text (768-dim)
```

## Search Workflows

### Workflow 1: Find Past Solution

**Scenario**: Encountered a problem, want to know if we've solved it before.

```bash
# Search for the problem/solution
/retrieval search "docker compose healthcheck configuration"

# Review results, open most relevant
vim docs/knowledge/patterns/docker-healthcheck-pattern.md

# If found, adapt solution
# If not found, solve and document as new pattern
```

### Workflow 2: Pre-Decision Research

**Scenario**: About to make architectural decision, check what we've decided before.

```bash
# Search for related decisions
/retrieval search "vector database selection" --type decision

# Find similar past decisions
/retrieval similar docs/knowledge/decisions/2026-02-06-chromadb-vs-qdrant.md

# Review alternatives and consequences
# Make informed decision incorporating past learnings
```

### Workflow 3: AAR Cross-Reference

**Scenario**: Writing AAR, want to link to related incidents.

```bash
# Search for similar issues
/retrieval search "context window overflow" --type aar --severity significant

# Add related-files to frontmatter
related-files:
  - docs/knowledge/aars/2026-01-15-context-management.md
  - docs/knowledge/aars/2025-12-10-token-limit-exceeded.md
```

### Workflow 4: Workspace Artifact Discovery

**Scenario**: Need a code template or past implementation.

```bash
# Search workspace artifacts
/retrieval search "FastAPI CRUD endpoint" --collection workspace

# Found: ~/.claude/workspace/artifacts/fastapi-crud-template.py
# Promote to project if useful
```

## Indexing Workflows

### Workflow 1: File New Document

**Scenario**: Just filed an AAR using knowledge operon.

```bash
# 1. File the AAR
/knowledge file aar

# 2. Update INDEX.md (knowledge operon does this)

# 3. Index the new document
/retrieval index docs/knowledge/aars/2026-02-06-example-aar.md
```

**Future** (Phase 4 auto-indexing): Steps 2-3 happen automatically via file watcher.

### Workflow 2: Bulk Re-Index

**Scenario**: Changed frontmatter schema or added many documents at once.

```bash
# Re-index entire knowledge base
/retrieval index docs/knowledge/ --force

# Verify indexing
/retrieval status

# Test search
/retrieval search "test query"
```

### Workflow 3: Cross-Collection Update

**Scenario**: Promoted workspace artifacts, need to index both collections.

```bash
# Index workspace
/retrieval index ~/.claude/workspace/artifacts/

# Index knowledge base
/retrieval index docs/knowledge/

# Verify both collections
/retrieval status
```

## Integration With Other Operons

| Operon | Integration | When |
|--------|-------------|------|
| **Knowledge** | Auto-index filed documents | After filing AAR/decision/pattern |
| **Workspace** | Semantic search complements SQLite FTS | Use `/workspace search` for keywords, `/retrieval search` for concepts |
| **Auditing** | Verify indexing in session audit | Check "New documents indexed?" |
| **Evolution** | Find recurring patterns across AARs | Search for similar issues before extracting patterns |
| **Scratchpad** | Search scratchpad for past work-in-progress | Index scratchpad items for continuity across sessions |

### Knowledge Operon Integration

**Before retrieval operon**:
- File document → Update INDEX.md → Done
- Search: Manual directory navigation

**After retrieval operon**:
- File document → Update INDEX.md → Auto-index → Semantic search available
- Search: `/retrieval search "query"` finds by concept

**Modified knowledge workflow**:
1. Create document with YAML frontmatter
2. File to appropriate directory
3. Update INDEX.md
4. **Trigger indexing**: `/retrieval index <path>`
5. Verify: `/retrieval search` finds new document

### Workspace Operon Integration

**Complementary search approaches**:

| Use Case | Tool | Example |
|----------|------|---------|
| **Exact keyword** | `/workspace search` (SQLite FTS) | "docker-compose.yml" |
| **Concept/meaning** | `/retrieval search` (semantic) | "container orchestration" |
| **Hybrid** | Both | Use FTS first, then semantic for related concepts |

**When to use each**:
- **SQLite FTS**: Fast, exact matches, filename search, Boolean queries
- **Semantic search**: Conceptual relationships, paraphrasing, cross-domain connections

### Auditing Checklist Integration

**New audit checks**:
- [ ] New knowledge documents indexed? (`/retrieval status` check)
- [ ] Search performance acceptable? (latency < 100ms)
- [ ] Collection stats current? (chunk count matches file count)
- [ ] Failed searches documented? (track queries that miss expected results)

## Examples

### Example 1: Solve Recurring Problem

```bash
# Encountered error: "Pydantic validation error in ChromaDB"
/retrieval search "pydantic chromadb compatibility"

# Found: docs/knowledge/aars/2026-02-06-chromadb-python314-issue.md
# Solution: Migrate to Qdrant (documented in AAR)
# Apply solution immediately
```

### Example 2: Pre-Decision Research

```bash
# Deciding on embedding model
/retrieval search "embedding model comparison" --type decision

# Found decision: docs/knowledge/decisions/2026-01-15-embedding-model-selection.md
# Context: Chose nomic-embed-text for 768-dim, local-first
# Consequence: Fast, accurate, no API costs
# Use same decision criteria for new choice
```

### Example 3: Pattern Discovery

```bash
# Writing FastAPI endpoint, need pattern
/retrieval search "FastAPI error handling pattern"

# Found pattern: docs/knowledge/patterns/fastapi-error-handling.md
# Apply pattern:
# - Use HTTPException for client errors
# - Use custom exception middleware for server errors
# - Log all errors with request context
```

### Example 4: Cross-Reference AARs

```bash
# Writing AAR about context window management
/retrieval search "context window" --type aar

# Found 3 related AARs:
# - 2026-01-15: Context window optimization
# - 2025-12-10: Token limit exceeded
# - 2025-11-03: Prompt compression techniques

# Add to related-files in frontmatter
# Check if this is a recurring issue (evolution operon)
```

## Anti-Patterns

### ❌ Anti-Pattern 1: Keyword-Only Search

**Wrong**:
```bash
/retrieval search "docker-compose.yml"
```

**Why wrong**: Semantic search is for concepts, not exact filenames.

**Right**:
```bash
# Use workspace FTS for filenames
/workspace search "docker-compose.yml"

# Use retrieval for concepts
/retrieval search "container orchestration configuration"
```

### ❌ Anti-Pattern 2: Not Indexing After Filing

**Wrong**:
```bash
/knowledge file aar
# [Don't index]
# [Later] /retrieval search finds nothing
```

**Why wrong**: New documents not searchable until indexed.

**Right**:
```bash
/knowledge file aar
/retrieval index docs/knowledge/aars/2026-02-06-new-aar.md
/retrieval search "query related to new AAR"  # ✓ Found
```

### ❌ Anti-Pattern 3: Over-Filtering

**Wrong**:
```bash
/retrieval search "API design" --type decision --domain web --tags api,rest --after 2026-01-01
```

**Why wrong**: Too many filters = zero results. Start broad, narrow if needed.

**Right**:
```bash
# Start broad
/retrieval search "API design"

# If too many results, add one filter
/retrieval search "API design" --type decision

# Still too many? Add another
/retrieval search "API design" --type decision --domain web
```

### ❌ Anti-Pattern 4: Ignoring Scores

**Wrong**:
```bash
/retrieval search "docker"
# Top result score: 0.301 (low!)
# [Use it anyway]
```

**Why wrong**: Low scores (<0.5) indicate weak matches. Refine query or document doesn't exist.

**Right**:
```bash
/retrieval search "docker"
# Top result score: 0.301 (low)
# Refine query with more context
/retrieval search "docker compose healthcheck configuration"
# Top result score: 0.687 ✓
```

### ❌ Anti-Pattern 5: Not Using Similar Search

**Wrong**:
```bash
# Writing new AAR, manually guessing related files
related-files:
  - docs/knowledge/aars/some-aar.md  # [Guessed]
```

**Why wrong**: Similar search finds related documents automatically.

**Right**:
```bash
# After writing AAR, find similar documents
/retrieval similar docs/knowledge/aars/2026-02-06-new-aar.md --type aar

# Add top results to related-files
related-files:
  - docs/knowledge/aars/2026-01-15-similar-issue.md
  - docs/knowledge/aars/2025-12-03-related-problem.md
```

## Performance Targets

| Metric | Phase 1 | Phase 3 (Hybrid) | Phase 4 (Optimized) |
|--------|---------|------------------|---------------------|
| **Hit Rate (Top-5)** | 70% | 85-90% | 90-95% |
| **Latency** | <100ms | <100ms | <50ms |
| **Collection Size** | 200 chunks | 500 chunks | 1000+ chunks |

**Current** (Phase 1):
- Hit rate: 70% (semantic only)
- Latency: ~57ms median (outliers need investigation)
- Collections: knowledge_base (102 chunks), workspace_artifacts (not indexed)

**Phase 3 improvements**:
- Hybrid search: +30-40% accuracy (BM25 + semantic + RRF)
- Date filtering: Timestamp conversion for range queries
- Domain/tag filtering: List containment queries

**Phase 4 enhancements**:
- Auto-indexing: File watcher
- Reranking: Cross-encoder (+10-12% accuracy)
- GraphRAG: Multi-hop related-files traversal
- Monitoring: Query logs, hit rate tracking

## Technical Details

**Embedding Model**: nomic-embed-text (768-dim)
- Trained on paired questions/answers
- Optimized for semantic similarity
- Local inference via Ollama
- ~300ms per embedding

**Vector Store**: Qdrant
- Cosine similarity search
- Metadata filtering support
- Local persistent storage
- Sub-50ms query latency

**Chunking Strategy**:
- Recursive text splitting
- 500 tokens per chunk (approximate)
- 10% overlap between chunks
- Markdown-aware separators (preserve section structure)

**Metadata Schema**:
```yaml
# Document-level (from frontmatter)
type: aar | decision | research | pattern
title: str
date: YYYY-MM-DD
domain: [str]
tags: [str]
severity: minor | moderate | significant  # AAR only
related_files: [path]

# Chunk-level (generated)
chunk_id: UUID
chunk_position: int
chunk_total: int
heading: str
heading_level: int
file_path: absolute path
```

## Troubleshooting

### Issue: Search returns no results

**Causes**:
1. Document not indexed
2. Query too specific
3. Metadata filter too restrictive

**Solutions**:
```bash
# 1. Check index status
/retrieval status

# 2. Re-index if needed
/retrieval index docs/knowledge/

# 3. Try broader query
/retrieval search "broader query"

# 4. Remove filters
/retrieval search "query" --type decision  # With filter
/retrieval search "query"                  # Without filter
```

### Issue: Low relevance scores

**Causes**:
1. Query doesn't match document content
2. Document needs better metadata
3. Need more context in query

**Solutions**:
```bash
# 1. Add more context to query
/retrieval search "docker"                    # Too vague
/retrieval search "docker compose patterns"   # Better

# 2. Check document content
vim docs/knowledge/patterns/docker-pattern.md
# Ensure key terms present in content

# 3. Update document metadata
# Add relevant tags/domains to frontmatter
```

### Issue: Indexing takes too long

**Expected**: ~0.33s per chunk (embedding generation dominates)

**If slower**:
1. Check Ollama is running: `curl http://localhost:11434/api/tags`
2. Check system load: `htop`
3. Verify Ollama model loaded: `ollama list`

**Optimization**:
```bash
# Index in background (Phase 4)
/retrieval index docs/knowledge/ --background

# Or split into batches
/retrieval index docs/knowledge/aars/
/retrieval index docs/knowledge/decisions/
```

## Future Enhancements

### Phase 3: Hybrid Search (Week 4)
- [ ] Add BM25 keyword search (SQLite FTS integration)
- [ ] Implement Reciprocal Rank Fusion (merge semantic + keyword)
- [ ] Date range filtering (convert ISO dates to timestamps)
- [ ] Domain/tag array filtering (list containment)

### Phase 4: Advanced Features (Optional)
- [ ] Auto-indexing: File watcher on `docs/knowledge/`
- [ ] Reranking: Cross-encoder model for top-K refinement
- [ ] Hierarchical chunking: Document → section → chunk levels
- [ ] GraphRAG: Multi-hop related-files traversal
- [ ] Query logs and hit rate tracking
- [ ] Performance dashboard

### Phase 5: Multi-Project (Future)
- [ ] Index multiple projects simultaneously
- [ ] Project-scoped search
- [ ] Cross-project pattern discovery
- [ ] Shared knowledge base for common patterns
