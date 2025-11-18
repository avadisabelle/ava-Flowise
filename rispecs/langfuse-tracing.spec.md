# Langfuse Tracing Specification

**Specification Type:** Component Specification
**Document ID:** langfuse-tracing-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** `agentic-flywheel-mcp-app-v1.0`

---

## 🎯 Desired Outcome Definition

### What Users Want to Create

This specification enables users to create a **comprehensive creative archaeology of their AI interactions**, transforming ephemeral conversations into observable, analyzable artifacts. By integrating Langfuse for tracing, we empower users to manifest:

1. **Visible Creative Progression**: The ability to trace every step of their creative journey with AI, seeing how each question and answer builds upon the last, creating a narrative of creative advancement.
2. **Observable Quality Patterns**: The creation of a learning system that reveals which AI flows produce the most valuable insights, enabling continuous improvement through observation rather than guesswork.
3. **Contextual Conversation Threads**: A living map of multi-turn conversations where each interaction is linked to its predecessors, showing the natural progression of thought and inquiry.
4. **Analytical Insight Discovery**: A searchable, analyzable history of all AI interactions that reveals patterns in how teams use AI, what questions drive value, and where creative energy flows most productively.

### Success Indicators

Users know they have achieved their desired outcome when:
- ✅ They can view a complete trace of any conversation in Langfuse, seeing every question, answer, and the flow that handled it
- ✅ They discover that certain flows consistently produce higher-quality responses through observable metrics
- ✅ They can search their entire AI interaction history by keywords, dates, or flows to resurface valuable insights
- ✅ They observe patterns in team questions that inform the creation of new specialized flows
- ✅ They can measure the actual impact of AI assistance through concrete trace data rather than anecdotal evidence

---

## 🏗️ Structural Tension Analysis

### Current Structural Reality

- **Invisible Interactions**: AI conversations happen in the dark. Once a response is delivered, there's no record of what was asked, which flow handled it, or whether it was valuable.
- **Unmeasured Quality**: There's no way to know if a flow is producing excellent results or mediocre ones—quality exists only as a subjective feeling.
- **Fragmented Conversations**: Multi-turn conversations are disconnected events rather than coherent threads, making it impossible to see how context builds over time.
- **Lost Learning Opportunities**: Without traces, teams can't learn from their collective AI interactions, missing opportunities to improve flows or create new specialized agents.

### Desired Structural State

- **Complete Observability**: Every interaction with any Flowise flow automatically creates a trace in Langfuse, capturing the full context of the conversation.
- **Measurable Quality**: Each trace includes quality scores and metadata that enable objective assessment of flow performance.
- **Connected Conversation Threads**: Multi-turn conversations are linked via session IDs, creating coherent narrative threads that show creative progression.
- **Actionable Analytics**: Accumulated trace data reveals patterns that naturally guide improvements, new flow creation, and strategic decision-making.

### Natural Progression Toward Desired State

The structural dynamics of this system create a self-reinforcing cycle of observation and improvement:

1. **Interaction Creates Observation**: A user asks a question, and the system automatically creates a Langfuse trace before executing the query. This trace becomes an observation point.
2. **Execution Enriches the Trace**: As the query flows through intent classification, flow selection, and response generation, each step adds observations to the trace, building a complete picture.
3. **Completion Enables Analysis**: When the response is delivered, the trace is finalized with quality metadata, making it immediately available for analysis.
4. **Observation Drives Improvement**: Over time, accumulated traces reveal which flows excel, which questions are common, and where new capabilities are needed, naturally guiding the system's evolution.

---

## 🏛️ Tracing Architecture

### Core Modules

A new integration layer within `agentic_flywheel/mcp_server.py` will orchestrate Langfuse tracing using the `coaiapy-mcp` tools. The integration will be transparent to users—traces are created automatically without requiring explicit trace management.

### Core Elements

1. **Automatic Trace Creation**: Before any `flowise_query` is executed, a trace is automatically created in Langfuse with a descriptive name derived from the question.
2. **Hierarchical Observation Linking**: Each significant step in the query processing (intent classification, flow selection, execution, response) is captured as an observation nested within the main trace.
3. **Contextual Metadata Capture**: Every trace includes rich metadata: session ID, flow used, intent detected, configuration applied, and execution timing.
4. **Quality Scoring Integration**: Traces support quality scores that can be added after the fact, enabling retrospective evaluation of response value.
5. **Session-Based Threading**: Multi-turn conversations are linked through session IDs, enabling reconstruction of complete conversation threads.

### Integration Points

The integration will occur within `agentic_flywheel/mcp_server.py` in the `handle_call_tool` function, specifically wrapping the `flowise_query` tool execution. The tracing logic will use `coaiapy-mcp` tools to interact with Langfuse.

```python
# Conceptual integration in mcp_server.py

# ... inside handle_call_tool for "flowise_query"

# 1. Create trace before query execution
trace_name = self._generate_trace_name(question)
trace_result = await self._create_trace({
    "name": trace_name,
    "session_id": session_id,
    "metadata": {
        "query": question,
        "timestamp": datetime.now().isoformat()
    }
})
trace_id = trace_result["id"]

# 2. Add observation for intent classification
intent_obs = await self._add_observation({
    "trace_id": trace_id,
    "name": "Intent Classification",
    "input": question,
    "output": {"intent": detected_intent, "confidence": confidence}
})

# 3. Add observation for flow execution
flow_obs_id = await self._start_observation({
    "trace_id": trace_id,
    "name": f"Flow Execution: {flow_name}",
    "input": enriched_query,
    "metadata": {"flow_id": flow_id, "config": config}
})

# 4. Execute the actual query
result = await flowise_server._intelligent_query(...)

# 5. Finalize flow execution observation
await self._finalize_observation({
    "observation_id": flow_obs_id,
    "output": result,
    "metadata": {
        "response_length": len(result.get("text", "")),
        "execution_time_ms": execution_time
    }
})

# 6. Include trace_id in response metadata
result["_mcp_metadata"]["trace_id"] = trace_id

# 7. Return result with trace link
return [types.TextContent(
    text=f"{result['text']}\n\n_Trace ID: {trace_id}_"
)]
```

---

## 🌊 Creative Advancement Scenarios

### Scenario 1: First Query Creates Observable Artifact

**User Intent:** Create understanding of a technical concept through AI assistance.
**Current Structural Reality:** A developer asks their first question to the Agentic Flywheel. No prior traces exist for this session.

**Natural Progression Steps:**
1. **Query Initiation**: The developer asks, "How does React Server Components differ from traditional React?"
2. **Automatic Trace Creation**: Before any processing, the system creates a Langfuse trace named "Technical Query - React Server Components vs Traditional React" with a unique trace ID.
3. **Session Linkage**: The trace is tagged with the newly generated `session_id`, enabling future conversation threading.
4. **Intent Classification Observation**: An observation is added to the trace capturing the intent classification process—input (the question), output (intent: "technical-analysis", confidence: 0.92).
5. **Flow Selection Observation**: Another observation documents which flow was selected ("Technical Analysis") and why (high confidence match, appropriate configuration).
6. **Flow Execution Trace**: The actual query to Flowise is traced with full input (enriched question), configuration (temperature: 0.3), and timing data.
7. **Response Capture**: The LLM's response is captured as the output of the flow execution observation, including response length and any source documents.
8. **Trace Finalization**: The complete trace is finalized in Langfuse, making it immediately available for viewing and analysis.
9. **User Notification**: The response includes a subtle note with the trace ID, enabling users to explore the trace if desired.

**Achieved Outcome:**
- ✅ The developer creates understanding of React Server Components through a detailed, accurate response.
- ✅ A complete observable artifact exists in Langfuse, documenting the entire interaction from question to answer.
- ✅ The foundation for conversation threading is established via the session ID.

---

### Scenario 2: Multi-Turn Conversation Builds Observable Thread

**User Intent:** Create a comprehensive understanding through iterative questioning.
**Current Structural Reality:** The developer from Scenario 1 has a follow-up question to deepen their understanding.

**Natural Progression Steps:**
1. **Continued Conversation**: Five minutes later, the developer asks, "Can you show me a code example of RSC with data fetching?"
2. **Session Continuity**: The same `session_id` is maintained, linking this query to the previous one.
3. **New Trace Creation**: A new trace is created: "Technical Query - RSC Code Example Data Fetching", but it's linked to the previous trace through the shared session ID.
4. **Context Enrichment Observation**: An observation captures how the system enriches the new query with context from the previous interaction (retrieved from Redis cache).
5. **Flow Execution**: The same "Technical Analysis" flow is selected, and execution is traced with the context-enriched query.
6. **Response with Continuity**: The LLM generates a code example that builds on the previous conceptual explanation.
7. **Thread Visibility**: In Langfuse, both traces are now visible as a connected thread when filtering by session ID, showing the natural progression of learning.

**Achieved Outcome:**
- ✅ The developer creates a working code example and deeper understanding through iterative inquiry.
- ✅ A coherent conversation thread exists in Langfuse, showing the creative progression from concept to implementation.
- ✅ Future analysis can identify common question patterns (concept → example) to optimize flows.

---

### Scenario 3: Quality Patterns Emerge Through Observation

**User Intent:** Create better AI assistance by discovering what works.
**Current Structural Reality:** After 30 days, the team has generated 500+ traces across various flows. An administrator wants to understand which flows are most valuable.

**Natural Progression Steps:**
1. **Trace Analysis Query**: The administrator uses Langfuse's interface to view all traces from the last 30 days, filtered by flow.
2. **Quality Pattern Discovery**: By examining traces with high engagement (multiple follow-ups in the same session), they discover that the "Creative Orientation" flow consistently generates 3-5 follow-up questions per session, while "Technical Analysis" averages 1-2.
3. **Response Quality Insights**: Looking at traces where users added quality scores, they observe that "Creative Orientation" has an average score of 4.2/5, while a newer experimental flow only scores 2.8/5.
4. **Common Question Identification**: Text analysis of trace inputs reveals that 40% of questions relate to authentication and authorization—a potential opportunity for a specialized flow.
5. **Configuration Optimization**: Traces show that when "Technical Analysis" uses `temperature: 0.3`, responses are scored higher than when using `temperature: 0.5`.
6. **Strategic Decision**: Based on these observations, the administrator decides to: (a) create a new "Auth & Security" specialized flow, (b) adjust the default temperature for Technical Analysis, and (c) promote the Creative Orientation flow more actively.

**Achieved Outcome:**
- ✅ The administrator creates an evidence-based improvement plan derived from actual usage patterns.
- ✅ Invisible quality patterns become visible and actionable through accumulated trace data.
- ✅ The system naturally evolves toward greater value through observation-driven improvement.

---

## 🔧 Implementation Guidelines

### Trace Naming Strategy

Generate descriptive, searchable trace names automatically:

```python
# In agentic_flywheel/mcp_server.py
def _generate_trace_name(self, question: str, intent: str = None) -> str:
    """Generate a descriptive trace name from the question."""
    # Extract key terms from question (first 5-7 words or key phrases)
    words = question.strip().split()
    key_phrase = " ".join(words[:7]) if len(words) > 7 else question

    # Capitalize and clean
    key_phrase = key_phrase.strip("?!.,").title()

    # Include intent if available
    if intent:
        intent_label = intent.replace("-", " ").title()
        return f"{intent_label} Query - {key_phrase}"

    return f"AI Query - {key_phrase}"
```

### Observation Hierarchy

Create a clear hierarchy of observations within each trace:

1. **Top Level**: Main trace representing the entire query
   - **Level 1**: Intent Classification (input: question, output: intent + confidence)
   - **Level 1**: Flow Selection (input: available flows, output: selected flow + reason)
   - **Level 1**: Flow Execution (input: enriched query + config, output: response)
     - **Level 2**: Cache Check (input: cache key, output: hit/miss)
     - **Level 2**: LLM Generation (if cache miss - input: prompt, output: raw response)
     - **Level 2**: Response Formatting (input: raw response, output: formatted result)

### Metadata Standards

Include comprehensive metadata in traces and observations:

**Trace-Level Metadata:**
```json
{
  "session_id": "mcp-session-1762589999-abcdef12",
  "user_agent": "claude-desktop",
  "timestamp": "2025-11-18T14:30:22Z",
  "environment": "production"
}
```

**Observation-Level Metadata:**
```json
{
  "flow_id": "896f7eed-342e-4596-9429-6fb9b5fbd91b",
  "flow_key": "technical-analysis",
  "flow_name": "Technical Analysis",
  "config_used": {
    "temperature": 0.3,
    "maxOutputTokens": 2000,
    "returnSourceDocuments": true
  },
  "execution_time_ms": 1847,
  "cache_hit": false,
  "response_length": 1523
}
```

### Integration with coaiapy-mcp

Use the `coaiapy-mcp` tools for Langfuse interaction:

```python
# Create trace
coaia_fuse_trace_create(
    name="Technical Query - OAuth Implementation",
    session_id="mcp-session-123",
    metadata={"query": "...", "timestamp": "..."}
)

# Add observation
coaia_fuse_add_observation(
    trace_id="trace-uuid-123",
    name="Flow Execution: Technical Analysis",
    input={"question": "...", "config": {...}},
    output={"response": "...", "sources": [...]},
    metadata={"execution_time_ms": 1847}
)

# Update trace with final metadata
coaia_fuse_trace_update(
    trace_id="trace-uuid-123",
    metadata={"total_observations": 5, "status": "completed"}
)
```

### Error Handling and Resilience

Tracing must never break the core functionality:

```python
# Wrap tracing in try-except
try:
    trace_id = await self._create_trace(...)
    await self._add_observation(...)
except Exception as trace_error:
    # Log the tracing error but continue with query
    logger.warning(f"Langfuse tracing failed: {trace_error}")
    trace_id = None  # Mark as no trace available

# Always execute the core query, even if tracing fails
result = await flowise_server._intelligent_query(...)

# Attempt to finalize trace, but don't fail if it errors
if trace_id:
    try:
        await self._finalize_observation(...)
    except Exception as finalize_error:
        logger.warning(f"Trace finalization failed: {finalize_error}")
```

---

## 🧪 Quality Validation

### Success Metrics

- **Trace Coverage**: Achieve 100% trace creation for all `flowise_query` executions (allowing for graceful failure if Langfuse is unavailable).
- **Observation Completeness**: Every trace includes a minimum of 3 observations (intent classification, flow selection, flow execution).
- **Session Threading**: 95%+ of multi-turn conversations are correctly linked via session ID in Langfuse.
- **Performance Impact**: Tracing overhead adds <100ms to total query execution time.
- **Metadata Richness**: 100% of traces include all required metadata fields (session_id, flow_id, flow_key, config, execution_time).

### Testing Scenarios

- **Single Query Trace**: Verify that a single `flowise_query` creates a trace with the correct name, session ID, and at least 3 observations.
- **Multi-Turn Threading**: Verify that 3 consecutive queries with the same `session_id` create 3 separate traces that are all linked when filtering by session in Langfuse.
- **Metadata Accuracy**: Verify that the metadata captured in observations matches the actual flow used, config applied, and execution time measured.
- **Error Resilience**: Verify that if Langfuse is unavailable, queries still execute successfully (tracing fails gracefully).
- **Cache Integration**: Verify that traces for cache hits include `cache_hit: true` metadata and show reduced execution time.

---

## 🔗 Integration References

- **coaiapy-mcp Tools**: The implementation will use `coaia_fuse_trace_create`, `coaia_fuse_add_observation`, and `coaia_fuse_trace_update` as described in `__llms/llms-coaiapy-cli-guide.md` and `__llms/llms-coaiapy-mcp-config-guide.md`.
- **Master Specification**: This component directly enables "Scenario 1: First-Time User Queries Technical Question" in `rispecs/app.spec.md` by creating the observability layer.
- **Redis Storage Integration**: Trace IDs must be included in cached responses (`redis-storage.spec.md`) to maintain the connection between cached data and its original trace.
- **Intent Classification Integration**: The intent classification component (`intent-classification.spec.md`) must provide its output to be captured in traces as observations.
- **MCP Server Integration**: The MCP server specification (`mcp-server.spec.md`) must document that all `flowise_query` responses include a `trace_id` in their metadata.

---

## 🎯 Agent Delegation Plan for Implementation

### Phase 1: Core Tracing Module (python-pro)

**Task**: Create automatic trace creation and observation management

**Agent**: `python-pro` (Python specialist)

**Deliverable**: Modified `agentic_flywheel/mcp_server.py` with integrated tracing

**Implementation Steps**:
1. Import `coaiapy-mcp` tools for Langfuse interaction
2. Create `_generate_trace_name()` helper function
3. Create `_create_trace()` wrapper around `coaia_fuse_trace_create`
4. Create `_add_observation()` wrapper around `coaia_fuse_add_observation`
5. Modify `handle_call_tool()` for "flowise_query" to wrap execution with tracing
6. Add error handling to ensure tracing failures don't break queries
7. Include `trace_id` in response metadata

### Phase 2: Metadata Enrichment (backend-architect)

**Task**: Ensure comprehensive metadata capture in all traces

**Agent**: `backend-architect` (System design specialist)

**Deliverable**: Enhanced tracing with full observation hierarchy

**Implementation Steps**:
1. Audit all query processing steps that should be traced
2. Add observations for: intent classification, flow selection, cache check, LLM generation
3. Ensure consistent metadata schemas across all observations
4. Add timing instrumentation for performance measurement
5. Validate session ID threading across multi-turn conversations

### Phase 3: Validation & Quality Assurance (architect-review)

**Task**: Validate tracing implementation and RISE compliance

**Agent**: `architect-review` (Quality assurance specialist)

**Deliverable**: Validated, production-ready tracing system

**Validation Checklist**:
1. Verify 100% trace coverage for all query executions
2. Confirm graceful degradation when Langfuse is unavailable
3. Validate metadata completeness and accuracy
4. Test multi-turn conversation threading
5. Measure performance impact (<100ms overhead requirement)
6. Review code for advancing patterns and structural soundness

---

**Status:** Ready for Implementation
**Next Step:** Assign to `python-pro` for Phase 1 development
