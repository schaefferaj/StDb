# Copyright 2019 Andrew Schaeffer
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

#!/usr/bin/env python
# encoding: utf-8

"""
Program
-------
``merge_stdb.py``

Description
-----------
Merge multiple ``StDb`` database files together.
Performs a rudimentary check for mulitple keys.

Usage
-----

.. code-block::none

    merge_stdb.py -h
    Usage: merge_stdb.py [options] <station pickle file 1> <station pickle file 2> [additional station pickle files]

    Helper program to merge multiple station database files together.

    Options:
      -h, --help            show this help message and exit
      -v, --verbose         Enable more verbose output. Default is quiet (no
                            prompts).
      -O, --overwrite       Ovewrite output file if it already exists. Default
                            behaviour quits with warning.
      -o ONAME, --output-file=ONAME
                            Specify output file name. Defaults to the input file
                            with '.apd' added to the end.
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

Example
-------

Assume we have already created a StDb database named ``ta_list.pkl`` using the example 
in :mod:`~Scripts.query_fdsn_stdb.py`. Now create a second StDb database by querying the
FDSN archive for stations in the CN network in the same region. Send the prompt to a stdb.log 
file.

.. note::

    This could have been performed during the first call to ``query_fdsn_stdb.py`` with the 
    option ``-N TA,CN`` - this is just for illustration

.. code-block:: none

    $ query_fdsn_stdb.py -C BH? -N CN --minlat=60 --maxlat=65 --minlon=-135 --maxlon=-120  --start=2017-01-01 cn_list >> stdb.log

List the content of cn_list.pkl:

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

Merge ``ta_list.pkl`` and ``cn_list.pkl`` into a new file called ``merged_list.pkl``:

.. code-block:: none

    $ merge_stdb.py -o merged_list ta_list cn_list 

.. code-block:: none

    $ ls_stdb.py merged_list
    Listing Station Pickle: merged_list.pkl
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


    CN.WHY
    --------------------------------------------------------------------------
    4) CN.WHY
         Station: CN WHY  
          Alternate Networks: None
          Channel: BH ;  Location: --
          Lon, Lat, Elev:  60.65970, -134.88251,   1.273
          StartTime: 1994-10-03 00:00:00
          EndTime:   2599-12-31 23:59:59
          Status:    open
          Polarity: 1
          Azimuth Correction: 0.000000

"""


import sys
import os.path as osp
from stdb import load_db, write_db
from stdb import StDbElement
from obspy import UTCDateTime

def get_options():
    from optparse import OptionParser
    
    parser = OptionParser(usage="Usage: %prog [options] <station pickle file 1> <station pickle file 2> [additional station pickle files]", \
        description="Helper program to merge multiple station database files together.")
    parser.add_option("-v", "--verbose", action="store_true", dest="verb", default=False, \
        help="Enable more verbose output. Default is quiet (no prompts).")
    parser.add_option("-O", "--overwrite", action="store_true", dest="ovr", default=False, \
        help="Ovewrite output file if it already exists. Default behaviour quits with warning.")
    parser.add_option("-o", "--output-file", action="store", type="str", dest="oname", default="", \
        help="Specify output file name. Defaults to the input file with '.apd' added to the end.")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Check number of arguments
    if len(args) < 2:
        print("Specify more than one input database")
        sys.exit()

    # Parse Input Filename
    for ia in range(0,len(args)):
        if args[ia].find('.pkl') < 0:
            args[ia] = args[ia] + ".pkl"


    # Construct output file name
    if len(opts.oname) == 0:
        opts.oname = "merged.pkl"
    else:
        if opts.oname.find('.pkl') < 0:
            opts.oname = opts.oname + ".pkl"

    # return options
    return opts, args


if __name__=='__main__':

    # get options
    (opts, args) = get_options()

    # Check Output File
    if osp.exists(opts.oname) and not opts.ovr:
        print("Error: Output File exists " + opts.oname)
        print("  Run using --overwrite to replace existing file")
        sys.exit()

    # Load First Database
    if opts.verb: print("Loading " + args[0])
    tdb = load_db(args[0], binp=opts.use_binary)

    # construct station key loop
    allkeys = tdb.keys()
    sorted(allkeys)

    # Any added?
    stadd = False

    # Loop adding additional databases
    for ndb in args[1:]:

        # load database
        if opts.verb: print(" Adding " + ndb)
        db = load_db(ndb, binp=opts.use_binary)

        # Get new keys
        nkeys = db.keys()
        sorted(nkeys)

        # Loop through new keys
        for nkey in nkeys:
            if nkey not in tdb:
                tdb[nkey] = db[nkey]
                stadd = True
            else:
                if opts.verb:
                    print("")
                    print("*********************************************************")
                    print("! Duplicate Entry: " + nkey)
                    print("  Retaining: ")
                    print(tdb[nkey](5))
                    print("  Discarding: ")
                    print(db[nkey](5))
                    print("*********************************************************")

    # Were any new stations added?
    if stadd:
        if opts.verb:
            print("")
            print("Saving merged database: " + opts.oname)
        write_db(fname=opts.oname, stdb=tdb, binp=opts.use_binary)
    else:
        if opts.verb:
            print("")
            print("No actual merges performed...")
