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
for i in range(1,nrows):
    row_data = sh.row_values(i)
    peak_ratio = 0.08
    peak_hours = 3
    direct_selected = row_data[6]
    volume_per_hours = row_data[3] * peak_ratio / peak_hours / (row_data[5] + row_data[6]) * 1.5
    avg_velocity = sum([a['max_velocity']*b for a,b in zip(CARS_INFO,ratios)])
    avg_length = sum([a['length']*b for a,b in zip(CARS_INFO,ratios)])
    max_density = 1/avg_length
    x = symbols('x')
    density_per_miles = max(solve(Eq(avg_velocity*(x - (1/max_density)*x**2),volume_per_hours),x))
    item = {'id':row_data[0],'startpost':row_data[1],'endpost':row_data[2],'density':density_per_miles,'path_number':direct_selected}
    if input_data.has_key(item['id']):
        # 不是第一个数据
        input_data[item['id']].append(item)
    else:
        # 是第一个数据
        input_data[item['id']] = [item]
    print item
    print volume_per_hours
    print max_density

cell_handler = CellularHandler(input_data,ratios)
cell_handler.driver(5)
