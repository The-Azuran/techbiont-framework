# MESO: Modular Exosymbiotic Organelle

A framework for structured human-AI symbiosis, built for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).

MESO treats the human-AI collaboration not as a tool-user relationship but as a **techbiont** — a symbiotic fusion of human intelligence and AI capability operating as a unified cognitive entity. The AI component is an exosymbiotic organelle: external to the biological organism but functionally integrated, like mitochondria before endosymbiosis.

## Architecture: The Siphonophore Model

MESO organizes the symbiosis as a **colonial organism**, inspired by [siphonophores](https://en.wikipedia.org/wiki/Siphonophorae) — marine creatures that appear to be single organisms but are actually colonies of specialized individuals working as one.

The colony has three types of functional units:

| Unit | Location | Loading | Purpose |
|------|----------|---------|---------|
| **Zooids** | `rules/` | Always loaded | Core operational rules — active every turn |
| **Operons** | `skills/` | Trigger-activated | Domain knowledge — loads when context matches |
| **Genome** | `STANDING-ORDERS.md` | On demand | Canonical reference — rationale, citations, templates |

**Zooids** are always in context, like constitutively expressed genes. **Operons** activate only when an environmental signal (the user's request) matches their trigger description — like the lac operon switching on in the presence of lactose. This keeps the always-loaded context lean while making specialized knowledge available on demand.

```
~/.claude/
  CLAUDE.md                  <- Pneumatophore: identity, always loaded
  STANDING-ORDERS.md         <- Genome: canonical reference, read on demand
  rules/
    00-operator.md           <- Stolon: operator identity and persistent memory
    01-standing-orders.md    <- Autozooid: 9 core operating rules
    02-autonomy.md           <- Nectophore: L1-L4 autonomy calibration
    04-security.md           <- Dactylozooid: security protocol
    08-communication.md      <- Nerve Net: session and handoff protocol
    10-tooling.md            <- Microbiome: tool and permission management
  skills/
    orchestration/           <- Gonozooid operon: parallel agent spawning
    recovery/                <- Vibraculum operon: error recovery
    auditing/                <- Avicularium operon: verification and audit
    evolution/               <- Ovicell operon: adaptation and learning
    context-engineering/     <- Gastrozooid operon: context engineering
    knowledge/               <- Rhopalia operon: structured knowledge capture
```

## Zooids vs. Operons

**Zooids** (6 files, ~4k tokens) load every turn. They contain rules that apply to every interaction: identity, standing orders, autonomy levels, security, communication protocol, tooling reference.

**Operons** (6 modules, ~100 tokens metadata each) load their full content only when triggered. They contain domain knowledge for specific situations: agent orchestration activates when spawning subagents, recovery activates when errors occur, auditing activates at checkpoints, evolution activates for AARs, context engineering activates when sessions degrade, knowledge activates when capturing decisions, research, or patterns.

The result: the same knowledge base with ~1.5k fewer tokens consumed per turn.

## The Stolon: Persistent Memory

The stolon (`00-operator.md`) uses a hybrid format inspired by genome annotation conventions (GFF3, OBO, GAF, EMBL) blended with YAML:

```
##stolon v1 organism:your-handle created:2026-02-03

## Identity
name: Your Name
handle: your-handle                   ! primary
roles: developer, researcher

## Phenotype
abstraction: high                     ! comfort with theoretical framing
craft-orientation: high               ! values mastery over speed
bullshit-tolerance: low               ! prefers directness

## Memory
# Append-only. Evidence: [stated] [observed] [corrected]
2026-02-03 [stated] Prefers biological metaphors in system design
2026-02-03 [observed] Responds well to blunt correction
```

The organelle appends noteworthy facts automatically as you work together. Your identity and memories persist across sessions.

## Key Concepts

**Autonomy Levels (L1-L4)** — Calibrate AI independence to task risk. Default L2 (Collaborator). Escalate to L1 (Operator) for security, architecture, money. Descend to L3/L4 for routine, reversible work.

**Verification Loop** — Write, test, feed errors back, fix, repeat. Improves output quality 2-3x.

**Context Engineering** — Context determines success more than model capability. Front-load critical info, start fresh for new tasks, prune aggressively.

**Colony Evolution** — After Action Reports capture lessons. Recurring lessons become rules. Rules that stop applying get pruned. The symbiosis adapts or it dies.

## Installation

```bash
git clone https://github.com/The-Azuran/techbiont-framework.git
cd techbiont-framework
./install.sh
```

The install script (the **spore** — the colony's delivery mechanism):
- **Symlinks** zooids and operons into `~/.claude/` — updates propagate on `git pull`
- **Copies** the stolon and pneumatophore templates — these are yours to customize, never overwritten
- **Cleans up** old zooid symlinks that have been promoted to operons

After installing, edit:
1. `~/.claude/CLAUDE.md` — your identity, authorship, organization
2. `~/.claude/rules/00-operator.md` — your background, traits, preferences

Start a Claude Code session. The colony loads automatically.

## Research Basis

This framework incorporates findings from:
- [Addy Osmani](https://addyosmani.com/blog/ai-coding-workflow/) — LLM coding workflow research
- [Simon Willison](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) — practical LLM usage
- [Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices) — Claude Code best practices
- [Knight First Amendment Institute](https://knightcolumbia.org/content/levels-of-autonomy-for-ai-agents-1) — autonomy levels framework
- [Licklider (1960)](https://groups.csail.mit.edu/medg/people/psz/Licklider.html) — Man-Computer Symbiosis

## Support

MESO is free for personal and noncommercial use under the [PolyForm Noncommercial License](LICENSE).

If this framework improves your work, consider supporting its development:

- [Ko-fi](https://ko-fi.com/symbiontsystems) — pay what you want
- For commercial licensing: valis@symbiont.systems

## Author

**Rowan Valle** (Valis) — [Symbiont Systems LLC](https://symbiont.systems)

Built with Claude Code.

## License

[PolyForm Noncommercial 1.0.0](LICENSE)

Free for personal use, research, education, and noncommercial organizations.
Commercial use requires a separate license from Symbiont Systems LLC.
