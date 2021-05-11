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
Program ``query_fdsn_stdb.py``
------------------------------

Description
-----------
Program to query a datacenter using the :mod:``obspy`` fdsn client. All stations 
returned based on the query criteria are saved into a both a ``.csv`` file and a 
stdb dictionary ``pickle`` file for future use.

Usage
-----

.. code-block:: none

    $ query_fdsn_stdb.py -h
    Usage: query_fdsn_stdb.py [options] <station list filename>

    Program to query a datacenter using the obspy fdsn client. All station
    returned in this query are saved into both a csv format 1sls file as well as a
    stationdb (stdb.StDbElement) pickled dictionary. The input argument, <station
    file name> is the prefix for the output file, which is by default <station
    file name>.csv and <station file name>.pkl.

    Options:
      -h, --help            show this help message and exit
      -D, --debug           Debug mode. After the client query is complete (and
                            successful), instead of parsing the inventory, it is
                            instead pickled to <station file name>_query_debug.pkl
                            which can be loaded in ipython to examine manually.
      --long-keys           Specify Key format. Default is Net.Stn. Long keys are
                            Net.Stn.Chn
      -a, --ascii           Specify to write ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

      Server Settings:
        Settings associated with which datacenter to log into.

        --Server=SERVER     Specify the server to connect to. Options include:
                            BGR, ETH, GEONET, GFZ, INGV, IPGP, IRIS, KOERI, LMU,
                            NCEDC, NEIP, NERIES, ODC, ORFEUS, RESIF, SCEDC, USGS,
                            USP. [Default IRIS]
        --User-Auth=USERAUTH
                            Enter your IRIS Authentification Username and Password
                            (--User-Auth='username:authpassword') to access and
                            download restricted data. [Default no user and
                            password]

      Channel Priority/Selection Settings:
        Settings associated with selecting the channels to retain.

        --channel-rank=CHNRANK
                            If requesting more than one type of channel, specify a
                            comma separated list of the first two lettres of the
                            desired components to retain. Default is HH > BH > LH
                            : [ 'HH','BH','LH']

      Station-Channel Settings:
        Options to narrow down the specific channels based on network,
        station, etc

        -N NETS, --networks=NETS
                            Specify a comma separated list of network codes to
                            search for [Default *]
        -S STNS, --stations=STNS
                            Specify a comma separated list of station names. If
                            you want wildcards, enclose in quotes [Default *]
        -C CHNS, --channels=CHNS
                            Specify a comma separated, wildcarded list of channel
                            names. [Default LH*,BH*,HH*]
        -L LOCS, --locations=LOCS
                            Specify a comma separated list of location ids. If you
                            want the default empty id, use "--". If you want a wild-
                            card, encluse in quotes. [Default *]

      Geographic Lat/Lon Box Search:
        Define the coordinates of a lat/lon box in which to select stations.
        If filled out, takes precedence over values for Radius Search (below).

        --minlat=MINLAT, --min-latitude=MINLAT
                            Specify minimum latitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --maxlat=MAXLAT, --max-latitude=MAXLAT
                            Specify maximum latitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --minlon=MINLON, --min-longitude=MINLON
                            Specify minimum longitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).
        --maxlon=MAXLON, --max-longitude=MAXLON
                            Specify maximum longitude to search (must specify all
                            of minlat, maxlat, minlon, maxlon).

      Geographic Radius Search:
        Central point and min/max radius search settings. Box Search Settings
        take precedence over radius search.

        --lat=LAT, --latitude=LAT
                            Specify a Lat (if any of --lon --min-radius and --max-
                            radius are empty, an error will prompt).
        --lon=LON, --longitude=LON
                            Specify a Lon (if any of --lat --min-radius and --max-
                            radius are empty, an error will prompt).
        --minr=MINR, --min-radius=MINR
                            Specify a minimum search radius (in degrees) around
                            the point defined by --lat and --lon (if any of --lat
                            --lon and --max-radius are empty, an error will
                            prompt). [Default 0. degrees]
        --maxr=MAXR, --max-radius=MAXR
                            Specify a maximum search radius (in degrees) around
                            the point defined by --lat and --lon (if any of --lat
                            --lon and --min-radius are empty, an error will
                            prompt).

      Fixed Time Range Settings:
        Find all stations operating within the start and end date/time. If
        either are filled out, they take precedence over Non-Specific time
        range search (below)

        --start=STDATE, --start-date=STDATE
                            Specify the Start Date/Time in a UTCDateTime
                            compatible String (ie, 2010-01-15 15:15:45.2).
                            [Default Blank]
        --end=ENDDATE, --end-date=ENDDATE
                            Specify the End Date/Time in a UTCDateTime compatible
                            String (ie, 2010-01-15 15:15:45.2). [Default Blank]

      Non-Specific Time Range Settings:
        Time settings with less specificity. Ensure that those you specify do
        not interfere with each other. If above Fixed Range values are set,
        they will take precedence over these values.

        --start-before=STBEFORE
                            Specify a Date/Time which stations must start before
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --start-after=STAFTER
                            Specify a Date/Time which stations must start after
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --end-before=ENDBEFORE
                            Specify a Date/Time which stations must end before
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]
        --end-after=ENDAFTER
                            Specify a Date/Time which stations must end after
                            (must be UTCDateTime compatible string, ie 2010-01-15
                            15:15:45.2). [Default empty]

"""

import pickle
from sys import exit
from sys import stdout
from os.path import exists
from os import system
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client
from stdb import StDbElement
from stdb import write_db


def get_options():
    '''
    subroutine to capture the optional inputs
    '''
    from os import remove as rmfile
    from optparse import OptionParser,OptionGroup
    
    parser = OptionParser(usage="Usage: %prog [options] <station list filename>", \
        description="Program to query a datacenter using the obspy fdsn client. " \
        "All station returned in this query are saved into both a csv format 1sls " \
        "file as well as a stationdb (stdb.StDbElement) pickled dictionary. The input " \
        "argument, <station file name> is the prefix for the output file, which is by " \
        "default <station file name>.csv and <station file name>.pkl.")
    
    # General Settings
    parser.add_option("-D", "--debug", action="store_true", dest="debug", default=False, \
        help="Debug mode. After the client query is complete (and successful), instead of " \
        "parsing the inventory, it is instead pickled to <station file name>_query_debug.pkl " \
        "which can be loaded in ipython to examine manually.")
    parser.add_option("--long-keys", action="store_true", dest="lkey", default=False, \
        help="Specify Key format. Default is Net.Stn. Long keys are Net.Stn.Chn")
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")
    
    # Server Settings
    ServerGroup = OptionGroup(parser, title="Server Settings", description="Settings associated with " \
        "which datacenter to log into.")
    ServerGroup.add_option("--Server", action="store", type=str, dest="Server", default="IRIS", \
        help="Specify the server to connect to. Options include: BGR, ETH, GEONET, GFZ, INGV, IPGP, " \
        "IRIS, KOERI, LMU, NCEDC, NEIP, NERIES, ODC, ORFEUS, RESIF, SCEDC, USGS, USP. [Default IRIS]")
    ServerGroup.add_option("--User-Auth", action="store", type=str, dest="UserAuth", default="", \
        help="Enter your IRIS Authentification Username and Password (--User-Auth='username:authpassword') " \
        "to access and download restricted data. [Default no user and password]")

    # Selection Settings
    SelectGroup = OptionGroup(parser, title="Channel Priority/Selection Settings", description="Settings " \
        "associated with selecting the channels to retain.")
    SelectGroup.add_option("--channel-rank", action="store", type=str, dest="chnrank", default="HH,BH,LH", \
        help="If requesting more than one type of channel, specify a comma separated list of the first two " \
        "lettres of the desired components to retain. Default is HH > BH > LH : ['HH,BH,LH']")

    # Channel Settings
    ChannelGroup=OptionGroup(parser, title="Station-Channel Settings", description="Options to narrow down " \
        "the specific channels based on network, station, etc")
    ChannelGroup.add_option("-N","--networks", action="store", type=str, dest="nets", default="*", \
        help="Specify a comma separated list of network codes to search for [Default *]")
    ChannelGroup.add_option("-S","--stations", action="store", type=str, dest="stns", default="*", \
        help="Specify a comma separated list of station names. If you want wildcards, enclose in quotes [Default *]")
    ChannelGroup.add_option("-L","--locations", action="store", type=str, dest="locs", default="*", \
        help="Specify a comma separated list of location codes. If you want wildcards, enclose in quotes [Default *]")
    ChannelGroup.add_option("-C","--channels", action="store", type=str, dest="chns", default="HH*,BH*,LH*", \
        help="Specify a comma separated, wildcarded list of channel names. [Default HH*,BH*,LH*]")
    
    # Geographic Settings
    BoxGroup = OptionGroup(parser, title="Geographic Lat/Lon Box Search", description="Define the coordinates " \
        "of a lat/lon box in which to select stations. If filled out, takes precedence over values for " \
        "Radius Search (below).")
    BoxGroup.add_option("--minlat","--min-latitude", action="store", type="float", dest="minlat", default=None, \
        help="Specify minimum latitude to search (must specify all of minlat, maxlat, minlon, maxlon).")
    BoxGroup.add_option("--maxlat","--max-latitude", action="store", type="float", dest="maxlat", default=None, \
        help="Specify maximum latitude to search (must specify all of minlat, maxlat, minlon, maxlon).")
    BoxGroup.add_option("--minlon","--min-longitude", action="store", type="float", dest="minlon", default=None, \
        help="Specify minimum longitude to search (must specify all of minlat, maxlat, minlon, maxlon).")
    BoxGroup.add_option("--maxlon","--max-longitude", action="store", type="float", dest="maxlon", default=None, \
        help="Specify maximum longitude to search (must specify all of minlat, maxlat, minlon, maxlon).")  
    RadGroup=OptionGroup(parser, title="Geographic Radius Search", description="Central point and min/max " \
        "radius search settings. Box Search Settings take precedence over radius search.")
    RadGroup.add_option("--lat","--latitude", action="store", type="float", dest="lat", default=None, \
        help="Specify a Lat (if any of --lon --min-radius and --max-radius are empty, an error will prompt).")
    RadGroup.add_option("--lon","--longitude", action="store", type="float", dest="lon", default=None, \
        help="Specify a Lon (if any of --lat --min-radius and --max-radius are empty, an error will prompt).")
    RadGroup.add_option("--minr","--min-radius", action="store", type="float", dest="minr", default=0., \
        help="Specify a minimum search radius (in degrees) around the point defined by --lat and --lon " \
        "(if any of --lat --lon and --max-radius are empty, an error will prompt). [Default 0. degrees]")
    RadGroup.add_option("--maxr","--max-radius", action="store", type="float", dest="maxr", default=None, \
        help="Specify a maximum search radius (in degrees) around the point defined by --lat and --lon " \
        "(if any of --lat --lon and --min-radius are empty, an error will prompt).")
    
    # Temporal Settings
    FixedRangeGroup = OptionGroup(parser, title="Fixed Time Range Settings", description="Find all stations " \
        "operating within the start and end date/time. If either are filled out, they take precedence over " \
        "Non-Specific time range search (below)")
    FixedRangeGroup.add_option("--start","--start-date", action="store", type=None, dest="stdate", default=None, \
        help="Specify the Start Date/Time in a UTCDateTime compatible String (ie, 2010-01-15 15:15:45.2). [Default Blank]")
    FixedRangeGroup.add_option("--end","--end-date", action="store", type=None, dest="enddate", default=None, \
        help="Specify the End Date/Time in a UTCDateTime compatible String (ie, 2010-01-15 15:15:45.2). [Default Blank]")
    
    VarRangeGroup = OptionGroup(parser, title="Non-Specific Time Range Settings", description="Time settings " \
        "with less specificity. Ensure that those you specify do not interfere with each other. If above Fixed " \
        "Range values are set, they will take precedence over these values.")
    VarRangeGroup.add_option("--start-before", action="store", type=None, dest="stbefore", default=None, \
        help="Specify a Date/Time which stations must start before (must be UTCDateTime compatible string, " \
        "ie 2010-01-15 15:15:45.2). [Default empty]")
    VarRangeGroup.add_option("--start-after", action="store", type=None, dest="stafter", default=None, \
        help="Specify a Date/Time which stations must start after (must be UTCDateTime compatible string, " \
        "ie 2010-01-15 15:15:45.2). [Default empty]")
    VarRangeGroup.add_option("--end-before", action="store", type=None, dest="endbefore", default=None, \
        help="Specify a Date/Time which stations must end before (must be UTCDateTime compatible string, " \
        "ie 2010-01-15 15:15:45.2). [Default empty]")
    VarRangeGroup.add_option("--end-after", action="store", type=None, dest="endafter", default=None, \
        help="Specify a Date/Time which stations must end after (must be UTCDateTime compatible string, " \
        "ie 2010-01-15 15:15:45.2). [Default empty]")
        
    # Add All Groups
    parser.add_option_group(ServerGroup)
    parser.add_option_group(SelectGroup)
    parser.add_option_group(ChannelGroup)
    parser.add_option_group(BoxGroup)
    parser.add_option_group(RadGroup)
    parser.add_option_group(FixedRangeGroup)
    parser.add_option_group(VarRangeGroup)

    # Run Parser
    (opts, args) = parser.parse_args()

    # Check output file name
    if len(args) != 1: parser.error("Need station database file")
    outpref = args[0]
    if not opts.debug:
        if exists(outpref + ".csv") and exists(outpref + ".pkl"):
            print ("Warning: Output Files " + outpref + ".csv and " + outpref + \
                ".pkl already exist. These will be overwritten...")
            rmfile(outpref + ".pkl");    rmfile(outpref + ".csv")
        elif exists(outpref + ".csv"):
            print ("Warning: Output File " + outpref + ".csv already exists. It will be overwritten...")
            rmfile(outpref + ".csv")
        elif exists(outpref + ".pkl"):
            print ("Warning: Output File " + outpref + ".pkl already exists. It will be overwritten...")
            rmfile(outpref + ".pkl")

    # Parse User Authentification
    if not len(opts.UserAuth) == 0:
        tt = opts.UserAuth.split(':')
        if not len(tt) == 2:
            parser.errer("Error: Incorrect Username and Password Strings for User Authentification")
        else:
            opts.UserAuth = tt
    else:
        opts.UserAuth = []
    
    # Parse Channel Rank to List
    opts.chnrank = opts.chnrank.split(',')
    
    # Check Geographic Settings
    if opts.minlat is not None or opts.maxlat is not None or opts.minlon is not None or opts.maxlon is not None:
        if opts.minlat is None or opts.maxlat is None or opts.minlon is None or opts.maxlon is None:
            # Not all value set
            opts.minlat = None; opts.maxlat = None; opts.minlon = None; opts.maxlon = None 
            print ("Warning: one of minlat,maxlat,minlon,maxlon were not set. All values reset to None. ")
            print ("")
        else:
            # Ensure proper min/max set
            tempminlat = min([opts.minlat,opts.maxlat]); tempmaxlat = max([opts.minlat,opts.maxlat])
            opts.minlat = tempminlat; opts.maxlat = tempmaxlat
            tempminlon = min([opts.minlon,opts.maxlon]); tempmaxlon = max([opts.minlon,opts.maxlon])
            opts.minlon = tempminlon; opts.maxlon = tempmaxlon
            print ("Performing Geographic Box Search:")
            print ("    LL: {0:9.4f}, {1:8.4f}".format(opts.minlat, opts.minlon))
            print ("    UR: {0:9.4f}, {1:8.4f}".format(opts.maxlat,opts.maxlon))
            print (" ")
            # set all other box parameters to none
            opts.minr = None; opts.maxr = None
            opts.lat = None; opts.lon = None

    elif opts.lat is not None or opts.lon is not None or opts.minr is not None or opts.maxr is not None:
        if opts.lat is None or opts.lon is None or opts.minr is None or opts.maxr is None:
            opts.lat = None; opts.lon = None; opts.minr = None; opts.maxr = None
            print ("Warning: one of lat,lon,minr,maxr were not set. All values reset to None. ")
            print (" ")
        else:
            # Ensure minr/maxr set
            opts.minr = min([opts.minr, opts.maxr]); opts.maxr = max([opts.minr, opts.maxr])
            print ("Performing Geographic Radius Search: ")
            print ("   Centre Point: {0:9.4f}, {1:8.4f}".format(opts.lon, opts.lat))
            print ("   Radius: {0:6.2f} to {1:6.2f} degrees".format(opts.minr, opts.maxr))
            print (" ")
    

    # Check Time Settings
    if opts.stdate is not None or opts.enddate is not None:
        # Use Fixed Range, not other
        opts.stbefore = None; opts.stafter = None; opts.endbefore = None; opts.endafter = None
        # Fix End Date
        if opts.enddate is None:
            opts.enddate = UTCDateTime("2599-12-31 23:59:59.9")
        else:
            opts.enddate = UTCDateTime(opts.enddate)
        # Assign stdate as UTCDateTime
        if opts.stdate is not None:
            opts.stdate = UTCDateTime(opts.stdate)
        print ("Performing Fixed Time Range Search: ")
        print ("   Start: " + opts.stdate.strftime("%Y-%m-%d %H:%M:%S"))
        print ("   End:   " + opts.enddate.strftime("%Y-%m-%d %H:%M:%S"))
        print (" ")
    else:
        # No Fixed Range Set. Are other values set?
        if opts.stbefore is not None or opts.stafter is not None or opts.endbefore is not None or opts.endafter is not None:
            print ("Performing Non-Specific Time Search: ")
            if opts.stbefore is not None:
                opts.stbefore = UTCDateTime(opts.stbefore)
                print ("   Start Before: " + opts.stbefore.strftime("%Y-%m-%d %H:%M:%S"))
            if opts.stafter is not None:
                opts.stafter = UTCDateTime(opts.stafter)
                print ("   Start After: " + opts.stafter.strftime("%Y-%m-%d %H:%M:%S"))
            if opts.endbefore is not None:
                opts.endbefore = UTCDateTime(opts.endbefore)
                print ("   End Before: " + opts.endbefore.strftime("%Y-%m-%d %H:%M:%S"))
            if opts.endafter is not None:
                opts.endafter = UTCDateTime(opts.endafter)
                print ("   End After: " + opts.endafter.strftime("%Y-%m-%d %H:%M:%S"))
            print (" ")
            
        else:
            print ("Warning: No Time Range Specified for Search")
            print (" ")
    
    # Station/Channel Search Parameters
    print ("Station/Channel Search Parameters:")
    print ("   Network:  {0:s}".format(opts.nets))
    print ("   Stations: {0:s}".format(opts.stns))
    print ("   Locations: {0:s}".format(opts.locs))
    print ("   Channels: {0:s}".format(opts.chns))
    print ("   Channel Rank: {0:s}".format(",".join(opts.chnrank)))
    print (" ")
    if opts.debug:
        print ("Output Files: {0:s}_query_debug.pkl and {0:s}_query_debug.kcsv".format(outpref))
    else:
        print ("Output Files: {0:s}.csv and {0:s}.pkl".format(outpref))
    print (" ")
    
    # Return Values
    return opts, outpref


if __name__=='__main__':

    # Get Input Options
    (opts, outp) = get_options()

    # Initialize the client
    stdout.writelines("Initializing Client ({0:s})...".format(opts.Server))
    if len(opts.UserAuth) == 0:
        client = Client(opts.Server)
    else:
        client = Client(opts.Server, user=opts.UserAuth[0], password=opts.UserAuth[1])
    stdout.writelines("Done\n\n")
    
    # Search the Client for stations
    stdout.writelines("Querying client...")
    try:
        inv = client.get_stations(network=opts.nets, station=opts.stns, channel=opts.chns, location=opts.locs,
                starttime=opts.stdate, endtime=opts.enddate, 
                startbefore=opts.stbefore, startafter=opts.stafter, endbefore=opts.endbefore, endafter=opts.endafter, 
                latitude=opts.lat, longitude=opts.lon, minradius=opts.minr, maxradius=opts.maxr,
                minlatitude=opts.minlat, maxlatitude=opts.maxlat, minlongitude=opts.minlon, maxlongitude=opts.maxlon,
                includeavailability=None, includerestricted=True, level='channel')
        stdout.writelines("Done\n\n")
    except:
        print ('Exception: Cannot complete query or no data in query...')
        exit()
    
    # Summarize Search
    nstn = 0
    for net in inv.networks:
        for stn in net.stations:
            nstn = nstn + 1
    print ("Search Complete: ")
    print ("  {0:d} stations in {1:d} networks".format(nstn, len(inv.networks)))
    print (" ")
    
    # If Debug mode, pickle inventory and exit
    if opts.debug:
        stdout.writelines("Pickling Inventory into {0:s}_query_debug.pkl...".format(outp))
        pickle.dump(inv, open('{0:s}_query_debug.pkl'.format(outp),'wb'))
        stdout.writelines("Done\n\n")
        stdout.writelines("Writing csv2kml format file to {0:s}_query_debug.kcsv\n".format(outp))
        fcsv=open("{0:s}_query_debug.kcsv".format(outp), 'w')
        for net in inv.networks:
            for stn in net.stations:
                lat = stn.latitude; lon = stn.longitude; stdt = stn.start_date; eddt = stn.end_date
                fcsv.writelines("{0:11.6f},{1:10.6f},{2:2s},{3:5s},{4:s},{5:s}\n".format(\
                    lon, lat, net.code, stn.code, stdt.strftime("%Y-%m-%d"), eddt.strftime("%Y-%m-%d")))
        fcsv.close()
        aa = system("csv2kml --field-names='lon,lat,net,station,start,end' {0:s}_query_debug.kcsv".format(outp))
        if aa == 0:
            print ("Generated a KML file {0:s}_query_debug.kcsv.kml".format(outp))
        else:
            print ("Generate a kml file using: ")
            print ("   csv2kml --no-random-colours --field-names='lon,lat,net,station,start,end' " \
                "{0:s}_query_debug.kcsv".format(outp))
        
        exit()
    
    #-- Split locations for later parsing
    opts.locs=opts.locs.split(',')
    #-- Sort selected location keys
    for i,l in enumerate(opts.locs):
        if len(l)==0:
            opts.locs[i]=="--"

    # Initialize station dictionary
    stations = {}
    
    # Loop through results
    for net in inv.networks:
        network = net.code.upper()
        print ("Network: {0:s}".format(network))
        for stn in net.stations:
            station = stn.code.upper()
            print ("   Station: {0:s}".format(station))

            # get standard values
            lat = stn.latitude; lon = stn.longitude; elev = stn.elevation/1000.;
            stdt = stn.start_date
            if stn.end_date is None:
                eddt = UTCDateTime("2599-12-31")
            else:
                eddt = stn.end_date
            stat = stn.restricted_status

            print ("     Lon, Lat, Elev: {0:9.4f}, {1:8.4f}, {2:7.3f}".format(lon, lat, elev))
            print ("     Start Date: {0:s}".format(stdt.strftime("%Y-%m-%d %H:%M:%S")))
            print ("     End Date:   {0:s}".format(eddt.strftime("%Y-%m-%d %H:%M:%S")))
            print ("     Status:     {0:s}".format(stat))

            # Parse Channels
            if opts.lkey:
                # Select Multiple Channels based on those in the rank list
                # Do not keep overlapping time windows
                # Select Channels based on those available compared to channel rank
                chn = []
                for pchn in opts.chnrank:
                    stnchn = stn.select(channel=pchn + "Z")
                    if len(stnchn.channels) > 0:
                        chn.append(pchn)
                
                #-- If no channels with Z found, skip        
                if chn is None:
                    if len(stn.select(channel='*Z')) == 0:
                        print ("     Error: No Z component. Skipping")
                        continue

                #-- loop through channels and select time windows
                for pchn in chn:
                    locs=[]; stdts=[]; eddts=[]
                    stnchn = stn.select(channel=pchn + "Z")
                    #--Collect Start/end Dates and locations
                    for chnl in stnchn:
                        chnlloc=chnl.location_code
                        if len(chnlloc)==0: chnlloc="--"
                        for selloc in opts.locs:
                            # print (selloc, chnlloc)
                            if selloc == '*' or chnlloc in selloc:
                                locs.append(chnlloc)
                                stdts.append(chnl.start_date)
                                if chnl.end_date is None:
                                    eddts.append(UTCDateTime("2599-12-31"))
                                else:
                                    eddts.append(chnl.end_date)

                    #-- Unique set of locids, get minmax time for channel across all locids
                    locs=list(set(locs))
                    stdts.sort(); eddts.sort()
                    stnchnstdt=stdts[0]; stnchneddt=eddts[-1]                    

                    print ("       Selected Channel: {0:s}".format(pchn))
                    print ("         Locations:  {0:s}".format(",".join(locs)))
                    print ("         Start Date: {0:s}".format(stnchnstdt.strftime("%Y-%m-%d %H:%M:%S")))
                    print ("         End Date:   {0:s}".format(stnchneddt.strftime("%Y-%m-%d %H:%M:%S")))
                    

                    #-- Add single key to station database
                    key = "{0:s}.{1:s}.{2:2s}".format(network, station, pchn)
                    if key not in stations:
                        stations[key] = StDbElement(network=network, station=station, channel=pchn, \
                            location=locs, latitude=lat, longitude=lon, elevation=elev, polarity=1., \
                            azcorr=0., startdate=stnchnstdt, enddate=stnchneddt, restricted_status=stat)
                        print ("       Added as: " + key)
                    else:
                        print ("       Warning: " + key + " already exists...Skip")
                        
            else:
                # Select a single channel type if only short keys
                chn = None; locs = []; stdts=[]; eddts=[]
                for pchn in opts.chnrank:
                    stnchn = stn.select(channel=pchn + "Z")
                    if len(stnchn.channels) > 0:
                        chn = pchn
                         #--Collect Start/end Dates and locations
                        for chnl in stnchn:
                            chnlloc=chnl.location_code
                            if len(chnlloc)==0: chnlloc="--"
                            for selloc in opts.locs:
                                # print (selloc, chnlloc)
                                if selloc == '*' or chnlloc in selloc:
                                    locs.append(chnlloc)
                                    stdts.append(chnl.start_date)
                                    if chnl.end_date is None:
                                        eddts.append(UTCDateTime("2599-12-31"))
                                    else:
                                        eddts.append(chnl.end_date)
                        if len(locs)>0:
                            break
                
                if chn is None:
                    if len(stn.select(channel='*Z')) == 0:
                        print ("     Error: No Z component. Skipping")
                        continue
                if len(locs) ==0:
                	print("     Error: Location {} not available. Skipping".format(",".join(opts.locs)))
                	continue

                #-- Unique set of locids, get minmax time for channel across all locids
                locs=list(set(locs))
                stdts.sort(); eddts.sort()
                stnchnstdt=stdts[0]; stnchneddt=eddts[-1]  

                # # return location codes for selected channel
                # locs = list(set([a.location_code for a in stn.select(channel=chn+'Z').channels]))
                
                # print ("     Selected Channel: {0:s}".format(chn))
                # print ("     Locations:        {0:s}".format(",".join(locs)))
        
                print ("       Selected Channel: {0:s}".format(pchn))
                print ("         Locations:  {0:s}".format(",".join(locs)))
                print ("         Start Date: {0:s}".format(stnchnstdt.strftime("%Y-%m-%d %H:%M:%S")))
                print ("         End Date:   {0:s}".format(stnchneddt.strftime("%Y-%m-%d %H:%M:%S")))
                    

                key = "{0:s}.{1:s}".format(network, station)

                #-- Add single key to station database
                if key not in stations:
                    stations[key] = StDbElement(network=network, station=station, channel=chn, \
                        location=locs, latitude=lat, longitude=lon, elevation=elev, polarity=1., \
                        azcorr=0., startdate=stdt, enddate=eddt, restricted_status=stat)
                    print ("    Added as: " + key)
                else:
                    print ("    Warning: " + key + " already exists...Skip")
            print ()

    # Save and Pickle
    print (" ")
    print ("  Pickling to {0:s}.pkl".format(outp))
    write_db(fname=outp + '.pkl', stdb=stations, binp=opts.use_binary)

    # Save csv
    print ("  Saving csv to: {0:s}.csv".format(outp))
    fcsv = open(outp + ".csv",'w')
    stkeys = stations.keys()
    sorted(stkeys) # python3!

    for stkey in stkeys:
        #                 net    stn   locs   chn   std      stt         edd      edt          lat       lon       elev       pol      azc       res
        fcsv.writelines("{0:s},{1:s},{2:s},{3:s}*,{4:s},{5:s}.{6:1.0f},{7:s},{8:s}.{9:1.0f},{10:8.4f},{11:9.4f},{12:6.2f},{13:3.1f},{14:8.4f},{15:s}\n".format( 
             stations[stkey].network, stations[stkey].station, ":".join(stations[stkey].location), stations[stkey].channel[0:2],
             stations[stkey].startdate.strftime("%Y-%m-%d"), stations[stkey].startdate.strftime("%H:%M:%S"), stations[stkey].startdate.microsecond/100000.,
             stations[stkey].enddate.strftime("%Y-%m-%d"), stations[stkey].enddate.strftime("%H:%M:%S"), stations[stkey].enddate.microsecond/100000.,
             stations[stkey].latitude, stations[stkey].longitude, stations[stkey].elevation, stations[stkey].polarity, stations[stkey].azcorr, stations[stkey].status))
