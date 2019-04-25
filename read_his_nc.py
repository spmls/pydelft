import numpy as np
from netCDF4 import Dataset as NetCDFFile
from PyQt4 import QtGui
import os
import sys

class his():
    '''Loads data from a netcdf file that was converted from a NEFIS history file.'''
    def __init__(self, fname=None):
        self.read_his_nc(fname)
    def read_his_nc(self, fname=None):
        # Set filename via GUI if it's not specified.
        if not fname:
            fname = filedialog.askopenfilename()
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
            elif '-' in obs:
                obs_str = obs.replace("-","_")
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
            # calculate depth averaged velocity if needed
            if d['u_x'].shape[1] > 1: # test if velocity array has more than one layer
                Ux = [self.calc_da_vel(d['u_x'][t], d['waterlevel'][t] - (-d['depth'])) for t in range(0, self.times.size)]
                Uy = [self.calc_da_vel(d['u_y'][t], d['waterlevel'][t] - (-d['depth'])) for t in range(0, self.times.size)]
                d['U_x'] = np.array(Ux)
                d['U_y'] = np.array(Uy)
            else:
                d['U_x'] = d['u_x']
                d['U_y'] = d['u_y']
            # calculate Froude number
            frx = [self.calc_froude(d['U_x'][t], d['waterlevel'][t] - (-d['depth'])) for t in range(0, self.times.size)]
            fry = [self.calc_froude(d['U_y'][t], d['waterlevel'][t] - (-d['depth'])) for t in range(0, self.times.size)]
            d['fr_x'] = frx
            d['fr_y'] = fry

            setattr(self,obs_str,d)

    def calc_da_vel(self, velocities, depth, layers=[100,80,60,45,33,23,15,9,5,2]):
        '''Calculate the depth averaged velocity if using a layered model
        layers: the percentage of depth in the water column at which velocity points are measured [enter in %]
        '''
        layers = np.array(layers)*0.01*depth
        dav = np.trapz(velocities, layers, dx = 0.001, axis = -1)/depth
        return dav

    def calc_froude(self, dav, depth):
        '''Calculate the froude number using depth averaged velocity and depth'''
        fr  = np.abs(dav)/np.sqrt(9.81*np.abs(depth))
        return fr
