#!/usr/bin/env python

from distutils.core import setup

setup(
    name='LeBonPrix',
    version=0.1,
    install_requires = [
        'requests',
        'numpy',
        'scipy',
        'scikit-learn'  
    ],
    packages = [
        'lebonprix',
        'lebonprix.crawler'
    ]
)
