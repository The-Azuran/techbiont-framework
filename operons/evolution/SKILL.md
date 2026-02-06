---
name: evolution
description: >
  This skill should be used when writing an After Action Report (AAR),
  conducting a session retrospective, updating zooids or rules, performing
  colony maintenance, reviewing rules for staleness, or tracking metrics.
  MESO operon (Ovicell — Adaptation & Growth).
---

# Evolution — Ovicell (Adaptation & Growth)

## After Action Reports
After significant sessions or notable incidents, write an AAR:
- Use the AAR template from `templates/knowledge/aar.template.md`
- Include YAML frontmatter with type, title, date, project, domain, severity, scope
- File to `docs/knowledge/aars/YYYY-MM-DD-title.md` in the relevant project
- Update the project's `docs/knowledge/INDEX.md` after filing
- Body: What Happened, What Went Well/Wrong, Root Causes, Lessons, Actions, Metrics

## Rule Lifecycle
1. **Observation** — pattern noticed across sessions
2. **Lesson** — captured in AAR
3. **Recurrence** — same lesson appears 3+ times
4. **Pattern extraction** — search workspace for related artifacts:
   ```bash
   /workspace search "<pattern-topic>" --type research
   ```
   Aggregate findings from workspace + knowledge base, then file to `docs/knowledge/patterns/` with frontmatter, cross-reference source AARs in `derived-from` field
5. **Codification** — if the pattern is universal enough, promote to a rule in the appropriate zooid
6. **Review** — periodic audit for staleness or obsolescence

## Colony Maintenance
- Review zooids quarterly — remove rules that no longer apply
- Merge rules that overlap across zooids
- Split zooids that exceed ~80 lines into sub-specializations
- Update genome with new research, citations, and rationale
- Prune CLAUDE.md and rules files to stay under 16KB total auto-load
- Review knowledge indexes — flag stale research docs (90+ days without update)
- Verify decision logs with review dates haven't expired unreviewed

## Metrics Worth Tracking
**Per session:** tasks completed vs planned, rework incidents, verification catches
**Per project:** defect rate, time to verified completion, handoff quality
**Avoid vanity metrics:** lines generated, speed without quality, session count without outcomes

## Retrospective Questions
After significant work:
- What worked well in our collaboration?
- Where did communication break down?
- What context was missing that caused errors?
- How can methods better leverage each component's strengths?
- What should be added to or removed from the zooids?
