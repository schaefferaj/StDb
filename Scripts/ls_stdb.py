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
Program ``ls_stdb.py``
----------------------

Description
-----------
Lists databse dictionary contained in a pickled ``StDb`` database file.

Usage
-----

.. code-block:: none

    ls_stdb.py -h
    Usage: ls_stdb.py [options] <station pickle file>

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
"""


import sys
import os.path as osp
from stdb import load_db

def get_options():
    from optparse import OptionParser
    
    parser=OptionParser(usage="Usage: %prog [options] <station pickle file>", \
        description="Helper program to examine the contents of a station pickle file")
    parser.add_option("-N", "--networks", action="store_true", dest="networks", default=False, \
        help="Use flag to retrieve only the list of networks in the database")
    parser.add_option("--keys", action="store", type=str, dest="keys", default="", \
        help="Specify a comma separated list of keys to return. These can be fragments " \
        "of a key to include all keys matching any fragment.")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file " \
        "size, but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Parse Input Filename
    if len(args) == 0:
        parser.error("Must provide at least 1 input database!")
    for iin in range(0,len(args)):
        if args[iin].find('.pkl') > 0:
            args[iin] = osp.splitext(args[iin])[0]

    # Check input
    errfl = []
    for iin in range(0,len(args)):
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


if __name__=='__main__':

    # get options
    (opts, inpickles) = get_options()

    # Loop through inputs
    for inpickle in inpickles:

        # Pickle Already Created...
        print ("Listing Station Pickle: {0:s}".format(inpickle))
        db, stkeys = load_db(inpickle, binp=opts.use_binary, keys=opts.keys)
        
        # Networks only?
        if opts.networks:
            nets = []
        
        # # construct station key loop
        # allkeys = db.keys()
        # sorted(allkeys)
     
        # # Extract key subset
        # if len(opts.keys) > 0:
        #     stkeys = []
        #     for skey in opts.keys:
        #         stkeys.extend([s for s in allkeys if skey in s] )
        # else:
        #     stkeys = db.keys()
        #     sorted(stkeys)
        
        ikey = 0
        for key in stkeys:
            #print(key)
            ikey += 1
            if opts.networks:
                nets.append(db[key].network)
                continue
            print ("--------------------------------------------------------------------------")
            print ("{0:.0f}) {1:s}".format(ikey, key))
            print (db[key](5))
            print ("")
        
        if opts.networks:
            nets = list(set(nets))
            nets.sort()
            print ("Networks: ")
            for net in nets:
                print (net)
