# Edge Computing Architecture Research

**Date:** 2026-02-04
**Context:** MESO colony expansion via distributed edge nodes
**Status:** Research complete, implementation planning

## Executive Summary

Distributed AI architecture using central orchestrator (Claude/DeepSeek) with local edge LLMs on development boards and mobile devices. Enables privacy-preserving local processing with sensitive data never leaving operator control, while maintaining sophisticated reasoning capability through cloud orchestrator.

## Architecture Overview

```
Operator ←→ Central LLM (Claude/DeepSeek)
                ↓
          MCP Protocol
                ↓
    ┌───────────┴────────────┬──────────────┐
    ↓                        ↓              ↓
Pi/Jetson (system)    Phone (mobile)    Mini PC (build)
Mistral 7B            Phi-3 3B          Qwen 14B
```

**Central Orchestrator:**
- Complex reasoning and planning
- Natural language interface with operator
- Dispatches work to edge nodes
- Security boundary - only direct operator interface
- Synthesizes results from distributed processing

**Edge Nodes:**
- Domain-specific processing
- No direct prompting (only structured commands from orchestrator)
- Operate on sensitive local data
- Return structured results only
- Specialized by hardware and task

## Security Model

**Major advantages over single-model approach:**

1. **No prompt injection on edge devices** - structured commands only
2. **Constrained capabilities** - limited tool access per domain
3. **Data compartmentalization** - sensitive data processed locally
4. **Single trust boundary** - operator → orchestrator → authenticated edge nodes
5. **Audit trail** - all operations logged centrally

## Hardware Research

### Development Boards

| Device | CPU/GPU | RAM | Best For | Cost | Performance |
|--------|---------|-----|----------|------|-------------|
| Raspberry Pi 5 | ARM A76 | 8GB | Entry point, basic tasks | $80 | 3B: 10-20 t/s, 7B: 2-5 t/s |
| Jetson Orin Nano | ARM + GPU | 8GB | Vision, GPU tasks | $300 | 7B: 15-25 t/s, 13B: 5-10 t/s |
| Mini PC + RTX 3060 | x86 + GPU | 16GB+ | Serious inference | $500+ | 13B: 20-40 t/s, 34B: 10-15 t/s |

**Token/sec (t/s) = inference speed**

### Model Quality Comparison

| Size | Quality vs Claude | Practical Use Case |
|------|-------------------|-------------------|
| 1-3B | Below GPT-3 | Classification, extraction |
| 7B | ~GPT-3.5 simple tasks | Log parsing, commands, basic Q&A |
| 13B | GPT-3.5 to Claude 3 | Code review, docs, reasoning |
| 34B | ~Claude 3.5 Haiku | Most development tasks |
| 70B | ~Claude 3.5 Sonnet | Complex reasoning, architecture |

### Mobile Edge Node: Ulefone Armor 19T

**Specifications:**
- MediaTek Helio G99 (Mali G57 GPU)
- 12GB RAM (expandable to 17GB virtual)
- 256GB storage
- 9600mAh battery (3x normal phone capacity)
- Android 12
- IP68 waterproof, MIL-STD-810H rugged

**Special Sensors:**
- **FLIR Lepton 3.5 thermal camera** (160x120 resolution, -10°C to 400°C)
- 108MP main camera (Samsung ISOCELL HM2)
- GPS, accelerometer, gyroscope, barometer, compass

**LLM Performance:**
- Phi-3 (3.8B): 10-15 tokens/sec - actually usable
- Gemma 2 (2B): 15-25 tokens/sec - fast but limited
- Llama 3.2 (3B): 8-12 tokens/sec - good balance
- Mistral 7B (4-bit): 3-5 tokens/sec - usable for some tasks

**Thermal Reality:**
- Burst inference: works well for short tasks
- Sustained inference: 3-5 hours possible (vs 30-60min normal phones)
- Background processing: significant battery drain but manageable

## Thermal Camera Integration

### FLIR SDK Access

**Official SDK exists:** FLIR Mobile SDK for Android
- Supports Ulefone devices (20T Mini, 27T Pro confirmed)
- 19T support unclear - same Lepton 3.5 sensor, needs verification
- Developer portal: developer.flir.com (registration required)
- Provides full radiometric access (temperature values per pixel)

**Sources:**
- [FLIR Mobile SDK for Ulefone](https://www.flir.com/developer/developer-mobile-sdk/)
- [FLIR Developer Program](https://www.flir.com/developer/mobile-sdk/)
- [SDK Download Instructions](https://flir.custhelp.com/app/answers/detail/a_id/1748/)

### Alternative Access Methods

1. **Android Camera2 API** - generic thermal camera access (may lack radiometric data)
2. **MyFLIR app automation** - trigger via intents, process saved files
3. **Direct file access** - if thermal images save with embedded temperature data

### Thermal Camera Use Cases

**Environmental Monitoring:**
- Soil temperature gradients
- Water stress in vegetation (thermal signature)
- Wildlife census (heat signatures)
- Microclimate analysis

**Infrastructure/Trades:**
- Building envelope inspection
- Electrical panel diagnostics
- HVAC efficiency assessment
- Insulation quality verification
- Water leak detection

**Agricultural:**
- Crop health monitoring
- Irrigation effectiveness
- Livestock health screening
- Frost risk assessment

**Workshop:**
- Equipment overheating detection
- Welding quality assessment
- Material temperature verification
- Safety monitoring

## Proposed Custom Thermal App Architecture

```
┌─────────────────────────────────┐
│  Custom Thermal Analysis App   │
├─────────────────────────────────┤
│  UI Layer (Jetpack Compose)    │
│   ├─ Live thermal preview       │
│   ├─ Capture controls           │
│   ├─ Analysis display           │
│   └─ Observation log            │
├─────────────────────────────────┤
│  Processing Layer               │
│   ├─ FLIR SDK (thermal)         │
│   ├─ Camera2 (visible)          │
│   ├─ GPS/sensors                │
│   └─ llama.cpp JNI binding      │
├─────────────────────────────────┤
│  LLM Analysis Engine            │
│   ├─ Phi-3 for fast analysis    │
│   ├─ LLaVA for vision tasks     │
│   └─ Prompt templates           │
├─────────────────────────────────┤
│  Data Layer                     │
│   ├─ SQLite observation log     │
│   ├─ Image storage              │
│   └─ Sync queue                 │
├─────────────────────────────────┤
│  Network Layer                  │
│   ├─ MCP server interface       │
│   ├─ REST API                   │
│   └─ Tailscale integration      │
└─────────────────────────────────┘
```

### Planned Features

**Core:**
- Dual capture (thermal + visible simultaneously)
- Live thermal preview with temperature overlay
- GPS tagging with timestamp
- Offline-first operation

**LLM Integration:**
- On-device Phi-3 analysis of thermal patterns
- Custom prompt templates by task type
- Structured JSON output for orchestrator
- Background analysis queue

**Orchestrator Integration:**
- MCP server for Claude queries
- Background sync to home server
- Remote capture triggering
- Query interface for historical data

**Field Optimizations:**
- Volume button quick capture
- Voice annotation (hands-free)
- Custom workflow templates
- GeoJSON export for GIS integration

## Model Context Protocol (MCP)

**Why it's perfect for this architecture:**
- Designed for LLM-to-tool communication
- Supports remote tool execution
- JSON-RPC based, lightweight
- Security via authentication tokens
- Already researched for Linux system integration

**Existing work:** Red Hat Linux MCP server provides system diagnostics interface - proof of concept that this architecture works.

## Implementation Phases

### Phase 1: Hardware Setup
- Acquire dev board (Pi 5 or Jetson Orin recommended)
- Install Ollama/llama.cpp
- Deploy test models (Phi-3, Mistral 7B)
- Verify inference performance

### Phase 2: Phone Setup (Parallel)
- Register for FLIR developer program
- Verify 19T SDK support
- Test Camera2 API access as fallback
- Install Termux + llama.cpp
- Test basic thermal capture + analysis

### Phase 3: MCP Integration
- Set up MCP server on edge nodes
- Configure Claude to use edge tools
- Test orchestrator → edge communication
- Implement authentication and security

### Phase 4: Custom Thermal App
- Build minimal capture app
- Integrate local LLM analysis
- Add MCP server interface
- Deploy to phone for field testing

### Phase 5: Production Hardening
- Battery optimization
- Error handling and retry logic
- Offline queue and sync
- Monitoring and logging

## Technology Stack

**Edge Devices:**
- OS: Linux (dev boards), Android (phone)
- LLM Runtime: llama.cpp (C++, portable, efficient)
- Models: Phi-3 (3B), Mistral 7B, Llama 3.1 (7/13B), Qwen 2.5 (14B)
- Quantization: 4-bit GGUF format for mobile/edge

**Mobile App:**
- Language: Kotlin
- UI: Jetpack Compose
- Camera: FLIR SDK + Camera2 API
- LLM: llama.cpp with JNI bindings
- Storage: SQLite
- Networking: Tailscale, MCP protocol

**Infrastructure:**
- Orchestrator: Claude API (current), DeepSeek V3 (future self-hosted option)
- Protocol: Model Context Protocol (MCP)
- Networking: Tailscale for secure device mesh
- Sync: Home server (location TBD)

## Privacy and Data Flow

**Sensitive data stays local:**
- System logs, credentials → processed on local dev board
- Thermal imagery, GPS → processed on phone
- Only analysis results/summaries sent to orchestrator

**Two-tier trust model:**
1. **Operator ↔ Orchestrator** - full natural language, high trust
2. **Orchestrator ↔ Edge nodes** - structured commands only, authenticated

**Data never leaves operator control:**
- Local processing on operator-owned hardware
- Cloud orchestrator sees only derived/summarized data
- Original sensitive data stays on edge devices

## Strategic Value

**Compared to single cloud LLM:**
1. Privacy - sensitive data local
2. Cost - bulk processing on local hardware
3. Latency - real-time local inference
4. Resilience - offline capable
5. Specialization - domain-optimized models
6. Security - reduced attack surface

**Compared to fully local:**
1. Reasoning quality - Claude for complex tasks
2. No massive hardware investment for 70B+ models
3. Hybrid approach - local for routine, cloud for hard problems

## MESO Integration

**Maps perfectly to colonial organism model:**

- **Central LLM** = nucleus/brain (Claude)
- **Edge models** = specialized organelles (mitochondria, chloroplasts)
- **MCP** = cellular signaling pathways
- **Operator** = organism directing colony

**Each edge node is a zooid:**
- Specialized function
- Cannot survive independently
- Integrated into colony
- Responds to central nervous system

**Phone as mobile gastrozooid:**
- Forages for data in environment
- Processes locally
- Reports findings to colony

## Next Actions

1. **FLIR SDK verification** - register, check 19T support
2. **Dev board selection** - decide on Pi 5 vs Jetson Orin based on budget/needs
3. **Phone setup** - Termux + llama.cpp baseline installation
4. **Proof of concept** - build thermal field logger on phone
5. **MCP server** - implement basic server on one edge device
6. **Orchestrator test** - connect Claude to first edge node

## References

**Device Specifications:**
- [Ulefone Armor 19T Specs - GSMArena](https://www.gsmarena.com/ulefone_power_armor_19t-12194.php)
- [Ulefone Power Armor 19T Official](https://www.ulefone.com/products/power-armor-19t)
- [FLIR Lepton 3.5 Details](https://www.devicespecifications.com/en/news/a56114dd)

**SDK and Development:**
- [FLIR Mobile SDK Portal](https://www.flir.com/developer/developer-mobile-sdk/)
- [FLIR Lepton Integration Guide](https://oem.flir.com/developer/lepton-family/)
- [GitHub - Lepton Module Code](https://github.com/groupgets/LeptonModule)

**Model Context Protocol:**
- Red Hat Linux MCP server research (see auto memory 2026-02-04)
- MCP specification (to be added)

## Decision Log

**2026-02-04:** Validated edge computing architecture for MESO expansion. Ulefone Armor 19T confirmed as excellent mobile edge node (12GB RAM, FLIR thermal, rugged, massive battery). FLIR SDK access to be verified. Development board recommendation: Jetson Orin Nano for serious work, Pi 5 for budget testing.

**Architecture decision:** Separation of concerns - local edge for sensitive data processing, cloud orchestrator for complex reasoning. Privacy preserved, capabilities maximized.
