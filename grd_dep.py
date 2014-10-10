import numpy as np
from PyQt4 import QtGui
import sys
import os
import matplotlib.pyplot as plt

#------------------------------------------------------------------------------
# READ DELFT GRID FILE

class grdFileDialog(QtGui.QMainWindow):
    def __init__(self):
        super(grdFileDialog, self).__init__()
        fname = []
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Open grid file')
        self.openfileDialog()
    def openfileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "GRD (*.grd)")
        self.fname = fname

class grd():
    """Orthogonal curvilinear grid file.  See A.3.2 in Delft3D-FLOW user manual.

    Attributes:
        m   number of rows, derived from the file header
        n   number of columns, derived from the file header
        x   the mxn array of x coordinates
        y   the mxn array of y coordinates
        coordinate_system   the coordinate system labeled in the header (cartesian or spherical)
        filename    the full path of the .grd file
    """
    def __init__(self, fname=None):
        x = ''
        y = ''
        m = ''
        n = ''
        coordinate_system = ''
        filename = ''
        self.read_grd(fname)

    def read_grd(self, fname=None, nan_value = 0.0):
        '''Read a Delft3d Grid file.  If fname not specified, opens a file dialog. Some grids have
        a nan value specified in header, default nan value is 0... Can add functionality in this
        script to see if that is specified in the header or not.'''
        # Set filename via GUI if it's not specified.
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = grdFileDialog()
            fname = filedialog.fname
        else:
            fname = fname

        f = open(fname, 'r')

        # Read the header
        header = []
        while True:
            line = f.readline()
            if 'ETA' in line:
                break
            else:
                header.append(line)
        header = np.array(header)
        coordinate_system = [h for h in header if 'Coordinate System' in h][0].rstrip('\n').split('=')[1]
        shape = header[np.where(header == [h for h in header if 'Coordinate System' in h][0])[0][0]+1].split()
        m, n = int(shape[1]), int(shape[0])

        # Read the coordinates
        coordinates = f.readlines()
        coordinates.insert(0,line) # inserts the first line of coordinates ('line')

        x = [] # generate an array of x coordinates
        for line in coordinates[0:int(np.size(coordinates)/2)]:
            if 'ETA=' in line:
                coords = line.split()[2:]
                for i in coords:
                    x.append(float(i))
            else:
                coords = line.split()
                for i in coords:
                    x.append(float(i))

        y = []  # generate an array of y coordinates
        for line in coordinates[int(np.size(coordinates) / 2):]:
            if 'ETA=' in line:
                coords = line.split()[2:]
                for i in coords:
                    y.append(float(i))
            else:
                coords = line.split()
                for i in coords:
                    y.append(float(i))

        # reshape x and y to reflect the rows columns in the header
        x, y = np.reshape(x, (m, n)), np.reshape(y, (m, n))
        # mask nan
        x, y = np.ma.masked_equal(x, nan_value), np.ma.masked_equal(y, nan_value)

        # update the class
        self.x = x
        self.y = y
        self.m = m
        self.n = n
        self.coordinate_system = coordinate_system
        self.filename = fname

        fname = None
        f.close()

    def plot_grd(self):
        plt.pcolormesh(self.x,self.y,np.zeros(np.shape(self.x)),
                       edgecolor = 'k', facecolor = 'none', linewidth = 0.0005)
        plt.axis('equal')
        plt.show()

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

    def plot_dep(self):
        plt.pcolormesh(self.grid.x, self.grid.y, self.depth,
                        edgecolor = 'none', linewidth = 0.0005)
        plt.axis('equal')
        plt.show()
