#!/usr/bin/env python3
from setuptools import setup, find_packages

required = [
    "apispec",
    "pymongo",
    "mongoengine",
    "Flask",
    "flask-cors",
    "flask-compress",
    "flask_mongoengine",
    "flask-smorest",
    "marshmallow",
    "marshmallow_enum",
    "colorlog",
    "gunicorn",
    "requests",
    "environs",
    "passlib",
    "healthcheck",
]

VERSION = "2023.05.0"

setup(
      name='mfe-python-flask',
      version=VERSION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=required,
)
