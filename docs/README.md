# Ludwig Programming Language

Ludwig is a modern development platform that combines Python-inspired syntax with Laravel-style features for building both web applications and desktop applications. Designed to be simple, elegant, and developer-friendly.

## Features

- **Simple Syntax**: Python-like syntax that's easy to learn
- **Interactive REPL**: Test code quickly with the built-in shell
- **Web Framework**: Laravel-inspired web development with APIs, authentication, and database ORM
- **Desktop Framework**: C#/.NET-inspired cross-platform desktop application development
- **Type System**: Support for integers, floats, booleans, and variables
- **Control Flow**: If/elif/else statements and while loops
- **Artisan-Style CLI**: Command-line tools for scaffolding and development

## Quick Start

### Option 1: Create a New Project (Recommended)

**Web Application:**
```bash
# Create a complete web app with authentication and database
python ludwig_setup.py my_blog web

# Navigate to project
cd my_blog

# Start development server
python artisan.py dev
```

**Desktop Application:**
```bash
# Create a modern desktop app
python ludwig_setup.py my_app desktop

# Navigate to project  
cd my_app

# Run the desktop app
python artisan.py run main.ludwig
```

**Simple Project:**
```bash
# Create a basic Ludwig project
python artisan.py new my_app

# Navigate to project
cd my_app

# Start the interactive shell
python artisan.py serve
```

### Option 3: Use the Interactive Shell Directly

```bash
python shell.py
```

### Option 2: Generate Code Files

**Web Development:**
```bash
# Generate complete API with model and controller
python artisan.py make:api products --model

# Generate authentication controller
python artisan.py make:auth

# Generate custom controller
python artisan.py make:controller UserController
```

**Desktop Development:**
```bash
# Generate desktop application
python artisan.py make:desktop Calculator

# Generate UI form
python artisan.py make:form UserProfile

# Generate background service
python artisan.py make:service DataProcessor
```

**General Development:**
```bash
# Generate a function
python artisan.py make:function calculate

# Generate a class
python artisan.py make:class User

# Generate a test
python artisan.py make:test UserTest
```

### Basic Syntax

```ludwig
# Variables and basic operations
name = "Ludwig"
age = 25
score = 95.5
is_active = true

# Control flow
if age >= 18:
    print("Adult")
else:
    print("Minor")

# Functions
function greet(name):
    return "Hello, " + name
end

result = greet("World")
print(result)
```

### Web Development Example

```bash
# Create a complete blog application
python ludwig_setup.py my_blog web
cd my_blog

# Generated structure includes:
# - User authentication (JWT)
# - User and Post models with database
# - RESTful API endpoints
# - Modern UI with TailwindCSS
# - Input validation
```

### Desktop Development Example

```bash
# Create a desktop application
python ludwig_setup.py calculator_app desktop
cd calculator_app

# Generated structure includes:
# - Cross-platform GUI framework
# - Modern UI controls (buttons, forms, etc.)
# - Built-in services (file, database, HTTP)
# - Event-driven architecture
# - Menu and toolbar support
```

**Desktop App Sample Code:**
```ludwig
# main.ludwig - Simple calculator app
app = DesktopApp("Calculator", "1.0.0")
window = app.create_window("Calculator", 400, 300)

# Add controls
display = window.add_control(TextBox("display"))
display.set_size(360, 40)
display.set_position(20, 20)

# Add calculator buttons
button1 = window.add_control(Button("1", "number_clicked"))
button1.set_size(60, 40)
button1.set_position(20, 80)

# Event handler
function number_clicked(sender):
    display.set_text(display.get_text() + sender.text)
end

# Run the application
app.run()
```
# Variable declaration
let name = "Ludwig"
let age = 25
let pi = 3.14

# Arithmetic operations
let result = 10 + 5 * 2

# Comparisons
let is_adult = age >= 18

# Control flow
if age >= 18 do
    let status = "adult"
elif age >= 13 do
    let status = "teen"
else do
    let status = "child"

# Loops
let counter = 0
while counter < 5 do
    let counter = counter + 1
```

## Language Grammar

### Variables
- Declaration keywords: `let`, `create`, `start`
- Example: `let variable_name = value`

### Data Types
- **Integers**: `42`, `-10`
- **Floats**: `3.14`, `-2.5`
- **Booleans**: `and`, `or`, `not`

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`
- **Comparison**: `>`, `<`, `>=`, `<=`, `?=` (equals)
- **Logical**: `and`, `or`, `not`

### Control Flow
- **Conditionals**: `if`, `elif`, `else`
- **Loops**: `while`
- **Keywords**: `do` (required for block execution)

## Architecture

Ludwig follows a traditional interpreter architecture:

1. **Lexer** (`lexer.py`) - Converts source code into tokens
2. **Parser** (`parse.py`) - Builds an Abstract Syntax Tree (AST)
3. **Interpreter** (`interpreter.py`) - Executes the AST
4. **Data Store** (`data.py`) - Manages variable storage
5. **Shell** (`shell.py`) - Interactive REPL interface

## Ludwig Features

Ludwig brings modern development capabilities to both web and desktop applications:

### ✅ Currently Available

- **🎨 Artisan CLI**: Laravel-style command-line tools
  ```bash
  # Web development
  python artisan.py make:api products --model  # Generate complete API
  python artisan.py make:auth                   # Generate authentication
  
  # Desktop development  
  python artisan.py make:desktop Calculator     # Generate desktop app
  python artisan.py make:form UserProfile      # Generate UI form
  python artisan.py make:service DataProcessor # Generate service
  
  # General development
  python artisan.py new my_app          # Create new project
  python artisan.py make:function calc  # Generate function
  python artisan.py make:class User     # Generate class
  python artisan.py serve               # Start REPL
  ```

- **🌐 Web Framework**: Complete web development platform
  ```bash
  # One command creates full-stack web app
  python ludwig_setup.py my_blog web
  # Includes: Authentication, Database ORM, RESTful APIs, Modern UI
  ```

- **�️ Desktop Framework**: Cross-platform desktop application development
  ```bash
  # One command creates desktop app
  python ludwig_setup.py my_app desktop
  # Includes: Modern UI, Services, Event handling, System integration
  ```

- **�📋 Collections**: Fluent data manipulation
  ```python
  from ludwig_collections import collect
  numbers = collect([1, 2, 3, 4, 5])
  result = numbers.map(lambda x: x * 2).filter(lambda x: x > 4)
  ```

- **✅ Validation**: Data validation system
  ```python
  from validation import validate
  result = validate(data, {
      'name': ['required', 'string', 'min:2'],
      'age': ['required', 'integer', 'between:18,100']
  })
  ```

- **⚙️ Configuration**: Centralized config management
  ```python
  from config import config, set_config
  app_name = config('app.name', 'Ludwig App')
  set_config('database.host', 'localhost')
  ```

- **📁 Project Templates**: Scaffolding for different project types
  - `web`: Full-stack web applications with authentication and database
  - `desktop`: Cross-platform desktop applications with modern UI
  - `cli`: Command-line application tools
  - `basic`: Simple Ludwig application for learning

### � Advanced Features

- **Database ORM**: Laravel Eloquent-inspired database operations
- **JWT Authentication**: Secure user authentication for web apps
- **RESTful APIs**: Auto-generated CRUD endpoints
- **Modern UI Components**: TailwindCSS + shadcn/ui for web
- **Cross-Platform Desktop**: Native-like desktop apps on Windows, Mac, Linux
- **Service Architecture**: Built-in services for file, database, HTTP operations
- **Event-Driven Programming**: Modern event handling for desktop applications

## Contributing

Ludwig is open source! Contributions are welcome.

## License

MIT License - see LICENSE file for details.
