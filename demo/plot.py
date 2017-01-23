#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
# Version     :   1.0
# plot.py

import numpy as np
from scipy import stats
from matplotlib import pyplot as plt
n=3600  
k=np.arange(n+1)  
pcoin = np.arange(n+1)
plt.plot(k[0:30],pcoin[0:30],'o-')
k = [1,2,3,4,5,6]
pcoin= [6,5,4,3,2,1]
plt.plot(k,pcoin,'o-')
plt.title("binomial: n=%i, p=%.2f"%(n,0.0008),fontsize=15)
plt.xlabel("number of successes")
plt.ylabel("probability of successes", fontsize=15)
plt.show()