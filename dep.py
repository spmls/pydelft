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

    def read_dep(self, fname = None):
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
                    
        # Reshape depth
        if delimiter != 'space':
            z = np.reshape(z, (np.size(lines), 
                np.size(line.split('%s' % delimiter))))
        else:
            z = np.reshape(z, (np.size(lines), np.size(line.split())))
        
        z = z[:-1, :-1] # get rid of -999. Nans        

        # update the class
        self.depth = z
        self.filename = fname
        self.delimiter = delimiter

        fname = None

        f.close()

    def write_dep(self, Z, fname = None, grid_fname = None):
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = depwriteFileDialog()
            fname = filedialog.fname
            app = []
        else:
            fname = fname
        
        if not grid_fname:
            m = np.shape(Z)[0]
            n = np.shape(Z)[1]
        else:
            grid_fname = grid_fname
            grid = grd()
            grid.read_grd(fname = grid_fname)
            m = grid.m
            n = grid.n

        Z = np.array([np.append(i,-999.) for i in Z])
        Z = np.insert(Z, -1, np.ones(np.shape(Z[0]))*-999.)
        Z = Z.reshape((m+1, n+1))

        np.savetxt(fname, Z, delimiter = '\t', fmt = '%.3f')
        print('saved depth file: %s' %os.path.basename(fname))

        self.read_dep(fname)

    def plot_dep(self):
        plt.pcolormesh(self.grid.x, self.grid.y, self.depth,
                        edgecolor = 'none', linewidth = 0.0005)
        plt.axis('equal')
        plt.show()
