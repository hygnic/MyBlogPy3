# -*- coding:utf-8 -*-
# -------------------------------------------
# Name:              t1
# Author:            Hygnic
# Created on:        2021/7/21 17:16
# Version:           
# Reference:         
"""
Description:         
Usage:               
"""
# -------------------------------------------
from math import pi, exp, cos, sin, radians
from os.path import basename, isdir

from os import makedirs
import subprocess
from svgpathtools import Line, svg2paths, Path, parse_path
from svgwrite import Drawing, rgb

# from svgpathtools.svg2paths  import combine_transforms, transform_path
# from utils import calc_overall_bbox, get_paletton
import argparse
import xml.dom.minidom

def cexp(x):
    return pow(exp(1), x)
angle01 = 60.0
length1 = 300
# start with the top corner at 0, 0
points = [0, None, None, None, None]
points[1] = points[0] + length1 * cexp(1j * radians(angle01))
points[4] = points[0] + length1 * cexp(-1j * radians(angle01))
angle12 = -(90 - angle01)
points[2] = points[1] + length1 * cexp(1j * radians(angle12))
points[3] = points[4] + length1 * cexp(-1j * radians(angle12))


def new_pentagon():
    return Path(*[Line(start=points[i - 1], end=points[i]) for i in range(len(points))])

transforms = [[0, 0]]
cairo_group = [new_pentagon()]
# point 1 of pentagon 1 needs to be attached to point 1 of pentagon 0
cairo_group.append(transform_path(rotate_transform(90), new_pentagon()))
diff = cairo_group[0][1].end - cairo_group[1][1].end
transforms.append([90, diff])
cairo_group[1] = cairo_group[1].translated(diff)
cairo_group.append(transform_path(rotate_transform(180), new_pentagon()))
# point 3 of pentagon 2 needs to be attached to point 2 of pentagon 0
diff = cairo_group[0][2].end - cairo_group[2][3].end
transforms.append([180, diff])
cairo_group[2] = cairo_group[2].translated(diff)
cairo_group.append(transform_path(rotate_transform(-90), new_pentagon()))
# point 4 of pentagon 3 needs to be attached to point 1 of pentagon 0
diff = cairo_group[0][4].end - cairo_group[3][4].end
transforms.append([-90, diff])
cairo_group[3] = cairo_group[3].translated(diff)