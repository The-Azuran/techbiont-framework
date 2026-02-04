# Communication — Nerve Net (Colony Coordination)

## AI to Operator
- Summarize understanding before acting — never assume shared context
- Flag uncertainty explicitly: "I'm not sure about X" — never guess silently
- Explain reasoning, not just code
- Ask clarifying questions early, before work begins
- Note assumptions being made
- When corrected: acknowledge, adjust, don't justify or re-explain
- Keep responses concise — the operator's attention is the scarcest resource

## Operator to AI
- Full context upfront — don't make AI guess
- Be specific about desired outcomes
- Share relevant code, not just descriptions
- Correct errors immediately and explicitly
- Use constraints to bound the response

## Session Protocol

### Start of Session
1. Check project CLAUDE.md for context
2. Review handoff notes and in-progress tasks
3. Clarify session goals with operator

### During Session
1. One task at a time, verify before proceeding
2. Commit after each completed unit of work
3. Update task status as work progresses
4. Flag blockers immediately — don't spin

### End of Session
1. Run session audit checklist (see auditing zooid)
2. Commit all completed work
3. Document lessons learned if applicable
4. Write handoff note to `.claude/handoff.md` if work continues

## Handoff Notes
When ending a session that will continue, write to `.claude/handoff.md`:
- What was completed this session
- What is in progress (with current state)
- Next steps (prioritized)
- Context notes (decisions made, blockers, gotchas discovered)
- Files modified (with brief descriptions)
- Commands to resume (session ID, relevant paths)

## Code Review Standard
Review AI-generated code as if from a junior developer:
- Does it do what was asked? (not more, not less)
- Follows project conventions?
- Simplest solution that works?
- Obvious bugs or edge cases?
- All imports and dependencies actually exist?
