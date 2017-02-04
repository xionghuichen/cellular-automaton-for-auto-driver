#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.2.4
# Modified    :   2017.2.4
# Version     :   1.0


# iterator.py

a = range(1,6)
print a
for index,i in enumerate(a):
    if index == 2:
        temp = a[index]
        print "temp %s"%temp
        a[index] = 99
        print "temp %s"%temp
        del a[index]
        print "temp %s"%temp
print a
for i in a:
    if i == 1:
        a.append(10)
    print i
print a
# 结论，遍历过程中删除一个元素不会影响遍历
# 遍历过程中加入一个元素，这个元素会参与遍历

# 和其他语言不一样，传递参数的时候，
# python不允许程序员选择采用传值还是传引用。
# Python参数传递采用的肯定是“传对象引用”的方式。
# 实际上，这种方式相当于传值和传引用的一种综合。
# 如果函数收到的是一个可变对象（比如字典或者列表）的引用，就能修改对象的原始值－－
# 相当于通过“传引用”来传递对象。如果函数收到的是一个不可变对象（比如数字、字符或者元组）的引用，
# 就不能直接修改原始对象－－相当于通过“传值'来传递对象。
# 如果a=b的话， a和b的地址是相同的；如果只是想拷贝，那么就得用 a=b[:]。
#　python一般内部赋值变量的话，都是传个引用变量，和C语言的传地址的概念差不多。可以用id()来查询内存地址