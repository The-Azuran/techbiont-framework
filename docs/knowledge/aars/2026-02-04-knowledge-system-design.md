---
type: aar
title: "Knowledge Accumulation System Design"
date: 2026-02-04
project: techbiont-framework
domain: [meso, architecture]
severity: minor
scope: "Design and implement Phase 1 of structured knowledge capture for MESO"
tags: [knowledge-capture, templates, schemas, rag-preparation]
related-files:
  - operons/knowledge/SKILL.md
  - docs/schemas/knowledge-schemas.md
  - templates/knowledge/aar.template.md
  - templates/knowledge/decision.template.md
  - templates/knowledge/research.template.md
  - templates/knowledge/pattern.template.md
---

## AAR: Knowledge Accumulation System Design

### What Happened
Designed and implemented Phase 1 of a structured knowledge accumulation system for MESO. Created a new knowledge operon (Rhopalia), four document templates with YAML frontmatter schemas, a canonical schema reference, and updated existing operons (evolution, auditing) to integrate with the new system. Updated STANDING-ORDERS.md with new templates and the README with the new operon.

### What Went Well
- Plan agent produced a thorough design that required minimal revision
- Split concerns approach (templates in framework, data in projects) keeps MESO generic
- YAML frontmatter is the natural format — already in use for SKILL.md files
- No impact on auto-load budget since the operon is trigger-activated
- install.sh already iterates `operons/*/` so no script changes needed

### What Went Wrong
- Nothing significant. Minor friction from needing to read source files in techbiont-framework rather than the symlinked copies in ~/.claude/ for edits.

### Root Causes
- Symlinks point ~/.claude/skills/ -> techbiont-framework/operons/, but edits must target the source. This is by design but easy to forget.

### Lessons Learned
- When editing operons, always target the source in techbiont-framework, not the symlink in ~/.claude/skills/
- Starting with the format question (markdown+YAML vs JSON vs sidecar) before the structure question saved rework

### Action Items
- [ ] Create first real decision log and pattern document from actual project work
- [ ] Retrofit frontmatter onto existing research docs when revisiting them (Phase 2)
- [ ] Build RAG indexer once knowledge base reaches critical mass (Phase 2)

### Metrics
- Estimated time saved/lost: net positive — templates now exist for future use
- Rework required: none
- Errors caught by audit: 1 (wrong file path for operon edits)
- Errors that escaped: 0
