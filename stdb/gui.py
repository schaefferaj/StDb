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

This module defines a function ``EditMsgBox``, which instantiates an object
from class ``TextMessageBox``, allowing creation of a message box for GUI 
interaction. This class is used in the script ``edit_stdb.py``. 

"""

# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):
    """
    GUI message box for editing the fields of a station dictionary

    """

    def __init__(self, ststr="", title=""):
        super().__init__()
        self.title = "Edit Entry: " + title
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 140
        self.ststr = ststr
        self.initUI()
    
    def initUI(self):

        # Geometry
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(860,40)
        
        # Create a button in the window
        self.OKbutton = QPushButton('OK', self)
        self.OKbutton.move(20,80)
        self.cancelbutton = QPushButton('Cancel', self)
        self.cancelbutton.move(110,80)

        # Text Entry
        self.textbox.setText(self.ststr)

        # Connect button to function on_click
        self.OKbutton.clicked.connect(self.on_click_OK)
        self.cancelbutton.clicked.connect(self.on_click_cancel)
        self.show()
    
    @pyqtSlot()
    def on_click_OK(self):
        textboxValue = self.textbox.text()
        self.returning = textboxValue
        self.close()

    @pyqtSlot()
    def on_click_cancel(self):
        self.returning = ""
        self.close()


def EditMsgBox(title="", ststr=""):
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

    app = QApplication(sys.argv)
    msgbox = App(ststr=ststr, title=title)
    app.exec_()

    return msgbox.returning

