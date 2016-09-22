#!/usr/bin/env python

import os
import sys
import re

from setuptools import setup, find_packages

with open('pylixing/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pylixing',
    version=version,
    packages=find_packages(exclude=['docs', 'tests']),
    url='https://github.com/hifiveszu/pylixing',
    license='MIT',
    author='hifiveszu',
    author_email='hifiveszu@gmail.com',
    description='Python SDK for LiXing (http://www.lixing.biz/) APIs',
    zip_safe=False,
    install_requires=[
        'Mako>=1.0.2',
        'requests>=2.7.0',
        'schematics>=1.1.0',
        'xmltodict>=0.9.2'
    ]
)
