---
name: scratchpad
description: >
  This skill should be used when staging work-in-progress code, persisting
  intermediate outputs across sessions, managing agent output staging areas,
  creating pre-merge snapshots, or cleaning up stale scratchpad items.
  MESO operon (Cystozooid — Storage & Buoyancy).
---

# Scratchpad — Cystozooid (Storage & Buoyancy)

Persistent staging area for work that outlives a session but isn't ready for the project.
Prevents loss of intermediate work (code in session-scoped temp dirs disappears).

## Scratchpad Locations

| Scope | Location | Use |
|-------|----------|-----|
| Global | `~/.claude/scratchpad/` | Cross-project staging, research notes, reusable fragments |
| Project | `<project>/.claude/scratchpad/` | Project-specific WIP code |

### Directory Structure

```
.claude/scratchpad/
  MANIFEST.md              # What's here, why, where it's going
  agent-output/            # Staging area for background agent deliverables
  snapshots/               # Pre-operation state snapshots for recovery
```

## The Manifest

Every scratchpad MUST have a `MANIFEST.md`. This is the memory of the scratchpad.
Update it every time you add, promote, or delete an item.

```markdown
# Scratchpad Manifest

| File | Purpose | Target | Status | Created | Last Touched |
|------|---------|--------|--------|---------|--------------|
| example.html | Tier 3 hex animation | templates/hexagon-bg.html | draft | 2026-02-03 | 2026-02-03 |
```

**Status values:**
- `draft` — work in progress, not ready for review
- `review` — complete, awaiting operator review before promotion
- `promoted` — graduated to project (delete the scratchpad copy)
- `stale` — untouched for 2+ sessions, needs decision

**Rules:**
- Never add a file without updating the manifest
- Never delete a file without updating the manifest
- The manifest is the source of truth — if it's not in the manifest, it doesn't exist

## Agent Staging Area

Background agents SHOULD write to the scratchpad instead of project files.
This eliminates permission failures and adds a review gate.

### Agent Output Protocol

1. **Before dispatch:** set the agent's output target to `.claude/scratchpad/agent-output/<task-name>/`
2. **Agent writes:** to the scratchpad path (no project file conflicts)
3. **On completion:** orchestrator reviews the output in place
4. **If good:** promote to project location, update manifest
5. **If bad:** fix in place or re-dispatch, scratchpad copy is harmless

### Prompt Template for Agent Scratchpad Targeting

Include in every write-capable agent prompt:
```
Write your output to: <project>/.claude/scratchpad/agent-output/<task-name>/
Do NOT write directly to project files.
```

## Snapshots

Before risky operations (large refactors, multi-file changes, untested transformations),
snapshot the affected files to `.claude/scratchpad/snapshots/`.

### Snapshot Protocol

1. Copy affected files to `snapshots/<date>-<description>/`
2. Note in manifest: what was snapshotted and why
3. After the operation succeeds and is verified: delete the snapshot
4. After the operation fails: restore from snapshot, then delete it

Snapshots are cheaper than git stashes and don't pollute the reflog.

## Lifecycle Rules

Items must move through the lifecycle. The scratchpad is a staging area, not storage.

```
draft → review → promoted (move to project) → delete from scratchpad
                → deleted (not needed)       → delete from scratchpad
```

### Hard Rules

- **Nothing lives in the scratchpad indefinitely.** Every item has a target destination or a deletion date.
- **Stale after 2 sessions** without activity. Flag in manifest as `stale`.
- **Dead after 1 week** without explicit justification. Delete or promote.
- **Promoted items get deleted** from scratchpad. Don't keep copies.

### Session Start Protocol

At the start of every session, if a scratchpad exists:
1. Read the manifest
2. Report stale items to the operator
3. Ask: promote, continue working, or delete?

### Session End Protocol

At the end of every session, if scratchpad items were touched:
1. Update manifest with current status and `Last Touched` date
2. Reference scratchpad items in the handoff note
3. Flag anything that should be promoted before next session

## Git Integration

**Track the manifest, ignore the contents.**

Add to project `.gitignore`:
```
# Scratchpad: track manifest, ignore working files
.claude/scratchpad/*
!.claude/scratchpad/MANIFEST.md
```

The manifest persists in git history (so future sessions know what was staged).
The actual files don't clutter commits, diffs, or status.

## Integration With Workspace Operon

The workspace operon extends scratchpad with lifecycle management:

- **Scratchpad lifecycle**: draft → review → promoted/deleted (unchanged)
- **On session end**: Archive-worthy items auto-archived to workspace (if retention enabled)
- **Scratchpad manifest**: Track promotion destination (workspace/artifacts/ or project files)

**No breaking changes** - existing scratchpad workflows continue to work. Workspace is opt-in extension.

**Promotion decision tree:**

```
Is this reusable across projects?
├─ Yes → Promote to workspace artifacts
│         └─ Symlink to project if needed
└─ No  → Promote directly to project files
          └─ Delete from scratchpad
```

**Updated manifest format** (optional, for workspace integration):

```markdown
| File | Purpose | Target | Status | Created | Last Touched |
|------|---------|--------|--------|---------|--------------|
| api-auth.md | FastAPI auth research | workspace/artifacts/research | promoted | 2026-02-06 | 2026-02-06 |
| docker-setup.sh | Docker install script | project/scripts/ | promoted | 2026-02-05 | 2026-02-06 |
```

## Integration With Other Operons

| Operon | Integration |
|--------|-------------|
| **Workspace** | Scratchpad is tier 1 (ephemeral). Workspace provides tier 2 (archive) and tier 3 (artifacts). Promote reusable items. |
| **Orchestration** | Agents target scratchpad instead of project files. Orchestrator promotes after review. |
| **Recovery** | Snapshots provide rollback points for risky operations. Recovery operon references snapshots. |
| **Handoff** | Session-end handoff includes scratchpad inventory. Next session starts by checking manifest. |
| **Auditing** | Stale scratchpad items flagged during session audit. Dead items (>1 week) flagged for deletion. |
| **Evolution** | AAR drafts can stage in scratchpad before finalizing in the genome. |

## Cleanup Commands

When cleaning the scratchpad:
- Promote ready items to their target locations
- Delete stale items after operator confirmation
- Clear empty `agent-output/` subdirectories
- Update manifest to reflect current state
- Verify no orphaned files (files present but not in manifest)
