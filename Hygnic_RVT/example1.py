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
import rvt.default
from pprint import pprint


"""--------DATA"""

# 峨眉山附近
raster_dataset = r"D:\MyProject\BaiduNetdiskWorkspace\1.Blog\7_可视化\000_rvt介绍\1_data\SRTMv3_1_N29E103_峨眉山附近.tif"

"""--------"""


dem_dict = rvt.default.get_raster_arr(raster_dataset)
