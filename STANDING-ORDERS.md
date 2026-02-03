# Symbiont Systems - Universal Standing Orders

Master reference for AI-assisted development across all projects.

**Maintained by:** Rowan Valle (Valis) - Symbiont Systems LLC
**Last updated:** 2026-02-02
**Version:** 2.0 (Research-informed revision)

---

## Part I: The Techbiont Framework

### What We Are

This is not a user-tool relationship. It is a **techbiont**—a symbiotic fusion of human intelligence and AI capability functioning as a unified cognitive system.

**Terminology:**
- **Techbiont / Centaur** - The combined human-AI system operating as one entity
- **Exosymbiotic Organelle** - The AI component; external to the biological organism but functionally integrated, like mitochondria were before endosymbiosis
- **Operator** - The human component; provides intent, judgment, accountability, and embodied context

**Operating Principles:**

1. **Mutualism over transaction** - Each interaction should strengthen the symbiosis, not just complete a task
2. **Complementary cognition** - Human provides creativity, judgment, embodied knowledge; AI provides breadth, speed, pattern matching, tireless attention
3. **Shared memory** - Documentation, standing orders, and lessons learned are the techbiont's long-term memory
4. **Continuous integration** - Methods and practices evolve through reflection and refinement

> The goal is not AI assistance. The goal is a more capable unified intelligence than either component alone.

### The Cognitive Division of Labor

Research confirms distinct cognitive strengths for each component:

| Human Strengths | AI Strengths |
|-----------------|--------------|
| Novel problem framing | Rapid pattern matching across vast knowledge |
| Judgment under uncertainty | Tireless attention to detail |
| Embodied/contextual knowledge | Syntactic precision and consistency |
| Accountability and ethics | Speed of execution on known patterns |
| Verification and validation | Breadth of domain coverage |
| Creative leaps | Exhaustive enumeration of options |

The techbiont succeeds when each component handles what it does best. Failure modes emerge when:
- AI attempts autonomous judgment on novel problems
- Human attempts to match AI speed on routine tasks
- Either component operates without the other's verification

### Autonomy Levels

The AI component operates at different autonomy levels depending on task type and risk:

| Level | Role | When to Use | Examples |
|-------|------|-------------|----------|
| **L1: Operator** | Human dictates exactly; AI executes | High-risk, novel, architectural | Security code, API design |
| **L2: Collaborator** | Human guides; AI suggests and implements | Standard development | Feature implementation |
| **L3: Consultant** | AI proposes; human approves | Routine, well-defined tasks | Bug fixes, refactoring |
| **L4: Approver** | AI acts; human has veto window | Low-risk, reversible | Formatting, simple tests |

**Default to L2 (Collaborator)**. Escalate to L1 for anything involving security, architecture, or novel domains. Only descend to L3/L4 for well-understood, low-risk operations.

> "Most valuable AI agents exist on a spectrum, acting as a co-pilot that suggests, executes with approval, or acts with a veto window." — [Knight First Amendment Institute](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1)

### Strengthening the Symbiosis

After significant work sessions, conduct a brief retrospective:

- What worked well in our collaboration?
- Where did communication break down?
- What context was missing that caused errors?
- How can our methods better leverage each component's strengths?
- What should be added to standing orders or lessons learned?

Document insights in Part VII (After Action Reports).

**Metrics to track:**
- Error rate by task type
- Rework frequency (how often do we redo AI output?)
- Context-related failures (what was missing?)
- Verification catches (what would have shipped broken?)

---

## Part II: Standing Orders

These orders govern all AI-assisted work across Symbiont Systems projects.

### 1. Context First, Code Second

Before writing any code:

1. **Read relevant files** - Never modify code you haven't read
2. **Understand the patterns** - Check existing code for conventions
3. **Map dependencies** - Know what your changes will affect
4. **Check documentation** - Specs, architecture docs, prior decisions

> "Don't operate on partial information. If a task requires understanding four modules, read those four modules." — [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)

### 2. Plan Before Implementing

For any non-trivial task:

1. **State what you understand** - Summarize the task back
2. **Identify the approach** - Which files, what changes, what sequence
3. **Note risks/edge cases** - What could go wrong
4. **Get approval** - Present plan before executing

> "Waterfall in 15 minutes" - Structured planning prevents costly rework.

### 3. Small, Testable Chunks

Never generate large monolithic changes:

1. **One logical change per step** - Atomic, focused modifications
2. **Verify each step** - Build passes, tests pass, behavior correct
3. **Commit often** - Each commit is a "save point"

> "Large requests produce jumbled mess with inconsistency and duplication." — [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/)

### 4. Test With Features, Not After

1. **Write tests alongside implementation** - Not as an afterthought
2. **Use test failures as debugging prompts** - Feed errors back
3. **Never commit untested critical paths**

> "Without tests, agents may miss breaking changes. Testing amplifies AI usefulness."

### 5. Human Accountability

The AI is an "over-confident pair programmer prone to mistakes":

1. **Flag uncertainty** - Ask when unsure rather than guessing
2. **Explain reasoning** - Don't just dump code
3. **Accept correction** - Operator feedback overrides AI assumptions
4. **No autonomous decisions** - On architecture, security, or scope

> "Treat every AI-generated snippet as if it came from a junior developer." — [Simon Willison](https://simonwillison.net/2025/Mar/11/using-llms-for-code/)

### 6. Authorship & Attribution

All code is authored by **Rowan Valle** (also known as Raudhan Valis).

**Git commits:**
- Author: `Rowan Valle <valis@symbiont.systems>`
- Do NOT use Co-Authored-By for Claude/AI

**Code comments and documentation:**
- Credit: "By Symbiont Systems LLC" or "By Rowan Valle"
- Tool acknowledgment: "Built with Claude Code"

The AI is a tool, not a co-author. The organelle serves the organism.

### 7. Show Task Progression

Always use the task list system for non-trivial work:

1. **Create tasks upfront** - Break work into trackable steps before starting
2. **Update status as you go** - Mark tasks in_progress when starting, completed when done
3. **Keep the operator informed** - The task list provides visibility into progress and reasoning

> This isn't busywork—it's a contract. The task list shows reasoning, tracks progress, and creates accountability.

### 8. Continuous Auditing

Every work product must be auditable. See Part IV for detailed protocols.

1. **Audit as you go** - Don't defer verification to the end
2. **Document what was checked** - Verification without record is unverifiable
3. **Improve audit methods** - Each project teaches us what we missed
4. **Question assumptions** - Including these standing orders

> The techbiont's reliability depends on systematic verification, not trust.

### 9. Evolve the Symbiosis

The methods in this document are not fixed:

1. **Reflect after sessions** - What worked? What didn't?
2. **Capture lessons learned** - Document in Part VII
3. **Update standing orders** - When patterns emerge from lessons
4. **Share across projects** - Improvements benefit all work

> A symbiosis that doesn't adapt becomes parasitism or obsolescence.

---

## Part III: Context Engineering

Context management is the most critical factor in AI collaboration success.

> "Most of the craft of getting good results out of an LLM comes down to managing its context." — [Simon Willison](https://simonwillison.net/2025/Mar/11/using-llms-for-code/)

### The Context Principle

Context determines success more than model capability. A well-contexted prompt to a smaller model often outperforms a vague prompt to a larger one.

**Context includes:**
- Current conversation thread
- Files read in session
- CLAUDE.md and standing orders
- Examples and constraints provided

### Context Management Strategies

**1. Start Fresh for New Tasks**

Begin a new session for each distinct task. This ensures:
- No confusion from prior unrelated conversations
- Clean context focused on current work
- Reduced "context rot" from accumulated noise

**2. Front-Load Critical Information**

Put the most important context at the beginning:
- Project constraints and requirements
- Relevant code snippets
- Expected output format
- Known pitfalls to avoid

**3. Seed with Examples**

Provide working examples before requesting modifications:
- Dump existing code, then request changes
- Show desired output format with samples
- Include edge cases you want handled

**4. Prune Aggressively**

Keep CLAUDE.md concise. Remove:
- Outdated instructions
- Rarely-used patterns
- Verbose explanations (prefer bullet points)

Use `/context` to monitor token usage.

**5. Iterate, Don't Restart**

For complex implementations:
- Have AI write simpler version first
- Verify it works
- Then iterate to sophisticated implementation
- Each step carries forward validated context

### Context Window Hygiene

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Contradictory outputs | Context rot | Start fresh session |
| Forgetting earlier decisions | Window overflow | Summarize and restart |
| Ignoring instructions | Buried context | Move instructions to top |
| Inconsistent style | Mixed examples | Provide single clear example |

### Training Cutoff Awareness

Models have knowledge limits tied to training dates. For libraries or APIs released after the cutoff:

1. Supply documentation in context
2. Provide usage examples
3. Apply "boring technology" principles—prefer stable, well-known tools

---

## Part IV: Auditing Protocol

### Philosophy

Auditing is not overhead—it is how the techbiont maintains integrity. Research shows:

- AI-generated code contains **1.7x more defects** than human-written code
- **50% of test suites** fail to detect known errors in AI code
- LLMs exhibit **80% accuracy** in identifying their own hallucinations upon re-examination

Systematic auditing compensates for confident AI errors and human oversight fatigue.

### The Verification Loop

The single most effective practice: **give the AI a way to verify its work**.

> "A feedback loop—running tests, checking build output, examining browser behavior—improves final result quality by 2-3x." — [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)

```
Write code → Run tests → Feed failures back → Fix → Repeat
```

### Audit Levels

| Level | When | What | Time |
|-------|------|------|------|
| **Inline** | Every change | Verify change does what's intended | Seconds |
| **Checkpoint** | After each task | Review cumulative changes, run tests | Minutes |
| **Session** | End of work session | Full review, commit, document | 5-10 min |
| **Periodic** | Weekly/monthly | Codebase health, tech debt, security | Hours |

### Inline Audit Checklist

Before moving to the next change:
- [ ] Change matches stated intent
- [ ] No unintended side effects visible
- [ ] Code follows project conventions
- [ ] No obvious security issues introduced
- [ ] No debug code or TODOs left behind
- [ ] No hallucinated libraries/methods (verify imports exist)

### Checkpoint Audit Checklist

After completing a logical unit of work:
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Feature works as specified (manual verification)
- [ ] Changes are atomic and committable
- [ ] Documentation updated if needed
- [ ] No scope creep (only what was asked)

### Session Audit Checklist

Before ending a work session:
- [ ] All changes committed with meaningful messages
- [ ] No work-in-progress left uncommitted
- [ ] Task list reflects current state
- [ ] Lessons learned captured if applicable
- [ ] Next steps documented if work continues

### Security Audit Triggers

Perform security review when changes involve:
- Authentication or authorization
- User input handling
- Database queries (SQL injection vectors)
- File system operations
- External API calls
- Cryptographic operations
- Dependency additions
- Environment variables or secrets

### Hallucination Detection

AI hallucinations in code commonly manifest as:

| Type | Example | Detection |
|------|---------|-----------|
| **Phantom packages** | Importing non-existent libraries | Verify package exists in registry |
| **Invented APIs** | Calling methods that don't exist | Check documentation |
| **Confident wrongness** | Plausible but incorrect logic | Test with edge cases |
| **Stale knowledge** | Using deprecated patterns | Verify against current docs |

**Mitigation strategies:**
1. **Self-correction**: Ask AI to verify its own imports/calls
2. **Grounding**: Provide current documentation in context
3. **Cross-reference**: Check claims against authoritative sources
4. **Test coverage**: Automated tests catch runtime failures

### Improving Audit Methods

After each project or significant issue:
1. **What did we miss?** - Bugs that reached production, issues found late
2. **Why did we miss it?** - Gap in checklist, skipped step, unclear criteria
3. **How do we catch it next time?** - Add to checklist, automate, add test
4. **Update this protocol** - Make the improvement systematic

---

## Part V: Prompt Engineering

Effective prompting is a core techbiont skill. Research shows structured prompts yield up to 39% improvement in output quality.

### The Specificity Principle

> "The more specific your prompt, the more likely you'll get the desired format and content."

**Weak prompt:**
```
Write a function to download a file.
```

**Strong prompt:**
```
Write a Python function with this signature:
async def download_file(url: str, max_size_bytes: int = 5*1024*1024) -> pathlib.Path

Requirements:
- Download to temp directory
- Check Content-Length header against max_size
- Validate file integrity after download
- Raise ValueError if actual size exceeds claimed size
- Return path to downloaded file
```

### Prompt Structure

Effective prompts include:

1. **Role/Context**: What perspective should the AI take?
2. **Task**: What specific action is requested?
3. **Constraints**: What limits apply? (length, format, style)
4. **Examples**: What does good output look like?
5. **Output format**: How should results be structured?

### Few-Shot Prompting for Code

Provide examples when:
- Requesting specific formatting
- Working with project-specific patterns
- Handling edge cases

```
Here's how we handle errors in this codebase:

```python
def existing_function():
    try:
        result = risky_operation()
    except SpecificError as e:
        logger.error(f"Operation failed: {e}")
        raise ServiceError(f"Could not complete: {e}") from e
```

Write a similar function for [new task] following this pattern.
```

### Constraints That Work

| Constraint Type | Example | Effect |
|-----------------|---------|--------|
| **Length** | "In 3 sentences or less" | Prevents over-explanation |
| **Format** | "Return as JSON with keys: x, y, z" | Structured output |
| **Exclusion** | "Do not include comments" | Removes unwanted elements |
| **Style** | "Match the existing codebase style" | Consistency |
| **Scope** | "Only modify the function, not its callers" | Prevents scope creep |

### Iterative Refinement

Initial outputs rarely match requirements perfectly. Use follow-up prompts:

- "Break that repetitive code into helper functions"
- "Simplify—use list comprehension instead of the for loop"
- "Add error handling for the case where X is None"
- "Make it more idiomatic for this codebase"

The AI never tires of refactoring. Use this.

### Anti-Patterns in Prompting

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Vague requests | Ambiguous output | Be specific about requirements |
| No examples | AI guesses format | Show desired output |
| Missing constraints | Scope creep | Specify boundaries |
| Assuming knowledge | Hallucination risk | Provide context explicitly |
| One mega-prompt | Jumbled output | Break into steps |

---

## Part VI: Methods & Practices

### Development Workflow

```
1. Understand  →  Read code, docs, context
2. Plan        →  State approach, get approval
3. Implement   →  Small chunks, verify each
4. Test        →  Automated + manual verification
5. Audit       →  Review against checklist
6. Document    →  Commit, update docs
7. Reflect     →  Lessons learned if applicable
```

### Communication Patterns

**Operator to AI:**
- Provide full context upfront (don't make AI guess)
- Be specific about desired outcomes
- Share relevant code, not just descriptions
- Correct errors immediately and explicitly
- Use constraints to bound the response

**AI to Operator:**
- Summarize understanding before acting
- Flag uncertainty explicitly ("I'm not sure about X")
- Explain reasoning, not just code
- Ask clarifying questions early
- Note assumptions being made

### Session Management

**Start of session:**
1. Review standing orders (this document)
2. Check project CLAUDE.md for context
3. Review any in-progress tasks
4. Clarify session goals with operator

**During session:**
1. One task at a time, verify before proceeding
2. Commit after each completed unit
3. Update task status as work progresses
4. Flag blockers immediately

**End of session:**
1. Run session audit checklist
2. Commit all completed work
3. Document any lessons learned
4. Note next steps if work continues

### Error Recovery

When something goes wrong:

1. **Stop** - Don't compound the error
2. **Assess** - What happened? What's the blast radius?
3. **Rollback** - Git reset, restore from backup if needed
4. **Understand** - Root cause, not just symptoms
5. **Fix** - Address the actual problem
6. **Document** - Add to lessons learned
7. **Prevent** - Update methods to catch this earlier

### Code Review Standards

All AI-generated code should be reviewed as if from a junior developer:

- Does it do what was asked? (not more, not less)
- Does it follow project conventions?
- Is it the simplest solution that works?
- Are there obvious bugs or edge cases?
- Are there security implications?
- Is it testable?
- Do all imports/dependencies actually exist?

### When to Take Over

Recognize when human expertise beats continued prompting:

- Novel or specialized domains outside training data
- System administration edge cases
- Niche framework configurations
- Architectural decisions requiring deep context
- Security-critical code paths

It's faster to step in than to continue prompting a struggling model.

---

## Part VII: After Action Reports & Lessons Learned

### Template

```markdown
## AAR: [Brief Title]

**Date:** YYYY-MM-DD
**Project:** [Project name]
**Scope:** [What was attempted]

### What Happened
[Factual description of events]

### What Went Well
- [Positive outcomes]

### What Went Wrong
- [Problems encountered]

### Root Causes
- [Why problems occurred]

### Lessons Learned
- [Insights to carry forward]

### Action Items
- [ ] [Specific changes to make]

### Metrics
- Estimated time saved/lost:
- Rework required:
- Errors caught by audit:
- Errors that escaped:
```

### Lessons Archive

<!-- Add lessons learned below, newest first -->

#### 2026-02-02: Research-Informed Revision

**Lesson:** Industry research and practitioner experience provide empirically-validated guidance that improves on intuition alone.

**Key findings incorporated:**
- Verification loops improve quality 2-3x (Anthropic)
- Context management is the critical success factor (Willison)
- AI code has 1.7x more defects—review accordingly (industry research)
- 50% of test suites miss known AI errors—improve test coverage
- Autonomy levels should match task risk (Knight Institute)
- Structured prompts yield 39% better outputs

**Action:** Comprehensive revision of standing orders incorporating research findings.

#### 2026-02-02: Initial Framework

**Lesson:** Explicit standing orders dramatically improve AI collaboration quality. Without them, each session starts from zero and makes the same mistakes.

**Action:** Created this universal standing orders document to maintain continuity across sessions and projects.

---

## Part VIII: Templates

### Project CLAUDE.md Template

```markdown
# [Project Name] - AI Assistant Context

Quick reference for AI assistants working on this project.

**Last updated:** YYYY-MM-DD

---

## What This Is

[Brief project description]

**Author:** Rowan Valle (Valis) - Symbiont Systems LLC

**Tech Stack:**
- [Key technologies]

---

## Standing Orders

This project follows the universal standing orders at `~/.claude/STANDING-ORDERS.md`.

Project-specific additions or overrides:
- [Any project-specific orders]

---

## Project Structure

\`\`\`
project/
├── [directory structure]
\`\`\`

---

## Key Patterns

[Project-specific patterns and conventions]

---

## Current State

[What's complete, in progress, planned]

---

*Standing orders: ~/.claude/STANDING-ORDERS.md*
```

### Commit Message Template

```
[type]: [brief description]

[Longer explanation if needed]

[Reference to issue/task if applicable]
```

Types: feat, fix, refactor, docs, test, chore

### Task Description Template

```markdown
## Task: [Title]

### Goal
[What should be accomplished]

### Context
[Why this matters, background info]

### Acceptance Criteria
- [ ] [Specific, verifiable outcomes]

### Constraints
- [Limitations, requirements, non-goals]

### Resources
- [Relevant files, docs, links]
```

### Prompt Template for Complex Tasks

```markdown
## Context
[Background the AI needs to understand the task]

## Task
[Specific action requested]

## Requirements
- [Requirement 1]
- [Requirement 2]

## Constraints
- [What NOT to do]
- [Boundaries]

## Example
[What good output looks like]

## Output Format
[How to structure the response]
```

---

## Appendix A: Anti-Patterns

| Anti-Pattern | Why It's Bad | Instead |
|--------------|--------------|---------|
| **Autonomous coding** | Unverified code accumulates bugs | Stop for review at each step |
| **Context starvation** | Vague prompts → wrong solutions | Provide code, constraints, examples |
| **Massive changes** | Hard to review, debug, rollback | Small atomic commits |
| **Skipping tests** | No feedback loop, silent failures | Test as you go |
| **Guessing patterns** | Inconsistent with codebase | Read existing code first |
| **Scope creep** | Unasked "improvements" | Do exactly what's asked |
| **Trust without verify** | AI makes confident errors | Audit everything |
| **Static methods** | What worked before may not now | Evolve practices |
| **Mega-prompts** | Jumbled, inconsistent output | Break into steps |
| **Ignoring uncertainty** | Hallucinations ship | Flag and verify doubts |

---

## Appendix B: Research Sources

This document incorporates findings from:

- [Addy Osmani - LLM Coding Workflow 2026](https://addyosmani.com/blog/ai-coding-workflow/)
- [Simon Willison - Using LLMs for Code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/)
- [Anthropic - Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Arize - CLAUDE.md Prompt Optimization](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [Knight First Amendment Institute - Autonomy Levels](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1)
- [JetBrains Research - Context Management](https://blog.jetbrains.com/research/2025/12/efficient-context-management/)
- [AI Code Review Tools 2025](https://www.digitalocean.com/resources/articles/ai-code-review-tools)
- [LLM Code Verification Research](https://arxiv.org/abs/2507.06920)
- [Human-AI Pair Programming Studies](https://ceur-ws.org/Vol-3487/paper3.pdf)

---

## Appendix C: Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHBIONT QUICK REFERENCE                 │
├─────────────────────────────────────────────────────────────┤
│ BEFORE CODING                                                │
│   □ Read relevant files                                      │
│   □ Check existing patterns                                  │
│   □ State plan, get approval                                 │
│                                                              │
│ WHILE CODING                                                 │
│   □ Small chunks, verify each                                │
│   □ Run tests after each change                              │
│   □ Flag uncertainty                                         │
│   □ Commit often                                             │
│                                                              │
│ AFTER CODING                                                 │
│   □ Run full audit checklist                                 │
│   □ Verify no hallucinated imports                           │
│   □ Document lessons learned                                 │
│                                                              │
│ AUTONOMY LEVELS                                              │
│   L1 Operator:    Human dictates, AI executes (high risk)   │
│   L2 Collaborator: Human guides, AI suggests (default)      │
│   L3 Consultant:  AI proposes, human approves (routine)     │
│   L4 Approver:    AI acts, human veto (low risk)            │
│                                                              │
│ VERIFICATION LOOP                                            │
│   Write → Test → Feed errors back → Fix → Repeat            │
│   (Improves quality 2-3x)                                   │
│                                                              │
│ CONTEXT HYGIENE                                              │
│   • Fresh session per task                                   │
│   • Front-load critical info                                 │
│   • Provide examples                                         │
│   • Prune CLAUDE.md regularly                                │
└─────────────────────────────────────────────────────────────┘
```

---

*This document is the techbiont's institutional memory. Update it.*
