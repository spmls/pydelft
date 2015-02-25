import numpy as np
from netCDF4 import Dataset as NetCDFFile
from PyQt4 import QtGui
import os
import sys

class ncFileDialog(QtGui.QMainWindow):
    '''A file dialog for opening Delft3d FLOW history files in netcdf format.
    Assumes that the netcdf file was converted in matlab from a NEFIS file using
    vs_trih2nc, which is why the file dialog prompts for .nc files with 'his' in
    the filename.  This class is called in __init__ in the 'obs' class.'''
    def __init__(self):
        super(ncFileDialog, self).__init__()
        fname = []
        self.initUI()
    def initUI(self):
        self.setGeometry(300,300,350,300)
        self.setWindowTitle('Open netcdf history file')
        self.openfileDialog()
    def openfileDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(self,
                                                  'Open netcdf history file',
                                                  os.getcwd(),
                                                  "netcdf (*his*.nc);; all (*)")
        self.fname = fname

class his():
    '''Loads data from a netcdf file that was converted from a NEFIS history file.'''
    def __init__(self, fname=None):
        self.read_his_nc(fname)
    def read_his_nc(self, fname=None):
        # Set filename via GUI if it's not specified.
        if not fname:
            app = QtGui.QApplication(sys.argv)
            filedialog = ncFileDialog()
            fname = os.path.abspath(filedialog.fname)
        else:
            fname = os.path.abspath(fname)
        ncFile = NetCDFFile(fname)
        #get times in unix epoch format (seconds since 01/01/1970)
        self.times = (np.array(ncFile.variables['time'])-np.array(ncFile.variables['time'])[0])*24*60*60
        # get name of each obs station
        self.obs = [''.join(i.astype(str)).strip()
                    for i in np.array(ncFile.variables['platform_name'])]
        for idx, obs in enumerate(self.obs):
            if obs[0].isdigit():
                obs_str = "_" + obs
            else:
                obs_str = obs
            d = {}
            for i in ncFile.variables:
                if i == 'platform_name':
                    d['name'] = obs
                elif i == 'platform_m_index':
                    d['m'] = int(np.array(ncFile.variables[i])[idx])
                elif i == 'platform_n_index':
                    d['n'] = int(np.array(ncFile.variables[i])[idx])
                else:
                    array = np.array(ncFile.variables[i])
                    shape = np.shape(array.shape)[0]
                    if shape == 1:
                        try:
                            d[i] = array[idx]
                        except IndexError:
                            d[i] = array
                    elif shape == 2:
                        d[i] = array[:,idx]
                    elif shape == 3:
                        d[i] = array[:,idx,:]
                    else:
                        print("Error: variable '%s' shape not defined" %i)
            setattr(self,obs_str,d)
