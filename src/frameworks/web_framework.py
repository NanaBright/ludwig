"""
Ludwig Web Framework

A modern, Laravel-inspired web framework for Ludwig with TailwindCSS and shadcn/ui integration.
Provides routing, templating, database, authentication, and RESTful API development.
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Import Ludwig systems
try:
    from database import Database, Model, Migration
    from auth import Auth, JWTToken, PasswordHasher
    from validation import Validator
    from ludwig_collections import Collection
except ImportError:
    # Graceful fallback for standalone usage
    Database = Model = Migration = Auth = JWTToken = PasswordHasher = Validator = Collection = None


class Route:
    """Represents a web route in Ludwig."""
    
    def __init__(self, method, path, handler, middleware=None, name=None):
        """
        Initialize a route.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            path (str): Route path pattern
            handler (str): Handler function name
            middleware (list): List of middleware to apply
            name (str): Optional route name for URL generation
        """
        self.method = method.upper()
        self.path = path
        self.handler = handler
        self.middleware = middleware or []
        self.name = name
    
    def to_dict(self):
        """Convert route to dictionary."""
        return {
            'method': self.method,
            'path': self.path,
            'handler': self.handler,
            'middleware': self.middleware,
            'name': self.name
        }


class APIRoute(Route):
    """Represents a RESTful API route with automatic JSON responses."""
    
    def __init__(self, method, path, handler, middleware=None, model=None):
        """Initialize API route with optional model binding."""
        super().__init__(method, path, handler, middleware)
        self.model = model
        self.is_api = True


class Controller:
    """Base controller class with common functionality."""
    
    def __init__(self, db=None, auth=None, validator=None):
        """Initialize controller with dependencies."""
        self.db = db
        self.auth = auth
        self.validator = validator or (Validator() if Validator else None)
    
    def validate(self, data, rules):
        """Validate request data."""
        if self.validator:
            return self.validator.validate(data, rules)
        return {"valid": True, "errors": {}}
    
    def json_response(self, data, status=200):
        """Return JSON response."""
        return {
            "type": "json",
            "data": data,
            "status": status,
            "headers": {"Content-Type": "application/json"}
        }
    
    def success_response(self, data=None, message="Success"):
        """Return success JSON response."""
        return self.json_response({
            "success": True,
            "message": message,
            "data": data
        })
    
    def error_response(self, message="Error", errors=None, status=400):
        """Return error JSON response."""
        return self.json_response({
            "success": False,
            "message": message,
            "errors": errors or {}
        }, status)


class AuthController(Controller):
    """Authentication controller with login, register, logout."""
    
    def register(self, request_data):
        """Register a new user."""
        rules = {
            'name': ['required', 'string', 'min:2'],
            'email': ['required', 'email', 'unique:users'],
            'password': ['required', 'string', 'min:8']
        }
        
        validation = self.validate(request_data, rules)
        if not validation['valid']:
            return self.error_response("Validation failed", validation['errors'], 422)
        
        # Create user (assuming User model exists)
        if Model:
            try:
                user_data = {
                    'name': request_data['name'],
                    'email': request_data['email'],
                    'password': PasswordHasher.hash(request_data['password']) if PasswordHasher else request_data['password']
                }
                
                # In real implementation, this would use the User model
                user = {"id": 1, "name": user_data['name'], "email": user_data['email']}
                
                # Generate JWT token
                if JWTToken:
                    jwt = JWTToken()
                    token = jwt.encode({"user_id": user['id'], "email": user['email']})
                    
                    return self.success_response({
                        "user": user,
                        "token": token
                    }, "User registered successfully")
                
                return self.success_response(user, "User registered successfully")
                
            except Exception as e:
                return self.error_response(f"Registration failed: {str(e)}", status=500)
        
        return self.error_response("User registration not available", status=501)
    
    def login(self, request_data):
        """Authenticate user login."""
        rules = {
            'email': ['required', 'email'],
            'password': ['required', 'string']
        }
        
        validation = self.validate(request_data, rules)
        if not validation['valid']:
            return self.error_response("Validation failed", validation['errors'], 422)
        
        # In real implementation, find user by email and verify password
        # For now, mock user authentication
        if request_data['email'] == 'demo@ludwig.dev' and request_data['password'] == 'password':
            user = {"id": 1, "name": "Demo User", "email": "demo@ludwig.dev"}
            
            if JWTToken:
                jwt = JWTToken()
                token = jwt.encode({"user_id": user['id'], "email": user['email']})
                
                return self.success_response({
                    "user": user,
                    "token": token
                }, "Login successful")
            
            return self.success_response(user, "Login successful")
        
        return self.error_response("Invalid credentials", status=401)
    
    def logout(self, request_data):
        """Logout user (invalidate token)."""
        # In real implementation, add token to blacklist
        return self.success_response(message="Logged out successfully")


class WebFramework:
    """Ludwig Web Framework core class."""
    
    def __init__(self, app_name="Ludwig Web App", config=None):
        """Initialize the web framework."""
        self.app_name = app_name
        self.config = config or {}
        self.routes = []
        self.api_routes = []
        self.middleware = []
        self.components = {}
        
        # Initialize core systems
        self.db = None
        self.auth = None
        
        if Database:
            db_config = self.config.get('database', {
                'driver': 'sqlite',
                'database': 'ludwig.db'
            })
            self.db = Database(db_config)
        
        if Auth and JWTToken:
            auth_config = self.config.get('auth', {
                'jwt_secret': 'ludwig_secret_change_in_production'
            })
            self.auth = Auth(auth_config)
    
    def route(self, method, path, handler, middleware=None, name=None):
        """Register a route."""
        route = Route(method, path, handler, middleware, name)
        self.routes.append(route)
        return route
    
    def api_route(self, method, path, handler, middleware=None, model=None):
        """Register an API route with automatic JSON handling."""
        route = APIRoute(method, path, handler, middleware, model)
        self.api_routes.append(route)
        return route
    
    def get(self, path, handler, middleware=None, name=None):
        """Register a GET route."""
        return self.route('GET', path, handler, middleware, name)
    
    def post(self, path, handler, middleware=None, name=None):
        """Register a POST route."""
        return self.route('POST', path, handler, middleware, name)
    
    def put(self, path, handler, middleware=None, name=None):
        """Register a PUT route."""
        return self.route('PUT', path, handler, middleware, name)
    
    def delete(self, path, handler, middleware=None, name=None):
        """Register a DELETE route."""
        return self.route('DELETE', path, handler, middleware, name)
    
    def resource(self, name, controller, middleware=None):
        """Register RESTful resource routes."""
        base_path = f"/{name}"
        api_path = f"/api/{name}"
        
        # Standard REST routes
        routes = [
            ('GET', base_path, f'{controller}.index'),
            ('GET', f'{base_path}/create', f'{controller}.create'),
            ('POST', base_path, f'{controller}.store'),
            ('GET', f'{base_path}/{{id}}', f'{controller}.show'),
            ('GET', f'{base_path}/{{id}}/edit', f'{controller}.edit'),
            ('PUT', f'{base_path}/{{id}}', f'{controller}.update'),
            ('DELETE', f'{base_path}/{{id}}', f'{controller}.destroy'),
        ]
        
        # API routes (JSON responses)
        api_routes = [
            ('GET', api_path, f'{controller}.index'),
            ('POST', api_path, f'{controller}.store'),
            ('GET', f'{api_path}/{{id}}', f'{controller}.show'),
            ('PUT', f'{api_path}/{{id}}', f'{controller}.update'),
            ('DELETE', f'{api_path}/{{id}}', f'{controller}.destroy'),
        ]
        
        # Register web routes
        for method, path, handler in routes:
            self.route(method, path, handler, middleware)
        
        # Register API routes  
        for method, path, handler in api_routes:
            self.api_route(method, path, handler, middleware)
    
    def auth_routes(self, prefix="/auth"):
        """Register authentication routes."""
        self.post(f"{prefix}/register", "AuthController.register")
        self.post(f"{prefix}/login", "AuthController.login")
        self.post(f"{prefix}/logout", "AuthController.logout", ["auth"])
        
        # API versions
        self.api_route('POST', f"/api{prefix}/register", "AuthController.register")
        self.api_route('POST', f"/api{prefix}/login", "AuthController.login")
        self.api_route('POST', f"/api{prefix}/logout", "AuthController.logout", ["auth"])
    
    def get_all_routes(self):
        """Get all registered routes."""
        return {
            'web': [route.to_dict() for route in self.routes],
            'api': [route.to_dict() for route in self.api_routes]
        }


class UIComponentGenerator:
    """Generates shadcn/ui components for Ludwig web apps."""
    
    def __init__(self):
        """Initialize the component generator."""
        self.components = {
            'button': self._generate_button,
            'card': self._generate_card,
            'input': self._generate_input,
            'form': self._generate_form,
            'navigation': self._generate_navigation,
            'layout': self._generate_layout,
            'alert': self._generate_alert,
            'modal': self._generate_modal,
            'table': self._generate_table,
            'avatar': self._generate_avatar,
        }
    
    def generate(self, component_name, props=None):
        """Generate a UI component."""
        if component_name not in self.components:
            raise ValueError(f"Unknown component: {component_name}")
        
        return self.components[component_name](props or {})
    
    def _generate_button(self, props):
        """Generate a shadcn/ui button component."""
        variant = props.get('variant', 'default')
        size = props.get('size', 'default')
        text = props.get('text', 'Button')
        
        classes = {
            'default': 'bg-primary text-primary-foreground hover:bg-primary/90',
            'destructive': 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
            'outline': 'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
            'secondary': 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
            'ghost': 'hover:bg-accent hover:text-accent-foreground',
            'link': 'text-primary underline-offset-4 hover:underline',
        }
        
        sizes = {
            'default': 'h-10 px-4 py-2',
            'sm': 'h-9 rounded-md px-3',
            'lg': 'h-11 rounded-md px-8',
            'icon': 'h-10 w-10',
        }
        
        base_classes = "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
        
        return f'''<button class="{base_classes} {classes.get(variant, classes['default'])} {sizes.get(size, sizes['default'])}">{text}</button>'''
    
    def _generate_card(self, props):
        """Generate a shadcn/ui card component."""
        title = props.get('title', '')
        content = props.get('content', '')
        
        return f'''<div class="rounded-lg border bg-card text-card-foreground shadow-sm">
  {f'<div class="flex flex-col space-y-1.5 p-6"><h3 class="text-2xl font-semibold leading-none tracking-tight">{title}</h3></div>' if title else ''}
  <div class="p-6 pt-0">{content}</div>
</div>'''
    
    def _generate_input(self, props):
        """Generate a shadcn/ui input component."""
        placeholder = props.get('placeholder', '')
        input_type = props.get('type', 'text')
        
        return f'''<input type="{input_type}" class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" placeholder="{placeholder}" />'''
    
    def _generate_form(self, props):
        """Generate a form with shadcn/ui styling."""
        fields = props.get('fields', [])
        title = props.get('title', 'Form')
        
        field_html = []
        for field in fields:
            field_type = field.get('type', 'text')
            label = field.get('label', '')
            name = field.get('name', '')
            
            field_html.append(f'''
    <div class="space-y-2">
      <label class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70">{label}</label>
      <input type="{field_type}" name="{name}" class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50" />
    </div>''')
        
        return f'''<div class="rounded-lg border bg-card text-card-foreground shadow-sm">
  <div class="flex flex-col space-y-1.5 p-6">
    <h3 class="text-2xl font-semibold leading-none tracking-tight">{title}</h3>
  </div>
  <div class="p-6 pt-0">
    <form class="space-y-4">
      {''.join(field_html)}
      <button type="submit" class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2">Submit</button>
    </form>
  </div>
</div>'''
    
    def _generate_navigation(self, props):
        """Generate a navigation component."""
        items = props.get('items', [])
        brand = props.get('brand', 'Ludwig App')
        
        nav_items = []
        for item in items:
            name = item.get('name', '')
            href = item.get('href', '#')
            nav_items.append(f'<a href="{href}" class="text-sm font-medium transition-colors hover:text-primary">{name}</a>')
        
        return f'''<header class="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
  <div class="container flex h-14 items-center">
    <div class="mr-4 hidden md:flex">
      <a class="mr-6 flex items-center space-x-2" href="/">
        <span class="hidden font-bold sm:inline-block">{brand}</span>
      </a>
      <nav class="flex items-center space-x-6 text-sm font-medium">
        {''.join(nav_items)}
      </nav>
    </div>
  </div>
</header>'''
    
    def _generate_layout(self, props):
        """Generate a full page layout."""
        title = props.get('title', 'Ludwig App')
        content = props.get('content', '')
        nav_items = props.get('nav_items', [])
        
        navigation = self._generate_navigation({'brand': title, 'items': nav_items})
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        border: "hsl(var(--border))",
                        input: "hsl(var(--input))",
                        ring: "hsl(var(--ring))",
                        background: "hsl(var(--background))",
                        foreground: "hsl(var(--foreground))",
                        primary: {{
                            DEFAULT: "hsl(var(--primary))",
                            foreground: "hsl(var(--primary-foreground))",
                        }},
                        secondary: {{
                            DEFAULT: "hsl(var(--secondary))",
                            foreground: "hsl(var(--secondary-foreground))",
                        }},
                        destructive: {{
                            DEFAULT: "hsl(var(--destructive))",
                            foreground: "hsl(var(--destructive-foreground))",
                        }},
                        muted: {{
                            DEFAULT: "hsl(var(--muted))",
                            foreground: "hsl(var(--muted-foreground))",
                        }},
                        accent: {{
                            DEFAULT: "hsl(var(--accent))",
                            foreground: "hsl(var(--accent-foreground))",
                        }},
                        popover: {{
                            DEFAULT: "hsl(var(--popover))",
                            foreground: "hsl(var(--popover-foreground))",
                        }},
                        card: {{
                            DEFAULT: "hsl(var(--card))",
                            foreground: "hsl(var(--card-foreground))",
                        }},
                    }},
                }}
            }}
        }}
    </script>
    <style>
        :root {{
            --background: 0 0% 100%;
            --foreground: 222.2 84% 4.9%;
            --card: 0 0% 100%;
            --card-foreground: 222.2 84% 4.9%;
            --popover: 0 0% 100%;
            --popover-foreground: 222.2 84% 4.9%;
            --primary: 222.2 47.4% 11.2%;
            --primary-foreground: 210 40% 98%;
            --secondary: 210 40% 96%;
            --secondary-foreground: 222.2 47.4% 11.2%;
            --muted: 210 40% 96%;
            --muted-foreground: 215.4 16.3% 46.9%;
            --accent: 210 40% 96%;
            --accent-foreground: 222.2 47.4% 11.2%;
            --destructive: 0 84.2% 60.2%;
            --destructive-foreground: 210 40% 98%;
            --border: 214.3 31.8% 91.4%;
            --input: 214.3 31.8% 91.4%;
            --ring: 222.2 84% 4.9%;
            --radius: 0.5rem;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --background: 222.2 84% 4.9%;
                --foreground: 210 40% 98%;
                --card: 222.2 84% 4.9%;
                --card-foreground: 210 40% 98%;
                --popover: 222.2 84% 4.9%;
                --popover-foreground: 210 40% 98%;
                --primary: 210 40% 98%;
                --primary-foreground: 222.2 47.4% 11.2%;
                --secondary: 217.2 32.6% 17.5%;
                --secondary-foreground: 210 40% 98%;
                --muted: 217.2 32.6% 17.5%;
                --muted-foreground: 215 20.2% 65.1%;
                --accent: 217.2 32.6% 17.5%;
                --accent-foreground: 210 40% 98%;
                --destructive: 0 62.8% 30.6%;
                --destructive-foreground: 210 40% 98%;
                --border: 217.2 32.6% 17.5%;
                --input: 217.2 32.6% 17.5%;
                --ring: 212.7 26.8% 83.9%;
            }}
        }}
    </style>
</head>
<body class="min-h-screen bg-background font-sans antialiased">
    {navigation}
    <main class="flex-1">
        <div class="container mx-auto py-6">
            {content}
        </div>
    </main>
</body>
</html>'''
    
    def _generate_alert(self, props):
        """Generate an alert component."""
        variant = props.get('variant', 'default')
        title = props.get('title', '')
        message = props.get('message', '')
        
        variants = {
            'default': 'bg-background text-foreground',
            'destructive': 'border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive',
        }
        
        return f'''<div class="relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground {variants.get(variant, variants['default'])}">
  {f'<h5 class="mb-1 font-medium leading-none tracking-tight">{title}</h5>' if title else ''}
  <div class="text-sm [&_p]:leading-relaxed">{message}</div>
</div>'''
    
    def _generate_modal(self, props):
        """Generate a modal component."""
        title = props.get('title', 'Modal')
        content = props.get('content', '')
        
        return f'''<div class="fixed inset-0 z-50 bg-background/80 backdrop-blur-sm">
  <div class="fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 sm:rounded-lg">
    <div class="flex flex-col space-y-1.5 text-center sm:text-left">
      <h2 class="text-lg font-semibold">{title}</h2>
    </div>
    <div>{content}</div>
  </div>
</div>'''
    
    def _generate_table(self, props):
        """Generate a table component."""
        headers = props.get('headers', [])
        rows = props.get('rows', [])
        
        header_html = ''.join([f'<th class="h-12 px-4 text-left align-middle font-medium text-muted-foreground">{header}</th>' for header in headers])
        
        row_html = []
        for row in rows:
            cells = ''.join([f'<td class="p-4 align-middle">{cell}</td>' for cell in row])
            row_html.append(f'<tr class="border-b transition-colors hover:bg-muted/50">{cells}</tr>')
        
        return f'''<div class="relative w-full overflow-auto">
  <table class="w-full caption-bottom text-sm">
    <thead class="[&_tr]:border-b">
      <tr class="border-b transition-colors hover:bg-muted/50">{header_html}</tr>
    </thead>
    <tbody class="[&_tr:last-child]:border-0">
      {''.join(row_html)}
    </tbody>
  </table>
</div>'''
    
    def _generate_avatar(self, props):
        """Generate an avatar component."""
        src = props.get('src', '')
        alt = props.get('alt', 'Avatar')
        fallback = props.get('fallback', 'A')
        
        if src:
            return f'''<span class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
  <img class="aspect-square h-full w-full" alt="{alt}" src="{src}" />
</span>'''
        else:
            return f'''<span class="relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full">
  <span class="flex h-full w-full items-center justify-center rounded-full bg-muted">{fallback}</span>
</span>'''


# Example usage and testing
if __name__ == "__main__":
    # Test component generation
    generator = UIComponentGenerator()
    
    # Generate some components
    button = generator.generate('button', {'text': 'Click me', 'variant': 'default'})
    card = generator.generate('card', {'title': 'Welcome', 'content': 'This is a card component'})
    
    print("Button component:")
    print(button)
    print("\nCard component:")
    print(card)
