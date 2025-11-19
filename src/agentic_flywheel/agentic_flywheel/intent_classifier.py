"""
Agentic Flywheel Intent Classification Module

This module enables users to create a natural expertise-finding system that
connects their questions to the most capable AI agent without requiring
technical knowledge of the system's architecture. Through intelligent intent
classification with confidence scoring, users experience effortless expertise
discovery and continuous conversation coherence.

Based on intent-classification.spec.md (v1.0) - RISE Framework
"""

import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class IntentClassifier:
    """
    Manifests natural expertise discovery through intelligent intent classification.

    This class transforms arbitrary natural language questions into confident,
    context-aware routing decisions, creating a self-improving intelligence
    that learns from routing outcomes.
    """

    # Common stop words to exclude from keyword extraction
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "up", "about", "into", "through", "during",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "should", "could", "may", "might",
        "can", "how", "what", "when", "where", "who", "which", "why", "this",
        "that", "these", "those", "i", "you", "we", "they", "my", "your", "our"
    }

    # Confidence thresholds
    HIGH_CONFIDENCE_THRESHOLD = 0.70
    MEDIUM_CONFIDENCE_THRESHOLD = 0.40

    def __init__(
        self,
        flow_registry: Dict[str, Dict],
        persistence_manager=None,
        observability_manager=None,
        default_flow: str = "creative-orientation"
    ):
        """
        Initialize the intent classifier.

        Args:
            flow_registry: Dictionary mapping flow keys to flow configurations
            persistence_manager: Optional persistence manager for session context
            observability_manager: Optional observability manager for logging
            default_flow: Default flow to use for low-confidence classifications
        """
        self.flow_registry = flow_registry
        self.persistence = persistence_manager
        self.observability = observability_manager
        self.default_flow = default_flow
        self._classification_stats = {
            'total': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0
        }

    def extract_keywords(self, question: str) -> List[str]:
        """
        Extracts meaningful keywords from a question.

        This creates a semantic fingerprint of the question by removing
        stop words and identifying technical terms, domain concepts, and
        action verbs.

        Args:
            question: The user's question text

        Returns:
            List of extracted keywords

        Example:
            >>> classifier = IntentClassifier({})
            >>> keywords = classifier.extract_keywords(
            ...     "How do I implement OAuth2 authentication in my React app?"
            ... )
            >>> keywords
            ['implement', 'oauth2', 'authentication', 'react', 'app']
        """
        # Convert to lowercase and split into words
        words = re.findall(r'\b\w+\b', question.lower())

        # Remove stop words and keep meaningful terms (length > 2)
        keywords = [
            word for word in words
            if word not in self.STOP_WORDS and len(word) > 2
        ]

        logger.debug(f"Extracted {len(keywords)} keywords from question: {keywords}")
        return keywords

    def calculate_keyword_score(
        self,
        keywords: List[str],
        flow_keywords: List[str]
    ) -> float:
        """
        Calculates keyword overlap score between question and flow.

        Uses fuzzy matching to handle variations (e.g., "auth" matches "authentication").

        Args:
            keywords: Keywords extracted from question
            flow_keywords: Intent keywords defined for the flow

        Returns:
            Score from 0.0 to 1.0 representing keyword match strength

        Example:
            >>> score = classifier.calculate_keyword_score(
            ...     ['implement', 'oauth2', 'authentication'],
            ...     ['auth', 'authentication', 'security', 'login']
            ... )
            >>> score
            0.67  # 2/3 keywords matched
        """
        if not keywords or not flow_keywords:
            return 0.0

        # Count matches using fuzzy substring matching
        matches = 0
        for kw in keywords:
            # Check if keyword matches any flow keyword (or vice versa for substring matching)
            if any(fk in kw or kw in fk for fk in flow_keywords):
                matches += 1

        # Score = matches / max(question keywords, flow keywords)
        max_possible = max(len(keywords), len(flow_keywords))
        score = matches / max_possible if max_possible > 0 else 0.0

        return score

    async def get_session_context(self, session_id: Optional[str]) -> Dict[str, Any]:
        """
        Retrieves recent session history from persistence layer.

        This enables conversation continuity by understanding what flows
        were recently used and what topics were recently discussed.

        Args:
            session_id: The session identifier

        Returns:
            Dictionary containing session context

        Example:
            >>> context = await classifier.get_session_context("mcp-session-123")
            >>> context
            {
                'last_flow': 'technical-analysis',
                'recent_keywords': ['oauth2', 'react', 'authentication']
            }
        """
        if not session_id or not self.persistence:
            return {}

        try:
            # Retrieve recent session history
            history = await self.persistence.get_session_history(session_id, limit=3)

            if not history:
                return {}

            # Extract last flow used
            last_flow = None
            recent_keywords = []

            for item in history:
                # Extract flow information
                metadata = item.get('_mcp_metadata', {})
                if not last_flow and 'flow_key' in metadata:
                    last_flow = metadata['flow_key']

                # Extract keywords from previous questions
                question = metadata.get('query', '')
                if question:
                    keywords = self.extract_keywords(question)
                    recent_keywords.extend(keywords)

            # Deduplicate keywords while preserving order
            seen = set()
            unique_keywords = []
            for kw in recent_keywords:
                if kw not in seen:
                    seen.add(kw)
                    unique_keywords.append(kw)

            return {
                'last_flow': last_flow,
                'recent_keywords': unique_keywords[:10]  # Limit to most recent 10
            }

        except Exception as e:
            logger.warning(f"Failed to retrieve session context: {str(e)}")
            return {}

    def calculate_context_boost(
        self,
        flow_key: str,
        session_context: Dict[str, Any],
        current_keywords: List[str]
    ) -> float:
        """
        Calculates a boost score based on session context.

        This rewards conversation continuity by boosting flows that align
        with recent interactions.

        Args:
            flow_key: The flow being scored
            session_context: Session context from get_session_context()
            current_keywords: Keywords from current question

        Returns:
            Boost value to add to base score (0.0 to 0.35)

        Example:
            >>> boost = classifier.calculate_context_boost(
            ...     'technical-analysis',
            ...     {'last_flow': 'technical-analysis', 'recent_keywords': ['oauth2']},
            ...     ['token', 'refresh']
            ... )
            >>> boost
            0.30  # 0.25 for same flow + 0.05 for keyword overlap
        """
        boost = 0.0

        # Strong boost for same flow as last query (conversation continuity)
        if session_context.get('last_flow') == flow_key:
            boost += 0.25
            logger.debug(f"Applied continuity boost (+0.25) for flow {flow_key}")

        # Moderate boost for keyword overlap with recent context
        recent_keywords = session_context.get('recent_keywords', [])
        if recent_keywords and current_keywords:
            overlap = len(set(current_keywords) & set(recent_keywords))
            if overlap > 0:
                keyword_boost = min(overlap * 0.05, 0.10)  # Max 0.10 boost
                boost += keyword_boost
                logger.debug(f"Applied keyword context boost (+{keyword_boost:.2f}) for {overlap} overlapping keywords")

        return boost

    async def classify_with_confidence(
        self,
        question: str,
        session_id: Optional[str] = None,
        domain_context: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classifies intent with comprehensive confidence scoring.

        This is the primary classification function that coordinates keyword
        extraction, multi-flow scoring, confidence calculation, and observability.

        Args:
            question: The user's question text
            session_id: Optional session identifier for context
            domain_context: Optional domain-specific context
            trace_id: Optional trace ID for observability linkage

        Returns:
            Classification result dictionary

        Example:
            >>> result = await classifier.classify_with_confidence(
            ...     "How do I implement OAuth2 in React?",
            ...     session_id="mcp-session-123"
            ... )
            >>> result
            {
                'selected_flow': 'technical-analysis',
                'confidence': 0.85,
                'all_scores': {'technical-analysis': 0.85, 'creative-orientation': 0.11, ...},
                'reasoning': 'Strong keyword match (4 keywords)',
                'threshold_met': 'high',
                'keywords_extracted': ['implement', 'oauth2', 'react']
            }
        """
        self._classification_stats['total'] += 1

        try:
            # 1. Extract keywords from question
            keywords = self.extract_keywords(question)

            # 2. Get session context if available
            session_context = await self.get_session_context(session_id) if session_id else {}

            # 3. Score each flow
            raw_scores = {}
            for flow_key, flow_config in self.flow_registry.items():
                # Get intent keywords for this flow
                flow_keywords = flow_config.get('intent_keywords', [])

                # Base score from keyword matching
                base_score = self.calculate_keyword_score(keywords, flow_keywords)

                # Context boost for conversation continuity
                context_boost = self.calculate_context_boost(
                    flow_key,
                    session_context,
                    keywords
                )

                # Domain boost if domain context provided
                domain_boost = 0.0
                if domain_context and domain_context.get('specialized_keywords'):
                    domain_keywords = domain_context['specialized_keywords']
                    domain_overlap = len(set(keywords) & set(domain_keywords))
                    domain_boost = min(domain_overlap * 0.05, 0.10)

                # Combined score (capped at 1.0)
                total_score = min(base_score + context_boost + domain_boost, 1.0)
                raw_scores[flow_key] = total_score

                logger.debug(
                    f"Flow '{flow_key}': base={base_score:.2f}, "
                    f"context={context_boost:.2f}, domain={domain_boost:.2f}, "
                    f"total={total_score:.2f}"
                )

            # 4. Normalize to probabilities (confidences)
            total_score_sum = sum(raw_scores.values())
            if total_score_sum > 0:
                confidences = {k: v / total_score_sum for k, v in raw_scores.items()}
            else:
                # Uniform distribution if no matches
                num_flows = len(raw_scores)
                confidences = {k: 1.0 / num_flows for k in raw_scores.keys()}

            # 5. Select best flow
            if confidences:
                best_flow, best_confidence = max(confidences.items(), key=lambda x: x[1])
            else:
                best_flow = self.default_flow
                best_confidence = 1.0

            # 6. Determine confidence threshold and reasoning
            threshold, reasoning = self._determine_threshold_and_reasoning(
                best_flow,
                best_confidence,
                keywords,
                session_context
            )

            # Update stats
            if threshold == 'high':
                self._classification_stats['high_confidence'] += 1
            elif threshold == 'medium':
                self._classification_stats['medium_confidence'] += 1
            else:
                self._classification_stats['low_confidence'] += 1

            # 7. Construct result
            result = {
                'selected_flow': best_flow,
                'confidence': best_confidence,
                'all_scores': confidences,
                'reasoning': reasoning,
                'threshold_met': threshold,
                'keywords_extracted': keywords,
                'session_context_used': bool(session_context)
            }

            # 8. Log to observability if available
            if self.observability and trace_id:
                await self._log_classification(
                    trace_id,
                    question,
                    result,
                    session_id,
                    session_context
                )

            logger.info(
                f"✅ Classified intent: {best_flow} "
                f"(confidence: {best_confidence:.0%}, threshold: {threshold})"
            )

            return result

        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            # Return safe default
            return {
                'selected_flow': self.default_flow,
                'confidence': 0.5,
                'all_scores': {},
                'reasoning': f"Classification error, using default flow: {str(e)}",
                'threshold_met': 'low',
                'keywords_extracted': [],
                'error': str(e)
            }

    def _determine_threshold_and_reasoning(
        self,
        flow_key: str,
        confidence: float,
        keywords: List[str],
        session_context: Dict[str, Any]
    ) -> Tuple[str, str]:
        """
        Determines confidence threshold and generates human-readable reasoning.

        Args:
            flow_key: Selected flow
            confidence: Confidence score
            keywords: Extracted keywords
            session_context: Session context data

        Returns:
            Tuple of (threshold_level, reasoning_string)
        """
        # Get flow config for keyword matching count
        flow_config = self.flow_registry.get(flow_key, {})
        flow_keywords = flow_config.get('intent_keywords', [])

        # Count actual keyword matches
        matched_keywords = [
            kw for kw in keywords
            if any(fk in kw or kw in fk for fk in flow_keywords)
        ]

        # Determine threshold
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            threshold = 'high'
            reasoning = f"Strong keyword match ({len(matched_keywords)} keywords)"
        elif confidence >= self.MEDIUM_CONFIDENCE_THRESHOLD:
            threshold = 'medium'
            reasoning = f"Moderate confidence based on {len(keywords)} keywords"
        else:
            threshold = 'low'
            reasoning = "Low confidence - using default flow"

        # Add session continuity to reasoning if applicable
        if session_context.get('last_flow') == flow_key:
            reasoning += " + conversation continuity"

        return threshold, reasoning

    async def _log_classification(
        self,
        trace_id: str,
        question: str,
        classification: Dict[str, Any],
        session_id: Optional[str],
        session_context: Dict[str, Any]
    ) -> None:
        """
        Logs classification decision to observability system.

        This creates a learning record that enables future pattern analysis
        and classification refinement.

        Args:
            trace_id: Trace ID to attach observation to
            question: The user's question
            classification: Classification result
            session_id: Session identifier
            session_context: Session context data
        """
        try:
            await self.observability.add_observation(
                trace_id=trace_id,
                name="Intent Classification",
                input_data={
                    "question": question,
                    "session_id": session_id,
                    "session_context": session_context
                },
                output_data={
                    "selected_flow": classification['selected_flow'],
                    "confidence": classification['confidence'],
                    "threshold": classification['threshold_met']
                },
                metadata={
                    "all_scores": classification['all_scores'],
                    "reasoning": classification['reasoning'],
                    "keywords_extracted": classification['keywords_extracted'],
                    "timestamp": datetime.utcnow().isoformat()
                },
                observation_type="EVENT"
            )

            logger.debug(f"Logged classification to trace {trace_id}")

        except Exception as e:
            logger.warning(f"Failed to log classification: {str(e)}")

    def get_classification_stats(self) -> Dict[str, Any]:
        """
        Returns classification statistics.

        These metrics reveal the system's routing patterns and confidence
        distribution, helping identify areas for improvement.

        Returns:
            Dictionary with classification statistics

        Example:
            >>> stats = classifier.get_classification_stats()
            >>> print(f"High confidence rate: {stats['high_confidence_rate']:.1%}")
        """
        total = self._classification_stats['total']
        if total == 0:
            return {
                'total_classifications': 0,
                'high_confidence': 0,
                'medium_confidence': 0,
                'low_confidence': 0,
                'high_confidence_rate': 0.0,
                'medium_confidence_rate': 0.0,
                'low_confidence_rate': 0.0
            }

        return {
            'total_classifications': total,
            'high_confidence': self._classification_stats['high_confidence'],
            'medium_confidence': self._classification_stats['medium_confidence'],
            'low_confidence': self._classification_stats['low_confidence'],
            'high_confidence_rate': self._classification_stats['high_confidence'] / total,
            'medium_confidence_rate': self._classification_stats['medium_confidence'] / total,
            'low_confidence_rate': self._classification_stats['low_confidence'] / total
        }

    def reset_stats(self) -> None:
        """Resets classification statistics counters."""
        self._classification_stats = {
            'total': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0
        }
        logger.info("📊 Classification statistics reset")


# Singleton instance for use across the application
_intent_classifier = None


def get_intent_classifier(
    flow_registry: Optional[Dict[str, Dict]] = None,
    persistence_manager=None,
    observability_manager=None,
    default_flow: str = "creative-orientation"
) -> IntentClassifier:
    """
    Returns the singleton intent classifier instance.

    This ensures consistent statistics and configuration across all
    parts of the application.

    Args:
        flow_registry: Flow registry dictionary
        persistence_manager: Persistence manager instance
        observability_manager: Observability manager instance
        default_flow: Default flow for low-confidence classifications

    Returns:
        The global IntentClassifier instance
    """
    global _intent_classifier

    if _intent_classifier is None and flow_registry is not None:
        _intent_classifier = IntentClassifier(
            flow_registry=flow_registry,
            persistence_manager=persistence_manager,
            observability_manager=observability_manager,
            default_flow=default_flow
        )
        logger.info("✨ Intent classifier initialized - ready for natural expertise discovery!")

    return _intent_classifier
