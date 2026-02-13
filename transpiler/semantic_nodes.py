"""
Semantic AST Nodes - High-level intent-based UI components
"""

from dataclasses import dataclass
from typing import List, Optional
from transpiler.ast_nodes import ASTNode
from transpiler.ui_nodes import UINode


@dataclass
class SemanticNode(UINode):
    """Base for intent-first nodes"""
    pass


@dataclass
class HeroNode(SemanticNode):
    title: str
    subtitle: Optional[str] = None
    cta_text: Optional[str] = None
    image_url: Optional[str] = None


@dataclass
class FeatureNode(SemanticNode):
    title: str
    description: Optional[str] = None
    icon: Optional[str] = None


@dataclass
class PricingNode(SemanticNode):
    plan_name: str
    price: str
    features: List[str]
    is_premium: bool = False


@dataclass
class CtaNode(SemanticNode):
    title: str
    button_text: str


@dataclass
class BookingNode(SemanticNode):
    service_name: Optional[str] = None
    price_prefix: Optional[str] = None


@dataclass
class ContactNode(SemanticNode):
    email: Optional[str] = None
    show_form: bool = True


@dataclass
class IntentPageNode(SemanticNode):
    """
    A full product generated from a single intent string.
    If sections is empty, the VRE will auto-generate them based on the intent.
    """
    intent_text: str
    sections: List[UINode]
