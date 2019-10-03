Generate Database
=================

Program ``gen_stdb.py``
-----------------------

Description
-----------
Create Station Database dictionary from input text file.

Usage
-----

.. code-block::

    $ gen_stdb.py -h
    Usage: gen_stdb.py [options] <station list>

    Script to generate a pickled station database file.

    Options:
      -h, --help       show this help message and exit
      -L, --long-keys  Specify Key format. Default is Net.Stn. Long keys are
                       Net.Stn.Chn
      -a, --ascii      Specify to write ascii Pickle files instead of binary.
                       Ascii are larger file size, but more likely to be system
                       independent.

  Input File Type 1 (chS csv):
  NET[:NET2:...],STA,LOC[:LOC2:...],CHN,YYYY-MM-DD,HH:MM:SS.SSS,YYYY-MM-
  DD,HH:MM:SS.SSS,lat,lon,elev,pol,azcor,status
  Input File Type 2 (IPO SPC):
  NET STA CHAN lat lon elev YYYY-MM-DD YYYY-MM-DD
  Output File Types:
  Each element corresponding to each dictionary key is saved as StDb.StbBElement
  class.

Example
-------

Let's use the example in :ref:`database` and create a database from information 
contained in a <space>-separated file. 
The basic format of the <space>-separated file for some TA stations would look like:

.. csv-table::

   network, station, channel, latitude, longitude, elevation, startdate, enddate

.. csv-table::
   :widths: 4, 6, 4, 6, 6, 4, 10, 10

   TA,M31M,BH*,62.2024,-134.3906,0.64,2015-10-17,2599-12-31
   TA,N32M,BH*,61.1512,-133.0818,0.82,2016-05-11,2599-12-31
   TA,P33M,BH*,60.2114,-132.8174,1.07,2015-10-15,2599-12-31

We can generate a database using the program:

.. code-block::

    $ gen_stdb.py ta_table.txt

    Parse Station List ta_table.txt
    Adding key: TA.M31M
    Adding key: TA.N32M
    Adding key: TA.P33M
      Pickling ta_table.txt.pkl

Or if we used the alternative input file format with <comma>-separated values,
we would get:

.. code-block::

    $ gen_stdb.py ta_table.csv

    Parse Station List ta_table.csv
    Adding key: TA.M31M
    Adding key: TA.N32M
    Adding key: TA.P33M
      Pickling ta_table.pkl

Now we can check that the databases contain the same list using the program
``ls_stdy.py``:

.. code-block::

    $ ls_stdb.py ta_table.txt.pkl

    Listing Station Pickle: ta_table.txt.pkl
    TA.M31M
    --------------------------------------------------------------------------
    1) TA.M31M
         Station: TA M31M 
          Alternate Networks: None
          Channel: BH ;  Location: 
          Lon, Lat, Elev:  62.20240, -134.39060,   0.640
          StartTime: 2015-10-17 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.N32M
    --------------------------------------------------------------------------
    2) TA.N32M
         Station: TA N32M 
          Alternate Networks: None
          Channel: BH ;  Location: 
          Lon, Lat, Elev:  61.15120, -133.08180,   0.820
          StartTime: 2016-05-11 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.P33M
    --------------------------------------------------------------------------
    3) TA.P33M
         Station: TA P33M 
          Alternate Networks: None
          Channel: BH ;  Location: 
          Lon, Lat, Elev:  60.21140, -132.81740,   1.070
          StartTime: 2015-10-15 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000


and finally:

.. code-block:: 

    $ ls_stdb.py ta_table.pkl

    Listing Station Pickle: ta_table.pkl
    TA.M31M
    --------------------------------------------------------------------------
    1) TA.M31M
         Station: TA M31M 
          Alternate Networks: None
          Channel: BH ;  Location: "--"
          Lon, Lat, Elev:  62.20240, -134.39060,   0.640
          StartTime: 2015-10-17 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.N32M
    --------------------------------------------------------------------------
    2) TA.N32M
         Station: TA N32M 
          Alternate Networks: None
          Channel: BH ;  Location: "--"
          Lon, Lat, Elev:  61.15120, -133.08180,   0.820
          StartTime: 2016-05-11 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000


    TA.P33M
    --------------------------------------------------------------------------
    3) TA.P33M
         Station: TA P33M 
          Alternate Networks: None
          Channel: BH ;  Location: "--"
          Lon, Lat, Elev:  60.21140, -132.81740,   1.070
          StartTime: 2015-10-15 00:00:00
          EndTime:   2599-12-31 00:00:00
          Status:    
          Polarity: 1
          Azimuth Correction: 0.000000

