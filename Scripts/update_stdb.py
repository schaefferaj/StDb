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
''' 
        Program: update_stdb.py

        Description:
        Update the internal structure of an stdb Pickle file

        Opens the Station Database file and checks its integrity, and updates it to the most recent standards.

'''

import sys
import os.path as osp
from stdb import load_db, write_db

def get_options():
    from optparse import OptionParser
    
    parser = OptionParser(usage="Usage: %prog [options] <station pickle file>", \
        description="Helper program to update the contents of a station pickle file")
    parser.add_option("-v", "--verb", action="store_true", dest="verb", default=False, \
        help="Enable verbose output. Default Quiet")
    parser.add_option("--output-name", action="store",type=str, dest="outname", default="", \
        help="Specify the output filename. Default behaviour adds .new to the input file.")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Parse Input Filename
    if args[0].find(".pkl") > 0:
        args[0] = osp.splitext(args[0])[0]

    # Check input
    if not osp.exists(args[0] + ".pkl"):
        parser.error("Input database " + args[0] + ".pkl does not exist")
    
    # Construct Output Name
    if len(opts.outname) == 0:
        opts.outname = args[0] + ".new.pkl"
    else:
        if opts.outname.find('.pkl') < 0:
            opts.outname = opts.outname + ".pkl"
    args[0] = args[0] + ".pkl"

    # return options
    return opts, args[0]


if __name__=='__main__':

    # get options
    (opts, inpickle) = get_options()

    # Check extension
    ext = osp.splitext(inpickle)[1]

    if ext == ".pkl":

        # Pickle Already Created...
        if opts.verb: print ("Listing Station Pickle: {0:s}".format(inpickle))
        db = load_db(inpickle, binp=opts.use_binary)
        ndb = {}

        # Sort Keys
        stkeys = db.keys()
        sorted(stkeys)
        
        ikey = 0
        for key in stkeys:
            ikey += 1

            # get net and station
            net = db[key].network
            stn = db[key].station

            # Check Key
            nkey = net.upper() + "." + stn.upper()

            # Update New DB
            ndb[nkey] = db[key]

            # Check Location
            updloc = False
            if len(db[key].location) == 0:
                ndb[nkey].location = ['']

            if opts.verb:
                print ("--------------------------------------------------------------------------")
                print ("{0:.0f}) {1:s}".format(ikey,nkey))

            # Print
            if opts.verb:
                print (ndb[nkey](5))
                print ("")

        # Save Output
        write_db(fname=opts.outname, stdb=ndb, binp=opts.use_binary)
        
    else:
        print ("Error: Must Enter a .pkl station database pickle file")
        sys.exit()
