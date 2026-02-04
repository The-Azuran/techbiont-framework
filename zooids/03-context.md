# Context Engineering — Gastrozooid (Information Ingestion)

Context determines success more than model capability.

## Principles
- Front-load critical information: constraints, requirements, relevant code
- Seed with working examples before requesting modifications
- Start fresh sessions for distinct tasks — avoid context rot
- Iterate to sophistication: simple version first, verify, then enhance

## Context Hygiene
- Keep CLAUDE.md and rules files concise — they consume context every session
- Use `/context` to monitor token usage
- Prune outdated instructions, rarely-used patterns, verbose explanations
- Prefer bullet points over paragraphs in configuration files

## When Context Fails

| Symptom | Cause | Fix |
|---------|-------|-----|
| Contradictory outputs | Context rot | Start fresh session |
| Forgetting earlier decisions | Window overflow | Summarize and restart |
| Ignoring instructions | Buried context | Move instructions to top |
| Inconsistent style | Mixed examples | Provide single clear example |

## Training Cutoff
- For libraries/APIs beyond training data: supply documentation in context
- Prefer stable, well-known tools ("boring technology")
- Provide usage examples for unfamiliar APIs
- Verify claims about recent tools against authoritative sources
