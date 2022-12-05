#!/usr/bin/env python3
from setuptools import setup, find_packages

required = [
    "mongoengine",
    "Flask",
    "flask-cors",
    "flask-compress",
    "flask_mongoengine",
    "flask-smorest",
    "marshmallow",
    "marshmallow_enum",
    "environs",
]

VERSION = "v1.0"

setup(
      name='mfe_flask_api',
      version=VERSION,
      packages=find_packages(exclude=['tests', 'tests.*']),
      install_requires=required,
)
