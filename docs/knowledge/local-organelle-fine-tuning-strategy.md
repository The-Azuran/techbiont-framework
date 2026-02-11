---
type: research
title: "Local Organelle: MESO-Native Fine-Tuning Strategy"
date: 2026-02-08
updated: 2026-02-08
project: techbiont-framework
domain: [meso, architecture, ai, hardware, sovereignty]
status: active
confidence: medium
sources:
  - url: "internal"
    title: "Session analysis of system sovereignty video summary"
    accessed: 2026-02-08
tags: [fine-tuning, qlora, local-inference, open-weights, model-sovereignty]
related:
  - edge-computing-architecture.md
  - pi-minimalist-agent-architecture.md
  - mesocomplete-productization-architecture.md
---

## Summary

Analysis of fine-tuning open-weight models to create a MESO-native local organelle, eliminating single-point dependency on Claude API. Inspired by "system sovereignty" philosophy: own your hardware, run your tools locally, build capability on your timeline instead of vendor upgrade cycles.

**Key finding:** QLoRA fine-tuning is cheap ($50-300 cloud, near-free on owned hardware). The real cost is curating high-quality training data from session transcripts. A fine-tuned local model can handle routine L3/L4 tasks today; replacing the primary organelle requires waiting for open model reasoning to mature.

## Findings

### System Sovereignty Alignment

The MESO architecture already embodies system sovereignty at the software layer:
- Zooids and operons are local markdown files, not SaaS features
- Colony structure is model-agnostic in principle
- Install script copies files rather than pulling a managed service
- No vendor can deprecate, paywall, or alter the colony architecture

**The gap:** The organelle itself (Claude API) is the one dependency that violates sovereignty. Anthropic controls pricing, rate limits, model behavior, and availability. This is the exact vendor lock-in the sovereignty philosophy warns against.

### Fine-Tuning Approach: QLoRA

QLoRA (Quantized Low-Rank Adaptation) adapts a pre-trained model with minimal parameter changes. Not training from scratch — teaching an existing capable model MESO-specific patterns.

| Approach | Cloud Cost | Local (3x3090 / 72GB VRAM) | Viability |
|----------|-----------|---------------------------|-----------|
| QLoRA fine-tune | $50-300 | Electricity + time | **Primary approach** |
| Full fine-tune | $2,000-10,000 | Won't fit for 70B+ | Backup if QLoRA insufficient |
| Train from scratch | $1M-100M+ | Impossible | Not considered |

### Base Model Candidates (as of 2026-02)

| Model | Parameters | VRAM Fit (3x3090) | Strengths |
|-------|-----------|-------------------|-----------|
| Qwen 2.5-Coder 32B | 32B | Comfortable | Excellent code quality, right size for local |
| DeepSeek-Coder-V2 | 236B MoE | Quantized only | Strong agentic reasoning |
| Llama 3.3 | 70B | Tight, needs quantization | Good instruction following |

**Recommendation:** Start with Qwen 2.5-Coder 32B. Fits the hardware, strong baseline, active development community.

### Training Data Requirements

1,000-5,000 high-quality examples of MESO-compliant interactions:
- Tool orchestration (read/grep/glob/agent dispatch sequences)
- Autonomy level compliance (L1 escalation, L2 collaboration patterns)
- Boring code style (named intermediates, early returns, no cleverness)
- Authorship conventions (Rowan Valle, no Co-Authored-By)
- Security deny-list compliance
- Multi-step agentic task completion

**Data sources:**
- Session transcripts in `~/.claude/projects/` (JSONL format, already captured)
- Synthetic generation using Claude to produce gold-standard examples
- Manual curation by operator (grade examples as good/bad)

**Data curation is the real cost.** Measured in operator time, not dollars.

### Capability Assessment: What Fine-Tuning Does and Doesn't Do

Fine-tuning teaches **style**, not **capability**.

**A MESO-tuned 33B model WOULD:**
- Speak colony vocabulary natively (zooids, operons, autonomy levels)
- Default to MESO conventions without 16KB system prompt
- Follow authorship, coding style, and security rules from weights
- Free up context window for actual work (no prompt overhead)
- Handle routine, well-defined tasks reliably

**A MESO-tuned 33B model WOULD NOT:**
- Match 400B+ model reasoning on complex multi-step tasks
- Handle long agentic chains without losing coherence
- Avoid hallucination on unfamiliar code patterns as well as larger models
- Solve novel architectural problems at the same level
- Reliably orchestrate complex multi-tool workflows

### Hardware Sovereignty Strategy

Aligned with "dollar-per-VRAM" and "efficiency-per-teraflop" metrics:
- Used 3090s: $800-1,000 each, 24GB VRAM — excellent $/VRAM
- 3x 3090s = 72GB VRAM, sufficient for 32B models and quantized 70B
- RTX Pro 4000 Blackwell with 256GB ECC RDIMM for inference serving
- Buy capability when prices are right, not on industry upgrade cycles
- Previous-gen GPUs outperform new integrated-graphics builds at fraction of cost

## Recommended Phased Approach

### Phase 1: Data Curation (Free, start now)
- Export session transcripts from `~/.claude/projects/`
- Curate high-quality MESO interaction examples
- Build training dataset with good/bad example pairs
- Value: Documentation of the symbiosis regardless of fine-tuning

### Phase 2: Initial Fine-Tune (~$100-200)
- QLoRA fine-tune Qwen 2.5-Coder 32B on curated dataset
- Run locally on 3x3090 rig
- Benchmark against base model on MESO-specific tasks
- Evaluate: Does it follow colony rules? How far does it drift?

### Phase 3: Hybrid Deployment (Evaluate)
- Local organelle handles L3/L4 tasks (routine, well-defined, low-risk)
- Claude API handles L1/L2 tasks (security, architecture, novel work)
- Dual-organelle colony: local for cost savings, API for capability
- Measure: task completion rate, error rate, operator satisfaction

### Phase 4: Full Sovereignty (Wait for ecosystem)
- When open 70B+ models handle agentic loops reliably (~2027 estimate)
- Fine-tune the best available on accumulated MESO data
- Potentially drop API dependency entirely
- Maintain API as fallback, not primary

**Total estimated cost for Phases 1-3:** Under $500 on owned hardware.

## Open Questions

- What's the minimum viable dataset size for useful MESO adaptation?
- Can synthetic data from Claude effectively train a competitor model? (Legal/ToS review needed)
- How do we benchmark "MESO compliance" objectively?
- Should the local organelle use the same tool interface (Claude Code compatible) or a custom harness?
- What's the energy cost of 3x3090 inference vs. API calls at scale?

## Cross-References

- [Edge Computing Architecture](edge-computing-architecture.md) — distributed edge nodes as workers (complementary, not overlapping)
- [Pi Minimalist Agent Architecture](pi-minimalist-agent-architecture.md) — lightweight edge agents
- [MESOcomplete Productization](mesocomplete-productization-architecture.md) — hardware+software sovereignty product vision
- [Multi-Instance Claude Methods](multi-instance-claude-methods.md) — orchestration patterns applicable to hybrid deployment

---

*Authored by Rowan Valle; Executed by Claude Code*
*Symbiont Systems LLC*
