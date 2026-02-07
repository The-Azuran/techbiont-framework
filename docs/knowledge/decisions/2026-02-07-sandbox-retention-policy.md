---
type: proposal
title: "Status-Based Sandbox Retention with Workspace Auto-Archiving"
date: 2026-02-07
project: techbiont-framework
domain: [security, storage, lifecycle, meso]
status: proposed
author: ai-research
awaiting-decision: valis
tags: [sandbox, retention, ttl, forensics, workspace]
related-files:
  - operons/scratchpad/SKILL.md
  - operons/workspace/SKILL.md
  - docs/knowledge/decisions/2026-02-07-curl-security-architecture.md
---

**STATUS**: Research proposal awaiting operator review and decision.
**Operator requirement**: "Research to find the optimal options then come back to me"

## Context

As part of container sandboxing design (Phase 2 of curl security enhancement), operator asked:

> "Research to find the optimal options then come back to me"

Regarding: **How long should sandbox execution outputs be retained? When should they be deleted?**

**Competing concerns**:
- **Forensic value**: Keep outputs for debugging, root-cause analysis, security audit
- **Disk space**: Sandbox outputs accumulate (logs, stderr, environment snapshots)
- **Operator review**: Some outputs need manual inspection before promotion/deletion
- **Automation**: Manual cleanup doesn't scale, but automated deletion risks losing evidence

**Constraints**:
- Must integrate with existing MESO operons (scratchpad, workspace)
- Must balance forensic value vs disk space
- Must support operator review workflow (sandbox → promote or delete)
- Must distinguish successful vs failed vs security-flagged executions
- Must align with L1/L2 autonomy (cleanup requires approval)

## Proposed Approach

**Recommendation: Implement status-based TTL retention with workspace auto-archiving:**

### Retention Policy by Execution Status

| Status | TTL | Cleanup Trigger | Archive Destination |
|--------|-----|----------------|---------------------|
| **Success** | 7 days | Time-based | Workspace archive (if approved) |
| **Failure** | 14 days | Time-based | No (logs only, for debugging) |
| **Quarantine** | 90+ days (∞ if security-flagged) | Manual only | Workspace artifacts (immutable) |
| **Unreviewed** | 3 days | Nag operator | Conditional (ask operator) |
| **Promoted** | Delete (moved) | Immediate | Workspace artifacts or project files |

### Status Values (Lifecycle Stages)

- `draft` - Execution captured, not yet reviewed
- `review` - Waiting operator approval before promoting to production
- `approved` - Passed review, safe to promote or archive
- `failed` - Execution failed, keep for debugging (14d window)
- `quarantine` - Security concern, indefinite retention for audit
- `promoted` - Moved to production/workspace (delete local copy)
- `deleted` - Cleaned up after TTL or operator decision

### Manifest Tracking

**File**: `.claude/scratchpad/sandbox/MANIFEST.md`

```markdown
| Exec ID | Source | Status | Exit | Result | Created | Reviewed | Keep Until | Promoted To | Notes |
|---------|--------|--------|------|--------|---------|----------|------------|-------------|-------|
| exec-001 | https://example.com/script.sh | approved | 0 | SUCCESS | 2026-02-07 | 2026-02-07 | 2026-02-14 | - | Safe, pending promotion |
| exec-002 | malware.sh | quarantine | 1 | SECURITY | 2026-02-06 | 2026-02-06 | ∞ | workspace/artifacts/security | Credential theft attempt |
| exec-003 | test.sh | failed | 127 | FAILED | 2026-02-06 | 2026-02-07 | 2026-02-20 | - | Command not found |
```

### Workspace Integration (Tier-2 Storage)

**Auto-archive protocol** (on session end):
1. Collect sandbox outputs marked "approved" or "promoted"
2. Archive to `~/.claude/workspace/archive/YYYY-MM/session-{uuid}/sandbox/`
3. Index in SQLite for forensic search (FTS5)
4. Apply workspace archive TTL (30 days, configurable)
5. Delete local copies (moved, not copied)

**Quarantine handling**:
- Move to `~/.claude/workspace/artifacts/security/sandbox-quarantine/`
- Mark immutable (chmod 600, append-only audit log)
- Never auto-delete (requires manual operator decision)
- Index with security tag for audit queries

### Configuration (`.claude/workspace/.workspace.conf` extension)

```toml
[sandbox]
# TTL by status
success_ttl_days = 7
failure_ttl_days = 14
quarantine_ttl_days = 90
unreviewed_ttl_days = 3

# Size management
max_sandbox_size_mb = 200
auto_compress_after_days = 3

# Cleanup behavior
auto_archive_at_session_end = true
manual_approval_required = true
cleanup_unreviewed_on_session_end = false  # Ask operator first
```

## Alternatives Considered

### Alternative A: Fixed TTL for All Executions
- **Pros**: Simplest to implement (one TTL value, time-based cleanup)
- **Cons**:
  - No distinction between success/failure/security (forensic value varies)
  - Failed executions deleted too early (lose debugging context)
  - Security-flagged items deleted automatically (compliance risk)
  - Successful executions kept too long (disk waste)

### Alternative B: Manual-Only Cleanup (No Automation)
- **Pros**: Operator reviews every deletion (maximum control)
- **Cons**:
  - Doesn't scale (manual review for every execution = operator burden)
  - Disk space grows unbounded (operator forgets to clean up)
  - No forcing function (stale outputs accumulate indefinitely)

### Alternative C: Size-Based Only (No Time Component)
- **Pros**: Disk space bounded (delete oldest when limit reached)
- **Cons**:
  - No predictable retention (executions deleted unpredictably)
  - Low-disk environments delete too aggressively (lose forensics)
  - High-disk environments accumulate stale outputs (never hit limit)
  - Operator can't reason about retention (no guaranteed window)

### Alternative D: Immediate Archive to Workspace (No Scratchpad)
- **Pros**: Centralized storage (everything in workspace from start)
- **Cons**:
  - No review stage (scratchpad is for draft/review before promotion)
  - Pollutes workspace with unreviewed outputs
  - Violates MESO operon separation (scratchpad = ephemeral, workspace = curated)
  - No ephemeral storage tier (everything committed immediately)

### Alternative E: Persistent Storage for All (No Deletion)
- **Pros**: Maximum forensic preservation (never lose evidence)
- **Cons**:
  - Disk space grows unbounded (unsustainable)
  - No incentive to review outputs (accumulation without curation)
  - Stale data pollution (old outputs mixed with current)
  - Violates MESO lifecycle model (draft → review → promote/delete)

## Rationale

**Status-based TTL chosen because**:

1. **Reflects forensic value gradients**:
   - Success (7d): Low value after review (safe to delete)
   - Failure (14d): High value for debugging (extended window)
   - Quarantine (90d+): Maximum value for audit (indefinite if security-relevant)
   - Unreviewed (3d): Nag operator (don't accumulate unreviewed)

2. **Balances forensic value vs disk space**:
   - Short TTL for low-value items (successes after review)
   - Long TTL for high-value items (failures, security)
   - Compression for old outputs (gzip after 3 days)
   - Size limit enforces upper bound (200MB sandbox directory)

3. **Integrates with MESO operons**:
   - Scratchpad model (draft → review → promoted/deleted)
   - Workspace tier-2 storage (archive approved items)
   - Existing TTL patterns (scratchpad 2 sessions, workspace 30 days)
   - SQLite indexing (forensic search capability)

4. **Supports operator workflow**:
   - Unreviewed items nagged after 3 days (forcing function)
   - Review stage before cleanup (manual approval gate)
   - Promotion moves files (no duplication)
   - Quarantine preserved indefinitely (audit compliance)

5. **Research findings alignment**:
   - Container systems: Ephemeral volumes + artifact capture (design pattern)
   - Testing frameworks: Different retention for pass/fail (forensic distinction)
   - Workspace operon: Already implements 30-day archive + auto-cleanup (extend to sandbox)
   - Scratchpad operon: Already implements status-based lifecycle (reuse pattern)

**Why 7d success / 14d failure / 90d quarantine**:
- **7 days**: One week for operator to review successful outputs and promote
- **14 days**: Two weeks for root-cause analysis of failures (standard debug window)
- **90 days**: Three months for security audit (compliance standard, extendable to ∞)
- **3 days unreviewed**: Nag operator (don't let unreviewed accumulate)

**Why workspace auto-archiving**:
- Promotes ephemeral → permanent lifecycle (scratchpad → workspace)
- Leverages existing workspace retention policies (30d archive)
- SQLite indexing enables cross-session forensic search
- Operator reviews before archive (promoted = reviewed)

**Why manual approval for cleanup**:
- L1 accountability (security-critical decisions require operator)
- Prevents accidental loss (operator sees what will be deleted)
- Audit trail (deletions logged with reason)
- Operator can override (extend TTL, mark quarantine)

## Consequences

### Forensic Capabilities

✅ **Debugging support**:
- Failed executions kept 14 days (root-cause analysis window)
- stdout/stderr logs captured
- Exit codes and duration tracked
- Environment snapshots available (scrubbed of secrets)

✅ **Security audit**:
- Quarantine items preserved indefinitely
- Immutable audit log (append-only)
- Indexed for search (SQLite FTS5)
- Promotion decisions tracked (who, when, why)

✅ **Cross-session search**:
- Workspace archive indexed (30 days)
- Full-text search on outputs
- Query by status, source, date, exit code
- Related executions linkable (same source, different times)

⚠️ **Blind spots**:
- Successful executions deleted after 7 days (operator must review before TTL)
- Unreviewed items nagged but not auto-deleted (accumulate if ignored)
- Compressed outputs (gzip after 3d) require decompression for review

### Operational Impact

✅ **Disk space management**:
- Bounded growth (200MB sandbox directory, 30-day archive)
- Compression reduces footprint (gzip after 3d, ~70% reduction)
- Cleanup automation (time-based + size-based triggers)
- Workspace archive auto-cleanup (existing mechanism)

✅ **Operator workflow**:
- Session-start audit (report unreviewed items older than 3 days)
- Session-end archive (move approved items to workspace)
- Cleanup approval gate (review candidates before deletion)
- Promotion workflow (sandbox → project files or workspace artifacts)

⚠️ **Operational overhead**:
- Manifest maintenance (status updates, notes, promotion tracking)
- Cleanup approval prompts (every session end if candidates exist)
- Quarantine decisions (operator classifies security-relevant items)
- Configuration tuning (TTL values may need adjustment per deployment)

### Integration Points

**Scratchpad operon**:
- Extend with `sandbox/` subdirectory
- Reuse manifest structure (status values, lifecycle tracking)
- Session-end cleanup triggers

**Workspace operon**:
- Add sandbox auto-archive protocol
- Extend `.workspace.conf` with `[sandbox]` section
- SQLite schema extension (executions table, audit log)
- Artifact promotion workflow (sandbox → artifacts/)

**Auditing operon**:
- Session-start checklist (report unreviewed sandbox items)
- Session-end checklist (archive approved, report cleanup candidates)
- Cleanup verification (confirm deletions logged)

**Security zooid**:
- Reference sandbox retention policy
- Document quarantine criteria
- Link to safe download workflow

### Long-term Commitments

**Configuration maintenance**:
- `.workspace.conf` includes `[sandbox]` section (distributed via install.sh)
- Operator can tune TTL values per deployment
- Default values validated via operational experience

**Manifest schema**:
- Stable format (breaking changes avoided)
- Versioned (manifest version field for migration)
- Documented in genome or schemas/

**Cleanup automation**:
- Time-based triggers (nightly or session-end)
- Size-based triggers (when max_sandbox_size_mb exceeded)
- Manual approval gate (never auto-delete without operator review)

**Archive search**:
- SQLite FTS5 indexing (full-text search on outputs)
- Retention in workspace archive (30 days post-archiving)
- Cross-session queries (find all executions from source X)

## Review Date

**2026-03-07** (30 days, when Phase 2 implemented):
- Validate TTL values (7d/14d/90d appropriate for actual usage?)
- Check disk space impact (200MB limit sufficient?)
- Assess operator friction (too many approval prompts?)
- Tune compression trigger (3 days optimal or adjust?)

**Re-evaluate if**:
- Disk space exceeded frequently (reduce TTLs or increase compression)
- Operator misses review window (extend success TTL from 7d)
- Debugging hampered by 14d failure window (extend or make configurable)
- Quarantine grows unbounded (add size limit with manual cleanup)

**Metrics to track**:
- Executions per status (how many success/failure/quarantine?)
- Average time to review (is 3d unreviewed nag effective?)
- Disk space usage (average, peak, cleanup effectiveness)
- Promotion rate (% of executions promoted vs deleted)
