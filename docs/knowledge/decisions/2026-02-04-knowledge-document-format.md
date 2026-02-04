---
type: decision
title: "Markdown with YAML frontmatter for knowledge documents"
date: 2026-02-04
project: techbiont-framework
domain: [meso, architecture]
status: accepted
deciders: [valis]
tags: [knowledge-capture, rag-preparation, document-format]
related-files:
  - docs/schemas/knowledge-schemas.md
  - operons/knowledge/SKILL.md
---

## Context
MESO needs a standardized format for knowledge documents (AARs, decision logs, research docs, patterns) that serves two masters: human readability now and machine indexability for future RAG.

## Decision
Use Markdown files with YAML frontmatter for all knowledge documents.

## Alternatives Considered

### Alternative A: Pure YAML/JSON files
- **Pros:** Trivially machine-parseable, no ambiguity in structure, schema validation with JSON Schema
- **Cons:** Painful to write and read by hand, git diffs are unreadable for prose, unnatural for documents that are primarily narrative

### Alternative B: Markdown with sidecar JSON metadata
- **Pros:** Clean separation of prose and metadata, each file does one thing
- **Cons:** Doubles file count, metadata can drift from content, two files to manage per document

### Alternative C: Markdown with YAML frontmatter
- **Pros:** Already the MESO pattern (SKILL.md files), human-readable, git-friendly, standard YAML parsers handle frontmatter, every RAG pipeline and static site generator supports it, one file per document
- **Cons:** Frontmatter can't express deeply nested structures well, no schema validation without custom tooling

## Rationale
YAML frontmatter is the existing MESO convention. It provides machine-parseable metadata without sacrificing the readability that makes documents useful to humans. The alternatives solve problems we don't have (deeply nested structured data, formal schema validation) while creating problems we do (unreadable prose, double file management). The operator does not write code independently, so document formats must be accessible without tooling.

## Consequences
- All new knowledge documents must include YAML frontmatter with at minimum: type, title, date, domain
- Existing documents without frontmatter remain valid but won't be indexed by future RAG
- Retrofitting frontmatter onto existing docs is a manual process (Phase 2)
- Schema validation requires custom tooling if desired (a simple Python script, not a framework)

## Review Date
2026-08-04 — revisit after 6 months of use to evaluate whether the schema fields are sufficient or need revision.
