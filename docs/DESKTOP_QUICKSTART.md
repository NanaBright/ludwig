# 🚀 Quick Start Guide - Desktop Apps

This guide shows how easy it is to create desktop applications with Ludwig, inspired by the simplicity of C# and .NET.

## 📱 Create Your First Desktop App (30 seconds)

### Option 1: Complete Desktop Project
```bash
# Create a complete desktop application project
python ludwig_setup.py MyTextEditor desktop

# Navigate to the project
cd MyTextEditor

# Run the application
python artisan.py run main.ludwig
```

**What you get:**
- ✅ Cross-platform desktop app structure
- ✅ Modern UI controls (buttons, forms, text boxes)
- ✅ Built-in services (file, database, HTTP, notifications)
- ✅ Event-driven architecture
- ✅ Menu and toolbar support
- ✅ Complete project structure with assets, data, and tests

### Option 2: Simple Desktop App File
```bash
# Generate a single desktop app file
python artisan.py make:desktop Calculator

# Run the app
python calculator_app.ludwig
```

## 📝 Sample Desktop App Code

**Simple Calculator App:**
```ludwig
# Import the desktop framework
import desktop_framework as Desktop

# Create the main application
app = Desktop.DesktopApp("Simple Calculator", "1.0.0")

# Create the main window
window = app.create_window("Calculator", 400, 300)

# Add a display text box
display = window.add_control(Desktop.TextBox("display"))
display.set_size(360, 40)
display.set_position(20, 20)
display.set_text("0")

# Add number buttons
buttons = []
for i in range(10):
    button = window.add_control(Desktop.Button(str(i), "number_clicked"))
    button.set_size(60, 40)
    
    # Position buttons in a grid
    row = (9 - i) // 3
    col = (9 - i) % 3
    x = 20 + col * 70
    y = 80 + row * 50
    button.set_position(x, y)

# Add operation buttons
plus_btn = window.add_control(Desktop.Button("+", "operation_clicked"))
plus_btn.set_size(60, 40)
plus_btn.set_position(300, 80)

equals_btn = window.add_control(Desktop.Button("=", "equals_clicked"))
equals_btn.set_size(60, 40)
equals_btn.set_position(300, 130)

clear_btn = window.add_control(Desktop.Button("C", "clear_clicked"))
clear_btn.set_size(60, 40)
clear_btn.set_position(300, 180)

# Event handlers
current_value = 0
operation = ""
new_input = true

function number_clicked(sender):
    global current_value, new_input
    if new_input:
        display.set_text(sender.text)
        new_input = false
    else:
        current_text = display.get_text()
        if current_text == "0":
            display.set_text(sender.text)
        else:
            display.set_text(current_text + sender.text)
        end
    end
end

function operation_clicked(sender):
    global current_value, operation, new_input
    current_value = float(display.get_text())
    operation = sender.text
    new_input = true
end

function equals_clicked(sender):
    global current_value, operation, new_input
    if operation == "+":
        result = current_value + float(display.get_text())
        display.set_text(str(result))
        new_input = true
    end
end

function clear_clicked(sender):
    global current_value, operation, new_input
    display.set_text("0")
    current_value = 0
    operation = ""
    new_input = true
end

# Run the application
app.run()
```

## 🛠️ Desktop Development Features

### Modern UI Controls
- **Button**: Clickable buttons with text and event handlers
- **TextBox**: Text input fields with validation
- **Label**: Static text displays
- **ListView**: Data grids and lists
- **MenuBar**: Application menus
- **StatusBar**: Status information

### Layout Management
- **StackLayout**: Vertical/horizontal stacking
- **GridLayout**: Grid-based positioning
- **BorderLayout**: Border-based arrangement
- **Custom positioning**: Manual control placement

### Built-in Services
- **FileService**: File operations (read, write, copy, delete)
- **DatabaseService**: SQLite database operations
- **HttpService**: Web requests and API calls
- **NotificationService**: System notifications
- **ConfigService**: Application configuration

### System Integration
- **Window management**: Multiple windows, dialogs
- **Event handling**: Click, keyboard, window events
- **Menu systems**: Application and context menus
- **Toolbar support**: Icon toolbars
- **System tray**: Background operation

## 🎯 Why Choose Ludwig for Desktop Apps?

### Simple & Modern
- **Clean Syntax**: Python-inspired, easy to read and write
- **C# Inspiration**: Familiar patterns for .NET developers
- **Modern Architecture**: Event-driven, service-oriented design

### Cross-Platform
- **Windows**: Native-like experience
- **macOS**: Mac-friendly applications
- **Linux**: GTK integration

### Developer Friendly
- **One Command Setup**: Get started in seconds
- **Code Generation**: Automatic form and service creation
- **Hot Reload**: Fast development iteration
- **Built-in Services**: No need to write boilerplate

### Production Ready
- **Error Handling**: Built-in exception management
- **Logging**: Integrated logging system
- **Configuration**: Environment-based config
- **Testing**: Test framework included

## 📚 Next Steps

1. **Try the Examples**: Check the `examples/desktop/` directory
2. **Generate Components**: Use `make:form` and `make:service`
3. **Explore Services**: Try file operations and HTTP requests
4. **Build Something Real**: Create your own desktop application!

Ludwig makes desktop development as simple as web development. Get started today! 🚀
