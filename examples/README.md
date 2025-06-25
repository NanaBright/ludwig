# Ludwig Examples

This directory contains example applications and components demonstrating Ludwig's capabilities.

## 📁 Directory Structure

### Web Examples (`web/`)
- `test_auto_setup/` - Complete web application with authentication, posts, and users
- `blogcontroller.ludwig` - Sample blog controller with CRUD operations
- `dashboard_page.ludwig` - Dashboard page component

### Desktop Examples (`desktop/`)
- **Complete Projects:**
  - `MyDashboard/` - Full-featured dashboard application
  - `MyDesktopApp/` - Complete desktop app with services
  - `SimpleDemo/` - Basic demo application
  - `TextEditor/` - Text editor implementation
- **Individual Examples:**
  - `mycalculator_app.ludwig` - Simple calculator desktop application
  - `mydesktopapp_app.ludwig` - Basic desktop app template
  - `userprofile_form.ludwig` - User profile form with validation
  - `dataprocessor_service.ludwig` - Background data processing service
  - `simplenotepad_app.ludwig` - Simple notepad application
  - `todoapp_app.ludwig` - Todo list application

### Embedded Examples (`embedded/`)
- **IoT Systems:** Complete embedded device examples
- **POS Systems:** Point of sale implementations
- **Smart Home:** Home automation examples
- **Robotics:** Robot control systems
- See `embedded/README.md` for detailed documentation

### Components (`components/`)
- `blogcard_component.ludwig` - Reusable blog card component

### Other Examples
- `calculate_average.ludwig` - Simple function example
- `demo.ludwig` - Basic Ludwig syntax demonstration
- `test_project/` - Minimal project structure
- `showcase.html` - HTML showcase file

## 🚀 Running Examples

### Web Examples
```bash
cd web/test_auto_setup
python artisan.py dev
```

### Desktop Examples
```bash
python artisan.py run desktop/mycalculator_app.ludwig
```

### Basic Examples
```bash
python shell.py
# Then load any .ludwig file
```

## 📚 Learning

These examples demonstrate:
- **Web Development**: Controllers, authentication, database models
- **Desktop Development**: GUI applications, forms, services
- **Ludwig Syntax**: Functions, classes, control flow
- **Project Structure**: How to organize Ludwig projects

Use these as starting points for your own Ludwig applications!
