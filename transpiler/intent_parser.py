"""
Intent Parser - Extracts semantic meaning and tone from natural language strings
Key to Aura 4.0's "Intent over Layout" philosophy
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class IntentResult:
    intent_type: str  # landing, dashboard, blog, app
    industry: Optional[str] = None
    tone: str = "modern"  # default
    audience: str = "general"
    features: List[str] = None


class IntentParser:
    """Parses raw strings to understand what the user is trying to build"""

    def __init__(self):
        self.industry_keywords = {
            'ai': ['ai', 'artificial intelligence', 'machine learning', 'ml'],
            'finance': ['finance', 'fintech', 'bank', 'money', 'trading'],
            'saas': ['saas', 'software', 'productivity', 'tool'],
            'health': ['health', 'medical', 'fitness', 'wellness'],
            'education': ['education', 'learning', 'school', 'academy'],
            'barber': ['barber', 'salon', 'haircut', 'grooming']
        }

        self.type_keywords = {
            'landing': ['landing page', 'homepage', 'teaser', 'marketing'],
            'dashboard': ['dashboard', 'analytics', 'admin', 'portal'],
            'app': ['app', 'application', 'mobile app', 'platform']
        }

        self.blueprints = {
            'landing': ['hero', 'features', 'pricing', 'cta', 'footer'],
            'dashboard': ['header', 'stats_overview', 'main_chart', 'recent_activity'],
            'app': ['auth_shell', 'onboarding_flow', 'main_view'],
            'booking': ['hero', 'service_list', 'booking_calendar', 'contact']
        }

    def parse(self, text: str) -> IntentResult:
        """Extract IntentResult from text"""
        text_lower = text.lower()

        # Determine Type
        intent_type = "landing"  # default
        for t, keywords in self.type_keywords.items():
            if any(k in text_lower for k in keywords):
                intent_type = t
                break

        # Special case for 'booking' intent
        if 'booking' in text_lower or 'reservation' in text_lower:
            intent_type = 'booking'

        # Determine Industry
        industry = None
        for ind, keywords in self.industry_keywords.items():
            if any(k in text_lower for k in keywords):
                industry = ind
                break

        # Determine Tone
        tone = "modern"
        if "premium" in text_lower or "luxury" in text_lower:
            tone = "premium"
        elif "playful" in text_lower or "fun" in text_lower:
            tone = "playful"
        elif "minimal" in text_lower or "clean" in text_lower:
            tone = "minimal"

        # Get suggested features/sections
        features = self.blueprints.get(intent_type, self.blueprints['landing'])

        return IntentResult(
            intent_type=intent_type,
            industry=industry,
            tone=tone,
            features=features
        )
