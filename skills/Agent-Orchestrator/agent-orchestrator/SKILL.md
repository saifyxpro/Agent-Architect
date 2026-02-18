---
name: agent-orchestrator
description: Design and implement multi-agent systems with proven coordination patterns. Use when building agent teams, delegation architectures, inter-agent communication, lead-agent orchestration, or agent swarm coordination. Covers 5 orchestration topologies (hub-and-spoke, pipeline, broadcast, hierarchical, mesh), delegation protocols, state sharing across agent boundaries, conflict resolution, and the plan-and-execute pattern. Based on patterns from Kimi Agent Swarm, Devin, BabyAGI, MetaGPT, Google A2A, and DyLAN architectures.
---

# Agent Orchestrator

Design multi-agent systems with proven coordination and delegation patterns.

## Workflow

### Design Workflow

1. Identify the task domain and decompose into agent roles
2. Select an orchestration topology from the topology guide
3. Define inter-agent communication protocol
4. Implement delegation rules and conflict resolution
5. Add observability and fallback handling

### Evaluation Workflow

1. Map existing multi-agent system to topology patterns
2. Check for single points of failure
3. Verify delegation boundaries and escalation paths
4. Score against the orchestration checklist

## Orchestration Topologies

Five topologies for multi-agent coordination. Read the relevant reference for templates.

| # | Topology | When to Use | Reference |
|---|----------|-------------|-----------|
| 1 | Hub-and-Spoke | Single coordinator delegates to specialists | `references/01-hub-and-spoke.md` |
| 2 | Pipeline | Sequential processing with handoff gates | `references/02-pipeline.md` |
| 3 | Broadcast | Parallel execution with result aggregation | `references/03-broadcast.md` |
| 4 | Hierarchical | Multi-level delegation with sub-coordinators | `references/04-hierarchical.md` |
| 5 | Mesh | Peer-to-peer collaboration with shared state | `references/05-mesh.md` |

## Topology Selection Guide

**Customer service system** (triage → route → resolve):
→ Topology 1 (Hub-and-Spoke) with triage coordinator

**Data processing pipeline** (extract → transform → validate → load):
→ Topology 2 (Pipeline) with validation gates between stages

**Code review system** (multiple reviewers in parallel):
→ Topology 3 (Broadcast) with consensus aggregation

**Enterprise workflow** (departments with sub-teams):
→ Topology 4 (Hierarchical) with department-level coordinators

**Collaborative research** (agents share findings dynamically):
→ Topology 5 (Mesh) with shared knowledge graph

## Agent Role Definition Template

When defining agent roles, specify:

```
<agent name="[NAME]" role="[ROLE]">
  <capabilities>
    - [Specific capability 1]
    - [Specific capability 2]
  </capabilities>
  <boundaries>
    - Cannot [limitation 1]
    - Cannot [limitation 2]
  </boundaries>
  <inputs>[What this agent receives]</inputs>
  <outputs>[What this agent produces]</outputs>
  <escalation>[When and how to escalate to coordinator]</escalation>
</agent>
```

## Inter-Agent Communication Protocol

### Message Format

```
<agent_message>
  <from>[sender_agent]</from>
  <to>[receiver_agent]</to>
  <type>[request|response|broadcast|escalation]</type>
  <payload>[structured data]</payload>
  <context>[relevant state for receiver]</context>
  <priority>[low|normal|high|critical]</priority>
</agent_message>
```

### Delegation Rules

- Coordinator MUST include task context in every delegation
- Worker agents MUST report completion status back to coordinator
- Failed tasks MUST include error details and partial results
- Escalation MUST happen when confidence drops below threshold

## Conflict Resolution

When multiple agents produce conflicting outputs:

1. **Voting** — majority wins (use for low-stakes decisions)
2. **Authority** — designated expert agent decides (use for domain-specific conflicts)
3. **Escalation** — human-in-the-loop resolves (use for high-stakes ambiguity)
4. **Synthesis** — coordinator merges compatible parts (use when outputs are complementary)

## Anti-Patterns

- **God Agent** — one agent does everything, others are stubs
- **Chat Loop** — agents endlessly request clarification from each other
- **State Amnesia** — agents lose context between interactions
- **Over-delegation** — breaking tasks too fine, coordination cost exceeds benefit
- **Missing Fallback** — no recovery path when a worker agent fails

## Validation Scripts

Validate orchestration topology configs with automated scoring (0-10):

```bash
python3 scripts/validate_topology.py <config_file> [--strict]
```

Checks topology detection, agent count, required sections (roles, routing, communication, error handling), and flags anti-patterns (SPOF, deadlocks, shared mutable state).
