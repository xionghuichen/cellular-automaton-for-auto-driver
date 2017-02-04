#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.2.1
# Version     :   1.0

# Main.py

#encoding=utf-8
# import pudb; pu.db
import xlrd 
import xlwt
import json
fname = "../Resource/2017_MCM_Problem_C_Data2.xlsx"
import logging
from sympy import *
from Handler import CellularHandler
from Global import CARS_INFO, CELL_RATIO
from matplotlib import pyplot as plt
import numpy as np
logging.basicConfig(level=logging.INFO,
                    filename='log.log',
                    filemode='w')

bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
 sh = bk.sheet_by_name("parsed mile posts")
except:
 print "no sheet in %s named parsed mile posts" % fname
nrows = sh.nrows
#获取列数
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows,ncols)
#获取第一行第一列数据 
ratios = [0,1]
input_data = {}
nrows = sh.nrows
# calculate density from vehicle amount.
avg_length = sum([a['length']*b for a,b in zip(CARS_INFO,ratios)])
max_density = 1/avg_length
avg_velocity = sum([a['max_velocity']*b for a,b in zip(CARS_INFO,ratios)])
print "max_density : %s"%max_density
print "avg velocity : %s"%avg_velocity
for i in range(1,nrows):
    row_data = sh.row_values(i)
    peak_ratio = 0.08
    peak_hours = 3
    direct_selected = row_data[6]
    volume_per_hours = row_data[3] * peak_ratio / peak_hours / (row_data[5] + row_data[6]) * 1.5

    x = symbols('x')
    density_per_miles = max(solve(Eq(x*avg_velocity*log(max_density/x),volume_per_hours),x))
    # density_per_miles = max(solve(Eq(avg_velocity*(x - (1/max_density)*x**2),volume_per_hours),x))
    item = {'id':row_data[0],'startpost':row_data[1],'endpost':row_data[2],'density':density_per_miles,'path_number':direct_selected}
    if input_data.has_key(item['id']):
        # 不是第一个数据
        input_data[item['id']].append(item)
    else:
        # 是第一个数据
        input_data[item[ 'id']] = [item]
    print item
    print "volume_per_hours : %s"%volume_per_hours
# print input_data
# volume = []
# velocity = []
# density_list = range(1,int(max_density),5)
# for density in density_list:
#     input_data = {5.0: [{'path_number': 1.0, 'endpost': 11.56, 'startpost': 10.15, 'id': 5.0, 'density': density}]}
#     cell_handler = CellularHandler(input_data,ratios)
#     (vo,ve)=cell_handler.driver(5)
#     volume.append(vo)
#     velocity.append(ve)
# print volume
# print velocity
# plt.subplot(3,1,1)
# plt.plot(velocity,volume,'o')
# c1 = np.polyfit(velocity,volume,5)
# x_new = np.linspace(5,58,2000)
# y_new = np.polyval(c1,x_new)
# plt.plot(x_new,y_new)
# plt.xlabel("velocity /mph")
# plt.ylabel("volume /vph", fontsize=15)
# plt.title("relation between velocity and volume")
# plt.subplot(3,1,2)
# plt.plot(density_list,velocity,'o')
# c2 = np.polyfit(density_list,velocity,1)
# x_new = np.linspace(0,max_density,2000)
# y_new = np.polyval(c2,x_new)
# plt.plot(x_new,y_new)
# plt.xlabel("density /vpm")
# plt.ylabel("velocity /mph", fontsize=15)
# plt.title("relation between density and velocity")
# plt.subplot(3,1,3)
# plt.plot(density_list,volume,'o')
# c3 = np.polyfit(density_list,volume,4)
# x_new = np.linspace(0,max_density,2000)
# y_new = np.polyval(c3,x_new)
# plt.plot(x_new,y_new)
# plt.xlabel("density /vpm")
# plt.ylabel("volume /vph", fontsize=15)
# plt.title("relation between density and volume")
# print c1
# print c2
# print c3
# plt.show()

input_data = {5.0: [{'path_number': 2.0, 'endpost': 11.56, 'startpost': 10.15, 'id': 5.0, 'density': 210}]}
cell_handler = CellularHandler(input_data,ratios)
(vo,ve)=cell_handler.driver(5)