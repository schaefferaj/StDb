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

This module defines the main class ``StDbElement`` to create a station object, 
which contains attributes of a single station in the dabase dictionary.

"""
from obspy.geodetics.base import gps2dist_azimuth as epiaz
from numpy import pi
from obspy import UTCDateTime

class StDbElement(dict):
    """
    Class that defines the structure of each station entry in the station
    database.

    Attributes
    ----------
    station : str
        Station name
    network : std
        Network name
    altnet : List
        List of alternative networks
    channel : str
        Channel name (last digit only)
    location : List
        List of strings for station location
    latitude : float
        Latitude of station
    longitude : float
        Longitude of station
    elevation : float
        Elevation of station
    startdate : :class:`~obspy.core.utcadatetime.UTCDateTime`
        Start time of station operation
    enddate : :class:`~obspy.core.utcadatetime.UTCDateTime`
        End time of station operation
    polarity : float
        Polarity of vertical component
    azcorr : float
        Azimuth correction
    restricted_status : str
        Whether or not the data are restricted for a given station

    """
    def __init__(self, station="", network="", altnet=[], channel="", location=[''], 
        latitude=0., longitude=0., elevation=0., startdate=UTCDateTime, enddate=UTCDateTime, 
        polarity=1., azcorr=0. , restricted_status="?"):
        """
        Initialization for a Database Element

        """
        self.__dict__ = self
        self.station = station
        self.network = network
        self.altnet = altnet
        self.channel = channel
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.startdate = startdate
        self.enddate = enddate
        self.polarity = polarity
        self.azcorr = azcorr
        self.status = restricted_status
    
    def __call__(self, deadspace=0):
        m1 = " "*deadspace + "Station: {0:2s} {1:5s}\n".format(self.network, self.station)
        if len(self.altnet) > 0:
            m1 = m1 + " "*deadspace + " Alternate Networks: " + ",".join(self.altnet) + "\n"
        else:
            m1 = m1 + " "*deadspace + " Alternate Networks: None\n"
        if len(self.location) > 1:
            m2 = " "*deadspace + " Channel: {0:3s};  Locations: {1:s}\n".format(self.channel,",".join(self.location))
        else:
            m2 = " "*deadspace + " Channel: {0:3s};  Location: {1:s}\n".format(self.channel, ",".join(self.location))
        m3 = " "*deadspace + " Lon, Lat, Elev: {0:9.5f}, {1:10.5f}, {2:7.3f}\n".format(self.latitude, self.longitude, self.elevation)
        m4 = " "*deadspace + " StartTime: {0:s}\n".format(self.startdate.strftime("%Y-%m-%d %H:%M:%S"))
        m5 = " "*deadspace + " EndTime:   {0:s}\n".format(self.enddate.strftime("%Y-%m-%d %H:%M:%S"))
        if hasattr(self, 'restricted_status'):
            m6 = " "*deadspace + " Status:    {0:s}\n".format(self.restricted_status)
        elif hasattr(self, 'status'):
            m6 = " "*deadspace + " Status:    {0:s}\n".format(self.status)
        else:
            m6 = ""
        m7 = " "*deadspace + " Polarity: {0:.0f}\n".format(self.polarity)
        m8 = " "*deadspace + " Azimuth Correction: {0:f}\n".format(self.azcorr)
        return m1 + m2 + m3 + m4 + m5 + m6 + m7 + m8

