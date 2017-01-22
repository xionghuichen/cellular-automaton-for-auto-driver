#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
# Version     :   1.0

import random

def do_probability_test(rate):
	"""
		指定概率必须是两位小数，即0.00~100.00
	"""
	 result = random.randint(0, 10000)
	 if result < rate*100:
	 	return True
	 else:
	 	return False