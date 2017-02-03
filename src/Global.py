#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.27
# Modified    :   2017.1.27
# Version     :   1.0
# Golbal.py
# 长度单位：英里
# 时间单位：小时

MAX_PATH = 5
TIME_SLICE = 1
CELL_RATIO = 1000
MAX_VELOCITY = int(60.0/3600*CELL_RATIO*TIME_SLICE)
mile_per_kilometer = 0.621
mile_per_meter = mile_per_kilometer / 1000

CARS_INFO = [
    {'type':0,'length':(4.5+1.5)*mile_per_meter,'max_velocity':60.0,'slow_rate':0.04,'safe_distance':1},# slef drive car
    {'type':1,'length':(4.5+1.5)*mile_per_meter,'max_velocity':60.0,'slow_rate':0.33,'safe_distance':2}# not self drive car
]

print MAX_VELOCITY