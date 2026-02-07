---
type: proposal
title: "Defense-in-Depth curl Security with Phased Implementation"
date: 2026-02-07
project: techbiont-framework
domain: [security, architecture, meso]
status: proposed
author: ai-research
awaiting-decision: valis
tags: [curl, security, containers, sandboxing, defense-in-depth]
related-files:
  - zooids/04-security.md
  - docs/knowledge/aars/2026-02-06-curl-security-research.md
  - docs/knowledge/curl-strategic-applications.md
---

**STATUS**: Research proposal awaiting operator review and decision.
**Phase 1 implementation complete**; this document proposes Phase 2 architecture.

## Context

Three parallel research agents analyzed curl usage across MESO and identified security gaps:

**Current vulnerabilities**:
- `curl | bash` enables MITM attacks, server-side evasion, and supply chain attacks
- Deny-list only blocked piping to bash/sh (missing Python, certificate bypass, HTTP)
- Security zooid had minimal guidance (one line mentioning piping)
- No safe download workflow for legitimate script needs
- No sandboxing infrastructure for testing untrusted code

**Operator request**: Implement comprehensive curl security while maintaining MESO's legitimate use cases (API testing, data acquisition, knowledge ingestion, operon distribution).

**Constraints**:
- Must not disrupt existing workflows (localhost API testing, HTTPS data retrieval)
- Must align with L1/L2 autonomy model (security = L1 escalation)
- Must avoid premature complexity (build only what's needed now)
- Must support future needs (MESOcomplete edge deployment, operon spore distribution)

## Proposed Approach

**Recommendation: Implement defense-in-depth security in two phases:**

**Phase 1 (Immediate)**: Expand deny-list + zooid security guidelines
- Add 10 new deny patterns (Python piping, cert bypass, HTTP, secrets)
- Add "Script Download Security" section to security zooid
- Enforce L1 escalation for all script downloads
- Define safe download pattern (download → verify → inspect → approve → execute)

**Phase 2 (Deferred)**: Container-based sandboxing infrastructure
- Podman ephemeral containers for untrusted script execution
- Scratchpad sandbox integration with manifest tracking
- Status-based retention (7d success, 14d failure, 90d quarantine)
- Workspace auto-archiving for forensic preservation

**Trigger for Phase 2 implementation**:
- Operator frequently tests untrusted scripts
- MESO deployed in high-exposure environments (many 3rd party installers)
- Developing script distribution tools (MESOcomplete installers)
- After 2-4 weeks validating Phase 1 in production

## Alternatives Considered

### Alternative A: Immediate Full Sandboxing
- **Pros**: Maximum security from day one, demonstrates container capability
- **Cons**:
  - Premature complexity (5 hours implementation + testing)
  - No validated need yet (operator hasn't requested script testing)
  - Violates MESO philosophy (build when needed, not speculatively)
  - Container overhead for every download (even benign API calls)

### Alternative B: Allowlist-Only Model (No Deny-List)
- **Pros**: Explicit permission grants (principle of least privilege)
- **Cons**:
  - Breaks existing workflows (every curl requires explicit allowlist entry)
  - False negatives (forgetting to block dangerous patterns)
  - Maintenance burden (allowlist grows unbounded)
  - User friction (constant permission prompts for routine tasks)

### Alternative C: AI-Driven Risk Assessment (No Fixed Rules)
- **Pros**: Context-aware decisions (distinguish malicious from benign)
- **Cons**:
  - Unreliable (AI can be fooled by obfuscation)
  - No audit trail (why was this allowed/blocked?)
  - Violates operator accountability (L1 decisions offloaded to AI)
  - Prompt injection risk (malicious content directs AI to approve)

### Alternative D: Full Ban on Script Downloads
- **Pros**: Zero risk from script execution
- **Cons**:
  - Breaks legitimate needs (installing tools, operon spores)
  - Forces workarounds (manual downloads outside MESO = less safe)
  - Incompatible with MESOcomplete vision (edge device bootstrapping)

## Rationale

**Phased approach chosen because**:

1. **Defense-in-depth**: Multiple barriers (deny-list → zooid rules → L1 escalation → optional sandboxing)
2. **Fail-safe defaults**: Block dangerous patterns immediately (Phase 1), add sandboxing when needed (Phase 2)
3. **Pragmatic incrementalism**: Deliver protection today, design infrastructure for tomorrow
4. **Operator accountability**: L1 approval required at all phases (human final authority)
5. **MESO philosophy alignment**:
   - Military background → layered defenses
   - Craft orientation → build only what's needed
   - Symbiosis evolution → adapt based on operational lessons

**Why deny-list over allowlist**:
- MESO uses deny-list model globally (see zooids/04-security.md deny patterns)
- Curl has legitimate uses (API testing, data acquisition) that shouldn't require explicit grants
- Deny-list targets dangerous combinations (`curl | bash`) without blocking safe patterns
- Allowlist would require enumerating every valid curl use case (intractable)

**Why defer Phase 2**:
- No current operational need (operator hasn't requested script testing)
- Design complete (5-hour implementation path defined)
- Can validate Phase 1 effectiveness before committing to containers
- Avoids premature infrastructure complexity

## Consequences

### Immediate (Phase 1)
✅ **Protections added**:
- Blocks interpreter piping (bash, sh, python)
- Prevents certificate bypass (-k, --insecure, --no-check-certificate)
- Prevents HTTP downloads (enforces HTTPS)
- Expands secret detection (password, token files)

✅ **No workflow disruption**:
- API testing allowed (localhost, HTTPS with safety flags)
- File downloads allowed (just not direct piping)
- Legitimate script needs handled via safe download pattern

✅ **L1 escalation enforced**:
- Script downloads trigger operator approval
- Verification plan required (SHA256/GPG + manual inspection)
- API calls and data retrieval stay L2 (no escalation)

⚠️ **Tradeoffs accepted**:
- Deny-list is not exhaustive (new bypass techniques may emerge)
- Manual inspection required (operator time investment)
- No automation for bulk script downloads (intentional friction)

### Future (Phase 2, When Implemented)
✅ **Additional protections**:
- Network isolation (--network none)
- Filesystem isolation (read-only root, ephemeral containers)
- Resource limits (512MB RAM, 1 CPU core)
- Forensic capture (execution logs, exit codes, environment snapshots)

⚠️ **New complexity**:
- Podman dependency (rootless containers)
- Manifest tracking (scratchpad/sandbox/ integration)
- Cleanup workflows (TTL enforcement, workspace archiving)
- Container maintenance (image updates, security patches)

⚠️ **Operational overhead**:
- Sandbox output review before promotion
- Manifest auditing on session start/end
- Retention policy tuning (7d/14d/90d TTLs)

### Long-term Commitments
- **Template distribution**: safe-download.sh maintained in framework/templates/scripts/
- **Trust domain model**: Three-tier architecture (verified, known-good, untrusted)
- **Session-only cache**: No persistent approval cache (security over convenience)
- **Operator-editable policies**: trust-domains.json, .workspace.conf [sandbox] section

## Review Date

**Phase 1**: 2026-03-07 (30 days) - validate deny-list effectiveness, check for false positives

**Phase 2 decision**: 2026-03-07 (30 days) - assess whether container sandboxing is operationally needed

**Trust domain model**: 2026-05-07 (90 days) - evaluate whether three-tier model is appropriate or needs refinement

**Retention policy**: When Phase 2 implemented - tune TTLs based on actual usage patterns
