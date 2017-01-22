#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
# Version     :   1.0

# Main.py

#encoding=utf-8
import xlrd
import xlwt
import json
fname = "../Resource/2017_MCM_Problem_C_Data2.xlsx"
import logging

from Handler import CellularHandler

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
cell_handler = CellularHandler(sh,[0,1])
cell_handler.driver(5)