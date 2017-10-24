#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 09:20:19 2017
https://software.ecmwf.int/wiki/display/GRIB/get.py
@author: lvkai
"""

from __future__ import print_function
import traceback
import sys
import ftpconfig
from gribapi import *
import matplotlib.pyplot as plt
if len(sys.argv)<2:
    iniPath="paras.ini"
else:
    iniPath=sys.argv[1]
fc=ftpconfig.FtpConfig()
fc.setFromIni(iniPath)
#INPUT = '../../data/reduced_latlon_surface.grib1'
INPUT=fc.SendFiles
VERBOSE = 1  # verbose error reporting
 
 
maxs=[]
averages=[]
mins=[]
index=[]
def example():
    with open(INPUT) as f:
 
        keys = [
            'Ni',
            'Nj',
            'latitudeOfFirstGridPointInDegrees',
            'longitudeOfFirstGridPointInDegrees',
            'latitudeOfLastGridPointInDegrees',
            'longitudeOfLastGridPointInDegrees',
            ]
 
        ai=0
        while 1:
            gid = grib_new_from_file(f)
            if gid is None:
                break
 
            for key in keys:
                if not grib_is_defined(gid, key):
                    raise ValueError("Key '%s' was not defined" % key)
                print('%s=%s' % (key, grib_get(gid, key)))
 
            print('There are %d values, average is %f, min is %f, max is %f'
                  % (grib_get_size(gid, 'values'),
                     grib_get(gid, 'average'),
                     grib_get(gid, 'min'),
                     grib_get(gid, 'max')))
            maxs.append(grib_get(gid, 'max'))
            averages.append(grib_get(gid, 'average'))
            mins.append(grib_get(gid, 'min'))
            index.append(ai)
            ai+=1
            grib_release(gid)
 
 
def main():
    try:
        example()
    except GribInternalError as err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print(err.msg, file=sys.stderr)
 
#        return 1
            exit
    plt.plot(index,maxs)
    
 
if __name__ == "__main__":
    sys.exit(main())