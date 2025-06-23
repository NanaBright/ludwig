"""
Ludwig Configuration System

Laravel-inspired configuration management for Ludwig projects.
Provides a centralized way to manage application settings.
"""

import json
import os
from pathlib import Path


class Config:
    """
    Configuration manager for Ludwig applications.
    
    Provides a centralized way to manage application configuration
    with support for environment-specific settings and nested values.
    
    Example usage:
        config = Config()
        app_name = config.get('app.name', 'Ludwig App')
        debug_mode = config.get('app.debug', False)
        config.set('database.host', 'localhost')
    """
    
    def __init__(self, config_path="ludwig.json"):
        """
        Initialize configuration manager.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config_path = config_path
        self.config_data = {}
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.config_data = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {self.config_path}: {e}")
                self.config_data = {}
        else:
            # Create default configuration
            self.config_data = self.get_default_config()
            self.save()
    
    def save(self):
        """Save configuration to file."""
        try:
            # Ensure directory exists
            config_dir = os.path.dirname(self.config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config_data, f, indent=2)
        except IOError as e:
            print(f"Error saving config file: {e}")
    
    def get(self, key, default=None):
        """
        Get a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'app.name')
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        Set a configuration value using dot notation.
        
        Args:
            key (str): Configuration key (e.g., 'app.name')
            value: Value to set
        """
        keys = key.split('.')
        current = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        
        # Set the final value
        current[keys[-1]] = value
        self.save()
    
    def has(self, key):
        """
        Check if a configuration key exists.
        
        Args:
            key (str): Configuration key
            
        Returns:
            bool: True if key exists
        """
        return self.get(key) is not None
    
    def remove(self, key):
        """
        Remove a configuration key.
        
        Args:
            key (str): Configuration key to remove
        """
        keys = key.split('.')
        current = self.config_data
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                return  # Key doesn't exist
        
        # Remove the final key
        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
            self.save()
    
    def all(self):
        """
        Get all configuration data.
        
        Returns:
            dict: All configuration data
        """
        return self.config_data.copy()
    
    def merge(self, data):
        """
        Merge configuration data.
        
        Args:
            data (dict): Data to merge
        """
        self._deep_merge(self.config_data, data)
        self.save()
    
    def _deep_merge(self, base, update):
        """Recursively merge dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get_default_config(self):
        """
        Get default configuration structure.
        
        Returns:
            dict: Default configuration
        """
        return {
            "name": "Ludwig App",
            "version": "1.0.0",
            "description": "A Ludwig programming language application",
            "main": "main.ludwig",
            "ludwig_version": "0.1.0-alpha",
            "app": {
                "name": "Ludwig App",
                "version": "1.0.0",
                "debug": False,
                "environment": "development"
            },
            "database": {
                "driver": "file",
                "host": "localhost",
                "port": 5432,
                "name": "ludwig_db",
                "username": "",
                "password": ""
            },
            "cache": {
                "driver": "memory",
                "ttl": 3600
            },
            "logging": {
                "level": "info",
                "file": "ludwig.log"
            },
            "features": []
        }


class Environment:
    """
    Environment-specific configuration management.
    
    Handles loading configuration based on the current environment
    (development, testing, production, etc.).
    """
    
    def __init__(self, env_name="development"):
        """
        Initialize environment configuration.
        
        Args:
            env_name (str): Environment name
        """
        self.env_name = env_name
        self.config = Config()
    
    def load_env_config(self):
        """Load environment-specific configuration."""
        env_config_path = f"config/{self.env_name}.json"
        
        if os.path.exists(env_config_path):
            try:
                with open(env_config_path, 'r') as f:
                    env_data = json.load(f)
                self.config.merge(env_data)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load environment config: {e}")
    
    def is_development(self):
        """Check if running in development environment."""
        return self.env_name == "development"
    
    def is_production(self):
        """Check if running in production environment."""
        return self.env_name == "production"
    
    def is_testing(self):
        """Check if running in testing environment."""
        return self.env_name == "testing"


# Global configuration instance
_config = None


def config(key=None, default=None):
    """
    Global configuration function.
    
    Args:
        key (str): Configuration key
        default: Default value
        
    Returns:
        Configuration value or Config instance
    """
    global _config
    
    if _config is None:
        _config = Config()
    
    if key is None:
        return _config
    
    return _config.get(key, default)


def set_config(key, value):
    """
    Set a global configuration value.
    
    Args:
        key (str): Configuration key
        value: Value to set
    """
    global _config
    
    if _config is None:
        _config = Config()
    
    _config.set(key, value)


# Example usage and testing
if __name__ == "__main__":
    # Test configuration system
    config_manager = Config()
    
    # Set some values
    config_manager.set('app.name', 'Test Ludwig App')
    config_manager.set('app.debug', True)
    config_manager.set('database.host', 'localhost')
    config_manager.set('database.port', 5432)
    
    # Get values
    print("App name:", config_manager.get('app.name'))
    print("Debug mode:", config_manager.get('app.debug'))
    print("Database host:", config_manager.get('database.host'))
    print("Non-existent key:", config_manager.get('non.existent', 'default_value'))
    
    # Test global function
    print("Global config app name:", config('app.name'))
    set_config('app.version', '2.0.0')
    print("Updated version:", config('app.version'))
