try:
    from .ast_nodes import ASTNode, VariableNode, PageNode, AppNode, NavigationNode, LayoutNode, SlotNode, AddNode, RemoveNode, FetchNode, NotifyNode
    from .ui_nodes import (
        UINode, ButtonNode, TextNode, InputNode, ColumnNode, RowNode,
        TableNode, GridNode, LayoutBlockNode, CardNode, ListNode,
        PanelNode, DividerNode, IconNode, ImageNode
    )
except ImportError:
    from ast_nodes import ASTNode, VariableNode, PageNode, AppNode, NavigationNode, LayoutNode, SlotNode, AddNode, RemoveNode, FetchNode, NotifyNode
    from ui_nodes import (
        UINode, ButtonNode, TextNode, InputNode, ColumnNode, RowNode,
        TableNode, GridNode, LayoutBlockNode, CardNode, ListNode,
        PanelNode, DividerNode, IconNode
    )

import json


class HTMLGenerator:
    """
    Generates React Code (JSX) from parsed Aura commands.
    Now supports Multi-Page components, Rich Text, and Links.
    """

    def __init__(self, component_name="App", params=None, shared_states=None):
        self.component_name = component_name
        self.params = params or []
        self.shared_states = shared_states or {}
        # React State
        self.imports = set([
            "import React, { useState, useEffect, useRef } from 'react';",
            "import { motion } from 'framer-motion';",
            # Added for routing and links
            "import { useNavigate, Link, useParams } from 'react-router-dom';",
            "import { useGlobalState } from '../context/GlobalContext';",
        ])

        # Internal tracking
        self.states = {}     # { 'varName': 'initialValue' }
        self.elements = []   # List of element dictionaries
        self.handlers = {}   # { 'elementId': { 'event': 'code' } }
        self.refs = {}       # { 'elementId': 'refName' }
        self.effects = []    # List of useEffect code blocks

        self.element_counter = 0
        self.last_element_id = None
        self.theme = 'dark'  # Default theme
        self.layout_name = None  # For page uses layout

    def generate(self, commands: Any) -> str:
        # Check if it's a list of commands or a Program (AST)
        if hasattr(commands, 'statements'):
            for stmt in commands.statements:
                self._handle_ast_node(stmt, self.elements)
        elif isinstance(commands, ASTNode):
            self._handle_ast_node(commands, self.elements)
        else:
            for cmd in commands:
                self._process_command(cmd)
        return self._build_jsx()

    def _process_command(self, cmd):
        # Check if it's an AST node or a legacy AuraCommand
        if isinstance(cmd, ASTNode):
            self._handle_ast_node(cmd, self.elements)
            return

        # Legacy command handling (remains flat)
        if cmd.command_type == 'variable':
            self._handle_variable(cmd)
        elif cmd.command_type == 'theme':
            self._handle_theme(cmd)
        elif cmd.command_type.startswith('ui_'):
            self._handle_ui_element(cmd)
        elif cmd.command_type == 'action_sequence':
            self._handle_action_sequence(cmd)
        elif cmd.command_type.startswith('style_'):
            self._handle_style_command(cmd)
        elif cmd.command_type.startswith('visibility_'):
            self._handle_visibility_command(cmd)

    def _handle_ast_node(self, node, parent_list, in_sidebar=False):
        if isinstance(node, VariableNode):
            # Mapping AST Variable to legacy format for generator
            state_name = node.name.lower()
            val = node.value

            if isinstance(val, FetchNode):
                self.states[state_name] = "[]"
                # Add fetch effect
                self.effects.append(
                    f"fetch('{val.source}').then(r => r.json()).then(data => set{node.name.capitalize()}(data));")
            elif isinstance(val, list):
                # Array literal
                self.states[state_name] = json.dumps(val)
            elif isinstance(val, str) and val.isdigit():
                self.states[state_name] = val
            elif isinstance(val, str) and (val.startswith("'") or val.startswith('"')):
                self.states[state_name] = val
            else:
                self.states[state_name] = f"'{val}'"

        elif isinstance(node, PageNode):
            self.layout_name = node.layout
            for child in node.children:
                self._handle_ast_node(child, parent_list, in_sidebar)

        elif isinstance(node, NavigationNode):
            # This is handled within action sequences usually, but can be a standalone command
            pass

        elif isinstance(node, (ButtonNode, TextNode, InputNode, TableNode, GridNode, LayoutBlockNode, LayoutNode, SlotNode, CardNode, ListNode, PanelNode, DividerNode, IconNode, ImageNode)):
            self._handle_ui_node(node, parent_list, in_sidebar)

        elif isinstance(node, (ColumnNode, RowNode)):
            # Create a container element for Column/Row
            container = self._create_base_element('div')
            container['props']['className'] = "flex flex-col gap-4" if isinstance(
                node, ColumnNode) else "flex flex-row gap-4"
            parent_list.append(container)
            for child in node.children:
                self._handle_ast_node(child, container['children'], in_sidebar)

    def _create_base_element(self, tag_type):
        self.element_counter += 1
        el_id = f"el_{self.element_counter}"
        self.last_element_id = el_id
        ref_name = f"{el_id}_ref"
        self.refs[el_id] = ref_name

        return {
            'id': el_id,
            'type': tag_type,
            'props': {
                'className': '',
                'ref': ref_name
            },
            'children': [],
            'text_content': None
        }

    def _handle_ui_node(self, node, parent_list, in_sidebar=False):
        tag = 'div'
        if isinstance(node, ButtonNode):
            tag = 'button'
        elif isinstance(node, TextNode):
            tag = 'span'
        elif isinstance(node, InputNode):
            tag = 'input'
        elif isinstance(node, LayoutBlockNode):
            tag = 'section'
        elif isinstance(node, LayoutNode):
            tag = 'div'
        elif isinstance(node, SlotNode):
            tag = 'SLOT'

        element = self._create_base_element(tag)
        parent_list.append(element)

        if isinstance(node, ButtonNode):
            element['text_content'] = node.label

            # 🎨 Context-Aware Styling
            if in_sidebar:
                element['props']['className'] = "w-full text-left px-4 py-3 rounded-xl text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-blue-600 transition-all font-medium"
            else:
                element['props']['className'] = "px-8 py-3 bg-gradient-to-r from-blue-600 to-indigo-700 text-white font-bold rounded-xl shadow-md hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200"

            if node.on_click:
                self.handlers[element['id']] = {
                    'onClick': self._generate_handler_code(node.on_click)}

        elif isinstance(node, TextNode):
            if node.is_binding:
                val = node.value
                # 🧠 Aura Semantic Transformation: sum(cart.price) -> sum(cart)
                # Our smart sum helper will handle the property extraction
                import re
                val = re.sub(r"sum\((\w+)\.\w+\)", r"sum(\1)", val)
                element['text_content'] = f"{{{val}}}"
            else:
                element['text_content'] = node.value

            # Heading vs Paragraph detection
            if len(node.value) < 40:
                element['type'] = 'h2'
                element['props']['className'] = "text-3xl font-extrabold text-gray-900 dark:text-white mb-6 tracking-tight"
            else:
                element['props']['className'] = "text-lg text-gray-600 dark:text-gray-400 leading-relaxed max-w-2xl"

        elif isinstance(node, InputNode):
            element['props']['placeholder'] = node.placeholder or "Search or enter value..."
            element['props']['className'] = "w-full max-w-md px-4 py-3 rounded-xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all shadow-sm"

        elif isinstance(node, TableNode):
            element['props']['className'] = "overflow-hidden rounded-2xl border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shadow-xl w-full"
            element['text_content'] = "📊 Data Table Placeholder"

        elif isinstance(node, GridNode):
            element['props']['className'] = "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full py-6"
            element['repeater'] = {
                'data': node.items_expr, 'item_name': 'item'}
            for child in node.children:
                self._handle_ast_node(child, element['children'], in_sidebar)

        elif isinstance(node, LayoutBlockNode):
            if node.block_type == 'sidebar':
                element['props']['className'] = "w-72 h-screen sticky top-0 bg-gray-50 dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800 p-8 hidden md:flex flex-col gap-2"
                # Add a logo placeholder to the sidebar
                logo = self._create_base_element('div')
                logo['props']['className'] = "text-2xl font-black mb-10 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent uppercase tracking-tighter"
                logo['text_content'] = "AURA CORE"
                element['children'].append(logo)
            elif node.block_type == 'main':
                element['props']['className'] = "flex-1 p-12 min-w-0 bg-white dark:bg-gray-950 overflow-y-auto"
            elif node.block_type == 'header':
                element['props']['className'] = "w-full py-6 px-12 border-b border-gray-200 dark:border-gray-800 flex justify-between items-center"

            # Recursively handle children of the block
            is_sidebar = (node.block_type == 'sidebar')
            for child in node.children:
                self._handle_ast_node(child, element['children'], is_sidebar)

        elif isinstance(node, LayoutNode):
            # Don't create a wrapper div for LayoutNode, _build_jsx will handle it
            for child in node.children:
                self._handle_ast_node(child, parent_list, in_sidebar)

        elif isinstance(node, SlotNode):
            element['type'] = 'SLOT'

        elif isinstance(node, CardNode):
            classes = [
                "p-6 rounded-2xl bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 transition-all duration-300 shadow-sm"]
            if 'hover' in node.effects:
                classes.append("hover:shadow-xl")
            if 'lift' in node.effects:
                classes.append("hover:-translate-y-2")
            element['props']['className'] = " ".join(classes)
            for child in node.children:
                self._handle_ast_node(child, element['children'], in_sidebar)

        elif isinstance(node, ImageNode):
            element['type'] = 'img'
            src = node.src
            if (src.startswith('"') and src.endswith('"')) or (src.startswith("'") and src.endswith("'")):
                element['props']['src'] = src[1:-1]
            else:
                element['props']['src'] = f"{{{src}}}"
            element['props']['className'] = "w-full h-48 object-cover rounded-xl mb-4"
            element['props']['alt'] = "Shop Item"

        elif isinstance(node, ListNode):
            element['props']['className'] = "flex flex-col gap-4 w-full"
            element['repeater'] = {
                'data': node.items_expr, 'item_name': 'item'}
            for child in node.children:
                self._handle_ast_node(child, element['children'], in_sidebar)

        elif isinstance(node, PanelNode):
            element['props']['className'] = "p-8 rounded-2xl bg-gray-50 dark:bg-gray-900/50 border border-gray-200 dark:border-gray-800"
            title = self._create_base_element('h3')
            title['props']['className'] = "text-xl font-bold mb-4"
            title['text_content'] = node.title
            element['children'].append(title)
            for child in node.children:
                self._handle_ast_node(child, element['children'], in_sidebar)

        elif isinstance(node, DividerNode):
            element['type'] = 'hr'
            element['props']['className'] = "my-6 border-gray-200 dark:border-gray-800"

        elif isinstance(node, IconNode):
            element['type'] = 'span'
            # Mapping common icon names to simple emojis or SVG classes for now
            icon_map = {'check-circle': '✅', 'credit-card': '💳',
                        'trash': '🗑️', 'shopping-cart': '🛒'}
            element['text_content'] = icon_map.get(node.icon_name.lower(), '📍')
            element['props'][
                'className'] = f"inline-block align-middle mr-2 text-{node.size or 'lg'}"
            if node.color:
                element['props']['style'] = f"{{{{ color: '{node.color}' }}}}"

    def _generate_handler_code(self, statements: List[ASTNode]) -> str:
        body_lines = []
        is_async = False

        for stmt in statements:
            if isinstance(stmt, NavigationNode):
                body_lines.append(f"navigate('/{stmt.target_page.lower()}');")
            elif isinstance(stmt, VariableNode):
                setter = f"set{stmt.name.capitalize()}"
                body_lines.append(f"{setter}({stmt.value});")
            elif isinstance(stmt, AddNode):
                setter = f"set{stmt.target.capitalize()}"
                body_lines.append(f"{setter}(prev => [...prev, {stmt.item}]);")
            elif isinstance(stmt, RemoveNode):
                setter = f"set{stmt.target.capitalize()}"
                # Simple removal by item itself or item.id if exists
                body_lines.append(
                    f"{setter}(prev => prev.filter(i => i !== {stmt.item}));")
            elif isinstance(stmt, NotifyNode):
                # Simple alert for now
                body_lines.append(f"alert({stmt.message});")

        prefix = "async " if is_async else ""
        return f"{prefix}() => {{\n        " + "\n        ".join(body_lines) + "\n    }"

    def _handle_variable(self, cmd):
        obj = cmd.data['object']
        prop = cmd.data['property']
        val = cmd.data['value']
        state_name = f"{obj}_{prop}".lower()
        if val.isdigit():
            self.states[state_name] = val
        else:
            self.states[state_name] = f"'{val}'"

    def _handle_theme(self, cmd):
        self.theme = cmd.data['theme'].lower()

    def _handle_ui_element(self, cmd):
        self.element_counter += 1
        el_id = f"el_{self.element_counter}"
        self.last_element_id = el_id
        ref_name = f"{el_id}_ref"
        self.refs[el_id] = ref_name

        element = {
            'id': el_id,
            'type': 'div',  # default
            'props': {
                'className': '',
                'ref': ref_name
            },
            'children': [],
            'text_content': None
        }

        # Tailwind Types
        if cmd.command_type == 'ui_button':
            element['type'] = 'button'
            element['text_content'] = cmd.data['text']
            element['props']['className'] = "px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold rounded-xl shadow-lg hover:shadow-2xl hover:scale-105 transition-all duration-200"

        elif cmd.command_type == 'ui_heading':
            element['type'] = 'h1'
            element['text_content'] = cmd.data['text']
            element['props']['className'] = "text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500 mb-6 drop-shadow-sm"

        elif cmd.command_type == 'ui_paragraph':
            element['type'] = 'p'
            element['text_content'] = cmd.data['text']
            element['props']['className'] = "text-lg text-gray-700 dark:text-gray-300 leading-relaxed mb-6 max-w-2xl"

        elif cmd.command_type == 'ui_input':
            element['type'] = 'input'
            element['props']['placeholder'] = cmd.data['text']
            element['props']['className'] = "w-full max-w-md px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all shadow-sm"

        elif cmd.command_type == 'ui_card':
            element['type'] = 'div'
            element['props']['className'] = "p-8 rounded-2xl bg-white dark:bg-gray-800 shadow-xl border border-gray-100 dark:border-gray-700 hover:shadow-2xl transition-all duration-300"
            title = cmd.data.get('title', '')
            desc = cmd.data.get('description', '')

            element['children'].append({'type': 'h3', 'props': {
                                       'className': 'text-2xl font-bold mb-2 text-gray-800 dark:text-white'}, 'text_content': title})
            if desc:
                element['children'].append({'type': 'p', 'props': {
                                           'className': 'text-gray-600 dark:text-gray-400'}, 'text_content': desc})

        elif cmd.command_type in ['ui_image', 'ui_image_simple']:
            element['type'] = 'img'
            element['props']['src'] = cmd.data['url']
            element['props']['alt'] = cmd.data.get('alt', 'Image')
            element['props']['className'] = "rounded-xl shadow-lg max-w-full h-auto hover:scale-[1.02] transition-transform duration-300"

        # NEW: Links
        elif cmd.command_type == 'ui_link_page':
            element['type'] = 'Link'
            element['text_content'] = cmd.data['text']
            # Normalization
            page = cmd.data['page'].replace(
                ' ', '').replace('_', '').replace('-', '')
            element['props']['to'] = f"/{page.lower()}"
            element['props']['className'] = "text-blue-600 dark:text-blue-400 font-medium hover:underline transition-colors cursor-pointer inline-flex items-center gap-1"

        elif cmd.command_type == 'ui_link_url':
            element['type'] = 'a'
            element['text_content'] = cmd.data['text']
            element['props']['href'] = cmd.data['url']
            element['props']['target'] = "_blank"
            element['props']['rel'] = "noopener noreferrer"
            element['props']['className'] = "text-blue-600 dark:text-blue-400 font-medium hover:underline transition-colors cursor-pointer inline-flex items-center gap-1"

        self.elements.append(element)

    def _handle_action_sequence(self, cmd):
        if not self.last_element_id:
            return

        event = cmd.data['event'].lower()
        react_event = 'onClick' if 'click' in event else 'onChange' if 'change' in event else 'onMouseEnter'

        try:
            from .aura_parser import AuraParser
        except ImportError:
            try:
                from aura_parser import AuraParser
            except ImportError:
                # Fallback for when running as script vs module
                from transpiler.aura_parser import AuraParser

        parser = AuraParser()
        parsed = parser.parse_action_sequence(cmd.data['actions'])

        body_lines = []
        is_async = False

        for action in parsed:
            atype = action['type']
            params = action['params']

            if atype == 'wait':
                secs = params.get('seconds', '1')
                body_lines.append(
                    f"await new Promise(resolve => setTimeout(resolve, {secs} * 1000));")
                is_async = True
            elif atype in ['display', 'alert']:
                body_lines.append(f"alert('{params.get('content', '')}');")
            elif atype == 'refresh':
                body_lines.append("window.location.reload();")
            elif atype == 'style_color':
                color = params.get('color', '')
                body_lines.append(
                    f"{self.refs[self.last_element_id]}.current.style.color = '{color}';")
            elif atype == 'style_size':
                size = params.get('size', '')
                scale = '1.2' if size in ['bigger', 'large'] else '0.8'
                body_lines.append(
                    f"{self.refs[self.last_element_id]}.current.style.transform = 'scale({scale})';")
            elif atype == 'hide':
                body_lines.append(
                    f"{self.refs[self.last_element_id]}.current.style.display = 'none';")
            elif atype == 'show':
                body_lines.append(
                    f"{self.refs[self.last_element_id]}.current.style.display = 'block';")
            elif atype == 'clear_input':
                body_lines.append(
                    f"{self.refs[self.last_element_id]}.current.value = '';")
            elif atype == 'navigate':  # External URL (Same tab)
                url = params.get('url', '')
                body_lines.append(f"window.location.href = '{url}';")
            elif atype == 'navigate_new_tab':  # NEW: External URL (New tab)
                url = params.get('url', '')
                body_lines.append(f"window.open('{url}', '_blank');")
            elif atype == 'navigate_page':  # Internal Router Page
                page = params.get('page', '')
                body_lines.append(f"navigate('/{page.lower()}');")
            elif atype == 'style_format':  # Dynamic formatting
                fmt = params.get('format', '').lower()
                cls = ''
                if fmt in ['bold']:
                    cls = 'font-bold'
                elif fmt in ['italic']:
                    cls = 'italic'
                elif fmt in ['underline', 'underlined']:
                    cls = 'underline'
                if cls:
                    body_lines.append(
                        f"{self.refs[self.last_element_id]}.current.classList.add('{cls}');")

        if self.last_element_id not in self.handlers:
            self.handlers[self.last_element_id] = {}

        fn_prefix = "async " if is_async else ""
        self.handlers[self.last_element_id][react_event] = f"{fn_prefix}() => {{\n        " + "\n        ".join(
            body_lines) + "\n    }"

    def _handle_style_command(self, cmd):
        if not self.last_element_id:
            return
        ref = self.refs[self.last_element_id]
        effect_code = ""

        if cmd.command_type == 'style_color':
            color = cmd.data['color']
            effect_code = f"{ref}.current.style.color = '{color}';"
        elif cmd.command_type == 'style_size':
            size = cmd.data['size']
            scale = '1.2' if size in ['bigger', 'large'] else '0.8'
            effect_code = f"{ref}.current.style.transform = 'scale({scale})';"
        elif cmd.command_type == 'style_format':
            fmt = (cmd.data.get('format') or cmd.data.get('verb') or '').lower()
            cls = ''
            if fmt in ['bold']:
                cls = 'font-bold'
            elif fmt in ['italic', 'italicize']:
                cls = 'italic'
            elif fmt in ['underline', 'underlined']:
                cls = 'underline'
            elif fmt in ['uppercase']:
                cls = 'uppercase'
            elif fmt in ['lowercase']:
                cls = 'lowercase'
            elif fmt in ['capitalize']:
                cls = 'capitalize'

            if cls:
                effect_code = f"{ref}.current.classList.add('{cls}');"
        elif cmd.command_type == 'style_align':
            align = (cmd.data.get('align') or 'center').lower()
            cls = f"text-{align}"
            effect_code = f"{ref}.current.classList.add('{cls}');"

        if effect_code:
            self.effects.append(effect_code)

    def _handle_visibility_command(self, cmd):
        if not self.last_element_id:
            return
        ref = self.refs[self.last_element_id]
        if cmd.command_type == 'visibility_hide':
            self.effects.append(f"{ref}.current.style.display = 'none';")

    def _build_jsx(self):
        imports_str = "\n".join(sorted(list(self.imports)))
        states_str = ""
        for name, initial in self.states.items():
            setter = f"set{name.replace('_', ' ').title().replace(' ', '')}"
            states_str += f"    const [{name}, {setter}] = useState({initial});\n"
        refs_str = ""
        for ref in self.refs.values():
            refs_str += f"    const {ref} = useRef(null);\n"
        effects_str = ""
        if self.effects:
            effects_str = "    useEffect(() => {\n"
            for ef in self.effects:
                effects_str += f"        {ef}\n"
            effects_str += "    }, []);\n"
        params_str = f"    const {{ {', '.join(self.params)} }} = useParams();" if self.params else ""
        shared_state_str = "    const { " + ", ".join(
            [f"{name}, set{name.capitalize()}" for name in self.shared_states]) + " } = useGlobalState();" if self.shared_states else ""
        render_str = self._render_elements(self.elements, indent=2)

        # 🧠 Layout Engine Transformation
        is_layout = self.component_name.lower().endswith('layout')

        if is_layout:
            # Check if layout itself has dashboard blocks
            has_sidebar = any(el.get('type') == 'section' and 'w-72' in el.get(
                'props', {}).get('className', '') for el in self.elements)
            container_class = "min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans flex" if has_sidebar else "min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans"

            return f"""{imports_str}

export default function {self.component_name}({{ children }}) {{
    const navigate = useNavigate(); // For layout-level nav
    const sum = (arr) => arr ? arr.reduce((acc, curr) => acc + (parseFloat(curr.price) || parseFloat(curr) || 0), 0) : 0;
{shared_state_str}
{states_str}
{refs_str}
{effects_str}
    return (
        <div className="{container_class}">
{render_str}
        </div>
    );
}}
"""

        # If page uses a layout
        if self.layout_name:
            clean_name = self.layout_name.replace(
                ' ', '').replace('_', '').replace('-', '')
            layout_comp = clean_name[0].upper(
            ) + clean_name[1:] if clean_name else "Layout"
            if not layout_comp.endswith('Layout'):
                layout_comp += 'Layout'

            # Add import for layout
            imports_str += f"\nimport {layout_comp} from '../layouts/{layout_comp}';"

            return f"""{imports_str}

export default function {self.component_name}() {{
    const navigate = useNavigate();
    const sum = (arr) => arr ? arr.reduce((acc, curr) => acc + (parseFloat(curr.price) || parseFloat(curr) || 0), 0) : 0;
{params_str}
{shared_state_str}
{states_str}
{refs_str}
{effects_str}
    return (
        <{layout_comp}>
{render_str}
        </{layout_comp}>
    );
}}
"""

        # 🧠 Structural Layout Detection
        # If the page contains sidebar/main blocks, use a dashboard-style layout
        has_sidebar = any(el.get('type') == 'section' and 'w-72' in el.get(
            'props', {}).get('className', '') for el in self.elements)

        if has_sidebar:
            return f"""{imports_str}

export default function {self.component_name}() {{
    const navigate = useNavigate();
    const sum = (arr) => arr ? arr.reduce((acc, curr) => acc + (parseFloat(curr.price) || parseFloat(curr) || 0), 0) : 0;
{params_str}
{shared_state_str}
{states_str}
{refs_str}
{effects_str}
    return (
        <div className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans flex">
{render_str}
        </div>
    );
}}
"""

        return f"""{imports_str}

export default function {self.component_name}() {{
    const navigate = useNavigate();
    const sum = (arr) => arr ? arr.reduce((acc, curr) => acc + (parseFloat(curr.price) || parseFloat(curr) || 0), 0) : 0;
{params_str}
{shared_state_str}
{states_str}
{refs_str}
{effects_str}
    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="w-full max-w-4xl flex flex-col items-center gap-6">
{render_str}
            </div>
        </div>
    );
}}
"""

    def _render_elements(self, elements, indent=0):
        lines = []
        base_indent = "    " * indent
        for el in elements:
            if not isinstance(el, dict) or 'id' not in el:
                continue
            tag = el['type']
            props = el['props']
            el_id = el['id']
            if el_id in self.handlers:
                for event, code in self.handlers[el_id].items():
                    props[event] = code
            props_str = ""
            for k, v in props.items():
                if k.startswith('on') or k == 'ref':
                    props_str += f" {k}={{{v}}}"
                else:
                    props_str += f' {k}="{v}"'

            if tag == 'SLOT':
                lines.append(f"{base_indent}{{children}}")
                continue

            if el.get('repeater'):
                data = el['repeater']['data']
                item_name = el['repeater'].get('item_name', 'item')
                children_str = self._render_elements(
                    el['children'], indent=indent + 2)

                content = f"{base_indent}<{tag}{props_str}>\n"
                content += f"{base_indent}  {{{data} && {data}.map(({item_name}, index) => (\n"
                content += f"{children_str}\n"
                content += f"{base_indent}  ))}}\n"
                content += f"{base_indent}</{tag}>"
                lines.append(content)
                continue

            if el.get('children'):
                children_str = self._render_elements(
                    el['children'], indent=indent + 1)
                lines.append(
                    f"{base_indent}<{tag}{props_str}>\n{children_str}\n{base_indent}</{tag}>")
            elif el.get('text_content'):
                lines.append(
                    f"{base_indent}<{tag}{props_str}>{el['text_content']}</{tag}>")
            else:
                lines.append(f"{base_indent}<{tag}{props_str} />")
        return "\n".join(lines)
