# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              example1
# Author:            Hygnic
# Created on:        2021/12/30 12:35
# Version:           
# Reference:         
"""
Description:         适用于投影完成后的数据
Usage:               
"""
# -------------------------------------------
# G:\MoveOn\MyBlogPy3\Hygnic_RVT\create_SVF_projected.py

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
# filepath = r"E:\MyD\BaiduNetdiskWorkspace\1.Blog\7_可视化\rrim系列作品\4_梵净山\1_data"
# filepath = r"E:\MyD\BaiduNetdiskWorkspace\1.Blog\7_可视化\rrim系列作品\5_梅里雪山\1_data"
filepath = r"E:\MyD\Tonga\GEBCO_16_Jan_2022_2ca57a5386c0"
filename = os.path.join(filepath, "zc_projected.tif")
os.chdir(filepath)



"""--------RASTER_INFO"""
dem_dataset = filename
dem_dict = rvt.default.get_raster_arr(dem_dataset)
dem_arr = dem_dict["array"]  # numpy array of DEM
dem_resolution = dem_dict["resolution"]
dem_res_x = dem_resolution[0]  # resolution in X direction
dem_res_y = dem_resolution[1]  # resolution in Y direction

sun_azimuth = 315  # Solar azimuth angle (clockwise from North) in degrees
sun_elevation = 45  # Solar vertical angle (above the horizon) in degrees


"""--------Hillshade"""
hillshade_arr = rvt.vis.hillshade(
    dem=dem_arr, resolution_x=dem_res_x,
    resolution_y=dem_res_y,sun_azimuth=sun_azimuth,
    sun_elevation=sun_elevation, ve_factor=1)

hillshade_path = "Hillshade_315_45_f1.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=hillshade_path, out_raster_arr=hillshade_arr,
                        e_type=6)
print("Hillshade Exported")


"""--------Multiple directions hillshade"""
nr_directions = 16  # Number of solar azimuth angles (clockwise from North) (number of directions, number of bands)
sun_elevation = 45  # Solar vertical angle (above the horizon) in degrees
multi_hillshade_arr = rvt.vis.multi_hillshade(
    dem=dem_arr, resolution_x=dem_res_x,
    resolution_y=dem_res_y,
    nr_directions=nr_directions,
    sun_elevation=sun_elevation, ve_factor=1)

multi_hillshade_path = "MultiHS.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=multi_hillshade_path, out_raster_arr=multi_hillshade_arr,
                        e_type=6)
print("Multi_Hillshade Exported")


"""--------------------Slope"""
dict_slope_aspect = rvt.vis.slope_aspect(
    dem=dem_arr, resolution_x=dem_res_x,
    resolution_y=dem_res_y, output_units="degree",
    ve_factor=1)
slope_arr = dict_slope_aspect["slope"]
slope_name = "slope.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=slope_name, out_raster_arr=slope_arr,
                        e_type=6)
print("Slope Exported")


"""--------Positive_openness & SVF"""
svf_n_dir = 16  # number of directions
svf_r_max = 10  # max search radius in pixels
svf_noise = 3  # level of noise remove (0-don't remove, 1-low, 2-med, 3-high)
dict_svf = rvt.vis.sky_view_factor(
    dem=dem_arr, resolution=dem_res_x,
    compute_svf=True, compute_asvf=False,
    compute_opns=False,svf_n_dir=svf_n_dir,
    svf_r_max=svf_r_max, svf_noise=svf_noise)

SVF_arr = dict_svf["svf"]
svf_arr_name = "SVF_denoise3.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=svf_arr_name, out_raster_arr=SVF_arr,
                        e_type=6)

print("SVF_3 Exported")

svf_noise = 1  # level of noise remove (0-don't remove, 1-low, 2-med, 3-high)
dict_svf = rvt.vis.sky_view_factor(
    dem=dem_arr, resolution=dem_res_x,
    compute_svf=True, compute_asvf=False,
    compute_opns=False,svf_n_dir=svf_n_dir,
    svf_r_max=svf_r_max, svf_noise=svf_noise)

SVF_arr = dict_svf["svf"]
svf_arr_name = "SVF_denoise1.tif"
rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=svf_arr_name, out_raster_arr=SVF_arr,
                        e_type=6)
print("SVF_1 Exported")


# """--------Negative_openness"""
# dem_arr_neg_opns = dem_arr * -1  # dem * -1 for neg opns
# # we don't need to calculate svf and asvf (compute_svf=False, compute_asvf=False)
# dict_svf = rvt.vis.sky_view_factor(
#     dem=dem_arr_neg_opns, resolution=dem_res_x,
#     compute_svf=False, compute_asvf=False,
#     compute_opns=True,svf_n_dir=svf_n_dir,
#     svf_r_max=svf_r_max, svf_noise=svf_noise)
#
# neg_opns_arr = dict_svf["opns"]
# neg_opns_arr_path = "Negative_openness.tif"
#
# rvt.default.save_raster(src_raster_path=dem_dataset, out_raster_path=neg_opns_arr_path, out_raster_arr=neg_opns_arr,
#                         e_type=6)
# print("Negative_openness Exported")