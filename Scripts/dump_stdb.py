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
Program dump_stdb.py
--------------------

Description
-----------
Program to dump a Station Database into ``.csv`` format. If an output file is 
specified, file is dumped there (with ``.csv`` extension). 
Otherwise output is directed to standard output.

Use the --keys option to only dump certain keys.

Usage
-----

.. code-block:: none

    dump_stdb.py -h
    Usage: dump_stdb.py [options] <station pickle file>

    Program to dump the contents of a station database (.pkl) as csv. By default
    the output is directed to standard out. If a filename is optionally included,
    then the contents are also dumped to file.

    Options:
      -h, --help            show this help message and exit
      --keys=KEYS           Specify a comma separated list of keys to dump. Any
                            key not specified by this search is not included in
                            the output.
      -O OFILE, --output-file=OFILE
                            Specify an output file name for the dumped csv format
                            data. If no .csv extenion is included, one is added.
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

"""

import sys
import os.path as osp
from os import remove
from stdb import load_db
from stdb import tocsv

def get_options():
    from optparse import OptionParser
    
    parser = OptionParser(usage='Usage: %prog [options] <station pickle file>', \
        description="Program to dump the contents of a station database (.pkl) as csv. " \
        "By default the output is directed to standard out. If a filename is optionally " \
        "included, then the contents are also dumped to file.")
    parser.add_option("--keys", action="store", type=str, dest="keys", default="", \
        help="Specify a comma separated list of keys to dump. Any key not specified by " \
        "this search is not included in the output.")
    parser.add_option("-O","--output-file", type=str, dest="ofile", default="", \
        help="Specify an output file name for the dumped csv format data. If no .csv " \
        "extenion is included, one is added.")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file " \
        "size, but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Check input
    if not osp.exists(args[0]):
        parser.error("Input database " + args[0] + " does not exist")
    
    # Construct keys
    if len(opts.keys) > 0:
        opts.keys = opts.keys.split(",")

    # return options
    return opts, args[0]


if __name__=='__main__':

    # get options
    (opts, inpickle) = get_options()

    # check output
    wtf = False
    if len(opts.ofile) > 0:
        wtf = True
        if opts.ofile.find('.csv') > 0:
            ofile = opts.ofile
        else:
            ofile = opts.ofile + ".csv"
        fout = open(ofile,'w')

    # Check input extension extension
    ext = osp.splitext(inpickle)[1]
    if ext == ".pkl":
        
        # Pickle Already Created...
        db,stkeys = load_db(inpickle, binp=opts.use_binary, keys=opts.keys)
        
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
        nout = 0
        for key in stkeys:
            ikey += 1

            # generate csvline
            csvline = tocsv(db[key])

            # StdOut
            print (csvline)
            
            # Save to File
            if wtf:
                fout.writelines(csvline + "\n")
                nout = nout + 1
        
        # Did we make any changes?
        if wtf and nout == 0:
            remove(ofile)    
        
    else:
        print ("Error: Must Enter a .pkl station database pickle file")
        sys.exit()