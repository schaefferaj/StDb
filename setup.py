#!/usr/bin/env python

from distutils.core import setup
from os import listdir

scripts = ['Scripts/' + i for i in listdir('Scripts/')]

setup(
	name =             'stdb',
	version =          '0.1.0',
	description =      'Python Module for managing Station Databases',
	author =           'Andrew Schaeffer, Pascal Audet',
	maintainer =       'Andrew Schaeffer, Pascal Audet',
	maintainer_email = 'andrew.schaeffer@canada.ca, pascal.audet@uottawa.ca',
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
	url =              'https://github.com/schaefferaj/StDb/archive/v0.1.0.tar.gz')
