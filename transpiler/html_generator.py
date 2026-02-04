
from typing import List, Dict, Any


class HTMLGenerator:
    """
    Generates React Code (JSX) from parsed Aura commands.
    Now supports Multi-Page components, Rich Text, and Links.
    """

    def __init__(self, component_name="App"):
        self.component_name = component_name
        # React State
        self.imports = set([
            "import React, { useState, useEffect, useRef } from 'react';",
            "import { motion } from 'framer-motion';",
            # Added for routing and links
            "import { useNavigate, Link } from 'react-router-dom';",
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

    def generate(self, commands: List) -> str:
        for cmd in commands:
            self._process_command(cmd)
        return self._build_jsx()

    def _process_command(self, cmd):
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
            from parser import AuraParser
        except:
            from transpiler.parser import AuraParser

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
        render_str = self._render_elements(self.elements, indent=2)

        return f"""{imports_str}

export default function {self.component_name}() {{
    const navigate = useNavigate();
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

            if el.get('children'):
                children_str = ""
                for child in el['children']:
                    c_tag = child['type']
                    c_props = " ".join(
                        [f'{k}="{v}"' for k, v in child['props'].items()])
                    c_text = child.get('text_content', '')
                    children_str += f"\n{base_indent}    <{c_tag} {c_props}>{c_text}</{c_tag}>"
                lines.append(
                    f"{base_indent}<{tag}{props_str}>{children_str}\n{base_indent}</{tag}>")
            elif el.get('text_content'):
                lines.append(
                    f"{base_indent}<{tag}{props_str}>{el['text_content']}</{tag}>")
            else:
                lines.append(f"{base_indent}<{tag}{props_str} />")
        return "\n".join(lines)
