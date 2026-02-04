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
After significant sessions or notable incidents, write an AAR to the genome (Part X):
- Date, project, scope
- What happened (factual)
- What went well / what went wrong
- Root causes
- Lessons learned
- Action items
- Metrics: rework incidents, verification catches, errors escaped

## Rule Lifecycle
1. **Observation** — pattern noticed across sessions
2. **Lesson** — captured in AAR
3. **Recurrence** — same lesson appears 3+ times
4. **Codification** — promoted to a rule in the appropriate zooid
5. **Review** — periodic audit for staleness or obsolescence

## Colony Maintenance
- Review zooids quarterly — remove rules that no longer apply
- Merge rules that overlap across zooids
- Split zooids that exceed ~80 lines into sub-specializations
- Update genome with new research, citations, and rationale
- Prune CLAUDE.md and rules files to stay under 16KB total auto-load

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
