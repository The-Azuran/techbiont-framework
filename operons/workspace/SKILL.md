---
name: workspace
description: >
  This skill should be used when managing persistent artifacts, promoting
  scratchpad items to long-term storage, searching workspace history,
  auto-archiving sessions, configuring retention policies, querying artifact
  indexes, or creating cross-project reusable knowledge.
  MESO operon (Cystozooid Evolved — Storage with Memory).
---

# Workspace — Cystozooid Evolved (Storage & Memory)

Persistent artifact storage with lifecycle management, extending the scratchpad operon.
Prevents knowledge loss, enables artifact reuse, and provides temporal organization.

## The Problem

Without persistent workspace:
1. **Knowledge loss** — research and reusable artifacts deleted after scratchpad TTL
2. **Poor discoverability** — no way to search past sessions for that "docker compose setup"
3. **Duplication** — reusable artifacts recreated across projects
4. **Session amnesia** — valuable intermediate work either promoted immediately or lost
5. **Cross-project isolation** — insights don't transfer

## The Solution

Three-tier lifecycle architecture:

```
Scratchpad (ephemeral) → Archive (time-limited) → Artifacts (permanent)
```

## Architecture

### Spatial: Hybrid Global + Project

| Location | Scope | Git | Purpose |
|----------|-------|-----|---------|
| `~/.claude/workspace/` | Global | Yes | Cross-project artifacts, version controlled |
| `<project>/.claude/workspace/` | Project | No | Project-specific artifacts, symlinks to global |
| `~/.claude/scratchpad/` | Global | No | Ephemeral staging (existing) |
| `<project>/.claude/scratchpad/` | Project | No | Project WIP (existing) |

### Temporal: Three Lifecycle Stages

#### 1. Scratchpad (Ephemeral)

**Location**: `.claude/scratchpad/`
**Duration**: Until promoted or stale (2 sessions / 1 week)
**Purpose**: Active work-in-progress
**Governed by**: Scratchpad operon (unchanged)

Use scratchpad for:
- Code you're actively working on
- Agent outputs pending review
- Pre-merge snapshots
- Experiments that may fail

#### 2. Archive (Time-Limited)

**Location**: `.claude/workspace/archive/YYYY-MM/session-{uuid}/`
**Duration**: 30 days (configurable)
**Purpose**: Searchable session history
**Indexed**: SQLite full-text search

Archives contain:
- Session handoff notes
- Promoted scratchpad items
- Agent output (if configured)
- Task lists and summaries

**Automatic archiving** (if `auto_archive.enabled = true`):
- Triggered on session end
- Only if `min_file_count` threshold met
- Includes items marked `review` or `promoted` in scratchpad manifest

#### 3. Artifacts (Permanent)

**Location**: `.claude/workspace/artifacts/{type}/`
**Duration**: Permanent (until explicitly archived/deleted)
**Purpose**: Reusable cross-project knowledge
**Version control**: Git-backed (global only)

Artifact types:
- `code/` — reusable code snippets, templates, utilities
- `research/` — investigation notes, API studies, comparisons
- `templates/` — file templates, boilerplate, scaffolds
- `configs/` — configuration files, setup scripts

### Directory Structure

```
~/.claude/workspace/
  MANIFEST.md                # Workspace statistics and recent activity
  .workspace.conf            # Retention policies and lifecycle config
  .index.db                  # SQLite index (full-text search)
  .gitignore                 # Track artifacts, ignore archives/index
  artifacts/
    code/
      {uuid}.md              # Artifact with YAML frontmatter
    research/
    templates/
    configs/
  archive/
    2026-02/
      session-abc123/
        MANIFEST.md          # Session metadata
        handoff.md           # Session handoff note
        files/               # Archived files
```

## The Manifest

**Global workspace manifest** (`~/.claude/workspace/MANIFEST.md`):

```markdown
# Workspace Manifest (Global)

## Statistics
- Artifacts: 42
- Archives: 18
- Symlinks: 7

## Recent Activity
| Date | Action | Artifact | Type |
|------|--------|----------|------|
| 2026-02-06 | promote | docker-compose-pattern | template |
| 2026-02-06 | archive | session-def456 | - |
| 2026-02-05 | link | api-auth-research | research |
```

**Update on every workspace operation.**

## Artifact Structure

Every artifact MUST have YAML frontmatter with metadata:

```markdown
---
id: "550e8400-e29b-41d4-a716-446655440000"
type: code
title: "Docker Compose FastAPI + PostgreSQL"
description: "Production-ready docker-compose setup for FastAPI with PostgreSQL, Nginx, and Let's Encrypt"
created: 2026-02-06
updated: 2026-02-06
domain: [web, devops]
tags: [docker, fastapi, postgresql, nginx]
promoted_from: scratchpad
source_session: "session-abc123"
related_artifacts: []
status: active
---

# Docker Compose FastAPI + PostgreSQL

[Content follows...]
```

**Metadata fields:**
- `id` — UUID (generate with `uuidgen` or Python `uuid.uuid4()`)
- `type` — `code|research|template|config`
- `title` — Human-readable title
- `description` — What this is and why it exists
- `domain` — `[web, gis, game-dev, etc]`
- `tags` — `[technology, pattern, use-case]`
- `promoted_from` — `scratchpad|archive|manual`
- `source_session` — Session ID where this was created
- `related_artifacts` — List of related artifact IDs
- `status` — `active|archived|deprecated`

## Retention Policies

Configured in `.claude/workspace/.workspace.conf` (TOML format):

```toml
[retention]
archive_ttl_days = 30
archive_promotion_threshold = 3
archive_size_limit_mb = 100

[auto_archive]
enabled = true
on_session_end = true
include_agent_output = true
include_snapshots = false
min_file_count = 5

[git]
enabled = true
auto_commit_artifacts = true

[search]
fts_enabled = true
index_file_contents = true
```

## Lifecycle Workflows

### Session End: Automatic Archiving

If `auto_archive.enabled = true` and `min_file_count` threshold met:

1. **Collect session artifacts**:
   - Scratchpad items marked `review` or `promoted`
   - Agent outputs from `scratchpad/agent-output/`
   - Handoff note (`.claude/handoff.md`)
   - Task list snapshot

2. **Create archive directory**:
   ```bash
   mkdir -p ~/.claude/workspace/archive/YYYY-MM/session-{uuid}/files/
   ```

3. **Copy artifacts**:
   - Create `MANIFEST.md` with session metadata
   - Copy `handoff.md`
   - Copy collected files to `files/`

4. **Index in SQLite**:
   ```python
   import sqlite3
   conn = sqlite3.connect('~/.claude/workspace/.index.db')
   conn.execute("""
       INSERT INTO sessions (id, project_path, started_at, ended_at, archived_at, artifact_count, summary)
       VALUES (?, ?, ?, ?, ?, ?, ?)
   """, (session_id, project_path, start_time, end_time, now, count, summary))

   # Index each file with full-text content
   for file in files:
       conn.execute("""
           INSERT INTO artifacts (id, path, type, title, description, created_at, updated_at, source_session)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
       """, (uuid, path, 'archive', title, desc, now, now, session_id))
   ```

5. **Check promotion triggers**:
   - Query: files referenced in 3+ sessions
   - Auto-promote to `artifacts/` if threshold met
   - Generate UUID and frontmatter

6. **Enforce retention**:
   - Delete archives older than `archive_ttl_days`
   - Log deletions to `retention_log` table

7. **Update workspace manifest**:
   - Increment statistics
   - Add activity log entry

**This protocol is automatic if configured, but the AI executes it based on this guidance.**

### Session Start: Workspace Context

At session start, if workspace exists:

1. **Scratchpad audit** (existing scratchpad operon protocol)

2. **Workspace context** (new):
   ```
   Workspace Status:
   - Last 3 archived sessions: 2026-02-05, 2026-02-04, 2026-02-03
   - Artifacts pending promotion: 2 (referenced 3+ times)
   - Archives nearing expiration: 1 (7 days remaining)
   ```

3. **Retention policy check**:
   - Report archives nearing TTL expiration (< 7 days)
   - Report unused artifacts (180+ days since last access)

### Manual Promotion: Scratchpad → Artifacts

During a session, to promote a scratchpad item:

**Protocol:**

1. **Ask operator for metadata**:
   - Type? (`code|research|template|config`)
   - Domain? (`web`, `gis`, etc.)
   - Tags? (technology keywords)
   - Title and description?

2. **Generate artifact**:
   ```bash
   UUID=$(uuidgen)
   cp scratchpad/item.py workspace/artifacts/code/${UUID}.md
   ```

3. **Add YAML frontmatter** (use template at `templates/workspace-artifact.template.md`):
   ```yaml
   ---
   id: "{uuid}"
   type: code
   title: "{operator-provided}"
   description: "{operator-provided}"
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   domain: [web]
   tags: [fastapi, docker]
   promoted_from: scratchpad
   source_session: "{current-session-id}"
   related_artifacts: []
   status: active
   ---
   ```

4. **Index in SQLite**:
   ```python
   conn.execute("""
       INSERT INTO artifacts (id, path, type, title, description, created_at, updated_at, promoted_from, source_session, domain, tags, status)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
   """, (uuid, path, type, title, desc, now, now, 'scratchpad', session_id, domain_json, tags_json, 'active'))

   # Full-text index
   conn.execute("""
       INSERT INTO artifacts_fts (title, description, content, tags)
       VALUES (?, ?, ?, ?)
   """, (title, desc, file_content, tags_str))
   ```

5. **Git commit** (global workspace only):
   ```bash
   cd ~/.claude/workspace
   git add artifacts/code/${UUID}.md
   git commit -m "feat(workspace): promote code — {title}"
   ```

6. **Update scratchpad manifest**:
   - Set status to `promoted`
   - Delete scratchpad copy (no duplicates)

7. **Update workspace manifest**:
   - Increment artifact count
   - Add activity log entry

### Automatic Promotion: Archive → Artifacts

On session end, check for frequently-referenced files:

```python
# Query SQLite for files referenced 3+ times
results = conn.execute("""
    SELECT path, COUNT(*) as ref_count
    FROM artifacts
    WHERE promoted_from = 'archive'
    GROUP BY path
    HAVING ref_count >= ?
""", (threshold,)).fetchall()

for path, count in results:
    # Auto-promote with generated metadata
    promote_to_artifacts(path, auto_generated_metadata)
```

### Cross-Project Sharing: Symlinks

To use a global artifact in a project:

**Protocol:**

1. **Create symlink**:
   ```bash
   mkdir -p <project>/.claude/workspace/
   ln -s ~/.claude/workspace/artifacts/code/{uuid}.md <project>/.claude/workspace/{name}.md
   ```

2. **Track in SQLite**:
   ```python
   conn.execute("""
       INSERT INTO symlinks (id, artifact_id, target_path, created_at, project_path)
       VALUES (?, ?, ?, ?, ?)
   """, (symlink_uuid, artifact_id, target_path, now, project_path))
   ```

3. **Update project workspace manifest**:
   ```markdown
   ## Symlinks
   | Name | Source | Type |
   |------|--------|------|
   | docker-compose.md | ~/.claude/workspace/artifacts/.../uuid.md | template |
   ```

**Symlink validation** (session audit):
- Check for broken symlinks (target deleted)
- Report orphaned symlinks
- Clean up if configured

## Search and Query

### Full-Text Search

**Command syntax** (conceptual — AI executes):

```bash
# Full-text search
/workspace search "docker compose setup"

# Filtered search
/workspace search "API auth" --type research --domain web

# Search archives only
/workspace search "session notes" --scope archive --after 2026-01-01
```

**Implementation** (AI generates and executes):

```python
import sqlite3
import os

def search_artifacts(query, filters=None):
    conn = sqlite3.connect(os.path.expanduser('~/.claude/workspace/.index.db'))

    sql = """
    SELECT a.id, a.path, a.title, a.type, a.domain, a.created_at,
           snippet(artifacts_fts, -1, '<mark>', '</mark>', '...', 32) as snippet
    FROM artifacts a
    JOIN artifacts_fts fts ON a.rowid = fts.rowid
    WHERE artifacts_fts MATCH ?
    """

    params = [query]

    if filters:
        if filters.get('type'):
            sql += " AND a.type = ?"
            params.append(filters['type'])
        if filters.get('domain'):
            sql += " AND a.domain LIKE ?"
            params.append(f"%{filters['domain']}%")
        if filters.get('after'):
            sql += " AND a.created_at >= ?"
            params.append(filters['after'])

    sql += " ORDER BY rank LIMIT 20"

    results = conn.execute(sql, params).fetchall()
    conn.close()

    return results

# Execute and format results
results = search_artifacts("docker compose", {"type": "template"})
for r in results:
    print(f"{r['title']} ({r['type']}) — {r['snippet']}")
```

### Artifact Operations

**Show artifact details:**
```bash
/workspace show <artifact-id>
# Displays: full metadata, content preview, related artifacts, usage history
```

**Find related artifacts:**
```bash
/workspace related <artifact-id>
# Query: artifacts with overlapping tags/domain, linked in related_artifacts field
```

**Artifact history:**
```bash
/workspace history <artifact-id>
# Query git log for the artifact file (global workspace only)
```

**Workspace statistics:**
```bash
/workspace stats
# Shows: artifact count by type, archive count, total size, recent activity
```

**Implementation** (AI executes based on this guidance):

```python
def show_artifact(artifact_id):
    conn = sqlite3.connect('~/.claude/workspace/.index.db')
    result = conn.execute("""
        SELECT * FROM artifacts WHERE id = ?
    """, (artifact_id,)).fetchone()

    # Display metadata
    print(f"Title: {result['title']}")
    print(f"Type: {result['type']}")
    print(f"Domain: {result['domain']}")
    print(f"Tags: {result['tags']}")
    print(f"Created: {result['created_at']}")

    # Read and display content preview
    with open(result['path']) as f:
        content = f.read()
        print(f"\nContent preview:\n{content[:500]}...")

    # Show related artifacts
    related_ids = json.loads(result['related_artifacts'] or '[]')
    for rid in related_ids:
        # Fetch and display related artifact titles
        pass

    # Show usage history (symlinks)
    symlinks = conn.execute("""
        SELECT * FROM symlinks WHERE artifact_id = ?
    """, (artifact_id,)).fetchall()
    print(f"\nUsed in {len(symlinks)} projects")
```

## Git Integration

**Global workspace is git-backed:**

```bash
cd ~/.claude/workspace
git log --oneline artifacts/
git show abc123:artifacts/code/{uuid}.md
```

**Commit message template** (configured in `.workspace.conf`):
```
feat(workspace): {action} {type} — {title}

{description}

Type: {type}
Domain: {domain}
Tags: {tags}
Session: {session_id}
```

**Auto-commit on artifact promotion** (if `git.auto_commit_artifacts = true`):
- Every manual promotion creates a commit
- Automatic promotions batched (one commit per session end)

**Project workspaces are NOT git-backed** (they live in project repos):
- Symlinks to global artifacts
- Project-specific artifacts stored locally
- No independent version history

## Retention Enforcement

**Triggered on session end** (if retention policies configured):

1. **Archive cleanup**:
   ```python
   # Delete archives older than TTL
   cutoff = datetime.now() - timedelta(days=archive_ttl_days)
   old_archives = conn.execute("""
       SELECT * FROM sessions WHERE archived_at < ?
   """, (cutoff,)).fetchall()

   for archive in old_archives:
       # Delete directory
       shutil.rmtree(archive['path'])
       # Log deletion
       conn.execute("""
           INSERT INTO retention_log (artifact_id, action, reason)
           VALUES (?, ?, ?)
       """, (archive['id'], 'deleted', f'TTL expired ({archive_ttl_days} days)'))
       # Delete from index
       conn.execute("DELETE FROM sessions WHERE id = ?", (archive['id'],))
   ```

2. **Artifact warnings**:
   ```python
   # Warn about unused artifacts
   cutoff = datetime.now() - timedelta(days=artifact_unused_warning_days)
   unused = conn.execute("""
       SELECT * FROM artifacts
       WHERE updated_at < ? AND status = 'active'
   """, (cutoff,)).fetchall()

   print(f"Warning: {len(unused)} artifacts unused for 180+ days")
   # Optionally: set status to 'archived' after artifact_auto_archive_days
   ```

3. **Symlink validation**:
   ```python
   # Check for broken symlinks
   broken = []
   symlinks = conn.execute("SELECT * FROM symlinks").fetchall()
   for link in symlinks:
       if not os.path.exists(link['target_path']):
           broken.append(link)

   # Clean up broken symlinks
   for link in broken:
       os.remove(link['target_path'])
       conn.execute("DELETE FROM symlinks WHERE id = ?", (link['id'],))
       conn.execute("""
           INSERT INTO retention_log (artifact_id, action, reason)
           VALUES (?, ?, ?)
       """, (link['artifact_id'], 'symlink_removed', 'Target deleted'))
   ```

## Integration With Scratchpad Operon

**No breaking changes.** Workspace extends scratchpad with lifecycle management:

- **Scratchpad lifecycle** — `draft → review → promoted/deleted` (unchanged)
- **New option** — promote to workspace instead of directly to project
- **Session end** — archive-worthy scratchpad items auto-archived (if configured)
- **Scratchpad manifest** — track promotion destination (`workspace/artifacts/` or project files)

**Updated scratchpad manifest format:**

```markdown
| File | Purpose | Target | Status | Created | Last Touched |
|------|---------|--------|--------|---------|--------------|
| api-auth.md | FastAPI auth research | workspace/artifacts/research | promoted | 2026-02-06 | 2026-02-06 |
| docker-setup.sh | Docker install script | project/scripts/ | promoted | 2026-02-05 | 2026-02-06 |
```

**Promotion decision tree:**

```
Is this reusable across projects?
├─ Yes → Promote to workspace artifacts
│         └─ Symlink to project if needed
└─ No  → Promote directly to project files
          └─ Delete from scratchpad
```

## Integration With Other Operons

| Operon | Integration |
|--------|-------------|
| **Scratchpad** | Workspace is the next tier after scratchpad. Promote reusable items. |
| **Auditing** | Session audit checks: workspace indexed, retention enforced, no broken symlinks. |
| **Evolution** | Extract patterns from workspace research. Archive AARs. Search past solutions. |
| **Knowledge** | Promote high-value research to `docs/knowledge/`. Keep original in workspace. |
| **Orchestration** | Agents can query workspace for reusable templates before generating new code. |
| **Recovery** | Workspace archives provide session recovery points beyond git history. |
| **Retrieval** | Semantic search complements SQLite FTS. Use `/workspace search` for keywords, `/retrieval search` for concepts. |

### Auditing Checklist Addition

**Add to session audit:**

```markdown
### Workspace Checks (if workspace operon active)
- [ ] Scratchpad items promoted or deleted (nothing stale left)
- [ ] Session archived to workspace (if retention enabled)
- [ ] Retention policies enforced (old archives cleaned up)
- [ ] Symlinks validated (no broken links)
- [ ] Workspace index updated (all artifacts indexed)
- [ ] Git commits created (for promoted artifacts in global workspace)
```

### Evolution Pattern Extraction

**Add workspace search to pattern extraction workflow:**

```markdown
## Pattern Extraction Workflow

1. Evolution operon identifies recurring lesson (3+ AARs)
2. **Search workspace for related artifacts**:
   ```bash
   /workspace search "context window optimization" --type research
   ```
3. Aggregate findings from workspace + knowledge base
4. Extract pattern to docs/knowledge/patterns/
5. Update pattern catalog
```

### Knowledge Integration

**Promote workspace artifact to knowledge base:**

```bash
/workspace promote <artifact-id> --to-knowledge

# This:
# 1. Validates YAML frontmatter (knowledge schema)
# 2. Copies to docs/knowledge/research/
# 3. Updates knowledge INDEX.md
# 4. Keeps original in workspace/artifacts/ (symlink back)
```

**Implementation:**

```python
def promote_to_knowledge(artifact_id):
    # Read artifact
    artifact = get_artifact(artifact_id)

    # Validate frontmatter (must have: domain, tags, description)
    if not validate_knowledge_schema(artifact):
        print("Error: Artifact missing required knowledge fields")
        return

    # Copy to knowledge base
    knowledge_path = f"docs/knowledge/{artifact['type']}/{artifact['title'].lower().replace(' ', '-')}.md"
    shutil.copy(artifact['path'], knowledge_path)

    # Update knowledge INDEX.md
    update_knowledge_index(knowledge_path, artifact)

    # Create symlink back to workspace (bidirectional link)
    workspace_link = f"{artifact['path']}.knowledge-link"
    os.symlink(knowledge_path, workspace_link)

    # Update artifact metadata
    conn.execute("""
        UPDATE artifacts
        SET metadata = json_set(metadata, '$.knowledge_link', ?)
        WHERE id = ?
    """, (knowledge_path, artifact_id))

    print(f"Promoted to knowledge: {knowledge_path}")
```

## Commands Reference

### Search and Query

```bash
/workspace search <query> [--type TYPE] [--domain DOMAIN] [--after DATE]
/workspace show <artifact-id>
/workspace related <artifact-id>
/workspace history <artifact-id>
/workspace stats
```

**Hybrid Search** (with Retrieval operon):
- `/workspace search`: SQLite FTS keyword search (fast, exact matches, Boolean queries)
- `/retrieval search --collection workspace`: Semantic search (concepts, paraphrasing, related ideas)
- **Best practice**: Try keyword search first, then semantic search for broader results

### Artifact Management

```bash
/workspace promote <scratchpad-file> [--type TYPE] [--domain DOMAIN] [--tags TAGS]
/workspace promote <artifact-id> --to-knowledge
/workspace link <artifact-id> --to <project-path>
/workspace archive <artifact-id>
/workspace delete <artifact-id>
```

### Maintenance

```bash
/workspace audit
/workspace cleanup [--dry-run]
/workspace rebuild-index
/workspace validate-symlinks
```

## Graceful Degradation

**If SQLite not installed:**
- Workspace directory structure still created
- Manual file organization still works
- Search falls back to grep (slower)
- No automatic indexing
- Warning displayed on install

**If git fails:**
- Artifacts still stored (no version control)
- Manual file management still works
- No commit history
- Warning logged

**If auto-archive disabled:**
- Manual archiving still available
- Scratchpad lifecycle unchanged
- Operator manually promotes items

## Anti-Patterns

**Don't:**
- ❌ Store project-specific code as global artifacts (use project workspace)
- ❌ Promote everything to artifacts (dilutes value, use archives for ephemeral)
- ❌ Skip metadata (artifacts without frontmatter are unsearchable)
- ❌ Keep duplicates in scratchpad + workspace (promote means move, not copy)
- ❌ Archive without retention policies (unbounded growth)
- ❌ Store secrets in workspace (git-backed, use environment variables)

**Do:**
- ✅ Promote reusable patterns, templates, research
- ✅ Use archives for session continuity (reference past decisions)
- ✅ Tag artifacts with domain and technology (enables search)
- ✅ Link related artifacts (build knowledge graph)
- ✅ Enforce retention policies (clean up old archives)
- ✅ Use symlinks for cross-project sharing (don't duplicate)

## Example Workflows

### Workflow 1: Reusable Template

1. Create docker-compose setup in scratchpad
2. Test in current project
3. Mark as `review` in scratchpad manifest
4. Promote to workspace: `/workspace promote scratchpad/docker-compose.yml --type template --domain web --tags docker,fastapi`
5. AI generates UUID, adds frontmatter, indexes, commits to git
6. Delete from scratchpad (promoted)
7. Use in other projects: `/workspace link {uuid} --to other-project/.claude/workspace/`

### Workflow 2: Session Research

1. Research FastAPI authentication patterns (agent output to scratchpad)
2. Session ends → auto-archive to `workspace/archive/2026-02/session-{uuid}/`
3. Next session: work on different project, need auth pattern
4. Search: `/workspace search "fastapi authentication" --type archive`
5. Find archived research, decide to promote
6. Promote to artifacts: `/workspace promote {archive-path} --type research`
7. Now permanently searchable and reusable

### Workflow 3: Pattern Extraction

1. Evolution operon identifies recurring pattern (3+ AARs about context window)
2. Search workspace: `/workspace search "context window" --type research`
3. Find 5 archived sessions with related research
4. Aggregate findings
5. Extract to `docs/knowledge/patterns/context-window-management.md`
6. Link back to workspace artifacts in `related_artifacts` field

## SQLite Schema Reference

**Tables:**
- `schema_version` — schema version tracking
- `artifacts` — core artifact metadata
- `artifacts_fts` — full-text search index (FTS5)
- `sessions` — archived session metadata
- `symlinks` — cross-project symlink tracking
- `retention_log` — audit log for retention actions

**Key queries:**
- Full-text search: `SELECT * FROM artifacts_fts WHERE artifacts_fts MATCH ?`
- Promotion candidates: `SELECT path, COUNT(*) FROM artifacts GROUP BY path HAVING COUNT(*) >= 3`
- Retention cleanup: `SELECT * FROM sessions WHERE archived_at < ?`
- Broken symlinks: `SELECT * FROM symlinks WHERE artifact_id NOT IN (SELECT id FROM artifacts)`

See `templates/workspace-schema.sql` for full schema.

## Configuration Reference

**File**: `.claude/workspace/.workspace.conf` (TOML)

**Sections:**
- `[metadata]` — version tracking
- `[retention]` — TTL and cleanup policies
- `[auto_archive]` — session archival configuration
- `[git]` — version control settings
- `[search]` — SQLite FTS configuration
- `[symlinks]` — cross-project linking settings

See `templates/workspace.conf.template` for full config with comments.
