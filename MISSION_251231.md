# 🌟 Agentic Flywheel: Narrative Intelligence Integration (2025-12-31)

**Reference**: See main unified mission at `/workspace/langgraph/MISSION_251231.md`

## Your Role in the Stack

The Agentic Flywheel is the **Flowise-specific agent coordination layer**. While ava-langflow handles universal routing across multiple backends, you specialize in:
- Flowise flow management and execution
- Domain-specific flow registry
- Flowise-native intent classification
- Flow parameter optimization

**Relationship to ava-langflow**: ava-langflow routes to you when Flowise is the best backend for a query.

## The Three Universes Context

Every query can be processed through three lenses:
- **Engineer World (Mia)**: Technical precision, API schemas, build status
- **Ceremony World (Ava8)**: Relational accountability, sacred pause, K'é mapping
- **Story Engine World (Miette)**: Narrative function, act position, character arc

When ava-langflow routes a query to Flowise, you receive the universe analysis and should select flows that serve the lead universe.

## Current Status

✅ **Strengths**:
- Flowise flow management complete
- MCP server architecture solid
- Configuration system (flow-registry.yaml) flexible
- Intent classification framework exists

❌ **Gaps**:
- No narrative context understanding
- Flow selection too simplistic
- Session state doesn't track narrative position
- Not integrated with NCP protocol

## Integration Tasks for This Codebase

### **Phase 2: Intelligence Layer** (Your Primary Responsibility)

#### Task 1: Narrative Intent Classifier
**File**: `agentic_flywheel/narrative_intent_classifier.py` (NEW)

```python
"""
Extend intent classification to understand narrative position, not just keywords.

Examples:
- Query: "The character faces an impossible choice"
  NCP Analysis: Crisis moment, antagonistic force active
  Intent: narrative_crisis_moment
  Routes to: conflict_deepener, dialogue_enhancer flows

- Query: "After the revelation, the character must decide"
  NCP Analysis: Turning point, resolution phase starting
  Intent: narrative_turning_point
  Routes to: decision_maker, commitment_flow flows
"""

class NarrativeIntentClassifier:
    def classify(self, text: str, narrative_context: NCPState) -> NarrativeIntent:
        # 1. Analyze narrative state (character position, theme status, emotional arc)
        # 2. Detect what type of narrative moment this is
        # 3. Return: intent category + suggested flows + context parameters
        pass
```

**Success**: Flows selected based on narrative coherence, not just keyword matching

#### Task 2: NCP Context Injector
**File**: `agentic_flywheel/ncp_context_injector.py` (NEW)

```python
"""
Inject narrative state into Flowise queries so flows understand context.

Example context injection:
  User prompt: "What does the character say?"
  
  Injected context:
  - Character arc: "Has grown from doubt to conviction through 3 scenes"
  - Emotional beat: "Building tension, moving toward crisis"
  - Theme focus: "Exploring the tension between duty and desire"
  - Perspective: "First-person internal monologue"
  
  Combined query to Flowise:
  "Generate dialogue for [CHARACTER] who has [ARC]. The emotional moment is
   [BEAT]. The thematic focus is [THEME]. Use [PERSPECTIVE]. The dialogue
   should: [goals from NCP state]"
"""

class NCPContextInjector:
    def inject(self, query: str, narrative_state: NCPState) -> EnrichedQuery:
        # 1. Extract relevant NCP information (character, theme, beat)
        # 2. Format as narrative context
        # 3. Prepend to query while preserving user intent
        # 4. Return enriched query + metadata for response processing
        pass
```

**Success**: Flowise responses respect narrative structure and character arcs

#### Task 3: Narrative Flow Router
**File**: `agentic_flywheel/narrative_flow_router.py` (NEW)

```python
"""
Route to different Flowise flows based on narrative needs, not just intent keywords.

Dynamic flow activation examples:
- If character_arc_strength < threshold: route to "character_deepener" flow
- If emotional_beat_quality < threshold: route to "sentiment_enhancer" flow  
- If theme_clarity < threshold: route to "thematic_resonance" flow
- If dialogue_consistency_check fails: route to "dialogue_coherence_checker" flow
"""

class NarrativeFlowRouter:
    def select_flows(self, narrative_state: NCPState, gap_analysis: dict) -> List[FlowRoute]:
        # 1. Analyze narrative quality (received from analyzer)
        # 2. Identify gaps (weak character, weak emotion, theme not clear)
        # 3. Select and sequence flows to address gaps
        # 4. Return ordered list of flows with parameters
        pass
    
    def should_route_to_enrichment(self, beat: StoryBeat, analysis: AnalysisResult) -> bool:
        # Determine if this beat needs enrichment
        pass
```

**Success**: Stories improved through targeted agent interventions

### **Phase 3: Session State Enhancement**

#### Task 4: Narrative Session Manager
**File**: `agentic_flywheel/narrative_session_manager.py` (ENHANCE)

Current: Session IDs for conversation continuity
Needed: Narrative state continuity

```python
class NarrativeSessionManager:
    def create_narrative_session(self, story_id: str) -> NarrativeSession:
        """
        Track narrative state across conversations:
        - Which character perspective is active?
        - What is the current emotional beat?
        - What narrative phase (setup, crisis, resolution)?
        - What themes are active?
        - What has been analyzed vs not yet analyzed?
        """
        pass
    
    def get_narrative_context(self, session_id: str) -> NCPState:
        """Retrieve full narrative state for flow context injection"""
        pass
    
    def update_with_flow_result(self, session_id: str, flow_result: FlowResult) -> None:
        """Update narrative session state after Flowise flow execution"""
        pass
```

### **Phase 4: Flow Registry Enhancement**

Update `flow-registry.yaml` structure:

```yaml
metadata:
  version: "2.0"
  narrative_aware: true

operational_flows:
  character_deepener:
    flow_id: "abc123"
    description: "Deepen character motivations and backstory"
    narrative_triggers:
      - character_arc_strength < 0.6
      - needs: "character_background"
    context_requirements:
      - current_character_state
      - emotional_beat_type
      - character_arc_so_far
    response_processing:
      - extract_character_insights: true
      - update_ncp_state: true
  
  sentiment_enhancer:
    flow_id: "def456"
    description: "Strengthen emotional resonance of scenes"
    narrative_triggers:
      - emotional_beat_quality < 0.5
      - needs: "emotional_deepening"
    context_requirements:
      - current_emotion
      - desired_emotion
      - character_perspective
    response_processing:
      - validate_emotion_continuity: true
      - update_beat_quality: true

routing_flows:
  # Routes based on narrative analysis, not just keywords
  narrative_analyzer:
    flow_id: "ghi789"
    purpose: "Analyze narrative gaps and suggest flows"
    inputs:
      - current_story_beats
      - character_states
      - theme_threads
    outputs:
      - gap_analysis
      - suggested_flows
      - priority_order
```

## What Success Looks Like

```
┌─────────────────────────────────────────────────────────┐
│ Story Beat Generated                                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Narrative Intent Classifier                             │
│ - Analyzes narrative position                          │
│ - Detects type of moment (crisis, turning point, etc)  │
│ - Routes to appropriate flow                           │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ NCP Context Injector                                    │
│ - Extracts narrative state                             │
│ - Formats as context for Flowise                       │
│ - Enriches user query with story awareness             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Narrative Flow Router                                   │
│ - Selects best flow(s) for this moment                │
│ - Sequences flows if multiple needed                   │
│ - Passes context through flow-registry                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Flowise Execution                                       │
│ - Flow receives enriched context                       │
│ - Generates narrative-aware response                   │
│ - Returns with metadata (confidence, emotion, etc)     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ Narrative Session Manager                              │
│ - Updates narrative state with flow result             │
│ - Records which flows were used and why                │
│ - Tracks narrative enrichment history                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
        ✨ Enriched Story Returned
```

## Integration Points

1. **From LangGraph**:
   - Receive `NCPState` objects
   - Receive `StoryBeat` sequences
   - Receive analysis gaps from Narrative Intelligence Toolkit

2. **To LangGraph**:
   - Send enriched beats
   - Send flow execution metadata
   - Send routing decisions for trace logging

3. **To LangChain/Langfuse**:
   - Each flow execution creates a trace span
   - Intent classification results logged
   - Context injection and response processing tracked

## Development Checklist

- [ ] Implement `narrative_intent_classifier.py`
  - [ ] Narrative moment detection logic
  - [ ] Flow suggestion algorithm
  - [ ] Intent category system

- [ ] Implement `ncp_context_injector.py`
  - [ ] NCP state extraction
  - [ ] Context formatting
  - [ ] Query enrichment logic

- [ ] Implement `narrative_flow_router.py`
  - [ ] Gap analysis evaluation
  - [ ] Multi-flow sequencing
  - [ ] Flow parameter injection

- [ ] Enhance `narrative_session_manager.py`
  - [ ] NCP state tracking
  - [ ] Session-based narrative context
  - [ ] Result integration

- [ ] Update `flow-registry.yaml`
  - [ ] Narrative trigger definitions
  - [ ] Context requirements
  - [ ] Response processing rules

- [ ] Testing
  - [ ] Unit tests for each component
  - [ ] Integration tests with story generation
  - [ ] End-to-end narrative enrichment flow

## Dependencies to Import

From `/workspace/langgraph/libs/narrative-intelligence/`:
```python
from narrative_intelligence import (
    NCPState, StoryBeat, CharacterArcState,
    NarrativeTraversalNode, EmotionalBeatClassifierNode
)
```

From `/src/storytelling/`:
```python
from storytelling import StoryGenerationState
```

From LangFuse (via LangChain):
```python
from langfuse import Langfuse
```

## Remember

> The Agentic Flywheel's job is not just to execute flows—it's to execute the *right* flow at the *right* narrative moment based on *deep understanding* of the story being told.

This is what separates narrative-intelligent agents from generic AI automation.

---

**Last Updated**: 2025-12-31
**Your Focus**: Making agents narrative-aware
**Success Metric**: Generated stories improved in coherence and emotional resonance after agent enrichment
