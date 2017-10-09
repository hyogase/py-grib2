#coding=utf-8
import traceback
import sys
import time
import os
 
from gribapi import *
 
INPUT = sys.argv[1]
rootPath = sys.argv[2]
OUTPUT = rootPath + "/" + sys.argv[3] + ".grib2"
VERBOSE = 1 # verbose error reporting
 
lon_start = 90
lat_start = 60
lon_end = 150
lat_end = 10
short_name = sys.argv[4]
 
def regionExtract():
    if not os.path.exists(rootPath):
        os.makedirs(rootPath)
		
    fin = open(INPUT)
    fout = open(OUTPUT,'w')
	
    while 1: 
        gid = grib_new_from_file(fin)
 	
        if gid is None:
            break
        
        shortName = grib_get(gid,'shortName')
        shrtName = short_name.lower()		
		
        if shortName != shrtName:
            continue
		
        # 获取起止经纬度、经度纬度格距以及数据值
    	xCount = grib_get(gid,'Ni')
    	yCount = grib_get(gid,'Nj')
    	lonStart = grib_get(gid, "longitudeOfFirstGridPointInDegrees")
    	latStart = grib_get(gid, "latitudeOfFirstGridPointInDegrees")
    	lonEnd = grib_get(gid, "longitudeOfLastGridPointInDegrees")
    	latEnd = grib_get(gid, "latitudeOfLastGridPointInDegrees")
    	lonGap = grib_get(gid, "iDirectionIncrementInDegrees")
    	latGap = grib_get(gid, "jDirectionIncrementInDegrees")
    	values = grib_get_values(gid)
        pointNum = len(values)
		
        L1 = []
        L2 = []
        L3 = [] # 存放网格二位数组数据值
        regionVals = [] # 存放区域提取后的数据
		
        for i in range(0, pointNum, xCount):
            L1.append(i)
			
        for j in range(xCount, pointNum + 1, xCount):
            L2.append(j)
		
        # 将一位数组转为二位数组
    	for idx in range(0, len(L1)):
            L3.append(values[L1[idx]:L2[idx]])
    	
        # 计算提取区域所处的下标范围
        xStart = int((lon_start - lonStart) / lonGap)
        yStart = int((latStart - lat_start) / latGap)        
        xEnd = int((lon_end - lonStart) / lonGap)
        yEnd = int((latStart - lat_end) / latGap)
        # 计算提取区域的纬向和经向格点数
        xNewCount = xEnd - xStart + 1
        yNewCount = yEnd - yStart + 1
        # 区域数据提取
        for row in range(yStart, yEnd + 1):
            for col in range(xStart, xEnd + 1):
                regionVals.append(L3[row][col])
		
        grib_set(gid, "centre", 38) # 38 - Beijing
        grib_set(gid, "Ni", xNewCount)
        grib_set(gid, "Nj", yNewCount)
        grib_set(gid, "longitudeOfFirstGridPointInDegrees", lon_start)
        grib_set(gid, "latitudeOfFirstGridPointInDegrees", lat_start)
        grib_set(gid, "longitudeOfLastGridPointInDegrees", lon_end)
        grib_set(gid, "latitudeOfLastGridPointInDegrees", lat_end)
        grib_set_values(gid, regionVals)
        grib_write(gid, fout)
        grib_release(gid)
 
    fin.close()
    fout.close()
 
def main():
    try:
        timeStart = time.time()
        regionExtract()
        timeEnd = time.time()
        spendTime = timeEnd - timeStart
        print "Region and parameter extract successfully, spend " + str(round(spendTime, 3)) + " seconds. File path is:[" + OUTPUT + "]"
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg
 
        return 1
 
if __name__ == "__main__":
    sys.exit(main())
