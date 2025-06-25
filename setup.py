#!/usr/bin/env python3
"""
Ludwig Programming Language Setup Script
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename), encoding='utf-8') as f:
        return f.read()

setup(
    name="ludwig-lang",
    version="0.1.0",
    description="Modern multi-platform development framework for Web, Desktop, and Embedded/IoT systems",
    long_description=read_file("docs/README.md"),
    long_description_content_type="text/markdown",
    author="Ludwig Development Team",
    author_email="dev@ludwig-lang.org",
    url="https://github.com/ludwig-lang/ludwig",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        # Add any dependencies here
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    scripts=[
        "bin/ludwig",
        "bin/ludwig-shell", 
        "bin/ludwig-setup",
    ],
    entry_points={
        "console_scripts": [
            "ludwig=cli.artisan:main",
            "ludwig-shell=cli.shell:main",
            "ludwig-setup=cli.ludwig_setup:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Languages",
        "Topic :: Software Development :: Interpreters",
    ],
    keywords="programming-language web desktop framework",
    include_package_data=True,
    zip_safe=False,
)
