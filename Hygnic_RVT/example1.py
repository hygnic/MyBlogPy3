# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              example1
# Author:            Hygnic
# Created on:        2021/12/30 12:35
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
# print(ord("文"))

"""--------IMPORT_SETTINGS"""

import sys
try:
    from osgeo import gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

print(">>"*50)
print('Python: {}'.format(sys.version))
print('GDAL: {}'.format(gdal.__version__))
print(">>"*50)



"""--------DATA"""

# 峨眉山附近
# raster_dataset = r"D:\MyProject\BaiduNetdiskWorkspace\1.Blog\7_可视化\000_rvt介绍\1_data\SRTMv3_1_N29E103_峨眉山附近.tif"


"""--------"""
# dem_dict = rvt.default.get_raster_arr(raster_dataset)

