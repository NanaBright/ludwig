#!/usr/bin/env python3
"""
Ludwig Platform Demonstration

This script demonstrates Ludwig's complete development platform capabilities:
- Web Development (Laravel-inspired)
- Desktop Development (C#/.NET-inspired) 
- Embedded Systems (Arduino/RPi-inspired)
"""

import subprocess
import sys
import os
import time

def run_command(command, description=""):
    """Run a command with nice output."""
    print(f"\n🔧 {description}")
    print(f"💻 Running: {command}")
    print("-" * 50)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout)
        print("✅ Success!")
    else:
        print(f"❌ Error: {result.stderr}")
    
    return result.returncode == 0

def demo_web_development():
    """Demonstrate web development capabilities."""
    print("\n🌐 LUDWIG WEB DEVELOPMENT")
    print("=" * 60)
    print("Laravel-inspired full-stack web applications")
    print("✨ Features: Authentication, Database, Modern UI, APIs")
    
    # Show available web commands
    run_command("python bin/ludwig help | grep -A 10 'make:api'", 
                "Available web development commands")

def demo_desktop_development():
    """Demonstrate desktop development capabilities."""
    print("\n🖥️  LUDWIG DESKTOP DEVELOPMENT") 
    print("=" * 60)
    print("C#/.NET-inspired cross-platform desktop applications")
    print("✨ Features: Modern GUI, Services, Event-driven, Cross-platform")
    
    # Show available desktop commands
    run_command("python bin/ludwig help | grep -A 5 'make:desktop'",
                "Available desktop development commands")

def demo_embedded_development():
    """Demonstrate embedded development capabilities."""
    print("\n🔌 LUDWIG EMBEDDED SYSTEMS DEVELOPMENT")
    print("=" * 60) 
    print("Arduino/Raspberry Pi-inspired IoT and embedded applications")
    print("✨ Features: Hardware abstraction, Sensors, IoT, Robotics")
    
    # Show available embedded commands
    run_command("python bin/ludwig help | grep -A 8 'make:embedded'",
                "Available embedded development commands")

def demo_code_generation():
    """Demonstrate rapid code generation."""
    print("\n⚡ RAPID CODE GENERATION DEMO")
    print("=" * 60)
    
    # Generate examples of each type
    examples = [
        ("make:embedded IoTSensor", "IoT sensor application"),
        ("make:pos CoffeeShop", "Point of Sale system"),
        ("make:smarthome MyHouse", "Smart home controller"),
        ("make:robotics CleanBot", "Cleaning robot system")
    ]
    
    for command, description in examples:
        run_command(f"python bin/ludwig {command}", f"Generate {description}")
        time.sleep(1)
    
    # Show generated files
    run_command("ls -la *_*.ludwig | head -10", "Generated application files")

def demo_platform_stats():
    """Show platform statistics."""
    print("\n📊 LUDWIG PLATFORM STATISTICS")
    print("=" * 60)
    
    # Count files by type
    stats = [
        ("find src/frameworks -name '*.py' | wc -l", "Framework files"),
        ("find examples -name '*.ludwig' | wc -l", "Example applications"), 
        ("find docs -name '*.md' | wc -l", "Documentation files"),
        ("python bin/ludwig help | grep 'make:' | wc -l", "CLI commands"),
    ]
    
    for command, description in stats:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        count = result.stdout.strip()
        print(f"  📈 {description}: {count}")

def main():
    """Run the complete Ludwig platform demonstration."""
    print("🎉 LUDWIG DEVELOPMENT PLATFORM DEMONSTRATION")
    print("=" * 80)
    print("A complete modern development platform for web, desktop, and embedded!")
    print("🚀 From simple syntax to full applications in seconds")
    
    # Check if we're in the right directory
    if not os.path.exists("bin/ludwig"):
        print("❌ Please run this demo from the Ludwig root directory")
        sys.exit(1)
    
    # Demo each platform capability
    demo_web_development()
    demo_desktop_development() 
    demo_embedded_development()
    demo_code_generation()
    demo_platform_stats()
    
    print("\n🎯 PLATFORM SUMMARY")
    print("=" * 60)
    print("✅ Web Development - Laravel-inspired, full-stack, modern UI")
    print("✅ Desktop Development - C#/.NET-inspired, cross-platform GUI") 
    print("✅ Embedded Systems - Arduino/RPi-inspired, IoT and robotics")
    print("✅ Developer Tools - Artisan CLI, templates, one-command setup")
    print("✅ Documentation - Comprehensive guides and examples")
    
    print("\n🚀 GET STARTED")
    print("=" * 60)
    print("# Web app:      python ludwig_setup.py my_blog web")
    print("# Desktop app:  python ludwig_setup.py my_app desktop") 
    print("# IoT device:   python bin/ludwig make:embedded my_device")
    print("# Smart home:   python bin/ludwig make:smarthome my_home")
    
    print("\n🎉 Ludwig makes building applications as easy as writing Python!")
    print("   Try it now and build your next project in minutes! ⚡")

if __name__ == "__main__":
    main()
