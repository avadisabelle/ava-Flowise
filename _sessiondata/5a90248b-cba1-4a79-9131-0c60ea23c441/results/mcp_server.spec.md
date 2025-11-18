# MCP Server Specification

**Specification Type:** Component Specification
**Document ID:** mcp-server-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** `agentic-flywheel-mcp-app-v1.0`

---

## 🎯 Desired Outcome Definition

### What Users Want to Create

This specification enables users to create a **discoverable and composable AI capabilities ecosystem** through the Model Context Protocol (MCP). By exposing all Agentic Flywheel functionality as standardized MCP tools and resources, users manifest:

1. **Effortless Capability Discovery**: The ability to ask "What can this system do?" and receive an instantly understandable catalog of AI capabilities, without reading documentation or studying code.

2. **Natural Workflow Composition**: Tools that combine fluidly—where the output of one capability becomes the input for another—enabling users to create sophisticated multi-step AI workflows through simple commands.

3. **Living System Visibility**: Real-time insight into system state through resource endpoints, creating transparency that enables informed decisions about flow selection, performance optimization, and usage patterns.

4. **Zero-Friction Integration**: Automatic discovery and connection with Claude and other MCP clients, where capabilities become available immediately upon server startup without manual configuration.

5. **Community-Driven Expansion**: A foundation for ecosystem growth where new tools and resources can be added dynamically, creating a living capability platform that evolves with user needs.

### Success Indicators

Users know they have achieved their desired outcome when:
- ✅ Claude automatically discovers all 13+ Agentic Flywheel tools on connection, without configuration
- ✅ They can compose complex workflows by chaining tools naturally (query → trace view → quality score)
- ✅ System resources provide instant visibility into performance, active sessions, and flow health
- ✅ Error messages include actionable recovery suggestions, not just failure descriptions
- ✅ New capabilities added to the server become discoverable immediately without client restarts
- ✅ Tool definitions are self-documenting—descriptions alone enable correct usage

---

## 🏗️ Structural Tension Analysis

### Current Structural Reality

**What Exists Today:**
- **7 Core MCP Tools**: Flowise operations (query, configure, list_flows, session_info, domain_query, add_flow, browse)
- **3 System Resources**: Flow registry, active sessions, configuration schema
- **Protocol Compliance**: Full MCP standard implementation via `mcp` Python library
- **Intent Classification**: Automatic flow selection based on keyword matching
- **Session Tracking**: Active session registry with metadata
- **Dynamic Flow Registry**: YAML-based flow configuration with runtime loading

**Current Strengths:**
- Tools work independently with clear schemas
- Intent classification reduces routing complexity
- Session continuity through ID tracking
- Domain specialization via context injection
- Dynamic flow addition without server restart

**Current Limitations:**
- No tracing visibility tools (Langfuse observations hidden from users)
- No caching performance tools (Redis metrics invisible)
- No administrative analytics tools (usage patterns not exposed)
- Limited tool composition examples (tools designed independently)
- Basic error handling (minimal recovery guidance)
- Resource catalog incomplete (missing observability endpoints)

### Desired Structural State

**What We're Creating:**
- **13+ Comprehensive Tools**: Flowise (7) + Tracing (3) + Storage (2) + Administration (2) + future expansion
- **6+ Observable Resources**: System state (3) + Observability (3) for complete system transparency
- **Rich Error Context**: Every error includes recovery suggestions, retry strategies, and diagnostic information
- **Tool Composition Patterns**: Documented workflows showing how tools combine to create value
- **Auto-Discovery Protocol**: Resources that describe available capabilities dynamically
- **Performance Observability**: Real-time metrics on cache hit rates, response times, quality scores

### Natural Progression Toward Desired State

The structural dynamics of this system create a self-reinforcing cycle of capability expansion and usage:

1. **Discovery Creates Understanding**: A user connects Claude to the MCP server. Claude calls `list_tools()` and discovers 13 available capabilities organized by category. The user sees: "I can query AI flows, view conversation traces, check cache performance, and analyze usage patterns."

2. **Usage Reveals Composition Opportunities**: The user queries a technical question using `flowise_query`. The response includes metadata showing session_id and trace_id. The user realizes: "I can use that session_id with `flowise_trace_view` to see how the answer was constructed."

3. **Composition Enables Workflows**: The user creates a pattern: Query → Trace → Quality Score. This workflow becomes repeatable. Over time, common patterns emerge: Debug workflow (query + trace + session_history), Performance workflow (cache_stats + flow_health + usage_analytics).

4. **Workflows Drive Tool Addition**: As users create workflows, gaps become visible. "I can see traces, but I can't search them by keyword." This drives creation of `flowise_trace_search` tool. The ecosystem expands organically based on observed needs.

5. **Ecosystem Growth Compounds Value**: More tools → More composition possibilities → More workflow patterns → More community knowledge → Higher value for all users. The MCP server becomes infrastructure that continuously increases in capability.

---

## 🏛️ MCP Server Architecture

### Core Architectural Components

**1. Protocol Layer**
- **MCP Standard Compliance**: Implements `mcp.server.Server` protocol
- **Request Handling**: `@app.call_tool()`, `@app.list_tools()`, `@app.list_resources()`, `@app.read_resource()`
- **Error Marshalling**: Converts internal errors to MCP-compliant error responses
- **Session Management**: stdio transport for Claude desktop integration

**2. Tool Registry**
- **Dynamic Discovery**: Tools registered via decorators, listed through `list_tools()`
- **Schema Validation**: JSON Schema for each tool's input parameters
- **Categorization**: Logical grouping (Flowise Operations, Tracing, Storage, Administration)
- **Versioning Support**: Tool names include semantic meaning for evolution

**3. Resource Registry**
- **URI-Based Access**: Resources addressable via `flowise://` URI scheme
- **Dynamic Content**: Resources return current system state, not cached snapshots
- **MIME Type Support**: JSON resources for programmatic consumption
- **Metadata Richness**: Resources include update timestamps, data freshness indicators

**4. Integration Layer**
- **Flowise Manager**: Wraps `FlowiseManager` for intelligent query routing
- **Langfuse Client**: Integration for trace observation and quality scoring
- **Redis Client**: Connection for cache statistics and session history
- **Flow Registry**: YAML-based configuration loader with cascade support

**5. Error Handling Framework**
- **Structured Errors**: `{error, details, recovery_suggestions, retry_after}` format
- **Context Preservation**: Errors include attempted operation context
- **Recovery Guidance**: Actionable suggestions for resolving failures
- **Graceful Degradation**: Partial results when possible, not total failure

### Tool Categories and Definitions

**Category 1: Flowise Operations (7 tools)**

These tools enable querying, configuring, and managing Flowise chatflows.

1. **`flowise_query`** - Intelligent query with auto-routing
   - Input: `question`, optional `intent`, `session_id`, `flow_override`
   - Output: AI response + metadata (flow_used, session_id, intent_detected, config)
   - Integration: Intent classifier → Flow selection → Flowise API → Response

2. **`flowise_configure`** - Dynamic flow configuration
   - Input: `flow_id`, `config` object, optional `session_id`
   - Output: Configuration confirmation + session details
   - Integration: Merges with default config, validates parameters

3. **`flowise_list_flows`** - Flow discovery
   - Input: None
   - Output: Available flows with descriptions, intent keywords, capabilities
   - Integration: Reads from flow registry (YAML or runtime additions)

4. **`flowise_session_info`** - Session metadata
   - Input: Optional `session_id` (returns all if omitted)
   - Output: Session details (flow used, created_at, metadata)
   - Integration: Queries active session registry

5. **`flowise_domain_query`** - Domain-specialized query
   - Input: `question`, `domain_name`, `domain_description`, `context_type`, optional `stack_info`/`cultural_info`
   - Output: Contextualized AI response with domain enrichment
   - Integration: Context builder → Intent classifier → Flowise query

6. **`flowise_add_flow`** - Runtime flow registration
   - Input: `flow_id`, `flow_name`, `description`, `intent_keywords`, optional `temperature`/`max_tokens`
   - Output: Confirmation of flow addition to registry
   - Integration: Updates in-memory flow registry, persists to YAML

7. **`flowise_browse`** - Web UI access
   - Input: `flow_name`, optional `canvas` boolean
   - Output: Confirmation of browser launch (or failure if headless)
   - Integration: Opens Flowise web interface for visual flow editing

**Category 2: Tracing Operations (3 NEW tools)**

These tools enable visibility into conversation traces captured by Langfuse.

1. **`flowise_trace_view`** - View conversation trace
   - Input: `session_id` or `trace_id`
   - Output: Hierarchical observation tree showing query → intent classification → flow execution → response
   - Integration: Langfuse API query for observations by session/trace ID
   - Purpose: Understand how answers were constructed, what sources were used

2. **`flowise_trace_search`** - Search historical traces
   - Input: `query` (keyword search), optional `date_range`, `flow_filter`, `min_quality_score`
   - Output: List of matching traces with summaries
   - Integration: Langfuse dataset search with filtering
   - Purpose: Find past conversations on specific topics, identify patterns

3. **`flowise_quality_score`** - Evaluate response quality
   - Input: `session_id` or `trace_id`, `score` (1-10), optional `feedback_text`
   - Output: Confirmation of score submission
   - Integration: Creates Langfuse score observation linked to trace
   - Purpose: Provide feedback for learning loop, validate routing accuracy

**Category 3: Storage Operations (2 NEW tools)**

These tools expose Redis cache performance and session continuity.

1. **`flowise_cache_stats`** - Cache performance metrics
   - Input: Optional `flow_filter`, `time_range`
   - Output: Hit rate, miss rate, total queries, average retrieval time, top cached queries
   - Integration: Redis INFO command + key pattern analysis
   - Purpose: Understand cache effectiveness, identify optimization opportunities

2. **`flowise_session_history`** - Retrieve session context
   - Input: `session_id`, optional `limit` (default 5 most recent)
   - Output: Chronological list of queries and responses from session
   - Integration: Redis LIST operations on session:{id}:history keys
   - Purpose: View conversation context, resume interrupted sessions

**Category 4: Administration (2 NEW tools)**

These tools provide system health and usage analytics.

1. **`flowise_flow_health`** - Flow performance dashboard
   - Input: Optional `flow_id` (returns all if omitted)
   - Output: Response time stats (p50, p95, p99), error rate, quality scores, usage count
   - Integration: Langfuse trace aggregation + Flowise database queries
   - Purpose: Identify underperforming flows, validate configuration changes

2. **`flowise_usage_analytics`** - Pattern insights
   - Input: `time_range` (e.g., "7d", "30d"), optional `grouping` (by_flow, by_user, by_intent)
   - Output: Usage distribution, peak times, intent accuracy, common queries
   - Integration: Langfuse dataset analysis + Redis cache patterns
   - Purpose: Data-driven system optimization, capacity planning

### Resource Categories and Definitions

**Category 1: System State (3 resources)**

1. **`flowise://flows`** - Available flow catalog
   - Content: JSON array of flows with id, name, description, intent_keywords, default_config
   - Update frequency: Real-time (includes runtime additions)
   - Purpose: Enable dynamic flow selection, validate flow_id parameters

2. **`flowise://sessions`** - Active session registry
   - Content: JSON object mapping session_id → {flow_key, flow_name, created_at}
   - Update frequency: Real-time
   - Purpose: Session discovery, continuity validation, debugging

3. **`flowise://config-schema`** - Configuration options
   - Content: JSON schema for all configurable parameters (temperature, maxOutputTokens, prompts, etc.)
   - Update frequency: Static (changes with Flowise model updates)
   - Purpose: Validate configuration before applying, discover tuning options

**Category 2: Observability (3 NEW resources)**

1. **`flowise://traces`** - Recent trace summary
   - Content: JSON array of last 20 traces with session_id, flow_used, quality_score, timestamp
   - Update frequency: Real-time
   - Purpose: Quick health check, identify recent activity patterns

2. **`flowise://cache-metrics`** - Cache performance snapshot
   - Content: JSON object with hit_rate, miss_rate, total_keys, memory_usage, eviction_count
   - Update frequency: Real-time (Redis metrics)
   - Purpose: Performance monitoring dashboard, optimization decisions

3. **`flowise://flow-health`** - Health status dashboard
   - Content: JSON object with per-flow metrics (avg_response_time, error_rate, quality_avg, last_24h_count)
   - Update frequency: Real-time (aggregated from traces)
   - Purpose: System health overview, flow comparison, issue detection

### Tool Composition Patterns

**Pattern 1: Debug Workflow**
```
User: "Why did I get this answer?"
→ flowise_query("question") → Get session_id from metadata
→ flowise_trace_view(session_id) → See intent classification, flow selected, sources used
→ flowise_session_history(session_id) → Review conversation context
Result: Complete understanding of answer construction
```

**Pattern 2: Performance Optimization Workflow**
```
User: "Is the system performing well?"
→ Read flowise://flow-health → Identify slow flows
→ flowise_cache_stats() → Check cache effectiveness
→ flowise_usage_analytics("7d") → Understand load patterns
Result: Data-driven optimization targets identified
```

**Pattern 3: Quality Improvement Workflow**
```
User: "How can we improve routing accuracy?"
→ flowise_trace_search(min_quality_score=0, max_quality_score=5) → Find low-scoring responses
→ For each trace: flowise_trace_view(trace_id) → Analyze intent classification
→ Identify misclassification patterns
→ Update flow registry intent_keywords based on patterns
Result: Learning loop completion, improved accuracy
```

**Pattern 4: Session Continuity Workflow**
```
User: "Continue my conversation from yesterday"
→ flowise_session_history(session_id) → Load context
→ flowise_query("follow-up question", session_id=previous) → Maintain context
→ Response automatically enriched with session history
Result: Seamless multi-session conversation
```

---

## 🌊 Creative Advancement Scenarios

### Scenario 1: First-Time User Discovers Capabilities

**User Intent**: Understand what the Agentic Flywheel system can do

**Current Structural Reality**:
- User has connected Claude to the Agentic Flywheel MCP server
- No prior knowledge of available capabilities
- Wants to explore naturally without reading documentation

**Natural Progression Steps**:

1. **Discovery Initiation**
   - User asks Claude: "What can the Agentic Flywheel system do?"
   - Claude calls `list_tools()` to retrieve all available capabilities
   - MCP server returns 13 tools organized by category

2. **Capability Catalog Presented**
   - Claude presents organized list:
     - **Flowise Operations (7)**: Query AI, configure flows, manage sessions, domain-specific queries
     - **Tracing (3)**: View conversation traces, search history, score quality
     - **Storage (2)**: Cache statistics, session history retrieval
     - **Administration (2)**: Flow health monitoring, usage analytics

3. **Natural Exploration Begins**
   - User sees "flowise_query" and asks: "How do I use that?"
   - Claude reads the tool schema showing required `question` parameter and optional `intent`/`session_id`
   - User understands immediately: "I can ask questions and the system auto-routes to the right AI agent"

4. **Resource Discovery**
   - User asks: "What flows are available?"
   - Claude reads `flowise://flows` resource
   - Returns: Creative Orientation, Technical Analysis, Document Q&A with descriptions and capabilities

5. **First Query Execution**
   - User: "Ask a technical question about Python async patterns"
   - Claude calls: `flowise_query(question="How do Python async patterns work for concurrent API calls?")`
   - Response includes metadata showing: flow_used="technical-analysis", confidence=0.89, session_id generated

6. **Composition Discovery**
   - User notices session_id in response, asks: "Can I see how that answer was generated?"
   - Claude calls: `flowise_trace_view(session_id="...")`
   - User sees: Intent classification → Technical Analysis selected → Sources referenced → Response constructed

**Achieved Outcome**:
- ✅ User discovered all capabilities through natural conversation
- ✅ Tool schemas were self-documenting, no external docs needed
- ✅ Composition pattern emerged organically (query → trace view)
- ✅ Resources provided context for informed decisions
- ✅ User excited to explore additional capabilities

---

### Scenario 2: Power User Composes Multi-Step Workflow

**User Intent**: Create a quality assurance workflow for validating AI responses

**Current Structural Reality**:
- User has used basic flowise_query many times
- Noticed occasional incorrect routing or low-quality responses
- Wants to systematically identify and improve quality issues

**Natural Progression Steps**:

1. **Workflow Conception**
   - User: "I want to find all low-quality responses from the past week and understand why they scored poorly"
   - Claude recognizes multi-step workflow requirement

2. **Step 1: Identify Low-Quality Traces**
   - Claude calls: `flowise_usage_analytics(time_range="7d", grouping="by_flow")`
   - Results show: Technical Analysis flow has avg quality 8.2/10, but Creative Orientation has 6.5/10
   - User decides to investigate Creative Orientation

3. **Step 2: Search for Problematic Traces**
   - Claude calls: `flowise_trace_search(query="", flow_filter="creative-orientation", min_quality_score=0, max_quality_score=5, date_range="7d")`
   - Returns: 12 traces with quality scores below 5/10

4. **Step 3: Analyze Each Low-Quality Trace**
   - For each trace, Claude calls: `flowise_trace_view(trace_id="...")`
   - Pattern emerges: 8 of 12 traces contain keywords like "implementation", "code", "technical setup"
   - These queries were routed to Creative Orientation but should have gone to Technical Analysis

5. **Step 4: Pattern Documentation**
   - User observes: "The system is routing technical implementation questions to Creative Orientation because they contain words like 'design' or 'approach'"
   - User identifies missing keywords: Technical Analysis flow needs "implementation", "setup", "build"

6. **Step 5: Registry Update**
   - User: "Add those keywords to the Technical Analysis flow"
   - Claude calls: `flowise_add_flow(flow_id="896f7eed...", intent_keywords=[...existing, "implementation", "setup", "build"])`
   - Flow registry updated immediately

7. **Step 6: Validation**
   - User: "Run a test query: 'How do I implement OAuth2 in React?'"
   - Claude calls: `flowise_query(question="How do I implement OAuth2 in React?")`
   - Response metadata shows: flow_used="technical-analysis", confidence=0.91
   - User: "Perfect! That now routes correctly."

8. **Workflow Automation**
   - User creates documented pattern: "Quality Audit Workflow"
   - Steps: Analytics → Trace Search → Pattern Analysis → Registry Update → Validation
   - Shares with team as repeatable quality improvement process

**Achieved Outcome**:
- ✅ Complex 6-step workflow composed from individual tools
- ✅ Data-driven quality improvement achieved
- ✅ Pattern analysis revealed actionable insights
- ✅ System configuration updated based on evidence
- ✅ Workflow became repeatable organizational knowledge

---

### Scenario 3: Administrator Monitors System Health

**User Intent**: Ensure the Agentic Flywheel system is performing optimally

**Current Structural Reality**:
- System has been running for 3 months
- 500+ queries processed across multiple flows
- Users occasionally report "slow responses"
- Admin wants proactive performance monitoring

**Natural Progression Steps**:

1. **Health Dashboard Creation**
   - Admin: "Show me system performance overview"
   - Claude composes dashboard from resources:
     - Read `flowise://flow-health` → Response time distribution
     - Read `flowise://cache-metrics` → Cache hit rate
     - Read `flowise://sessions` → Active sessions count

2. **Performance Metrics Analysis**
   - Flow health data reveals:
     - Technical Analysis: p95 response time = 3.2s (slow!)
     - Creative Orientation: p95 = 1.8s (good)
     - Document Q&A: p95 = 1.5s (good)
   - Cache metrics show: Hit rate = 28% (low)

3. **Root Cause Investigation**
   - Admin: "Why is Technical Analysis slow?"
   - Claude calls: `flowise_flow_health(flow_id="896f7eed...")`
   - Detailed metrics show:
     - Average tokens: 4800 (high token usage)
     - Source documents: Average 8 per query (retrieval overhead)
     - Config: `returnSourceDocuments=true` causing extra processing

4. **Cache Effectiveness Analysis**
   - Admin: "Why is cache hit rate only 28%?"
   - Claude calls: `flowise_cache_stats(flow_filter="technical-analysis")`
   - Analysis reveals:
     - Technical queries are highly variable (low repetition)
     - TTL = 7 days but tech advice changes frequently
     - Most queries unique, few repeat questions

5. **Optimization Decisions**
   - **Decision 1**: Technical Analysis flow configured with too high maxOutputTokens
   - Admin: "Reduce Technical Analysis maxOutputTokens to 2500"
   - Claude calls: `flowise_configure(flow_id="896f7eed...", config={maxOutputTokens: 2500})`

   - **Decision 2**: Cache TTL too long for technical content
   - Admin notes: "Reduce TTL to 24 hours for technical responses" (implementation task)

6. **Validation After Changes**
   - One week later, admin reviews health again
   - Claude reads `flowise://flow-health`
   - New metrics:
     - Technical Analysis: p95 = 2.1s (34% improvement!)
     - Quality scores unchanged (8.2/10 maintained)
     - Cache hit rate increased to 35% with shorter TTL

7. **Proactive Monitoring Establishment**
   - Admin creates weekly review workflow:
     - Monday morning: Read flow-health resource
     - If any flow p95 > 2.5s: Investigate with flow_health tool
     - Monthly: Run usage_analytics to identify optimization opportunities
   - System performance maintained proactively

**Achieved Outcome**:
- ✅ System health visible through observable resources
- ✅ Performance issues identified through metrics
- ✅ Data-driven optimization decisions made
- ✅ Improvements validated with measurable results
- ✅ Proactive monitoring workflow established

---

### Scenario 4: Error Recovery with Graceful Guidance

**User Intent**: Query the system but Flowise server is temporarily unavailable

**Current Structural Reality**:
- User submits query via `flowise_query`
- Flowise server experiencing network issues (transient failure)
- System must provide helpful error response, not cryptic failure

**Natural Progression Steps**:

1. **Query Initiation**
   - User: "How do I implement rate limiting in Express?"
   - Claude calls: `flowise_query(question="How do I implement rate limiting in Express?")`

2. **Connection Failure Detection**
   - MCP server attempts to connect to Flowise at `https://beagle-emerging-gnu.ngrok-free.app`
   - Connection times out after 30 seconds
   - Exception caught: `httpx.RequestError: Connection timeout`

3. **Rich Error Construction**
   - MCP server constructs structured error:
   ```json
   {
     "error": "Flowise connection failed",
     "error_type": "network_timeout",
     "details": {
       "attempted_url": "https://beagle-emerging-gnu.ngrok-free.app/api/v1/prediction/896f7eed...",
       "flow_attempted": "Technical Analysis",
       "session_id": "mcp-session-1700000000-abc123",
       "timeout_seconds": 30
     },
     "recovery_suggestions": [
       "1. Check if Flowise server is running: Visit https://beagle-emerging-gnu.ngrok-free.app in browser",
       "2. Verify network connectivity to server",
       "3. Check ngrok tunnel status if using ngrok",
       "4. Review MCP server logs for detailed error trace",
       "5. Try again in 30 seconds - this may be a transient issue"
     ],
     "retry_after": 30,
     "support_context": {
       "timestamp": "2025-11-18T12:45:00Z",
       "mcp_server_version": "1.0.0",
       "error_id": "err_abc123"
     }
   }
   ```

4. **User-Friendly Error Presentation**
   - Claude receives error and presents to user:
   - "I encountered an issue connecting to the Flowise server. Here's what happened and how to resolve it:"
   - Lists recovery suggestions in plain English
   - "I'll automatically retry in 30 seconds, or you can check the server status now."

5. **User Takes Action**
   - User opens browser to `https://beagle-emerging-gnu.ngrok-free.app`
   - Sees: "ngrok tunnel expired" message
   - User restarts ngrok tunnel
   - Flowise becomes accessible again

6. **Successful Retry**
   - User: "Try again"
   - Claude calls: `flowise_query(question="How do I implement rate limiting in Express?")`
   - Connection succeeds, response returned
   - User: "Great, it works now!"

7. **Learning from Failure**
   - Error logged to Langfuse with recovery context
   - Admin reviews errors weekly, notices ngrok tunnel failures
   - Admin decision: Switch to persistent domain instead of ngrok
   - Future failures prevented

**Achieved Outcome**:
- ✅ User received actionable error information, not cryptic message
- ✅ Recovery suggestions enabled self-service debugging
- ✅ Error context preserved for administrative review
- ✅ Retry strategy provided (30-second backoff)
- ✅ Failure contributed to system improvement (ngrok → persistent domain)

---

## 🔧 Implementation Guidelines

### Core Module: `agentic_flywheel/mcp_server.py`

**Module Structure:**

```python
#!/usr/bin/env python3
"""
Agentic Flywheel MCP Server
Exposes all capabilities as standardized MCP tools and resources
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from mcp import server, types
import mcp.server.stdio

# Component Imports
from .flowise_manager import FlowiseManager
from .intent_classifier import IntentClassifier
from .persistence import RedisClient  # NEW
from .observability import LangfuseClient  # NEW

logger = logging.getLogger(__name__)

class FlowiseMCPServer:
    """Enhanced MCP Server with full observability"""

    def __init__(self,
                 flowise_base_url: str,
                 flow_registry_path: Optional[str] = None,
                 redis_url: Optional[str] = None,
                 langfuse_config: Optional[Dict] = None):

        # Core integrations
        self.flowise = FlowiseManager(base_url=flowise_base_url, flow_registry_path=flow_registry_path)
        self.classifier = IntentClassifier(flow_registry=self.flowise.flows)
        self.redis = RedisClient(url=redis_url) if redis_url else None
        self.langfuse = LangfuseClient(config=langfuse_config) if langfuse_config else None

        # Session tracking
        self.active_sessions = {}

    # Tool implementations...
```

### Tool Implementation Pattern

**Standard Tool Structure:**

```python
async def _tool_implementation(self, param1: str, param2: Optional[str] = None) -> Dict[str, Any]:
    """
    Tool implementation with error handling

    Args:
        param1: Required parameter description
        param2: Optional parameter description

    Returns:
        Structured response with data and metadata

    Raises:
        Structured error with recovery suggestions
    """
    try:
        # 1. Validate inputs
        if not param1:
            raise ValueError("param1 is required")

        # 2. Log to Langfuse (if available)
        if self.langfuse:
            self.langfuse.observation(
                name="tool_name",
                input={"param1": param1, "param2": param2}
            )

        # 3. Execute core logic
        result = await self._core_operation(param1, param2)

        # 4. Add metadata
        result["_metadata"] = {
            "tool": "tool_name",
            "timestamp": time.time(),
            "parameters_used": {"param1": param1, "param2": param2}
        }

        # 5. Log outcome
        if self.langfuse:
            self.langfuse.observation_update(output=result)

        return result

    except Exception as e:
        # Structured error with recovery guidance
        return self._create_error_response(
            error=str(e),
            error_type=type(e).__name__,
            recovery_suggestions=self._get_recovery_suggestions(e),
            context={"param1": param1, "param2": param2}
        )

def _create_error_response(self, error: str, error_type: str,
                          recovery_suggestions: List[str],
                          context: Dict) -> Dict[str, Any]:
    """Create rich error response"""
    return {
        "error": error,
        "error_type": error_type,
        "details": context,
        "recovery_suggestions": recovery_suggestions,
        "retry_after": self._calculate_retry_delay(error_type),
        "support_context": {
            "timestamp": time.time(),
            "error_id": generate_error_id()
        }
    }
```

### Resource Implementation Pattern

**Dynamic Resource Content:**

```python
@app.read_resource()
async def handle_read_resource(uri: str) -> str:
    """Read MCP resources with real-time data"""

    if uri == "flowise://flow-health":
        # Aggregate data from Langfuse traces
        health_data = {}

        for flow_key, flow_config in flowise_server.flowise.flows.items():
            # Query Langfuse for flow metrics
            traces = await flowise_server.langfuse.get_traces(
                filter={"metadata.flow_id": flow_config['id']},
                limit=100
            )

            # Calculate metrics
            response_times = [t.duration for t in traces if t.duration]
            quality_scores = [t.scores[0].value for t in traces if t.scores]

            health_data[flow_key] = {
                "flow_name": flow_config['name'],
                "response_time_p50": percentile(response_times, 50),
                "response_time_p95": percentile(response_times, 95),
                "avg_quality_score": mean(quality_scores),
                "total_queries_24h": len([t for t in traces if is_within_24h(t.timestamp)]),
                "error_rate": calculate_error_rate(traces),
                "last_updated": time.time()
            }

        return json.dumps(health_data, indent=2)

    elif uri == "flowise://cache-metrics":
        # Query Redis for cache statistics
        if not flowise_server.redis:
            return json.dumps({"error": "Redis not configured"})

        metrics = await flowise_server.redis.get_metrics()
        return json.dumps({
            "hit_rate": metrics['hits'] / (metrics['hits'] + metrics['misses']),
            "miss_rate": metrics['misses'] / (metrics['hits'] + metrics['misses']),
            "total_keys": metrics['total_keys'],
            "memory_usage_mb": metrics['memory_bytes'] / (1024 * 1024),
            "eviction_count": metrics['evictions'],
            "last_updated": time.time()
        }, indent=2)

    # ... other resources
```

### Error Recovery Strategy

**Recovery Suggestion Mapping:**

```python
def _get_recovery_suggestions(self, error: Exception) -> List[str]:
    """Map errors to actionable recovery steps"""

    error_type = type(error).__name__

    suggestions_map = {
        "ConnectionError": [
            "1. Verify Flowise server is running and accessible",
            "2. Check network connectivity between MCP server and Flowise",
            "3. Confirm Flowise base URL is correct in configuration",
            "4. Review firewall rules allowing MCP → Flowise traffic",
            "5. Check Flowise server logs for errors"
        ],
        "TimeoutError": [
            "1. Flowise query may be processing a complex request - wait 30s and retry",
            "2. Check if Flowise server is under heavy load",
            "3. Consider increasing timeout threshold in MCP configuration",
            "4. Review query complexity - simplify if possible"
        ],
        "AuthenticationError": [
            "1. Verify API key or authentication credentials are configured",
            "2. Check if credentials have expired or been revoked",
            "3. Confirm authentication method matches Flowise configuration",
            "4. Review MCP server environment variables"
        ],
        "FlowNotFoundError": [
            "1. Use flowise_list_flows to see available flows",
            "2. Check if flow_id is correct (may have been deleted or renamed)",
            "3. Verify flow is marked as 'active' in flow registry",
            "4. Consider using flow_override parameter with valid flow key"
        ],
        "RedisConnectionError": [
            "1. Check if Redis server is running and accessible",
            "2. Verify Redis URL configuration in MCP server",
            "3. Caching features will be disabled until Redis is available",
            "4. Core query functionality will continue working without cache"
        ]
    }

    return suggestions_map.get(error_type, [
        "1. Review error details for specific failure context",
        "2. Check MCP server logs for additional diagnostic information",
        "3. Retry the operation after ensuring dependencies are healthy",
        "4. Contact support with error_id if issue persists"
    ])

def _calculate_retry_delay(self, error_type: str) -> int:
    """Determine appropriate retry delay in seconds"""

    retry_delays = {
        "ConnectionError": 30,
        "TimeoutError": 30,
        "RateLimitError": 60,
        "ServiceUnavailableError": 120,
        "ValidationError": 0,  # No retry, user must fix input
        "AuthenticationError": 0   # No retry, credentials must be fixed
    }

    return retry_delays.get(error_type, 10)  # Default 10s
```

### Integration with Other Components

**Component Integration Map:**

```python
# 1. Intent Classification Integration
# Used by: flowise_query, flowise_domain_query
from .intent_classifier import IntentClassifier

classification = await self.classifier.classify_with_confidence(
    question=question,
    session_id=session_id
)
flow_key = classification['selected_flow']
confidence = classification['confidence']

# 2. Redis Storage Integration
# Used by: flowise_query (cache check), flowise_cache_stats, flowise_session_history
from .persistence import RedisClient

# Before query
cached = await self.redis.fetch(cache_key)
if cached:
    return cached

# After query
await self.redis.tash(cache_key, result, ttl=ttl)

# 3. Langfuse Tracing Integration
# Used by: All tools (auto-trace), flowise_trace_view, flowise_trace_search, flowise_quality_score
from .observability import LangfuseClient

# Create observation for tool call
self.langfuse.observation(
    name="flowise_query",
    input={"question": question},
    metadata={"flow": flow_key, "confidence": confidence}
)

# Later: update with output
self.langfuse.observation_update(output=result)

# 4. Flowise Manager Integration
# Used by: All flowise_* tools
from .flowise_manager import FlowiseManager

result = await self.flowise.adaptive_query(
    question=question,
    intent=flow_key,
    session_id=session_id
)
```

---

## 🧪 Quality Validation

### Success Metrics

**Protocol Compliance:**
- **Target**: 100% MCP protocol compliance (passes official MCP validator)
- **Measurement**: Run `mcp-validator` against server, all tests pass
- **Baseline**: Current implementation passes all core protocol tests

**Tool Discovery:**
- **Target**: 100% of tools discoverable via `list_tools()`
- **Measurement**: Count tools in `list_tools()` response vs. implemented tools
- **Baseline**: All 7 existing tools discoverable, targeting 13+

**Performance Overhead:**
- **Target**: < 50ms tool dispatch overhead (time from MCP call to internal function)
- **Measurement**: Instrument `@app.call_tool()` decorator with timing
- **Baseline**: Current overhead ~10-20ms, maintain as tools increase

**Error Coverage:**
- **Target**: 90%+ of errors include recovery suggestions
- **Measurement**: Analyze error responses, count with/without suggestions
- **Validation**: All ConnectionError, TimeoutError, ValidationError include suggestions

**Resource Freshness:**
- **Target**: Resources return data < 5 seconds old
- **Measurement**: Compare resource timestamps to current time
- **Validation**: `flowise://flow-health` aggregates from recent traces only

**Composition Viability:**
- **Target**: 80%+ of tools output data usable as input to another tool
- **Measurement**: Map tool outputs → valid inputs for other tools
- **Examples**: `flowise_query` → `session_id` → `flowise_trace_view`, `flowise_trace_search` → `trace_id` → `flowise_quality_score`

### Testing Scenarios

**Test 1: Full Tool Discovery**
```python
# Arrange
mcp_client = connect_to_server()

# Act
tools = await mcp_client.list_tools()

# Assert
assert len(tools) >= 13
assert "flowise_query" in [t.name for t in tools]
assert "flowise_trace_view" in [t.name for t in tools]
assert "flowise_cache_stats" in [t.name for t in tools]
assert all(t.inputSchema is not None for t in tools)
```

**Test 2: Tool Composition (Query → Trace)**
```python
# Arrange
mcp_client = connect_to_server()

# Act - Execute query
query_result = await mcp_client.call_tool(
    name="flowise_query",
    arguments={"question": "What is structural tension?"}
)
session_id = extract_session_id(query_result)

# Act - View trace
trace_result = await mcp_client.call_tool(
    name="flowise_trace_view",
    arguments={"session_id": session_id}
)

# Assert
assert "intent_classification" in trace_result
assert "flow_execution" in trace_result
assert trace_result['session_id'] == session_id
```

**Test 3: Resource Real-Time Updates**
```python
# Arrange
mcp_client = connect_to_server()

# Act - Read resource before query
flows_before = await mcp_client.read_resource("flowise://sessions")
sessions_before = json.loads(flows_before)

# Execute query to create session
await mcp_client.call_tool(
    name="flowise_query",
    arguments={"question": "test"}
)

# Read resource after query
flows_after = await mcp_client.read_resource("flowise://sessions")
sessions_after = json.loads(flows_after)

# Assert - New session visible immediately
assert len(sessions_after) == len(sessions_before) + 1
```

**Test 4: Error Recovery Guidance**
```python
# Arrange
mcp_client = connect_to_server()
stop_flowise_server()  # Simulate failure

# Act
result = await mcp_client.call_tool(
    name="flowise_query",
    arguments={"question": "test"}
)

# Assert
assert "error" in result
assert "recovery_suggestions" in result
assert len(result['recovery_suggestions']) >= 3
assert "retry_after" in result
assert result['retry_after'] > 0
```

**Test 5: Tool Schema Validation**
```python
# Arrange
mcp_client = connect_to_server()
tools = await mcp_client.list_tools()

# Act & Assert - Each tool has valid schema
for tool in tools:
    schema = tool.inputSchema

    assert schema['type'] == 'object'
    assert 'properties' in schema

    # Required fields must exist in properties
    if 'required' in schema:
        for req_field in schema['required']:
            assert req_field in schema['properties']

    # Each property has type and description
    for prop_name, prop_schema in schema['properties'].items():
        assert 'type' in prop_schema
        assert 'description' in prop_schema
```

---

## 🔗 Integration References

### Component Dependencies

**Flowise Integration Component**: All `flowise_*` tools wrap FlowiseManager methods for intelligent query routing, flow management, and session tracking

**Intent Classification Component**: Used by `flowise_query` and `flowise_domain_query` to automatically select optimal flow based on question content and context

**Langfuse Tracing Component**: Powers `flowise_trace_view`, `flowise_trace_search`, `flowise_quality_score` tools and auto-traces all MCP tool calls

**Redis Storage Component**: Enables `flowise_cache_stats` and `flowise_session_history` tools, used by query tools for cache-before-call pattern

**Domain Specialization Component**: Integrated via `flowise_domain_query` for context-aware responses with stack/cultural enrichment

**Flow Registry**: Central configuration source for `flowise://flows` resource and all flow-related operations

### MCP Protocol References

**Tool Definition Standard**: Tools defined using `mcp.types.Tool` with JSON Schema input validation
**Resource URI Scheme**: Resources use `flowise://` URI scheme for namespacing
**Error Format**: Errors returned as `types.TextContent` with structured JSON for parsing
**Transport**: stdio transport for Claude desktop integration

### External System Integration

**Flowise API**: HTTP/REST calls to `/api/v1/prediction/{flow_id}` endpoint
**Langfuse API**: SDK calls for trace retrieval, observation creation, quality scoring
**Redis**: Direct client connection for cache operations and metrics queries
**YAML Registry**: File-based configuration loaded on startup and updated dynamically

---

## 🎯 Implementation Roadmap

### Phase 1: Enhanced Tool Registry (Week 1)

**Deliverables:**
1. Add `flowise_trace_view` tool with Langfuse integration
2. Add `flowise_cache_stats` tool with Redis metrics
3. Add `flowise_flow_health` tool with trace aggregation
4. Update `list_tools()` to return 10+ tools

**Validation:**
- All new tools discoverable via MCP
- Tool schemas validated
- Integration tests pass

### Phase 2: Enhanced Resource Registry (Week 1)

**Deliverables:**
1. Add `flowise://traces` resource
2. Add `flowise://cache-metrics` resource
3. Add `flowise://flow-health` resource
4. Implement real-time data refresh

**Validation:**
- Resources return current data (< 5s old)
- JSON format valid
- Resource reads don't block tool calls

### Phase 3: Error Handling Enhancement (Week 2)

**Deliverables:**
1. Implement `_create_error_response()` helper
2. Map all error types to recovery suggestions
3. Add retry delay calculation
4. Test all failure modes

**Validation:**
- 90%+ errors include recovery suggestions
- Error format consistent across all tools
- Users can self-service common failures

### Phase 4: Remaining Tools (Week 2)

**Deliverables:**
1. Add `flowise_trace_search` with keyword/filter support
2. Add `flowise_quality_score` for user feedback
3. Add `flowise_session_history` for context retrieval
4. Add `flowise_usage_analytics` for pattern insights

**Validation:**
- All 13+ tools implemented
- Tool composition patterns work
- Documentation updated

### Phase 5: Optimization & Polish (Week 3)

**Deliverables:**
1. Performance profiling, ensure < 50ms overhead
2. Comprehensive error scenario testing
3. Tool composition example documentation
4. Integration test suite expansion

**Validation:**
- Performance targets met
- 100% MCP protocol compliance
- Production-ready quality

---

## 📊 Success Narrative

### How Users Experience This Specification

**Day 1**: A developer connects Claude to the enhanced MCP server. Immediately sees 13 tools organized by category. Thinks: "This is a complete system, not just a query interface."

**Week 1**: The developer creates their first workflow: Query → Trace View → Quality Score. Shares the pattern with team. Three colleagues adopt the same workflow for debugging.

**Week 2**: Administrator uses `flowise://flow-health` resource to create monitoring dashboard. Discovers Technical Analysis flow is slow. Uses `flowise_flow_health` tool to diagnose high token usage. Optimizes configuration, performance improves 34%.

**Month 1**: Team has documented 5 standard workflows (Debug, Performance Audit, Quality Review, Session Recovery, Pattern Analysis). New team members learn these patterns, not individual tools. Expertise compounds.

**Month 3**: Usage analytics show 1,200+ queries processed, 89% cache hit rate on common questions, 96% routing accuracy (up from 80% initial). System has become invisible infrastructure—users think in terms of outcomes, not tools.

**Month 6**: Community contributor proposes new tool: `flowise_semantic_search` for finding similar past queries. Uses existing pattern: Integrates with Langfuse, follows error handling standards, composes with existing tools. Tool added in 3 days, discoverable immediately.

---

**Specification Status:** Draft → Ready for Implementation
**Confidence Level:** High (95%)
**Autonomous Implementation:** ✅ Yes - Comprehensive implementation guidance provided
**RISE Compliance:** ✅ Creative orientation throughout, ecosystem collaboration emphasized
**Composition Patterns:** ✅ Four detailed workflows demonstrating tool synergy
