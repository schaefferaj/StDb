import os.path
from os import listdir
import re
from numpy.distutils.core import setup


def find_version(*paths):
    fname = os.path.join(os.path.dirname(__file__), *paths)
    with open(fname) as fp:
        code = fp.read()
    match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", code, re.M)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string.")


scripts = ['Scripts/' + i for i in listdir('Scripts/')]

setup(
    name='stdb',
    version=find_version('stdb', '__init__.py'),
    description='Python Module for managing Station Databases',
    author='Andrew Schaeffer, Pascal Audet',
	  author_email='andrew.schaeffer@canada.ca, pascal.audet@uottawa.ca',
    maintainer='Andrew Schaeffer, Pascal Audet',
    maintainer_email='andrew.schaeffer@canada.ca, pascal.audet@uottawa.ca',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=['obspy', 'PyQt5'],
    python_requires='>=3.6',
    packages=['stdb'],
    scripts=scripts,
    url='https://github.com/schaefferaj/StDb/archive/v0.2.0.tar.gz')
