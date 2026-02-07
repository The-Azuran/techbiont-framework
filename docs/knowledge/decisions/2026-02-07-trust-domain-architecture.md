---
type: proposal
title: "Three-Tier Trust Domain Model with Multi-Layer Gating"
date: 2026-02-07
project: techbiont-framework
domain: [security, trust-model, meso]
status: proposed
author: ai-research
awaiting-decision: valis
tags: [trust-domains, gating, security, L1-escalation]
related-files:
  - zooids/04-security.md
  - docs/knowledge/decisions/2026-02-07-curl-security-architecture.md
  - templates/trust-domains.template.json
---

**STATUS**: Research proposal awaiting operator review and decision.
**Operator requirement**: "Even then we still must be cautious and ask me for permissions and implement gates/gating"

## Context

As part of curl security enhancement (Phase 2 planning), operator asked:

> "Yes please! But even then we still must be cautious and ask me for permissions and implement gates/gating"

This prompted the question: **Should MESO maintain an allowlist of trusted domains for script downloads?**

**Competing concerns**:
- **Operator efficiency**: Avoid repetitive approvals for known-good sources (npm, pip, operator's own repos)
- **Security accountability**: L1 escalation must remain for ALL script downloads (even from "trusted" sources)
- **Supply chain risk**: Even trusted infrastructure can be compromised (npm, PyPI, GitHub all have attack history)
- **MESO philosophy**: Operator has final authority (L1), AI is tool not decision-maker

**Constraints**:
- Must not bypass L1 escalation (security = operator accountability)
- Must not persist approval across sessions (session-only cache maximum)
- Must layer multiple defenses (not rely on domain trust alone)
- Must be opt-in (explicit operator configuration, not default)

## Proposed Approach

**Recommendation: Implement three-tier trust domain model with mandatory multi-layer gating:**

### Tier 1: Verified Sources (Still L1 Gated)
- Official package managers (npm, pip, cargo registries)
- Operator's own repositories (github.com/operator/*)
- MESO framework distributions

**Gate**: Require L1 approval on first download per session. Cache approval for session only.

### Tier 2: Known-Good Infrastructure (L1 + Verification)
- Public repositories (github.com/*, gitlab.com/*)
- Official documentation sites (docs.python.org, nodejs.org)
- Well-known CDNs (cdn.jsdelivr.net, unpkg.com)

**Gate**: L1 approval + SHA256 verification mandatory every time. No caching.

### Tier 3: Untrusted (L1 + Sandbox Required)
- All other domains (default)

**Gate**: L1 approval + sandbox execution + manual inspection before native execution.

### Configuration Requirements
- **File**: `~/.claude/trust-domains.json` (operator-editable, mode 600)
- **Creation**: NOT created automatically - operator must explicitly opt-in
- **Default behavior**: If file absent, treat ALL sources as Tier 3 (untrusted)
- **Update mechanism**: Manual editing only (no AI modification)

### Gating Logic (Always Multi-Layer)

**Before ANY download**, AI must:
1. Check domain tier (which trust level applies)
2. Escalate to L1 with trust tier explanation and required gates
3. Present approval request with full context
4. Enforce HTTPS + safety flags (automated)
5. Require SHA256 verification (manual operator input)
6. Require manual inspection (operator reviews file before execution)
7. Cache approval ONLY for Tier 1, ONLY for current session

## Alternatives Considered

### Alternative A: Binary Trust Model (Trusted/Untrusted)
- **Pros**: Simpler to implement (one allowlist, one deny-by-default)
- **Cons**:
  - No nuance (official registries treated same as random GitHub repos)
  - All-or-nothing gating (trusted = no verification vs untrusted = full sandbox)
  - Doesn't reflect real-world risk gradients

### Alternative B: Persistent Approval Cache
- **Pros**: Minimize operator friction (approve once, trust forever)
- **Cons**:
  - Violates L1 accountability (approvals persist without review)
  - Supply chain drift (trusted repo compromised weeks after approval)
  - No forcing function to review sources periodically
  - Session boundaries exist for a reason (fresh context, re-evaluation)

### Alternative C: AI-Assessed Trust Scores
- **Pros**: Context-aware decisions (download history, domain reputation)
- **Cons**:
  - No reliable trust signal (AI can't assess supply chain integrity)
  - Prompt injection risk (malicious content influences scoring)
  - Offloads L1 decisions to AI (violates operator accountability)
  - Black box (why was this domain scored 7/10?)

### Alternative D: No Trust Domains (All Tier 3)
- **Pros**: Maximum security (every download sandboxed)
- **Cons**:
  - Unnecessary overhead (official registries are low-risk)
  - Operator friction (sandbox review for every npm install)
  - Doesn't reflect operator's actual trust model

### Alternative E: Auto-Populate Trust Domains from Framework
- **Pros**: Operators get sensible defaults immediately
- **Cons**:
  - Implicit trust (operator never reviewed domains)
  - Framework maintainers decide trust policy (not operator)
  - Violates opt-in principle (trust must be explicit)

## Rationale

**Three tiers chosen because**:

1. **Reflects real-world risk gradients**:
   - Tier 1: Very low risk (official registries, operator repos) - minimize friction
   - Tier 2: Low-moderate risk (public infrastructure) - require verification
   - Tier 3: Unknown risk (default) - full sandbox isolation

2. **Balances security and efficiency**:
   - Session cache for Tier 1 (avoid repetitive approvals same session)
   - No cache for Tier 2/3 (force fresh evaluation each time)
   - All tiers require L1 approval (operator always has final say)

3. **Layered defense**:
   - Trust tier + HTTPS enforcement + SHA256 verification + manual inspection
   - Even Tier 1 requires L1 approval (trust ≠ automatic execution)
   - Supply chain compromise mitigated by verification + inspection

4. **Operator control**:
   - Opt-in configuration (explicit, not implicit)
   - Operator edits trust-domains.json directly (sees what they're trusting)
   - No AI modification of trust policy
   - Session-only cache (no persistent trust without review)

5. **MESO philosophy alignment**:
   - L1 accountability maintained (operator approves every script download)
   - Defense-in-depth (multiple barriers, not single trust decision)
   - Military background (trust but verify - even "trusted" sources get gates)

**Why session-only cache (not persistent)**:
- Supply chain state changes between sessions (repos can be compromised)
- Session boundaries force re-evaluation (fresh context)
- Prevents approval fatigue (persistent cache → blind trust)
- Low friction cost (same-session downloads are rare, approval cache still helps)

**Why opt-in (not default)**:
- Trust is an explicit operator decision (not framework assumption)
- Forces operator to review trust policy before using it
- Framework maintainers don't impose trust decisions
- Absent file = safest default (all Tier 3, all sandboxed)

## Consequences

### Security Properties

✅ **L1 accountability preserved**:
- Every script download requires operator approval (even Tier 1)
- No automatic execution based on domain alone
- Approval prompts include trust tier and required gates
- Session-only cache (never persistent)

✅ **Defense-in-depth**:
- Domain tier (trust assessment)
- HTTPS enforcement (transport security)
- SHA256 verification (integrity check)
- Manual inspection (human review)
- Sandbox isolation (Tier 3 only)

✅ **Supply chain resilience**:
- Even trusted domains require verification (SHA256/GPG)
- Manual inspection catches unexpected content
- Session boundaries force re-evaluation
- Compromise of Tier 1 source still caught by verification layer

⚠️ **Tradeoffs accepted**:
- Operator friction (L1 approval always required, even Tier 1)
- No fully automated downloads (intentional - security over convenience)
- Trust domains require manual configuration (opt-in overhead)

### Operational Impact

✅ **Efficiency gains** (Tier 1 with session cache):
```bash
# First download from registry.npmjs.org (this session):
→ L1 approval prompt (explains Tier 1, session cache)
→ Operator approves
→ Download proceeds with verification

# Second download from registry.npmjs.org (same session):
→ Reminder: "Cached approval for registry.npmjs.org (Tier 1, this session)"
→ Operator sees reminder (not blocking prompt)
→ Download proceeds with verification
```

✅ **No false security** (Tier 2, no cache):
```bash
# Every download from github.com/random-user/repo:
→ L1 approval prompt (explains Tier 2, no cache)
→ Operator provides SHA256 checksum
→ Operator approves download
→ Download proceeds with verification
→ Operator inspects file before execution
→ Next download from github.com/random-user/repo: FULL APPROVAL AGAIN
```

⚠️ **Configuration overhead**:
- Operator must create trust-domains.json (copy template, edit tiers)
- Operator must decide domain tier assignments (which repos go where)
- Operator must maintain trust-domains.json (add/remove as trust changes)

### Long-term Commitments

**Template maintenance**:
- `templates/trust-domains.template.json` distributed via install.sh
- Template includes example domains per tier (commented out, opt-in)
- Template includes explanation of tier semantics

**Security zooid integration**:
- Update zooids/04-security.md with trust domain section
- Document gating requirements per tier
- Document session cache behavior (Tier 1 only)

**AI behavior when trust-domains.json absent**:
- Treat ALL sources as Tier 3 (untrusted, sandbox required)
- Notify operator: "No trust policy configured. All downloads require sandbox."
- Suggest: "Create ~/.claude/trust-domains.json from template to define trust tiers"

**Permission prompts**:
- Always show trust tier in approval request
- Always show required gates (HTTPS, SHA256, inspection, sandbox)
- Always show cache status (first download vs cached approval)
- Always allow operator to override (deny even if Tier 1)

## Review Date

**2026-05-07** (90 days):
- Assess whether three-tier model is appropriate or needs refinement
- Evaluate session cache effectiveness (too much friction vs too permissive)
- Review whether opt-in configuration is used (if not, why not?)
- Check for supply chain incidents (were gates sufficient?)

**Re-evaluate if**:
- Tier 1 sources compromised (did verification layers catch it?)
- Operator friction too high (session cache insufficient?)
- Trust domain usage low (is opt-in too much overhead?)
- New attack vectors emerge (do tiers need redefinition?)
