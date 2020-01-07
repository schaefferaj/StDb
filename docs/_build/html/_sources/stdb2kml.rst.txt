Convert Database to KML
=======================

Program ``stdb_to_kml.py``
--------------------------

Description
-----------
Convert a station Database from a ``.pkl`` file into a ``.kml`` file for use 
in plotting in Google Earth.

Fields in the ``.kml`` file include
-----------------------------------
* Latitude
* Longitude
* Elevation
* Start Time
* End Time
* Open?
* Channels

.. _kmlusage:

Usage
-----

.. code-block::

    $ stdb_to_kml.py -h
    Usage: stdb_to_kml.py [options] <station pickle file>

    Program to create a KML file for plotting based on the contents of a station
    pickle file

    Options:
      -h, --help            show this help message and exit
      --keys=KEYS           Specify a comma separated list of keys to return.
                            These can be fragments of a key to include all keys
                            matching any fragment.
      -V VERB, -v VERB, --verb-level=VERB
                            Specify verbosity. Default 0: no output. 1: network
                            list. 2: include station list.
      -o OUTFILE, --outfile=OUTFILE
                            Output kml file
      -s SCALE, --icon-scale=SCALE
                            Icon Size Scale (default 1.8)
      -r, --no-random-colours
                            Turn off random colours (default random on)
      -T DOCTITLE, --Document-title=DOCTITLE
                            KML Document Title
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

Examples
--------

Run the example in :ref:`merge` to generate a database named ``ta_table.pkl``.
To generate a ``.kml`` file with only one station to load in Google Earth, run

.. code-block::

    $ stdb_to_kml.py --keys=TA.P33M -o P33M.kml ta_table.pkl

This produces a new file called ``P33M.kml`` that you can import in Google Earth

.. figure:: ../stdb/examples/figures/P33M.png
   :align: center

To show more than one network, follow the example in :ref:`query` to generate
a ``merged_list.pkl`` database and convert its content to kml:

.. code-block::

    $ stdb_to_kml.py -o merged.kml merged_list.pkl

This produces a new file called ``merged.kml`` that you can import in Google Earth

.. figure:: ../stdb/examples/figures/merged.png
   :align: center

Check out the :ref:`kmlusage` above for more control on the KML properties.