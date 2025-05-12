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
Program ``gen_stdb``
--------------------

Description
-----------
Create Station Database dictionary
The station dictionary contains keys that are named NET.STA.CHAN, where CHAN
is a two character representation of the desired channel (ex, BH, HH, LH).
Within each KEY is the set of data used in later programs to define the 
station information. The data is stored in a dictionary, with each dictionary 
element being an object of Class :class:`~stdb.classes.StDbElement`. An item has:

Usage
-----

.. code-block:: none

    gen_stdb -h
    Usage: gen_stdb [options] <station list>

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
"""


from sys import exit
import os.path as osp
from obspy.core import UTCDateTime
from stdb import write_db
from stdb import StDbElement
from optparse import OptionParser


class MyParser(OptionParser):
    def format_epliog(self, formatter):
        return self.epilog


def main(args=None):

    # Get options
    parser = MyParser(
        usage="Usage: %prog [options] <station list>",
        description="Script to generate a pickled station database file.",
        epilog="""Input File Type 1 (chS csv):                                                
NET[:NET2:...],STA,LOC[:LOC2:...],CHN,YYYY-MM-DD,HH:MM:SS.SSS,YYYY-MM-DD,HH:MM:SS.SSS,lat,lon,elev,pol,azcor,status
                                                                                                            
Input File Type 2 (IPO SPC):                                                                            
NET STA CHAN lat lon elev YYYY-MM-DD YYYY-MM-DD                                                     
                                                                                                    
                                                                                                                                        
Output File Types:                                                            
Each element corresponding to each dictionary key is saved as StDb.StbBElement class.                                         
                                                                                                                                                                                                                                                    
""")
    parser.add_option(
        "-L",
        "--long-keys",
        action="store_true",
        dest="lkey",
        default=False,
        help="Specify Key format. Default is Net.Stn. " +
        "Long keys are Net.Stn.Chn")
    parser.add_option(
        "-a",
        "--ascii",
        action="store_false",
        dest="use_binary",
        default=True,
        help="Specify to write ascii Pickle files instead of binary. " +
        "Ascii are larger file size, but more likely to be system " +
        "independent.")
    (opts, args) = parser.parse_args()

    if not osp.exists(args[0]):
        parser.error("Input File " + args[0] + " does not exist")

    # Check Extension
    ofn, ext = osp.splitext(args[0])
    if (ext == ".pkl") or (ext not in ['.txt', '.csv', '.xml']):

        print(
            "Error: Must supply a station list in text or .xml format " +
            "(.txt, .csv, .xml)")
        exit()

    elif ext in ['.txt', '.csv']:

        # Station List...Pickle it.
        print("Parse Station List: " + args[0])

        pklfile = ofn + ".pkl"

        fin = open(args[0], 'r')
        stations = {}
        for line in fin:
            line = line.strip()
            if len(line) == 0 or line[0] == "#":
                continue
            if len(line.split(',')) > 6:
                line = line.split(',')

                # Networks
                nets = line[0].split(':')
                if len(nets) == 1:
                    net = nets[0]
                    altnet = []
                else:
                    net = nets[0]
                    altnet = nets[1:]

                # Required Station Parameters
                stn = line[1]
                # Required Location Parameters
                loc = line[2].split(':')
                # Required Channel Parmaeters
                chn = line[3][0:2]
                # Required Timing Parameters
                stdt = UTCDateTime(line[4])
                sttm = line[5]
                eddt = UTCDateTime(line[6])
                edtm = line[7]
                # Required Position Parameters
                lat = float(line[8])
                lon = float(line[9])

                # Set Default values for Optional elements
                elev = 0.
                pol = 1.
                azcor = 0.
                status = ""
                if len(line) >= 11:
                    elev = float(line[10])
                if len(line) >= 12:
                    pol = float(line[11])
                if len(line) >= 13:
                    azcor = float(line[12])
                if len(line) == 14:
                    status = line[13]

            elif len(line.split()) > 6 or len(line.split('\t')) > 6:
                if len(line.split()) > 6:
                    line = line.split()
                else:
                    line = line.split('\t')
                net = line[0]
                stn = line[1]
                chn = line[2][0:2]
                stdt = UTCDateTime(line[6])
                eddt = UTCDateTime(line[7])
                lat = float(line[3])
                lon = float(line[4])
                elev = float(line[5])
                altnet = []
                status = ""
                azcor = 0.
                pol = 0.
                loc = ""

            # Now Add lines to station Dictionary
            if opts.lkey:
                key = "{0:s}.{1:s}.{2:2s}".format(
                    net.strip(), stn.strip(), chn.strip())
            else:
                key = "{0:s}.{1:s}".format(
                    net.strip(), stn.strip())
            if key not in stations:
                stations[key] = StDbElement(
                    network=net,
                    station=stn,
                    channel=chn,
                    location=loc,
                    latitude=lat,
                    longitude=lon,
                    elevation=elev,
                    polarity=pol,
                    azcorr=azcor,
                    startdate=stdt,
                    enddate=eddt,
                    restricted_status=status)
                print("Adding key: " + key)
            else:
                print("Warning: Key " + key + " already exists...Skip")

        # import pprint
        # print(stations.keys())
        # pprint.pprint(stations['TA.M31M'])

        # Save and Pickle the station database
        print("  Pickling {0:s}".format(pklfile))
        write_db(fname=pklfile, stdb=stations, binp=opts.use_binary)

    # This is from query_fdsn_stdb, with some tweaks
    elif ext == '.xml':

        from obspy import read_inventory

        # Station List...Pickle it.
        print("Parse Station XML: " + args[0])

        pklfile = ofn + ".pkl"

        inv = read_inventory(args[0])

        # Summarize Search
        nstn = 0
        for net in inv.networks:
            for stn in net.stations:
                nstn = nstn + 1
        print("Search Complete: ")
        print("  {0:d} stations in {1:d} networks".format(
            nstn, len(inv.networks)))
        print(" ")

        # # Split locations for later parsing
        # opts.locs = opts.locs.split(',')
        # # Sort selected location keys
        # for i, l in enumerate(opts.locs):
        #     if len(l) == 0:
        #         opts.locs[i] == "--"

        # Initialize station dictionary
        stations = {}

        # Loop through results
        for net in inv.networks:
            network = net.code.upper()
            print("Network: {0:s}".format(network))
            for stn in net.stations:
                station = stn.code.upper()
                print("   Station: {0:s}".format(station))

                # get standard values
                lat = stn.latitude
                lon = stn.longitude
                elev = stn.elevation/1000.
                stdt = stn.start_date
                if stn.end_date is None:
                    eddt = UTCDateTime("2599-12-31")
                else:
                    eddt = stn.end_date
                stat = stn.restricted_status
                if stat is None:
                    stat = "Unknown"

                print(
                    "     Lon, Lat, Elev: {0:9.4f}, {1:8.4f}, {2:7.3f}".format(
                        lon, lat, elev))
                print(
                    "     Start Date: {0:s}".format(
                       stdt.strftime("%Y-%m-%d %H:%M:%S")))
                print(
                    "     End Date:   {0:s}".format(
                       eddt.strftime("%Y-%m-%d %H:%M:%S")))
                print(
                    "     Status:     {0:s}".format(stat))

                # Parse Channels
                if opts.lkey:
                    # Select Multiple Channels based on those in the rank list
                    # Do not keep overlapping time windows
                    # Select Channels based on those available compared to
                    # channel rank
                    chn = []
                    vcomp = "Z"
                    for pchn in ['HH', 'BH', 'CH', 'LH', 'EH', 'SH']:
                        stnchn = stn.select(channel=pchn + vcomp)
                        if len(stnchn.channels) > 0:
                            chn.append(pchn)
                        else:
                            stnchn = stn.select(channel=pchn + "3")
                            if len(stnchn.channels) > 0:
                                chn.append(pchn)
                                vcomp = "3"

                    # If no channels with Z found, skip
                    if chn is None:
                        if (len(stn.select(channel='*Z')) == 0) and (len(sta.select(channel='*3')) == 0):
                            print(
                                "     Error: No Vertical (Z/3) component. " +
                                "Skipping")
                            continue

                    # loop through channels and select time windows
                    for pchn in chn:
                        locs = []
                        stdts = []
                        eddts = []
                        stnchn = stn.select(channel=pchn + vcomp)
                        # Collect Start/end Dates and locations
                        for chnl in stnchn:
                            chnlloc = chnl.location_code
                            if len(chnlloc) == 0:
                                chnlloc = "--"
                            for selloc in ['*']:
                                # print(selloc, chnlloc)
                                if selloc == '*' or chnlloc in selloc:
                                    locs.append(chnlloc)
                                    stdts.append(chnl.start_date)
                                    if chnl.end_date is None:
                                        eddts.append(UTCDateTime("2599-12-31"))
                                    else:
                                        eddts.append(chnl.end_date)

                        # Unique set of locids
                        # get minmax time for channel across all locids
                        locs = list(set(locs))
                        stdts.sort()
                        eddts.sort()
                        stnchnstdt = stdts[0]
                        stnchneddt = eddts[-1]

                        print(
                            "       Selected Channel: {0:s}".format(pchn))
                        print(
                            "         Locations:  {0:s}".format(
                                ",".join(locs)))
                        print(
                            "         Start Date: {0:s}".format(
                               stnchnstdt.strftime("%Y-%m-%d %H:%M:%S")))
                        print(
                            "         End Date:   {0:s}".format(
                               stnchneddt.strftime("%Y-%m-%d %H:%M:%S")))

                        # Add single key to station database
                        key = "{0:s}.{1:s}.{2:2s}".format(
                            network, station, pchn)
                        if key not in stations:
                            stations[key] = StDbElement(
                                network=network,
                                station=station,
                                channel=pchn,
                                location=locs,
                                latitude=lat,
                                longitude=lon,
                                elevation=elev,
                                polarity=1.,
                                azcorr=0.,
                                startdate=stnchnstdt,
                                enddate=stnchneddt,
                                restricted_status=stat)
                            print(
                                "       Added as: " + key)
                        else:
                            print(
                                "       Warning: " + key +
                                " already exists...Skip")

                else:
                    # Select a single channel type if only short keys
                    chn = None
                    locs = []
                    stdts = []
                    eddts = []
                    for pchn in ['HH', 'BH', 'CH', 'LH', 'EH', 'SH']:
                        vcomp = "Z"
                        stnchn = stn.select(channel=pchn + "Z")
                        if len(stnchn.channels) > 0:
                            vcomp = "Z"
                        else:
                            stnchn = stn.select(channel=pchn + "3")
                            if len(stnchn.channels) > 0:
                                vcomp = "3"

                        stnchn = stn.select(channel=pchn + vcomp)

                        if len(stnchn.channels) > 0:
                            chn = pchn

                            # Collect Start/end Dates and locations
                            for chnl in stnchn:
                                chnlloc = chnl.location_code
                                if len(chnlloc) == 0:
                                    chnlloc = "--"
                                for selloc in ['*']:
                                    # print(selloc, chnlloc)
                                    if selloc == '*' or chnlloc in selloc:
                                        locs.append(chnlloc)
                                        stdts.append(chnl.start_date)
                                        if chnl.end_date is None:
                                            eddts.append(
                                                UTCDateTime("2599-12-31"))
                                        else:
                                            eddts.append(chnl.end_date)
                            if len(locs) > 0:
                                break

                    if chn is None:
                        if (len(stn.select(channel='*Z')) == 0) and (len(stn.select(channel='*3')) == 0):
                            print(
                                "     Error: No Vertical (Z/3) component. " +
                                "Skipping")
                            continue
                    # if len(locs) == 0:
                    #     print(
                    #         "     Error: Location {} not available. " +
                    #         "Skipping".format(
                    #             ",".join(['*'])))
                    #     continue

                    #  Unique set of locids
                    #  get minmax time for channel across all locids
                    locs = list(set(locs))
                    stdts.sort()
                    eddts.sort()
                    stnchnstdt = stdts[0]
                    stnchneddt = eddts[-1]

                    # # return location codes for selected channel
                    # locs = list(set([a.location_code for a in stn.select(
                    # channel=chn+'Z').channels]))

                    # print("     Selected Channel: {0:s}".format(chn))
                    # print("     Locations:        {0:s}".format(
                    # ",".join(locs)))

                    print(
                        "       Selected Channel: {0:s}".format(pchn))
                    print(
                        "         Locations:  {0:s}".format(",".join(locs)))
                    print(
                        "         Start Date: {0:s}".format(
                            stnchnstdt.strftime("%Y-%m-%d %H:%M:%S")))
                    print(
                        "         End Date:   {0:s}".format(
                            stnchneddt.strftime("%Y-%m-%d %H:%M:%S")))

                    key = "{0:s}.{1:s}".format(network, station)

                    # Add single key to station database
                    if key not in stations:
                        stations[key] = StDbElement(
                            network=network,
                            station=station,
                            channel=chn,
                            location=locs,
                            latitude=lat,
                            longitude=lon,
                            elevation=elev,
                            polarity=1.,
                            azcorr=0.,
                            startdate=stnchnstdt,
                            enddate=stnchneddt,
                            restricted_status=stat)
                        print("    Added as: " + key)
                    else:
                        print("    Warning: " + key + " already exists...Skip")
                print()

        # Save and Pickle
        print(" ")
        print("  Pickling to {0:s}.pkl".format(pklfile))
        write_db(fname=pklfile, stdb=stations, binp=opts.use_binary)

        # Save csv
        outp = ofn + ".csv"
        print("  Saving csv to: {0:s}".format(outp))
        fcsv = open(outp, 'w')
        stkeys = stations.keys()

        for stkey in sorted(stkeys):
            # net, stn, locs, chn, std, stt, edd, edt, lat, lon, elev, pol, azc, res
            out = ("{0:s},{1:s},{2:s},{3:s}*,{4:s},{5:s}.{6:1.0f},{7:s},"
                   "{8:s}.{9:1.0f},{10:8.4f},{11:9.4f},{12:6.2f},{13:3.1f},"
                   "{14:8.4f},{15:s}\n").format(
                   stations[stkey].network,
                   stations[stkey].station, ":".join(stations[stkey].location),
                   stations[stkey].channel[0:2],
                   stations[stkey].startdate.strftime("%Y-%m-%d"),
                   stations[stkey].startdate.strftime("%H:%M:%S"),
                   stations[stkey].startdate.microsecond/100000.,
                   stations[stkey].enddate.strftime("%Y-%m-%d"),
                   stations[stkey].enddate.strftime("%H:%M:%S"),
                   stations[stkey].enddate.microsecond/100000.,
                   stations[stkey].latitude,
                   stations[stkey].longitude,
                   stations[stkey].elevation,
                   stations[stkey].polarity,
                   stations[stkey].azcorr,
                   stations[stkey].status)
            fcsv.writelines(out)


if __name__ == '__main__':

    main()
