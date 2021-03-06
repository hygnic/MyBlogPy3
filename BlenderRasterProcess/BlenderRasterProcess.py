# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              BlenderRasterProcess
# Author:            Hygnic
# Created on:        2022/4/1 22:05
# Version:           
# Reference:         
"""
Description:  导出0-65535范围内的uint16位的栅格数据
注意事项：使用的栅格图层只能是单一波段，比如经常
使用的 DEM 数据。
Usage:               
"""
# -------------------------------------------
import arcpy
from pprint import pprint
import os

# raster_path = r"C:\Users\Administrator\Documents\同步空间\3_RasterData\SRTM30-90\GanZi\MinyaKonka\1RawData\Merged.tif"
# new_raster_path = r"C:\Users\Administrator\Documents\同步空间\3_RasterData\SRTM30-90\GanZi\MinyaKonka\2ProcessedData"
# raster_path = r"C:\Users\Administrator\Documents\同步空间\1.Blog\2.MapMake\3.NEW长白山\1.DataANDMap\scene2.tif"
# new_raster_path = r"C:\Users\Administrator\Documents\同步空间\1.Blog\2.MapMake\3.NEW长白山\1.DataANDMap"

# raster_path = r"C:\Users\Administrator\Documents\同步空间\1.Blog\2.MapMake\00.Blender渲染中国包括周边地图\1.Data\DEMWithAllPositive.tif"
# new_raster_path = r"C:\Users\Administrator\Documents\同步空间\1.Blog\2.MapMake\00.Blender渲染中国包括周边地图\1.Data"
# new_raster_name = r"RescaleMerged_30.tif"

raster_path = r"D:\BaiduSyncdisk\4.Blender\5.Render\1.中华民国全图\1.TIFFAndDEM\ETOPO1DEM范围扩大后.tif"
new_raster_path = r"D:\BaiduSyncdisk\4.Blender\5.Render\1.中华民国全图\1.TIFFAndDEM"
new_raster_name = r"ETOPO1DEMRescale.tif"

if not os.path.isfile(raster_path):
    raise FileNotFoundError("FileNotFoundError")

if not os.path.isdir(new_raster_path):
    raise FileExistsError("FileNotFoundError")

# Useful Para
raster_file = arcpy.Raster(raster_path)
arcpy.env.overwriteOutput = True
arcpy.env.compression = "LZW"
arcpy.env.outputCoordinateSystem = raster_file  # 必须
arcpy.env.cellSize = raster_file
arcpy.env.tileSize = "128 128"
x = raster_file.extent.XMin
y = raster_file.extent.YMin

raster_array = arcpy.RasterToNumPyArray(raster_file)
raster_max = raster_array.max()
raster_min = raster_array.min()
desc = arcpy.Describe(raster_file)
cell_h, cell_w = desc.meanCellHeight, desc.meanCellWidth
cellsize = 'Hight = {0}, Width = {1}'.format(cell_h, cell_w)

pprint(raster_array)
print(raster_max)
print(raster_min)
print(cellsize)

# DEM 数据标准化
new_array = ((raster_array - raster_min) / (raster_max - raster_min)) * 65535
# new_array = new_array.astype(np.uint16)
pprint(new_array)
pprint(new_array.mean())
print("---")
print(new_array.shape)
print(new_array.ndim)

# 使用 arcpy.Point(x, y) 锚定左下角坐标才能使栅格数据的坐标正确
new_raster = arcpy.NumPyArrayToRaster(new_array, arcpy.Point(x, y),
                                      cell_w, cell_h)

# arcpy.MosaicToNewRaster_management(new_raster, new_raster_path,
#                                    new_raster_name,
#                                    pixel_type="16_BIT_UNSIGNED",
#                                    number_of_bands=1)

arcpy.CopyRaster_management(new_raster, os.path.join(new_raster_path, new_raster_name),
                                   pixel_type="16_BIT_UNSIGNED")

# cellsize=int(cell_h),

print(type(new_raster))
print(type(raster_file))

# 栅格数据导出
# new_raster.save(new_raster_path)
