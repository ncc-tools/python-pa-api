#!/usr/bin/env python3

"""NCC Performance Analyser API to ElasticSearch coupler"""

import os
from setuptools import setup, find_packages
from pip.req import parse_requirements

reqs_path = os.path.dirname(os.path.realpath(__file__)) + '/requirements/release.txt'
install_reqs = parse_requirements(reqs_path, session=False)
requires = [str(ir.req) for ir in install_reqs]

setup(
    name='paapi',
    version='0.0.1',
    description='Abstraction classes to access the PA API',
    author='NCC Group',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requires
)
