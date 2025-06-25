<p align="center">
  <img src="https://raw.githubusercontent.com/NanaBright/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="120"/>
</p>

# Contributing to Ludwig 🚀

Thank you for your interest in contributing to Ludwig! This guide will help you get started with contributing to our modern development platform.

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Search existing issues first
- Use our bug report template
- Include reproduction steps
- Provide system information

### ✨ Feature Requests
- Check the roadmap first
- Use our feature request template
- Explain the use case clearly
- Consider implementation complexity

### 📝 Documentation
- Fix typos and improve clarity
- Add examples and tutorials
- Translate documentation
- Update API references

### 💻 Code Contributions
- Framework improvements
- New CLI commands
- Example applications
- Test coverage
- Performance optimizations

---

## 🛠️ Development Setup

### Prerequisites
```bash
# Required
Python 3.8+
Git

# Optional (for testing)
Node.js 16+ (for web examples)
.NET 6+ (for desktop testing)
Arduino IDE (for embedded examples)
```

### Getting Started
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/ludwig.git
cd ludwig

# 3. Set up remote upstream
git remote add upstream https://github.com/NanaBright/ludwig.git

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Verify installation
python bin/ludwig help
python tests/test_embedded_integration.py
```

---

## 🏗️ Project Architecture

### Core Components
```
ludwig/
├── src/
│   ├── frameworks/           # Platform frameworks
│   │   ├── web_framework.py     # Laravel-inspired web
│   │   ├── desktop_framework.py # .NET-inspired desktop
│   │   └── embedded_framework.py # Arduino-inspired IoT
│   ├── cli/                  # Command-line tools
│   │   └── artisan.py           # Code generation CLI
│   ├── core/                 # Language implementation
│   │   ├── lexer.py, parse.py, interpreter.py
│   │   └── data.py, tokens.py
│   └── utils/                # Shared utilities
│       ├── database.py, auth.py, validation.py
│       └── templates.py, ludwig_collections.py
├── examples/                 # Sample applications
│   ├── web/, desktop/, embedded/
├── docs/                     # Documentation
├── tests/                    # Test suite
└── bin/                      # Executables
```

### Key Design Principles
1. **Simplicity**: Python-like syntax, intuitive APIs
2. **Consistency**: Same patterns across web/desktop/embedded
3. **Developer Experience**: One-command setup, hot reload, helpful errors
4. **Modularity**: Clean separation between frameworks
5. **Extensibility**: Easy to add new commands and templates

---

## 🔄 Development Workflow

### Branch Strategy
```bash
# Main branches
main          # Stable release code
develop       # Integration branch
feature/*     # New features
bugfix/*      # Bug fixes
hotfix/*      # Critical fixes
docs/*        # Documentation updates
```

### Making Changes
```bash
# 1. Update your fork
git checkout main
git pull upstream main

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make your changes
# ... code, test, document ...

# 4. Test thoroughly
python tests/test_embedded_integration.py
python demo.py

# 5. Commit with conventional commits
git add .
git commit -m "feat: add amazing new feature"

# 6. Push to your fork
git push origin feature/amazing-feature

# 7. Open a Pull Request
```

### Conventional Commits
We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add new embedded sensor support
fix: resolve desktop layout issue
docs: update contributing guide
test: add integration tests for CLI
refactor: improve code organization
style: fix code formatting
chore: update dependencies
```

---

## 🧪 Testing Guidelines

### Test Categories
1. **Unit Tests**: Individual component testing
2. **Integration Tests**: Cross-component testing
3. **CLI Tests**: Command-line interface testing
4. **Example Tests**: Sample application validation

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python tests/test_embedded_integration.py

# Test CLI commands
python bin/ludwig help
python bin/ludwig make:embedded TestDevice

# Test examples
cd examples/embedded
python testiot_embedded.ludwig
```

### Writing Tests
```python
# Example test structure
def test_embedded_sensor():
    """Test embedded sensor functionality."""
    import sys
    sys.path.append('src/frameworks')
    import embedded_framework as ef
    
    sensor = ef.TemperatureSensor()
    assert sensor.name == "temperature"
    
    reading = sensor.read_value()
    assert isinstance(reading, float)
    assert -40 <= reading <= 85  # Valid temp range
```

### Test Requirements
- All new features must include tests
- Aim for 80%+ code coverage
- Test both success and error cases
- Include integration tests for CLI commands

---

## 📋 Code Standards

### Python Style
```python
# Follow PEP 8 with these specifics:
# - Line length: 88 characters (Black default)
# - Use type hints where possible
# - Docstrings for all public functions/classes
# - Import organization: stdlib, third-party, local

# Example function
def create_embedded_device(name: str, config: Dict[str, Any]) -> EmbeddedDevice:
    """Create a new embedded device with configuration.
    
    Args:
        name: Device name
        config: Device configuration dictionary
        
    Returns:
        Configured EmbeddedDevice instance
        
    Raises:
        ValueError: If name is empty or config is invalid
    """
    if not name:
        raise ValueError("Device name cannot be empty")
    
    device = EmbeddedDevice(name)
    device.configure(config)
    return device
```

### Ludwig Language Style
```ludwig
# Use consistent indentation (4 spaces)
# Clear variable names
# Comments for complex logic

function process_sensor_data(sensor_data):
    # Validate sensor readings
    if sensor_data.temperature < -40 or sensor_data.temperature > 85:
        throw ValueError("Temperature out of range")
    end
    
    # Process the data
    normalized_temp = normalize_temperature(sensor_data.temperature)
    return normalized_temp
end
```

### Documentation Style
```markdown
# Use clear headings and structure
# Include code examples
# Link to related documentation
# Keep examples up-to-date

## Function Name

Brief description of what the function does.

### Parameters
- `param1` (type): Description
- `param2` (type): Description

### Returns
- `return_type`: Description

### Example
\`\`\`ludwig
result = function_name(param1, param2)
\`\`\`
```

---

## 📚 Contribution Areas

### 🌐 Web Framework
**Skills needed**: Python, Laravel knowledge, web development

**Opportunities**:
- Add new middleware types
- Improve ORM functionality
- Create UI component library
- Add testing utilities
- Enhance authentication system

### 🖥️ Desktop Framework
**Skills needed**: Python, GUI development, .NET knowledge

**Opportunities**:
- Add new layout managers
- Improve cross-platform compatibility
- Create desktop widgets
- Add system integration features
- Enhance event handling

### 🔌 Embedded Framework
**Skills needed**: Python, Arduino/RPi, IoT development

**Opportunities**:
- Add new sensor types
- Create hardware drivers
- Improve connectivity options
- Add edge AI capabilities
- Create robotics templates

### 🛠️ CLI & Tooling
**Skills needed**: Python, CLI development, code generation

**Opportunities**:
- Add new artisan commands
- Improve code generation templates
- Create VS Code extension
- Add package manager
- Enhance developer tools

### 📖 Documentation
**Skills needed**: Technical writing, markdown

**Opportunities**:
- Create video tutorials
- Write platform-specific guides
- Translate documentation
- Add API reference
- Create cookbook examples

### 🧪 Testing & QA
**Skills needed**: Python testing, automation

**Opportunities**:
- Add unit tests
- Create end-to-end tests
- Improve CI/CD pipeline
- Add performance benchmarks
- Create testing utilities

---

## 🎯 Specific Contribution Tasks

### Good First Issues
- [ ] Add temperature sensor calibration
- [ ] Create Ludwig syntax highlighter
- [ ] Add more CLI command examples
- [ ] Improve error messages
- [ ] Add configuration validation

### Medium Complexity
- [ ] Create package manager (`lpm`)
- [ ] Add database migration rollback
- [ ] Implement OAuth providers
- [ ] Add desktop theme support
- [ ] Create IoT device simulator

### Advanced Features
- [ ] Add edge AI/ML support
- [ ] Create Ludwig Cloud platform
- [ ] Build online IDE/playground
- [ ] Add multi-language support
- [ ] Create visual designer tools

---

## 🚀 Release Process

### Version Strategy
We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features, backward compatible
- Patch: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] Release notes prepared
- [ ] Examples tested
- [ ] Breaking changes documented

---

## 📞 Getting Help

### Communication Channels
- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: General questions, ideas
- **Discord**: Real-time chat (coming soon)
- **Email**: maintainers@ludwig-platform.com

### Asking Questions
1. Search existing issues/discussions first
2. Use descriptive titles
3. Provide context and examples
4. Include system information
5. Be respectful and patient

### Mentorship
New contributors can request mentorship:
- Tag `@maintainers` in issues
- Join our contributor onboarding sessions
- Pair program with experienced contributors

---

## 🏆 Recognition

### Contributor Levels
- **First-time**: First contribution merged
- **Regular**: 5+ contributions merged
- **Core**: Trusted with review privileges
- **Maintainer**: Repository maintenance access

### Recognition
- Contributors listed in README
- Shoutouts in release notes
- Contributor spotlight blog posts
- Ludwig swag for significant contributions

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment:

### Our Pledge
- Be respectful and inclusive
- Welcome newcomers
- Value diverse perspectives
- Focus on constructive feedback
- Help others learn and grow

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or inflammatory comments
- Publishing private information
- Disruptive behavior
- Spam or off-topic content

### Enforcement
Report violations to: conduct@ludwig-platform.com

---

## 🎉 Thank You!

Every contribution makes Ludwig better! Whether you:
- Fix a typo
- Report a bug
- Add a feature
- Help other users
- Spread the word

**You're helping build the future of development platforms!**

> **Together, we're making modern development joyful for everyone.** 🚀✨

---

*Last updated: June 2025*
*This guide is itself a living document - please help improve it!*
