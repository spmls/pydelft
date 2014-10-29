import numpy as np
from PyQt4 import QtGui
import sys
import os
import matplotlib.pyplot as plt
import mpl_toolkits.basemap.pyproj as pyproj
from pydelft.grd import grd

#--------------------------------------------------------------------------------------------------
# READ DELFT DEPTH FILE
class depFileDialog(QtGui.QMainWindow):
    def __init__(self):
        super(depFileDialog, self).__init__()
        fname = []
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Open depth file')
        self.openfileDialog()
    def openfileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "DEP (*.dep)")
        self.fname = fname

class depwriteFileDialog(QtGui.QMainWindow):
    def __init__(self):
        super(depwriteFileDialog, self).__init__()
        fname = []
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Save depth file')
        self.savefileDialog()
    def savefileDialog(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "DEP (*.dep)")
        self.fname = fname

class dep():
    """Bathymetry file.  See A.3.4 in Delft3D-FLOW user manual.

    Attributes:
        depth       array of depths, formatted to match grid mxn
        grid        class, from the grid file associated with the depth file
        delimiter   the delimiter type (default is tab )
        filename    the full path of the .grd file
    """
    def __init__(self, fname = None, grid_fname = None):
        depth = ''
        grid = ''
        filename = ''
        delimiter = ''
        self.read_dep(fname, grid_fname)

    def read_dep(self, fname = None, grid_fname = None):
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = depFileDialog()
            fname = filedialog.fname
            app = []
        else:
            fname = fname
        # Read lines
        f = open(fname, 'r')
        lines = f.readlines()

        if '\t' in lines[0]:
            delimiter = '\t'
        else:
            delimiter = 'space'

        z = []

        if delimiter != 'space':
            for line in lines:
                for s in line.split('%s' % delimiter):
                    z.append(float(s))
        else:
            for line in lines:
                for s in line.split():
                    z.append(float(s))

        # Get the shape from an associated grd file
        grid = grd(grid_fname)
        # Reshape depth to match grid
        z = np.reshape(z, (grid.m+1, grid.n+1))
        z = z[:-1, :-1] # get rid of -999. Nans

        # update the class
        self.depth = z
        self.grid = grid
        self.filename = fname
        self.delimiter = delimiter

        fname = None
        f.close()

    def write_dep(self, Z, fname = None):
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = depwriteFileDialog()
            fname = filedialog.fname
            app = []
        else:
            fname = fname

        blank_row = np.ones(np.shape.(Z))*-999.
        Z = np.append(Z, 999.)
        np.savetxt(fname, [-Z, blank_row], delimiter = '\t', fmt = '%.3f')

        self.read_dep(fname = fname)

    def plot_dep(self):
        plt.pcolormesh(self.grid.x, self.grid.y, self.depth,
                        edgecolor = 'none', linewidth = 0.0005)
        plt.axis('equal')
        plt.show()
