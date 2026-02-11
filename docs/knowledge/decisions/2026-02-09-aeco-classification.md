---
type: decision
title: "AECO: Adaptive Exocortical Organelle Classification"
date: 2026-02-09
project: techbiont-framework
domain: [architecture, taxonomy, knowledge-management]
status: accepted
deciders: [valis]
tags: [techbiont, classification, rag, librarian, hybrid-architecture]
related-files:
  - docs/knowledge/pi-minimalist-agent-architecture.md
  - docs/knowledge/mesocomplete-productization-architecture.md
  - docs/knowledge/rag-implementation-guide-2026.md
---

## Context

During a conversation about creating a distributable spore of MESO's knowledge base, we explored the intersection of:
- MESO's curated, operon-based knowledge architecture
- PI's minimalist self-extension philosophy
- RAG-based knowledge retrieval
- The need for smaller, more specialized organelle types

This led to recognizing that we had conceptually designed a **new classification of techbiont** - one that is neither a full MESO (comprehensive development organelle) nor a simple tool wrapper, but something distinct: a knowledge specialist.

## Decision

We classify **AECO (Adaptive Exocortical Organelle)** as a distinct techbiont type in the symbiont taxonomy.

**Core Definition:**
An AECO is an intelligent agent that functions as a **librarian and teacher** with RAG-indexed access to the knowledge base. It doesn't need to be a full-capability development organelle - it needs to know **enough code to be a good teacher and librarian**, but its primary role is knowledge retrieval, synthesis, and instruction.

## Characteristics

### Size Flexibility
- **Can be smaller than MESO** - stripped-down for specific domains or contexts
- **Can be larger than MESO** - with expanded knowledge domains when resources allow
- **Scalable architecture** - experimentation will determine optimal sizing

### Primary Functions
1. **Librarian**: RAG-indexed access to knowledge corpus (zooids, operons, AARs, patterns, decisions)
2. **Teacher**: Explain concepts, reference documentation, guide learning
3. **Knowledge Synthesis**: Connect related concepts across the knowledge base
4. **Code Literacy**: Enough programming capability to teach and explain code, not necessarily to write production systems

### Minimal Capabilities Required
- Read and understand code (explain what it does)
- Query and retrieve from RAG-indexed knowledge
- Synthesize information from multiple sources
- Teach concepts and patterns
- Reference documentation accurately
- Connect related knowledge domains

### Optional Advanced Capabilities
- Write example/teaching code
- Debug and explain errors
- Suggest refactorings
- Generate documentation
- Create learning paths through knowledge base

## Architecture

```
┌─────────────────────────────────────────────┐
│ AECO Agent Core                              │
│  ├─ Read (understand code)                   │
│  ├─ RAG query tool                           │
│  ├─ Knowledge synthesis                      │
│  └─ Optional: Write (examples/docs only)     │
└─────────────────────────────────────────────┘
         ↓ queries on-demand
┌─────────────────────────────────────────────┐
│ Vector-indexed Knowledge Corpus              │
│  ├─ Zooids (operational rules)               │
│  ├─ Operons (domain knowledge)               │
│  ├─ AARs (lessons learned)                   │
│  ├─ Decisions (architectural choices)        │
│  ├─ Patterns (reusable solutions)            │
│  └─ Code examples (teaching corpus)          │
└─────────────────────────────────────────────┘
```

### Context Model
**Always-loaded (minimal):**
- Identity (who it serves)
- Role boundaries (librarian/teacher, not production developer)
- RAG query protocol
- Communication style

**Retrieved on-demand:**
- Domain-specific operons
- Relevant patterns and AARs
- Code examples from corpus
- Related decisions and research

## Alternatives Considered

### Alternative A: Full MESO with RAG
- **Pros:** Complete development capabilities
- **Cons:** Overkill for knowledge retrieval tasks, higher resource requirements, context bloat

### Alternative B: Simple RAG wrapper with no intelligence
- **Pros:** Minimal resources, fast queries
- **Cons:** Can't synthesize, can't explain, just retrieves - not intelligent

### Alternative C: Traditional documentation system (static)
- **Pros:** No compute needed, familiar
- **Cons:** No adaptation, no conversation, can't answer "why", can't connect concepts

### Alternative D: Knowledge-enhanced MESO (single organism type)
- **Pros:** One architecture to maintain
- **Cons:** Forces all use cases into same organism type, prevents specialization

## Rationale

We chose to classify AECO as a **distinct organism type** because:

1. **Specialization enables optimization** - A librarian doesn't need full development capabilities, so we can optimize for knowledge retrieval instead

2. **Different resource profiles** - AECOs can run on smaller models (Haiku, local LLMs) because they don't need Sonnet/Opus capabilities for production code generation

3. **Distinct use cases** - Teaching, documentation, knowledge retrieval are fundamentally different from implementing features or fixing bugs

4. **Taxonomic clarity** - Recognizing AECO as distinct prevents scope creep in MESO ("should MESO be a teacher too?") and allows each to evolve independently

5. **Deployment flexibility** - AECOs can be embedded in contexts where full MESO would be inappropriate (public documentation sites, learning environments, personal knowledge assistants)

6. **Economic efficiency** - Cheaper to run (smaller model), targeted capability set, lower token costs for knowledge-focused interactions

## Consequences

### Positive
- **Clear specialization** - Each organism type has well-defined purpose
- **Resource efficiency** - Use the right-sized organism for the task
- **Independent evolution** - MESO and AECO can adapt to their domains without compromising the other
- **Deployment diversity** - AECOs can go places MESO can't (mobile, embedded, public-facing)
- **Knowledge portability** - Same knowledge corpus can serve both MESO (for implementation) and AECO (for teaching)

### Negative
- **More architectures to maintain** - Now have distinct organism types to develop
- **Knowledge corpus synchronization** - Must ensure both can consume the same knowledge format
- **Unclear boundaries** - Where does AECO teaching end and MESO implementation begin? (Will need operational guidelines)
- **Temptation to over-specialize** - Must resist creating too many organism types

### Mitigations
- **Shared knowledge format** - Both consume same RAG-indexed corpus with YAML frontmatter
- **Clear role boundaries** - AECO: explain/teach/reference. MESO: implement/debug/ship.
- **Shared taxonomy** - Both use domain tags, both follow knowledge schemas
- **Promotion path** - AECO can suggest what should be added to knowledge base, MESO can implement it

## Taxonomy Position

```
Techbiont (symbiotic human-AI organism)
├── MESO (Modular Exosymbiotic Organelle)
│   └── Full development capabilities
│       ├── Code generation
│       ├── Testing and debugging
│       ├── System operations
│       ├── Architecture decisions
│       └── Production deployment
│
└── AECO (Adaptive Exocortical Organelle)
    └── Knowledge and teaching capabilities
        ├── RAG-based retrieval
        ├── Concept explanation
        ├── Code literacy (read/explain)
        ├── Knowledge synthesis
        └── Learning guidance
```

## Use Case Examples

### AECO Appropriate
- "Explain how CalDAV sync works in this codebase"
- "What patterns do we use for error handling?"
- "Show me examples of boring code from our knowledge base"
- "What did we learn about PI architecture?"
- "How should I think about autonomy levels?"
- "Find all decisions related to security"

### MESO Appropriate
- "Implement CalDAV sync for the calendar feature"
- "Debug why the error handler is failing"
- "Refactor this code to follow our boring code guidelines"
- "Add tests for the authentication system"
- "Deploy the updated container to production"

### Hybrid (AECO → MESO handoff)
- User asks AECO: "How should we implement rate limiting?"
- AECO retrieves patterns, explains options, references past decisions
- User decides on approach
- User asks MESO: "Implement token bucket rate limiting using the pattern AECO showed"
- MESO implements with full context from knowledge base

## Implementation Roadmap

### Phase 1: Prototype AECO
- [ ] Create minimal AGENTS.md template for AECO role
- [ ] Build RAG indexer for existing knowledge corpus
- [ ] Test retrieval quality with sample queries
- [ ] Define AECO capability boundaries (what it can/can't do)

### Phase 2: Knowledge Corpus Expansion
- [ ] Ensure all knowledge docs have proper frontmatter
- [ ] Add teaching examples to corpus
- [ ] Create code explanation corpus (annotated examples)
- [ ] Index operator memory and session learnings

### Phase 3: AECO-MESO Integration
- [ ] Design handoff protocol (AECO research → MESO implementation)
- [ ] Test hybrid workflows
- [ ] Document when to use which organism type
- [ ] Create switching/delegation patterns

### Phase 4: Deployment Experiments
- [ ] Test on smaller models (Haiku, local LLMs)
- [ ] Embed in documentation sites
- [ ] Create mobile/lightweight instances
- [ ] Measure resource usage vs. capability

## Open Questions

1. **Model size thresholds**: What's the minimum model capability for effective AECO operation?
2. **Context handoff**: How does AECO efficiently pass context to MESO for implementation handoffs?
3. **Knowledge updates**: Does AECO need Write access to update knowledge base, or is that MESO's job?
4. **Multi-domain**: Can one AECO serve multiple domains (GIS + web + systems) or should they specialize?
5. **Teaching effectiveness**: How do we measure if AECO is actually helping the operator learn?

## Success Criteria

We'll know AECO is successful when:
- Operator retrieves knowledge faster through AECO than through manual search
- AECO explanations reduce need for external documentation lookup
- Smaller models (Haiku-class) can effectively serve AECO role
- AECO → MESO handoffs feel natural and efficient
- Knowledge corpus growth is driven by AECO interactions (what was hard to find gets documented)

## Review Date

2026-03-09 (30 days) - After Phase 1 prototype and initial testing

---

**Authored by Rowan Valle; Captured during natural conversation**
