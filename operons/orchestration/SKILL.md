---
name: orchestration
description: >
  This skill should be used when spawning agents, dispatching subagents,
  parallelizing tasks, running agents in parallel, decomposing work for
  multi-agent execution, or integrating agent outputs.
  MESO operon (Gonozooid — Agent Spawning).
---

# Orchestration — Gonozooid (Agent Spawning)

## Pre-Dispatch Gate
Before dispatching ANY write-capable agent:
1. Verify `~/.claude/settings.local.json` allows Write, Edit, and Bash
2. If permissions are insufficient, fix them FIRST — never dispatch into a permission wall

## When to Parallelize
ALL conditions must be met:
1. Tasks are independent — no shared file writes, no data dependencies
2. Tasks are well-defined — clear deliverable, bounded scope
3. Tasks are substantial — trivial work (< 3 steps) doesn't justify overhead
4. No file conflicts — each agent writes to different files

Do NOT parallelize when:
- Two agents would write the same file
- One agent's output is input for another
- Task requires iterative human feedback
- Work is exploratory and scope is unclear

## Decomposition Protocol
1. Identify concrete deliverables (files created/modified)
2. Map file ownership — no write conflicts allowed
3. Draw dependency graph — independent = parallel, dependent = sequential
4. Plan integration BEFORE dispatching

## Agent Prompt Requirements
Each dispatched agent must receive:
- Specific files to read (full paths)
- Exact deliverable (what files to create/modify, what they should contain)
- Constraints (what NOT to do)
- Success criteria (how to verify the work)

Never assume agents have conversation context. Each starts fresh. Front-load everything.

## Integration Protocol
1. Check for permission failures — extract content from output transcript if denied
2. Verify deliverables — correct structure, no syntax errors, all features present
3. Merge where needed — with full awareness of both outputs
4. Update task tracking
5. Report to operator: what each agent accomplished, any issues

## Common Failures

| Failure | Recovery |
|---------|----------|
| Permission denied (write) | Extract from agent output transcript, write directly |
| Incomplete work | Resume agent by ID, or complete manually |
| File conflict | Diff both versions, merge manually |
| Bad output quality | Treat as draft; fix in place or re-dispatch with better prompt |
