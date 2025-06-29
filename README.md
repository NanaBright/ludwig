<p align="center">
  <img src="https://raw.githubusercontent.com/NanaBright/ludwig/main/assets/logo.png" alt="Ludwig Logo" width="160"/>
</p>

<h1 align="center">Ludwig ⚙️</h1>
<p align="center">A complete modern development platform for Web, Desktop, and Embedded systems.</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-yellow.svg" alt="MIT License"></a>
  <a href="https://github.com/NanaBright/ludwig"><img src="https://img.shields.io/github/downloads/NanaBright/ludwig/total?style=flat&logo=github&color=brightgreen" alt="Total Downloads"></a>
  <a href="https://github.com/NanaBright/ludwig/network/members"><img src="https://img.shields.io/github/forks/NanaBright/ludwig?style=flat&logo=github&color=blue" alt="Forks"></a>
  <a href="https://github.com/NanaBright/ludwig/stargazers"><img src="https://img.shields.io/github/stars/NanaBright/ludwig?style=flat&logo=github&color=yellow" alt="Stars"></a>
  <a href="SECURITY.md"><img src="https://img.shields.io/badge/security-policy-red?style=flat&logo=shield" alt="Security Policy"></a>
  <a href="#"><img src="https://img.shields.io/badge/platform-web%20%7C%20desktop%20%7C%20embedded-blue" alt="Platform Support"></a>
  <a href="#"><img src="https://img.shields.io/badge/made%20with-%E2%9D%A4-red" alt="Made with Love"></a>
</p>

---

## 🚀 Overview

**Ludwig** combines the elegance of Python-inspired syntax with the power of Laravel, .NET, and Arduino — enabling developers to build:

- 🧱 Full-stack **Web** applications
- 🖥️ Cross-platform **Desktop** software
- 📟 **Embedded & IoT** firmware and systems
- 🛠️ Unified CLI with intelligent scaffolding
- ✨ Built-in ORM, Auth, Validation, UI Components, and REPL

> **"Write once, deploy anywhere — with elegance."**

---

## 📸 Demo

> 📽️ *[Coming Soon]* — Watch Ludwig build a full-stack blog, a smart kiosk, and a calculator app in seconds.

---

## ✨ Features

### 🌐 Web Development
- **Native Web Framework**: Pure Python HTTP server - no Flask/Django required  
- **Zero Dependencies**: Built-in routing, templating, and static file serving
- **TailwindCSS Integration**: Modern responsive UI out of the box
- **REST API Support**: JSON responses and API generation
- **Component System**: Reusable UI components with `make:component`

### 🖥️ Desktop Development
- C#-inspired cross-platform GUI apps
- Forms, toolbars, file/database services
- Layout managers: Grid, Stack, Border
- System notifications and tray support

### 🔌 Embedded & IoT
- Templates for Arduino, RPi, ESP32
- Hardware abstraction: Sensors, Actuators
- POS, Kiosk, Smart Home & Robotics generators
- WiFi, Bluetooth, Cloud-ready

### 🛠️ CLI & Tooling
- **Native Web Framework**: Pure Python - no Flask/Django required
- **Artisan CLI**: `artisan.py` for project creation and scaffolding
- **Component Generation**: Controllers, components, embedded systems
- **Zero Dependencies**: Built-in HTTP server and templating
- **Hot Reload**: Instant development feedback

---

## 🏁 Quick Start

```bash
git clone https://github.com/NanaBright/ludwig.git
cd ludwig
pip install -r requirements.txt  # Optional dev dependencies only
```

**👉 [Get Started Now](docs/GETTING_STARTED.md) - Complete setup guide with examples**

#### Web
```bash
python artisan.py new my_blog web
cd my_blog
python main.ludwig
```

#### Desktop
```bash
python artisan.py make:desktop my_app
python myapp_app.ludwig
```

#### Embedded
```bash
python artisan.py make:embedded MyDevice
#### Embedded
```bash
python artisan.py make:embedded MyDevice
python mydevice_embedded.ludwig
```

---

## 📁 Project Structure

```
ludwig/
├── web_framework.py          # Native web framework (no Flask!)
├── artisan.py               # CLI for project generation
├── create_project.py        # Project scaffolding utility
├── src/
│   ├── frameworks/          # Framework implementations
│   ├── cli/                # Command-line tools
│   └── templates/          # Project templates
├── examples/               # Example projects
│   ├── web/               # Web application examples
│   ├── desktop/           # Desktop app examples  
│   └── embedded/          # IoT/embedded examples
└── docs/                  # Documentation
```

---

## 📦 Used By

- 🔹 `modern_blog/` – Blog system with auth and comments
- 🔹 `MyTextEditor` – Desktop text editing app
- 🔹 `RetailScanner` – IoT barcode inventory tool
- 🔹 `SmartHomeBot` – Connected home control system

---

## 🗺️ Roadmap

- [x] Web: ORM, Auth, REST, Validation, UI
- [x] Desktop: GUI framework, Forms, Services
- [x] Embedded: POS, Kiosk, Smart Home templates
- [ ] AI/ML Support (Edge AI, Model Inference)
- [ ] VSCode Syntax Plugin
- [ ] Package Manager (`lpm install`)
- [ ] Online Playground
- [ ] Ludwig Cloud (Web-hosted IDE + deploy)

---

## 🧠 Why Ludwig?

| For           | Benefit |
|---------------|---------|
| **Web Developers** | No Flask/Django setup - pure Python web framework |
| **Laravel Devs**  | Familiar Artisan CLI + MVC architecture |
| **Python Devs**   | Zero dependencies, pure Python implementation |
| **IoT Builders**  | Generate firmware with readable syntax |
| **Beginners**     | One command creates working applications |
| **Teams**         | Unified platform for web, desktop, and embedded |

---

## 📚 Documentation

- **[🚀 Getting Started](docs/GETTING_STARTED.md)** - Quick setup and first projects
- [Complete Guide](docs/COMPLETE_GUIDE.md) - Comprehensive feature documentation
- [Desktop Quickstart](docs/DESKTOP_QUICKSTART.md) - Desktop development guide
- [Embedded Guide](docs/EMBEDDED_GUIDE.md) - IoT and embedded systems
- [Integration Summary](docs/INTEGRATION_COMPLETE.md) - Technical overview

---

## 🤝 Contributing

We welcome contributions from developers of all skill levels! Ludwig is built by the community, for the community.

### 🚀 Quick Start for Contributors

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/ludwig.git
cd ludwig

# 2. Set up development environment  
pip install -r requirements-dev.txt

# 3. Create feature branch
git checkout -b feature/amazing-feature

# 4. Make changes & test
python tests/test_embedded_integration.py
python demo.py

# 5. Submit Pull Request
git push origin feature/amazing-feature
```

### 🎯 Ways to Contribute

| Type | Examples | Skills Needed |
|------|----------|---------------|
| 🐛 **Bug Fixes** | Fix framework issues, CLI bugs | Python, debugging |
| ✨ **Features** | New sensors, UI components, CLI commands | Python, domain knowledge |
| 📚 **Documentation** | Guides, examples, API docs | Technical writing |
| 🧪 **Testing** | Unit tests, integration tests | Python testing |
| 🌍 **Translation** | Multi-language support | Language skills |

### 📋 Contribution Areas

- **🌐 Web Framework**: Laravel-style features, ORM, Auth
- **🖥️ Desktop Framework**: GUI components, cross-platform features
- **🔌 Embedded Framework**: IoT sensors, robotics, connectivity  
- **🛠️ CLI Tools**: Code generation, project templates
- **📖 Examples**: Real-world applications, tutorials

### 📚 Detailed Guide

👉 **See [CONTRIBUTING.md](CONTRIBUTING.md) for:**
- Development setup
- Code standards
- Testing guidelines
- Architecture overview
- Release process

### 🏆 Recognition

Contributors are recognized in:
- README contributor list
- Release notes
- Community shoutouts
- Ludwig swag program

**Every contribution matters - from typo fixes to major features!**

---

## 🙏 Contributors

Ludwig is built by an amazing community of developers! See our [Contributors](CONTRIBUTORS.md) page for a full list.

### 🏆 Special Thanks
- **Core Team**: Building the platform foundations
- **Community**: Feature requests, bug reports, and feedback  
- **Documentation**: Improving guides and examples
- **Testers**: Ensuring quality across all platforms

**Want to join them?** Check out our [Contributing Guide](CONTRIBUTING.md)!

---

## 📄 License & Policies

Ludwig is licensed under the **MIT License** — see [LICENSE](LICENSE).

- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines and standards
- **[Security Policy](SECURITY.md)** - Vulnerability reporting and security practices
- **[Contributing Guide](CONTRIBUTING.md)** - How to contribute to Ludwig

---

## 💡 Final Note

Ludwig makes **modern development joyful**.  
No matter where your code runs — browser, desktop, or device — Ludwig brings power, simplicity, and speed.

> **Ludwig: Write less. Build more. Deploy anywhere.**
