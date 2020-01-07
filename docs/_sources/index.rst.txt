.. figure:: ../stdb/examples/figures/StDb_logo.png
   :align: center

StDb Tools - documentation
==========================

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


Quick links
"""""""""""

* `StDb Git repository <https://github.com/schaefferaj/StDb>`_
* `SplitPy Git repository <https://github.com/paudetseis/SplitPy>`_
* `RfPy Git repository <https://github.com/paudetseis/RfPy>`_
* `OBStools Git repository <https://github.com/paudetseis/OBStools>`_

.. Getting Started
.. """""""""""""""

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   api
   database

.. Content
.. """""""

.. toctree::
   :maxdepth: 1
   :caption: Content

   classes
   io
   convert
   gui
   kml

.. Programs & Tutorials
.. """"""""""""""""""""

.. toctree::
   :maxdepth: 1
   :caption: Programs & Tutorials

   query
   ls
   merge
   gen
   append
   edit
   dump
   stdb2kml
