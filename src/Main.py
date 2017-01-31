#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
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
# cell_handler = CellularHandler(sh,[0,1])
# cell_handler.driver(5)
ratios = [0,1]
input_data = []
nrows = sh.nrows
for i in range(1,nrows):
    row_data = sh.row_values(i)
    peak_ratio = 0.08
    peak_hours = 3
    mile_per_kilometer = 0.621
    mile_per_meter = mile_per_kilometer / 1000
    volume_per_hours = row_data[3] * peak_ratio / peak_hours / (row_data[5] + row_data[6]) * row_data[6] * 1.5
    avg_velocity = sum([a['max_velocity']*b for a,b in zip(CARS_INFO,ratios)]) * mile_per_kilometer
    avg_length = sum([a['length']*b for a,b in zip(CARS_INFO,ratios)])
    safe_distance = 0.5 
    max_density = 1/((avg_length+safe_distance)*mile_per_meter)
    x = symbols('x')
    density_per_miles = max(solve(Eq(avg_velocity*(x - (1/max_density)*x**2),volume_per_hours),x))
    item = {'id':row_data[0],'startpost':row_data[1],'endpost':row_data[2],'density':density_per_miles}
    print item
    print volume_per_hours
    print max_density