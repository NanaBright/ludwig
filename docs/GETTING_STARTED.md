<p align="center">
  <img src="https://raw.githubusercontent.com/NanaBright/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="120"/>
</p>

# Getting Started with Ludwig 🚀

Welcome to Ludwig! This guide will help you get up and running quickly with our modern development platform for Web, Desktop, and Embedded systems.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Your First Ludwig Project](#your-first-ludwig-project)
4. [Web Development](#web-development)
5. [Desktop Applications](#desktop-applications)
6. [Embedded/IoT Systems](#embeddediot-systems)
7. [CLI Commands Reference](#cli-commands-reference)
8. [Next Steps](#next-steps)

---

## Prerequisites

Before getting started with Ludwig, make sure you have:

- **Python 3.9+** installed on your system
- **Git** for version control
- A code editor (VS Code recommended)
- Terminal/Command prompt access

### System Requirements

| Platform | Requirements |
|----------|-------------|
| **Windows** | Windows 10+ with Python 3.9+ |
| **macOS** | macOS 10.15+ with Python 3.9+ |
| **Linux** | Ubuntu 20.04+ or equivalent with Python 3.9+ |

---

## Installation

### Option 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/NanaBright/ludwig.git
cd ludwig

# Install dependencies
pip install -r requirements.txt

# Verify installation
python artisan.py version
```

### Option 2: Quick Download

```bash
# Download and extract
wget https://github.com/NanaBright/ludwig/archive/main.zip
unzip main.zip
cd ludwig-main

# Install dependencies
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check Ludwig CLI
python artisan.py help

# Test framework imports
python -c "import ludwig_collections; print('✅ Ludwig ready!')"
```

---

## Your First Ludwig Project

Let's create your first Ludwig project! Choose your platform:

### 🌐 Web Project

```bash
# Create a new web project
python ludwig_setup.py my_blog web
cd my_blog

# Start development
python artisan.py dev
```

### 🖥️ Desktop Project

```bash
# Create a desktop application
python ludwig_setup.py my_app desktop
cd my_app

# Run the application
python artisan.py run main.ludwig
```

### 🔌 Embedded Project

```bash
# Create an IoT device
python artisan.py make:embedded MyDevice

# Run the embedded application
python mydevice_embedded.ludwig
```

---

## Web Development

Ludwig provides Laravel-inspired features for modern web development.

### Creating a Blog Application

```bash
# 1. Create project
python ludwig_setup.py blog web
cd blog

# 2. Generate components
python artisan.py make:controller PostController
python artisan.py make:component BlogCard
python artisan.py make:page Dashboard

# 3. Set up authentication
python artisan.py make:auth

# 4. Start development server
python artisan.py dev
```

### Available Web Commands

| Command | Description |
|---------|-------------|
| `make:controller <name>` | Create a web controller |
| `make:component <name>` | Create a UI component |
| `make:page <name>` | Create a complete page |
| `make:api <name>` | Generate REST API |
| `make:middleware <name>` | Create middleware |

### Features Included

- ✅ **TailwindCSS** for styling
- ✅ **shadcn/ui** components
- ✅ **JWT Authentication**
- ✅ **Form validation**
- ✅ **Database ORM**
- ✅ **REST API generation**

---

## Desktop Applications

Build cross-platform desktop applications with Ludwig's C#-inspired framework.

### Creating a Text Editor

```bash
# 1. Create desktop app
python artisan.py make:desktop TextEditor

# 2. Add forms and services
python artisan.py make:form MainWindow
python artisan.py make:service FileService

# 3. Run the application
python texteditor_app.ludwig
```

### Desktop Features

- 🪟 **Cross-platform GUI**
- 📝 **Forms and controls**
- 🗃️ **File and database services**
- 🔔 **System notifications**
- 🎨 **Layout managers**

### Example Controls

```ludwig
# Create a text editor window
let main_window = create window do
    let title = "Ludwig Text Editor"
    let width = 800
    let height = 600

# Add controls
let text_area = Desktop.textbox({
    "multiline": true,
    "scrollbars": true
})

let menu_bar = Desktop.menubar({
    "File": ["New", "Open", "Save", "Exit"],
    "Edit": ["Cut", "Copy", "Paste"],
    "Help": ["About"]
})
```

---

## Embedded/IoT Systems

Ludwig makes embedded development accessible with hardware abstraction and pre-built templates.

### Quick Start Examples

#### IoT Sensor Device
```bash
python artisan.py make:embedded WeatherStation
```

#### Point of Sale System
```bash
python artisan.py make:pos RetailPOS
```

#### Smart Home Controller
```bash
python artisan.py make:smarthome HomeController
```

#### Robotics System
```bash
python artisan.py make:robotics CleaningBot
```

### Supported Hardware

| Category | Examples |
|----------|----------|
| **Microcontrollers** | Arduino, ESP32, Raspberry Pi |
| **Sensors** | Temperature, Motion, Ultrasonic |
| **Displays** | LCD, OLED, TouchScreen |
| **Communication** | WiFi, Bluetooth, Serial |
| **Actuators** | Motors, Servos, LEDs |

### Example IoT Code

```ludwig
import embedded_framework as Embedded

# Create device
device = Embedded.EmbeddedDevice("WeatherStation", "1.0.0")

# Add sensors
device.add_sensor("temp", Embedded.TemperatureSensor(pin=A0))
device.add_sensor("humidity", Embedded.HumiditySensor(pin=A1))

# Add connectivity
device.add_service("wifi", Embedded.WiFiService())
device.add_service("cloud", Embedded.CloudService())

function main():
    device.initialize()
    
    while device.is_running():
        temp = device.get_sensor("temp").read()
        humidity = device.get_sensor("humidity").read()
        
        device.get_service("cloud").send_data({
            "temperature": temp,
            "humidity": humidity,
            "timestamp": get_timestamp()
        })
        
        device.sleep(60000)  # Send every minute
end
```

---

## CLI Commands Reference

Ludwig's Artisan CLI provides powerful code generation and project management.

### Project Management
```bash
python artisan.py new <name> [template]    # Create new project
python artisan.py templates                # List available templates
python artisan.py version                  # Show version
python artisan.py help                     # Show all commands
```

### Web Development
```bash
python artisan.py make:controller <name>   # Web controller
python artisan.py make:component <name>    # UI component
python artisan.py make:page <name>         # Complete page
python artisan.py make:api <name>          # REST API
python artisan.py make:middleware <name>   # Middleware
python artisan.py dev                      # Start dev server
```

### Desktop Development
```bash
python artisan.py make:desktop <name>      # Desktop app
python artisan.py make:form <name>         # UI form
python artisan.py make:service <name>      # App service
```

### Embedded Development
```bash
python artisan.py make:embedded <name>     # IoT device
python artisan.py make:pos <name>          # POS system
python artisan.py make:kiosk <name>        # QR kiosk
python artisan.py make:scanner <name>      # Barcode scanner
python artisan.py make:smarthome <name>    # Smart home
python artisan.py make:robotics <name>     # Robot controller
```

### Utility Commands
```bash
python artisan.py make:class <name>        # Class file
python artisan.py make:function <name>     # Function file
python artisan.py make:test <name>         # Test file
python artisan.py serve                    # Start REPL
python artisan.py run <file>               # Execute file
```

---

## Next Steps

### 📚 Learn More

- **[Complete Guide](COMPLETE_GUIDE.md)** - Comprehensive feature documentation
- **[Embedded Guide](EMBEDDED_GUIDE.md)** - IoT and embedded development
- **[Desktop Quickstart](DESKTOP_QUICKSTART.md)** - Desktop application development
- **[Examples](../examples/)** - Real-world project examples

### 🛠️ Development

- **[Contributing Guide](../CONTRIBUTING.md)** - How to contribute to Ludwig
- **[Architecture Overview](DEVELOPMENT_SUMMARY.md)** - Technical deep-dive
- **[API Reference](PROJECT_STRUCTURE.md)** - Code structure and APIs

### 💬 Community

- **GitHub Issues** - Bug reports and feature requests
- **Discussions** - Community help and questions
- **Contributors** - See our amazing [contributors](../CONTRIBUTORS.md)

### 🎯 Project Ideas

#### Beginner Projects
- **Personal Blog** - Web development with auth and content management
- **Todo App** - Desktop application with local storage
- **Temperature Monitor** - IoT sensor with data logging

#### Intermediate Projects
- **E-commerce Site** - Full-stack web app with payments
- **Media Player** - Desktop app with file management
- **Smart Garden** - IoT system with automated watering

#### Advanced Projects
- **Social Platform** - Scalable web application
- **IDE/Editor** - Complex desktop application
- **Home Automation** - Complete IoT ecosystem

---

## 🆘 Getting Help

### Common Issues

#### Import Errors
```bash
# If you see import errors, check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -r requirements.txt
```

#### CLI Not Working
```bash
# Verify Ludwig installation
python artisan.py version

# Check file permissions
ls -la artisan.py
```

#### Embedded Development
```bash
# Install additional dependencies for embedded
pip install pyserial
pip install requests  # For cloud services
```

### Support Channels

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/NanaBright/ludwig/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/NanaBright/ludwig/discussions)
- 📖 **Documentation**: [Ludwig Docs](README.md)
- 🤝 **Contributing**: [Contribution Guide](../CONTRIBUTING.md)

---

## 🎉 Welcome to Ludwig!

You're now ready to build amazing applications with Ludwig! Whether you're creating web applications, desktop software, or IoT devices, Ludwig provides the tools and frameworks you need.

**Happy coding!** 🚀

---

<p align="center">
  <strong>Ludwig: Write less. Build more. Deploy anywhere.</strong>
</p>

<p align="center">
  <a href="../README.md">← Back to Main README</a> |
  <a href="COMPLETE_GUIDE.md">Complete Guide →</a>
</p>
