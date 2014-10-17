import numpy as np
from pydelft.grd import grd
from pydelft.bnd import bnd
from PyQt4 import QtGui
import sys
import os
import pandas as pd

class bctFileDialog(QtGui.QMainWindow):
    def __init__(self):
        super(bctFileDialog, self).__init__()
        fname = []
        self.initUI()

    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Open boundary conditions time-series file')
        self.openfileDialog()

    def openfileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "BCT (*.bct)")
        self.fname = fname

class bct():
    '''Delft3d boundary conditions time-series file'''
    def __init__(self,fname=None, bnd_fname=None):
        if fname:
            self.read_bct(fname)
        if bnd_fname:
            self.bnd = bnd(bnd_fname)
    def read_bct(self, fname=None):
        '''Read a Delft3d boundary conditions time-series file'''
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = bctFileDialog()
            fname = filedialog.fname
        else:
            fname = fname

        self.filename = fname

        self.name = []
        self.contents = []
        self.location = []
        self.time_function = []
        self.reference_time = []
        self.time_unit = []
        self.interpolation = []
        self.parameter = []
        self.data = []

