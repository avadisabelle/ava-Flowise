# DELEGATION TASK 03: Redis Storage Specification

**Task ID:** task-03-redis-storage
**Parent Session:** 5a90248b-cba1-4a79-9131-0c60ea23c441
**Trace Session:** a50f3fc2-eb8c-434d-a37e-ef9615d9c07d
**Priority:** MEDIUM (enhances performance)
**Estimated Effort:** 45-60 minutes

---

## 🎯 Your Mission

Create a comprehensive RISE specification for **Redis Storage Integration** that enables persistent conversation memory and intelligent response caching for the Agentic Flywheel MCP.

**Output File:** `redis_storage.spec.md`
**Destination:** Save to `../_sessiondata/5a90248b-cba1-4a79-9131-0c60ea23c441/results/`

---

## 📋 Context You Need

### Master Specification
- **File:** `../../rispecs/app.spec.md`
- **Focus on:** Scenario 2 (session continuity), caching strategy

### Redis Tools Available
Study coaiapy Redis integration:
- **Guide:** `__llms/llms-coaiapy-cli-guide.md`
- **Commands:** `coaia tash` (store), `coaia fetch` (retrieve)

### RISE Framework
- **File:** `__llms/llms-rise-framework.txt`
- **Key Principle:** Caching enables continuity, not just speed

---

## 📐 Specification Requirements

### 1. Desired Outcome Definition
**What users want to create through persistent storage:**
- Continuous conversations across sessions (no memory loss)
- Instant retrieval of previously generated insights
- Knowledge accumulation over time
- Searchable conversation history

**Success indicators:**
- Users resume conversations seamlessly days later
- Frequently asked questions answered instantly (cache hits)
- Team members find relevant past conversations
- Conversation threads show learning progression

### 2. Structural Tension Analysis
**Current Reality:**
- Each session starts from scratch
- Previously generated insights lost
- Same questions re-queried (wasted compute)
- No cross-session learning

**Desired Structural State:**
- Session continuity maintained automatically
- Response cache accelerates common queries
- Conversation history searchable
- Knowledge compounds over time

**Natural Progression:**
- First query → Cached response
- Second query → Retrieved instantly
- Pattern: Popular questions emerge in cache metrics
- Outcome: FAQ automatically identified

### 3. Storage Architecture
**Core Elements:**
- Response Caching (`coaia tash`)
- Session Retrieval (`coaia fetch`)
- Cache Key Generation (session + question hash)
- TTL Management (per flow type)
- Cache Invalidation Strategy

**Integration Points:**
- Caches every `flowise_query` response
- Links to Langfuse traces (trace_id in metadata)
- Keyed by session_id for continuity
- Invalidates on flow configuration changes

### 4. Creative Advancement Scenarios
**Required: At least 3 scenarios**

**Scenario A: First Cache Write**
- User asks technical question
- Flow generates detailed response
- `coaia tash` stores: {session_id}:{question_hash} → {response, metadata, trace_id}
- TTL: 7 days for technical content

**Scenario B: Cache Hit Acceleration**
- Different user asks identical technical question
- Cache key matches previous query
- Response retrieved in <50ms (vs. 2-5s flow query)
- Trace metadata shows "cache_hit: true"

**Scenario C: Session Continuity**
- User returns after 2 days
- Provides session_id from previous conversation
- `coaia fetch` retrieves last 5 responses
- Context automatically enriches new query

### 5. Implementation Guidelines
**Cache Key Strategy:**
```python
# Conceptual structure
import hashlib

def generate_cache_key(session_id, question, flow_id):
    question_hash = hashlib.md5(question.lower().strip().encode()).hexdigest()[:8]
    return f"afw:session:{session_id}:flow:{flow_id}:q:{question_hash}"
```

**TTL Strategy by Flow Type:**
- Technical queries: 7 days (code/implementation details change slowly)
- Creative orientation: 30 days (strategic insights remain relevant)
- Document Q&A: 3 days (knowledge base may update)

**Cache Invalidation:**
- Flow configuration changes → Clear all caches for that flow_id
- Redis max memory → LRU eviction (least recently used)
- Manual: Admin tool to clear specific session or flow caches

**Metadata Stored with Response:**
```json
{
  "response": "...",
  "flow_id": "...",
  "flow_name": "...",
  "timestamp": "...",
  "trace_id": "...",
  "session_id": "...",
  "configuration_used": {...}
}
```

### 6. Quality Validation
**Success Metrics:**
- 30%+ cache hit rate for common technical questions
- < 50ms cache retrieval time
- Zero cache corruption incidents
- 100% session continuity success rate

**Testing Scenarios:**
- Verify cache write after flowise_query
- Confirm cache hit on identical question
- Validate TTL expiration behavior
- Test session history retrieval

---

## 🎨 RISE Framework Compliance

### Creative Orientation ✅
- [ ] Frames caching as "knowledge accumulation" not just performance
- [ ] Emphasizes continuity and learning, not speed alone
- [ ] Describes searchable history as institutional memory
- [ ] Focus on what users CREATE with persistent storage

### Structural Tension ✅
- [ ] Current ephemeral vs. desired persistent state
- [ ] Natural progression: Cache → Retrieve → Accumulate → Search
- [ ] Structural force: More usage = Better cache coverage
- [ ] Inevitable outcome: Frequently needed knowledge always available

### Autonomous Implementation ✅
- [ ] Clear cache key generation algorithm
- [ ] Explicit TTL strategy per flow type
- [ ] Complete invalidation rules
- [ ] Testing scenarios well-defined

---

## 🔍 Key Questions to Answer

1. **Cache Granularity:** Cache per exact question, or semantic similarity?

2. **Session Scope:** How many past responses to retrieve for context?

3. **TTL Tuning:** How do admins adjust TTL per flow type?

4. **Cache Warming:** Should popular queries be pre-cached?

5. **Privacy:** How do users control caching of sensitive queries?

6. **Conflict Resolution:** What if cached response conflicts with updated flow?

---

## 📊 Deliverable Format

```markdown
# Redis Storage Specification

**Specification Type:** Component Specification
**Document ID:** redis-storage-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** app.spec.md

## Desired Outcome Definition
## Structural Tension Analysis
## Storage Architecture
## Creative Advancement Scenarios
## Implementation Guidelines
## Quality Validation
## Integration References
```

---

## ✅ Completion Checklist

- [ ] Knowledge accumulation framing (not just speed)
- [ ] Cache key generation algorithm defined
- [ ] TTL strategy per flow type documented
- [ ] Invalidation rules clear
- [ ] At least 3 advancement scenarios
- [ ] Session continuity mechanism explained
- [ ] Privacy considerations addressed
- [ ] File saved to: `../results/redis_storage.spec.md`

---

## 🚀 Getting Started

1. Read `__llms/llms-coaiapy-cli-guide.md` for `tash`/`fetch` commands
2. Study master spec's session continuity scenario
3. Review RISE framework's structural dynamics
4. Draft specification with knowledge accumulation focus
5. Validate RISE compliance
6. Save to results folder

**Remember:** You're enabling users to CREATE institutional knowledge, not just cache responses!
