# Copyright 2019 Andrew Schaeffer & Pascal Audet
#
# This file is part of StDb.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
StDb is a package containing tools for building a database of station information
from geophysical observatories. The code is used through command-line scripts 
and include several options for querying an online fdsn archive, list 
the content of an existing station database, merge existing databases, and 
manually append new station information (e.g., for stations not hosted on
any fdsn archive). 

The resulting station dictionary is used in various seismic applications, 
such as `SplitPy <https://github.com/paudetseis/SplitPy>`_, 
`RfPy <https://github.com/paudetseis/RfPy>`_ and 
`OBStools <https://github.com/paudetseis/OBStools>`_.

Licence
-------

Copyright 2019 Andrew Schaeffer & Pascal Audet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Installation
------------

Dependencies
++++++++++++

The current version was developed using **Python3.7** \
Also, the following package is required:

- `obspy <https://github.com/obspy/obspy/wiki>`_
- `PyQt5 <https://pypi.org/project/PyQt5/>`_

Conda environment
+++++++++++++++++

We recommend creating a custom ``conda`` environment
where ``telewavesim`` can be installed along with its dependencies.

.. sourcecode:: bash

   conda create -n stdb python=3.7 obspy -c conda-forge

Activate the newly created environment:

.. sourcecode:: bash

   conda activate stdb

Installing from Pypi
++++++++++++++++++++

.. sourcecode:: bash

   pip install stdb

Installing from source
++++++++++++++++++++++

- Clone the repository:

.. sourcecode:: bash

   git clone https://github.com/schaefferaj/StDb.git
   cd StDb

- Install using pip:

.. sourcecode:: bash

   pip install .

"""

__version__ = '0.2.0'

from . import kml
from .io import write_db, load_db
from .classes import StDbElement
from .convert import tocsv, fromcsv
from .gui import EditMsgBox
