# MESOcomplete: Productization Architecture

**Type**: Architecture Planning
**Date**: 2026-02-05
**Status**: Strategic research, implementation planning
**Relevance**: MESO product development, hardware architecture, platform evolution

## Summary

MESOcomplete is the proposed product name for deployable MESO instances. This document explores hardware architectures, VPS deployment, persistence models, and novel approaches to session branching and identity management. Research driven by operator's vision of MESO as platform-agnostic product that gradually evolves away from Claude Code while maintaining curated quality.

---

## Strategic Decisions (Operator Input: 2026-02-05)

### 1. Platform Philosophy
**Decision**: Platform-agnostic, gradual evolution away from Claude Code

**Quote**: *"We must be our own platform at some point, but let us slowly evolve that capacity away from Claude while still using it as our platform until full evolution is complete."*

**Implications**:
- Multi-platform support required from start
- Abstraction layers for platform-specific vs universal features
- Migration path must be incremental, not big-bang
- Claude Code remains primary platform during transition

### 2. Quality vs. Anarchy
**Decision**: Curated quality primary, but adopt best anarchic ideas

**Quote**: *"Curated quality all day! But we also love the anarchy and encourage others to do what they want! We will steal the best ideas anyway (this in turn will become a mechanism to rapidly evolve MESO)."*

**Implications**:
- Maintain curated operon library as foundation
- Monitor community innovations (Pi, OpenClaw, etc.)
- Rapid adoption cycle for validated external ideas
- Hybrid model confirmed: quality + adaptability
- Encourage forking and experimentation

### 3. Session Branching & Persistence
**Decision**: Critical priority, requires deep research

**Quote**: *"I want branching and saved states/handoff. These are massively useful tools separate and together. We need to explore all the possibilities, including novel ones. We will research this because this is a problem of persistence and identity consolidation."*

**Implications**:
- Session branching is core architectural requirement, not nice-to-have
- Saved states/checkpoints must be first-class feature
- Identity persistence across sessions, platforms, instances
- Novel approaches welcomed - not constrained by existing solutions

### 4. Relationship to Pi
**Decision**: Adopt good practices, don't migrate platform

**Quote**: *"Since we aren't on it as a platform, we might could just adopt their good and great practices. I don't know though, we have to discuss this further."*

**Implications**:
- Learn from Pi's architecture without becoming Pi
- Evaluate each Pi feature independently for adoption
- Maintain MESO's distinct identity and philosophy
- Further discussion needed on specific adoptions

---

## Hardware Architecture Options

### Option 1: Self-Contained Server (Recommended Starting Point)

**Concept**: Standalone device running MESO instances, like a NAS for AI agents.

#### Minimum Viable Hardware

```
Component         Spec                      Purpose
----------        ----                      -------
CPU               6-core (i5/Ryzen 5)       Orchestration overhead, multi-session
RAM               32GB DDR4/DDR5            Multiple sessions, caching, local models
Storage (Primary) 1TB NVMe SSD              Fast session access, genome storage
Storage (Backup)  2TB HDD (optional)        Session archives, checkpoints
Network           Gigabit Ethernet          API calls, edge coordination
GPU (Optional)    RTX 3060 / Arc A770       Local LLM inference (future-proofing)
Form Factor       Mini PC / Tower           Depends on GPU requirements
Power             ~65W idle, ~200W peak     Consider UPS for persistence

Estimated cost: $800-1200 (mini PC, no GPU)
Estimated cost: $1500-2000 (tower with GPU)
```

#### Software Stack

**Operating System**: Fedora Server
- Operator's native environment
- Excellent container support (podman native)
- SELinux for security
- Systemd for service management
- Familiar package management

**Container Runtime**: Podman
- Rootless containers (security)
- Systemd integration
- No daemon required
- Compatible with Docker images

**Orchestration**: Systemd + Quadlet
- Native Fedora service management
- Container lifecycle as systemd services
- Automatic restarts, logging
- No Kubernetes overhead for single-node

**Storage Architecture**:
```
/meso/
├── genome/          (ro, symlinked to git repo)
│   ├── STANDING-ORDERS.md
│   ├── templates/
│   └── reference/
├── zooids/          (rw, instance-specific copies)
├── operons/         (rw, instance-specific copies)
├── sessions/        (rw, persistent, backed up)
│   ├── main/
│   ├── branches/
│   └── archives/
├── memory/          (rw, auto-updated, persistent)
├── scratchpad/      (rw, ephemeral, cleared on restart)
└── checkpoints/     (rw, saved states)

/meso-backup/        (separate volume, automated snapshots)
```

**Backup Strategy**:
- Hourly snapshots of active sessions
- Daily snapshots of memory + checkpoints
- Weekly snapshots of entire /meso/ tree
- Retention: 24 hourly, 7 daily, 4 weekly
- Backup to external drive + optional cloud sync

#### Architecture Diagram

```
┌─────────────────────────────────────────────┐
│         MESOcomplete Device                 │
├─────────────────────────────────────────────┤
│  Genome (immutable, version-controlled)     │
│  ├── STANDING-ORDERS.md                     │
│  └── Reference documentation                │
├─────────────────────────────────────────────┤
│  Zooids (copied on deploy, instance-local)  │
│  Operons (copied on deploy, instance-local) │
├─────────────────────────────────────────────┤
│  Session Storage (persistent, backed up)    │
│  ├── Main branch                            │
│  ├── Experimental branches                  │
│  └── Archived sessions                      │
├─────────────────────────────────────────────┤
│  Memory (auto-updated, persistent)          │
│  ├── Auto memory (session-spanning)         │
│  └── Knowledge documents                    │
├─────────────────────────────────────────────┤
│  Scratchpad (ephemeral, cleared on restart) │
│  └── Temporary files, agent outputs         │
├─────────────────────────────────────────────┤
│  API Proxy Layer                            │
│  ├── Route to Claude API                    │
│  ├── Route to local models (if GPU)         │
│  └── Route to edge nodes via MCP            │
└─────────────────────────────────────────────┘
```

---

### Option 2: VPS Deployment

**Concept**: Cloud-hosted MESO instances for remote access.

#### Recommended VPS Specifications (Per Instance)

```
Provider         Linode / DigitalOcean / Hetzner
vCPU             4 cores
RAM              8GB
Storage          100GB SSD (sessions + memory)
Network          Unmetered bandwidth
Backups          Automated daily snapshots
Location         Geographically close to operator

Cost: $40-60/month per instance
```

#### Advantages

- **No hardware maintenance** - provider handles physical infrastructure
- **Easy scaling** - spin up more instances as needed
- **Remote access** - work from anywhere with internet
- **Professional infrastructure** - monitoring, backups, networking
- **Rapid deployment** - minutes to provision, not days
- **Elastic resources** - upgrade/downgrade as requirements change

#### Disadvantages

- **Ongoing costs** - $480-720/year vs. one-time hardware purchase
- **Privacy concerns** - operator data on third-party infrastructure
- **API key security** - credentials in cloud environment
- **Network latency** - if coordinating local edge nodes
- **Vendor lock-in** - migration requires effort
- **Limited local model support** - no GPU acceleration on affordable tiers

#### Security Considerations

**Secrets Management**:
- Encrypt API keys at rest (HashiCorp Vault or systemd-creds)
- Separate encryption key stored on operator's device
- Never log or expose credentials
- Rotate keys regularly

**Network Security**:
- VPN tunnel (WireGuard) to operator's devices
- Firewall rules (only SSH + VPN exposed)
- Fail2ban for SSH brute-force protection
- SELinux mandatory access control

**Data Security**:
- Encrypt storage volume (LUKS)
- Separate VPS per operator (no multi-tenancy)
- Regular backups to operator-controlled storage (encrypted)
- Session data never in plain text on provider storage

**Compliance**:
- Choose provider with SOC2, ISO 27001
- Data residency considerations (GDPR if applicable)
- Review provider's access policies

---

### Option 3: Hybrid Edge Architecture (Long-term Vision)

**Concept**: Combine central orchestrator with distributed edge nodes for privacy-preserving, specialized processing.

Based on Edge Computing Architecture research (2026-02-04).

#### Architecture

```
┌──────────────────────────────────────────────┐
│  Central Orchestrator                        │
│  (VPS or Home Server)                        │
│  ├── Primary MESO instance                   │
│  ├── Session history (canonical)             │
│  ├── Genome (version-controlled)             │
│  ├── Complex reasoning (Claude API)          │
│  └── Edge node coordination                  │
└────────────┬─────────────────────────────────┘
             │ MCP Protocol
             │
   ┌─────────┴─────────┬──────────────┬────────────┐
   │                   │              │            │
┌──▼────────────┐ ┌───▼────────┐ ┌──▼──────┐ ┌───▼────────┐
│ Edge Node 1   │ │ Edge Node 2│ │ Edge 3  │ │ Edge N     │
│ (Pi 5)        │ │ (Phone)    │ │ (Jetson)│ │ (Laptop)   │
│               │ │            │ │         │ │            │
│ Local LLM     │ │ Local LLM  │ │ Local   │ │ Local LLM  │
│ (Phi-3 3B)    │ │ (Phi-3 3B) │ │ (13B)   │ │ (7B)       │
│               │ │            │ │         │ │            │
│ Specialized:  │ │ Special:   │ │ Special:│ │ Special:   │
│ - GPIO        │ │ - Thermal  │ │ - GPU   │ │ - Mobile   │
│ - Sensors     │ │ - GPS      │ │ - Vision│ │ - Offline  │
│ - Actuators   │ │ - Mobile   │ │ - Heavy │ │ - Field    │
└───────────────┘ └────────────┘ └─────────┘ └────────────┘
```

#### Central Orchestrator Role

- **Coordination**: Task delegation to appropriate edge nodes
- **Complex reasoning**: Heavy cognitive work via Claude API
- **Canonical state**: Session history, genome, memory
- **Aggregation**: Collect summaries from edge nodes
- **Decision-making**: High-level planning and strategy

#### Edge Node Roles

Each node processes **sensitive data locally**, reports only summaries to orchestrator:

**Raspberry Pi 5** (GPIO, sensor integration):
- Environmental monitoring
- Home automation
- Sensor fusion
- Low-power always-on tasks

**Ulefone Armor 19T Phone** (thermal camera, GPS, mobile):
- Field environmental data collection
- Thermal imaging analysis
- GPS-tagged observations
- Offline-first operation

**Jetson Orin Nano** (GPU acceleration):
- Computer vision tasks
- Heavier local LLM inference (13B models)
- Real-time video analysis
- ML model training

**Laptop** (mobile general-purpose):
- Traveling workstation
- Offline MESO instance
- Development environment
- Sync when online

#### Benefits

- **Privacy**: Sensitive data (thermal images, GPS, local files) stays on edge devices
- **Resilience**: Edge nodes function offline, sync when reconnected
- **Specialization**: Right tool for right job (thermal camera phone for field work, GPU for vision)
- **Cost efficiency**: Only orchestrator needs premium APIs, edge uses local models
- **Latency**: Local processing for time-sensitive tasks

#### Communication Protocol

**MCP (Model Context Protocol)** for orchestrator-edge communication:
- Structured commands only (no direct prompting of edge models - security)
- Request/response pattern
- Status reporting from edge to orchestrator
- Task queuing when edge offline

---

## Persistence & Identity: The Core Problem

**Operator quote**: *"This is a problem of persistence and identity consolidation."*

This is the **central architectural challenge** for MESOcomplete.

### Current State (Claude Code)

**Session Persistence**:
- Sessions stored in internal database
- Linear conversation history
- No branching support
- Resume via session ID (`claude -c`, `claude -r`)
- Handoff notes are manual workaround for continuity

**Identity**:
- CLAUDE.md + rules/*.md define agent identity
- Loaded fresh each session start
- No inter-session memory beyond handoff notes
- Memory project (`~/.claude/projects/-home-Valis/memory/`) is workaround
- Identity is reconstructed each time, not persistent

**Limitations**:
- Cannot explore alternatives without contaminating main session
- Cannot save checkpoints before risky operations
- Manual documentation of state transitions (handoff notes)
- No portable identity across platforms

### What We Need

**Persistent identity across**:

1. **Sessions** - Resume exactly where you left off, context intact
2. **Branches** - Explore alternatives without contaminating main thread
3. **Platforms** - Same MESO identity on Claude Code, Pi, Goose, custom
4. **Instances** - Multiple MESOcomplete devices with shared or independent state
5. **Edge nodes** - Distributed identity, coordinated behavior
6. **Time** - Memory that accumulates, not resets

### Research Questions

#### 1. Session Branching Models

| Model | Description | Storage | Pros | Cons | Inspiration |
|-------|-------------|---------|------|------|-------------|
| **Git-like** | Each branch is a ref pointing to commits, shared history | Merkle tree (content-addressed) | Efficient storage, mature tooling, familiar mental model | Complex implementation, merge conflicts | Git VCS |
| **Pi JSONL trees** | Single append-only file, navigate via message index | JSONL + navigation index | Simple, portable, human-readable | File grows indefinitely, no deduplication | Pi coding agent |
| **Nested sessions** | Parent/child relationships in database | Relational DB (parent_id FK) | Queryable, scalable, ACID guarantees | Lock-in to specific DB, migration complexity | Traditional apps |
| **Event sourcing** | Immutable event log, replay to any point | Append-only event log | Time-travel debugging, complete audit trail | Storage intensive, replay overhead | CQRS pattern |
| **Hybrid DAG** | Directed acyclic graph of session states | Graph database or JSON | Flexible, supports merging, visual tools | Novel implementation, tooling TBD | Novel |

#### 2. Identity Persistence Layers

| Layer | What | How | Where | Sync Strategy |
|-------|------|-----|-------|---------------|
| **Genome** | Core MESO rules, templates, rationale | Version-controlled files (git) | Canonical repo, symlinked or cloned | Pull from upstream, operator approves updates |
| **Zooids** | Always-loaded identity rules | Copied on deploy, instance-specific edits | Instance storage (`~/.meso/zooids/`) | One-way copy, edits stay local |
| **Operons** | Triggered domain knowledge | Copied on deploy OR lazy-loaded from registry | Instance storage or remote fetch | One-way copy or cache with TTL |
| **Memory** | Session-spanning knowledge | Auto-updated markdown files | Instance storage (`~/.meso/memory/`) | Bi-directional sync between instances (conflict resolution needed) |
| **Sessions** | Conversation history | Branching structure (see models above) | Instance storage (`~/.meso/sessions/`) | Local-first, optional sync to archive |
| **State** | Active tasks, context, variables | Ephemeral or serialized | Scratchpad or KV store | Not synced (ephemeral) |
| **Checkpoints** | Saved states (full agent snapshot) | JSON/JSONL with metadata | Instance storage (`~/.meso/checkpoints/`) | Synced to backup, shareable between instances |

#### 3. Cross-Platform Abstraction

To achieve platform-agnostic MESO, we need abstraction layers:

```
┌──────────────────────────────────────────────┐
│         MESO Protocol (Abstract Interface)   │
├──────────────────────────────────────────────┤
│ Session Management                           │
│   - create(config)                           │
│   - branch(session_id, branch_name)          │
│   - merge(source_branch, target_branch)      │
│   - compact(session_id, strategy)            │
│   - checkpoint(session_id, label)            │
│   - restore(checkpoint_id)                   │
├──────────────────────────────────────────────┤
│ Tool Execution                               │
│   - read(file_path)                          │
│   - write(file_path, content)                │
│   - edit(file_path, old, new)                │
│   - bash(command)                            │
│   - custom_tool(tool_name, params)           │
├──────────────────────────────────────────────┤
│ Memory Operations                            │
│   - read_memory(path)                        │
│   - write_memory(path, content)              │
│   - search_memory(query)                     │
│   - append_memory(path, content)             │
├──────────────────────────────────────────────┤
│ Task Management                              │
│   - create_task(subject, desc)               │
│   - update_task(task_id, updates)            │
│   - list_tasks(filters)                      │
│   - get_task(task_id)                        │
├──────────────────────────────────────────────┤
│ Identity Loading                             │
│   - load_genome()                            │
│   - load_zooids()                            │
│   - load_operons(triggers)                   │
│   - get_identity_hash()                      │
└──────────────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
┌───────▼────────┐ ┌──▼──────────┐ ┌▼────────────┐
│ Claude Code    │ │ Pi Adapter  │ │ Goose       │
│ Adapter        │ │ (TypeScript)│ │ Adapter     │
│                │ │             │ │ (MCP)       │
│ - Maps to      │ │ - Extension │ │ - MCP       │
│   Claude tools │ │   API calls │ │   servers   │
│ - Session DB   │ │ - JSONL     │ │ - Prompt    │
│ - Task API     │ │   trees     │ │   injection │
└────────────────┘ └─────────────┘ └─────────────┘
```

**Adapter Responsibilities**:
- Translate abstract MESO operations to platform-specific implementations
- Handle platform limitations gracefully (fallbacks, warnings)
- Report capabilities (supports branching? tasks? custom tools?)
- Ensure behavioral consistency across platforms

#### 4. Saved States / Checkpoints

**Concept**: Like game saves, but for agent state.

**Use Cases**:
- Save before risky refactoring or system changes
- Create restore points for experimentation branches
- Share MESO state between instances (device to device)
- Disaster recovery (corrupted session, lost context)
- Collaboration (send checkpoint to another operator for review)
- Time-travel debugging (what was the agent thinking at this point?)

**Checkpoint Format** (JSON):

```json
{
  "checkpoint_id": "uuid-v4",
  "checkpoint_name": "Before risky refactor",
  "timestamp": "2026-02-05T14:32:00Z",
  "created_by": "operator-handle",

  "session": {
    "session_id": "parent-session-uuid",
    "branch_point": "message-index-42",
    "branch_name": "main",
    "message_count": 42
  },

  "identity": {
    "genome_version": "commit-hash-abc123",
    "loaded_zooids": ["00-operator", "01-standing-orders", "04-security"],
    "loaded_operons": ["orchestration", "knowledge", "math"],
    "operon_versions": {
      "orchestration": "v2",
      "knowledge": "v1",
      "math": "v1"
    }
  },

  "memory_snapshot": {
    "hash": "sha256-of-memory-state",
    "files": [
      {"path": "MEMORY.md", "size": 4821, "hash": "sha256-..."},
      {"path": "decisions/...", "size": 1234, "hash": "sha256-..."}
    ]
  },

  "active_tasks": [
    {
      "task_id": "1",
      "subject": "Implement session branching",
      "status": "in_progress",
      "metadata": {...}
    }
  ],

  "context_summary": "Mid-session during MESO architecture discussion. Researching session branching models. Next: prototype git-like branching.",

  "operator_note": "Checkpoint before attempting to refactor session storage. If it breaks, restore from here."
}
```

**Operations**:
- `checkpoint create <name>` - Save current state
- `checkpoint list` - Show available checkpoints
- `checkpoint restore <id>` - Load state from checkpoint
- `checkpoint export <id> <path>` - Export checkpoint file
- `checkpoint import <path>` - Import checkpoint from file
- `checkpoint delete <id>` - Remove checkpoint

**Storage**:
- Checkpoints stored in `~/.meso/checkpoints/`
- Memory snapshots stored separately (deduplicated)
- Compression (gzip) for storage efficiency
- Retention policy (keep last N, or all manually named)

---

## Novel Approaches to Explore

### 1. Distributed MESO Identity (Blockchain-Inspired)

**Concept**: Genome as a blockchain, instances sync state via consensus.

**Architecture**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Instance A │────▶│  Instance B │────▶│  Instance C │
│  (Laptop)   │     │  (VPS)      │     │  (Pi Edge)  │
│             │     │             │     │             │
│  Genome     │     │  Genome     │     │  Genome     │
│  Chain      │     │  Chain      │     │  Chain      │
│  Block 1..N │◀────│  Block 1..N │◀────│  Block 1..N │
└─────────────┘     └─────────────┘     └─────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                  Gossip Protocol
```

**How It Works**:
- Each MESO instance maintains local copy of genome chain
- Operator commits updates (signed with private key)
- Updates propagate via gossip protocol to all instances
- Instances validate signatures before accepting updates
- Forks allowed for experimentation
- Canonical chain determined by operator's signature

**Benefits**:
- Decentralized (no single point of failure)
- Resilient (instances work offline, sync when reconnected)
- Versioned (complete history, rollback capability)
- Auditable (cryptographic proof of all changes)
- Forkable (experiment without affecting canonical)

**Challenges**:
- Conflict resolution (two instances update simultaneously)
- Storage overhead (full chain history on each instance)
- Network requirements (instances must communicate)
- Complexity (implementing gossip, signature verification)

**Use Cases**:
- Multiple MESOcomplete devices staying synchronized
- Collaborative MESO development (multiple operators)
- Audit trail for compliance (provable genome history)

---

### 2. MESO as Operating System

**Concept**: Don't run MESO on an OS — MESO *is* the OS.

**Philosophy**: Minimal Linux base, everything is a MESO component.

**Stack**:
```
┌──────────────────────────────────────┐
│  MESO Services (PID 1, systemd-like) │
│  ├── Session manager                 │
│  ├── Memory manager                  │
│  ├── Tool executor                   │
│  ├── Operon loader                   │
│  └── API proxy                       │
├──────────────────────────────────────┤
│  Core Services                       │
│  ├── Storage (filesystem)            │
│  ├── Networking (TCP/IP stack)       │
│  ├── Security (SELinux/AppArmor)     │
│  └── Logging                         │
├──────────────────────────────────────┤
│  Minimal Linux Kernel                │
│  └── Alpine / NixOS base             │
└──────────────────────────────────────┘
```

**Characteristics**:
- **Declarative configuration**: Entire system state defined in config files (NixOS-like)
- **Atomic updates**: Genome updates are transactional (all or nothing)
- **Immutable infrastructure**: OS is read-only, state in dedicated volumes
- **Minimal attack surface**: Only MESO services, no unnecessary packages
- **Reproducible builds**: Same config = identical system

**Benefits**:
- Total control over environment
- Minimal bloat (no unused services)
- Security hardening (minimal attack surface)
- Reproducible deployments
- Boot directly into MESO

**Challenges**:
- Significant engineering effort
- Linux kernel/userspace expertise required
- Limited flexibility (purpose-built, not general-purpose)
- Debugging complexity

**Inspiration**:
- NixOS (declarative, reproducible)
- Alpine Linux (minimal base)
- CoreOS (container-optimized)

---

### 3. Session Branches as Git Worktrees

**Concept**: Each session branch is literally a git worktree.

**How It Works**:
```bash
# Main session
~/.meso/sessions/main/

# Create branch (new worktree)
git worktree add ~/.meso/sessions/experimental main

# Work in branch
cd ~/.meso/sessions/experimental
# ... agent modifies files ...

# Merge insights back
cd ~/.meso/sessions/main
git merge experimental

# Or cherry-pick specific changes
git cherry-pick <commit-hash>

# Delete branch
git worktree remove experimental
```

**Session as Git Repository**:
- Each message is a commit
- Files represent session state (tasks, memory snapshots, context)
- Branches are exploration paths
- Merges consolidate learnings
- All git tooling works: diff, blame, log, bisect

**Benefits**:
- **Leverage mature tooling**: Git has decades of development, battle-tested
- **Familiar mental model**: Developers already understand git branching
- **Visual tools**: GitKraken, GitHub Desktop, tig for session visualization
- **Powerful operations**: Rebase, cherry-pick, stash, bisect
- **Distributed**: Sessions can be pushed/pulled between instances

**Challenges**:
- Git is file-based, but sessions are conversational (impedance mismatch)
- Merge conflicts in conversation threads (how to resolve?)
- Binary data (embeddings, model state) doesn't merge well
- Git overhead for very large sessions

**Hybrid Approach**:
- Conversation history: JSONL (append-only, no merges needed)
- Session metadata: Git (branching, checkpoints, annotations)
- Best of both worlds

---

### 4. MESO Memory as Vector Database

**Concept**: Replace file-based memory with embedding search.

**Current**: Memory is markdown files manually organized by topic.

**Proposed**: Memory is embeddings semantically searchable.

**Architecture**:
```
┌─────────────────────────────────────────┐
│  Memory Interface (Abstract)            │
│  - write(content, metadata)             │
│  - search(query, limit)                 │
│  - related(memory_id, limit)            │
│  - forget(memory_id)                    │
│  - fade(age_threshold)                  │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  Vector Database (ChromaDB / Qdrant)    │
│  ├── Embedding model (local)            │
│  ├── Indexed memories                   │
│  ├── Metadata filters                   │
│  └── Similarity search                  │
└─────────────────────────────────────────┘
```

**How It Works**:
1. Agent writes memory: "Operator prefers curated quality over anarchy"
2. System generates embedding (768-dim vector)
3. Stores in vector DB with metadata (date, source, tags)
4. Later, agent searches: "What are operator's architectural preferences?"
5. Semantic search returns relevant memories ranked by similarity
6. No manual file organization required

**Advanced Features**:

**Auto-clustering**:
- Memories naturally cluster by topic
- Discover emergent themes without manual categorization
- Visualize memory landscape (t-SNE plot of embeddings)

**Memory Fade** (biological realism):
- Old memories decay in relevance (time-weighted similarity)
- Frequently accessed memories strengthen (reinforcement)
- Contradicted memories fade faster
- More human-like forgetting

**Related Memories**:
- "Show me memories related to this conversation"
- Automatically surface relevant context
- Connect disparate ideas (emergent insights)

**Benefits**:
- Scales better than file-based (millions of memories)
- Semantic retrieval (meaning, not keywords)
- Emergent organization (no manual filing)
- Biological realism (fade, reinforce, forget)

**Challenges**:
- Embedding model dependency (local or API?)
- Black box (less transparent than markdown files)
- Debugging difficulty (why did it retrieve this?)
- Storage overhead (embeddings + original text)

**Hybrid Approach**:
- Critical knowledge: Markdown files (genome, zooids, operons)
- Session memories: Vector DB (transient, searchable)
- Best of both: curated + emergent

---

### 5. Inter-Instance Communication (Colonial Signaling)

**Concept**: Multiple MESO instances communicate like cells in an organism.

**Biology Analogy**: Cells in a body signal each other via chemical messengers (hormones, neurotransmitters). Coordinated behavior emerges from local interactions.

**MESO Analogy**: Instances signal each other via MCP. Distributed cognition emerges from specialized instances.

**Architecture**:
```
┌────────────┐    ┌────────────┐    ┌────────────┐
│ Security   │───▶│ Coordin.   │───▶│ Web        │
│ Instance   │    │ Instance   │    │ Instance   │
│            │    │            │    │            │
│ Audit logs │    │ Task queue │    │ API calls  │
│ Threat det.│    │ State sync │    │ Data fetch │
└────────────┘    └────────────┘    └────────────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
              MCP Protocol (A2A)
```

**Specialized Instances**:

**Security Instance**:
- Monitors all instances for threats
- Audits tool execution, file access
- Enforces security policies
- Raises alerts to operator

**Coordinator Instance**:
- Task delegation across instances
- State synchronization (shared memory pool)
- Conflict resolution
- Resource allocation

**Web Instance**:
- Handles all external API calls
- Caches responses
- Rate limiting
- Sanitizes external data (prompt injection defense)

**Code Instance**:
- Software development tasks
- Test execution
- Git operations
- Build systems

**Research Instance**:
- Web searches, documentation reading
- Knowledge synthesis
- Long-running background research

**Benefits**:
- **Specialization**: Each instance optimized for domain
- **Isolation**: Compromised instance doesn't affect others
- **Parallelism**: Tasks run concurrently across instances
- **Resilience**: Failure of one instance doesn't crash colony
- **Emergent behavior**: Complex capabilities from simple interactions

**Communication Patterns**:

**Request/Response**:
```
Code Instance → Security Instance: "Can I execute rm -rf ?"
Security Instance → Code Instance: "Denied (destructive)"
```

**Broadcast**:
```
Security Instance → ALL: "Threat detected: prompt injection attempt"
All Instances: Update defensive posture
```

**Pub/Sub**:
```
Research Instance: Publishes new findings to topic "edge-computing"
Code Instance: Subscribed to "edge-computing", receives update
```

**Shared Memory** (like cache coherency):
```
Instance A writes to shared memory: "deployment-target=VPS"
Instance B reads shared memory: "deployment-target=VPS"
Coordinator ensures consistency across instances
```

**Challenges**:
- Message ordering and consistency
- Deadlock prevention
- Network partitions (split-brain)
- Debugging distributed systems

**Inspiration**:
- Actor model (Erlang, Akka)
- Microservices architecture
- Cellular signaling in biology

---

## Immediate Research Priorities

Based on operator's strategic decisions:

### Priority 1: Session Branching Proof of Concept

**Goal**: Demonstrate branching + saved states in Claude Code environment.

**Approach**:
1. Analyze Claude Code's session storage format
2. Build external tool to manipulate session database
3. Prototype branching operations (create, switch, merge)
4. Test checkpoint save/restore
5. Document limitations and workarounds

**Success Criteria**:
- Can create branch from current session
- Can switch between branches without losing context
- Can save checkpoint and restore later
- Can merge insights from branch back to main

**Output**:
- Working prototype (even if hacky)
- Technical documentation of Claude Code session format
- List of limitations and required platform changes
- Recommendations for production implementation

**Estimated Effort**: 2-3 sessions (research + prototype + testing)

---

### Priority 2: Platform Abstraction Layer Design

**Goal**: Define MESO protocol independent of Claude Code.

**Approach**:
1. Catalog all operations MESO performs (session, tools, memory, tasks, identity)
2. Define abstract interface for each operation category
3. Document platform-specific variations (Claude Code, Pi, Goose)
4. Design adapter architecture
5. Identify gaps where platforms lack capabilities

**Success Criteria**:
- Complete API specification for MESO protocol
- Adapter architecture design
- Capability matrix (which platforms support what)
- Migration path for current MESO to abstract protocol

**Output**:
- `MESO-PROTOCOL.md` specification document
- Adapter design diagrams
- Platform capability matrix
- Migration guide

**Estimated Effort**: 3-4 sessions (analysis + design + documentation)

---

### Priority 3: Pi Practices Adoption Roadmap

**Goal**: Steal Pi's best ideas without full migration.

**Approach**:
1. Catalog all Pi features and design decisions
2. Map each to MESO equivalent or gap
3. Evaluate adoption feasibility (effort, benefit, risk)
4. Prioritize adoption candidates
5. Create implementation roadmap

**Features to Evaluate**:
- Session trees (JSONL branching)
- Extension API (TypeScript modules)
- Context loading (AGENTS.md concatenation)
- Compaction strategies
- Multi-provider support
- Package management
- Programmatic SDK

**Success Criteria**:
- Complete feature comparison matrix
- Adoption roadmap with effort estimates
- Risk assessment for each adoption
- Quick wins identified (high value, low effort)

**Output**:
- Pi feature catalog
- MESO gap analysis
- Adoption roadmap (prioritized)
- Implementation tasks

**Estimated Effort**: 2-3 sessions (cataloging + analysis + prioritization)

---

### Priority 4: MESOcomplete Hardware Specification

**Goal**: Define reference hardware for self-hosted deployment.

**Approach**:
1. Benchmark current MESO usage patterns
   - Session I/O (reads/writes per minute)
   - Memory access patterns
   - Network traffic (API calls)
   - Storage growth rate
2. Model resource requirements for multi-session scenarios
3. Research hardware options (mini PC, NUC, custom build)
4. Create bill of materials with cost analysis
5. Write deployment automation (Ansible playbook or container image)

**Success Criteria**:
- Minimum viable hardware spec
- Recommended hardware spec (headroom for growth)
- Premium spec (local LLM inference capable)
- Cost breakdown for each tier
- Automated deployment process

**Output**:
- Hardware spec document (3 tiers: minimal, recommended, premium)
- Bill of materials with vendor links
- Deployment guide (Fedora Server setup)
- Ansible playbook or container images
- Backup/recovery procedures

**Estimated Effort**: 4-5 sessions (benchmarking + research + automation + testing)

---

## Questions for Future Discussion

### 1. Deployment Model
- **Self-hosted hardware**: One-time cost, full control, operator maintains
- **VPS**: Ongoing cost, professional infrastructure, less privacy
- **Hybrid**: Orchestrator on VPS, edge nodes local
- **Multi-instance**: Multiple MESOcomplete devices (home + mobile + edge)

**Operator preference?** (TBD)

---

### 2. Session Branching Implementation
- **Git-like**: Complex but mature tooling, familiar model
- **Pi JSONL trees**: Simple, portable, proven
- **Event sourcing**: Time-travel debugging, audit trail
- **Novel hybrid**: Custom design optimized for MESO

**Which model resonates most?** (TBD - requires research)

---

### 3. Identity Synchronization
- **Shared genome**: All instances pull from canonical repo
- **Independent genomes**: Each instance can diverge (forks)
- **Hybrid**: Core genome shared, instance-specific extensions
- **Blockchain-inspired**: Distributed consensus on updates

**Should multiple MESOcomplete instances share state or be independent?** (TBD)

---

### 4. Local Model Integration
- **Always API**: Simplest, requires internet, ongoing cost
- **Hybrid**: Local for edge/privacy, API for complex reasoning (recommended based on edge research)
- **Always local**: Full sovereignty, requires GPU, setup complexity
- **Dynamic**: Route to local or API based on task type

**Preference for API vs. local models?** (TBD - likely hybrid based on edge research)

---

### 5. Target Audience
- **Personal tool**: Just operator, optimized for individual use
- **Symbiont Systems clients**: Professional product, support required
- **Open source community**: Public release, documentation, community management
- **Commercial product**: Licensing, sales, marketing

**Who is MESOcomplete for?** (TBD - impacts design decisions)

---

### 6. Development Timeline
- **Prototype**: Proof-of-concept in weeks/months
- **MVP**: Minimal viable product in months
- **Product**: Production-ready in 6-12 months
- **Platform**: Full MESO-as-platform in 1-2 years

**What's the timeline expectation?** (TBD)

---

### 7. Licensing & IP
- **Open source**: MIT/Apache, community contributions welcome
- **Source-available**: Code visible, usage restricted
- **Proprietary**: Symbiont Systems IP, no public release
- **Dual-license**: Open core + commercial extensions

**How should MESOcomplete be licensed?** (TBD - operator mentioned IP protection)

---

### 8. Commercial Strategy
- **Free/open**: Community-driven, no revenue
- **SaaS**: Hosted MESOcomplete, subscription model
- **Self-hosted + support**: Sell support/consulting
- **Hardware appliance**: Sell preconfigured MESOcomplete devices

**If commercial, what's the business model?** (TBD)

---

## Related Research

- **Pi Minimalist Agent Architecture** - `pi-minimalist-agent-architecture.md` (session branching, extensions)
- **Edge Computing Architecture** - `edge-computing-architecture.md` (distributed nodes, hybrid orchestrator)
- **MESO Portability Analysis** - MEMORY.md 2026-02-04 (Goose integration, platform-agnostic)
- **MCP as MESO Architecture** - Handoff 2026-02-05 (MCP protocol, immune/nervous system)

---

## Status

**Research Phase**: Architecture exploration complete, strategic decisions partially answered.

**Next Phase**: Prototyping (session branching PoC, platform abstraction design).

**Blocking**: Awaiting operator decisions on deployment model, timeline, target audience, commercial strategy.

**Ready for**: Structured brainstorm session on MESOcomplete as product.

---

*Symbiont Systems LLC — Built with Claude Code*
