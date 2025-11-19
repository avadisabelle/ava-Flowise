"""
Agentic Flywheel Context Builder Module

This module enables users to create deeply relevant, precision-tailored AI
interactions that understand their specific domain context without requiring
constant re-explanation. Through intelligent context building, users experience
effortless contextual understanding and actionable, stack-specific guidance.

Based on domain-specialization.spec.md (v1.0) - RISE Framework
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DomainProfile:
    """
    Complete domain profile with all context types.

    This dataclass captures everything the AI needs to understand a specific
    domain, enabling responses that automatically reflect technical stack,
    cultural context, and business constraints.
    """
    # Identity
    id: str
    name: str
    description: str
    version: str = "1.0"

    # Context types
    technical_context: Optional[Dict[str, Any]] = None
    cultural_context: Optional[Dict[str, Any]] = None
    strategic_context: Optional[Dict[str, Any]] = None

    # Intent classification enhancement
    specialized_keywords: List[str] = field(default_factory=list)

    # Metadata
    privacy_level: str = "internal"  # public, internal, confidential
    owners: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ContextBuilder:
    """
    Builds rich, formatted context for domain-specific queries.

    This class transforms domain profiles into structured context strings
    that enable AI responses to be automatically relevant and actionable
    within the user's specific environment.
    """

    # Keywords for auto-detecting context type
    TECHNICAL_KEYWORDS = [
        'implement', 'code', 'build', 'api', 'database', 'architecture',
        'deploy', 'optimize', 'debug', 'framework', 'library', 'function',
        'class', 'method', 'endpoint', 'server', 'client', 'schema',
        'migration', 'test', 'performance', 'security', 'authentication'
    ]

    CULTURAL_KEYWORDS = [
        'content', 'lesson', 'audience', 'cultural', 'appropriate',
        'sensitivity', 'tone', 'messaging', 'branding', 'voice',
        'communication', 'language', 'localization', 'translation',
        'inclusive', 'accessible', 'user-facing', 'copy', 'narrative'
    ]

    STRATEGIC_KEYWORDS = [
        'strategy', 'roadmap', 'prioritize', 'feature', 'business',
        'growth', 'market', 'competitive', 'decision', 'direction',
        'plan', 'vision', 'goal', 'milestone', 'timeline', 'budget',
        'resource', 'team', 'hire', 'investment', 'revenue', 'user'
    ]

    @staticmethod
    def build_technical_context(profile: DomainProfile, question: str) -> str:
        """
        Creates technical context with stack and constraints.

        This enables AI responses to reference actual technologies and
        infrastructure, eliminating the need for users to mentally translate
        generic advice into their specific context.

        Args:
            profile: Domain profile with technical context
            question: The user's technical question

        Returns:
            Formatted context string with question

        Example:
            >>> context = ContextBuilder.build_technical_context(
            ...     profile,
            ...     "How do I implement caching?"
            ... )
            >>> # Returns:
            >>> # ## Technical Implementation Context
            >>> # **Project:** Language Learning Platform
            >>> # ### Current Stack:
            >>> # - **Frontend:** Next.js 14, React 18
            >>> # - **Backend:** Node.js 20, Express
            >>> # - **Database:** PostgreSQL 15, Redis 7
            >>> # ...
            >>> # ### Implementation Question:
            >>> # How do I implement caching?
        """
        if not profile.technical_context:
            return question

        context_parts = [
            "## Technical Implementation Context",
            f"**Project:** {profile.name}",
            ""
        ]

        # Format stack information
        stack = profile.technical_context.get('stack', {})
        if stack:
            context_parts.append("### Current Stack:")
            for category, technologies in stack.items():
                if isinstance(technologies, list):
                    tech_list = ", ".join(technologies)
                else:
                    tech_list = str(technologies)
                context_parts.append(f"- **{category.title()}:** {tech_list}")
            context_parts.append("")

        # Add architecture patterns if present
        architecture_patterns = profile.technical_context.get('architecture_patterns', [])
        if architecture_patterns:
            context_parts.append("### Architecture Patterns:")
            for pattern in architecture_patterns:
                context_parts.append(f"- {pattern}")
            context_parts.append("")

        # Add constraints
        constraints = profile.technical_context.get('constraints', [])
        if constraints:
            context_parts.append("### Constraints:")
            for constraint in constraints:
                context_parts.append(f"- {constraint}")
            context_parts.append("")

        # Add integrations if present
        integrations = profile.technical_context.get('integrations', [])
        if integrations:
            context_parts.append("### Existing Integrations:")
            for integration in integrations:
                context_parts.append(f"- {integration}")
            context_parts.append("")

        # Add the actual question
        context_parts.extend([
            "### Implementation Question:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_cultural_context(profile: DomainProfile, question: str) -> str:
        """
        Creates cultural context with audience and sensitivities.

        This enables AI responses to demonstrate authentic domain understanding,
        respecting cultural nuances and content standards without explicit
        reminders.

        Args:
            profile: Domain profile with cultural context
            question: The user's content-related question

        Returns:
            Formatted context string with question

        Example:
            >>> context = ContextBuilder.build_cultural_context(
            ...     profile,
            ...     "Create a lesson about French greetings"
            ... )
            >>> # Returns cultural sensitivity requirements, target audience,
            >>> # content standards, then the question
        """
        if not profile.cultural_context:
            return question

        context_parts = [
            "## Cultural Content Context",
            f"**Domain:** {profile.name}",
            f"**Type:** {profile.cultural_context.get('domain_type', 'General')}",
            ""
        ]

        # Target audience
        target_audience = profile.cultural_context.get('target_audience')
        if target_audience:
            context_parts.append("### Target Audience:")
            if isinstance(target_audience, dict):
                for key, value in target_audience.items():
                    display_key = key.replace('_', ' ').title()
                    if isinstance(value, list):
                        value = ", ".join(str(v) for v in value)
                    context_parts.append(f"- **{display_key}:** {value}")
            else:
                context_parts.append(f"- {target_audience}")
            context_parts.append("")

        # Cultural sensitivity requirements
        cultural_sensitivity = profile.cultural_context.get('cultural_sensitivity', [])
        if cultural_sensitivity:
            context_parts.append("### Cultural Sensitivity Requirements:")
            for requirement in cultural_sensitivity:
                context_parts.append(f"- {requirement}")
            context_parts.append("")

        # Content standards
        content_standards = profile.cultural_context.get('content_standards', [])
        if content_standards:
            context_parts.append("### Content Standards:")
            for standard in content_standards:
                context_parts.append(f"- {standard}")
            context_parts.append("")

        # Add question
        context_parts.extend([
            "### Content Request:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_strategic_context(profile: DomainProfile, question: str) -> str:
        """
        Creates strategic context with business stage and constraints.

        This enables AI responses to provide pragmatic, executable strategies
        that account for actual team size, budget, and priorities rather than
        theoretical best practices.

        Args:
            profile: Domain profile with strategic context
            question: The user's strategic question

        Returns:
            Formatted context string with question

        Example:
            >>> context = ContextBuilder.build_strategic_context(
            ...     profile,
            ...     "Should we build a mobile app?"
            ... )
            >>> # Returns business stage, team composition, priorities,
            >>> # constraints, then the question
        """
        if not profile.strategic_context:
            return question

        context_parts = [
            "## Strategic Planning Context",
            f"**Business:** {profile.name}",
            f"**Stage:** {profile.strategic_context.get('business_stage', 'Unknown')}",
            ""
        ]

        # Team composition
        team_composition = profile.strategic_context.get('team_composition')
        if team_composition:
            context_parts.append("### Team:")
            total = team_composition.get('total', sum(team_composition.values()))
            for role, count in team_composition.items():
                if role != 'total':
                    context_parts.append(f"- {role.replace('_', ' ').title()}: {count}")
            context_parts.append(f"- **Total:** {total}")
            context_parts.append("")

        # Current priorities
        current_priorities = profile.strategic_context.get('current_priorities', [])
        if current_priorities:
            context_parts.append("### Current Priorities (ordered):")
            for i, priority in enumerate(current_priorities, 1):
                context_parts.append(f"{i}. {priority}")
            context_parts.append("")

        # Business constraints
        business_constraints = profile.strategic_context.get('business_constraints', [])
        if business_constraints:
            context_parts.append("### Constraints:")
            for constraint in business_constraints:
                context_parts.append(f"- {constraint}")
            context_parts.append("")

        # Competitive position
        competitive_position = profile.strategic_context.get('competitive_position', [])
        if competitive_position:
            context_parts.append("### Competitive Position:")
            for position in competitive_position:
                context_parts.append(f"- {position}")
            context_parts.append("")

        # Add question
        context_parts.extend([
            "### Strategic Question:",
            question
        ])

        return "\n".join(context_parts)

    @staticmethod
    def build_general_context(profile: DomainProfile, question: str) -> str:
        """
        Creates lightweight general context (name + description only).

        This is used when the question doesn't clearly fit into technical,
        cultural, or strategic categories, or when you want minimal context
        enrichment.

        Args:
            profile: Domain profile
            question: The user's question

        Returns:
            Minimal context string with question

        Example:
            >>> context = ContextBuilder.build_general_context(profile, "...")
            >>> # Returns:
            >>> # ## Domain: Language Learning Platform
            >>> # **Description:** ...
            >>> # **Question:** ...
        """
        return f"""## Domain: {profile.name}

**Description:** {profile.description}

**Question:** {question}"""

    @staticmethod
    def auto_detect_context_type(question: str) -> str:
        """
        Automatically determines which context type to use.

        This analyzes the question to detect whether it's technical,
        cultural, strategic, or general in nature, enabling automatic
        selection of the most appropriate context enrichment.

        Args:
            question: The user's question

        Returns:
            Context type: 'technical', 'cultural', 'strategic', or 'general'

        Example:
            >>> context_type = ContextBuilder.auto_detect_context_type(
            ...     "How do I implement OAuth2 authentication?"
            ... )
            >>> context_type
            'technical'
        """
        question_lower = question.lower()

        # Count matches for each category
        technical_matches = sum(
            1 for kw in ContextBuilder.TECHNICAL_KEYWORDS
            if kw in question_lower
        )
        cultural_matches = sum(
            1 for kw in ContextBuilder.CULTURAL_KEYWORDS
            if kw in question_lower
        )
        strategic_matches = sum(
            1 for kw in ContextBuilder.STRATEGIC_KEYWORDS
            if kw in question_lower
        )

        # Determine best match
        max_matches = max(technical_matches, cultural_matches, strategic_matches)

        if max_matches == 0:
            logger.debug("No context type keywords detected, using general context")
            return 'general'

        if technical_matches == max_matches:
            logger.debug(f"Detected technical context ({technical_matches} keywords)")
            return 'technical'
        elif strategic_matches == max_matches:
            logger.debug(f"Detected strategic context ({strategic_matches} keywords)")
            return 'strategic'
        elif cultural_matches == max_matches:
            logger.debug(f"Detected cultural context ({cultural_matches} keywords)")
            return 'cultural'

        return 'general'

    @staticmethod
    def build_context(
        profile: DomainProfile,
        question: str,
        context_type: Optional[str] = None
    ) -> str:
        """
        Builds appropriate context based on automatic detection or explicit type.

        This is the main entry point for context building, automatically
        selecting the right context enrichment strategy.

        Args:
            profile: Domain profile
            question: The user's question
            context_type: Optional explicit context type, auto-detected if None

        Returns:
            Formatted context string with question

        Example:
            >>> # Auto-detect context type
            >>> context = ContextBuilder.build_context(profile, question)
            >>>
            >>> # Explicit context type
            >>> context = ContextBuilder.build_context(
            ...     profile,
            ...     question,
            ...     context_type='technical'
            ... )
        """
        # Auto-detect if not specified
        if context_type is None:
            context_type = ContextBuilder.auto_detect_context_type(question)

        # Build appropriate context
        if context_type == 'technical':
            return ContextBuilder.build_technical_context(profile, question)
        elif context_type == 'cultural':
            return ContextBuilder.build_cultural_context(profile, question)
        elif context_type == 'strategic':
            return ContextBuilder.build_strategic_context(profile, question)
        else:
            return ContextBuilder.build_general_context(profile, question)
