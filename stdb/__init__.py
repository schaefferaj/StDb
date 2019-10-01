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

'''
Module: StDb

Python Module containing Class Instance for the elements of the station dictionary.
SEveral variables are builtin, in addition to some helper functions which return
certain components or measures associated with the data.

Contains
 classes:
    StDbElement
        __init__
        __call__
        gcdist
        az
        baz
    TextMessageBox
        __init__
        b1_action
        b2_action
        close_mod
    EditMessageBox

 convert:
    tocsv
    fromcsv
 io:
    load_db
    write_db
    write_db_csv
'''

from . import kml
from .io import write_db, load_db
from .classes import StDbElement, EditMsgBox
from .convert import tocsv, fromcsv
