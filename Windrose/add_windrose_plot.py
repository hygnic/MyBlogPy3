# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              add_windrose_plot
# Author:            Hygnic
# Created on:        2021/7/18 19:41
# Version:           
# Reference:         
"""
Description:         将风玫瑰图添加到地图中；
                     使用 PIL 模块
Usage:               
"""
# -------------------------------------------
from PIL import Image

# Get map size
#   map_x: map image X
#   map_x: map image Y
map_path = "map.jpg"
we_map = Image.open(map_path)
map_x = we_map.size[0]
map_y = we_map.size[1]
# 风玫瑰图与边框的距离
offset_x , offset_y = 420, 420

# Get windrose image size:
#   w_d_x: windrose image X
#   w_d_y: windrose image Y
windrose_path = "wind-rose.png"
windrose = Image.open(windrose_path)
print(windrose.size)
w_d_x = windrose.size[0]
w_d_y = windrose.size[1]


x_topleft = map_x - offset_x - w_d_x
y_topleft = offset_y
x_bottomright = map_x - offset_x
y_bottomright = offset_y + w_d_y
box=(x_topleft, y_topleft, x_bottomright, y_bottomright)


# 使用透明图层为掩膜裁剪出目标区域。
clip_mask = windrose.convert('RGBA')
we_map.paste(windrose, box, clip_mask)
we_map.save("test.jpg")
# we_map.show()