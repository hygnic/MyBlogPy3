# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              example2_alg
# Author:            Hygnic
# Created on:        2022/1/7 10:15
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
import sys
import os
import rvt.vis  # fro calculating visualizations
import rvt.default  # for loading/saving rasters

try:
    from osgeo import gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

print(">>"*50)
print('Python: {}'.format(sys.version))
print('GDAL: {}'.format(gdal.__version__))
print(">>"*50)


"""--------DATA"""
filepath = r"D:\MyProject\BaiduNetdiskWorkspace\1.Blog\7_可视化\RRIM系列作品\3_剑门关\1_栅格和地图文档"
# filepath = r"E:\MyD\BaiduNetdiskWorkspace\1.Blog\7_可视化\rrim系列作品\3_剑门关\1_栅格和地图文档"
filename = os.path.join(filepath, "SRTMv3_1_N32E105.tif")
output_raster = os.path.join(filepath, "After_p.tif")
os.chdir(filepath)


raster_name = "Positive_openness.tif"

used_raster = gdal.Open(raster_name)
arr = used_raster.GetRasterBand(1).ReadAsArray()



