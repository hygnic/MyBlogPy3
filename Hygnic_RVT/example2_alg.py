# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              example2_alg
# Author:            Hygnic
# Created on:        2022/1/7 10:15
# Version:           
# Reference:
"""
Description:         结合 oppn 和 neg 栅格制作 Ridge Valley Index
Usage:               
"""
# -------------------------------------------
# G:\MoveOn\MyBlogPy3\Hygnic_RVT\example2_alg.py

###############################################################################
#                                  functions                                  #
###############################################################################

import numpy as np
import sys
import os
import rvt.vis  # fro calculating visualizations
import rvt.default  # for loading/saving rasters
from pprint import pprint


try:
    from osgeo import gdal
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')

print(">>"*50)
print('Python: {}'.format(sys.version))
print('GDAL: {}'.format(gdal.__version__))
print(">>"*50)


"""--------Function"""
def make_raster(in_ds, fn, data, data_type, nodata=None):
    """Create a one-band GeoTIFF.

    in_ds     - datasource to copy projection and geotransform from
    fn        - path to the file to create
    data      - NumPy array containing data to write
    data_type - output data type
    nodata    - optional NoData value
    """
    driver = gdal.GetDriverByName('GTiff')
    out_ds = driver.Create(
        fn, in_ds.RasterXSize, in_ds.RasterYSize, 1, data_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    out_band = out_ds.GetRasterBand(1)
    if nodata is not None:
        out_band.SetNoDataValue(nodata)
    out_band.WriteArray(data)
    out_band.FlushCache()
    out_band.ComputeStatistics(False)
    return out_ds


"""--------DATA"""
# filepath = r"D:\MyProject\BaiduNetdiskWorkspace\1.Blog\7_可视化\RRIM系列作品\3_剑门关\1_栅格和地图文档"
# filepath = r"E:\MyD\BaiduNetdiskWorkspace\1.Blog\7_可视化\rrim系列作品\3_剑门关\1_栅格和地图文档"
filepath = r"E:\MyD\BaiduNetdiskWorkspace\1.Blog\7_可视化\rrim系列作品\1_长白山"
filename = os.path.join(filepath, "Mt_ChangBai_4522.tif")
# filename = os.path.join(filepath, "SRTMv3_1_N32E105.tif")


os.chdir(filepath)


pos = "Positive_openness.tif"
neg = "Negative_openness.tif"

pos_raster = gdal.Open(pos)
neg_raster = gdal.Open(neg)


pos_arr = pos_raster.GetRasterBand(1).ReadAsArray()
neg_arr = neg_raster.GetRasterBand(1).ReadAsArray()
# Ridge Valley Index rvi
rvi_arr = (pos_arr-neg_arr)/2.0
rvi_name = "RVI.tif"
# make_raster(pos_raster, rvi_arr, rvi_arr, np.float)
make_raster(pos_raster, rvi_name, rvi_arr, gdal.GDT_Float32)