#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.23
# Modified    :   2017.1.23
# Version     :   1.0
# equation.py

from sympy import *
x = symbols('x')
result = solve(Eq((-9/50.0)*x**2+60.0*x,433),x)
print result