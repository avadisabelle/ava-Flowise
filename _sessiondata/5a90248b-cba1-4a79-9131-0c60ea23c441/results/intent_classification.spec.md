# Intent Classification Specification

**Specification Type:** Component Specification
**Document ID:** intent-classification-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** `agentic-flywheel-mcp-app-v1.0`

---

## 🎯 Desired Outcome Definition

### What Users Want to Create

This specification enables users to create a **natural expertise-finding system** that connects their questions to the most capable AI agent without requiring technical knowledge of the system's architecture. Through intelligent intent classification, users manifest:

1. **Effortless Expertise Discovery**: The ability to ask questions in natural language and automatically reach the AI agent with the most relevant capabilities, as if an expert colleague instantly directed them to the right specialist.

2. **Confident Routing Transparency**: Clear visibility into why a particular AI agent was selected, creating trust in the system's intelligence and enabling users to learn the system's capabilities organically.

3. **Continuous Conversation Coherence**: Automatic detection when follow-up questions relate to previous context, ensuring users experience natural conversation continuity rather than fragmented interactions.

4. **Self-Improving Intelligence**: A classification system that learns from routing outcomes through observation, becoming more accurate and valuable with every interaction without requiring manual retraining.

### Success Indicators

Users know they have achieved their desired outcome when:
- ✅ 95%+ of their questions route to the most appropriate AI agent on the first attempt, validated by quality scores
- ✅ They can ask follow-up questions without re-explaining context, experiencing natural conversation flow
- ✅ The system confidently handles ambiguous queries by explaining its reasoning or requesting clarification
- ✅ New users discover specialized AI capabilities through natural exploration, not documentation reading
- ✅ Routing accuracy improves month-over-month through observed usage patterns

---

## 🏗️ Structural Tension Analysis

### Current Structural Reality

**What Exists Today:**
- **Keyword Matching Foundation**: The `classify_intent()` method scores flows based on keyword overlap with predefined intent keywords in the flow registry
- **Simple Scoring Algorithm**: Counts keyword matches and selects the flow with the highest score, defaulting to "creative-orientation" if no matches
- **Context-Aware Extension**: The `classify_intent_with_context()` method in DomainSpecificFlowiseManager adds domain-specific keyword enhancement
- **Binary Routing Decision**: Classification produces a single flow selection without confidence scoring or alternative suggestions

**Current Limitations:**
- No confidence scores to indicate classification certainty
- No learning mechanism to improve from routing outcomes
- Limited context utilization beyond session continuity
- Ambiguous queries lack graceful handling or explanation
- No visibility into classification reasoning for users
- Pattern recognition limited to static keyword lists

### Desired Structural State

**What We're Creating:**
- **Multi-Signal Classification**: Intent detection considers keyword matches, session context, domain specialization, and historical routing patterns
- **Confidence-Scored Decisions**: Every routing decision includes confidence scores showing certainty and alternative flow probabilities
- **Learning Feedback Loop**: Langfuse observations link routing decisions to quality scores, enabling pattern discovery and classification refinement
- **Transparent Reasoning**: Users see why a particular flow was selected, creating trust and system understanding
- **Graceful Ambiguity Resolution**: Low-confidence classifications trigger clarification requests or provide routing explanations
- **Adaptive Pattern Recognition**: Monthly trace analysis identifies misclassification patterns, leading to intent keyword updates

### Natural Progression Toward Desired State

The structural dynamics of this system create a self-reinforcing cycle of routing intelligence:

1. **Initial Classification Creates Baseline**: A user asks a question, intent classification evaluates all flows, generates confidence scores, and selects the highest-confidence match. This routing decision is captured in Langfuse with full metadata.

2. **Observation Captures Outcomes**: The selected flow processes the query, and the response quality is scored in Langfuse. High scores validate the routing decision; low scores signal potential misclassification.

3. **Pattern Analysis Reveals Insights**: Monthly aggregation of Langfuse traces groups queries by detected intent and actual flow used. Misclassifications where low scores correlate with specific keyword patterns become visible.

4. **Classification Refinement Advances Accuracy**: Identified patterns inform intent keyword updates in the flow registry. For example, "user management" questions that were routed to Creative Orientation but scored low when re-routed to Technical Analysis lead to adding "management" keywords to the technical flow.

5. **Improved Routing Compounds Value**: More accurate intent classification reduces misrouting, increases user satisfaction, and generates higher-quality traces for future learning—a compounding flywheel of intelligence.

---

## 🧠 Classification Architecture

### Core Modules

A new module, `agentic_flywheel/intent_classifier.py`, will be created to encapsulate intelligent intent classification logic. This promotes modularity and enables independent testing and enhancement.

### Core Elements

1. **Keyword Extraction Engine**: Analyzes incoming questions to extract semantically meaningful keywords, removing stop words and identifying technical terms, domain concepts, and action verbs.

2. **Multi-Flow Scoring System**: Evaluates each available flow against the extracted keywords, session context, and domain specialization, producing a confidence score for each flow.

3. **Confidence Calibration**: Normalizes scores into probabilities and applies confidence thresholds to determine routing strategy (auto-route, explain-and-route, or request-clarification).

4. **Context Enrichment Layer**: Incorporates session history from Redis storage to boost scores for flows used in recent queries, creating conversation continuity.

5. **Learning Integration**: Logs every classification decision to Langfuse with full metadata (all scores, selected flow, confidence level, reasoning), enabling downstream pattern analysis.

6. **Ambiguity Handler**: Detects low-confidence or tied-score situations and generates user-friendly explanations or clarification requests.

### Integration Points

The classification system integrates with several Agentic Flywheel components:

- **Receives Input**: Questions arrive via the `flowise_query` MCP tool in `mcp_server.py`
- **References Flow Registry**: Reads intent keywords from `flow-registry.yaml` to understand available flows and their specializations
- **Enriches with Context**: Retrieves recent session history from Redis Storage component to detect conversation continuity patterns
- **Routes to Execution**: Passes the selected flow ID and classification metadata to the Flowise Integration component
- **Observes Outcomes**: Creates Langfuse observations via the Tracing component, linking classification decisions to response quality scores

### Classification Algorithm

**Conceptual Implementation:**

```python
# Conceptual structure for intent_classifier.py

from typing import Dict, List, Optional, Tuple
import hashlib

class IntentClassifier:
    """Intelligent intent classification with confidence scoring"""

    def __init__(self, flow_registry: Dict, redis_client=None, langfuse_client=None):
        self.flow_registry = flow_registry
        self.redis = redis_client
        self.langfuse = langfuse_client
        self.stop_words = {"the", "a", "an", "how", "what", "when", "where", "is", "are", "do", "does"}

    def extract_keywords(self, question: str) -> List[str]:
        """Extract meaningful keywords from question"""
        words = question.lower().split()
        keywords = [w for w in words if w not in self.stop_words and len(w) > 2]
        return keywords

    def calculate_keyword_score(self, keywords: List[str], flow_keywords: List[str]) -> float:
        """Score keyword overlap between question and flow"""
        matches = sum(1 for kw in keywords if any(fk in kw or kw in fk for fk in flow_keywords))
        max_possible = max(len(keywords), len(flow_keywords))
        return matches / max_possible if max_possible > 0 else 0.0

    def get_session_context(self, session_id: Optional[str]) -> Dict:
        """Retrieve recent session history from Redis"""
        if not session_id or not self.redis:
            return {}

        # Fetch last 3 interactions from session
        cache_key = f"session:{session_id}:history"
        history = self.redis.lrange(cache_key, -3, -1)

        return {
            "last_flow": history[-1].get("flow_id") if history else None,
            "recent_keywords": self._extract_session_keywords(history)
        }

    def calculate_context_boost(self, flow_id: str, session_context: Dict) -> float:
        """Boost score if flow aligns with session continuity"""
        boost = 0.0

        # Strong boost for same flow as last query (conversation continuity)
        if session_context.get("last_flow") == flow_id:
            boost += 0.25

        # Moderate boost for keyword overlap with recent context
        recent_keywords = session_context.get("recent_keywords", [])
        if recent_keywords:
            boost += 0.10

        return boost

    def classify_with_confidence(self,
                                 question: str,
                                 session_id: Optional[str] = None,
                                 domain_context: Optional[Dict] = None) -> Dict:
        """
        Classify intent with confidence scoring

        Returns:
            {
                'selected_flow': str,
                'confidence': float,
                'all_scores': Dict[str, float],
                'reasoning': str,
                'threshold_met': str  # 'high', 'medium', 'low'
            }
        """
        # Extract keywords from question
        keywords = self.extract_keywords(question)

        # Get session context if available
        session_context = self.get_session_context(session_id) if session_id else {}

        # Score each flow
        raw_scores = {}
        for flow_key, flow_config in self.flow_registry.items():
            # Base score from keyword matching
            base_score = self.calculate_keyword_score(keywords, flow_config['intent_keywords'])

            # Context boost for conversation continuity
            context_boost = self.calculate_context_boost(flow_config['id'], session_context)

            # Domain boost if domain context provided
            domain_boost = 0.0
            if domain_context and domain_context.get('specialized_keywords'):
                domain_overlap = len(set(keywords) & set(domain_context['specialized_keywords']))
                domain_boost = domain_overlap * 0.05

            # Combined score
            raw_scores[flow_key] = min(base_score + context_boost + domain_boost, 1.0)

        # Normalize to probabilities
        total_score = sum(raw_scores.values())
        if total_score > 0:
            confidences = {k: v/total_score for k, v in raw_scores.items()}
        else:
            # Uniform distribution if no matches
            confidences = {k: 1.0/len(raw_scores) for k in raw_scores.keys()}

        # Select best flow
        best_flow, best_confidence = max(confidences.items(), key=lambda x: x[1])

        # Determine confidence threshold
        if best_confidence >= 0.70:
            threshold = 'high'
            reasoning = f"Strong keyword match ({len([k for k in keywords if any(fk in k for fk in self.flow_registry[best_flow]['intent_keywords'])])} keywords)"
        elif best_confidence >= 0.40:
            threshold = 'medium'
            reasoning = f"Moderate confidence based on {len(keywords)} keywords and context"
        else:
            threshold = 'low'
            reasoning = "Low confidence - consider clarification or use default flow"

        # Add session continuity to reasoning if applicable
        if session_context.get('last_flow') == self.flow_registry[best_flow]['id']:
            reasoning += " + conversation continuity"

        result = {
            'selected_flow': best_flow,
            'confidence': best_confidence,
            'all_scores': confidences,
            'reasoning': reasoning,
            'threshold_met': threshold,
            'keywords_extracted': keywords
        }

        # Log to Langfuse if available
        if self.langfuse:
            self._log_classification(question, result, session_id)

        return result

    def _log_classification(self, question: str, classification: Dict, session_id: Optional[str]):
        """Log classification decision to Langfuse for learning"""
        self.langfuse.observation(
            name="intent_classification",
            input=question,
            output=classification['selected_flow'],
            metadata={
                "confidence": classification['confidence'],
                "all_scores": classification['all_scores'],
                "threshold": classification['threshold_met'],
                "reasoning": classification['reasoning'],
                "session_id": session_id
            }
        )
```

---

## 🌊 Creative Advancement Scenarios

### Scenario 1: Clear Technical Intent — High-Confidence Routing

**User Intent**: Implement OAuth2 authentication in React application

**Current Structural Reality**:
- User asks: "How do I implement OAuth2 authentication in my React app?"
- No previous session history exists
- Multiple flows available: creative-orientation, technical-analysis, document-qa

**Natural Progression Steps**:

1. **Keyword Extraction**
   - System identifies: `["implement", "oauth2", "authentication", "react", "app"]`
   - Technical action verb "implement" detected
   - Specific technologies "OAuth2" and "React" present

2. **Multi-Flow Scoring**
   - **Technical Analysis**: Base score 0.80 (strong keyword match: "implement", "OAuth2", "authentication")
   - **Creative Orientation**: Base score 0.15 (weak match on "implement")
   - **Document Q&A**: Base score 0.05 (minimal match)
   - No session context available (new conversation)

3. **Confidence Calculation**
   - Normalized confidences: Technical Analysis (0.85), Creative (0.11), Document (0.04)
   - Best flow: "technical-analysis"
   - Confidence: **0.85 (HIGH)**
   - Threshold: HIGH (auto-route without explanation)

4. **Routing Execution**
   - System routes to Technical Analysis flow automatically
   - Metadata added: `{intent_detected: "technical-analysis", confidence: 0.85, reasoning: "Strong keyword match (4 keywords) + technical implementation pattern"}`

5. **Langfuse Observation**
   - Classification decision logged with full confidence scores
   - Linked to subsequent flow execution observation
   - Quality score will later validate routing accuracy

**Achieved Outcome**:
- ✅ User receives accurate technical implementation guidance
- ✅ Routing decision made with high confidence, no user intervention needed
- ✅ Classification reasoning captured for future analysis
- ✅ Foundation established for learning from outcome quality

---

### Scenario 2: Ambiguous Query — Medium-Confidence with Explanation

**User Intent**: Unclear whether user wants strategic guidance or technical implementation

**Current Structural Reality**:
- User asks: "What's the best approach for user management?"
- "user management" could mean strategic user experience design OR technical user authentication system
- No session history to provide context

**Natural Progression Steps**:

1. **Keyword Extraction**
   - System identifies: `["best", "approach", "user", "management"]`
   - Ambiguous terms: "approach" (could be strategic or technical), "management" (broad concept)

2. **Multi-Flow Scoring**
   - **Creative Orientation**: Base score 0.45 ("approach" keyword, strategic framing)
   - **Technical Analysis**: Base score 0.40 ("user management" has technical connotations)
   - **Document Q&A**: Base score 0.15 (weak match)

3. **Confidence Calculation**
   - Normalized confidences: Creative (0.50), Technical (0.42), Document (0.08)
   - Best flow: "creative-orientation"
   - Confidence: **0.50 (MEDIUM)**
   - Threshold: MEDIUM (route with explanation)

4. **Transparent Routing Response**
   - System routes to Creative Orientation flow
   - Response includes explanation: *"I'm routing this to Creative Orientation based on 'best approach' phrasing (confidence: 50%). If you're looking for technical implementation details instead, please let me know."*

5. **User Feedback Opportunity**
   - User can accept the routing OR provide clarification: "Actually, I meant technical implementation"
   - If user clarifies, system re-routes and **logs the correction** to Langfuse as a learning signal

6. **Learning Capture**
   - If user accepts Creative flow and quality score is high → Validates classification
   - If user overrides to Technical flow → Creates "misclassification" event in Langfuse
   - Pattern: "user management" + "approach" + override to Technical → Suggests adding "management" to technical keywords

**Achieved Outcome**:
- ✅ System handles ambiguity gracefully with transparent reasoning
- ✅ User maintains control and can redirect if needed
- ✅ Misclassification captured as learning signal
- ✅ Future queries with "user management" will route more accurately

---

### Scenario 3: Context-Enhanced Continuity — Session-Aware Routing

**User Intent**: Follow-up question building on previous technical discussion

**Current Structural Reality**:
- Previous query: "How do I implement OAuth2 authentication in my React app?" → Routed to Technical Analysis
- Redis cache contains session history: `{last_flow: "technical-analysis", recent_keywords: ["oauth2", "react", "authentication"]}`
- User now asks: "How do I handle token refresh?"

**Natural Progression Steps**:

1. **Session Context Retrieval**
   - System fetches session history from Redis
   - Detects: Last flow was "technical-analysis", context includes OAuth2 authentication
   - Current query: "How do I handle token refresh?"

2. **Context-Enhanced Keyword Extraction**
   - Direct keywords: `["handle", "token", "refresh"]`
   - Enriched with session context: `["handle", "token", "refresh", "oauth2", "react"]` (from recent history)

3. **Continuity-Boosted Scoring**
   - **Technical Analysis**: Base score 0.60 + **Context boost 0.25** (same flow as last query) = **0.85**
   - **Creative Orientation**: Base score 0.20 (no continuity boost) = 0.20
   - **Document Q&A**: Base score 0.10 = 0.10

4. **High-Confidence Continuation**
   - Normalized confidence: Technical Analysis (0.87)
   - Confidence: **0.87 (HIGH)**
   - Reasoning: "Strong keyword match (3 keywords) + **conversation continuity**"

5. **Coherent Response**
   - System routes to Technical Analysis flow with enriched context
   - Flow receives: "How do I handle token refresh [Context: Previously discussed OAuth2 implementation in React]"
   - User experiences seamless conversation continuation

6. **Langfuse Hierarchical Trace**
   - New classification observation linked to previous OAuth2 observation
   - Session thread shows progression: OAuth2 setup → Token refresh → (future: error handling)
   - Pattern emerges: OAuth2 conversations follow predictable paths

**Achieved Outcome**:
- ✅ User experiences natural conversation flow without re-explaining context
- ✅ Session continuity creates coherent multi-turn interactions
- ✅ Classification accuracy improved by context awareness
- ✅ Conversation patterns visible in Langfuse for system optimization

---

### Scenario 4: Learning from Feedback — Misclassification Correction

**User Intent**: System learns from routing mistakes through observation

**Current Structural Reality**:
- Over 90 days, 500+ conversations traced in Langfuse
- Pattern detected: Questions containing "design patterns" routed to Creative Orientation (40 instances)
- Quality scores for these routings: Average 4.5/10 (LOW)
- Manual overrides: 25 instances where users explicitly selected Technical Analysis instead
- Quality scores after override: Average 8.9/10 (HIGH)

**Natural Progression Steps**:

1. **Monthly Pattern Analysis**
   - Data scientist runs Langfuse trace analysis
   - Groups observations by: `intent_detected`, `flow_used`, `quality_score`
   - Identifies low-scoring patterns

2. **Misclassification Pattern Discovery**
   - Query pattern: Questions with "design patterns" keyword
   - Current classification: Routes to "creative-orientation" (50% confidence)
   - Observed outcome: Low quality scores (4.5/10 avg) + frequent user overrides to "technical-analysis"
   - Validation: When routed to Technical Analysis, quality scores high (8.9/10)

3. **Root Cause Analysis**
   - "design patterns" interpreted as creative/strategic design
   - Actual user intent: Software design patterns (Gang of Four, MVC, etc.)
   - Intent keywords missing: Technical Analysis flow lacks "design" and "patterns" keywords

4. **Classification Refinement**
   - Update `flow-registry.yaml`: Add `["design patterns", "architecture patterns", "mvc", "singleton"]` to Technical Analysis `intent_keywords`
   - Commit change with message: "Add design pattern keywords to Technical Analysis based on 90-day trace analysis showing 40 misclassifications"

5. **Improved Routing**
   - Next user asks: "What are common design patterns for React apps?"
   - System now matches: `["design", "patterns", "react"]` → Technical Analysis
   - Confidence: **0.82 (HIGH)** (previously 0.50 Creative)
   - Correct routing on first attempt

6. **Validation and Feedback Loop**
   - Quality scores for "design patterns" queries improve to 8.5/10 average
   - Langfuse comments document: "Routing accuracy improved after keyword update based on observed pattern"
   - System continues learning from new interactions

**Achieved Outcome**:
- ✅ System learns from real usage patterns, not assumptions
- ✅ Misclassifications identified through data, corrected systematically
- ✅ Routing accuracy improves month-over-month
- ✅ Value compounds as classification becomes more intelligent

---

## 🔧 Implementation Guidelines

### Core Module: `agentic_flywheel/intent_classifier.py`

**Module Responsibilities:**
1. Extract meaningful keywords from natural language questions
2. Score all available flows against keywords and context
3. Calculate confidence levels and determine routing strategy
4. Integrate with Redis for session context retrieval
5. Log all classification decisions to Langfuse for learning
6. Handle ambiguous queries with graceful explanations

**Key Functions:**

```python
def classify_with_confidence(question: str, session_id: Optional[str] = None) -> Dict
    """
    Primary classification function

    Returns: {
        'selected_flow': flow_key,
        'confidence': 0.0-1.0,
        'all_scores': {flow: score},
        'reasoning': explanation_string,
        'threshold_met': 'high'|'medium'|'low'
    }
    """

def extract_keywords(question: str) -> List[str]
    """Remove stop words, extract meaningful terms"""

def calculate_keyword_score(keywords: List[str], flow_keywords: List[str]) -> float
    """Score keyword overlap with fuzzy matching"""

def get_session_context(session_id: str) -> Dict
    """Retrieve recent session history from Redis"""

def calculate_context_boost(flow_id: str, session_context: Dict) -> float
    """Boost score for conversation continuity"""
```

### Integration with MCP Server

**Modification Point**: `agentic_flywheel/mcp_server.py` in `handle_call_tool()` for `flowise_query`

```python
# Conceptual integration

from .intent_classifier import IntentClassifier

classifier = IntentClassifier(
    flow_registry=flow_registry,
    redis_client=redis_client,
    langfuse_client=langfuse
)

# Inside handle_call_tool for "flowise_query"
question = arguments.get("question")
session_id = arguments.get("session_id")
flow_override = arguments.get("flow_override")

# Classify intent unless flow explicitly overridden
if not flow_override:
    classification = classifier.classify_with_confidence(question, session_id)

    # Handle based on confidence threshold
    if classification['threshold_met'] == 'high':
        # Auto-route with high confidence
        selected_flow = classification['selected_flow']

    elif classification['threshold_met'] == 'medium':
        # Route but add explanation to response metadata
        selected_flow = classification['selected_flow']
        explanation = f"Routing to {selected_flow} (confidence: {classification['confidence']:.0%}). {classification['reasoning']}"

    else:  # low confidence
        # Consider asking for clarification OR use default
        selected_flow = 'creative-orientation'  # default
        explanation = f"Low confidence ({classification['confidence']:.0%}). Using default flow. Consider clarifying your question."
else:
    selected_flow = flow_override
    classification = None  # User explicitly chose flow

# Continue with flow execution...
result = await flowise_server._intelligent_query(
    question=question,
    flow_key=selected_flow,
    session_id=session_id
)

# Add classification metadata to response
if classification:
    result['_metadata']['intent_classification'] = classification
```

### Confidence Thresholds

**High Confidence (≥ 0.70)**: Auto-route without explanation
- User experiences seamless, instant routing
- High trust in classification accuracy
- No additional cognitive load

**Medium Confidence (0.40-0.69)**: Route with explanation
- System explains its reasoning transparently
- User maintains awareness of routing decision
- Opportunity to override if incorrect
- Builds user trust through transparency

**Low Confidence (< 0.40)**: Request clarification OR default flow
- System acknowledges uncertainty
- May ask: "Are you looking for technical implementation or strategic guidance?"
- Falls back to default flow (creative-orientation) with explanation
- Prevents poor routing experience

### Learning Integration with Langfuse

**Observation Structure:**

```python
langfuse.observation(
    name="intent_classification",
    trace_id=session_trace_id,
    input={
        "question": question,
        "session_id": session_id,
        "session_context": session_context
    },
    output={
        "selected_flow": selected_flow,
        "confidence": confidence_score
    },
    metadata={
        "all_scores": {flow: score for all flows},
        "threshold_met": "high|medium|low",
        "reasoning": explanation_string,
        "keywords_extracted": keywords,
        "context_boost_applied": True/False
    }
)
```

**Learning Workflow:**

1. **Monthly Trace Aggregation**: Query Langfuse for all `intent_classification` observations from past 90 days

2. **Pattern Analysis**: Group by `selected_flow` and correlate with downstream quality scores
   - Identify low-scoring classification patterns
   - Detect frequent user overrides (manual flow selection after auto-routing)
   - Find ambiguous query patterns (medium/low confidence clusters)

3. **Intent Keyword Refinement**: Update `flow-registry.yaml` based on insights
   - Add missing keywords to flows that were manually overridden
   - Remove misleading keywords that caused misclassifications
   - Document changes in commit messages with data justification

4. **Validation**: Monitor classification confidence and quality scores after updates to confirm improvements

---

## 🧪 Quality Validation

### Success Metrics

**Classification Accuracy:**
- **Target**: 95%+ routing accuracy validated by quality scores ≥ 7/10
- **Measurement**: Langfuse trace analysis correlating `intent_detected` with `quality_score`
- **Baseline**: Current keyword-only matching (estimate: 75-80% accuracy)

**Response Time:**
- **Target**: < 100ms classification time (negligible overhead)
- **Measurement**: Time between `flowise_query` invocation and classification result
- **Baseline**: Current classify_intent() is effectively instant

**Ambiguity Handling:**
- **Target**: < 10% of queries fall into low-confidence threshold
- **Measurement**: Percentage of classifications with confidence < 0.40
- **Success**: Users report graceful handling of unclear questions

**Learning Effectiveness:**
- **Target**: 80%+ of identified misclassifications corrected within 30 days
- **Measurement**: Track misclassification patterns pre/post keyword updates
- **Validation**: Quality score improvement for previously problematic query types

**User Override Rate:**
- **Target**: < 5% of queries result in manual flow override
- **Measurement**: Track when users explicitly select different flow after auto-routing
- **Interpretation**: Low override rate = high routing trust

### Testing Scenarios

**Test 1: High-Confidence Technical Query**
- Input: "How do I connect to PostgreSQL from Python?"
- Expected: Technical Analysis flow, confidence ≥ 0.70
- Validation: Keywords ["connect", "postgresql", "python"] strongly match technical flow

**Test 2: High-Confidence Creative Query**
- Input: "What's a strategic vision for improving team collaboration?"
- Expected: Creative Orientation flow, confidence ≥ 0.70
- Validation: Keywords ["strategic", "vision", "improving"] strongly match creative flow

**Test 3: Ambiguous Query (Medium Confidence)**
- Input: "How should I approach data modeling?"
- Expected: Medium confidence (0.40-0.69), explanation provided
- Validation: "data modeling" could be strategic (entity relationships) or technical (database schemas)

**Test 4: Context Continuity**
- Setup: Previous query routed to Technical Analysis
- Input: "And how do I optimize performance?"
- Expected: Technical Analysis with context boost, confidence ≥ 0.70
- Validation: Context boost from session continuity correctly applied

**Test 5: Learning from Misclassification**
- Setup: "design patterns" currently routes to Creative (incorrect)
- Input: "What design patterns should I use for this API?"
- Action: User overrides to Technical Analysis, quality score 9/10
- Expected: System logs override as learning signal
- Validation: After keyword update, same query routes to Technical automatically

---

## 🔗 Integration References

### Component Dependencies

**Flowise Integration Component**: Receives the selected flow ID and executes the query against the appropriate Flowise chatflow

**Redis Storage Component**: Provides session history for context-aware classification, enabling conversation continuity detection

**Langfuse Tracing Component**: Captures all classification decisions as observations, creating the foundation for learning and improvement

**Flow Registry (`flow-registry.yaml`)**: Defines available flows and their intent keywords, serving as the knowledge base for classification

**Domain Specialization Component**: Provides domain-specific keywords that enhance classification accuracy for specialized contexts

### MCP Tools Integration

**Primary Integration Point**: `flowise_query` tool in `mcp_server.py`
- Classification occurs before flow execution
- Results inform flow selection and metadata

**Secondary Integration**: `flowise_configure` and `flowise_add_flow` tools
- New flows automatically available for classification
- Intent keywords from new flows integrated into scoring

---

## 🎯 Agent Delegation Opportunities

### Implementation Phase Delegation

When transitioning from this specification to implementation, leverage the Mia Agent ecosystem:

**Phase 1: Core Classifier Module**
- **Agent**: `python-pro`
- **Task**: Create `agentic_flywheel/intent_classifier.py` module
- **Deliverables**: `IntentClassifier` class with all core functions (keyword extraction, scoring, confidence calculation)
- **Validation**: Unit tests for classification algorithm accuracy

**Phase 2: MCP Server Integration**
- **Agent**: `backend-architect`
- **Task**: Integrate `intent_classifier.py` into `mcp_server.py`
- **Deliverables**: Modified `handle_call_tool()` with classification wrapper, confidence-based routing logic
- **Validation**: Integration tests showing classification → routing flow

**Phase 3: Langfuse Learning Integration**
- **Agent**: `python-pro` or `ml-engineer`
- **Task**: Implement observation logging and pattern analysis scripts
- **Deliverables**: Classification observation logging, monthly analysis script for misclassification detection
- **Validation**: Sample trace analysis showing pattern discovery

**Phase 4: Architectural Review**
- **Agent**: `architect-review`
- **Task**: Validate structural soundness of classification system
- **Focus**: Ensure advancing patterns (learning loop), not oscillating patterns (static rules)
- **Deliverables**: Review report confirming RISE compliance and structural integrity

---

## 📊 Success Narrative

### How Users Experience This Specification

**Week 1**: A team deploys the Intent Classification system. Initial routing accuracy is 85%, with confident routing for clear technical and creative queries. Ambiguous queries receive explanations, building user trust.

**Week 4**: Session context integration creates natural conversation flow. Users notice the system "remembers" their previous question topics and maintains context across multi-turn conversations.

**Month 3**: The first learning cycle completes. Langfuse trace analysis identifies 5 misclassification patterns. Intent keywords are updated based on observed data. Routing accuracy improves to 91%.

**Month 6**: Users report rarely needing to override flow selection. The system confidently handles 95% of queries on first attempt. New team members discover specialized flows through natural exploration rather than documentation.

**Month 12**: Intent classification has become invisible infrastructure. Users think in terms of "asking the AI" rather than "selecting flows." The learning flywheel continues compounding intelligence month-over-month.

---

**Specification Status:** Draft → Ready for Implementation
**Confidence Level:** High (95%)
**Autonomous Implementation:** ✅ Yes - Detailed enough for independent implementation
**RISE Compliance:** ✅ Creative orientation throughout, structural tension clear, natural progression defined
