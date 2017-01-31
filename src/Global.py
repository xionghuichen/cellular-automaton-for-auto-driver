#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.27
# Modified    :   2017.1.27
# Version     :   1.0
# Golbal.py
CARS_INFO = [
	{'type':0,'length':4.5,'max_velocity':60,'slow_rate':0.04,'safe_distance':1},# slef drive car
	{'type':1,'length':4.5,'max_velocity':60,'slow_rate':1/64,'safe_distance':2}# not self drive car
]
MAX_PATH = 5
TIME_SLICE = 1
CELL_RATIO = 15