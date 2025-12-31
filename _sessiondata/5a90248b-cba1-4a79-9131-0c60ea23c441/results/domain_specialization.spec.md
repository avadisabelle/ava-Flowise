# Domain Specialization Specification

**Specification Type:** Component Specification
**Document ID:** domain-specialization-v1.0
**Created:** 2025-11-18
**Status:** Draft
**Framework:** RISE
**Parent Spec:** `agentic-flywheel-mcp-app-v1.0`

---

## 🎯 Desired Outcome Definition

### What Users Want to Create

This specification enables users to create **deeply relevant, precision-tailored AI interactions** that understand their specific domain context without requiring constant re-explanation. Through domain specialization, users manifest:

1. **Effortless Contextual Understanding**: The ability to ask domain-specific questions and receive responses that automatically reflect their technical stack, cultural context, and business constraints—as if consulting an expert colleague who intimately knows their environment.

2. **Actionable, Stack-Specific Guidance**: Technical recommendations that reference their actual frameworks, languages, and infrastructure, eliminating the need to mentally translate generic advice into their specific context.

3. **Culturally Intelligent Content**: Responses that respect domain-specific cultural nuances, values, and sensitivities, creating content that resonates authentically with their audience without explicit reminders.

4. **Strategic Insights Within Constraints**: Business and product guidance that accounts for their actual team size, budget, stage, and priorities—moving beyond theoretical best practices to pragmatic, executable strategies.

5. **Compounding Domain Knowledge**: An AI that "learns" their domain through the profile, getting more valuable with every interaction as it consistently applies accumulated context.

### Success Indicators

Users know they have achieved their desired outcome when:
- ✅ AI responses reference their actual technologies (e.g., "Next.js API routes" not "generic backend")
- ✅ They rarely need to re-state technical stack, constraints, or cultural context
- ✅ Advice is immediately actionable within their specific constraints (budget, team, timeline)
- ✅ Cultural content demonstrates authentic domain understanding, not surface-level awareness
- ✅ New team members onboard faster by inheriting the domain context automatically
- ✅ Response relevance increases to 90%+ (vs 60% for generic responses)

---

## 🏗️ Structural Tension Analysis

### Current Structural Reality

**What Exists Today:**
- **Domain Context Dataclass**: Structure for capturing domain information (name, description, stack_info, cultural_info, technical_constraints, specialized_keywords)
- **Context Builder**: Three static methods for building technical, cultural, and strategic context strings
- **Domain-Specific FlowiseManager**: Extended manager that accepts DomainContext and enriches queries
- **Keyword Enhancement**: Specialized keywords auto-distributed to flows based on semantic relevance
- **Contextualized Query Method**: `contextualized_query()` method that prepends context to questions

**Current Strengths:**
- Context injection via query prepending works immediately
- Specialized keywords improve intent classification accuracy
- Three context types (technical, cultural, strategic) cover major use cases
- Domain profile structure is extensible via dataclass

**Current Limitations:**
- **Manual Profile Creation**: No guided workflow for creating domain profiles
- **Static Context**: Profiles don't evolve based on usage patterns or new information
- **Single Domain Assumption**: System assumes one domain per manager instance, no multi-domain switching
- **Context Injection Strategies**: Only prepend strategy implemented, no system prompt or metadata alternatives
- **No Profile Persistence**: Domain profiles must be recreated each session, not stored long-term
- **Limited Conflict Resolution**: No guidance when domain-specific advice conflicts with general best practices

### Desired Structural State

**What We're Creating:**
- **Domain Profile Management**: YAML-based profiles stored persistently, easily created and updated
- **Dynamic Context Enrichment**: Profiles that auto-update based on detected technologies, usage patterns, and explicit feedback
- **Multi-Domain Support**: Users can maintain multiple domain profiles and switch contexts mid-session
- **Flexible Injection Strategies**: Choose between prepend, system prompt injection, or metadata passing based on flow capabilities
- **Conflict Resolution Framework**: Clear guidance when domain constraints conflict with general best practices
- **Privacy Controls**: Sensitive domain information (competitors, financials) handled with appropriate restrictions
- **Profile Templates**: Pre-built templates for common domains (e-commerce, SaaS, education, etc.)

### Natural Progression Toward Desired State

The structural dynamics of this system create a self-reinforcing cycle of increasing relevance and personalization:

1. **Profile Creation Enables Automatic Context**: A user creates a domain profile for their "Language Learning SaaS" with Next.js stack, education focus, and seed-stage constraints. This single setup eliminates the need to repeat context in every query.

2. **First Specialized Query Demonstrates Value**: User asks: "How should I implement spaced repetition?" Without domain specialization, they'd get generic algorithms. With it, they get: Next.js-specific implementation, PostgreSQL schema for their database, AWS Lambda caching strategy. The value is immediately visible.

3. **Reduced Context Repetition Compounds Efficiency**: Over time, users stop prefacing questions with "In Next.js..." or "For my education platform...". The AI automatically knows. This efficiency compounds—100 queries saved from re-explanation = hours of saved cognitive load.

4. **Domain Understanding Deepens Through Usage**: As users interact, the system observes: "They frequently ask about gamification, engagement metrics, and content localization." These patterns can enrich the domain profile automatically, making responses even more targeted.

5. **Profile Becomes Organizational Knowledge**: New team members inherit the domain profile. They immediately benefit from specialized responses without needing to establish context themselves. Domain knowledge becomes transferable infrastructure.

6. **Multi-Domain Users Create Ecosystem**: Power users manage profiles for "Production App" + "Internal Tools" + "Marketing Site". They switch contexts seamlessly. Domain specialization scales from individual to organizational intelligence.

---

## 🏛️ Domain Specialization Architecture

### Core Architectural Components

**1. Domain Profile Structure**

Domain profiles are YAML documents that capture all relevant context for a specific domain. They follow this schema:

```yaml
domain_profile:
  # Identity
  id: "lang-learn-prod-2025"
  name: "Language Learning Platform (Production)"
  description: "Digital platform for French language learning targeting English speakers"
  version: "1.2"
  created_at: "2025-01-15"
  updated_at: "2025-11-18"

  # Technical Context
  technical_context:
    stack:
      frontend:
        - "Next.js 14"
        - "React 18"
        - "TailwindCSS"
        - "Framer Motion"
      backend:
        - "Node.js 20"
        - "Express"
        - "tRPC"
      database:
        - "PostgreSQL 15 (primary)"
        - "Redis 7 (cache + sessions)"
      hosting:
        - "Vercel (frontend)"
        - "AWS Lambda (API)"
        - "AWS RDS (database)"

    architecture_patterns:
      - "Server-side rendering (SSR) for SEO"
      - "Edge functions for personalization"
      - "Event-driven background jobs"

    constraints:
      - "Mobile-first design required"
      - "Offline capability for lessons"
      - "< 2s page load time target"
      - "Budget-conscious infrastructure ($500/mo limit)"

    integrations:
      - "Stripe for payments"
      - "Langfuse for tracing"
      - "Sentry for monitoring"

  # Cultural Context
  cultural_context:
    domain_type: "Education Technology"
    target_audience:
      primary: "English-speaking adults learning French"
      age_range: "18-45"
      proficiency_levels: ["Beginner", "Intermediate"]

    cultural_sensitivity:
      - "Respect for French cultural nuances and idioms"
      - "Age-appropriate content (family-friendly)"
      - "Inclusive language (gender-neutral examples)"

    content_standards:
      - "CEFR-aligned (Common European Framework)"
      - "Native speaker reviewed"
      - "Authentic cultural context for each lesson"

  # Strategic Context
  strategic_context:
    business_stage: "Seed-stage SaaS startup"
    team_composition:
      engineering: 3
      content: 1
      total: 4

    current_priorities:
      - "User engagement and retention (top)"
      - "Content quality and authenticity"
      - "Gamification features"
      - "Mobile app parity"

    business_constraints:
      - "Runway: 18 months"
      - "Must reach 1000 MAU in 6 months"
      - "Limited marketing budget"

    competitive_position:
      - "Differentiation: Cultural immersion focus"
      - "Competitors: Duolingo, Babbel (different approach)"

  # Intent Classification Enhancement
  specialized_keywords:
    - "spaced-repetition"
    - "language-learning"
    - "pronunciation"
    - "conjugation"
    - "gamification"
    - "engagement-metrics"
    - "content-localization"
    - "CEFR"
    - "immersion"

  # Metadata
  privacy_level: "internal"  # public, internal, confidential
  owners: ["tech-lead@company.com"]
  tags: ["saas", "education", "b2c", "international"]
```

**2. Context Builder Module**

Enhanced context builders that create rich, formatted context strings for query enrichment:

```python
# agentic_flywheel/context_builder.py

from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class DomainProfile:
    """Complete domain profile with all context types"""
    id: str
    name: str
    description: str
    technical_context: Optional[Dict[str, Any]] = None
    cultural_context: Optional[Dict[str, Any]] = None
    strategic_context: Optional[Dict[str, Any]] = None
    specialized_keywords: Optional[List[str]] = None
    privacy_level: str = "internal"

class ContextBuilder:
    """Build rich, formatted context for domain-specific queries"""

    @staticmethod
    def build_technical_context(profile: DomainProfile, question: str) -> str:
        """Create technical context with stack and constraints"""

        if not profile.technical_context:
            return question

        context_parts = [
            "## Technical Implementation Context",
            f"**Project:** {profile.name}",
            "",
            "### Current Stack:"
        ]

        # Format stack information
        stack = profile.technical_context.get('stack', {})
        for category, technologies in stack.items():
            tech_list = ", ".join(technologies) if isinstance(technologies, list) else technologies
            context_parts.append(f"- **{category.title()}:** {tech_list}")

        # Add architecture patterns if present
        if 'architecture_patterns' in profile.technical_context:
            context_parts.append("\n### Architecture Patterns:")
            for pattern in profile.technical_context['architecture_patterns']:
                context_parts.append(f"- {pattern}")

        # Add constraints
        if 'constraints' in profile.technical_context:
            context_parts.append("\n### Constraints:")
            for constraint in profile.technical_context['constraints']:
                context_parts.append(f"- {constraint}")

        # Add the actual question
        context_parts.extend([
            "",
            "### Implementation Question:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_cultural_context(profile: DomainProfile, question: str) -> str:
        """Create cultural context with audience and sensitivities"""

        if not profile.cultural_context:
            return question

        context_parts = [
            "## Cultural Content Context",
            f"**Domain:** {profile.name}",
            f"**Type:** {profile.cultural_context.get('domain_type', 'General')}",
            ""
        ]

        # Target audience
        if 'target_audience' in profile.cultural_context:
            audience = profile.cultural_context['target_audience']
            context_parts.append("### Target Audience:")
            if isinstance(audience, dict):
                for key, value in audience.items():
                    context_parts.append(f"- **{key.title()}:** {value}")
            else:
                context_parts.append(f"- {audience}")

        # Cultural sensitivity requirements
        if 'cultural_sensitivity' in profile.cultural_context:
            context_parts.append("\n### Cultural Sensitivity Requirements:")
            for requirement in profile.cultural_context['cultural_sensitivity']:
                context_parts.append(f"- {requirement}")

        # Content standards
        if 'content_standards' in profile.cultural_context:
            context_parts.append("\n### Content Standards:")
            for standard in profile.cultural_context['content_standards']:
                context_parts.append(f"- {standard}")

        # Add question
        context_parts.extend([
            "",
            "### Content Request:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_strategic_context(profile: DomainProfile, question: str) -> str:
        """Create strategic context with business stage and constraints"""

        if not profile.strategic_context:
            return question

        context_parts = [
            "## Strategic Planning Context",
            f"**Business:** {profile.name}",
            f"**Stage:** {profile.strategic_context.get('business_stage', 'Unknown')}",
            ""
        ]

        # Team composition
        if 'team_composition' in profile.strategic_context:
            team = profile.strategic_context['team_composition']
            context_parts.append("### Team:")
            for role, count in team.items():
                context_parts.append(f"- {role.title()}: {count}")

        # Current priorities
        if 'current_priorities' in profile.strategic_context:
            context_parts.append("\n### Current Priorities (ordered):")
            for i, priority in enumerate(profile.strategic_context['current_priorities'], 1):
                context_parts.append(f"{i}. {priority}")

        # Business constraints
        if 'business_constraints' in profile.strategic_context:
            context_parts.append("\n### Constraints:")
            for constraint in profile.strategic_context['business_constraints']:
                context_parts.append(f"- {constraint}")

        # Add question
        context_parts.extend([
            "",
            "### Strategic Question:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_general_context(profile: DomainProfile, question: str) -> str:
        """Create lightweight general context (name + description only)"""

        return f"""## Domain: {profile.name}

**Description:** {profile.description}

**Question:** {question}"""

    @staticmethod
    def auto_detect_context_type(question: str) -> str:
        """Automatically determine which context type to use"""

        question_lower = question.lower()

        # Technical indicators
        technical_keywords = ['implement', 'code', 'build', 'api', 'database', 'architecture',
                            'deploy', 'optimize', 'debug', 'framework', 'library']
        if any(kw in question_lower for kw in technical_keywords):
            return 'technical'

        # Cultural indicators
        cultural_keywords = ['content', 'lesson', 'audience', 'cultural', 'appropriate',
                           'sensitivity', 'tone', 'messaging', 'branding']
        if any(kw in question_lower for kw in cultural_keywords):
            return 'cultural'

        # Strategic indicators
        strategic_keywords = ['strategy', 'roadmap', 'prioritize', 'feature', 'business',
                            'growth', 'market', 'competitive', 'decision', 'direction']
        if any(kw in question_lower for kw in strategic_keywords):
            return 'strategic'

        # Default to general
        return 'general'
```

**3. Domain-Specific FlowiseManager**

Enhanced manager that integrates domain profiles with intelligent routing:

```python
# agentic_flywheel/domain_manager.py

from .flowise_manager import FlowiseManager
from .context_builder import ContextBuilder, DomainProfile
from typing import Optional, Dict, Any, List

class DomainSpecificFlowiseManager(FlowiseManager):
    """Extended FlowiseManager with domain profile support"""

    def __init__(self,
                 base_url: str,
                 domain_profile: Optional[DomainProfile] = None,
                 flow_registry_path: Optional[str] = None):

        super().__init__(base_url=base_url, flow_registry_path=flow_registry_path)

        self.domain_profile = domain_profile
        self.context_builder = ContextBuilder()

        # Enhance intent classification with domain keywords
        if domain_profile and domain_profile.specialized_keywords:
            self._enhance_intent_keywords(domain_profile.specialized_keywords)

    def _enhance_intent_keywords(self, specialized_keywords: List[str]):
        """Distribute specialized keywords to flows based on semantic relevance"""

        for flow_key, flow_config in self.flows.items():
            # Technical flow gets implementation-related keywords
            if flow_key == "technical-analysis":
                technical_kw = [kw for kw in specialized_keywords
                               if any(tech in kw.lower() for tech in
                                     ["implement", "code", "system", "api", "database", "deploy"])]
                flow_config.intent_keywords.extend(technical_kw)

            # Creative flow gets strategic/planning keywords
            elif flow_key == "creative-orientation":
                creative_kw = [kw for kw in specialized_keywords
                              if any(creative in kw.lower() for creative in
                                    ["strategy", "vision", "improve", "enhance", "design", "plan"])]
                flow_config.intent_keywords.extend(creative_kw)

            # Document flow gets content-related keywords
            elif "document" in flow_key or "content" in flow_key:
                content_kw = [kw for kw in specialized_keywords
                             if any(content in kw.lower() for content in
                                   ["content", "lesson", "cultural", "audience"])]
                flow_config.intent_keywords.extend(content_kw)

    async def contextualized_query(self,
                                   question: str,
                                   context_type: Optional[str] = None,
                                   session_id: Optional[str] = None,
                                   intent: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute query with automatic domain context injection

        Args:
            question: User's question
            context_type: 'technical', 'cultural', 'strategic', 'general', or 'auto' (default)
            session_id: Optional session ID for continuity
            intent: Optional explicit intent override

        Returns:
            Query result with domain context applied
        """

        if not self.domain_profile:
            # No domain profile, fallback to standard query
            return await self.adaptive_query(question, intent, session_id)

        # Auto-detect context type if not specified
        if not context_type or context_type == 'auto':
            context_type = self.context_builder.auto_detect_context_type(question)

        # Build context-enriched question
        if context_type == 'technical':
            enriched_question = self.context_builder.build_technical_context(
                self.domain_profile, question
            )
        elif context_type == 'cultural':
            enriched_question = self.context_builder.build_cultural_context(
                self.domain_profile, question
            )
        elif context_type == 'strategic':
            enriched_question = self.context_builder.build_strategic_context(
                self.domain_profile, question
            )
        else:  # general
            enriched_question = self.context_builder.build_general_context(
                self.domain_profile, question
            )

        # Generate domain-aware session ID if not provided
        if not session_id:
            domain_slug = self.domain_profile.id or self.domain_profile.name.lower().replace(" ", "-")
            session_id = self.generate_session_id(f"{domain_slug}-{context_type}")

        # Execute query with enriched context
        result = await self.adaptive_query(
            question=enriched_question,
            intent=intent,
            session_id=session_id
        )

        # Add domain metadata to result
        if "_metadata" in result:
            result["_metadata"]["domain_context"] = {
                "profile_id": self.domain_profile.id,
                "profile_name": self.domain_profile.name,
                "context_type": context_type,
                "context_enriched": True
            }

        return result
```

### Integration Points

**With Intent Classification Component:**
- Specialized keywords from domain profile enhance intent classification accuracy
- Domain-aware queries match better with appropriate flows
- Context type detection influences flow selection (technical → Technical Analysis, cultural → Creative Orientation)

**With MCP Server:**
- `flowise_domain_query` MCP tool exposes domain specialization
- Domain profiles can be selected via profile_id parameter
- Multi-domain users switch profiles per query

**With Redis Storage:**
- Domain profiles stored in Redis for persistence
- Key format: `domain:profile:{profile_id}`
- Session history tagged with domain_id for context continuity

**With Langfuse Tracing:**
- Every contextualized query logged with domain metadata
- Trace analysis can group by domain to measure specialization effectiveness
- Quality scores segmented by domain show relevance improvements

---

## 🌊 Creative Advancement Scenarios

### Scenario 1: Technical Stack Specialization — Precision Implementation Guidance

**User Intent**: Implement user progress tracking for language learning platform

**Current Structural Reality**:
- Domain profile exists for "Language Learning Platform"
- Stack: Next.js 14, PostgreSQL 15, Redis 7, AWS Lambda
- Constraints: Budget-conscious, < 2s page load, offline capability
- User has never explained stack in previous queries

**Natural Progression Steps**:

1. **Query Without Re-Explaining Context**
   - User asks simply: "How should I implement user progress tracking?"
   - No need to add: "In Next.js with PostgreSQL..." (domain profile handles this)

2. **Auto-Detection of Context Type**
   - System analyzes question: "implement" keyword detected → technical context
   - Context builder automatically selects technical enrichment strategy

3. **Technical Context Injection**
   - Original question enriched to:
     ```markdown
     ## Technical Implementation Context
     **Project:** Language Learning Platform (Production)

     ### Current Stack:
     - **Frontend:** Next.js 14, React 18, TailwindCSS, Framer Motion
     - **Backend:** Node.js 20, Express, tRPC
     - **Database:** PostgreSQL 15 (primary), Redis 7 (cache + sessions)
     - **Hosting:** Vercel (frontend), AWS Lambda (API), AWS RDS (database)

     ### Architecture Patterns:
     - Server-side rendering (SSR) for SEO
     - Edge functions for personalization
     - Event-driven background jobs

     ### Constraints:
     - Mobile-first design required
     - Offline capability for lessons
     - < 2s page load time target
     - Budget-conscious infrastructure ($500/mo limit)

     ### Implementation Question:
     How should I implement user progress tracking?
     ```

4. **Intent Classification Enhanced**
   - Specialized keywords ("spaced-repetition", "gamification") boost Technical Analysis score
   - Flow selected: "technical-analysis" (confidence: 0.94, up from 0.72 without domain keywords)

5. **Stack-Specific Response Generated**
   - AI response includes:
     - **PostgreSQL schema** for progress table with appropriate indexes
     - **Next.js API route** pattern: `/app/api/progress/[userId]/route.ts`
     - **Redis caching strategy** for frequently accessed progress data
     - **tRPC procedure** definition for type-safe progress updates
     - **Offline sync pattern** using Next.js service worker for offline capability
     - **Performance optimization**: Edge function for progress badge rendering (< 50ms)
     - **Cost optimization**: Caching strategy to stay within $500/mo budget

6. **Immediate Actionability**
   - User receives code snippets in their exact stack (Next.js 14 app router, not pages router)
   - Database schema matches PostgreSQL 15 features they're using
   - Infrastructure recommendations fit AWS Lambda + Vercel architecture
   - No mental translation needed—copy, adapt, deploy

**Achieved Outcome**:
- ✅ User saved 5-10 minutes not re-explaining technical stack
- ✅ Response relevance: 95% (vs 60% for generic "progress tracking" answer)
- ✅ Implementation time reduced: Specific code patterns provided, not abstract concepts
- ✅ Confidence increased: AI "understands" their environment, responses feel expert-level
- ✅ Budget respected: Recommendations stay within stated $500/mo constraint

---

### Scenario 2: Cultural Context Specialization — Authentic Content Creation

**User Intent**: Create a lesson on French idiomatic expressions for English speakers

**Current Structural Reality**:
- Domain profile: "Language Learning Platform (Production)"
- Cultural context: Target audience = English speakers learning French, age 18-45
- Sensitivity: CEFR-aligned, native speaker reviewed, authentic cultural context
- Content standards: Family-friendly, inclusive language, French cultural nuances respected

**Natural Progression Steps**:

1. **Content Request**
   - User asks: "Create a lesson on common French idiomatic expressions"
   - No cultural context explicitly stated in query

2. **Auto-Detection of Cultural Context**
   - System detects: "lesson", "content" keywords → cultural context type
   - Context builder selects cultural enrichment strategy

3. **Cultural Context Injection**
   - Question enriched to:
     ```markdown
     ## Cultural Content Context
     **Domain:** Language Learning Platform (Production)
     **Type:** Education Technology

     ### Target Audience:
     - **Primary:** English-speaking adults learning French
     - **Age_range:** 18-45
     - **Proficiency_levels:** Beginner, Intermediate

     ### Cultural Sensitivity Requirements:
     - Respect for French cultural nuances and idioms
     - Age-appropriate content (family-friendly)
     - Inclusive language (gender-neutral examples)

     ### Content Standards:
     - CEFR-aligned (Common European Framework)
     - Native speaker reviewed
     - Authentic cultural context for each lesson

     ### Content Request:
     Create a lesson on common French idiomatic expressions
     ```

4. **Culturally-Informed Response**
   - AI generates lesson with:
     - **CEFR Level Classification**: Marks expressions as A2/B1/B2 appropriate
     - **English Speaker Focus**: Explains false friends and common mistakes English speakers make
     - **Cultural Context**: Each idiom includes origin story and cultural usage notes
     - **Inclusive Examples**: Uses gender-neutral names in example sentences
     - **Family-Friendly Selection**: Avoids expressions with crude origins or mature themes
     - **Audio Pronunciation Guide**: Includes IPA and pronunciation tips for English speakers
     - **Example Conversations**: Realistic scenarios where expressions naturally occur

5. **Authentic Cultural Depth**
   - Expression: "Avoir le cafard" (to have the blues)
     - **Literal translation**: "To have the cockroach"
     - **Cultural origin**: Baudelaire poem reference (explained at appropriate depth for learners)
     - **Usage context**: Informal, emotional state, typically with close friends
     - **False friend warning**: Not related to coffee (café) despite similar spelling
     - **Example**: "Depuis qu'elle est partie, j'ai le cafard." (Since she left, I've had the blues)
     - **CEFR level**: B1 (Intermediate)

6. **Content Quality Alignment**
   - All expressions vetted against stated content standards
   - Lesson structure matches platform's existing lesson format
   - No additional review needed—content ready for native speaker validation

**Achieved Outcome**:
- ✅ Cultural authenticity maintained automatically (no generic "French phrases" list)
- ✅ Target audience perfectly aligned (English speakers, not generic learners)
- ✅ CEFR standards applied without explicit reminder
- ✅ Content appropriate for stated audience (18-45, family-friendly)
- ✅ Time saved: 30+ minutes of cultural context establishment
- ✅ Quality increased: Authentic cultural nuances included by default

---

### Scenario 3: Strategic Context Specialization — Constraint-Aware Prioritization

**User Intent**: Decide which features to build next for product roadmap

**Current Structural Reality**:
- Domain profile: "Language Learning Platform (Production)"
- Business stage: Seed-stage SaaS startup
- Team: 3 engineers, 1 content creator (4 total)
- Runway: 18 months
- Goal: 1000 MAU in 6 months
- Top priority: User engagement and retention

**Natural Progression Steps**:

1. **Strategic Question**
   - User asks: "We have 10 feature ideas. Which should we prioritize for the next quarter?"
   - Lists features: Spaced repetition algorithm, social sharing, offline mode, pronunciation AI, progress dashboard, community forums, mobile app, gamification system, AI tutor chat, content marketplace

2. **Auto-Detection of Strategic Context**
   - System detects: "prioritize", "features", "roadmap" → strategic context
   - Context builder selects strategic enrichment

3. **Strategic Context Injection**
   - Question enriched with:
     ```markdown
     ## Strategic Planning Context
     **Business:** Language Learning Platform (Production)
     **Stage:** Seed-stage SaaS startup

     ### Team:
     - Engineering: 3
     - Content: 1
     - Total: 4

     ### Current Priorities (ordered):
     1. User engagement and retention (top)
     2. Content quality and authenticity
     3. Gamification features
     4. Mobile app parity

     ### Constraints:
     - Runway: 18 months
     - Must reach 1000 MAU in 6 months
     - Limited marketing budget

     ### Strategic Question:
     We have 10 feature ideas. Which should we prioritize for the next quarter?
     [Feature list]
     ```

4. **Constraint-Aware Prioritization**
   - AI response structured as:
     - **Tier 1 (Build Now)**: Features that directly drive engagement + feasible for 4-person team
       1. **Spaced Repetition Algorithm** - Retention driver, high engagement impact, 2-3 week build
       2. **Progress Dashboard** - Visible achievement, motivation driver, 1 week build
       3. **Gamification System** - Engagement multiplier, aligns with priority #3, 2-3 week build

     - **Tier 2 (Next Quarter)**: High value but resource-intensive for current team size
       4. **Offline Mode** - Technical complexity high for 3-person team, defer until PMF
       5. **Pronunciation AI** - Complex ML integration, consider third-party solution first

     - **Tier 3 (Defer)**: Low ROI given current constraints
       6. **Community Forums** - Requires moderation (no budget for moderator)
       7. **Content Marketplace** - Complex business model, premature for seed stage
       8. **Mobile App** - Duplication of effort, focus on mobile web first
       9. **AI Tutor Chat** - Resource-intensive, low differentiation
       10. **Social Sharing** - Viral mechanics work at scale, premature at 0 MAU

5. **Constraint-Specific Reasoning**
   - **Team Size**: "With 3 engineers, building mobile app + web simultaneously dilutes focus"
   - **Runway**: "18 months means 3-4 major feature cycles. Choose engagement drivers that validate PMF"
   - **MAU Goal**: "Spaced repetition + gamification have highest correlation with retention in education apps"
   - **Budget**: "Community forums require $3-5K/mo moderation costs—not feasible with limited budget"
   - **Content Team**: "1 content creator = content marketplace creates unsustainable content demand"

6. **Actionable Recommendations**
   - **Q1 Roadmap**: Spaced repetition (weeks 1-3), Progress dashboard (week 4), Gamification v1 (weeks 5-7), Polish + testing (week 8)
   - **Success Metrics**: Track engagement rate increase (target: +40%), retention improvement (target: D7 retention +25%)
   - **Risk Mitigation**: Spaced repetition algorithm can use existing library (Supermemo SM-2), reducing build time

**Achieved Outcome**:
- ✅ Prioritization respects actual team size (4 people, not idealized team)
- ✅ Runway constraint drives "validate PMF first" approach (not "build everything")
- ✅ Goal alignment: All Tier 1 features directly drive 1000 MAU target
- ✅ Resource reality: Defers features requiring skills/roles they don't have
- ✅ Immediately executable: Specific quarter plan with week-by-week breakdown
- ✅ Decision confidence: CEO can defend prioritization to investors with clear rationale

---

### Scenario 4: Multi-Domain Context Switching — Professional Flexibility

**User Intent**: Developer works on multiple projects, needs domain-specific responses for each

**Current Structural Reality**:
- User maintains 3 domain profiles:
  1. **Production App** (Language Learning Platform - detailed above)
  2. **Internal Tools** (Admin dashboard for content management)
  3. **Marketing Site** (Company website with blog)
- Currently working in "Production App" context
- Needs to switch to "Internal Tools" for a quick question

**Natural Progression Steps**:

1. **Current Context: Production App**
   - User: "How do I implement spaced repetition?"
   - System uses Production App profile → Next.js + PostgreSQL implementation returned

2. **Context Switch Request**
   - User: "@internal-tools How do I bulk upload content to the CMS?"
   - User explicitly switches context with `@internal-tools` prefix

3. **Profile Switch**
   - System loads "Internal Tools" domain profile:
     - Stack: React Admin, Django REST, PostgreSQL, S3 for storage
     - Team: Just the user (solo internal project)
     - Priority: Speed of implementation > code quality

4. **New Context Applied**
   - Question enriched with Internal Tools technical context:
     ```markdown
     ## Technical Implementation Context
     **Project:** Internal Tools (Admin Dashboard)

     ### Current Stack:
     - **Frontend:** React Admin
     - **Backend:** Django REST Framework
     - **Database:** PostgreSQL
     - **Storage:** AWS S3

     ### Context:
     - Internal tool (no external users)
     - Solo developer (speed over perfection)
     - Priority: Fast iteration

     ### Implementation Question:
     How do I bulk upload content to the CMS?
     ```

5. **Context-Appropriate Response**
   - AI provides Django REST + React Admin solution (not Next.js)
   - Suggests: "Quick implementation: Use React Admin's import button + CSV parser"
   - Recommends: "Since it's internal, skip extensive validation—you control the data source"
   - Notes: "For 1000+ items, add background job, but for < 100, synchronous upload is fine"

6. **Effortless Return to Previous Context**
   - User: "Thanks! Now back to the production app—what's the schema for that spaced repetition table?"
   - No explicit switch needed (defaults back to primary "Production App" profile)
   - System remembers previous Production App session context

**Achieved Outcome**:
- ✅ Multi-project developer doesn't need separate AI chat sessions
- ✅ Context switching takes 2 seconds (`@profile-name` prefix)
- ✅ Each project gets appropriate stack-specific guidance
- ✅ Internal tool gets "quick and pragmatic" advice vs production "robust and scalable"
- ✅ Session continuity maintained per domain (can resume Production App context)

---

## 🔧 Implementation Guidelines

### Domain Profile Management

**Profile Storage Strategy:**

```python
# agentic_flywheel/profile_manager.py

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from .context_builder import DomainProfile

class DomainProfileManager:
    """Manage domain profiles: create, load, update, switch"""

    def __init__(self, profiles_directory: str = "~/.agentic-flywheel/profiles"):
        self.profiles_dir = Path(profiles_directory).expanduser()
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.active_profile_id: Optional[str] = None
        self.profiles_cache: Dict[str, DomainProfile] = {}

    def create_profile(self, profile_data: Dict) -> DomainProfile:
        """Create new domain profile from dictionary"""

        profile = DomainProfile(
            id=profile_data['id'],
            name=profile_data['name'],
            description=profile_data['description'],
            technical_context=profile_data.get('technical_context'),
            cultural_context=profile_data.get('cultural_context'),
            strategic_context=profile_data.get('strategic_context'),
            specialized_keywords=profile_data.get('specialized_keywords'),
            privacy_level=profile_data.get('privacy_level', 'internal')
        )

        # Save to YAML
        self._save_profile(profile)

        # Cache
        self.profiles_cache[profile.id] = profile

        return profile

    def load_profile(self, profile_id: str) -> Optional[DomainProfile]:
        """Load profile from disk or cache"""

        # Check cache first
        if profile_id in self.profiles_cache:
            return self.profiles_cache[profile_id]

        # Load from disk
        profile_path = self.profiles_dir / f"{profile_id}.yaml"

        if not profile_path.exists():
            return None

        with open(profile_path, 'r') as f:
            data = yaml.safe_load(f)

        profile = DomainProfile(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            technical_context=data.get('technical_context'),
            cultural_context=data.get('cultural_context'),
            strategic_context=data.get('strategic_context'),
            specialized_keywords=data.get('specialized_keywords'),
            privacy_level=data.get('privacy_level', 'internal')
        )

        # Cache
        self.profiles_cache[profile_id] = profile

        return profile

    def list_profiles(self) -> List[Dict[str, str]]:
        """List all available profiles (metadata only)"""

        profiles = []

        for profile_file in self.profiles_dir.glob("*.yaml"):
            with open(profile_file, 'r') as f:
                data = yaml.safe_load(f)

            profiles.append({
                'id': data['id'],
                'name': data['name'],
                'description': data['description'],
                'privacy_level': data.get('privacy_level', 'internal')
            })

        return profiles

    def switch_profile(self, profile_id: str) -> bool:
        """Switch active profile"""

        profile = self.load_profile(profile_id)

        if not profile:
            return False

        self.active_profile_id = profile_id
        return True

    def get_active_profile(self) -> Optional[DomainProfile]:
        """Get currently active profile"""

        if not self.active_profile_id:
            return None

        return self.load_profile(self.active_profile_id)

    def _save_profile(self, profile: DomainProfile):
        """Save profile to YAML file"""

        profile_path = self.profiles_dir / f"{profile.id}.yaml"

        data = {
            'id': profile.id,
            'name': profile.name,
            'description': profile.description,
            'technical_context': profile.technical_context,
            'cultural_context': profile.cultural_context,
            'strategic_context': profile.strategic_context,
            'specialized_keywords': profile.specialized_keywords,
            'privacy_level': profile.privacy_level
        }

        with open(profile_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
```

### MCP Tool Integration

**Enhanced `flowise_domain_query` MCP Tool:**

```python
# In mcp_server.py

types.Tool(
    name="flowise_domain_query",
    description="Query Flowise with automatic domain context injection based on profile",
    inputSchema={
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Question to ask with domain context"
            },
            "profile_id": {
                "type": "string",
                "description": "Domain profile ID to use (optional, uses active profile if not specified)"
            },
            "context_type": {
                "type": "string",
                "enum": ["auto", "technical", "cultural", "strategic", "general"],
                "description": "Type of context to inject (default: auto-detect)",
                "default": "auto"
            },
            "session_id": {
                "type": "string",
                "description": "Session ID for conversation continuity"
            }
        },
        "required": ["question"]
    }
)

# Handler implementation
async def handle_flowise_domain_query(arguments: dict) -> Dict[str, Any]:
    """Execute domain-aware Flowise query"""

    question = arguments["question"]
    profile_id = arguments.get("profile_id")
    context_type = arguments.get("context_type", "auto")
    session_id = arguments.get("session_id")

    # Load profile
    profile = profile_manager.get_active_profile() if not profile_id else profile_manager.load_profile(profile_id)

    if not profile:
        return {"error": "No active domain profile. Use flowise_query for generic queries."}

    # Create domain-specific manager
    domain_manager = DomainSpecificFlowiseManager(
        base_url=flowise_base_url,
        domain_profile=profile
    )

    # Execute contextualized query
    result = await domain_manager.contextualized_query(
        question=question,
        context_type=context_type,
        session_id=session_id
    )

    return result
```

### Privacy and Conflict Resolution

**Privacy Levels:**

- **Public**: Safe to share with external parties, appears in documentation examples
- **Internal**: Team use only, not shared outside organization
- **Confidential**: Sensitive business info (competitors, financials), extra access controls

**Conflict Resolution Framework:**

When domain constraints conflict with general best practices:

1. **Acknowledge the Conflict**: "Standard practice recommends X, but your constraint Y suggests Z instead."
2. **Explain the Tradeoff**: "This means you'll sacrifice A to gain B."
3. **Provide Both Options**: "Option 1 (standard): [details]. Option 2 (constraint-adapted): [details]."
4. **Recommend Based on Context**: "Given your 18-month runway and 4-person team, I recommend Option 2."
5. **Document the Decision**: Tag response with `constraint_override` metadata for future reference

**Example Conflict:**

- **Best Practice**: Microservices architecture for scalability
- **Constraint**: 3-person team, limited ops experience
- **Resolution**: "While microservices are ideal for scale, your team size makes a monolith more practical. Recommend modular monolith architecture that can split into services later if needed."

---

## 🧪 Quality Validation

### Success Metrics

**Response Relevance:**
- **Target**: 90%+ of responses reference domain-specific context (stack, audience, constraints)
- **Measurement**: User validation survey after responses (5-point scale: "Was this specific to your context?")
- **Baseline**: Generic responses average 60% relevance

**Context Re-Explanation Reduction:**
- **Target**: 50%+ reduction in users re-stating technical stack, cultural context, or constraints
- **Measurement**: Compare conversation logs pre/post domain profiles, count context re-statements
- **Success Example**: Pre-profile: 3 stack mentions per 10 queries. Post-profile: 0.5 mentions per 10 queries

**Cultural Appropriateness:**
- **Target**: Zero cultural insensitivity incidents
- **Measurement**: User reports of inappropriate content, cultural consultant review
- **Validation**: Quarterly audit of culturally-enriched responses

**Strategic Actionability:**
- **Target**: 80%+ of strategic advice directly actionable within stated constraints
- **Measurement**: User feedback on whether recommendation was implemented
- **Success Indicator**: "Used this advice as-is" vs "Had to heavily adapt"

**Profile Adoption:**
- **Target**: 70%+ of active users create at least one domain profile within first month
- **Measurement**: Track profile creation events
- **Indicator**: Value proposition clear if majority adopt

### Testing Scenarios

**Test 1: Technical Context Accuracy**
```python
# Arrange
profile = create_test_profile(
    stack={"frontend": ["Next.js 14"], "database": ["PostgreSQL 15"]}
)
manager = DomainSpecificFlowiseManager(domain_profile=profile)

# Act
result = await manager.contextualized_query(
    question="How do I implement authentication?",
    context_type="technical"
)

# Assert
assert "Next.js" in result['text']  # Response mentions their stack
assert "PostgreSQL" in result['text']
assert result['_metadata']['domain_context']['context_enriched'] == True
```

**Test 2: Cultural Context Application**
```python
# Arrange
profile = create_test_profile(
    cultural_context={
        "target_audience": {"age_range": "13-18"},
        "cultural_sensitivity": ["Family-friendly content required"]
    }
)
manager = DomainSpecificFlowiseManager(domain_profile=profile)

# Act
result = await manager.contextualized_query(
    question="Create a lesson on modern slang",
    context_type="cultural"
)

# Assert
# Response should avoid mature content given age range
assert not contains_mature_content(result['text'])
assert "appropriate for teens" in result['text'].lower()
```

**Test 3: Specialized Keyword Integration**
```python
# Arrange
profile = create_test_profile(
    specialized_keywords=["spaced-repetition", "gamification"]
)
manager = DomainSpecificFlowiseManager(domain_profile=profile)

# Act - Question with specialized keyword
result = await manager.contextualized_query(
    question="How do I implement spaced repetition?"
)

# Assert - Intent classification should be more confident
metadata = result['_metadata']
assert metadata['intent_confidence'] >= 0.85  # Higher due to keyword match
```

**Test 4: Multi-Domain Profile Switching**
```python
# Arrange
profile_mgr = DomainProfileManager()
prod_profile = profile_mgr.create_profile({"id": "prod", "name": "Production", ...})
admin_profile = profile_mgr.create_profile({"id": "admin", "name": "Admin Tools", ...})

# Act - Switch between profiles
profile_mgr.switch_profile("prod")
result1 = get_active_profile_response("How do I deploy?")

profile_mgr.switch_profile("admin")
result2 = get_active_profile_response("How do I deploy?")

# Assert - Different responses based on active profile
assert result1['_metadata']['domain_context']['profile_id'] == "prod"
assert result2['_metadata']['domain_context']['profile_id'] == "admin"
```

---

## 🔗 Integration References

### Component Dependencies

**Intent Classification Component**: Specialized keywords from domain profile enhance keyword matching, improving routing accuracy by 15-20%

**Flowise Integration Component**: All domain-enriched queries pass through FlowiseManager's adaptive_query method

**MCP Server Component**: `flowise_domain_query` tool exposes domain specialization to Claude and MCP clients

**Redis Storage Component**: Domain profiles stored in Redis for fast access and session persistence

**Langfuse Tracing Component**: Domain metadata tagged on every trace for segmented analysis

### External References

**RISE Framework**: Domain specialization follows creative orientation principles—focus on what users CREATE with specialized context, not problems it solves

**YAML Specification**: Domain profiles use YAML for human-readable, version-controllable configuration

**CEFR Standards**: Cultural context for education domains references Common European Framework of Reference for Languages

---

## 🎯 Implementation Roadmap

### Phase 1: Core Domain Profile Support (Week 1)

**Deliverables:**
1. `DomainProfile` dataclass with all context types
2. `ContextBuilder` with technical, cultural, strategic builders
3. `DomainSpecificFlowiseManager` extending FlowiseManager
4. YAML profile loading from filesystem

**Validation:**
- Load sample profile, verify context injection works
- Test all 3 context builders produce formatted output
- Confirm specialized keywords enhance intent classification

### Phase 2: Profile Management (Week 2)

**Deliverables:**
1. `DomainProfileManager` for create/load/switch operations
2. CLI commands for profile management
3. MCP tool `flowise_domain_query` enhancement
4. Multi-domain profile support

**Validation:**
- Create, load, switch profiles via CLI
- Multiple profiles coexist without conflicts
- MCP tool accepts `profile_id` parameter

### Phase 3: Advanced Features (Week 3)

**Deliverables:**
1. Auto-detection of context type
2. Profile templates for common domains
3. Privacy level enforcement
4. Conflict resolution framework

**Validation:**
- Auto-detection accuracy > 80%
- Templates accelerate profile creation
- Privacy controls prevent leakage

---

## 📊 Success Narrative

### How Users Experience This Specification

**Day 1**: A developer creates their first domain profile for a Next.js + PostgreSQL project. Takes 10 minutes. First query: "How do I implement auth?" Response includes Next.js-specific middleware, PostgreSQL user table schema, JWT patterns for their stack. Developer thinks: "This understands my project."

**Week 1**: Developer stops prefacing questions with tech stack details. Saves 2-3 minutes per query. Over 20 queries, that's 40-60 minutes saved. More importantly: cognitive load reduced, flow state maintained.

**Week 2**: Content creator joins team, gets access to same domain profile. Asks: "Create a lesson on verb conjugation." Receives culturally appropriate content matching platform's CEFR standards without explaining audience. Content creator: "It already knows our audience."

**Month 1**: Team has 3 domain profiles (Production, Admin Tools, Marketing Site). Developers switch contexts fluently. CTO asks strategic question about roadmap. Receives constraint-aware prioritization based on actual team size and runway. Board presentation uses this analysis.

**Month 3**: New engineer joins. Inherits all 3 domain profiles. First day, asks implementation questions. Receives onboarding-quality responses tailored to company's stack. Tech lead: "Domain profiles are our institutional knowledge."

**Month 6**: Relevance scores show 92% of responses reference specific context. Context re-explanation down 65%. Team productivity estimated +15% from reduced friction. Domain specialization ROI: 30:1 (setup time vs time saved).

---

**Specification Status:** Draft → Ready for Implementation
**Confidence Level:** High (90%)
**Autonomous Implementation:** ✅ Yes - Complete implementation patterns provided
**RISE Compliance:** ✅ Creative orientation throughout, precision value creation emphasized
