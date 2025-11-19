"""
Agentic Flywheel Domain Manager Module

This module enables users to manage domain profiles persistently, supporting
multi-domain environments with seamless context switching. Through YAML-based
profile management, users can create compounding domain knowledge that makes
AI interactions increasingly relevant over time.

Based on domain-specialization.spec.md (v1.0) - RISE Framework
"""

import logging
import os
import yaml
from typing import Dict, Optional, List, Any
from pathlib import Path
from datetime import datetime

from .context_builder import DomainProfile, ContextBuilder

logger = logging.getLogger(__name__)


class DomainManager:
    """
    Manages domain profiles for multi-domain AI interactions.

    This class transforms domain knowledge into persistent, reusable infrastructure
    that enables deeply relevant responses across different project contexts.
    """

    def __init__(self, profiles_dir: Optional[str] = None):
        """
        Initialize the domain manager.

        Args:
            profiles_dir: Directory containing YAML domain profiles
                         Defaults to ~/.agentic_flywheel/profiles/
        """
        if profiles_dir is None:
            home = Path.home()
            profiles_dir = home / ".agentic_flywheel" / "profiles"

        self.profiles_dir = Path(profiles_dir)
        self.profiles_dir.mkdir(parents=True, exist_ok=True)

        self._loaded_profiles: Dict[str, DomainProfile] = {}
        self._active_profile_id: Optional[str] = None

        logger.info(f"📁 Domain manager initialized with profiles directory: {self.profiles_dir}")

    def load_profile(self, profile_path: str) -> DomainProfile:
        """
        Loads a domain profile from a YAML file.

        This enables users to define their domain context once and reuse it
        across all interactions, creating compounding efficiency.

        Args:
            profile_path: Path to YAML profile file (absolute or relative to profiles_dir)

        Returns:
            Loaded DomainProfile instance

        Raises:
            FileNotFoundError: If profile file doesn't exist
            yaml.YAMLError: If profile file is invalid

        Example:
            >>> manager = DomainManager()
            >>> profile = manager.load_profile("language-learning-prod.yaml")
            >>> print(f"Loaded profile: {profile.name}")
        """
        # Handle both absolute and relative paths
        path = Path(profile_path)
        if not path.is_absolute():
            path = self.profiles_dir / path

        if not path.exists():
            raise FileNotFoundError(f"Profile not found: {path}")

        logger.info(f"📖 Loading domain profile from: {path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Extract domain_profile section
            if 'domain_profile' not in data:
                raise ValueError("YAML file must contain 'domain_profile' root key")

            profile_data = data['domain_profile']

            # Create DomainProfile instance
            profile = DomainProfile(
                id=profile_data.get('id', path.stem),
                name=profile_data['name'],
                description=profile_data['description'],
                version=profile_data.get('version', '1.0'),
                technical_context=profile_data.get('technical_context'),
                cultural_context=profile_data.get('cultural_context'),
                strategic_context=profile_data.get('strategic_context'),
                specialized_keywords=profile_data.get('specialized_keywords', []),
                privacy_level=profile_data.get('privacy_level', 'internal'),
                owners=profile_data.get('owners', []),
                tags=profile_data.get('tags', []),
                created_at=profile_data.get('created_at'),
                updated_at=profile_data.get('updated_at')
            )

            # Cache loaded profile
            self._loaded_profiles[profile.id] = profile

            logger.info(f"✅ Loaded profile: {profile.name} (ID: {profile.id})")
            return profile

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML profile: {str(e)}")
            raise
        except KeyError as e:
            logger.error(f"Missing required field in profile: {str(e)}")
            raise ValueError(f"Invalid profile format: missing {str(e)}")

    def save_profile(self, profile: DomainProfile, filename: Optional[str] = None) -> str:
        """
        Saves a domain profile to a YAML file.

        This enables users to programmatically create and update domain profiles,
        building domain knowledge as their projects evolve.

        Args:
            profile: DomainProfile to save
            filename: Optional custom filename, defaults to "{profile.id}.yaml"

        Returns:
            Path to saved file

        Example:
            >>> profile = DomainProfile(
            ...     id="my-project",
            ...     name="My Project",
            ...     description="..."
            ... )
            >>> path = manager.save_profile(profile)
            >>> print(f"Saved to: {path}")
        """
        if filename is None:
            filename = f"{profile.id}.yaml"

        path = self.profiles_dir / filename

        # Update timestamp
        profile.updated_at = datetime.utcnow().isoformat()
        if profile.created_at is None:
            profile.created_at = profile.updated_at

        # Convert to YAML-friendly dict
        profile_data = {
            'domain_profile': {
                'id': profile.id,
                'name': profile.name,
                'description': profile.description,
                'version': profile.version,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at,
            }
        }

        # Add optional sections only if they have content
        if profile.technical_context:
            profile_data['domain_profile']['technical_context'] = profile.technical_context

        if profile.cultural_context:
            profile_data['domain_profile']['cultural_context'] = profile.cultural_context

        if profile.strategic_context:
            profile_data['domain_profile']['strategic_context'] = profile.strategic_context

        if profile.specialized_keywords:
            profile_data['domain_profile']['specialized_keywords'] = profile.specialized_keywords

        # Add metadata
        profile_data['domain_profile']['privacy_level'] = profile.privacy_level
        if profile.owners:
            profile_data['domain_profile']['owners'] = profile.owners
        if profile.tags:
            profile_data['domain_profile']['tags'] = profile.tags

        # Save to file
        try:
            with open(path, 'w', encoding='utf-8') as f:
                yaml.dump(
                    profile_data,
                    f,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False
                )

            logger.info(f"💾 Saved profile to: {path}")
            return str(path)

        except Exception as e:
            logger.error(f"Failed to save profile: {str(e)}")
            raise

    def list_profiles(self) -> List[Dict[str, str]]:
        """
        Lists all available domain profiles.

        Returns:
            List of profile metadata dictionaries

        Example:
            >>> profiles = manager.list_profiles()
            >>> for p in profiles:
            ...     print(f"{p['name']} - {p['description']}")
        """
        profiles = []

        for path in self.profiles_dir.glob("*.yaml"):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)

                if 'domain_profile' in data:
                    pd = data['domain_profile']
                    profiles.append({
                        'id': pd.get('id', path.stem),
                        'name': pd.get('name', path.stem),
                        'description': pd.get('description', ''),
                        'path': str(path),
                        'tags': pd.get('tags', [])
                    })
            except Exception as e:
                logger.warning(f"Failed to read profile {path}: {str(e)}")
                continue

        return profiles

    def get_profile(self, profile_id: str) -> Optional[DomainProfile]:
        """
        Retrieves a cached profile by ID.

        Args:
            profile_id: Profile identifier

        Returns:
            DomainProfile if found, None otherwise
        """
        return self._loaded_profiles.get(profile_id)

    def set_active_profile(self, profile_id: str) -> bool:
        """
        Sets the active domain profile.

        This enables seamless context switching between different domains
        within a multi-project environment.

        Args:
            profile_id: Profile identifier to activate

        Returns:
            True if successful, False if profile not loaded

        Example:
            >>> manager.load_profile("production-app.yaml")
            >>> manager.set_active_profile("production-app")
            >>> # All subsequent queries will use production-app context
        """
        if profile_id not in self._loaded_profiles:
            logger.warning(f"Cannot activate profile '{profile_id}' - not loaded")
            return False

        self._active_profile_id = profile_id
        profile = self._loaded_profiles[profile_id]
        logger.info(f"✨ Activated domain profile: {profile.name}")
        return True

    def get_active_profile(self) -> Optional[DomainProfile]:
        """
        Returns the currently active domain profile.

        Returns:
            Active DomainProfile, or None if no profile is active
        """
        if self._active_profile_id is None:
            return None

        return self._loaded_profiles.get(self._active_profile_id)

    def enrich_query(
        self,
        question: str,
        profile_id: Optional[str] = None,
        context_type: Optional[str] = None
    ) -> str:
        """
        Enriches a query with domain context.

        This is the main entry point for transforming generic questions into
        domain-specific, context-rich queries that yield highly relevant responses.

        Args:
            question: The user's question
            profile_id: Optional specific profile to use (defaults to active)
            context_type: Optional context type ('technical', 'cultural', 'strategic', 'general')

        Returns:
            Context-enriched query string

        Example:
            >>> enriched = manager.enrich_query("How do I implement caching?")
            >>> # Returns query with full technical context about their stack
        """
        # Determine which profile to use
        if profile_id is not None:
            profile = self.get_profile(profile_id)
        else:
            profile = self.get_active_profile()

        if profile is None:
            logger.debug("No domain profile available, returning original question")
            return question

        # Build context-enriched query
        enriched_query = ContextBuilder.build_context(
            profile,
            question,
            context_type
        )

        logger.debug(f"Enriched query with {profile.name} context (type: {context_type or 'auto'})")
        return enriched_query

    def create_profile_template(
        self,
        name: str,
        description: str,
        template_type: str = "saas"
    ) -> DomainProfile:
        """
        Creates a domain profile from a template.

        This accelerates profile creation by providing sensible defaults
        for common domain types.

        Args:
            name: Profile name
            description: Profile description
            template_type: Template to use ('saas', 'ecommerce', 'education', 'internal-tool')

        Returns:
            DomainProfile instance with template defaults

        Example:
            >>> profile = manager.create_profile_template(
            ...     "My SaaS App",
            ...     "Customer onboarding platform",
            ...     template_type="saas"
            ... )
            >>> # Edit profile as needed
            >>> manager.save_profile(profile)
        """
        # Generate profile ID
        profile_id = name.lower().replace(' ', '-').replace('_', '-')

        # Base profile
        profile = DomainProfile(
            id=profile_id,
            name=name,
            description=description
        )

        # Apply template defaults
        if template_type == "saas":
            profile.technical_context = {
                'stack': {
                    'frontend': ['React', 'Next.js'],
                    'backend': ['Node.js', 'Express'],
                    'database': ['PostgreSQL'],
                    'hosting': ['Vercel', 'AWS']
                },
                'constraints': [
                    'Cost-conscious architecture',
                    'Scalability for growth',
                    'Developer experience priority'
                ]
            }
            profile.strategic_context = {
                'business_stage': 'Startup',
                'current_priorities': [
                    'User acquisition',
                    'Product-market fit',
                    'Feature velocity'
                ]
            }
            profile.tags = ['saas', 'b2b', 'startup']

        elif template_type == "ecommerce":
            profile.technical_context = {
                'stack': {
                    'frontend': ['React', 'Next.js', 'TailwindCSS'],
                    'backend': ['Node.js'],
                    'database': ['PostgreSQL', 'Redis'],
                    'payments': ['Stripe'],
                    'hosting': ['Vercel']
                },
                'constraints': [
                    'High performance (< 2s load time)',
                    'PCI compliance for payments',
                    'Mobile-first design'
                ]
            }
            profile.strategic_context = {
                'current_priorities': [
                    'Conversion optimization',
                    'Customer retention',
                    'Checkout experience'
                ]
            }
            profile.tags = ['ecommerce', 'b2c', 'retail']

        elif template_type == "education":
            profile.cultural_context = {
                'domain_type': 'Education Technology',
                'cultural_sensitivity': [
                    'Age-appropriate content',
                    'Inclusive language',
                    'Accessibility standards (WCAG 2.1)'
                ]
            }
            profile.tags = ['education', 'edtech', 'learning']

        elif template_type == "internal-tool":
            profile.strategic_context = {
                'business_stage': 'Internal product',
                'current_priorities': [
                    'Developer productivity',
                    'Ease of maintenance',
                    'Integration with existing systems'
                ]
            }
            profile.tags = ['internal', 'tooling']

        logger.info(f"✨ Created {template_type} profile template: {name}")
        return profile

    def get_stats(self) -> Dict[str, Any]:
        """
        Returns domain manager statistics.

        Returns:
            Statistics dictionary
        """
        return {
            'profiles_loaded': len(self._loaded_profiles),
            'active_profile': self._active_profile_id,
            'profiles_dir': str(self.profiles_dir),
            'available_profiles': len(list(self.profiles_dir.glob("*.yaml")))
        }


# Singleton instance for use across the application
_domain_manager = None


def get_domain_manager(profiles_dir: Optional[str] = None) -> DomainManager:
    """
    Returns the singleton domain manager instance.

    This ensures consistent profile management across all parts of the application.

    Args:
        profiles_dir: Optional profiles directory path

    Returns:
        The global DomainManager instance
    """
    global _domain_manager

    if _domain_manager is None:
        _domain_manager = DomainManager(profiles_dir=profiles_dir)
        logger.info("✨ Domain manager initialized - ready for multi-domain intelligence!")

    return _domain_manager
