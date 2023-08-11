#!/usr/bin/env python3
from setuptools import setup, find_packages

required = [
    "mongoengine",
    "Flask",
    "flask_mongoengine",
    "flask-smorest",
    "marshmallow",
    "pytz",
    "gunicorn",
    "environs",
    "passlib"
]

VERSION = "2023.8.0"

setup(
      name='mfe-python-flask',
      version=VERSION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=required,
)
