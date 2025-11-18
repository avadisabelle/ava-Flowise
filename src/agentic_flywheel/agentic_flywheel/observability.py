"""
Agentic Flywheel Observability Module

This module enables users to create a comprehensive creative archaeology of
their AI interactions, transforming ephemeral conversations into observable,
analyzable artifacts through Langfuse tracing integration.

Based on langfuse-tracing.spec.md (v1.0) - RISE Framework
"""

import logging
import time
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class ObservabilityManager:
    """
    Manifests visible creative progression through comprehensive AI interaction tracing.

    This class transforms invisible conversations into observable artifacts, creating
    a learning system that reveals quality patterns and enables continuous improvement
    through observation rather than guesswork.
    """

    def __init__(self, enable_tracing: bool = True, project_name: str = "agentic-flywheel"):
        """
        Initialize the observability manager.

        Args:
            enable_tracing: Whether to enable Langfuse tracing (can disable for testing)
            project_name: Name of the project in Langfuse
        """
        self.enable_tracing = enable_tracing
        self.project_name = project_name
        self._active_traces = {}  # Track active traces for finalization
        self._trace_stats = {
            'created': 0,
            'observations_added': 0,
            'errors': 0,
            'graceful_failures': 0
        }

    def _generate_trace_id(self) -> str:
        """Generates a unique trace identifier."""
        return f"trace-{uuid.uuid4().hex[:16]}"

    def _generate_observation_id(self) -> str:
        """Generates a unique observation identifier."""
        return f"obs-{uuid.uuid4().hex[:12]}"

    def generate_trace_name(self, question: str, intent: Optional[str] = None) -> str:
        """
        Generates a descriptive, searchable trace name from the question.

        This creates human-readable trace names that enable users to quickly
        find and explore specific conversations in Langfuse.

        Args:
            question: The user's question text
            intent: Optional detected intent to include in the name

        Returns:
            A descriptive trace name

        Example:
            >>> om = ObservabilityManager()
            >>> name = om.generate_trace_name(
            ...     "How does React Server Components differ from traditional React?",
            ...     "technical-analysis"
            ... )
            >>> name
            'Technical Analysis Query - How Does React Server Components'
        """
        # Extract key terms from question (first 5-7 words or key phrases)
        words = question.strip().split()
        key_phrase = " ".join(words[:7]) if len(words) > 7 else question

        # Capitalize and clean
        key_phrase = key_phrase.strip("?!.,").title()

        # Truncate if still too long
        if len(key_phrase) > 60:
            key_phrase = key_phrase[:57] + "..."

        # Include intent if available
        if intent:
            intent_label = intent.replace("-", " ").title()
            return f"{intent_label} Query - {key_phrase}"

        return f"AI Query - {key_phrase}"

    async def create_trace(
        self,
        question: str,
        session_id: str,
        intent: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Creates a new Langfuse trace for an AI query.

        This manifests the foundation of an observable artifact, marking the
        beginning of a creative journey that will be fully documented.

        Args:
            question: The user's question text
            session_id: Unique session identifier for threading
            intent: Optional detected intent
            metadata: Additional metadata to include in the trace

        Returns:
            The trace ID if successful, None if tracing is disabled or fails

        Example:
            >>> trace_id = await om.create_trace(
            ...     "How do I implement OAuth?",
            ...     "mcp-session-123",
            ...     intent="technical-analysis"
            ... )
            >>> print(f"Created trace: {trace_id}")
        """
        if not self.enable_tracing:
            logger.debug("Tracing disabled, skipping trace creation")
            return None

        try:
            trace_id = self._generate_trace_id()
            trace_name = self.generate_trace_name(question, intent)

            # Prepare trace metadata
            trace_metadata = {
                "session_id": session_id,
                "query": question,
                "intent": intent,
                "timestamp": datetime.utcnow().isoformat(),
                "environment": "production",
                **(metadata or {})
            }

            # TODO: Call coaiapy-mcp tool for trace creation
            # In production, this would call:
            # await mcp__coaiapy__coaia_fuse_trace_create({
            #     "trace_id": trace_id,
            #     "name": trace_name,
            #     "session_id": session_id,
            #     "metadata": trace_metadata
            # })

            # For now, store in memory for tracking
            self._active_traces[trace_id] = {
                "name": trace_name,
                "session_id": session_id,
                "created_at": datetime.utcnow(),
                "observations": [],
                "metadata": trace_metadata
            }

            self._trace_stats['created'] += 1
            logger.info(f"✨ Created trace: {trace_name} (ID: {trace_id})")

            return trace_id

        except Exception as e:
            self._trace_stats['errors'] += 1
            self._trace_stats['graceful_failures'] += 1
            logger.warning(f"Langfuse tracing failed during trace creation: {str(e)}")
            # Gracefully fail - return None but don't break the query
            return None

    async def add_observation(
        self,
        trace_id: Optional[str],
        name: str,
        input_data: Any,
        output_data: Optional[Any] = None,
        metadata: Optional[Dict[str, Any]] = None,
        observation_type: str = "EVENT",
        start_time: Optional[float] = None
    ) -> Optional[str]:
        """
        Adds an observation to a trace.

        This captures significant steps in the query processing, building a
        complete picture of how the system progresses from question to answer.

        Args:
            trace_id: The trace to add this observation to
            name: Descriptive name for this observation (e.g., "Intent Classification")
            input_data: The input to this processing step
            output_data: The output from this processing step
            metadata: Additional metadata for this observation
            observation_type: Type of observation (EVENT, SPAN, GENERATION)
            start_time: Optional start timestamp (for SPAN observations)

        Returns:
            The observation ID if successful, None otherwise

        Example:
            >>> obs_id = await om.add_observation(
            ...     trace_id,
            ...     "Intent Classification",
            ...     input_data={"question": "..."},
            ...     output_data={"intent": "technical", "confidence": 0.92},
            ...     metadata={"model": "keyword-matcher"}
            ... )
        """
        if not self.enable_tracing or not trace_id:
            return None

        try:
            obs_id = self._generate_observation_id()

            observation = {
                "id": obs_id,
                "trace_id": trace_id,
                "name": name,
                "type": observation_type,
                "input": input_data,
                "output": output_data,
                "metadata": metadata or {},
                "timestamp": datetime.utcnow().isoformat(),
                "start_time": start_time or time.time()
            }

            # TODO: Call coaiapy-mcp tool for observation creation
            # In production, this would call:
            # await mcp__coaiapy__coaia_fuse_add_observation({
            #     "trace_id": trace_id,
            #     "observation_id": obs_id,
            #     "name": name,
            #     "input": input_data,
            #     "output": output_data,
            #     "metadata": metadata,
            #     "type": observation_type
            # })

            # Store in memory for tracking
            if trace_id in self._active_traces:
                self._active_traces[trace_id]["observations"].append(observation)

            self._trace_stats['observations_added'] += 1
            logger.debug(f"📊 Added observation '{name}' to trace {trace_id}")

            return obs_id

        except Exception as e:
            self._trace_stats['errors'] += 1
            self._trace_stats['graceful_failures'] += 1
            logger.warning(f"Langfuse observation creation failed: {str(e)}")
            # Gracefully fail - return None but don't break the query
            return None

    async def start_observation(
        self,
        trace_id: Optional[str],
        name: str,
        input_data: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Starts a SPAN observation that will be finalized later.

        This is useful for tracing long-running operations like LLM generation,
        where you want to capture both the start and end times.

        Args:
            trace_id: The trace to add this observation to
            name: Descriptive name for this observation
            input_data: The input to this processing step
            metadata: Additional metadata for this observation

        Returns:
            The observation ID to use for finalization

        Example:
            >>> obs_id = await om.start_observation(
            ...     trace_id,
            ...     "Flow Execution: Technical Analysis",
            ...     input_data={"question": "...", "config": {...}}
            ... )
            >>> # ... execute the flow ...
            >>> await om.finalize_observation(obs_id, output_data=response)
        """
        return await self.add_observation(
            trace_id,
            name,
            input_data,
            output_data=None,  # Will be added during finalization
            metadata=metadata,
            observation_type="SPAN",
            start_time=time.time()
        )

    async def finalize_observation(
        self,
        trace_id: Optional[str],
        observation_id: Optional[str],
        output_data: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Finalizes a SPAN observation with its output and end time.

        Args:
            trace_id: The trace containing this observation
            observation_id: The observation to finalize
            output_data: The output from the processing step
            metadata: Additional metadata to merge with existing metadata

        Returns:
            True if successful, False otherwise
        """
        if not self.enable_tracing or not trace_id or not observation_id:
            return False

        try:
            # Calculate execution time
            end_time = time.time()

            # Find and update the observation
            if trace_id in self._active_traces:
                for obs in self._active_traces[trace_id]["observations"]:
                    if obs["id"] == observation_id:
                        obs["output"] = output_data
                        obs["end_time"] = end_time
                        obs["execution_time_ms"] = int((end_time - obs["start_time"]) * 1000)

                        # Merge metadata
                        if metadata:
                            obs["metadata"].update(metadata)

                        logger.debug(f"✅ Finalized observation {observation_id} ({obs['execution_time_ms']}ms)")
                        return True

            # TODO: Call coaiapy-mcp tool to update observation
            # In production, this would update the observation in Langfuse

            return True

        except Exception as e:
            self._trace_stats['errors'] += 1
            logger.warning(f"Observation finalization failed: {str(e)}")
            return False

    @asynccontextmanager
    async def trace_operation(
        self,
        trace_id: Optional[str],
        operation_name: str,
        input_data: Any,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Context manager for tracing an operation with automatic timing.

        This enables clean, automatic observation creation with proper start/end times.

        Example:
            >>> async with om.trace_operation(
            ...     trace_id,
            ...     "LLM Generation",
            ...     input_data={"prompt": "..."}
            ... ) as obs:
            ...     response = await llm.generate(prompt)
            ...     obs.set_output(response)
        """
        obs_id = None
        output_container = {"output": None}

        class ObservationContext:
            def set_output(self, output_data):
                output_container["output"] = output_data

        ctx = ObservationContext()

        try:
            # Start the observation
            obs_id = await self.start_observation(
                trace_id,
                operation_name,
                input_data,
                metadata
            )

            # Yield control to the with block
            yield ctx

        finally:
            # Finalize the observation with output
            if obs_id:
                await self.finalize_observation(
                    trace_id,
                    obs_id,
                    output_container["output"],
                    metadata
                )

    async def update_trace_metadata(
        self,
        trace_id: Optional[str],
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Updates a trace with additional metadata.

        This is useful for adding summary information after all observations
        are complete.

        Args:
            trace_id: The trace to update
            metadata: Metadata to add/update

        Returns:
            True if successful, False otherwise
        """
        if not self.enable_tracing or not trace_id:
            return False

        try:
            if trace_id in self._active_traces:
                self._active_traces[trace_id]["metadata"].update(metadata)

            # TODO: Call coaiapy-mcp tool to update trace metadata
            # In production, this would call:
            # await mcp__coaiapy__coaia_fuse_trace_update({
            #     "trace_id": trace_id,
            #     "metadata": metadata
            # })

            logger.debug(f"📝 Updated trace {trace_id} metadata")
            return True

        except Exception as e:
            self._trace_stats['errors'] += 1
            logger.warning(f"Trace metadata update failed: {str(e)}")
            return False

    async def add_trace_score(
        self,
        trace_id: Optional[str],
        score_name: str,
        score_value: float,
        comment: Optional[str] = None
    ) -> bool:
        """
        Adds a quality score to a trace.

        This enables retrospective evaluation of response value, building
        a dataset for quality pattern analysis.

        Args:
            trace_id: The trace to score
            score_name: Name of the score (e.g., "helpfulness", "accuracy")
            score_value: Numeric score value (typically 0-1 or 1-5)
            comment: Optional comment explaining the score

        Returns:
            True if successful, False otherwise

        Example:
            >>> await om.add_trace_score(
            ...     trace_id,
            ...     "helpfulness",
            ...     4.5,
            ...     comment="Very detailed and accurate response"
            ... )
        """
        if not self.enable_tracing or not trace_id:
            return False

        try:
            # TODO: Call coaiapy-mcp tool for score creation
            # In production, this would call:
            # await mcp__coaiapy__coaia_fuse_scores_add({
            #     "trace_id": trace_id,
            #     "name": score_name,
            #     "value": score_value,
            #     "comment": comment
            # })

            logger.info(f"⭐ Added score '{score_name}={score_value}' to trace {trace_id}")
            return True

        except Exception as e:
            self._trace_stats['errors'] += 1
            logger.warning(f"Score creation failed: {str(e)}")
            return False

    def get_trace_stats(self) -> Dict[str, Any]:
        """
        Returns observability statistics.

        These metrics reveal the value created by the tracing system,
        showing coverage and reliability.

        Returns:
            Dictionary with tracing statistics

        Example:
            >>> stats = om.get_trace_stats()
            >>> print(f"Traces created: {stats['traces_created']}")
            >>> print(f"Graceful failure rate: {stats['graceful_failure_rate']:.1%}")
        """
        total_operations = (
            self._trace_stats['created'] +
            self._trace_stats['observations_added']
        )
        graceful_failure_rate = (
            self._trace_stats['graceful_failures'] / total_operations
            if total_operations > 0 else 0.0
        )

        return {
            'traces_created': self._trace_stats['created'],
            'observations_added': self._trace_stats['observations_added'],
            'total_errors': self._trace_stats['errors'],
            'graceful_failures': self._trace_stats['graceful_failures'],
            'active_traces': len(self._active_traces),
            'graceful_failure_rate': graceful_failure_rate,
            'status': 'healthy' if graceful_failure_rate < 0.05 else 'degraded'
        }

    def get_active_trace(self, trace_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves information about an active trace.

        Args:
            trace_id: The trace identifier

        Returns:
            Trace information dictionary, or None if not found
        """
        return self._active_traces.get(trace_id)

    def reset_stats(self) -> None:
        """Resets tracing statistics counters."""
        self._trace_stats = {
            'created': 0,
            'observations_added': 0,
            'errors': 0,
            'graceful_failures': 0
        }
        logger.info("📊 Observability statistics reset")


# Singleton instance for use across the application
_observability_manager = None


def get_observability_manager(
    enable_tracing: bool = True,
    project_name: str = "agentic-flywheel"
) -> ObservabilityManager:
    """
    Returns the singleton observability manager instance.

    This ensures consistent trace statistics and configuration
    across all parts of the application.

    Args:
        enable_tracing: Whether to enable Langfuse tracing
        project_name: Name of the project in Langfuse

    Returns:
        The global ObservabilityManager instance
    """
    global _observability_manager

    if _observability_manager is None:
        _observability_manager = ObservabilityManager(
            enable_tracing=enable_tracing,
            project_name=project_name
        )
        logger.info("✨ Observability manager initialized - ready to create observable artifacts!")

    return _observability_manager
