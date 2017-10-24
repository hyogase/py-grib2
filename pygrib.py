#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 08:27:51 2017

@author: lvkai
"""
#%matplotlib inline 
#from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
#%matplotlib inline 
from mpl_toolkits.basemap import Basemap  # import Basemap matplotlib toolkit
import numpy as np
import matplotlib.pyplot as plt
import pygrib # import pygrib interface to grib_api
import ftpconfig 
from gribapi import *
from datetime import datetime

#INPUT = sys.argv[1]
#rootPath = sys.argv[2]
#OUTPUT = rootPath + "/" + sys.argv[3] + ".grib2"
if len(sys.argv)<2:
    iniPath="paras.ini"
else:
    iniPath=sys.argv[1]
fc=ftpconfig.FtpConfig()
fc.setFromIni(iniPath)

INPUT = fc.SendFiles
rootPath = fc.OutputPath
OUTPUT = rootPath + "/" + fc.OutputFileName + ".grib2"
short_name = fc.shortname
 

grbs=pygrib.open(INPUT)
#grbs.seek(2)
#grbs.tell()
#grb=grbs.read(1)[0]
#grb
#grbs.tell()
#grbs.seek(0)
for grb in grbs:
    grb
#    print grb.keys()
    
    


grbs.rewind() # rewind the iterator

date_valid = datetime(2017,3,28,3,0)
t2mens = []
for grb in grbs:
    if grb.validDate == date_valid and grb.parameterName == 'Temperature' and grb.level == 2: 
        t2mens.append(grb.values)
t2mens = np.array(t2mens)
print t2mens.shape, t2mens.min(), t2mens.max()
lats, lons = grb.latlons()  # get the lats and lons for the grid.
print 'min/max lat and lon',lats.min(), lats.max(), lons.min(), lons.max()


fig = plt.figure(figsize=(16,35))
#m = Basemap(projection='lcc',lon_0=-74,lat_0=41,width=4.e6,height=4.e6)
#m = Basemap(projection='lcc',lon_0=20,lat_0=30,width=4.e6,height=4.e6)
#x,y = m(lons,lats)
#for nens in range(1,51):
#    ax = plt.subplot(10,5,nens)
#    m.drawcoastlines()
#    cs = m.contourf(x,y,t2mens[nens],np.linspace(230,300,41),cmap=plt.cm.jet,extend='both')
#    t = plt.title('ens member %s' % nens)

map = Basemap(projection='ortho',lat_0=45,lon_0=100,resolution='l')
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
map.fillcontinents(color='coral',lake_color='aqua')
# draw the edge of the map projection region (the projection limb)
map.drawmapboundary(fill_color='aqua')
# draw lat/lon grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
# make up some data on a regular lat/lon grid.
nlats = 360; nlons = 721; delta = 2.*np.pi/(nlons-1)
lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
lons = (delta*np.indices((nlats,nlons))[1,:,:])
wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
# compute native map projection coordinates of lat/lon grid.
x, y = map(lons*180./np.pi, lats*180./np.pi)
# contour data over the map.
cs = map.contour(x,y,wave+mean,15,linewidths=1.5)
plt.title('contour lines over filled continent background')
plt.show()

