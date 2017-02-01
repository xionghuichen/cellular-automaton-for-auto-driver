#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.2.1
# Modified    :   2017.2.1
# Version     :   1.0


# readonly.py
class test(object):
    def __init__(self):
        self._a = 10
        self.b = 11

    @property
    def aa(self):
        return self.a

    @property
    def bb(self):
        return self.b

    @bb.setter
    def bb(self,value):
        self.b = value
# 如果只有property， 无法进行初始化
t = test()
# t.a = 11

print t.a