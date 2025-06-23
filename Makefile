# Ludwig Programming Language Makefile

.PHONY: help install install-dev test lint format clean run-tests

help: ## Show this help message
	@echo "Ludwig Programming Language - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Ludwig in development mode
	pip install -e .

install-dev: ## Install with development dependencies
	pip install -e .
	pip install -r requirements-dev.txt

test: ## Run tests
	python -m pytest tests/ -v

lint: ## Run linting
	flake8 src/
	mypy src/

format: ## Format code
	black src/
	black bin/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Build distribution packages
	python setup.py sdist bdist_wheel

# Quick commands for common tasks
shell: ## Start Ludwig interactive shell
	./bin/ludwig-shell

create-web: ## Create a sample web project
	./bin/ludwig-setup sample_web web

create-desktop: ## Create a sample desktop project
	./bin/ludwig-setup sample_desktop desktop

# Development commands
run-examples: ## Run example applications
	@echo "Running desktop calculator example..."
	python src/cli/artisan.py run examples/desktop/mycalculator_app.ludwig

dev-setup: install-dev ## Complete development setup
	@echo "Ludwig development environment ready!"
	@echo "Try: make shell"
	@echo "Or:  make create-web"
