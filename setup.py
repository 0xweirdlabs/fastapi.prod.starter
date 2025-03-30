"""
Setup script for the FastAPI backend template.
This provides compatibility with older tooling while still using
pyproject.toml as the primary build configuration.
"""
from setuptools import setup

# This setup.py is kept minimal and exists primarily for compatibility
setup(
    name="fastapi-backend",
    version="0.1.0",
    packages=["app"],
)
