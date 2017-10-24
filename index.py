#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 10:55:55 2017

@author: lvkai
"""

import traceback
import sys,os 
from gribapi import *
import ftpconfig 
if len(sys.argv)<2:
    iniPath="paras.ini"
else:
    iniPath=sys.argv[1]
fc=ftpconfig.FtpConfig()
fc.setFromIni(iniPath)
#INPUT = '../../data/reduced_latlon_surface.grib1'
INPUT=fc.SendFiles.encode('utf-8')
VERBOSE=1 # verbose error reporting
rootPath = fc.OutputPath.encode('utf-8')
def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)
 
def example():
    index_keys = ["shortName","level","number","step"]
    index_file = "my.idx"
 
    iid = None
 
    if (os.path.exists(index_file)):
        iid = grib_index_read(index_file)
    else:
        iid = grib_index_new_from_file(INPUT,index_keys)
 
        # multiple files can be added to an index:
        # grib_index_add_file(iid,"grib file to add")
#        fo = open(rootPath + "/allindex.txt", "w")
#        print(rootPath + "/allindex.txt")
#        fo.writelines(iid)
#        fo.close()
        grib_index_write(iid,index_file)
 
    index_vals = []
 
    for key in index_keys:
        print "%sSize=%d" % (
            key,
            grib_index_get_size(iid,key)
        )
 
        key_vals = grib_index_get(iid,key)
        print " ".join(key_vals)
 
        index_vals.append(key_vals)
 
    for prod in product(*index_vals):
        for i in range(len(index_keys)):
            grib_index_select(iid,index_keys[i],prod[i])
 
        while 1:
            gid = grib_new_from_index(iid)
            if gid is None: break
            print " ".join(["%s=%s" % (key,grib_get(gid,key)) for key in index_keys])
            grib_release(gid)
 
    grib_index_release(iid)
     
 
def main():
    try:
        example()
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())