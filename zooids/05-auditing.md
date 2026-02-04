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
- [ ] Next steps documented, handoff written if work continues

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
