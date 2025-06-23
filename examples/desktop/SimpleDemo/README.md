# SimpleDemo

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
