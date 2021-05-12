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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    install_requires=['obspy', 'PyQt5'],
    python_requires='>=3.6',
    packages=['stdb'],
    entry_points={
        'console_scripts':
        ['append_stdb=stdb.scripts.append_stdb:main',
         'dump_stdb=stdb.scripts.dump_stdb:main',
         'edit_stdb=stdb.scripts.edit_stdb:main',
         'gen_stdb=stdb.scripts.gen_stdb:main',
         'ls_stdb=stdb.scripts.ls_stdb:main',
         'merge_stdb=stdb.scripts.merge_stdb:main',
         'query_fdsn_stdb=stdb.scripts.query_fdsn_stdb:main',
         'stdb_to_kml=stdb.scripts.stdb_to_kml:main']},
         url='https://github.com/schaefferaj/StDb',
         download_url='https://github.com/schaefferaj/StDb/archive/v0.2.1.tar.gz')
