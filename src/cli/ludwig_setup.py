#!/usr/bin/env python3
"""
Ludwig Quick Setup

One-command setup script to create a Ludwig project with all fea        print("   ludwig dev          # Start development server")
        print("   ludwig components   # List available components")
        print("   ludwig make:api <n> --model  # Create new API resource")es enabled.
This script simplifies the entire process of getting started with Ludwig.

Usage:
    python ludwig_setup.py [project_name] [template]

Examples:
    python ludwig_setup.py my_blog web
    python ludwig_setup.py my_api web
    python ludwig_setup.py my_cli cli
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    """Print Ludwig banner."""
    print("""
    ██╗     ██╗   ██╗██████╗ ██╗    ██╗██╗ ██████╗ 
    ██║     ██║   ██║██╔══██╗██║    ██║██║██╔════╝ 
    ██║     ██║   ██║██║  ██║██║ █╗ ██║██║██║  ███╗
    ██║     ██║   ██║██║  ██║██║███╗██║██║██║   ██║
    ███████╗╚██████╔╝██████╔╝╚███╔███╔╝██║╚██████╔╝
    ╚══════╝ ╚═════╝ ╚═════╝  ╚══╝╚══╝ ╚═╝ ╚═════╝ 
    
    🚀 Ludwig Programming Language - Quick Setup
    Modern, Python-inspired web development made simple
    """)


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False


def setup_project(project_name, template="web"):
    """Set up a complete Ludwig project."""
    print_banner()
    
    print(f"🎯 Creating Ludwig project: {project_name}")
    print(f"📋 Template: {template}")
    print(f"📁 Location: {os.getcwd()}/{project_name}")
    print()
    
    # Get the Ludwig root directory (two levels up from this file)
    ludwig_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    ludwig_bin = os.path.join(ludwig_root, "bin", "ludwig")
    
    # Step 1: Create project
    if not run_command(f"python {ludwig_bin} new {project_name} {template}", 
                      f"Creating {template} project"):
        return False
    
    # Step 2: Change to project directory
    os.chdir(project_name)
    
    # Step 3: Generate API resources (for web projects)
    if template == "web":
        print()
        print("🔧 Setting up API resources...")
        
        # Generate User API with model
        run_command(f"python {ludwig_bin} make:api users --model",
                   "Creating User API with model")
        
        # Generate Posts API with model
        run_command(f"python {ludwig_bin} make:api posts --model", 
                   "Creating Posts API with model")
        
        # Generate authentication controller
        run_command(f"python {ludwig_bin} make:controller AuthController",
                   "Creating authentication controller")
        
        # Run migrations
        run_command(f"python {ludwig_bin} migrate",
                   "Running database migrations")
    
    # Step 4: Create sample components
    if template == "web":
        print()
        print("🎨 Creating UI components...")
        
        run_command(f"python {ludwig_bin} make:component Header",
                   "Creating Header component")
        
        run_command(f"python {ludwig_bin} make:component UserCard", 
                   "Creating UserCard component")
        
        run_command(f"python {ludwig_bin} make:component PostCard",
                   "Creating PostCard component")
    
    print()
    print("✅ Project setup complete!")
    print()
    print("🚀 Next steps:")
    print(f"   cd {project_name}")
    
    if template == "web":
        print("   python ../artisan.py dev          # Start development server")
        print("   python ../artisan.py components   # List available components")
        print("   python ../artisan.py make:api <name> --model  # Create new API resource")
    elif template == "cli":
        print("   ludwig run main.ludwig  # Run your CLI app")
    else:
        print("   ludwig serve        # Start Ludwig REPL")
    
    print()
    print("📚 Documentation:")
    print("   README.md                 # Project documentation")
    print("   DEVELOPMENT_SUMMARY.md    # Ludwig language features")
    print()
    print("🔗 Key features enabled:")
    print("   ✓ Modern web framework with TailwindCSS and shadcn/ui")
    print("   ✓ Database ORM with migrations")
    print("   ✓ JWT authentication system")
    print("   ✓ RESTful API endpoints")
    print("   ✓ Input validation")
    print("   ✓ Collection utilities")
    print("   ✓ Artisan CLI tools")
    
    return True


def interactive_setup():
    """Interactive setup mode."""
    print_banner()
    
    print("🎯 Welcome to Ludwig Quick Setup!")
    print()
    
    # Get project name
    while True:
        project_name = input("📝 Enter project name: ").strip()
        if project_name and project_name.replace('_', '').replace('-', '').isalnum():
            break
        print("❌ Invalid project name. Use letters, numbers, hyphens, and underscores only.")
    
    # Get template
    print()
    print("📋 Available templates:")
    print("   1. web     - Modern web application (TailwindCSS, API, auth)")
    print("   2. desktop - Cross-platform desktop application")
    print("   3. cli     - Command-line application")
    print("   4. basic   - Basic Ludwig project")
    print()
    
    while True:
        choice = input("🎨 Choose template (1-4) [1]: ").strip() or "1"
        templates = {"1": "web", "2": "desktop", "3": "cli", "4": "basic"}
        if choice in templates:
            template = templates[choice]
            break
        print("❌ Invalid choice. Enter 1, 2, 3, or 4.")
    
    return setup_project(project_name, template)


def show_help():
    """Show help information."""
    print(__doc__)
    print()
    print("Template Options:")
    print("   web    - Full-stack web application with database, auth, API")
    print("   cli    - Command-line application template")  
    print("   basic  - Basic Ludwig project structure")
    print()
    print("Features included in 'web' template:")
    print("   🎨 TailwindCSS + shadcn/ui components")
    print("   🗄️  SQLite database with ORM")
    print("   🔐 JWT authentication system")
    print("   🌐 RESTful API endpoints")
    print("   ✅ Input validation")
    print("   🚀 Development server")
    print("   🛠️  Artisan CLI tools")


def main():
    """Main entry point."""
    if len(sys.argv) == 1:
        # Interactive mode
        return interactive_setup()
    
    if len(sys.argv) >= 2 and sys.argv[1] in ['-h', '--help', 'help']:
        show_help()
        return True
    
    # Command line mode
    project_name = sys.argv[1] if len(sys.argv) >= 2 else None
    template = sys.argv[2] if len(sys.argv) >= 3 else "web"
    
    if not project_name:
        print("❌ Error: Project name is required")
        show_help()
        return False
    
    return setup_project(project_name, template)


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
