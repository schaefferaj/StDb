#!/usr/bin/env python3
# encoding: utf-8

# Copyright 2021 Taylor Tracey Kyryliuk
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
Program ``remove_stdb``
---------------------------

Description
-----------
Program to remove listed stations from stdb ''pkl'' and ''csv'' files.


Usage
-----

.. code-block:: none

    $ remove_stdb -h
    Usage: remove_stdb [options] <station list filename (w/o extension)>

    Program to remove stations from stdb ''csv'' and ''pkl'' files. 

    Options:
      -h, --help            show this help message and exit
      -a, --ascii           Specify to read ascii Pickle files instead of binary.
                            Ascii are larger file size, but more likely to be
                            system independent.

      Station-Channel Settings:
        Options to narrow down the specific channels based on network,
        station, etc

        -N NETS, --networks=NETS
                            Specify a comma separated list of network codes to
                            remove [Default none]
        -S STNS, --stations=STNS
                            Specify a comma separated list of station names. If
                            you want wildcards, enclose in quotes [Default none]
        -C CHNS, --channels=CHNS
                            Specify a comma separated, wildcarded list of channel
                            names, enclose in quotes. [Default LH*,BH*,HH*]

"""

import pickle
from sys import exit
from sys import stdout
from os.path import exists
from os import system
from obspy.core import UTCDateTime
from obspy.clients.fdsn import Client
from stdb import StDbElement, write_db, load_db



def get_options():
    '''
    subroutine to capture the optional inputs
    '''
    from os import remove as rmfile
    from optparse import OptionParser,OptionGroup
    
    parser = OptionParser(usage="Usage: %prog [options] <station list filename>", \
        description="Program to remove stations from stdb ''csv'' and ''pkl'' files. ")
    
    # General Settings
    parser.add_option("-a", "--ascii", action="store_false", dest="use_binary", default=True, \
        help="Specify to write ascii Pickle files instead of binary. Ascii are larger file size, " \
        "but more likely to be system independent.")

    # Channel Settings
    ChannelGroup=OptionGroup(parser, title="Station-Channel Settings", description="Options to narrow down " \
        "the specific channels based on network, station, etc")
    ChannelGroup.add_option("-N","--networks", action="store", type=str, dest="nets", default=None, \
        help="Specify a comma separated list of network codes to remove [Default None]")
    ChannelGroup.add_option("-S","--stations", action="store", type=str, dest="stns", default=None, \
        help="Specify a comma separated list of station names to remove [Default None]")
    ChannelGroup.add_option("-C","--channels", action="store", type=str, dest="chns", default="HH*,BH*,LH*", \
        help="Specify a comma separated, wildcarded list of channel names, enclose in quotes. [Default HH*,BH*,LH*]")

        
    # Add All Groups
    parser.add_option_group(ChannelGroup)

    # Run Parser
    (opts, args) = parser.parse_args()

    # Check output file name
    if len(args) != 1: parser.error("Need station database file")
    inpref = args[0]
    if not exists(inpref + ".csv") and not exists(inpref + ".pkl"):
        print ("Warning: Input Files " + inpref + ".csv and " + inpref + \
            ".pkl do not exist. Aborting.")
        return -1,-1
    elif not exists(inpref + ".csv"):
        print ("Warning: Input File " + inpref + ".csv does not exist. It will be created.")
    elif not exists(inpref + ".pkl"):
        print ("Warning: Input File " + inpref + ".pkl does not exist. Only .csv will be changed.")


    # Station/Channel Removal Parameters
    print ("Station/Channel Removal Parameters:")
    print ("   Network:  {0:s}".format(str(opts.nets)))
    print ("   Stations: {0:s}".format(str(opts.stns)))
    print ("   Channels: {0:s}".format(opts.chns))
    print (" ")
    
    print ("Input Files: {0:s}.csv and {0:s}.pkl".format(inpref))
    print (" ")
    
    # Return Values
    return opts, inpref


def main(args=None):

    # Get Input Options
    (opts, inp) = get_options()
    
    if opts == -1:
        # Aborting
        return
    
    # Properly format strings into lists of strings
    if opts.nets != None: opts.nets = opts.nets.split(',')   
    if opts.stns != None: opts.stns = opts.stns.split(',') 

    opts.chns = opts.chns.split(',')
    if opts.chns != ['*']:
        # If the end of any of the specified channels are wildcard remove it
        opts.chns = [ch[:-1] for ch in opts.chns if ch[-1] == "*"]

    if exists(inp+'.pkl'):
        # Load pkl file 
        stdb = StDbElement(load_db(inp+'.pkl'))
        stdb = stdb['station']
        
        if opts.nets == ['*']:
            # User specified wildcard for networks
            # Use all networks from stdb
            all_nets = [stdb[x]['network'] for x in stdb]
            # Get unique list of networks
            opts.nets = list(set(all_nets))
        
        if opts.stns == ['*']:
            # User specified wildcard for stations
            # Use all stations from specified networks
            opts.stns = [stdb[x]['station'] for x in stdb if stdb[x]['network'] in opts.nets]

        if opts.chns == ['*']:
            # User specified wildcard for channels
            # Use all channels from specified networks
            all_chns = [stdb[x]['channel'] for x in stdb if stdb[x]['network'] in opts.nets]
            # Get unique list of channels
            opts.chns = list(set(all_chns))


        # REMOVE DESIRED STATIONS
        if opts.nets != None and opts.stns == None:
            # For each network, remove all stations with correct channels
            for net in opts.nets:  
                print ("  Removing stations with Network:  {0:s}".format(str(net)))
                # Go through each station in the stdb, is the network the same? 
                for station in stdb.copy():
                    if stdb[station]['network'] == net and (stdb[station]['channel'][:2] in opts.chns or stdb[station]['channel'] in opts.chns):
                        print("Removing Station {0:s}".format(str(stdb[station]['station'])))
                        del stdb[station]
                
        elif opts.nets != None and opts.stns != None:
            # For each network, remove specified stations with correct channels.
            for net in opts.nets:      

                for sta in opts.stns:
                    for station in stdb.copy():
                        if stdb[station]['station'] == sta and stdb[station]['network'] == net and (stdb[station]['channel'][:2] in opts.chns or stdb[station]['channel'] in opts.chns):
                            print("Removing Station {0:s}".format(str(stdb[station]['station'])))
                            del stdb[station]
                
        elif opts.nets == None and opts.stns != None:            
            # Remove user specified stations with correct channels, regardless of network
            for sta in opts.stns:
                for station in stdb.copy():
                    if stdb[station]['station'] == sta and (stdb[station]['channel'][:2] in opts.chns or stdb[station]['channel'] in opts.chns):
                        print("Removing Station {0:s}".format(str(stdb[station]['station'])))
                        del stdb[station]     
            
        elif opts.nets == None and opts.stns == None:
            # Do nothing <:O)
            print ("Nothing to remove.")

        # Write over the .pkl file
        print(" ")
        print("  Pickling to {0:s}.pkl".format(inp))
        write_db(fname=inp + '.pkl', stdb=stdb, binp=opts.use_binary)
        
        
        # Save csv
        print ("  Saving csv to {0:s}.csv".format(inp))
        fcsv = open(inp + ".csv",'w')
        stkeys = stdb.keys()
        sorted(stkeys) # python3!
        for stkey in stkeys:
            #                 net    stn   locs   chn   std      stt         edd      edt          lat       lon       elev       pol      azc       res
            fcsv.writelines("{0:s},{1:s},{2:s},{3:s}*,{4:s},{5:s}.{6:1.0f},{7:s},{8:s}.{9:1.0f},{10:8.4f},{11:9.4f},{12:6.2f},{13:3.1f},{14:8.4f},{15:s}\n".format( 
                 stdb[stkey].network, stdb[stkey].station, ":".join(stdb[stkey].location), stdb[stkey].channel[0:2],
                 stdb[stkey].startdate.strftime("%Y-%m-%d"), stdb[stkey].startdate.strftime("%H:%M:%S"), stdb[stkey].startdate.microsecond/100000.,
                 stdb[stkey].enddate.strftime("%Y-%m-%d"), stdb[stkey].enddate.strftime("%H:%M:%S"), stdb[stkey].enddate.microsecond/100000.,
                 stdb[stkey].latitude, stdb[stkey].longitude, stdb[stkey].elevation, stdb[stkey].polarity, stdb[stkey].azcorr, stdb[stkey].status))
    elif exists(inp+'.csv'):
        # Load .csv file
        
        reader = open(inp + ".csv",'r')
        data = list(reader)

        # Turn the string into a list using the comma delimeter
        data_copy = [x.split(',') for x in data ]

        if opts.nets == ['*']:
            # User specified wildcard for network
            # Get all networks from the data
            all_nets = [st[0] for st in data_copy]
            # Get a unique list of networks
            opts.nets = list(set(all_nets))
        
        if opts.stns == ['*']:
            # User specifid wildcard for station
            # Get all stations under opts.nets
            opts.stns = [st[1] for st in data_copy if st[0] in  opts.nets]

        if opts.chns == ['*']:
            # User specified wildcard for channels 
            # Get all possible channels under opts.nets
            all_chns = [st[3] for st in data_copy if st[0] in opts.nets]
            # Get a unique list of channels
            opts.chns = list(set(all_chns))

        # Only keep data that is not in the list of things to remove
        if opts.nets != None and opts.stns == None:
            # For each network, remove all stations
            for net in opts.nets:
                # Go through each line, is the network the same? what about the channels?
                data_copy = [x for x in data_copy if not (x[0] == net and (x[3][:2] in opts.chns or x[3] in opts.chns))]
        elif opts.nets != None and opts.stns != None:
            # For each network, remove specified stations with correct channels.
            for net in opts.nets:
                for sta in opts.stns:
                    data_copy = [x for x in data_copy if not (x[0] == net and x[1] == sta and (x[3][:2] in opts.chns or x[3] in opts.chns))]
        elif opts.nets == None and opts.stns != None:
            # For each station remove entry
            for sta in opts.stns:
                    data_copy = [x for x in data_copy if not (x[1] == sta and (x[3][:2] in opts.chns or x[3] in opts.chns))]
        elif opts.nets == None and opts.stns == None:
            # Do nothing <:O)
            print ("Nothing to remove.")       
        
        # Save csv
        print ("  Saving csv to {0:s}.csv".format(inp))
        fcsv = open(inp + ".csv",'w')
        for st in data_copy:
            # Return to original comma delimeted format:
            #                 net    stn   locs   chn   std      stt         edd      edt          lat       lon       elev       pol      azc       res
            st = ",".join(st)
            fcsv.writelines(st)

            
if __name__=='__main__':

    main()
