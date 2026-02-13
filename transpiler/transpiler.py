import os
import sys
import json
import subprocess
import glob
from pathlib import Path
from tqdm import tqdm

try:
    from .aura_parser import AuraParser
    from .logic_parser import LogicParser
    from .html_generator import HTMLGenerator
    from .ast_nodes import AppNode, PageNode, Program, LayoutNode, SlotNode, VariableNode, FetchNode
except ImportError:
    from aura_parser import AuraParser
    from logic_parser import LogicParser
    from html_generator import HTMLGenerator
    from ast_nodes import AppNode, PageNode, Program, LayoutNode, SlotNode, VariableNode, FetchNode


class AuraTranspiler:
    ENGINE_DIR = ".aura_engine"

    def __init__(self):
        self.parser = AuraParser()
        self.logic_parser = LogicParser()

    def build(self, input_file: str):
        """Builds the entire project (Multi-page support + Global Navbar)"""
        # print(f"[Aura] Project Build v4.0")

        if not os.path.exists(input_file):
            print(f"[Error] File not found: {input_file}")
            return False

        home_page_name = Path(input_file).stem
        input_dir = os.path.dirname(os.path.abspath(input_file))

        # Determine files to process: Only folder if in 'pages/', otherwise just the file
        if os.path.basename(input_dir) == 'pages':
            aura_files = glob.glob(os.path.join(input_dir, "*.aura"))
        else:
            aura_files = [input_file]

        pages = {}
        layouts = {}
        global_navbar = None

        # Helper to set home page correctly
        actual_home_page = None

        try:
            with tqdm(total=len(aura_files), desc="🚀 Building Project", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files") as pbar:
                for file_path in aura_files:
                    name = Path(file_path).stem
                    pbar.set_description(f"🚀 Scanning {name}")

                    # 🧠 Aura 6.0: Try structural parsing first
                    program = self.logic_parser.parse_file(file_path)

                    # Look for AppNode or PageNodes
                    structural_pages = []
                    structural_layouts = []
                    global_states = {}
                    app_node = None
                    for stmt in program.statements:
                        if isinstance(stmt, AppNode):
                            app_node = stmt
                            for p in stmt.pages:
                                if isinstance(p, PageNode):
                                    structural_pages.append(p)
                                elif isinstance(p, LayoutNode):
                                    structural_layouts.append(p)
                                elif isinstance(p, VariableNode):
                                    global_states[p.name] = p.value
                        elif isinstance(stmt, PageNode):
                            structural_pages.append(stmt)
                        elif isinstance(stmt, LayoutNode):
                            structural_layouts.append(stmt)
                        elif isinstance(stmt, VariableNode):
                            global_states[stmt.name] = stmt.value

                    if structural_pages or structural_layouts:
                        # Process Layouts first
                        for layout in structural_layouts:
                            l_name = layout.name
                            clean_l_name = l_name.replace(
                                ' ', '').replace('_', '').replace('-', '')
                            comp_name = clean_l_name[0].upper(
                            ) + clean_l_name[1:] if clean_l_name else "Layout"
                            if not comp_name.endswith('Layout'):
                                comp_name += 'Layout'

                            generator = HTMLGenerator(
                                component_name=comp_name, shared_states=global_states)
                            jsx = generator.generate(layout)
                            layouts[l_name] = {'comp': comp_name, 'code': jsx}

                        # Structural Build
                        for page in structural_pages:
                            p_name = page.name
                            clean_p_name = p_name.replace(
                                ' ', '').replace('_', '').replace('-', '')
                            comp_name = clean_p_name[0].upper(
                            ) + clean_p_name[1:] if clean_p_name else "Page"

                            generator = HTMLGenerator(
                                component_name=comp_name,
                                params=getattr(page, 'params', []),
                                shared_states=global_states)
                            jsx = generator.generate(page)
                            pages[p_name] = {
                                'comp': comp_name, 'code': jsx, 'params': getattr(page, 'params', [])}

                            # Set initial home page or explicit 'home'
                            if not actual_home_page:
                                actual_home_page = p_name
                            if p_name.lower() == 'home':
                                actual_home_page = p_name

                    else:
                        # Legacy/Hybrid Build (Single file = Single page)
                        clean_name = name.replace(' ', '').replace(
                            '_', '').replace('-', '')
                        comp_name = clean_name[0].upper(
                        ) + clean_name[1:] if clean_name else "Page"

                        commands = self.parser.parse_file(file_path)

                        # Check for Global Navbar Definition in legacy commands
                        for cmd in commands:
                            if hasattr(cmd, 'command_type') and cmd.command_type == 'ui_navbar':
                                global_navbar = cmd.data

                        generator = HTMLGenerator(component_name=comp_name)
                        jsx = generator.generate(commands)
                        pages[name] = {'comp': comp_name, 'code': jsx}

                        if not actual_home_page:
                            actual_home_page = name

                    pbar.update(1)

        except Exception as e:
            print(f"[Error] Compilation Failed: {e}")
            return False

        self._ensure_engine_structure()

        pages_dir = os.path.join(self.ENGINE_DIR, 'src', 'pages')
        layouts_dir = os.path.join(self.ENGINE_DIR, 'src', 'layouts')
        os.makedirs(pages_dir, exist_ok=True)
        os.makedirs(layouts_dir, exist_ok=True)

        for name, data in layouts.items():
            out_path = os.path.join(layouts_dir, f"{data['comp']}.jsx")
            self._write_file(out_path, data['code'])

        for name, data in pages.items():
            out_path = os.path.join(pages_dir, f"{data['comp']}.jsx")
            self._write_file(out_path, data['code'])

        # Generate Context and Router
        self._generate_global_context(
            global_states if 'global_states' in locals() else {})
        self._generate_router(
            pages, actual_home_page or home_page_name, global_navbar)

        # print("[Build] Project Updated.")
        return True

    def run(self, input_file: str):
        if not self.build(input_file):
            return

        router_path = os.path.join(
            self.ENGINE_DIR, 'node_modules', 'react-router-dom')
        if not os.path.exists(os.path.join(self.ENGINE_DIR, 'node_modules')) or not os.path.exists(router_path):
            print("[Install] Installing dependencies (including Router)...")
            self._run_npm(['install'])

        print("[Launch] Application...")
        print("Press Ctrl+C to stop.")
        self._run_npm(['run', 'dev', '--', '--open'], block=True)

    def _generate_router(self, pages, home_page_name, navbar_config=None):
        """Generates App.jsx and Navbar.jsx if needed"""

        imports = []
        routes = []
        home_comp = None

        for name, data in pages.items():
            comp = data['comp']
            params = data.get('params', [])
            imports.append(f"import {comp} from './pages/{comp}';")

            # Build path with params
            param_path = "".join([f"/:{p}" for p in params])
            path = f"/{name.lower()}{param_path}"

            if name == home_page_name and not params:
                path = "/"
                home_comp = comp
            routes.append(f'<Route path="{path}" element={{<{comp} />}} />')

        navbar_import = ""
        navbar_element = ""

        if navbar_config:
            self._generate_navbar_component(navbar_config)
            navbar_import = "import Navbar from './components/Navbar';"
            navbar_element = "<Navbar />"

        router_code = f"""import React from 'react';
import {{ Routes, Route }} from 'react-router-dom';
import {{ GlobalStateProvider }} from './context/GlobalContext';
{navbar_import}
{chr(10).join(imports)}

export default function App() {{
  return (
    <GlobalStateProvider>
      {navbar_element}
      <Routes>
        {chr(10).join(routes)}
        {f'<Route path="*" element={{<{home_comp} />}} />' if home_comp else ''}
      </Routes>
    </GlobalStateProvider>
  );
}}
"""
        self._write_file(os.path.join(
            self.ENGINE_DIR, 'src', 'App.jsx'), router_code)

    def _generate_navbar_component(self, config):
        """Generates the Navbar.jsx component"""
        components_dir = os.path.join(self.ENGINE_DIR, 'src', 'components')
        os.makedirs(components_dir, exist_ok=True)

        links_str = config['links']
        links_list = [l.strip() for l in links_str.split(',')]
        logo = config.get('logo', 'Aura App')

        # Generate generic link logic
        links_jsx = ""
        mobile_links_jsx = ""

        for link in links_list:
            path = "/" if link.lower() == 'home' else f"/{link.lower()}"
            # Desktop Link
            links_jsx += f"""
              <Link to="{path}" className={{`px-3 py-2 rounded-md text-sm font-medium transition-colors ${{location.pathname === '{path}' ? 'text-blue-500 bg-gray-100 dark:bg-gray-800' : 'text-gray-700 dark:text-gray-200 hover:text-blue-500'}}`}}>
                {link}
              </Link>
            """
            # Mobile Link
            mobile_links_jsx += f"""
              <Link to="{path}" onClick={{() => setIsOpen(false)}} className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 dark:text-gray-200 hover:text-blue-500 hover:bg-gray-50 dark:hover:bg-gray-800">
                {link}
              </Link>
            """

        navbar_code = f"""import React, {{ useState }} from 'react';
import {{ Link, useLocation }} from 'react-router-dom';
import {{ Menu, X }} from 'lucide-react';

export default function Navbar() {{
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  return (
    <nav className="sticky top-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              {logo}
            </Link>
          </div>
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {links_jsx}
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button onClick={{() => setIsOpen(!isOpen)}} className="inline-flex items-center justify-center p-2 rounded-md text-gray-700 dark:text-gray-200 hover:text-blue-500 focus:outline-none">
              {{isOpen ? <X size={{24}} /> : <Menu size={{24}} />}}
            </button>
          </div>
        </div>
      </div>
      {{/* Mobile Menu */}}
      {{isOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-white dark:bg-gray-900 shadow-lg">
            {mobile_links_jsx}
          </div>
        </div>
      )}}
    </nav>
  );
}}
"""
        self._write_file(os.path.join(
            components_dir, 'Navbar.jsx'), navbar_code)

    def _ensure_engine_structure(self):
        if not os.path.exists(self.ENGINE_DIR):
            os.makedirs(self.ENGINE_DIR)

        # NOTE: Excluding full template for brevity in this update, assuming key files handled in _write_file
        # But we must write main.jsx, tailwind, etc.
        # I'll rely on the fact that they are already written, OR re-write them to be safe.
        # Re-writing minimal needed.

        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import ErrorBoundary from './ErrorBoundary.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>,
)
"""
        src_dir = os.path.join(self.ENGINE_DIR, 'src')
        os.makedirs(src_dir, exist_ok=True)
        self._write_file(os.path.join(src_dir, 'main.jsx'), main_jsx)

        # Package.json handling to ensure router/lucide
        package_json = {
            "name": "aura-engine",
            "private": True,
            "version": "2.0.0",
            "type": "module",
            "scripts": {"dev": "vite", "build": "vite build", "preview": "vite preview"},
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.14.2",
                "lucide-react": "^0.263.1",
                "framer-motion": "^10.15.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.15", "@types/react-dom": "^18.2.7",
                "@vitejs/plugin-react": "^4.0.3", "autoprefixer": "^10.4.14",
                "postcss": "^8.4.27", "tailwindcss": "^3.3.3", "vite": "^4.4.5"
            }
        }
        self._write_file(os.path.join(
            self.ENGINE_DIR, 'package.json'), json.dumps(package_json, indent=2))

        # Configs
        vite_config = "import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\nexport default defineConfig({ plugins: [react()], server: { hmr: { overlay: false } } })"
        index_html = "<!doctype html><html lang='en'><head><meta charset='UTF-8' /><meta name='viewport' content='width=device-width, initial-scale=1.0' /><title>Aura App</title></head><body><div id='root'></div><script type='module' src='/src/main.jsx'></script></body></html>"
        index_css = "@tailwind base;\n@tailwind components;\n@tailwind utilities;"
        tailwind_config = "export default { content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'], theme: { extend: {} }, plugins: [], }"
        postcss_config = "export default { plugins: { tailwindcss: {}, autoprefixer: {}, }, }"
        error_boundary = "import React from 'react';\nclass ErrorBoundary extends React.Component {\n  constructor(props) { super(props); this.state = { hasError: false, error: null }; }\n  static getDerivedStateFromError(error) { return { hasError: true, error }; }\n  render() { if (this.state.hasError) return <div className='p-10 text-red-500'>Aura Error: {this.state.error.toString()}</div>; return this.props.children; }\n}\nexport default ErrorBoundary;"

        self._write_file(os.path.join(
            self.ENGINE_DIR, 'vite.config.js'), vite_config)
        self._write_file(os.path.join(
            self.ENGINE_DIR, 'index.html'), index_html)
        self._write_file(os.path.join(
            self.ENGINE_DIR, 'tailwind.config.js'), tailwind_config)
        self._write_file(os.path.join(
            self.ENGINE_DIR, 'postcss.config.js'), postcss_config)
        self._write_file(os.path.join(src_dir, 'index.css'), index_css)
        self._write_file(os.path.join(
            src_dir, 'ErrorBoundary.jsx'), error_boundary)

    def _write_file(self, path, content):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    if f.read() == content:
                        return
            except:
                pass
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _run_npm(self, args, block=True):
        use_shell = (os.name == 'nt')
        npm_cmd = 'npm.cmd' if use_shell else 'npm'
        try:
            cwd = os.path.abspath(self.ENGINE_DIR)
            if block:
                subprocess.run([npm_cmd] + args, cwd=cwd, shell=use_shell,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            else:
                subprocess.check_call([npm_cmd] + args, cwd=cwd, shell=use_shell,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    def _generate_global_context(self, global_states):
        context_dir = os.path.join(self.ENGINE_DIR, 'src', 'context')
        os.makedirs(context_dir, exist_ok=True)

        states_init = []
        context_values = []
        effects = []

        for name, val in global_states.items():
            setter = f"set{name.capitalize()}"
            if isinstance(val, FetchNode):
                initial = "[]"
                # Add useEffect for fetching
                effects.append(f"""    useEffect(() => {{
        fetch('{val.source}').then(res => res.json()).then(data => {setter}(data));
    }}, []);""")
            elif isinstance(val, (list, dict)):
                initial = json.dumps(val)
            elif isinstance(val, (int, float)):
                initial = str(val)
            else:
                initial = f"'{val}'"

            states_init.append(
                f"    const [{name}, {setter}] = useState({initial});")
            context_values.append(name)
            context_values.append(setter)

        states_code = "\n".join(states_init)
        effects_code = "\n".join(effects)
        values_code = ", ".join(context_values)

        code = f"""import React, {{ createContext, useContext, useState, useEffect }} from 'react';

const GlobalStateContext = createContext();

export const GlobalStateProvider = ({{ children }}) => {{
{states_code}

{effects_code}

    return (
        <GlobalStateContext.Provider value={{{{ {values_code} }}}}>
            {{children}}
        </GlobalStateContext.Provider>
    );
}};

export const useGlobalState = () => useContext(GlobalStateContext);
"""
        self._write_file(os.path.join(context_dir, 'GlobalContext.jsx'), code)


def main():
    if len(sys.argv) < 2:
        print("Usage: aura [init|run|build|dev] <filename.aura>")
        print("\nCommands:")
        print("  init  - Initialize a new Aura project with professional structure")
        print("  dev   - Start hot-reload dev server (watches all .aura files)")
        print("  run   - Build and launch dev server for a single file")
        print("  build - Build project without launching server")
        print("\nExamples:")
        print("  aura init              # Create new project")
        print("  aura dev               # Start development server")
        print("  aura run Home.aura     # Run a single file")
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        # Initialize a new Aura project
        try:
            from .init_project import AuraProjectInitializer
        except ImportError:
            from init_project import AuraProjectInitializer

        project_name = sys.argv[2] if len(sys.argv) > 2 else None
        initializer = AuraProjectInitializer(project_name)
        initializer.init()

    elif command == "dev":
        # Start the professional dev server
        try:
            from .dev_server import AuraDevServer
        except ImportError:
            from dev_server import AuraDevServer

        from pathlib import Path

        # Check if we're in a project with pages/ folder
        project_dir = Path.cwd()
        pages_dir = project_dir / 'pages'

        if pages_dir.exists():
            # Watch the pages/ folder
            dev_server = AuraDevServer(pages_dir)
        else:
            # Watch current directory (legacy mode)
            dev_server = AuraDevServer(project_dir)

        dev_server.start()

    else:
        transpiler = AuraTranspiler()

        if command == "run" and len(sys.argv) > 2:
            transpiler.run(sys.argv[2])
        elif command == "build" and len(sys.argv) > 2:
            transpiler.build(sys.argv[2])
        elif command.endswith('.aura'):
            transpiler.run(command)
        else:
            print(f"Unknown command: {command}")
            print("Run 'aura' without arguments to see usage")


if __name__ == "__main__":
    main()
