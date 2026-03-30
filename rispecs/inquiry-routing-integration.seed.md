# SEED — Inquiry Routing Integration for ava-Flowise

> Status: 🌱 Seed (future-oriented, not an implementation spec)
> Upstream: `ava-langchain-inquiry-routing@0.1.0`, `ava-langgraph-inquiry-routing-engine@0.1.0`

## Desired Outcome

ava-Flowise exposes inquiry routing as visual Flowise nodes — users can drag-and-drop an `InquiryRoutingGraph` node into their flow, connecting it downstream of a PDE decomposition node. The Flowise node wraps both the chain-level primitives (`ava-langchain-inquiry-routing`) and the graph engine (`ava-langgraph-inquiry-routing-engine`), surfacing `ceremony_hold` as a visible pause in the flow editor.

## Current Reality

- ava-Flowise has existing node infrastructure for PDE (`rispecs/prompt-decomposition/`)
- No inquiry routing nodes exist
- Flowise's node system can wrap LangChain/LangGraph components but requires adapter code for state management

## Structural Tension

The inquiry-routing packages are library code; Flowise needs *visual nodes* with input/output sockets. The tension between library abstraction and visual-flow concreteness resolves through adapter nodes that expose `InquiryRoutingState` fields as Flowise socket connections.

## Integration Path

1. **Add dependencies to Flowise node package:**
   - `ava-langchain-inquiry-routing: >=0.1.0`
   - `ava-langgraph-inquiry-routing-engine: >=0.1.0`

2. **Create Flowise nodes:**
   - `InquiryGeneratorNode` — wraps `InquiryGenerator`, input: `DecompositionResult`, output: `InquiryBatch`
   - `InquiryRouterNode` — wraps `InquiryRouter`, input: `InquiryBatch`, output: `RoutedInquiryBatch`
   - `InquiryRoutingGraphNode` — wraps full `InquiryRoutingGraph`, input: `DecompositionResult`, output: `InquiryRoutingState`

3. **Ceremony hold UI:** When `state.ceremonyRequired === true`, surface a visual indicator in the Flowise canvas — the flow pauses and awaits human input

4. **Dispatch outputs:** Each `FormattedDispatch` type maps to a Flowise output socket:
   - `QmdDispatch` → QMD search node input
   - `DeepSearchDispatch` → deep-search node input
   - `WorkspaceScanDispatch` → workspace scan node input

5. **Config panel:** Expose `InquiryRoutingConfig` and `RelationalValidatorOptions` as node configuration in the Flowise properties panel

## RISE Compliance

| Phase | Status |
|-------|--------|
| **R**everse-engineer | 🌱 Pending — analyze Flowise node adapter patterns from existing PDE nodes |
| **I**ntent-extract | 🌱 Seed — intent is visual-flow inquiry routing with ceremony_hold as visible pause |
| **S**pecify | 🌱 This seed |
| **E**xport | ⏳ Not started |
