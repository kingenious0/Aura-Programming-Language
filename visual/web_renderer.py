"""
Web Renderer - Converts render tree to HTML/DOM
Simple string templates for MVP (can optimize to vDOM later)
"""

from visual.render_tree import RenderTree, RenderNode
from typing import Optional


class WebRenderer:
    """
    Renders VRE output to HTML
    Uses string templates (simple, fast to ship)
    """

    def __init__(self, runtime, vre=None):
        self.runtime = runtime
        self.vre = vre

    def render(self, render_tree: RenderTree) -> str:
        """Convert render tree to HTML"""
        if not render_tree or not render_tree.root:
            return '<div class="aura-empty">No UI defined</div>'

        return self._render_node(render_tree.root)

    def _render_node(self, node: RenderNode) -> str:
        """Render single node to HTML"""

        # === PHASE 4.0 SEMANTIC COMPONENTS ===

        if node.type == 'page':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-page">{children_html}</div>'

        elif node.type == 'hero':
            title = node.props.get('title', 'Headline')
            subtitle = node.props.get('subtitle', '')
            cta = node.props.get('cta', '')

            cta_html = f'<button class="aura-button premium" data-node-id="{node.node_id}">{cta}</button>' if cta else ''
            subtitle_html = f'<p class="aura-subtitle">{subtitle}</p>' if subtitle else ''

            return f'''
            <section class="aura-hero">
                <div class="aura-container">
                    <h1 class="aura-title">{title}</h1>
                    {subtitle_html}
                    {cta_html}
                </div>
            </section>
            '''

        elif node.type == 'feature':
            title = node.props.get('title', 'Feature')
            desc = node.props.get('description', '')
            return f'''
            <div class="aura-feature-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            '''

        elif node.type == 'pricing':
            plan = node.props.get('plan', 'Standard')
            price = node.props.get('price', '$0')
            features = node.props.get('features', [])
            features_html = ''.join(f'<li>{f}</li>' for f in features)

            return f'''
            <div class="aura-pricing-card">
                <div class="plan">{plan}</div>
                <div class="price">{price}</div>
                <ul>{features_html}</ul>
                <button class="aura-button" data-node-id="{node.node_id}">Get Started</button>
            </div>
            '''

        elif node.type == 'cta':
            title = node.props.get('title', 'Ready?')
            btn = node.props.get('button_text', 'Join Now')
            return f'''
            <section class="aura-cta">
                <div class="aura-container">
                    <h2>{title}</h2>
                    <button class="aura-button premium" data-node-id="{node.node_id}">{btn}</button>
                </div>
            </section>
            '''

        elif node.type == 'booking':
            service = node.props.get('service', 'Session')
            return f'''
            <section class="aura-booking">
                <div class="aura-container">
                    <div class="aura-booking-card">
                        <h3>Book {service}</h3>
                        <div class="calendar-grid">
                            <span>Mon</span><span>Tue</span><span>Wed</span><span>Thu</span><span>Fri</span>
                            <button class="time-slot active" data-node-id="{node.node_id}">10:00 AM</button>
                            <button class="time-slot" data-node-id="{node.node_id}">1:00 PM</button>
                            <button class="time-slot" data-node-id="{node.node_id}">4:00 PM</button>
                        </div>
                        <button class="aura-button" data-node-id="{node.node_id}">confirm booking</button>
                    </div>
                </div>
            </section>
            '''

        elif node.type == 'contact':
            email = node.props.get('email', 'hello@aura.lang')
            return f'''
            <section class="aura-contact">
                <div class="aura-container">
                    <div class="aura-contact-grid">
                        <div>
                            <h2>Contact Us</h2>
                            <p>We'd love to hear from you. Send us a message or find us on the social machine.</p>
                            <strong>{email}</strong>
                        </div>
                        <form class="aura-form">
                            <input type="text" placeholder="Your Name" />
                            <input type="email" placeholder="Your Email" />
                            <textarea placeholder="How can we help?"></textarea>
                            <button class="aura-button" data-node-id="{node.node_id}">Send Message</button>
                        </form>
                    </div>
                </div>
            </section>
            '''

        # === PHASE 3.1 BASIC COMPONENTS ===

        elif node.type == 'screen':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-screen">{children_html}</div>'

        elif node.type == 'column':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-column">{children_html}</div>'

        elif node.type == 'row':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-row">{children_html}</div>'

        elif node.type == 'text':
            value = node.resolve_value(self.runtime)
            # Escape HTML
            value = str(value).replace('<', '&lt;').replace('>', '&gt;')
            return f'<span class="aura-text">{value}</span>'

        elif node.type == 'button':
            label = node.props.get('label', 'Button')
            return f'''<button class="aura-button" data-node-id="{node.node_id}">{label}</button>'''

        elif node.type == 'table':
            return '<div class="aura-table-container"><table class="aura-table"><thead><tr><th>ID</th><th>Name</th><th>Status</th></tr></thead><tbody><tr><td>#1</td><td>Demo Order</td><td>Pending</td></tr></tbody></table></div>'

        elif node.type == 'grid':
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-grid">{children_html}</div>'

        elif node.type in ['sidebar', 'main', 'header', 'footer']:
            children_html = ''.join(self._render_node(child)
                                    for child in node.children)
            return f'<div class="aura-{node.type}">{children_html}</div>'

        elif node.type == 'input':
            placeholder = node.props.get('placeholder', '')
            current_value = node.resolve_value(
                self.runtime) if node.binding else ''
            return f'''<input 
                class="aura-input" 
                data-node-id="{node.node_id}"
                data-binding="{node.binding or ''}"
                placeholder="{placeholder}"
                value="{current_value}"
            />'''

        else:
            return f'<div class="aura-unknown">Unknown: {node.type}</div>'

    def get_styles(self) -> str:
        """Return dynamic premium CSS styles based on Design System"""
        if not self.vre or not self.vre.current_system:
            return "<style>/* system not found */</style>"

        sys = self.vre.current_system
        colors = sys.colors
        typo = sys.typography
        spacing = sys.spacing

        return f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            
            body {{
                font-family: 'Inter', {typo['font_family']};
                background: {colors['bg']};
                color: {colors['text']};
                line-height: 1.6;
            }}
            
            .aura-container {{
                max-width: {spacing['max_width']};
                margin: 0 auto;
                padding: 0 40px;
            }}

            /* Grid Systems */
            .aura-page {{
                display: flex;
                flex-direction: column;
            }}

            .aura-features-grid, .aura-pricing-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                padding: 60px 0;
            }}

            /* Sections */
            .aura-hero {{
                padding: 160px 0 100px;
                text-align: center;
                animation: fadeIn 0.8s ease-out;
            }}

            .aura-cta {{
                padding: 100px 0;
                text-align: center;
                background: {colors['primary']}05;
                margin: 60px 0;
                border-radius: 40px;
            }}

            /* Cards */
            .aura-feature-card, .aura-pricing-card, .aura-booking-card {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(0,0,0,0.05);
                padding: 40px;
                border-radius: 24px;
                transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            }}

            /* Booking */
            .calendar-grid {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 10px;
                margin: 30px 0;
            }}
            .time-slot {{
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
                background: white;
                cursor: pointer;
            }}
            .time-slot.active {{
                background: {colors['primary']};
                color: white;
                border-color: {colors['primary']};
            }}

            /* Contact form */
            .aura-contact-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 80px;
                padding: 100px 0;
            }}
            .aura-form {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .aura-form input, .aura-form textarea {{
                padding: 16px;
                border: 1.5px solid #eee;
                border-radius: 12px;
                font-family: inherit;
                outline: none;
            }}
            .aura-form input:focus {{ border-color: {colors['primary']}; }}

            .aura-title {{
                font-size: {typo['h1']};
                font-weight: 800;
                letter-spacing: -0.02em;
                margin-bottom: 24px;
                background: linear-gradient(135deg, {colors['text']} 0%, {colors['primary']} 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            
            .aura-subtitle {{
                font-size: 1.5rem;
                color: #666;
                max-width: 600px;
                margin: 0 auto 40px;
            }}

            /* Cards */
            .aura-feature-card, .aura-pricing-card {{
                background: rgba(255,255,255,0.05);
                border: 1px solid rgba(0,0,0,0.05);
                padding: 32px;
                border-radius: 20px;
                transition: transform 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
            }}

            .aura-feature-card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.05);
            }}

            /* Buttons */
            .aura-button {{
                padding: 14px 28px;
                font-size: 1.1rem;
                font-weight: 600;
                background: {colors['primary']};
                color: #fff;
                border: none;
                border-radius: 12px;
                cursor: pointer;
                transition: all 0.2s;
            }}
            
            .aura-button.premium {{
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            }}

            .aura-button:hover {{
                opacity: 0.9;
                transform: scale(1.02);
            }}

            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
        </style>
        """
