#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:19:34 2019

@author: EAD2019

run: python setup.py install

"""

from os import path
from setuptools import setup, find_packages
from io import open

currentPath = path.abspath(path.dirname(__file__))

with open(path.join(currentPath, 'requirements.txt'), encoding='utf-8') as fp:
    requirements = [r.rstrip() for r in fp.readlines() if not r.startswith('#')]

with open(path.join(currentPath, 'README.md'), encoding='utf-8') as fp:
    long_description = fp.read()

setup(
    name='ead2019',
    version='1.2',
    description='Endoscopic artefact detection challenge (ISBI2019)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sharibox/EAD2019',
    author='EAD2019',
    author_email='sharib.ali@eng.ox.ac.uk',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha, 4 - Beta, 5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='endoscopy artefact detection segmentation',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=requirements,
)
