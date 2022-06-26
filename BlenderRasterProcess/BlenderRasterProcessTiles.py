# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              BlenderRasterProcess
# Author:            Hygnic
# Created on:        2022/4/1 22:05
# Version:           
# Reference:         
"""
Description:    导出0-65535范围内的uint16位的栅格数据，使用了分块技术，
将栅格分成小块分别计算后再镶嵌在一起。可以避免有的超大栅格直接处理合并报错：
“RuntimeError: 像素块超出了允许的最大尺寸”

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
fileout = os.path.join(new_raster_path, new_raster_name)
# 临时存放分块的栅格数据
tempfolder = os.path.join(new_raster_path, "temp")
if not os.path.exists(tempfolder):
    os.makedirs(tempfolder)

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
arcpy.env.resamplingMethod = "BILINEAR"
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


blocksize = 1024*10 # 512
filelist = []
blockno = 0
for x in range(0, raster_file.width, blocksize):
    for y in range(0, raster_file.height, blocksize):
        # Lower left coordinate of block (in map units)
        mx = raster_file.extent.XMin + x * raster_file.meanCellWidth
        my = raster_file.extent.YMin + y * raster_file.meanCellHeight
        # Upper right coordinate of block (in cells)
        lx = min([x + blocksize, raster_file.width])
        ly = min([y + blocksize, raster_file.height])

        # Extract data block
        raster_array = arcpy.RasterToNumPyArray(raster_file, arcpy.Point(mx, my),
                                          lx-x, ly-y)

        # PROCESS DATA BLOCK -----------------------------
        # e.g. DEM 数据标准化
        new_array = ((raster_array - raster_min) / (raster_max - raster_min)) * 65535
        # ------------------------------------------------

        # Convert data block back to raster
        myRasterBlock = arcpy.NumPyArrayToRaster(new_array, arcpy.Point(mx, my),
                                                 raster_file.meanCellWidth,
                                                 raster_file.meanCellHeight)

        # Save on disk temporarily as 'filename_#.ext'
        # filetemp = ('_%i.' % blockno).join(fileout.rsplit('.',1))
        filetemp = os.path.join(tempfolder, "temp_{}.tif".format(blockno))
        # filetemp = ('_%i.' % blockno).join(["temp", "tif"])
        print(filetemp)
        myRasterBlock.save(filetemp)
        # Maintain a list of saved temporary files
        filelist.append(filetemp)
        blockno += 1


# Mosaic temporary files

arcpy.env.workspace = tempfolder
blockrasters = arcpy.ListRasters()
print(tempfolder)
print(blockrasters)
arcpy.MosaicToNewRaster_management(blockrasters, new_raster_path,
                                              new_raster_name,
                                              pixel_type="16_BIT_UNSIGNED",
                                              number_of_bands=1)
                                   
# Mosaic_management 方法很慢
# arcpy.Mosaic_management(';'.join(filelist[1:]), filelist[0])
# if arcpy.Exists(fileout):
#     arcpy.Delete_management(fileout)
# arcpy.Rename_management(filelist[0], fileout)

# Remove temporary files
for fileitem in blockrasters:
    if arcpy.Exists(fileitem):
        arcpy.Delete_management(fileitem)
os.rmdir(tempfolder)
#
# Release raster objects from memory
del myRasterBlock
del raster_file

