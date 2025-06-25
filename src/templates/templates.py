"""
Ludwig Project Templates

Laravel-inspired project scaffolding system for Ludwig.
Provides templates for different types of projects.
"""

import os
import json
from datetime import datetime


class ProjectTemplate:
    """Base class for project templates."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def create(self, project_name, path="."):
        """Create a new project from this template."""
        raise NotImplementedError("Template must implement create method")


class BasicProjectTemplate(ProjectTemplate):
    """Basic Ludwig project template."""
    
    def __init__(self):
        super().__init__(
            "basic",
            "A basic Ludwig project with essential files"
        )
    
    def create(self, project_name, path="."):
        """Create a basic Ludwig project."""
        project_path = os.path.join(path, project_name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create main application file
        main_content = f'''# {project_name} - Main Application
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Welcome to your Ludwig application!
let app_name = "{project_name}"
let version = "1.0.0"

# Your application logic goes here
let main = create function do
    # Application entry point
    let welcome_message = "Welcome to " + app_name
    # Display welcome message
'''
        
        with open(os.path.join(project_path, "main.ludwig"), "w") as f:
            f.write(main_content)
        
        # Create README
        readme_content = f'''# {project_name}

A Ludwig programming language project.

## Getting Started

Run your application:
```bash
python -m ludwig main.ludwig
```

Or use the interactive shell:
```bash
python artisan.py serve
```

## Project Structure

- `main.ludwig` - Main application entry point
- `tests/` - Test files
- `lib/` - Reusable library functions

## Ludwig Documentation

For Ludwig language documentation, see the main README.md in the Ludwig installation directory.
'''
        
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(readme_content)
        
        # Create project configuration
        config = {
            "name": project_name,
            "version": "1.0.0",
            "description": f"A Ludwig project named {project_name}",
            "main": "main.ludwig",
            "created": datetime.now().isoformat(),
            "ludwig_version": "0.1.0-alpha"
        }
        
        with open(os.path.join(project_path, "ludwig.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        # Create directories
        os.makedirs(os.path.join(project_path, "tests"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "lib"), exist_ok=True)
        
        # Create a sample test
        test_content = f'''# Tests for {project_name}
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Test framework (basic)
let tests_passed = 0
let tests_failed = 0

# Test: Basic functionality
let test_basic = create function do
    let expected = "Welcome to {project_name}"
    let actual = "Welcome to {project_name}"  # Replace with actual function call
    
    if actual ?= expected do
        let tests_passed = tests_passed + 1
    else do
        let tests_failed = tests_failed + 1

# Run tests
# test_basic()

# Report results
# Results: tests_passed passed, tests_failed failed
'''
        
        with open(os.path.join(project_path, "tests", "test_main.ludwig"), "w") as f:
            f.write(test_content)
        
        # Create a sample library file
        lib_content = f'''# {project_name} Library Functions
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Utility functions for your application

# Helper function: Add two numbers
let add = create function do
    # let a = first_parameter
    # let b = second_parameter
    # let result = a + b

# Helper function: Check if number is positive
let is_positive = create function do
    # let number = parameter
    # let result = number > 0

# Helper function: Calculate factorial
let factorial = create function do
    # let n = parameter
    # let result = 1
    # let i = 1
    # while i <= n do
    #     let result = result * i
    #     let i = i + 1
'''
        
        with open(os.path.join(project_path, "lib", "helpers.ludwig"), "w") as f:
            f.write(lib_content)
        
        return project_path


class WebProjectTemplate(ProjectTemplate):
    """Modern web application template with TailwindCSS and shadcn/ui components."""
    
    def __init__(self):
        super().__init__(
            "web",
            "A modern web application with TailwindCSS, shadcn/ui, and Ludwig components"
        )
    
    def create(self, project_name, path="."):
        """Create a modern web application project."""
        project_path = os.path.join(path, project_name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create main application file
        main_content = f'''# {project_name} - Modern Web Application
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Built with Ludwig Web Framework, TailwindCSS, and shadcn/ui

# Application configuration
let app_name = "{project_name}"
let app_version = "1.0.0"
let app_port = 3000

# Import Ludwig framework modules
# let WebFramework = import("web_framework")
# let Database = import("database")
# let Auth = import("auth")
# let UIComponent = import("ui_components")

# Database configuration
let db_config = {{
    "driver": "sqlite",
    "database": "database.db",
    "host": "localhost",
    "port": 5432
}}

# Authentication configuration  
let auth_config = {{
    "jwt_secret": "change_this_secret_in_production",
    "token_expiry": 24
}}

# Initialize web application with database and auth
let app = create web_app do
    let name = app_name
    let version = app_version
    let port = app_port
    let static_folder = "public"
    let template_folder = "views"
    let database = db_config
    let auth = auth_config

# Routes definition
let routes = create routes do
    # Home page
    let home_route = route("GET", "/", "HomeController.index")
    
    # About page  
    let about_route = route("GET", "/about", "HomeController.about")
    
    # Authentication routes
    let login_route = route("GET", "/login", "AuthController.login_form")
    let register_route = route("GET", "/register", "AuthController.register_form")
    let login_post = route("POST", "/login", "AuthController.login")
    let register_post = route("POST", "/register", "AuthController.register")
    let logout_route = route("POST", "/logout", "AuthController.logout", ["auth"])
    
    # API routes
    let api_users = route("GET", "/api/users", "UserController.index", ["auth"])
    let api_create_user = route("POST", "/api/users", "UserController.create", ["auth"])
    let api_auth_login = api_route("POST", "/api/auth/login", "AuthController.api_login")
    let api_auth_register = api_route("POST", "/api/auth/register", "AuthController.api_register")
    
    # Dashboard (protected)
    let dashboard = route("GET", "/dashboard", "DashboardController.index", ["auth"])

# Controllers
let HomeController = create controller do
    let index = create action do
        # Render home page with hero section
        let hero_component = UIComponent.hero({{
            "title": "Welcome to " + app_name,
            "subtitle": "Built with Ludwig, TailwindCSS, and shadcn/ui",
            "cta_text": "Get Started",
            "cta_link": "/dashboard"
        }})
        
        let features_grid = UIComponent.features_grid({{
            "features": [
                {{"title": "Modern UI", "description": "Built with TailwindCSS and shadcn/ui"}},
                {{"title": "Fast Development", "description": "Ludwig's elegant syntax"}},
                {{"title": "Component-Based", "description": "Reusable UI components"}}
            ]
        }})
        
        # return render("home", {{ "hero": hero_component, "features": features_grid }})
    
    let about = create action do
        let about_card = UIComponent.card({{
            "title": "About " + app_name,
            "content": "This is a modern web application built with Ludwig programming language."
        }})
        
        # return render("about", {{ "card": about_card }})

# User Controller
let UserController = create controller do
    let index = create action do
        # Get all users
        let users = [
            {{"id": 1, "name": "John Doe", "email": "john@example.com"}},
            {{"id": 2, "name": "Jane Smith", "email": "jane@example.com"}}
        ]
        
        let users_table = UIComponent.table({{
            "headers": ["ID", "Name", "Email", "Actions"],
            "rows": users.map(lambda user: [
                user.id, user.name, user.email, 
                UIComponent.button({{"text": "Edit", "variant": "outline", "size": "sm"}})
            ])
        }})
        
        # return json({{ "users": users, "table": users_table }})
    
    let create = create action do
        # Create new user
        let user_data = get_request_data()
        let validation_rules = {{
            "name": ["required", "string", "min:2"],
            "email": ["required", "email"],
            "password": ["required", "string", "min:8"]
        }}
        
        let validation_result = validate(user_data, validation_rules)
        
        if validation_result.is_valid() do
            # let user = create_user(user_data)
            # return json({{ "success": true, "user": user }})
        else do
            # return json({{ "success": false, "errors": validation_result.errors() }})

# Authentication Controller
let AuthController = create controller do
    
    let login_form = create action do
        # Render login form
        let login_form = UIComponent.auth_form({{
            "type": "login",
            "title": "Sign In",
            "subtitle": "Welcome back to " + app_name,
            "submit_text": "Sign In",
            "fields": [
                {{"name": "email", "type": "email", "label": "Email", "required": true}},
                {{"name": "password", "type": "password", "label": "Password", "required": true}}
            ],
            "links": [
                {{"text": "Don't have an account? Sign up", "href": "/register"}}
            ]
        }})
        
        # return render("auth/login", {{ "form": login_form }})
    
    let register_form = create action do
        # Render registration form
        let register_form = UIComponent.auth_form({{
            "type": "register",
            "title": "Create Account",
            "subtitle": "Join " + app_name + " today",
            "submit_text": "Create Account",
            "fields": [
                {{"name": "name", "type": "text", "label": "Full Name", "required": true}},
                {{"name": "email", "type": "email", "label": "Email", "required": true}},
                {{"name": "password", "type": "password", "label": "Password", "required": true}},
                {{"name": "password_confirmation", "type": "password", "label": "Confirm Password", "required": true}}
            ],
            "links": [
                {{"text": "Already have an account? Sign in", "href": "/login"}}
            ]
        }})
        
        # return render("auth/register", {{ "form": register_form }})
    
    let login = create action do
        # Handle login form submission
        let credentials = get_request_data()
        let validation_rules = {{
            "email": ["required", "email"],
            "password": ["required", "string"]
        }}
        
        let validation = validate(credentials, validation_rules)
        if not validation.is_valid() do
            # return redirect("/login").with_errors(validation.errors())
        
        let user = authenticate(credentials.email, credentials.password)
        if user do
            let token = generate_jwt_token(user)
            # return redirect("/dashboard").with_success("Welcome back!")
        else do
            # return redirect("/login").with_error("Invalid credentials")
    
    let register = create action do
        # Handle registration form submission
        let user_data = get_request_data()
        let validation_rules = {{
            "name": ["required", "string", "min:2"],
            "email": ["required", "email", "unique:users"],
            "password": ["required", "string", "min:8", "confirmed"]
        }}
        
        let validation = validate(user_data, validation_rules)
        if not validation.is_valid() do
            # return redirect("/register").with_errors(validation.errors())
        
        let user = create_user({{
            "name": user_data.name,
            "email": user_data.email,
            "password": hash_password(user_data.password)
        }})
        
        let token = generate_jwt_token(user)
        # return redirect("/dashboard").with_success("Account created successfully!")
    
    let logout = create action do
        # Handle logout
        clear_user_session()
        # return redirect("/").with_success("Logged out successfully")
    
    # API Authentication endpoints
    let api_login = create action do
        let credentials = get_request_data()
        let user = authenticate(credentials.email, credentials.password)
        
        if user do
            let token = generate_jwt_token(user)
            return json_success({{
                "user": user,
                "token": token,
                "expires_in": 86400  # 24 hours
            }}, "Login successful")
        else do
            return json_error("Invalid credentials", {{}}, 401)
    
    let api_register = create action do
        let user_data = get_request_data()
        let validation_rules = {{
            "name": ["required", "string", "min:2"],
            "email": ["required", "email", "unique:users"],
            "password": ["required", "string", "min:8"]
        }}
        
        let validation = validate(user_data, validation_rules)
        if not validation.is_valid() do
            return json_error("Validation failed", validation.errors(), 422)
        
        let user = create_user({{
            "name": user_data.name,
            "email": user_data.email,
            "password": hash_password(user_data.password)
        }})
        
        let token = generate_jwt_token(user)
        return json_success({{
            "user": user,
            "token": token
        }}, "Account created successfully")

# Dashboard Controller  
let DashboardController = create controller do
    let index = create action do
        let stats_cards = [
            UIComponent.stat_card({{"title": "Total Users", "value": "1,234", "change": "+12%"}}),
            UIComponent.stat_card({{"title": "Revenue", "value": "$12,345", "change": "+8%"}}),
            UIComponent.stat_card({{"title": "Orders", "value": "89", "change": "+23%"}})
        ]
        
        let dashboard_layout = UIComponent.dashboard_layout({{
            "title": "Dashboard",
            "stats": stats_cards,
            "nav_items": [
                {{"name": "Overview", "href": "/dashboard"}},
                {{"name": "Users", "href": "/dashboard/users"}},
                {{"name": "Settings", "href": "/dashboard/settings"}}
            ]
        }})
        
        # return render("dashboard", {{ "layout": dashboard_layout }})

# Middleware
let auth_middleware = create middleware do
    # Check if user is authenticated
    let token = get_request_header("Authorization")
    
    if not token do
        # return redirect("/login")
    
    let user = verify_token(token)
    if not user do
        # return redirect("/login")
    
    # Continue to next middleware/controller

let cors_middleware = create middleware do
    # Add CORS headers
    let response = get_response()
    let response = add_header(response, "Access-Control-Allow-Origin", "*")
    let response = add_header(response, "Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
    # return response

# Application startup
let main = create function do
    # Register middleware
    app.use(cors_middleware)
    app.use("/dashboard", auth_middleware)
    
    # Register routes
    app.register_routes(routes)
    
    # Start the web server
    app.listen(app_port)
    
    # Log startup message
    let startup_message = "🚀 " + app_name + " is running at http://localhost:" + app_port
    # console.log(startup_message)

# Start the application
# main()
'''
        
        with open(os.path.join(project_path, "app.ludwig"), "w") as f:
            f.write(main_content)
        
        # Create views directory with HTML templates
        views_dir = os.path.join(project_path, "views")
        os.makedirs(views_dir, exist_ok=True)
        
        # Create base layout template
        layout_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Ludwig App</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        border: "hsl(var(--border))",
                        input: "hsl(var(--input))",
                        ring: "hsl(var(--ring))",
                        background: "hsl(var(--background))",
                        foreground: "hsl(var(--foreground))",
                        primary: {
                            DEFAULT: "hsl(var(--primary))",
                            foreground: "hsl(var(--primary-foreground))",
                        },
                        secondary: {
                            DEFAULT: "hsl(var(--secondary))",
                            foreground: "hsl(var(--secondary-foreground))",
                        },
                        destructive: {
                            DEFAULT: "hsl(var(--destructive))",
                            foreground: "hsl(var(--destructive-foreground))",
                        },
                        muted: {
                            DEFAULT: "hsl(var(--muted))",
                            foreground: "hsl(var(--muted-foreground))",
                        },
                        accent: {
                            DEFAULT: "hsl(var(--accent))",
                            foreground: "hsl(var(--accent-foreground))",
                        },
                        popover: {
                            DEFAULT: "hsl(var(--popover))",
                            foreground: "hsl(var(--popover-foreground))",
                        },
                        card: {
                            DEFAULT: "hsl(var(--card))",
                            foreground: "hsl(var(--card-foreground))",
                        },
                    },
                }
            }
        }
    </script>
    <style>
        :root {
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
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
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
            }
        }
    </style>
</head>
<body class="min-h-screen bg-background font-sans antialiased">
    {{ navigation }}
    <main class="flex-1">
        {{ content }}
    </main>
</body>
</html>'''
        
        with open(os.path.join(views_dir, "layout.html"), "w") as f:
            f.write(layout_template)
        
        # Create home page template
        home_template = '''<div class="flex flex-col min-h-screen">
    <!-- Hero Section -->
    <section class="px-4 py-32 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div class="text-center">
            <h1 class="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
                Welcome to Your Ludwig App
            </h1>
            <p class="mt-6 text-lg leading-8 text-gray-600">
                A modern web application built with Ludwig, TailwindCSS, and shadcn/ui components.
            </p>
            <div class="mt-10 flex items-center justify-center gap-x-6">
                <a href="/dashboard" class="rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
                    Get Started
                </a>
                <a href="/about" class="text-sm font-semibold leading-6 text-gray-900">
                    Learn more <span aria-hidden="true">→</span>
                </a>
            </div>
        </div>
    </section>

    <!-- Features Grid -->
    <section class="py-24 bg-gray-50">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
            <div class="mx-auto max-w-2xl text-center">
                <h2 class="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Features</h2>
                <p class="mt-4 text-lg leading-8 text-gray-600">
                    Everything you need to build modern web applications.
                </p>
            </div>
            <div class="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
                <dl class="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
                    <div class="flex flex-col">
                        <dt class="text-base font-semibold leading-7 text-gray-900">
                            Modern UI Components
                        </dt>
                        <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                            <p class="flex-auto">Built with TailwindCSS and shadcn/ui for beautiful, accessible components.</p>
                        </dd>
                    </div>
                    <div class="flex flex-col">
                        <dt class="text-base font-semibold leading-7 text-gray-900">
                            Ludwig Syntax
                        </dt>
                        <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                            <p class="flex-auto">Elegant, Python-inspired syntax that's easy to learn and powerful to use.</p>
                        </dd>
                    </div>
                    <div class="flex flex-col">
                        <dt class="text-base font-semibold leading-7 text-gray-900">
                            Laravel-Inspired
                        </dt>
                        <dd class="mt-1 flex flex-auto flex-col text-base leading-7 text-gray-600">
                            <p class="flex-auto">Familiar patterns from Laravel adapted for modern web development.</p>
                        </dd>
                    </div>
                </dl>
            </div>
        </div>
    </section>
</div>'''
        
        with open(os.path.join(views_dir, "home.html"), "w") as f:
            f.write(home_template)
        
        # Create components directory
        components_dir = os.path.join(project_path, "components")
        os.makedirs(components_dir, exist_ok=True)
        
        # Create UI components file
        ui_components_content = f'''# {project_name} - UI Components
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# shadcn/ui components for Ludwig

# Import Ludwig Web Framework
# let UIComponent = import("web_framework.UIComponentGenerator")

# Custom components for {project_name}
let AppComponents = create components do
    
    # Hero section component
    let hero = create component do
        # let title = props.title or "Welcome"
        # let subtitle = props.subtitle or "A Ludwig application"
        # let cta_text = props.cta_text or "Get Started"
        # let cta_link = props.cta_link or "#"
        
        # return UIComponent.hero({{
        #     "title": title,
        #     "subtitle": subtitle, 
        #     "cta_text": cta_text,
        #     "cta_link": cta_link
        # }})
    
    # Features grid component
    let features_grid = create component do
        # let features = props.features or []
        
        # return UIComponent.features_grid({{
        #     "features": features
        # }})
    
    # Stat card component
    let stat_card = create component do
        # let title = props.title or "Stat"
        # let value = props.value or "0"
        # let change = props.change or "+0%"
        
        # return UIComponent.stat_card({{
        #     "title": title,
        #     "value": value,
        #     "change": change
        # }})
    
    # Navigation component
    let navigation = create component do
        # let brand = props.brand or "{project_name}"
        # let items = props.items or []
        
        # return UIComponent.navigation({{
        #     "brand": brand,
        #     "items": items
        # }})
    
    # Dashboard layout
    let dashboard_layout = create component do
        # let title = props.title or "Dashboard"
        # let stats = props.stats or []
        # let nav_items = props.nav_items or []
        
        # return UIComponent.dashboard_layout({{
        #     "title": title,
        #     "stats": stats,
        #     "nav_items": nav_items
        # }})

# Form components
let FormComponents = create form_components do
    
    # Login form
    let login_form = create form do
        # let fields = [
        #     {{"type": "email", "name": "email", "label": "Email", "required": true}},
        #     {{"type": "password", "name": "password", "label": "Password", "required": true}}
        # ]
        
        # return UIComponent.form({{
        #     "title": "Sign In",
        #     "fields": fields,
        #     "submit_text": "Sign In"
        # }})
    
    # Registration form
    let register_form = create form do
        # let fields = [
        #     {{"type": "text", "name": "name", "label": "Full Name", "required": true}},
        #     {{"type": "email", "name": "email", "label": "Email", "required": true}},
        #     {{"type": "password", "name": "password", "label": "Password", "required": true}},
        #     {{"type": "password", "name": "password_confirmation", "label": "Confirm Password", "required": true}}
        # ]
        
        # return UIComponent.form({{
        #     "title": "Create Account",
        #     "fields": fields,
        #     "submit_text": "Create Account"
        # }})

# Data display components
let DataComponents = create data_components do
    
    # User table
    let user_table = create table do
        # let users = props.users or []
        
        # let headers = ["ID", "Name", "Email", "Created", "Actions"]
        # let rows = users.map(lambda user: [
        #     user.id,
        #     user.name,
        #     user.email,
        #     user.created_at,
        #     UIComponent.button({{"text": "Edit", "variant": "outline", "size": "sm"}}) +
        #     UIComponent.button({{"text": "Delete", "variant": "destructive", "size": "sm"}})
        # ])
        
        # return UIComponent.table({{
        #     "headers": headers,
        #     "rows": rows
        # }})
'''
        
        with open(os.path.join(components_dir, "ui_components.ludwig"), "w") as f:
            f.write(ui_components_content)
        
        # Create public directory for static files
        public_dir = os.path.join(project_path, "public")
        os.makedirs(public_dir, exist_ok=True)
        
        # Create CSS file with custom styles
        css_content = '''/* Custom styles for Ludwig web app */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
    font-family: 'Inter', sans-serif;
}

/* Custom component styles */
.ludwig-hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.ludwig-card {
    transition: transform 0.2s ease-in-out;
}

.ludwig-card:hover {
    transform: translateY(-2px);
}

/* Animation utilities */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.slide-in {
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { transform: translateX(-100%); }
    to { transform: translateX(0); }
}'''
        
        with open(os.path.join(public_dir, "styles.css"), "w") as f:
            f.write(css_content)
        
        # Create basic project structure first
        basic_template = BasicProjectTemplate()
        basic_template.create(project_name, path)
        
        # Update the ludwig.json to reflect modern web project
        config_path = os.path.join(project_path, "ludwig.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        
        config["type"] = "web"
        config["main"] = "app.ludwig"
        config["features"] = ["routing", "middleware", "controllers", "tailwindcss", "shadcn-ui", "components"]
        config["dependencies"] = {
            "tailwindcss": "^3.4.0",
            "shadcn-ui": "latest"
        }
        config["scripts"] = {
            "dev": "python artisan.py serve",
            "build": "python artisan.py build",
            "start": "python app.ludwig"
        }
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        return project_path


class DesktopProjectTemplate(ProjectTemplate):
    """Desktop application template with modern UI framework."""
    
    def __init__(self):
        super().__init__(
            "desktop",
            "Cross-platform desktop application with modern UI framework"
        )
    
    def create(self, project_name, path="."):
        """Create a desktop application project."""
        project_path = os.path.join(path, project_name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create main application file
        main_content = f'''# {project_name} - Desktop Application
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# Import Ludwig Desktop Framework
# let Desktop = import("desktop_framework")

# Application configuration
let app_config = {{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "Modern desktop application built with Ludwig",
    "author": "Your Name",
    "window_title": "{project_name}",
    "window_width": 1000,
    "window_height": 700,
    "resizable": true,
    "center_on_screen": true
}}

# Services configuration
let services_config = {{
    "database": {{
        "enabled": true,
        "type": "sqlite",
        "path": "data.db"
    }},
    "logging": {{
        "enabled": true,
        "level": "info",
        "file": "app.log"
    }},
    "settings": {{
        "enabled": true,
        "file": "settings.json"
    }}
}}

# Create the main application
let app = create desktop_app do
    let name = app_config.name
    let version = app_config.version

# Create main window
let main_window = create window do
    let title = app_config.window_title
    let width = app_config.window_width
    let height = app_config.window_height
    let resizable = app_config.resizable

# Application menu
let app_menu = create menu do
    
    let file_menu = create menu_item do
        let text = "File"
        let items = [
            {{"text": "New", "shortcut": "Ctrl+N", "action": "file_new"}},
            {{"text": "Open", "shortcut": "Ctrl+O", "action": "file_open"}},
            {{"text": "Save", "shortcut": "Ctrl+S", "action": "file_save"}},
            {{"separator": true}},
            {{"text": "Exit", "shortcut": "Ctrl+Q", "action": "app_exit"}}
        ]
    
    let edit_menu = create menu_item do
        let text = "Edit"
        let items = [
            {{"text": "Copy", "shortcut": "Ctrl+C", "action": "edit_copy"}},
            {{"text": "Paste", "shortcut": "Ctrl+V", "action": "edit_paste"}},
            {{"text": "Clear", "shortcut": "Delete", "action": "edit_clear"}}
        ]
    
    let help_menu = create menu_item do
        let text = "Help"
        let items = [
            {{"text": "About", "action": "help_about"}}
        ]

# Main UI layout
let main_layout = create border_layout do
    
    # Top toolbar
    let toolbar = create toolbar do
        let items = [
            Desktop.button({{"text": "New", "icon": "plus", "tooltip": "Create new item"}}),
            Desktop.button({{"text": "Open", "icon": "folder", "tooltip": "Open file"}}),
            Desktop.button({{"text": "Save", "icon": "save", "tooltip": "Save current work"}}),
            {{"separator": true}},
            Desktop.button({{"text": "Settings", "icon": "cog", "tooltip": "Application settings"}})
        ]
    
    # Left sidebar
    let sidebar = create sidebar do
        let width = 250
        let items = [
            {{"text": "Dashboard", "icon": "home", "selected": true}},
            {{"text": "Projects", "icon": "folder"}},
            {{"text": "Reports", "icon": "chart"}},
            {{"text": "Settings", "icon": "cog"}}
        ]
    
    # Main content area
    let content_area = create panel do
        let background_color = "#F8FAFC"
        let padding = 20
        
        # Content will be dynamically loaded based on sidebar selection
    
    # Bottom status bar
    let status_bar = create status_bar do
        let items = [
            {{"text": "Ready", "icon": "check"}},
            {{"text": "Version " + app_config.version}},
            {{"text": "Ludwig Desktop Framework"}}
        ]

# Add layouts to main layout
main_layout.add("top", toolbar)
main_layout.add("left", sidebar)
main_layout.add("center", content_area)
main_layout.add("bottom", status_bar)

# Set main window layout
main_window.set_layout(main_layout)
main_window.set_menu(app_menu)

# Dashboard content (default view)
let dashboard_content = create dashboard do
    
    # Welcome section
    let welcome_section = create section do
        let title = "Welcome to " + app_config.name
        let content = [
            Desktop.label({{"text": "Your modern desktop application is ready!", "font_size": 16}}),
            Desktop.label({{"text": "Built with Ludwig Desktop Framework", "font_size": 12, "color": "#6B7280"}})
        ]
    
    # Quick actions
    let quick_actions = create section do
        let title = "Quick Actions"
        let content = [
            Desktop.button({{"text": "Create New Project", "style": "primary", "width": 200}}),
            Desktop.button({{"text": "Import Data", "style": "secondary", "width": 200}}),
            Desktop.button({{"text": "View Reports", "style": "outline", "width": 200}})
        ]
    
    # Recent activity
    let recent_activity = create section do
        let title = "Recent Activity"
        let activity_list = Desktop.listview()
        activity_list.add_column("Activity", 300)
        activity_list.add_column("Date", 150)
        activity_list.add_item(["Application started", get_current_date()])
        
        let content = [activity_list]
    
    # Statistics cards
    let stats_section = create section do
        let title = "Statistics"
        let stats_grid = create grid_layout do
            let rows = 2
            let columns = 2
        
        let stats_cards = [
            Desktop.stat_card({{"title": "Total Items", "value": "0", "color": "#10B981"}}),
            Desktop.stat_card({{"title": "Completed", "value": "0", "color": "#3B82F6"}}),
            Desktop.stat_card({{"title": "In Progress", "value": "0", "color": "#F59E0B"}}),
            Desktop.stat_card({{"title": "Success Rate", "value": "100%", "color": "#8B5CF6"}})
        ]
        
        for card in stats_cards do
            stats_grid.add_control(card)
        
        let content = [stats_grid]

# Event handlers
let event_handlers = create handlers do
    
    # Menu actions
    let on_file_new = create handler do
        # Handle new file creation
        show_notification("Info", "New file created")
    
    let on_file_open = create handler do
        # Handle file opening
        let file_service = app.get_service("FileService")
        # Show file dialog and open selected file
    
    let on_file_save = create handler do
        # Handle file saving
        show_notification("Success", "File saved successfully")
    
    let on_app_exit = create handler do
        # Handle application exit
        save_application_state()
        app.close()
    
    # Sidebar navigation
    let on_sidebar_item_click = create handler do
        # let item = parameter
        
        if item.text == "Dashboard" do
            load_dashboard_content()
        else if item.text == "Projects" do
            load_projects_content()
        else if item.text == "Reports" do
            load_reports_content()
        else if item.text == "Settings" do
            load_settings_content()
    
    # Window events
    let on_window_closing = create handler do
        save_application_state()
        
    let on_window_resize = create handler do
        # Handle window resize
        adjust_layout()

# Content loading functions
let load_dashboard_content = create function do
    content_area.clear()
    content_area.add_content(dashboard_content)

let load_projects_content = create function do
    content_area.clear()
    
    let projects_view = create projects_panel do
        let toolbar = [
            Desktop.button({{"text": "New Project", "style": "primary"}}),
            Desktop.button({{"text": "Import", "style": "secondary"}}),
            Desktop.button({{"text": "Export", "style": "outline"}})
        ]
        
        let projects_grid = Desktop.data_grid()
        projects_grid.add_column("Name", 200)
        projects_grid.add_column("Status", 100)
        projects_grid.add_column("Created", 120)
        projects_grid.add_column("Actions", 100)
    
    content_area.add_content(projects_view)

let load_reports_content = create function do
    content_area.clear()
    
    let reports_view = create reports_panel do
        let chart_area = Desktop.chart({{"type": "line", "width": 600, "height": 300}})
        let report_filters = [
            Desktop.combobox({{"items": ["Last 7 days", "Last 30 days", "Last 3 months"]}}),
            Desktop.button({{"text": "Generate Report", "style": "primary"}})
        ]
    
    content_area.add_content(reports_view)

let load_settings_content = create function do
    content_area.clear()
    
    let settings_view = create settings_panel do
        let settings_form = [
            Desktop.label("Application Settings"),
            Desktop.textbox({{"label": "App Name", "value": app_config.name}}),
            Desktop.checkbox({{"label": "Enable notifications", "checked": true}}),
            Desktop.checkbox({{"label": "Auto-save", "checked": false}}),
            Desktop.button({{"text": "Save Settings", "style": "primary"}})
        ]
    
    content_area.add_content(settings_view)

# Application services
let application_services = create services do
    
    # Data service for application data
    let data_service = create service do
        let name = "DataService"
        
        let save_data = create method do
            # Save application data
        
        let load_data = create method do
            # Load application data
    
    # Settings service
    let settings_service = create service do
        let name = "SettingsService"
        
        let save_settings = create method do
            # Save user settings
        
        let load_settings = create method do
            # Load user settings

# Utility functions
let show_notification = create function do
    # let type = parameter[0]
    # let message = parameter[1]
    
    let notification_service = app.get_service("NotificationService")
    
    if type == "Success" do
        notification_service.show_info("Success", message)
    else if type == "Error" do
        notification_service.show_error("Error", message)
    else do
        notification_service.show_info("Info", message)

let save_application_state = create function do
    let state = {{
        "window_position": main_window.get_position(),
        "window_size": main_window.get_size(),
        "last_used": get_current_timestamp()
    }}
    
    let file_service = app.get_service("FileService")
    file_service.write_text("app_state.json", json_stringify(state))

let load_application_state = create function do
    let file_service = app.get_service("FileService")
    
    if file_service.exists("app_state.json") do
        let state_data = file_service.read_text("app_state.json")
        let state = json_parse(state_data)
        
        # Restore window position and size
        main_window.set_position(state.window_position)
        main_window.set_size(state.window_size)

let get_current_date = create function do
    # return new Date().toLocaleDateString()

let get_current_timestamp = create function do
    # return new Date().toISOString()

let json_stringify = create function do
    # let data = parameter
    # return JSON.stringify(data)

let json_parse = create function do
    # let json_string = parameter
    # return JSON.parse(json_string)

let adjust_layout = create function do
    # Adjust layout based on window size
    if main_window.width < 800 do
        sidebar.hide()
    else do
        sidebar.show()

# Application initialization
let initialize_application = create function do
    # Load application state
    load_application_state()
    
    # Load initial content
    load_dashboard_content()
    
    # Initialize services
    initialize_services()
    
    # Show welcome notification
    show_notification("Info", "Welcome to " + app_config.name + "!")

let initialize_services = create function do
    # Initialize application services
    app.add_service("DataService", application_services.data_service)
    app.add_service("SettingsService", application_services.settings_service)

# Main application entry point
let main = create function do
    # Initialize the application
    initialize_application()
    
    # Add main window to application
    app.add_window(main_window)
    
    # Bind event handlers
    bind_event_handlers()
    
    # Start the application
    app.run()

let bind_event_handlers = create function do
    # Bind all event handlers
    main_window.on("closing", on_window_closing)
    main_window.on("resize", on_window_resize)
    
    # Menu handlers would be bound here
    # Toolbar handlers would be bound here
    # Sidebar handlers would be bound here

# Run the application
main()
'''
        
        with open(os.path.join(project_path, "main.ludwig"), "w") as f:
            f.write(main_content)
        
        # Create app.ludwig file
        app_content = f'''# {project_name} Application Entry Point
# This file contains the main application logic

# Import the main application
# let main_app = import("main")

# Application metadata
let app_info = {{
    "name": "{project_name}",
    "version": "1.0.0",
    "description": "Desktop application built with Ludwig",
    "framework": "Ludwig Desktop Framework",
    "created": "{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}"
}}

# Start the application
# main_app.main()
'''
        
        with open(os.path.join(project_path, "app.ludwig"), "w") as f:
            f.write(app_content)
        
        # Create ludwig.json configuration
        config = {
            "name": project_name,
            "version": "1.0.0",
            "type": "desktop",
            "framework": "Ludwig Desktop Framework",
            "entry_point": "main.ludwig",
            "dependencies": {
                "ludwig_desktop": "^1.0.0"
            },
            "build": {
                "target": "desktop",
                "platforms": ["windows", "macos", "linux"],
                "output_dir": "dist"
            },
            "app": {
                "title": project_name,
                "width": 1000,
                "height": 700,
                "resizable": True,
                "center": True
            }
        }
        
        with open(os.path.join(project_path, "ludwig.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        # Create directories
        directories = ["forms", "services", "assets", "data", "lib", "tests"]
        for directory in directories:
            os.makedirs(os.path.join(project_path, directory), exist_ok=True)
        
        # Create sample service
        sample_service_content = '''# SampleService - Example desktop service
# Generated for demonstration

let SampleService = create service do
    let name = "SampleService"
    
    let process_data = create method do
        # Process application data
        return "Data processed successfully"
    
    let get_statistics = create method do
        return {
            "total_operations": 0,
            "success_rate": 100
        }
'''
        
        with open(os.path.join(project_path, "services", "sample_service.ludwig"), "w") as f:
            f.write(sample_service_content)
        
        # Create sample form
        sample_form_content = '''# SampleForm - Example desktop form
# Generated for demonstration

let SampleForm = create form do
    let title = "Sample Form"
    let width = 400
    let height = 300
    
    # Form controls would be defined here
'''
        
        with open(os.path.join(project_path, "forms", "sample_form.ludwig"), "w") as f:
            f.write(sample_form_content)
        
        # Create README
        readme_content = f'''# {project_name}

Desktop application built with Ludwig Desktop Framework.

## Features

- Modern cross-platform UI
- Built-in services (File, Database, HTTP, Notifications)
- Event-driven architecture
- Responsive layout system
- Menu and toolbar support

## Getting Started

### Run the Application
```bash
python artisan.py run main.ludwig
```

### Generate New Components
```bash
# Generate a new form
python artisan.py make:form UserProfile

# Generate a new service  
python artisan.py make:service DataProcessor

# Generate a new desktop app
python artisan.py make:desktop MyNewApp
```

## Project Structure

- `main.ludwig` - Main application file
- `app.ludwig` - Application entry point
- `forms/` - UI forms and dialogs
- `services/` - Application services
- `assets/` - Images, icons, and other assets
- `data/` - Application data files
- `lib/` - Utility libraries
- `tests/` - Test files

## Development

This application uses the Ludwig Desktop Framework, which provides:

- **UI Controls**: Buttons, labels, text boxes, list views, etc.
- **Layouts**: Stack, grid, border layouts for organizing UI
- **Services**: File operations, database access, HTTP requests
- **Events**: Click handlers, window events, keyboard shortcuts
- **Notifications**: System notifications and alerts

## Building

To build for production:
```bash
python artisan.py build
```

This will create distributable packages for Windows, macOS, and Linux.
'''
        
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(readme_content)
        
        return project_path


class CLIProjectTemplate(ProjectTemplate):
    """Command-line application template."""
    
    def __init__(self):
        super().__init__(
            "cli",
            "A command-line application template with argument parsing"
        )
    
    def create(self, project_name, path="."):
        """Create a CLI application project."""
        project_path = os.path.join(path, project_name)
        
        # Create basic project first
        basic_template = BasicProjectTemplate()
        basic_template.create(project_name, path)
        
        # Create CLI-specific main file
        cli_content = f'''# {project_name} - Command Line Tool
# Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# CLI application setup
let app_name = "{project_name}"
let version = "1.0.0"

# Command definitions
let commands = create commands do
    # help -> show_help
    # version -> show_version
    # run -> run_command

# Command handlers
let show_help = create command do
    let help_text = "Usage: " + app_name + " [command] [options]"
    # Display help information

let show_version = create command do
    let version_text = app_name + " version " + version
    # Display version information

let run_command = create command do
    # let options = parse_arguments()
    # Main application logic here

# Argument parser
let parse_arguments = create function do
    # Parse command line arguments
    # Return parsed options

# Main entry point
let main = create function do
    # let args = get_command_line_args()
    # let command = args[0] or "help"
    # execute_command(command, args)
'''
        
        with open(os.path.join(project_path, "cli.ludwig"), "w") as f:
            f.write(cli_content)
        
        # Update configuration
        config_path = os.path.join(project_path, "ludwig.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        
        config["type"] = "cli"
        config["main"] = "cli.ludwig"
        config["features"] = ["argument_parsing", "commands"]
        
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        
        return project_path


class ProjectGenerator:
    """Main project generator class."""
    
    def __init__(self):
        """Initialize the project generator."""
        self.templates = {
            "basic": BasicProjectTemplate(),
            "web": WebProjectTemplate(),
            "desktop": DesktopProjectTemplate(),
            # "embedded": EmbeddedProjectTemplate(),  # Removed because not implemented
            "cli": CLIProjectTemplate(),
        }
    
    def list_templates(self):
        """List available project templates."""
        print("Available project templates:")
        for name, template in self.templates.items():
            print(f"  {name:<10} - {template.description}")
    
    def create_project(self, template_name, project_name, path="."):
        """
        Create a new project from a template.
        
        Args:
            template_name (str): Template to use
            project_name (str): Name of the new project
            path (str): Path where to create the project
            
        Returns:
            str: Path to created project
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        project_path = template.create(project_name, path)
        
        print(f"Project '{project_name}' created successfully!")
        print(f"Location: {project_path}")
        print(f"Template: {template_name}")
        
        return project_path


# Example usage
if __name__ == "__main__":
    generator = ProjectGenerator()
    generator.list_templates()
    
    # Example: Create a basic project
    # generator.create_project("basic", "my_ludwig_app")
