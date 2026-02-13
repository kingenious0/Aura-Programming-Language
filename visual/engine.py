"""
Visual Runtime Engine (VRE) - Core of Aura's visual layer
Subscribes to runtime state, builds render tree, triggers updates
"""

from typing import Optional, List, Callable
from visual.render_tree import RenderTree, RenderNode
from transpiler.ui_nodes import (
    ScreenNode, ColumnNode, RowNode, StackNode,
    TextNode, ButtonNode, InputNode, UINode
)
from transpiler.semantic_nodes import (
    HeroNode, FeatureNode, PricingNode, IntentPageNode,
    CtaNode, BookingNode, ContactNode
)
from visual.die import DesignIntelligenceEngine
from transpiler.intent_parser import IntentParser


class VisualRuntimeEngine:
    """
    Visual Runtime Engine

    Responsibilities:
    - Convert UI AST to render tree
    - Subscribe to runtime state changes
    - Trigger re-renders on state updates
    - Maintain render tree (NOT state)
    """

    def __init__(self, runtime):
        self.runtime = runtime
        self.render_tree: Optional[RenderTree] = None
        self.ui_ast: Optional[UINode] = None
        self.on_render_callbacks: List[Callable] = []

        # Phase 4.0 Engines
        self.die = DesignIntelligenceEngine()
        self.intent_parser = IntentParser()
        self.current_system = self.die.generate_system("modern")

    def load_ui(self, ui_ast: UINode):
        """Load UI AST and build initial render tree"""
        self.ui_ast = ui_ast

        # If we have an IntentPageNode, use its intent to generate the design system
        if isinstance(ui_ast, IntentPageNode):
            intent = self.intent_parser.parse(ui_ast.intent_text)
            self.current_system = self.die.generate_system(
                intent.tone, intent.industry)

            # AURA 5.0: AUTO-EXPANSION
            # If the user provided ONLY the intent string without sections,
            # we auto-build the product based on the suggested blueprint.
            if not ui_ast.sections:
                self.expand_product(ui_ast, intent)

        self.render_tree = self.build_render_tree()
        self.subscribe_to_state()
        self.trigger_render()

    def expand_product(self, page_node: IntentPageNode, intent: Any):
        """Build a full product automatically from a blueprint"""
        print(
            f"🪄  Aura 5.0 - Compiling Product: {intent.intent_type} for {intent.industry or 'general'}")

        from transpiler.semantic_nodes import HeroNode, FeatureNode, PricingNode, CtaNode, BookingNode, ContactNode

        # Industry specific copy
        headers = {
            'ai': "The Future of Intelligence",
            'finance': "Secure Your Wealth",
            'health': "Wellness Redefined",
            'education': "Master Your Craft",
            'barber': "Premium Grooming Experience",
            'saas': "Scale Your Business"
        }

        industry_name = intent.industry or "Idea"
        title = headers.get(intent.industry, f"Your {industry_name} Platform")

        sections = []
        for feature_type in intent.features:
            if feature_type == 'hero':
                sections.append(HeroNode(line_number=0, raw_line="", title=title,
                                         subtitle=f"Aura 5.0 is building your {intent.intent_type} from human intent. No code, just results.",
                                         cta_text="Launch Project"))
            elif feature_type == 'features':
                sections.append(FeatureNode(line_number=0, raw_line="",
                                            title="Intent-First Design",
                                            description="Describe it, Aura builds it. No CSS required."))
                sections.append(FeatureNode(line_number=0, raw_line="",
                                            title="DIE Intelligence",
                                            description="The Design Intelligence Engine encodes good taste by default."))
            elif feature_type == 'pricing':
                sections.append(PricingNode(line_number=0, raw_line="",
                                            plan_name="Founder Plan",
                                            price="$0",
                                            features=["Unlimited Sites", "Custom Blueprints", "Aura Engine Access"]))
            elif feature_type == 'cta':
                sections.append(CtaNode(line_number=0, raw_line="",
                                title=f"Ready to launch your {industry_name}?", button_text="Get Started"))
            elif feature_type == 'booking':
                sections.append(BookingNode(line_number=0, raw_line="",
                                service_name=f"{industry_name.capitalize()} Consultation"))
            elif feature_type == 'service_list':
                sections.append(FeatureNode(line_number=0, raw_line="",
                                title="Standard Service", description="Quality guaranteed."))
                sections.append(FeatureNode(line_number=0, raw_line="",
                                title="Premium Service", description="The ultimate experience."))
            elif feature_type == 'contact':
                sections.append(ContactNode(line_number=0, raw_line=""))

        page_node.sections = sections

    def build_render_tree(self) -> RenderTree:
        """Convert UI AST to render tree"""
        if not self.ui_ast:
            return RenderTree()

        root = self._convert_node(self.ui_ast)
        return RenderTree(root)

    def _convert_node(self, ast_node: UINode) -> RenderNode:
        """Convert single AST node to render node"""

        # === PHASE 4.0 SEMANTIC NODES ===
        if isinstance(ast_node, IntentPageNode):
            return RenderNode(
                type='page',
                props={'intent': ast_node.intent_text},
                children=[self._convert_node(child)
                          for child in ast_node.sections]
            )

        elif isinstance(ast_node, HeroNode):
            return RenderNode(
                type='hero',
                props={
                    'title': ast_node.title,
                    'subtitle': ast_node.subtitle,
                    'cta': ast_node.cta_text
                }
            )

        elif isinstance(ast_node, FeatureNode):
            return RenderNode(
                type='feature',
                props={
                    'title': ast_node.title,
                    'description': ast_node.description
                }
            )

        elif isinstance(ast_node, PricingNode):
            return RenderNode(
                type='pricing',
                props={
                    'plan': ast_node.plan_name,
                    'price': ast_node.price,
                    'features': ast_node.features
                }
            )

        elif isinstance(ast_node, CtaNode):
            return RenderNode(
                type='cta',
                props={
                    'title': ast_node.title,
                    'button_text': ast_node.button_text
                }
            )

        elif isinstance(ast_node, BookingNode):
            return RenderNode(
                type='booking',
                props={
                    'service': ast_node.service_name or "Service",
                    'price': ast_node.price_prefix or "$"
                }
            )

        elif isinstance(ast_node, ContactNode):
            return RenderNode(
                type='contact',
                props={
                    'email': ast_node.email,
                    'form': ast_node.show_form
                }
            )

        # === PHASE 3.1 BASIC NODES ===

        elif isinstance(ast_node, ScreenNode):
            return RenderNode(
                type='screen',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, ColumnNode):
            return RenderNode(
                type='column',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, RowNode):
            return RenderNode(
                type='row',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, StackNode):
            return RenderNode(
                type='stack',
                children=[self._convert_node(child)
                          for child in ast_node.children]
            )

        elif isinstance(ast_node, TextNode):
            # Check if it's a variable binding or literal text
            if ast_node.is_binding:
                return RenderNode(
                    type='text',
                    binding=ast_node.value,
                    props={'value': ast_node.value}
                )
            else:
                # Literal text
                return RenderNode(
                    type='text',
                    props={'value': ast_node.value}
                )

        elif isinstance(ast_node, ButtonNode):
            return RenderNode(
                type='button',
                props={'label': ast_node.label},
                on_click=ast_node.on_click
            )

        elif isinstance(ast_node, InputNode):
            return RenderNode(
                type='input',
                binding=ast_node.binding,
                props={'placeholder': ast_node.placeholder or ''}
            )

        else:
            # Unknown node type
            return RenderNode(type='unknown')

    def subscribe_to_state(self):
        """Subscribe to runtime state changes"""
        if not hasattr(self.runtime, 'ui_binder'):
            return

        # Subscribe to all changes to ensure UI updates
        # In a more optimized version, we would only subscribe to bindings
        self.runtime.ui_binder.subscribe_all(self.on_state_change)

    def on_state_change(self, var_name, value):
        """Called when subscribed state changes"""
        # Trigger re-render
        self.trigger_render()

    def trigger_render(self):
        """Notify all render callbacks"""
        for callback in self.on_render_callbacks:
            try:
                callback(self.render_tree)
            except Exception as e:
                print(f"⚠️  Render callback error: {e}")

    def on_render(self, callback: Callable):
        """Register callback for render events"""
        self.on_render_callbacks.append(callback)

    def reload_ui(self, new_ui_ast: UINode):
        """Hot reload - rebuild tree without losing runtime state"""
        self.ui_ast = new_ui_ast
        self.render_tree = self.build_render_tree()
        self.subscribe_to_state()
        self.trigger_render()

    def __repr__(self):
        return f"<VisualRuntimeEngine tree={self.render_tree}>"
