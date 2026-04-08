# Prompt Decomposition: Flowise AgentFlow Node Specification

**Specification Type:** Platform Integration Specification
**Document ID:** `rispecs/prompt-decomposition/prompt-decomposition.spec.md`
**Framework:** RISE (Reverse-engineer → Intent-extract → Specify → Export)
**Platform:** Flowise (Node.js)
**Node Location:** `packages/components/nodes/agentflow/PromptDecomposition/`

---

## Desired Outcome Definition

### What Users Want to Create

Flowise users want to **visually compose prompt decomposition into their agent workflows** through a drag-and-drop node that:

1. **Accepts any prompt** — Free-text input in the AgentFlow canvas
2. **Decomposes through Four Directions** — EAST(Vision), SOUTH(Analysis), WEST(Validation), NORTH(Action)
3. **Outputs structured results** — JSON, Markdown, or raw action stack format
4. **Exposes relational metadata** — Balance score, lead direction, ceremony requirements, neglected directions
5. **Integrates with downstream nodes** — Output feeds into LLM chains, conditionals, or other AgentFlow nodes

### Success Indicators

- ✅ Node appears in the "Agent Flows" category with purple color and appropriate tags
- ✅ Users can configure output format, implicit intent extraction, max actions, and ceremony threshold
- ✅ Output includes both the formatted decomposition AND relational metadata
- ✅ The node works with `ava-langchain-prompt-decomposition` package via dynamic import
- ✅ Clear error message if the PDE package is not installed

---

## Structural Tension Analysis

### Current Structural Reality

The node is implemented as `PromptDecomposition_Agentflow` implementing the Flowise `INode` interface:

**Node Configuration:**
| Property | Value |
|----------|-------|
| `name` | `promptDecompositionAgentflow` |
| `label` | Prompt Decomposition |
| `type` | PromptDecomposition |
| `category` | Agent Flows |
| `color` | `#8B5CF6` (violet) |
| `tags` | Relational Intelligence, Medicine Wheel, PDE |
| `version` | 1.0 |

**Inputs:**
| Input | Type | Default | Description |
|-------|------|---------|-------------|
| `prompt` | string (4 rows) | — | The prompt to decompose |
| `outputFormat` | options | json | JSON, Markdown, or Action Stack Only |
| `includeImplicit` | boolean | true | Extract hidden/implicit requirements |
| `maxActions` | number | 20 | Maximum actions in the stack |
| `ceremonyThreshold` | number | 0.3 | Ceremony sensitivity (0-1) |

**Output Structure:**
```json
{
  "id": "node-id",
  "name": "promptDecompositionAgentflow",
  "input": { "prompt": "..." },
  "output": {
    "decomposition": "...(formatted per outputFormat)",
    "balance": 0.75,
    "leadDirection": "north",
    "neglectedDirections": ["west"],
    "ceremonyRequired": false,
    "relationalCoverage": 0.6,
    "actionCount": 5,
    "primaryIntent": { "action": "create", "target": "...", "urgency": "session", "confidence": 0.85 }
  }
}
```

### Natural Progression Within Flowise

The PromptDecomposition node advances the user's workflow by:
1. **Receiving** a raw prompt from a Start node or user input
2. **Decomposing** it into structured directional analysis
3. **Forwarding** the structured output to downstream nodes (LLM Agent, Condition, or custom logic)
4. **Enabling** conditional branching based on `ceremonyRequired`, `balance`, or `leadDirection`

---

## Functional Specification

### Execution Flow

1. Read inputs from `nodeData.inputs`
2. Dynamically import `ava-langchain-prompt-decomposition` (throws clear error if missing)
3. Instantiate: DirectionalDecomposer → IntentExtractor → DependencyMapper → ActionStackBuilder → MedicineWheelBridge
4. Run pipeline: decompose → extract → buildGraph → computeExecutionOrder → build → enrich
5. Format output per `outputFormat` selection
6. Return structured result with metadata

### Error Handling

- Missing prompt → `Error('Prompt is required for decomposition')`
- Missing PDE package → `Error('ava-langchain-prompt-decomposition is not installed...')`
- Pipeline errors bubble up with stack trace

---

## Integration Points

### Dependencies
- `ava-langchain-prompt-decomposition` (dynamic import) — Core PDE primitives

### Works With
- **Start Node**: Receives initial prompt input
- **LLM Agent Node**: Forwards decomposition to guide LLM responses
- **Condition Node**: Branch on `ceremonyRequired` or `balance` thresholds
- **StickyNote**: Display decomposition markdown for human review

---

## User Presentation

### In the Flowise Canvas

The node appears as a violet-colored block in the "Agent Flows" category sidebar. When dragged onto the canvas:
- Left side: Input handle for connecting prompt sources
- Center: Configurable properties panel with all 5 inputs
- Right side: Output handle carrying the full decomposition result

### For New Users

Users find the node by:
1. Opening the "Agent Flows" node palette
2. Searching for "Prompt Decomposition" or browsing the Relational Intelligence tags
3. Dragging it onto the canvas and connecting a prompt source
4. Configuring output format and sensitivity thresholds
5. Connecting the output to downstream processing nodes
