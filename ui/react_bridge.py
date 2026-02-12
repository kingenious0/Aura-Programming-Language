"""
React Bridge - Integration between Aura and React
Provides hooks and bindings for React components
"""

from typing import Any


class ReactBridge:
    """
    Bridge between Aura runtime and React components
    Generates React code with hooks
    """

    def __init__(self, ui_binder):
        self.ui_binder = ui_binder

    def generate_hook(self, var_name: str) -> str:
        """
        Generate React hook code for Aura state variable

        Returns JavaScript code:
        const [value, setValue] = useAuraState('varName');
        """
        return f"""
// Aura state hook for '{var_name}'
function useAuraState_{var_name}() {{
    const [value, setValue] = React.useState(null);
    
    React.useEffect(() => {{
        // Subscribe to Aura state
        const subscription = aura.subscribe('{var_name}', (newValue) => {{
            setValue(newValue);
        }});
        
        return () => {{
            // Cleanup
            aura.unsubscribe(subscription);
        }};
    }}, []);
    
    return [value, (newVal) => aura.setValue('{var_name}', newVal)];
}}
"""

    def generate_component(self, component_spec: dict) -> str:
        """
        Generate React component from Aura spec

        component_spec = {
            'name': 'Counter',
            'state': ['counter'],
            'elements': [...]
        }
        """
        name = component_spec.get('name', 'AuraComponent')
        state_vars = component_spec.get('state', [])

        # Generate hooks
        hooks = '\n'.join([
            f"  const [{var}, set{var.capitalize()}] = useAuraState('{var}');"
            for var in state_vars
        ])

        return f"""
function {name}() {{
{hooks}
  
  return (
    <div className="{name}">
      {{/* Component content */}}
    </div>
  );
}}
"""

    def generate_bridge_js(self) -> str:
        """Generate JavaScript bridge code"""
        return """
// Aura-React Bridge
const aura = {
    ws: null,
    subscriptions: new Map(),
    
    connect() {
        this.ws = new WebSocket('ws://localhost:8080');
        
        this.ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'state_update') {
                this.handleStateUpdate(message.data);
            }
        };
    },
    
    subscribe(varName, callback) {
        if (!this.subscriptions.has(varName)) {
            this.subscriptions.set(varName, []);
        }
        this.subscriptions.get(varName).push(callback);
        return { varName, callback };
    },
    
    unsubscribe({ varName, callback }) {
        const subs = this.subscriptions.get(varName);
        if (subs) {
            const index = subs.indexOf(callback);
            if (index > -1) subs.splice(index, 1);
        }
    },
    
    setValue(varName, value) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'set_variable',
                varName,
                value
            }));
        }
    },
    
    handleStateUpdate(data) {
        if (data.variables) {
            for (const [varName, value] of Object.entries(data.variables)) {
                const subs = this.subscriptions.get(varName);
                if (subs) {
                    subs.forEach(callback => callback(value));
                }
            }
        }
    }
};

// Auto-connect
aura.connect();

// React Hook
function useAuraState(varName) {
    const [value, setValue] = React.useState(null);
    
    React.useEffect(() => {
        const subscription = aura.subscribe(varName, setValue);
        return () => aura.unsubscribe(subscription);
    }, [varName]);
    
    return [value, (newVal) => aura.setValue(varName, newVal)];
}
"""
