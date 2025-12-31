# Redis Storage Specification

**Specification Type:** Component Specification
**Document ID:** redis-storage-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** `agentic-flywheel-mcp-app-v1.0`

---

## 🎯 Desired Outcome Definition

### What Users Want to Create

This specification enables users to create a **persistent and cumulative knowledge base** from their interactions with the Agentic Flywheel MCP. By integrating Redis for storage, we empower users to manifest:

1.  **Continuous, Uninterrupted Conversations**: The ability to resume a conversation at any time, with the system recalling all prior context, as if no time has passed.
2.  **Instantaneous Insight Retrieval**: The creation of a "second brain" where previously generated answers and insights are retrieved instantly, accelerating learning and decision-making.
3.  **A Compounding Institutional Memory**: A shared, searchable history of questions and answers that grows more valuable with every interaction, allowing the entire team to benefit from collective intelligence.
4.  **An Efficient Creative Ecosystem**: An environment where computational resources are preserved by avoiding redundant queries, allowing energy to be focused on novel, creative exploration.

### Success Indicators

Users know they have achieved their desired outcome when:
- ✅ They can pick up a conversation thread from two days ago, and the AI has perfect recall of the context.
- ✅ Common questions asked by new team members are answered instantly, without waiting for an LLM to generate a response.
- ✅ A project manager can search for all historical conversations tagged with a specific project to build a knowledge brief.
- ✅ The system feels faster and more responsive over time as the cache becomes more populated with relevant knowledge.

---

## 🏗️ Structural Tension Analysis

### Current Structural Reality

- **Ephemeral Sessions**: Each conversation is isolated. When a session ends, its context and generated knowledge are lost.
- **Redundant Computation**: The same or similar questions are repeatedly processed by the underlying LLMs, consuming unnecessary time and resources.
- **Fragmented Knowledge**: Insights are scattered across individual user sessions and are not centrally accessible or searchable.
- **Static Response Times**: The time to get an answer is always dependent on the LLM's generation speed, with no mechanism for acceleration.

### Desired Structural State

- **Persistent Continuity**: Session history is durably stored in Redis, accessible via a unique session ID.
- **Intelligent Caching**: Responses to queries are cached, with the cache key derived from the question's content.
- **Centralized Knowledge Store**: Redis acts as a centralized repository for all generated insights, forming a de facto knowledge base.
- **Accelerated Retrieval**: Subsequent identical queries are served directly from the Redis cache, bypassing the LLM entirely and providing near-instantaneous responses.

### Natural Progression Toward Desired State

The structural dynamics of this system create a self-reinforcing loop of knowledge accumulation:

1.  **Initial Query Creates a Knowledge Artifact**: A user asks a question, and the generated response is stored (`tashed`) in Redis, becoming the first knowledge artifact.
2.  **Repetition Enables Acceleration**: A second user asks the same question. The system finds the artifact in the cache (`fetches` it) and delivers it instantly. The structure naturally rewards common inquiries with speed.
3.  **Accumulation Builds a Knowledge Base**: As more unique questions are asked, the Redis store grows, organically building a rich database of the organization's most frequently needed information.
4.  **Analysis Reveals Insights**: By observing cache hit rates and popular keys, administrators can identify the most valuable knowledge and create proactive documentation or training, thus completing the flywheel.

---

## 🏛️ Storage Architecture

### Core Modules

A new, dedicated module, `agentic_flywheel/persistence.py`, will be created to encapsulate all interaction with Redis. This promotes modularity and isolates persistence logic.

### Core Elements

1.  **Response Caching**: After a `flowise_query` successfully returns a response from the LLM, the result is stored in Redis using the `coaia tash` command (or a direct Redis client).
2.  **Cache Retrieval**: Before a `flowise_query` is sent to the LLM, the system first attempts to retrieve a result from the Redis cache using `coaia fetch`.
3.  **Cache Key Generation**: A consistent and deterministic cache key is generated to uniquely identify a question. The proposed algorithm uses the session ID, the flow ID, and a hash of the question text.
4.  **TTL (Time-To-Live) Management**: Cached items are assigned a TTL based on the type of flow that generated them, ensuring knowledge stays relevant.
5.  **Cache Invalidation**: Mechanisms are in place to clear the cache when underlying data or configurations change.

### Integration Points

The integration will occur within `agentic_flywheel/mcp_server.py` inside the `handle_call_tool` function, specifically for the `flowise_query` tool. The logic will wrap the call to `flowise_server._intelligent_query`.

```python
# Conceptual integration in mcp_server.py

from . import persistence

# ... inside handle_call_tool for "flowise_query"

# 1. Check cache before calling the flow
cache_key = persistence.generate_cache_key(...)
cached_response = persistence.check_cache(cache_key)
if cached_response:
    # Add cache_hit metadata and return
    return persistence.format_cached_response(cached_response)

# 2. If not in cache, call original logic
result = await flowise_server._intelligent_query(...)

# 3. Store the result in the cache after the call
ttl = persistence.get_ttl_for_flow(result)
persistence.write_to_cache(cache_key, result, ttl)

# 4. Return the fresh result
return [types.TextContent(text=...)]
```

---

## 🌊 Creative Advancement Scenarios

### Scenario 1: The First Knowledge Artifact is Created

**User Intent:** Create a clear understanding of how to set up a new project.
**Current Structural Reality:** A developer is new to the team and has no prior knowledge. The system's cache is empty for this topic.

**Natural Progression Steps:**
1.  **Query Submission**: The developer asks, "What are the steps to initialize a new project with the company's template?"
2.  **Cache Miss**: The `persistence` module generates a cache key for the question but finds no corresponding entry in Redis.
3.  **Flow Execution**: The query proceeds to `flowise_server._intelligent_query`, which routes it to the "Technical Analysis" flow. The LLM generates a detailed, step-by-step guide.
4.  **Knowledge Artifact Creation**: The successful response, including the generated text and metadata, is passed to the `persistence.write_to_cache` function. It's stored in Redis with a TTL of 7 days.
5.  **Response Delivery**: The developer receives the freshly generated guide.

**Achieved Outcome:**
- ✅ The developer creates a new project successfully.
- ✅ A valuable knowledge artifact (the project setup guide) is created and preserved for future use.

---

### Scenario 2: Collective Knowledge is Instantly Retrieved

**User Intent:** Create a project plan without delay by getting an immediate answer to a common setup question.
**Current Structural Reality:** A week later, a different developer needs to set up a project and asks the exact same question as in Scenario 1.

**Natural Progression Steps:**
1.  **Query Submission**: The new developer asks, "What are the steps to initialize a new project with the company's template?"
2.  **Cache Hit**: The `persistence` module generates the identical cache key. It finds the existing entry in Redis.
3.  **Instantaneous Retrieval**: The cached response object is retrieved from Redis in milliseconds.
4.  **Trace Augmentation**: The response is augmented with `cache_hit: true` metadata before being returned, ensuring observability.
5.  **Immediate Response**: The developer receives the complete, detailed guide instantly, without waiting for an LLM.

**Achieved Outcome:**
- ✅ The developer creates their project plan without breaking their creative flow.
- ✅ The system demonstrates its ability to retain and share collective knowledge efficiently.

---

### Scenario 3: A Conversation is Resumed Across Time

**User Intent:** Create a complex feature by building upon a previous creative exploration.
**Current Structural Reality:** A product manager had a long conversation two days ago exploring ideas for a new feature, resulting in 10 question-response pairs under a single `session_id`. They now want to continue that train of thought.

**Natural Progression Steps:**
1.  **Session Resumption**: The user initiates a query, providing the `session_id` from two days prior.
2.  **Context Retrieval**: Before executing the new query, the system uses the `session_id` to fetch the last 5 related responses from Redis (keyed by `afw:session:{session_id}:...`).
3.  **Contextual Enrichment**: This retrieved history is used to enrich the user's new, short query (e.g., "What about mobile users?") into a fully contextualized prompt for the LLM.
4.  **Flow Execution**: The enriched query is sent to the "Creative Orientation" flow, which now has the full context to provide a relevant continuation.
5.  **Incremental Caching**: The new response is cached, linked to the same `session_id`, further deepening the conversational history.

**Achieved Outcome:**
- ✅ The product manager seamlessly creates the next iteration of their feature idea, building on past work.
- ✅ The system facilitates deep, multi-day creative work by transforming isolated queries into a continuous dialogue.

---

## 🔧 Implementation Guidelines

### Cache Key Strategy

The key must be deterministic and avoid collisions.

```python
# In agentic_flywheel/persistence.py
import hashlib

def generate_cache_key(session_id: str, question: str, flow_id: str) -> str:
    """Generates a consistent cache key for a given query."""
    question_hash = hashlib.md5(question.lower().strip().encode()).hexdigest()
    return f"afw:session:{session_id}:flow:{flow_id}:q_hash:{question_hash}"
```

### TTL Strategy by Flow Type

The TTL will be determined by the `flow_key` found in the response metadata.

- **Technical Flows** (e.g., `technical-analysis`): **7 days** (604,800 seconds). Code and implementation details are relatively stable.
- **Creative/Strategic Flows** (e.g., `creative-orientation`): **30 days** (2,592,000 seconds). High-level ideas and strategies have a longer shelf life.
- **Volatile Flows** (e.g., `document-qa`): **1 day** (86,400 seconds). The underlying knowledge base may be updated frequently.

### Cache Invalidation

- **Automatic**: When a flow's configuration is updated (e.g., via `flowise_add_flow` or a manual YAML change), a function should be triggered to clear all cache entries associated with that `flow_id`.
- **Memory Management**: Redis should be configured with a `maxmemory-policy` of `allkeys-lru` to automatically evict the least recently used keys if it reaches its memory limit.
- **Manual**: An administrative tool (e.g., a new `flowise_clear_cache` MCP tool) should be created to allow manual clearing of caches by `flow_id` or `session_id`.

### Metadata Stored with Response

The value stored in Redis should be a JSON string containing the full, unmodified response from Flowise, which already includes the `_mcp_metadata` block. This ensures all necessary information (including the `trace_id`) is preserved.

```json
{
  "text": "The generated response from the LLM...",
  "answer": "The generated response...",
  "_mcp_metadata": {
    "flow_used": "Technical Analysis",
    "flow_key": "technical-analysis",
    "flow_id": "896f7eed-342e-4596-9429-6fb9b5fbd91b",
    "session_id": "mcp-session-1762589999-abcdef12",
    "intent_detected": "technical-analysis",
    "config_used": { ... }
  },
  "trace_id": "trace-uuid-for-langfuse" // Assuming trace_id is added here
}
```

---

## 🧪 Quality Validation

### Success Metrics

- **Cache Hit Rate**: Achieve a >30% cache hit rate for the top 20% most common queries within 30 days of deployment.
- **Retrieval Time**: Cache retrievals must average < 50ms.
- **Session Continuity**: 100% of queries providing a valid `session_id` successfully retrieve and use context from the last 5 interactions.
- **Data Integrity**: Zero instances of cache corruption, measured by monitoring for deserialization errors.

### Testing Scenarios

- **Cache Write**: Verify that a new Redis key is created with the correct TTL after a `flowise_query` results in a cache miss.
- **Cache Hit**: Verify that a subsequent identical query returns the cached data and does *not* trigger a call to `_intelligent_query`.
- **TTL Expiration**: Verify that a cached key is automatically deleted by Redis after its TTL expires.
- **Session Retrieval**: Verify that providing a `session_id` correctly fetches previous responses to enrich a new query.
- **Invalidation**: Verify that updating a flow's configuration successfully clears all cache entries for that `flow_id`.

---

## 🔗 Integration References

- **coaiapy Tools**: The implementation will use `coaia tash` and `coaia fetch` as described in `__llms/llms-coaiapy-cli-guide.md`.
- **Master Specification**: This component directly supports "Scenario 2: Returning User Continues Previous Conversation" in `rispecs/app.spec.md`.
- **Langfuse Tracing**: The cached metadata must include the `trace_id` from the Langfuse integration (`langfuse_tracing.spec.md`) to link cached responses back to their original observability trace.
