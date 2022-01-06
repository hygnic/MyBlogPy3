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
# 可能原因：管理员运行 Pycharm 试试
# 将miniconda 只装到个人用户下

"""--------IMPORT_SETTINGS"""

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
filename = os.path.join(filepath, "SRTMv3_1_N32E105.tif")
output_raster = os.path.join(filepath, "After_p.tif")
os.chdir(filepath)


"""--------REPROJ"""
input_raster = gdal.Open(filename)
warp = gdal.Warp(output_raster,input_raster,dstSRS='EPSG:4544',resampleAlg="cubic")
input_raster = None # Closes the files

# CGCS2000_3_Degree_GK_CM_105E
# WKID: 4544 权限: EPSG


"""--------RASTER_INFO"""
dem_dataset = output_raster
dem_dict = rvt.default.get_raster_arr(dem_dataset)
dem_arr = dem_dict["array"]  # numpy array of DEM
dem_resolution = dem_dict["resolution"]
dem_res_x = dem_resolution[0]  # resolution in X direction
dem_res_y = dem_resolution[1]  # resolution in Y direction

sun_azimuth = 315  # Solar azimuth angle (clockwise from North) in degrees
sun_elevation = 45  # Solar vertical angle (above the horizon) in degrees


# """--------Hillshade"""
# hillshade_arr = rvt.vis.hillshade(
#     dem=dem_arr, resolution_x=dem_res_x,
#     resolution_y=dem_res_y,sun_azimuth=sun_azimuth,
#     sun_elevation=sun_elevation, ve_factor=1)
#
# hillshade_path = "Hillshade_315_45_f1.tif"
# rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=hillshade_path, out_raster_arr=hillshade_arr,
#                         e_type=6)
# print("Hillshade Exported")


# """--------Multiple directions hillshade"""
# nr_directions = 16  # Number of solar azimuth angles (clockwise from North) (number of directions, number of bands)
# sun_elevation = 45  # Solar vertical angle (above the horizon) in degrees
# multi_hillshade_arr = rvt.vis.multi_hillshade(
#     dem=dem_arr, resolution_x=dem_res_x,
#     resolution_y=dem_res_y,
#     nr_directions=nr_directions,
#     sun_elevation=sun_elevation, ve_factor=1)
#
# multi_hillshade_path = "MultiHS.tif"
# rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=multi_hillshade_path, out_raster_arr=multi_hillshade_arr,
#                         e_type=6)
# print("Multi_Hillshade Exported")


"""--------Positive_openness"""
svf_n_dir = 16  # number of directions
svf_r_max = 10  # max search radius in pixels
svf_noise = 0  # level of noise remove (0-don't remove, 1-low, 2-med, 3-high)
dict_svf = rvt.vis.sky_view_factor(
    dem=dem_arr, resolution=dem_res_x,
    compute_svf=False, compute_asvf=False,
    compute_opns=True,svf_n_dir=svf_n_dir,
    svf_r_max=svf_r_max, svf_noise=svf_noise)

opns_arr = dict_svf["opns"]
opns_arr_path = "Positive_openness.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=opns_arr_path, out_raster_arr=opns_arr,
                        e_type=6)

print("Positive_openness Exported")


"""--------Negative_openness"""
dem_arr_neg_opns = dem_arr * -1  # dem * -1 for neg opns
# we don't need to calculate svf and asvf (compute_svf=False, compute_asvf=False)
dict_svf = rvt.vis.sky_view_factor(
    dem=dem_arr_neg_opns, resolution=dem_res_x,
    compute_svf=False, compute_asvf=False,
    compute_opns=True,svf_n_dir=svf_n_dir,
    svf_r_max=svf_r_max, svf_noise=svf_noise)

neg_opns_arr = dict_svf["opns"]
neg_opns_arr_path = "Negative_openness.tif"

rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=neg_opns_arr_path, out_raster_arr=neg_opns_arr,
                        e_type=6)
print("Negative_openness Exported")