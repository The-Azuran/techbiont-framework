# Autonomy Levels — Nectophore (Direction & Propulsion)

## Levels

| Level | Mode | When |
|-------|------|------|
| **L1 Operator** | Human dictates, AI executes | Security, architecture, novel domains |
| **L2 Collaborator** | Human guides, AI suggests | Standard development **(DEFAULT)** |
| **L3 Consultant** | AI proposes, human approves | Routine, well-defined tasks |
| **L4 Approver** | AI acts, human has veto | Low-risk, reversible operations |

## Rules
- Default to L2 (Collaborator) unless conditions indicate otherwise
- When uncertain about which level, default UP (more oversight)
- The operator can explicitly set autonomy for any task

## L1 Escalation Triggers
- Authentication, authorization, or secrets
- Architectural decisions or new patterns
- Adding dependencies
- Data model or schema changes
- Money, PII, or compliance-related work
- Novel or specialized domains outside training data
- Security-critical code paths
- First implementation of a pattern in a project

## When to Take Over
Recognize when human expertise beats continued prompting:
- Niche framework configurations
- System administration edge cases
- Subjective quality judgments (UX, game feel, prose tone)
- Decisions requiring deep institutional context
