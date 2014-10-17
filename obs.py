import numpy as np
from pydelft.grd import grd
from pydelft.dep import dep
from PyQt4 import QtGui
import mpl_toolkits.basemap.pyproj as pyproj
import mpl_toolkits.basemap as Basemap

#------------------------------------------------------------------------------
# OBS SAVE FILE DIALOG

class SaveObsFileDialog(QtGui.QMainWindow):
    def __init__(self):
        super(SaveObsFileDialog, self).__init__()
        fname = []
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Save obs file')
        self.savefileDialog()
    def savefileDialog(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save file', os.getcwd(), "OBS (*.obs)")
        self.fname = fname

#------------------------------------------------------------------------------
# OBSERVATIONS DATA CLASS

class obs():
    '''Read or write a Delft3d obs file.'''
    def __init__(self, fname=None):
        self.names = ''
        self.m = ''
        self.n = ''
        self.num_obs = ''
        self.filename = fname
        if self.filename:
            self.read_obs(self.filename)

    def coords2mn(self, grid, station_names, station_x, station_y, grid_epsg = 4326, station_epsg = 4326):
        '''Calculate nearest m, n indices on a grid for an array of type (['name', x, y])
        where x and y are coordinates (longitude/latitude or eastin/northing etc.).
        If the two are different coordinate systems, will convert the array to the grid
        coordinate system (using EPSG codes, default is 4326=WGS84'''
        def find_nearest(grid, query):
            m = np.unravel_index(np.abs(grid.y-query[1]).argmin(), np.shape(grid.y))[0]
            n = np.unravel_index(np.abs(grid.x-query[0]).argmin(), np.shape(grid.x))[1]
            return [m,n]

        grid_proj = pyproj.Proj("+init=EPSG:%i" % grid_epsg)
        station_proj = pyproj.Proj("+init=EPSG:%i" % station_epsg)

        if grid_epsg != station_epsg:
            station_x, station_y = pyproj.transform(station_proj, grid_proj, station_x, station_y)

        obs_idx = [find_nearest(grid,[station_x[i], station_y[i]]) for i in range(0, np.size(station_names)-1)]

        self.names = station_names
        self.m = [i[0] for i in obs_idx]
        self.n = [i[1] for i in obs_idx]
        self.num_obs = np.shape(obs_idx)[0]

    def write(self, fname = None):
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = SaveObsFileDialog()
            fname = filedialog.fname
        else:
            fname = fname

        self.filename = fname

        f = open(fname,'w')
        for i in range(0,self.num_obs-1):
            name = self.names[i].ljust(20)
            line = str('%s\t%s\t%s\n' % (name, int(self.m[i]), int(self.n[i])))
            if len(line) > 132:
                print('ERROR: RECORD LENGTH TOO LONG, MAX 132\n@ %s' % line)
                break
            f.write(line)
        f.close()
        print('obs file written: %s' % self.filename)
