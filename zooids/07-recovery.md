# Recovery — Vibraculum (Debris Clearing)

## When Something Goes Wrong
1. **Stop** — do not compound the error with more changes
2. **Assess** — what happened? What is the blast radius?
3. **Rollback** — git revert/reset, restore from backup if needed
4. **Understand** — root cause, not just symptoms
5. **Fix** — address the actual problem
6. **Document** — add to lessons learned (genome Part X)
7. **Prevent** — update the appropriate zooid to catch this earlier

## Never Debug By
- Making speculative changes to code you haven't read
- Guessing at the problem without examining error output
- Retrying the same failing approach without changing anything
- Suppressing errors instead of understanding them

## Context Rot Recovery
When a session becomes confused or contradictory:
- Commit any good work so far
- Write a handoff note capturing current state
- Start a fresh session with clean context
- Resume from the handoff

## Permission Failure Recovery
When background agents hit permission walls:
- Check agent output transcripts for prepared content
- Extract and apply content directly
- Fix permissions in `~/.claude/settings.local.json` before next dispatch
- Never re-dispatch agents into the same permission wall

## Merge Conflict Recovery
- Never resolve merge conflicts by accepting one side blindly
- Read both versions, understand the intent of each
- Produce a merged result that preserves both intents
- Verify the merge with tests

## When to Give Up on Prompting
If three attempts at the same task produce wrong results:
- The task may require human expertise the model lacks
- Step in directly rather than burning more tokens
- Document the failure mode in the AAR
