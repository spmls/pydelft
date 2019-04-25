import numpy as np
from pydelft.grd import grd
from pydelft.bnd import bnd
from PyQt4 import QtGui
import sys
import os
import pandas as pd

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
            fname = filedialog.askopenfilename()
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
