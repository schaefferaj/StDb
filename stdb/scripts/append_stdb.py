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
Program ``append_stdb.py``
--------------------------

Description
-----------
Append new station information to an existing station database.

Usage
-----

.. code-block::

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

"""

import sys
import os.path as osp
from stdb import load_db, write_db
from stdb import StDbElement
from obspy import UTCDateTime

def get_options():
    from optparse import OptionParser
    
    parser = OptionParser(usage="Usage: %prog [options] <station pickle file>", \
        description="Helper program to append new stations to an existing station database.")
    parser.add_option("-o", "--output-file", action="store", type="str", dest="oname", default="", \
        help="Specify output file name. Defaults to the input file with '.apd' added to the end.")
    parser.add_option("-C", "--complex", action="store_true", dest="complex", default=False, \
        help="Default behaviour only promps for station basics (net,stn,chn,loc,lat,lon,start,end). " \
        "Complex includes additional data (alternate networks, multiple locations, elevation, polarity, " \
        "azimuth correction and restricted status)")
    parser.add_option("-L", "--long-keys", action="store_true", dest="lkey", default=False, \
        help="Specify Key format. Default is Net.Stn. Long keys are Net.Stn.Chn")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, but " \
        "more likely to be system independent.")

    # Parse Arguments
    (opts, args) = parser.parse_args()

    # Parse Input Filename
    if args[0].find(".pkl") > 0:
        args[0] = osp.splitext(args[0])[0]

    # Check input
    if not osp.exists(args[0] + ".pkl"):
        parser.error("Input database " + args[0] + ".pkl does not exist")

    # Construct output file name
    if len(opts.oname) == 0:
        opts.oname = args[0] + ".apd"
    else:
        if opts.oname.find('.pkl') > 0:
            opts.oname = osp.splitext(opts.oname)[0]

#  # Construct keys
#  if len(opts.keys)>0:
#    opts.keys=opts.keys.split(',')

    # Return extension
    args[0] = args[0] + ".pkl"
    opts.oname = opts.oname + ".pkl"

    # return options
    return opts, args[0]


if __name__=='__main__':

    # get options
    (opts, inpickle) = get_options()

    # Check Output File
    if osp.exists(opts.oname):
        print("Error: Output File exists ", opts.oname)
        sys.exit()

    # Load Database
    db = load_db(inpickle, binp=opts.use_binary)

    # construct station key loop
    allkeys = db.keys()
    sorted(allkeys)

    # Loop adding new stations
    newstn = ""
    addnew = False
    while len(newstn) == 0 or newstn.lower()[0] == "y":

        print("********************************")
        print("* New Station")

        # Get Basic Info
        net = input("*    Network:   ")
        stn = input("*    Station:   ")
        chn = input("*    Channel:   ")[0:2]
        loc = input("*    LocId:     ")
        lon = float(input("*    Longitude: "))
        lat = float(input("*    Latitude:  "))
        std = UTCDateTime(input("*    Start:     "))
        edd = UTCDateTime(input("*    End:       "))

        # Advanced Info
        if opts.complex:
            altnet = input("*    Alternate Networks: ")
            addloc = input("*    Additional LocIDs: ")
            pol = float(input("*    Polarity: "))
            azcor = float(input("*    Azimuth Correction: "))
            elev = float(input("*    Elevation: "))
            res_stat = input("*    Restricted Status: ")
            loc = [loc]
            loc.extend(addloc.split(','))
            altnet = altnet.split(',')
        else:
            altnet = []
            loc = [loc]
            pol = 1.
            azcor = 0.
            elev = 0.
            res_stat = "?"

        nloc = []
        for al in loc:
            if len(al) == 0:
                nloc.append('--')
            else:
                nloc.append(al)
        loc = nloc

        # Contruct Key
        if opts.lkey:
            nkey = net.upper() + "." + stn.upper() + "." + chn.upper()
        else:
            nkey = net.upper() + "." + stn.upper()

        #- New DBElement
        NewDbEntry = StDbElement(network=net, altnet=altnet, station=stn, channel=chn, \
                         location=loc, latitude=lat, longitude=lon, elevation=elev, \
                         polarity=pol, azcorr=azcor, startdate=std, enddate=edd)

        # Add key if not present
        if nkey not in db:
            db[nkey] = NewDbEntry
            addnew = True
            print("* Added to DB")
        else:
            print("*")
            print("* Key Exists: " + nkey)
            print("* Existing: ")
            print(db[nkey](10))
            print("* New:")
            print(NewDbEntry(10))
            print("--------------")
            ovr = input("Overwrite Existing? [Y]/N: ")
            if ovr.lower() == "n":
                print("* Retaining Original")
            else:
                db[nkey] = NewDBEntry
                addnew = True
                print("* Added to DB")
        print("")
        newstn = input("* Another Station? [Y]/N: ")

    # Were any new stations added?
    if addnew:
        print("")
        print("Saving new database: " + opts.oname)
        write_db(fname=opts.oname, stdb=db, binp=opts.use_binary)
    else:
        print("")
        print("No changes made...")

