---
type: aar
title: "RAG capability analysis for MESO"
date: 2026-02-06
project: techbiont-framework
domain: [meso, architecture, ai]
severity: minor
scope: "Analyze existing RAG infrastructure and plan integration with MESO"
tags: [rag, unified-ai, knowledge-base, workspace]
related-files:
  - /home/Valis/code/github.com/the-azuran/unified-ai/README.md
  - /home/Valis/code/github.com/the-azuran/techbiont-framework/operons/knowledge/SKILL.md
  - /home/Valis/code/github.com/the-azuran/techbiont-framework/docs/knowledge/decisions/2026-02-04-knowledge-document-format.md
---

## AAR: RAG capability analysis for MESO

### What Happened
Analyzed existing codebases to answer "Can we give MESO a RAG?" Found:

1. **Unified‑AI project** — local‑first RAG system with Ollama embeddings, LLM interface, ChromaDB config, but incomplete (no ingest/retrieval implementation).
2. **Knowledge operon** — guidelines for RAG‑ready documents (YAML frontmatter schemas) and capture workflows.
3. **Workspace operon** — SQLite full‑text search for artifacts, but not semantic/RAG.
4. **Architectural intent** — decision logs and AARs explicitly mention "future RAG indexer" as Phase 2.

### What Went Well
- **Foundation exists** — unified‑AI has embedding client, LLM wrapper, ChromaDB config
- **Knowledge schemas ready** — documents already structured for RAG (frontmatter)
- **Workspace search operational** — SQLite FTS provides baseline search capability
- **Clear architectural direction** — MESO CLI autonomic‑somatic model fits RAG well

### What Went Wrong
- **Unified‑AI incomplete** — ingest/, vectorstore/, retrieval/ directories empty
- **No integration** — RAG components isolated from MESO knowledge base
- **No operon trigger** — no way to activate RAG queries within MESO workflow
- **Documentation gap** — no clear path from knowledge schemas to vector indexing

### Root Causes
1. **Parallel development** — unified‑AI built as standalone project, not integrated with MESO
2. **Phase‑based roadmap** — RAG marked as "Phase 2" but never implemented
3. **Tool fragmentation** — workspace (SQLite) vs unified‑AI (ChromaDB) use different search backends
4. **Missing bridge** — no code to extract YAML frontmatter from knowledge docs for embedding

### Lessons Learned
1. **RAG readiness is high** — 80% of infrastructure exists, just needs wiring
2. **Local‑first aligns with MESO** — Ollama + ChromaDB fits autonomic pathway
3. **Knowledge schemas work** — YAML frontmatter provides structured metadata for RAG
4. **Integration > new code** — better to complete unified‑AI than build from scratch
5. **Autonomic‑somatic split** — simple retrieval (autonomic) vs complex reasoning (somatic)

### Action Items
- [ ] Audit unified‑AI codebase — identify exact gaps in ingest/vectorstore/retrieval
- [ ] Design RAG operon interface — commands (`/rag search`, `/rag index`), metadata handling
- [ ] Prototype indexing — start with `docs/knowledge/` using existing embedding client
- [ ] Integrate with workspace SQLite — hybrid search: full‑text + semantic
- [ ] Create decision log for RAG architecture choice (extend knowledge vs new operon)
- [ ] Update MESO CLI architecture docs with RAG neurozooid specification

### Metrics
- Estimated time saved/lost: 2 hours analysis saved future re‑discovery
- Rework required: Medium — need to complete unified‑AI and integrate
- Errors caught by audit: 0 — analysis only
- Errors that escaped: 0 — analysis only