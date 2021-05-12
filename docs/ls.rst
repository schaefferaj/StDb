List Database Content
=====================

Program ``ls_stdb``
-------------------

Description
-----------
Lists database dictionary contained in a pickled ``StDb`` database file.

Usage
-----

.. code-block::

    $ ls_stdb -h
    Usage: ls_stdb [options] <station pickle file>

    Helper program to examine the contents of a station pickle file

    Options:
      -h, --help      show this help message and exit
      -N, --networks  Use flag to retrieve only the list of networks in the
                      database
      --keys=KEYS     Specify a comma separated list of keys to return. These can
                      be fragments of a key to include all keys matching any
                      fragment.
      -a, --ascii     Specify to write ascii Pickle files instead of binary. Ascii
                      are larger file size, but more likely to be system
                      independent.

Examples
--------

Assume we have already created a StDb database named ``ta_list.pkl`` using the example in 
:ref:`query`. List its content:

.. code-block::

    $ ls_stdb ta_list
    Listing Station Pickle: ta_list.pkl
    TA.M31M
    --------------------------------------------------------------------------
    1) TA.M31M
         Station: TA M31M 
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  62.20240, -134.39059,   0.639
          StartTime: 2015-10-17 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.N32M
    --------------------------------------------------------------------------
    2) TA.N32M
         Station: TA N32M 
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  61.15120, -133.08180,   0.816
          StartTime: 2016-05-11 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.P33M
    --------------------------------------------------------------------------
    3) TA.P33M
         Station: TA P33M 
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  60.21140, -132.81740,   1.066
          StartTime: 2015-10-15 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000

List only one station key:

.. code-block:: none

    $ ls_stdb --keys=TA.P33M new_list
    Listing Station Pickle: new_list.pkl
    TA.P33M
    --------------------------------------------------------------------------
    1) TA.P33M
         Station: TA P33M 
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  60.21140, -132.81740,   1.066
          StartTime: 2015-10-15 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000
