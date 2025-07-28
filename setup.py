#!/usr/bin/env python3
"""Setup script for ClickHouse MCP Server."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="clickhouse-mcp-server",
        version="0.1.0",
        description="MCP server for ClickHouse database connections",
        author="Your Name",
        author_email="your.email@example.com",
        packages=find_packages(),
        install_requires=[
            "mcp>=1.0.0",
            "clickhouse-connect>=0.7.0",
            "pydantic>=2.0.0",
            "typing-extensions>=4.0.0",
        ],
        extras_require={
            "dev": [
                "pytest>=7.0.0",
                "black>=23.0.0",
                "isort>=5.0.0",
                "mypy>=1.0.0",
            ]
        },
        entry_points={
            "console_scripts": [
                "clickhouse-mcp-server=clickhouse_mcp_server.main:main",
            ],
        },
        python_requires=">=3.8",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
    ) 