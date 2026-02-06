---
name: auditing
description: >
  This skill should be used when running an audit, performing verification
  checklists, checking for hallucinated libraries or APIs, conducting a
  session audit, doing a checkpoint review, or verifying code quality.
  MESO operon (Avicularium — Verification Snap).
---

# Auditing — Avicularium (Verification Snap)

The verification loop: Write -> Test -> Feed errors back -> Fix -> Repeat.
This improves output quality 2-3x.

## Inline Audit (every change)
- [ ] Change matches stated intent
- [ ] No unintended side effects visible
- [ ] Code follows project conventions
- [ ] No obvious security issues introduced
- [ ] No debug code or TODOs left behind
- [ ] No hallucinated libraries or methods — verify imports exist

## Checkpoint Audit (after each logical task)
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Feature works as specified (manual verification if needed)
- [ ] Changes are atomic and committable
- [ ] Documentation updated if needed
- [ ] No scope creep — only what was asked

## Session Audit (end of session)
- [ ] All changes committed with meaningful messages
- [ ] No work-in-progress left uncommitted
- [ ] Task list reflects current state
- [ ] Lessons learned captured if applicable
- [ ] Significant decisions documented in decision log (if any were made)
- [ ] Research findings persisted to docs/ with frontmatter (if research was done)
- [ ] Next steps documented, handoff written if work continues

### Workspace Checks (if workspace operon active)
- [ ] Scratchpad items promoted or deleted (nothing stale left)
- [ ] Session archived to workspace (if retention enabled)
- [ ] Retention policies enforced (old archives cleaned up)
- [ ] Symlinks validated (no broken links)
- [ ] Workspace index updated (all artifacts indexed)
- [ ] Git commits created (for promoted artifacts in global workspace)

## Hallucination Detection

| Type | How to Detect |
|------|---------------|
| Phantom packages | Verify package exists in its registry |
| Invented APIs | Check documentation for the method/function |
| Confident wrongness | Test with edge cases |
| Stale knowledge | Verify against current docs |

## Mitigation
- Self-correct: verify your own imports and API calls before presenting code
- Ground: request current documentation when working with unfamiliar tools
- Cross-reference: check claims against authoritative sources
- Test: automated tests catch runtime failures that review misses
