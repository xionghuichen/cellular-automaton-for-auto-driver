#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
# Version     :   1.0

import random
import numpy as np
from scipy import stats

def do_probability_test(rate):
	"""
		指定概率必须是两位小数，即0.00~1.00
	"""
	result = random.randint(0, 100)
	if result < rate*100:
	 	return True
	else:
	 	return False

def binomial_creator(n,rate):
	"""
		生成二项分布的概率
	"""
	k=np.arange(n+1)
	probability=stats.binom.pmf(k,n,rate) 
	acc_pro = accumulator(probability)
	return acc_pro

def accumulator(rate_list):
	last_pro = 0
	acc_pro = []
	for value in rate_list:
		acc_pro.append(last_pro + value)
		last_pro = acc_pro[-1]
	return acc_pro

def multi_probility_test(rate_list):
	result = random.randint(0,10000)
	for key,value in enumerate(rate_list):
		if value*10000 >= result:
			return key
# count = 0
# while count < 10:
# 	print multi_probility_test(binomial_creator(100,0.05))
# 	count  = count + 1
