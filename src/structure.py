#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.21
# Modified    :   2017.1.22
# Version     :   1.0
# structure.py

from functions import do_probability_test
"""
车的基类
"""
class BasicCar(object):
	
	def __init__(self, init_vel,length,location,max_velocity,safe_distance):
		self.velocity=init_vel # 当前行驶速度
		self.max_velocity=max_velocity# 车辆的限制速度
		self.length=length# 车辆长度
		self.location=location# 车辆当前的位置，在路段的多个车道内定义:[x,y]
		self.accelerate=1# 车辆的等效加速度
		self.safe_distance= safe_distance
		self.slow_rate = 0.2
		self.slow_rate_low = 0.01
		self.slow_velocity = 1

	def change_lanes(self, around_cars):	
		"""
			around_cars: include 
				left_forward_car,
				left_back_car, 
				right_forward_car, 
				right_back_car
			根据左右最近车的位置情况做出车道变道决策
			1. 首先考虑右车道
				- 右车道和当前车道的距离大于其最大速度所行驶的距离
		"""

	def get_lanes(self):
		"""
			返回该车辆现在所在的车道位置
		"""
		return self.location[0]

	def update_place(self):
		"""
			设置新的坐标位置
		"""
		self.location[1] = self.location[1] + self.velocity

	def get_place(self):
		"""
			返回该辆车现在所在的前进的位置
		"""
		return self.location[1]

	def get_ditance(self, another_car):
		"""
			headway = 两辆车的坐标差- 前面的车的长度
		"""
		distance = abs(another_car.location - self.location)
		if self.location.get_place() > another_car.get_place():
			length = self.length
		else:
			length = another_car.length
		return distance - length

	def get_slow_rate(self,vn):
		"""
			获得随机慢化概率
		"""
		if vn == self.max_velocity or vn ==0:
			return self.slow_rate_low
		else:
			return sekf.slow_rate

	def do_slow(self,vn):
		return max(vn-self.slow_velocity,0)

	def update_status(self, around_cars):
		"""
			around_cars: include 
				forward_cars
				forward_forward_cars
				back_cars
			i. 加速过程：Vn->min(vn+1,vmax)
				1) 私家车和自动驾驶汽车应该有不同的加速度，1应该取值不同，下同
			ii. 减速过程【应用加速效应模型进行改进】：vn->min(vn,,dn+v'n+1)[n号的加速度为1[最大加速度]，和考虑了前车的位移的情况下的两者的间距]
				1) 为了避免相撞
				2) v'n+1=vn+1 - dsafe[安全距离]
				3) 对于自动驾驶汽车而言，安全距离减小，因为他能够灵活反应，对应在元胞机中，自动驾驶汽车是在私家车做出决策之后进行的决策，所以他所看到的私家车的vn是确定化的vn不会产生冲突
			iii. 随机慢化：
				1) 随机慢化的思想：模拟驾驶员状态导致的慢化
				2) 【应用巡航驾驶极限模型和VDR慢启动规则改进】
					a) 思想：
						i) 以期望的速度行驶[vmax]，不受随机慢化影响
						ii) 在上一刻静止的车辆，随机慢化的概率更大
					b) Pc = p(v) ->当v=0和v=max的时候，随机慢化概率远小于1，其他时间段随机慢化较高
					c) 进行随机慢化，在pc的概率下，vn->max(vn-1,0)
				3) 由于自动驾驶汽车的特性，其pc函数的值应该比私家车的低
			iv. 进行运动决策：xn->xn+vn
			v. 注意，这之前的步骤是每个步骤都要走一遍的，直到最后一步完成之后，再更新状态
		"""
		# 加速
		vn = min(self.velocity+self.accelerate, self.max_velocity)
		# 减速
		v_forward_imaginary = around_cars['car_n+1'].velocity + min(
			around_cars.max_velocity,around_cars.velocity,max(0,around_cars['car_n+1'].get_ditance(around_cars['car_n+2'])))
		vn = min(vn,self.get_ditance(around_cars['car_n'])+v_forward_imaginary)
		# 随机慢化
		# 计算当前随机漫画概率
		slow_rate = self.get_slow_rate(vn)
		if do_probability_test(slow_rate):
			# 进行随机慢化
			vn = self.do_slow(vn)
		# 更新速度
		self.velocity = vn
		# 更新坐标
		self.update_place()
		
