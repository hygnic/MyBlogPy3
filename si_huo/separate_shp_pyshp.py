# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              separate_shp
# Author:            Hygnic
# Created on:        2021/8/6 14:49
# Version:           
# Reference:         
"""
Description:         使用 PyShp 分割shp文件
Usage:               
"""
# -------------------------------------------
import shapefile

# shp_path = r"D:\新建文件夹 (2)\数据处理\FWX.shp"
shp_path = r"D:\新建文件夹 (2)\数据处理\CBDKXXDZ.shp"

with shapefile.Reader(shp_path, encoding='cp936') as shp:
    if shp.shapeType != shapefile.POLYGON:
        raise TypeError("Polygon only.")
    # shape = shp.shapes()
    # for name in dir(shape[0]):
    #     print(name)
    
    fields = shp.fields # 字段组成的列表
    # print(fields)
    
    rec = shp.record(-1)
    print(rec)
    print(rec["QSDWMC"])
    # for _ in rec:
        # print(_)
    