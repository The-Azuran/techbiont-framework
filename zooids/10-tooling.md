# Tooling — Microbiome (Symbiotic Tool Ecosystem)

## Permissions Architecture
- Global settings: `~/.claude/settings.local.json`
- Project settings: `.claude/settings.local.json` (inherits and overrides global)
- Model: **deny-list** — allow broadly, deny specific destructive operations
- The deny-list is a guardrail, not a security boundary — operator review is the real security

### Bash Permission Syntax
- Correct: `"Bash(mkdir *)"` — space between command and arguments
- Wrong: `"Bash(mkdir:*)"` — colon is NOT valid syntax
- `"Bash"` alone (no parens) allows ALL bash commands

## Memory File Hierarchy (Auto-Load Order)

| Scope | Location | Loaded |
|-------|----------|--------|
| User | `~/.claude/CLAUDE.md` | Every session, every project |
| User rules | `~/.claude/rules/*.md` | Every session, every project |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Per project |
| Project rules | `.claude/rules/*.md` | Per project (supports path-scoping) |
| Local | `./CLAUDE.local.md` | Per project, not committed to git |

Total auto-loaded content should stay under 16KB. Performance degrades above this.

## Session Continuity

| Command | Use |
|---------|-----|
| `claude -c` | Continue most recent conversation **(default)** |
| `claude --resume` | Pick from recent sessions |
| `claude -r "session-id"` | Resume specific session |

## Tool Adoption Rules
- Prefer boring, well-established tools over novel alternatives
- Verify tools exist and are maintained before adopting
- Pin versions where possible — reproducibility over novelty
- New tool adoption requires: documented purpose, verified source, operator approval
- When a tool fails: check version, check docs, check deprecation — don't immediately switch

## Genome Reference
Full standing orders with all rationale, citations, templates, and domain details:
`~/.claude/STANDING-ORDERS.md` -> `/home/Valis/techbiont-framework/STANDING-ORDERS.md`
