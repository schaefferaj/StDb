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
Program ``edit_stdb.py``
------------------------

Description
-----------
Edit Station Database Dictionary contained in pickle file.
The station dictionary contains keys that are named NET.STA.CHAN, where CHAN
is a two character representation of the desired channel (ex, BH, HH, LH).
Within each KEY is the set of data used in later programs to define the 
station information. The data is stored as a dictionary, with each dictionary 
element being an object of class :class:`~stdb.classes.StDbElement`. 

Usage
-----

.. code-block:: none

    edit_stdb.py -h
    Usage: edit_stdb.py [options] <station pickle file>

    Program to make basic modifications to a station database pickle file

    Options:
      -h, --help            show this help message and exit
      --keys=KEYS           Specify a comma separated list of keys to return.
                            These can be fragments of a key to include all keys
                            matching any fragment.
      -L, --long-keys       Specify Key format. Default is Net.Stn. Long keys are
                            Net.Stn.Chn
      -O OFILE, --output-file=OFILE
                            Specify an output file name for the edited database.
                            Default behaviour performs the changes in place on the
                            input file.
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

"""


import sys
import os.path as osp
import stdb
from stdb import EditMsgBox
from stdb import load_db, write_db

def get_options():
    from optparse import OptionParser
    
    parser = OptionParser(usage="Usage: %prog [options] <station pickle file>", \
        description="Program to make basic modifications to a station database pickle file")
    parser.add_option("--keys", action="store", type=str, dest="keys", default="", \
        help="Specify a comma separated list of keys to return. These can be fragments of a " \
        "key to include all keys matching any fragment.")
    parser.add_option("-L", "--long-keys", action="store_true", dest="lkey", default=False, \
        help="Specify Key format. Default is Net.Stn. Long keys are Net.Stn.Chn")
    parser.add_option("-O", "--output-file", type=str, dest="ofile", default="", \
        help="Specify an output file name for the edited database. Default behaviour performs " \
        "the changes in place on the input file.")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Check input
    if not osp.exists(args[0]):
        parser.error("Input database " + args[0] + " does not exist")
    
    # Construct keys
    if len(opts.keys) > 0:
        opts.keys = opts.keys.split(',')

    # return options
    return opts, args[0]


if __name__=='__main__':

    # get options
    (opts, inpickle) = get_options()

    # Check extension
    ext = osp.splitext(inpickle)[1]
    if ext == ".pkl":
        
        # Pickle Already Created...
        print ("Listing Station Pickle: {0:s}".format(inpickle))
        db,stkeys = load_db(inpickle, binp=opts.use_binary, keys=opts.keys)
        
        # # construct station key loop
        # allkeys = db.keys()
        # sorted(allkeys)
    
        # Do we make any changes
        tfEdit = False
    
        # # Extract key subset
        # if len(opts.keys) > 0:
        #     stkeys = []
        #     for skey in opts.keys:
        #         stkeys.extend([s for s in allkeys if skey in s])
        # else:
        #     stkeys = db.keys()
        #     sorted(stkeys)
        
        ikey = 0
        for key, val in db.items():
            if key not in stkeys: continue
            ikey += 1

            print ("--------------------------------------------------------------------------")
            print (" Original ")
            print ("{0:.0f}) {1:s}".format(ikey, key))
            print (db[key](5))
            print ("**************************************************************************")
            newline = EditMsgBox(ststr=stdb.convert.tocsv(db[key]), title=key)
            if len(newline) > 0:
                nkey, nel = stdb.convert.fromcsv(newline, lkey=opts.lkey)
                if nel == val:
                    print(" No Changes Made...")
                    continue
                if nkey is not None and nel is not None:
                    if key == nkey:
                        db[key] = nel
                        print (" Replaced " + key + ": ")
                        print (db[key](5))
                        tfEdit = True
                    else:
                        if nkey not in db:
                            del db[key]
                            db[nkey] = nel
                            print (" Added " + nkey + ":")
                            print (db[nkey](5))
                            tfEdit = True
                        else:
                            print (" Database already has key " + nkey + ". No changes made")
                            print (db[nkey](5))
                else:
                    print (" Error parsing: ")
                    print ( "  " + newline )
            else:
                print (" No Changes Made...")    
        
        # Did we make any changes?
        if tfEdit:

            # Changes Made... Save Database
            if len(opts.ofile) > 0:
                if opts.ofile.find('.pkl') > 0:
                    fname = opts.ofile
                else:
                    fname = opts.ofile + ".pkl"
                write_db(fname=fname, stdb=db, binp=opts.use_binary)
            else:
                write_db(fname=inpickle, stdb=db, binp=opts.use_binary)
        
    else:
        print ("Error: Must Enter a .pkl station database pickle file")
        sys.exit()