# Migrating to MESO Workspace

If you've been using the scratchpad operon, the workspace operon extends it with persistent artifact storage and lifecycle management.

## What's New

The workspace adds two new lifecycle tiers beyond scratchpad:

1. **Archive** (time-limited) — Session artifacts, 30-day TTL, searchable
2. **Artifacts** (permanent) — Git-backed reusable knowledge

```
Before:  Scratchpad → Project (or deleted)
After:   Scratchpad → Archive → Artifacts → Project
                  └─────────┘
                  workspace operon
```

## What Changes

### New Capabilities

**Auto-archiving** (opt-in):
- Sessions automatically archived on end
- Includes handoff notes, task lists, scratchpad items
- Searchable via SQLite full-text search

**Artifact promotion**:
- Promote scratchpad items to long-term storage
- Git-backed version control (global workspace)
- Cross-project sharing via symlinks

**Retention policies**:
- Configurable TTL for archives (default 30 days)
- Automatic cleanup of old archives
- Warnings for unused artifacts (180+ days)

**Search**:
- SQLite FTS5 full-text search
- Filter by type, domain, tags, date
- Find past solutions across sessions

### What Stays the Same

**Scratchpad workflow unchanged**:
- `draft → review → promoted/deleted` (same as before)
- Agent output staging (same location)
- Snapshot protocol (same process)
- Manifest protocol (same format, optional new fields)

**No breaking changes**:
- Existing scratchpad files continue to work
- Workspace is opt-in extension
- Auto-archiving disabled by default on first install

## Installation

If you already have MESO installed:

```bash
cd ~/path/to/techbiont-framework
git pull
./install.sh --update
```

This will:
1. Create `~/.claude/workspace/` directory structure
2. Initialize git repository in global workspace
3. Install SQLite index (if sqlite3 available)
4. Install retention policy config template
5. Install workspace operon to `~/.claude/skills/workspace/`

**No impact on existing scratchpad files.**

## Configuration

Edit `~/.claude/workspace/.workspace.conf` to customize:

```toml
[auto_archive]
enabled = true              # Auto-archive sessions on end
on_session_end = true
include_agent_output = true
min_file_count = 5          # Minimum files to trigger archiving

[retention]
archive_ttl_days = 30       # Delete archives after 30 days

[search]
fts_enabled = true          # Enable SQLite full-text search
```

## Usage Examples

### Promote Reusable Code

**Before** (scratchpad only):
```
1. Create docker-compose.yml in scratchpad
2. Test in current project
3. Promote to project files
4. Need same setup in other project → recreate from scratch
```

**After** (with workspace):
```
1. Create docker-compose.yml in scratchpad
2. Test in current project
3. Promote to workspace artifacts: /workspace promote scratchpad/docker-compose.yml --type template
4. Need same setup in other project → /workspace link {artifact-id} --to other-project
```

### Search Past Sessions

**Before**:
```
"Where did I put that FastAPI auth research from 2 months ago?"
→ grep through git history, hope you committed it
```

**After**:
```
/workspace search "fastapi authentication" --type research
→ Instant results from all past sessions, even if never committed
```

### Automatic Session Continuity

**Before**:
```
Session ends → handoff note in .claude/handoff.md
Next session → read handoff, manually recreate context
```

**After** (with auto-archive enabled):
```
Session ends → auto-archived to workspace with all context
Next session → workspace reports last 3 sessions, pending promotions
```

## Migration Workflow

### Step 1: Install (already done above)

### Step 2: Enable Auto-Archiving (optional)

Edit `~/.claude/workspace/.workspace.conf`:

```toml
[auto_archive]
enabled = true
```

### Step 3: Promote Existing Scratchpad Items (optional)

If you have reusable items in scratchpad:

```bash
# In a Claude Code session
/workspace promote scratchpad/existing-item.py --type code --domain web
```

### Step 4: Configure Retention Policies (optional)

Adjust TTL and cleanup rules in `.workspace.conf`:

```toml
[retention]
archive_ttl_days = 60       # Keep archives longer
artifact_unused_warning_days = 365  # Warn about stale artifacts after 1 year
```

## SQLite Requirement

**Workspace indexing requires SQLite.**

Check if installed:
```bash
sqlite3 --version
```

Install if missing (Fedora):
```bash
sudo dnf install sqlite
```

**If SQLite not installed:**
- Workspace directory structure still created
- Manual file organization still works
- Search falls back to grep (slower)
- No automatic indexing

## Operon Integration

Workspace integrates with existing operons:

**Auditing** — Session audit now includes workspace checks:
- Scratchpad items promoted or deleted
- Retention policies enforced
- Symlinks validated

**Evolution** — Pattern extraction now searches workspace:
- `/workspace search` finds related past research
- Aggregate findings before extracting patterns

**Knowledge** — Promote workspace artifacts to knowledge base:
- `/workspace promote {id} --to-knowledge`
- Copies to `docs/knowledge/`, keeps original in workspace

## FAQ

**Q: Do I have to use workspace?**
A: No, it's opt-in. Scratchpad continues to work exactly as before.

**Q: What happens to my existing scratchpad files?**
A: Nothing. Workspace doesn't touch existing scratchpad files. You can promote them to workspace when ready.

**Q: Do I need to enable auto-archiving?**
A: No. You can use workspace for manual artifact promotion without auto-archiving.

**Q: Can I disable workspace after installing?**
A: Yes. Just don't invoke workspace commands. It's a passive extension.

**Q: What if I don't have SQLite?**
A: Workspace still works for manual file organization. Search falls back to grep. Install sqlite3 for full-text search.

**Q: Will workspace fill up my disk?**
A: Retention policies prevent unbounded growth. Default: archives deleted after 30 days. Configurable.

**Q: Can I share workspace artifacts between machines?**
A: Global workspace is git-backed. You can push to a remote repo and pull on other machines. Add `.index.db` to `.gitignore` to avoid conflicts.

**Q: What about security? Will my scratchpad items leak to git?**
A: Archives are in `.gitignore`. Only artifacts (things you explicitly promote) are git-tracked. Scratchpad manifest protocol warns against committing secrets.

## Rollback

If you want to remove workspace (though you don't need to):

```bash
rm -rf ~/.claude/workspace
rm -rf ~/.claude/skills/workspace
```

This won't affect scratchpad or any other operons.

## Next Steps

1. **Start a session** — Workspace operon auto-loads when you invoke workspace commands
2. **Try a search** — `/workspace search "<topic>"` (works even on fresh install)
3. **Promote an artifact** — `/workspace promote scratchpad/example.py --type code`
4. **Enable auto-archiving** — Edit `.workspace.conf` when ready

See the full workspace operon (`~/.claude/skills/workspace/SKILL.md`) for comprehensive usage guidance.
