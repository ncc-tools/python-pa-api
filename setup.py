#!/usr/bin/env python3

"""NCC Performance Analyser API to ElasticSearch coupler"""

import os
from setuptools import setup

setup(
    name='ncc_paapi',
    version='0.0.1',
    description='Abstraction classes to access the PA API',
    author='NCC Group',
    packages=['paapi'],
    install_requires=['urllib3==1.19.1'],
    url='https://github.com/ncc-tools/python-pa-api'
)
