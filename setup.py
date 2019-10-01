#!/usr/bin/env python

from distutils.core import setup
from os import listdir

version = open('version.txt').read().split()[0]
scripts = ['Scripts/' + i for i in listdir('Scripts/')]

setup(
	name =             'stdb',
	version =          version,
	description =      'Python Module for managing Station Databases',
	author =           'Andrew Schaeffer',
	maintainer =       'Andrew Schaeffer',
	maintainer_email = 'andrew.schaeffer@uottawa.ca',
    classifiers         = [
                            'Development Status :: 3 - Alpha',
                            'License :: OSI Approved :: MIT License',
                            'Programming Language :: Python :: 3.5',
                            'Programming Language :: Python :: 3.6',
                            'Programming Language :: Python :: 3.7'
                            ],
    install_requires    = ['obspy'],
    python_requires     = '>=3.5',
	packages =         ['StDb'],
	scripts =          scripts,
	url =              'https://github.com/schaefferaj/stdb')
