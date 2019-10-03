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

A second class ``TextMessageBox`` allows creation of a message box for GUI
interaction. This class is used in the script ``edit_stdb.py``. 

"""
from obspy.geodetics.base import gps2dist_azimuth as epiaz
import tkinter
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


class TextMessageBox(object):
    """
    Class: TextMessageBox
    """
    def __init__(self, b1="OK", b2="Cancel", frame=True, ststr="", title=""):

        root = self.root = tkinter.Tk()
        root.title("Edit Entry: "+title)

        # remove the outer frame if frame=False
        if not frame: root.overrideredirect(True)

        # if b1 or b2 is a tuple unpack into the button text & return value
        if isinstance(b1, tuple): b1, self.b1_return = b1
        if isinstance(b2, tuple): b2, self.b2_return = b2

        # main frame
        frm_1 = tkinter.Frame(root)
        frm_1.pack(ipadx=2, ipady=2)

        # Text Entry
        self.entry = tkinter.Entry(frm_1, width=len(ststr) + 20)
        self.entry.insert(0, ststr)
        self.entry.pack(padx=5, pady=5)
        self.entry.focus_set()

        # button frame
        frm_2 = tkinter.Frame(frm_1)
        frm_2.pack(padx=4, pady=4)

        # buttons
        btn_1 = tkinter.Button(frm_2, width=8, text=b1)
        btn_1['command'] = self.b1_action
        btn_1.pack(side='left')
        btn_2 = tkinter.Button(frm_2, width=8, text=b2)
        btn_2['command'] = self.b2_action
        btn_2.pack(side='left')
        btn_2.focus_set()

        # the enter button will trigger the focused button's action
        btn_1.bind('<KeyPress-Return>', func=self.b1_action)
        btn_2.bind('<KeyPress-Return>', func=self.b2_action)

        # roughly center the box on screen
        # for accuracy see: http://stackoverflow.com/a/10018670/1217270
        root.update_idletasks()
        xp = (root.winfo_screenwidth() // 3) - (root.winfo_width() // 2)
        yp = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        geom = (root.winfo_width(), root.winfo_height(), xp, yp)
        root.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # call self.close_mod when the close button is pressed
        root.protocol("WM_DELETE_WINDOW", self.close_mod)

        # a trick to activate the window (on windows 7)
        root.deiconify()

    def b1_action(self, event=None):
        try: x = self.entry.get()
        except AttributeError:
            self.returning = ""
            self.root.quit()
        else:
            if x:
                self.returning = x
                self.root.quit()

    def b2_action(self, event=None):
        self.returning = ""
        self.root.quit()

    def close_mod(self):
        pass

def EditMsgBox(title="", ststr="", b1='OK', b2='Cancel', frame=True):
    """
    Create an instance of TextMessageBox, and get data back from the user.

    Parameters
    ----------
    title : str 
        Station name being edited
    ststr : str 
        CSV format data string to be edited
    b1 : str 
        Text for left button, or a tuple (<text for button>, <to return on press>)
    b2 : str
        Text for right button, or a tuple (<text for button>, <to return on press>)
    frame : bool 
        Include a standard outerframe: True or False

    Returns
    -------
    msgbox.returning : str
        String representation of button pressed
        
    """

    msgbox = TextMessageBox(title=title, ststr=ststr, b1=b1, b2=b2, frame=frame)
    msgbox.root.mainloop()

    # the function pauses here until the mainloop is quit
    msgbox.root.destroy()

    return msgbox.returning
