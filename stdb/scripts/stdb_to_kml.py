#!/usr/bin/env python3
# encoding: utf-8

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

"""
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

Usage
-----

.. code-block:: none

    stdb_to_kml.py -h
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

"""

import sys
import os.path as osp
from stdb.kml import createKML

def get_options():
    from optparse import OptionParser
    from datetime import datetime
    
    parser = OptionParser(usage="Usage: %prog [options] <station pickle file>", \
        description="Program to create a KML file for plotting based on the contents of a station pickle file")
    parser.add_option("--keys", action="store", type=str, dest="keys", default="", \
        help="Specify a comma separated list of keys to return. These can be fragments " \
        "of a key to include all keys matching any fragment.")
    parser.add_option("-V","-v","--verb-level", action="store", type="int", dest="verb", default=0, \
        help="Specify verbosity. Default 0: no output. 1: network list. 2: include station list.")
    parser.add_option("-o","--outfile", action="store", type="string", dest="outfile", default="", \
        help="Output kml file")
    parser.add_option("-s","--icon-scale", action="store", type="string", dest="scale", default="1.8", \
        help="Icon Size Scale (default 1.8)")
    parser.add_option("-r","--no-random-colours", action="store_true", dest="randoff", default=False, \
        help="Turn off random colours (default random on)")
    parser.add_option("-T","--Document-title", action="store", type="string", dest="doctitle", default="", \
        help="KML Document Title")
    parser.add_option("-a","--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Parse Input Filename
    if len(args) == 0:
        parser.error("Must provide at least 1 input database!")
    for iin in range(0, len(args)):
        if args[iin].find(".pkl") > 0:
            args[iin] = osp.splitext(args[iin])[0]
        elif args[iin][-1] == ".":
            args[iin] = args[iin][0:-1]

    # create output filename
    if len(opts.outfile) == 0:
        outfile = args[0].replace('.pkl','') + ".kml"
    else:
        outfile = opts.outfile
        if outfile.find('.kml') < 0:
                outfile = outfile + ".kml"
    opts.outfile = outfile

    # set document title
    if len(opts.doctitle) == 0:
        opts.doctitle = "; ".join(args) + ";; Created: " + str(datetime.now())

    # Check input
    errfl = []
    for iin in range(0, len(args)):
        if not osp.exists(args[iin] + ".pkl"):
            errfl.append(args[iin] + ".pkl")
    # 
    if len(errfl) > 0:
        parser.error("Input database(s) " + ", ".join(errfl) + " do not exist")
    
    # Construct keys
    if len(opts.keys) > 0:
        opts.keys = opts.keys.split(',')

    # Return extension
    for iin in range(0, len(args)):
        args[iin] = args[iin] + ".pkl"

    # return options
    return opts, args

def construct_mdb(inps=[], skeys=[], binp=True):
    from stdb.io import load_db
    
    # Construct Master DB from All Pickles
    mdb = {}

    # Loop through inputs
    for inp in inps:

        # Loading
        db,stkeys = load_db(inp, binp=binp, keys=skeys)

        # # construct station key loop
        # allkeys = db.keys()
        # sorted(allkeys)
    
        # # Extract key subset
        # if len(skeys) > 0:
        #     stkeys = []
        #     for skey in skeys:
        #         stkeys.extend([s for s in allkeys if skey in s] )
        # else:
        #     stkeys = db.keys()
        #     sorted(stkeys)
        
        # master
        for key in stkeys:
            if key not in mdb:
                mdb[key] = db[key]

    return mdb

def reorder_db(indb={}):
    ndb = {}
    nets = []
    keys = indb.keys()
    sorted(keys)
    for key in keys:
        net = indb[key].network
        if net in ndb:
            ndb[net].append(indb[key])
        else:
            ndb[net] = [indb[key]]
            nets.append(net)

    nets = list(set(nets))
    nets.sort()

    return nets, ndb


if __name__=='__main__':

    # get options
    (opts, inpickles) = get_options()

    # Get Master Database
    mdb = construct_mdb(inps=inpickles, skeys=opts.keys, binp=opts.use_binary)

    # Convert Database to Network Sorted
    nets, ndb = reorder_db(indb=mdb)

    # Create KML Files
    createKML(nets=nets, netd=ndb, fileName=opts.outfile, opts=opts)
    if opts.verb > 0:
        print ("Successfully wrote {0:d} Networks to file : {1}".format(len(nets), opts.outfile))
