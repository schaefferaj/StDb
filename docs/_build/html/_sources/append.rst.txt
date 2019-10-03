Append New Station
==================

Program ``append_stdb.py``
--------------------------

Description
-----------
Append new station information to an existing station database.

Usage
-----

.. code-block:: none

    append_stdb.py -h
    Usage: append_stdb.py [options] <station pickle file>

    Helper program to append new stations to an existing station database.

    Options:
      -h, --help            show this help message and exit
      -o ONAME, --output-file=ONAME
                            Specify output file name. Defaults to the input file
                            with '.apd' added to the end.
      -C, --complex         Default behaviour only promps for station basics
                            (net,stn,chn,loc,lat,lon,start,end). Complex includes
                            additional data (alternate networks, multiple
                            locations, elevation, polarity, azimuth correction and
                            restricted status)
      -L, --long-keys       Specify Key format. Default is Net.Stn. Long keys are
                            Net.Stn.Chn
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

Example
-------

Assume we have created the StDb database containing only one CN station 
(as in the example in :mod:`~Scripts.merge_stdb.py`). Let's append a new
station to the database with a different network code and using only the basic
station attributes. Note that the fields (e.g., ``NY``, ``NEW`` below are
typed in the terminal by the user)

.. code-block:: none

    $ ls_stdb.py cn_list
    Listing Station Pickle: cn_list.pkl
    CN.WHY
    --------------------------------------------------------------------------
    1) CN.WHY
         Station: CN WHY  
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  60.65970, -134.88251,   1.273
          StartTime: 1994-10-03 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000

.. code-block:: none

    $ append_stdb.py cn_list
    ********************************
    * New Station
    *    Network:   NY
    *    Station:   NEW
    *    Channel:   BH
    *    LocId:     --
    *    Longitude: -120.
    *    Latitude:  80.
    *    Start:     2018-01-01
    *    End:       2018-06-01
    * Added to DB

    * Another Station? [Y]/N: N

    Saving new database: cn_list.apd.pkl

.. code-block:: none

    $ ls_stdb.py cn_list.apd
    Listing Station Pickle: cn_list.apd.pkl
    CN.WHY
    --------------------------------------------------------------------------
    1) CN.WHY
         Station: CN WHY  
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  60.65970, -134.88251,   1.273
          StartTime: 1994-10-03 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000


    NY.NEW
    --------------------------------------------------------------------------
    2) NY.NEW
         Station: NY NEW  
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  80.00000, -120.00000,   0.000
          StartTime: 2018-01-01 00:00:00
          EndTime:   2018-06-01 00:00:00
          Status:    ?
          Polarity: 1
          Azimuth Correction: 0.000000

