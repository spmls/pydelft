import numpy as np
from tkinter import filedialog
import sys
import os
import matplotlib.pyplot as plt
import pyproj
import math
import datetime

#------------------------------------------------------------------------------
# READ DELFT GRID FILE
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
        #self.read_grd(fname)

    def read_grd(self, fname=None, nan_value = -999.):
        '''Read a Delft3d Grid file.  If fname not specified, opens a file dialog. Some grids have
        a nan value specified in header, default nan value is 0... Can add functionality in this
        script to see if that is specified in the header or not.'''
        # Set filename via GUI if it's not specified.
        if not fname:
            fname = filedialog.askopenfilename()
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

    def write_rectgrd(self, fname=None, coord_system = 'Cartesian', m = None,
                  n = None, cellsize = None, x0 = None, y0 = None, depth = None):

        if not depth:
            if not m:
                m = int(input('number of rows: '))
            if not n:
                n = int(input('number of columns: '))
        else:
            depth = np.array(depth)
            m = depth.shape[0]
            n = depth.shape[1]
        if not cellsize:
                cellsize = float(input('cellsize: '))
        if x0 is None:
                x0 = float(input('xllcorner: '))
        if y0 is None:
                y0 = float(input('yllcorner: '))

        records = []
        rows = math.floor(m/5)
        remainder = m%5

        records.append('* \n* Delft3d- rectilinear grid file created with pydelft \n* File creation date: %s\n* \n'
                       %str(datetime.datetime.now()))
        records.append('Coordinate System = %s\n' % coord_system)
        records.append('\t%i\t%i\n' % (m,n))
        records.append('0 0 0\n')

        # Values for x
        for i in range(1, n+1):
            etax = np.arange(x0, m*cellsize+x0, cellsize)
            if np.size(etax) > 5:
                etax_1 = etax[0:5]
                records.append('ETA=\t%i\t%.20e\t%.20e\t%.20e\t%.20e\t%.20e\n' % (i,
                                                                                  etax_1[0],
                                                                                  etax_1[1],
                                                                                  etax_1[2],
                                                                                  etax_1[3],
                                                                                  etax_1[4]))
                if remainder != 0:
                    etax_mid = etax[5:-remainder]
                    etax_last = etax[-remainder:]
                elif remainder == 0:
                    etax_mid = etax[5:-5]
                    etax_last = etax[-5:]
                for j in np.arange(0,np.size(etax_mid), 5):
                    records.append('      \t\t%.20e\t%.20e\t%.20e\t%.20e\t%.20e\n' % (etax_mid[j],
                                                                                    etax_mid[j+1],
                                                                                    etax_mid[j+2],
                                                                                    etax_mid[j+3],
                                                                                    etax_mid[j+4]))
                records.append('      \t\t%.20e' % etax_last[0])
                for j in etax_last[1:]:
                    records.append('\t%.20e' % j)
                records.append('\n')
            elif np.size(etax) <= 5:
                etax_1 = etax
                records.append('ETA=\t%i' % i)
                for j in etax_1:
                    records.append('\t%.20e' % j)
                records.append('\n')

        # Values for y
        y = np.arange(y0, y0+m*cellsize, cellsize)
        for i in range(1,n+1):
            etay = np.ones((m,1))*y[i-1]
            if np.size(etay) > 5:
                etay_1 = etay[0:5]
                records.append('ETA=\t%i\t%.20e\t%.20e\t%.20e\t%.20e\t%.20e\n' %(i,
                                                                            etay_1[0], etay_1[1],
                                                                            etay_1[2], etay_1[3],
                                                                            etay_1[4]))
                if remainder != 0:
                    etay_mid = etay[5:-remainder]
                    etay_last = etay[-remainder:]
                elif remainder == 0:
                    etay_mid = etay[5:-5]
                    etay_last = etay[-5:]
                for j in np.arange(0,np.size(etay_mid), 5):
                    records.append('      \t\t%.20e\t%.20e\t%.20e\t%.20e\t%.20e\n' % (etay_mid[j],
                                                                                    etay_mid[j+1],
                                                                                    etay_mid[j+2],
                                                                                    etay_mid[j+3],
                                                                                    etay_mid[j+4]))
                records.append('      \t\t%.20e' % etay_last[0])
                for j in etay_last[1:]:
                    records.append('\t%.20e' %j)
                records.append('\n')
            elif np.size(etay) <= 5:
                etay = np.ones((m,1))*y[i-1]
                etay_1 = etay
                records.append('ETA=\t%i' % i)
                for j in etay_1:
                    records.append('\t%.20e' % j)
                records.append('\n')

        # Set filename via GUI if it's not specified.
        if not fname:
            fname = filedialog.asksaveasfile()
        else:
            fname = fname

        f = open(fname, 'w')
        for r in records:
            f.write(r)
        f.close()

        self.read_grd(fname = fname)


    def plot_grd(self):
        plt.pcolormesh(self.x,self.y,np.zeros(np.shape(self.x)),
                       edgecolor = 'k', facecolor = 'none', linewidth = 0.0005)
        plt.axis('equal')
        plt.show()

    def get_mn(self,x,y, grid_epsg = 4326, query_epsg = 4326):
        def find_nearest(grid, query):
            m = np.unravel_index(np.abs(grid.y-query[1]).argmin(), np.shape(grid.y))[0]
            n = np.unravel_index(np.abs(grid.x-query[0]).argmin(), np.shape(grid.x))[1]
            return [m,n]

        grid_proj = pyproj.Proj("+init=EPSG:%i" % grid_epsg)
        query_proj = pyproj.Proj("+init=EPSG:%i" % query_epsg)

        if grid_epsg != query_epsg:
            x,y = pyproj.transform(query_proj, grid_proj, x, y)

        idx = [find_nearest(self,[x[i],y[i]]) for i in range(0, np.size(x)-1)]

        return idx
