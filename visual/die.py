"""
Design Intelligence Engine (DIE) - The "Figma Brain" of Aura
Generates design systems based on intent and tone
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class DesignSystem:
    colors: Dict[str, str]
    typography: Dict[str, str]
    spacing: Dict[str, str]
    animations: Dict[str, str]
    tone: str


class DesignIntelligenceEngine:
    """Central registry for Aura colors, typography, and layout rules"""

    def __init__(self):
        self.palettes = {
            'modern': {
                'primary': '#007acc',
                'bg': '#ffffff',
                'text': '#333333',
                'accent': '#f0f0f0',
                'safe_contrast': True
            },
            'premium': {
                'primary': '#000000',
                'bg': '#ffffff',
                'text': '#1a1a1a',
                'accent': '#d4af37',  # Gold
                'safe_contrast': True
            },
            'ai': {
                'primary': '#7c3aed',  # Violet
                'bg': '#0a0a0a',
                'text': '#f3f4f6',
                'accent': '#2dd4bf',  # Teal
                'safe_contrast': True
            }
        }

    def generate_system(self, tone: str, industry: str = None) -> DesignSystem:
        """Create a full design system token set"""

        # Pick palette
        palette_key = industry if industry in self.palettes else tone
        palette = self.palettes.get(palette_key, self.palettes['modern'])

        return DesignSystem(
            colors=palette,
            typography={
                'h1': 'clamp(2.5rem, 5vw, 4rem)',
                'body': '1.125rem',
                'font_family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
            },
            spacing={
                'section': '100px 0',
                'gap': '24px',
                'max_width': '1200px'
            },
            animations={
                'fade_in': 'fadeIn 0.6s ease-out forwards',
                'hover_lift': 'translateY(-5px)'
            },
            tone=tone
        )
