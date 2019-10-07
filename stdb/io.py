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

import pickle as pickle

def load_db(fname, binp=True):
    """
    Submodule to read the station database from file

    Parameters
    ----------
    fname : str
        File name
    binp : bool
        Whether or not to use binary input

    Returns
    -------
    stdb : :class:`~stdb.classes.StDbElement`
        Instance of :class:`~stdb.classes.StDbElement`

    """

    if binp:
        rflag = 'rb'
    else:
        rflag = 'r'
    
    stdb = pickle.load(open(fname, rflag))

    return stdb

def write_db(fname=str, stdb={}, binp=True):
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


