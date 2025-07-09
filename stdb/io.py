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
Tools used for loading and writing a station database to and from disk. 
These functions are used in most scripts bundled with this package. 

"""

import re
from stdb import StDbElement
import pickle as pickle
from obspy import UTCDateTime, read_inventory

def load_db(fname, binp=True, keys=None ):
    """
    Submodule to read the station database from .pkl, .csv or .xml file

    Parameters
    ----------
    fname : str
        File name. Assume csv format when ending in ".csv"
    binp : bool
        Whether or not to use binary input (only for pickle files)
    keys : List
        Default None
        If a list, then load database and select only keys that match those in this
        list. Returns the full db and a second optional output containing

    Returns
    -------
    stdb : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement`

    """

    if binp:
        rflag = 'rb'
    else:
        rflag = 'r'

    if fname.endswith('.csv'):
        stdb = {}
        with open(fname, 'r') as f:
            for line in f:
                k, v = fromcsv(line)
                stdb.update({k: v})
    elif fname.endswith('.xml'):
        inv = read_inventory(fname)
        stdb, stkeys = frominv(inv, keys=keys)
        return stdb, stkeys
    elif fname.endswith('.pkl'):
        stdb = pickle.load(open(fname, rflag))

    allkeys=stdb.keys()
    sorted(allkeys)

    #-- parse dictionary for specific keys if provided
    if keys is not None:
        # Extract key subset
        if len(keys) > 0:
           stkeys = []
           negkeys=[s[1:] for s in keys if '~' in s]
           getkeys=[s for s in keys if '~' not in s]
           if len(getkeys)>0:
               for skey in getkeys:
                   stkeys.extend([s for s in allkeys if skey in s])
           else:
                stkeys=allkeys
           if len(negkeys)>0:
                for skey in negkeys:
                    stkeys=[s for s in stkeys if skey not in s] 
        else:
            stkeys = allkeys    

    if keys is None:
        return stdb 
    else:
        stkeys=sorted(stkeys)
        return stdb, stkeys


def write_db(fname, stdb, binp=True):
    """
    Submodule to write the station database to file

    Parameters
    ----------
    fname : str
        File name
    stdb : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement`
    binp : bool
        Whether or not to use binary output

    """

    if binp:
        wflag = 'wb'
    else:
        wflag = 'w'

    pickle.dump(stdb, open(fname, wflag))


def tocsv(stel):
    """
    Subroutine to output an StDbElement to a csv formatted string

    Parameters
    ----------
    stel : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement` to convert to .csv

    Returns
    -------
    csvstr : str
        String representation of the csv content

    """
    csvstr = "{0:s}".format(stel.network)
    if len(stel.altnet) > 0:
        csvstr = csvstr + ":".join(stel.altnet)
    csvstr = csvstr + ",{0:s},".format(stel.station)
    csvstr = csvstr + ":".join(stel.location)
    csvstr = csvstr + ",{0:s},{1:10s},{2:8s},{3:10s},{4:8s},".format(stel.channel, \
        stel.startdate.strftime("%Y-%m-%d"), stel.startdate.strftime("%H:%M:%S"), \
        stel.enddate.strftime("%Y-%m-%d"),stel.enddate.strftime("%H:%M:%S"))
    csvstr = csvstr + "{0:f},{1:f},{2:f},{3:.0f},{4:f},{5:s}".format(stel.latitude, \
        stel.longitude, stel.elevation, stel.polarity, stel.azcorr, stel.status)
    return csvstr


def fromcsv(line="", lkey=False):
    """
    Subroutine to convert a csv format string into an StDbElement

    Parameters
    ----------
    line : str
        Line to read as csv
    lkey : bool
        Parameter controlling the length of the key (with or without CHANNEL info)

    Returns
    -------
    key : str
        Key associated with each entry in database
    entry : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement` class

    """
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
        
        # Required Channel Parameters
        chn = line[3][0:2]

        # Required Timing Parameters
        stdt = line[4]; sttm = line[5]; eddt = line[6]; edtm = line[7]

        # Required Position Parameters
        lat = float(line[8]); lon = float(line[9])
        
        # Set Default values for Optional elements 
        elev = 0.; pol = 1.; azcor = 0.
        if len(line) >= 11:
            elev = float(line[10])
        if len(line) >= 12:
            pol = float(line[11])
        if len(line) >= 13:
            azcor=float(line[12])
        if len(line) == 14:
            status = line[13]
        
        # Create Key
        if lkey:
            key = "{0:s}.{1:s}.{2:2s}".format(net.strip(), stn.strip(), chn.strip())
        else:
            key = "{0:s}.{1:s}".format(net.strip(), stn.strip())
        
        # Create Elemennt
        entry = StDbElement(network=net, altnet=altnet, station=stn, channel=chn, \
            location=loc, latitude=lat, longitude=lon, elevation=elev, polarity=pol, \
            azcorr=azcor, startdate=UTCDateTime(stdt), enddate=UTCDateTime(eddt), \
            restricted_status=status)
        
        return key, entry
        
    else:
        return None, None


def get_stkeys(inventory, keys=[]):

    allkeys = []
    station_list = inventory.get_contents()['stations']
    allkeys = [s.split(' ')[0] for s in station_list]

    if len(keys) > 0:
        # Extract key subset

        stkeys = []
        for key in keys:
            # Convert the pattern to a regex pattern
            # Replace '.' with '\.' to match literal dots
            # Replace '*' with '.*' to match any sequence of characters
            # Replace '?' with '.' to match any single character
            pattern = key.replace('.', r'\.').replace('*', '.*').replace('?', '.')

            # Compile the regex pattern
            regex = re.compile(f'^.*{pattern}.*$')

            # Filter allkeys based on the compiled regex
            stkeys.extend([key for key in allkeys if regex.match(key)])

    else:
        stkeys = allkeys

    return stkeys


def frominv(inventory, keys=[]):
    """
    Subroutine to convert an ObsPy inventory object into an StDbElement

    Parameters
    ----------
    inventory : :class:`~obspy.core.inventory.inventory.Inventory`
        Network inventory object
    keys : list
        List of keys used to search the database

    Returns
    -------
    key : str
        Key associated with each entry in database
    entry : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement` class

    """

    stkeys = get_stkeys(inventory, keys)

    stations = {}
    for key in stkeys:
        net = key.split('.')[0]
        sta = key.split('.')[1]
        cha = '?H?'
        inv = inventory.select(network=net, station=sta, channel=cha)
        seed_id = inv.get_contents()['channels'][0]
        coords = inv.get_coordinates(seed_id)

        stdb_element = StDbElement(
            station=sta,
            network=net,
            channel=seed_id.split('.')[3][0:2],
            location=seed_id.split('.')[2],
            latitude=coords['latitude'],
            longitude=coords['longitude'],
            elevation=coords['elevation'],
            startdate=inv[0].stations[0].start_date,
            enddate=inv[0].stations[0].end_date
            )
        stations[key] = stdb_element

    return stations, stkeys
