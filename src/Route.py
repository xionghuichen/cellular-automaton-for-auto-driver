#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.1.22
# Version     :   1.0
# Route.py

"""
路线类，包含了一个公路的诸多段落
"""
from functions import binomial_creator
import numpy as np
import random
import json
import logging
from matplotlib import pyplot as plt
class Route(object):
	def __init__(self,route_id,resource_item_list, time_slice):
		"""
		构造道路路段
		"""
		self.route_id = route_id# 该路线的id
		self.route_amount = len(resource_item_list)# 改路线拥有的道路的个数 
		self.road_list =[]# 构造每一个道路路段的数据结构
		for value in resource_item_list:
			self.road_list.append(Road(value, time_slice))

"""
公路段类，包含了两个方向的公路,对应excel的一调数据
"""
class Road(object):
	def __init__(self,resource_item, time_slice):
		"""
			构造一个路段
		"""
		self.startpost = resource_item[0]# A marker on the road that measures distance in miles from either the start of the route or a state boundary.
		self.endpost = resource_item[1]# The average number of cars per day driving on the road.
		self.traffic_amount = resource_item[2]# average daily traffic
		self.tre_type = resource_item[3]# interstate or state route 
		self.increase_dir = resource_item[4]# Northbound for N-S roads, Eastbound for E-W roads.
		self.decrease_dir = resource_item[5]# Southbound for N-S roads,  Westbound for E-W roads.
		self.peak_hours=2
		self.no_peak_hours = 18
		self.peak_ratio = 0.08
		self.no_peak_ratio = 0.8
		self.time_slice = time_slice
		# self.no_peak_amount_per_hours = self._no_peak_amount_per_hours()
		# 累加的二项分布概率
		
		self.acc_bi_peak = []
		self.acc_bi_no_peak = []
		self.inc_path=Path(self.increase_dir, self.startpost, self.endpost)
		self.dec_path=Path(self.decrease_dir, self.startpost, self.endpost)

	def get_Singleton_peak(self,last_amount,direction='up'):
		if self.acc_bi_peak== []:
			self.peak_amount_per_hours = self._peak_amount_per_hours(last_amount)
			probability_of_single_car = (self.peak_amount_per_hours/3600*self.time_slice)/(3600*self.time_slice)
			if direction == 'up':
				probability_of_single_car = probability_of_single_car * self.increase_dir
				amount_per_hours = self.peak_amount_per_hours* self.increase_dir
			else:
				probability_of_single_car = probability_of_single_car * self.decrease_dir
				amount_per_hours = self.peak_amount_per_hours* self.decrease_dir
			self.acc_bi_peak = binomial_creator(amount_per_hours,probability_of_single_car)
		return self.acc_bi_peak

	def get_Singleton_no_peak(self,last_amount,direction='up'):
		if self.acc_bi_no_peak== []:
			self.peak_amount_per_hours = self._peak_amount_per_hours()
			probability_of_single_car = (self.peak_amount_per_hours/3600*self.time_slice)/(3600*self.time_slice)
			if direction == 'up':
				probability_of_single_car = probability_of_single_car * self.increase_dir
				amount_per_hours = self.peak_amount_per_hours* self.increase_dir
			else:
				probability_of_single_car = probability_of_single_car * self.decrease_dir
				amount_per_hours = self.peak_amount_per_hours* self.decrease_dir
			self.acc_bi_no_peak = binomial_creator(amount_per_hours, probability_of_single_car)
		return self.acc_bi_no_peak
	
	def _peak_amount_per_hours(self, last_amount):
		return (self.traffic_amount - last_amount)* self.peak_ratio / self.peak_hours/(self.increase_dir + self.decrease_dir)

	def _no_peak_amount_per_hours(self, last_amount):
		return (self.traffic_amount - last_amount) * self.no_peak_ratio / self.no_peak_hours/(self.increase_dir + self.decrease_dir)

class Path(object):

	def __init__(self,pathnum, startpost,endpost):
		"""
			构造一个一个方向的路，这个是一个元胞自动机进行模拟的单元
		"""
		self.pathnum = pathnum
		self.startpost = startpost
		self.endpost = endpost
		self.path_map = []# np.zeros(self.direction,self.endpost - self.startpost)
		self.car_dictory = {}
		self.mile_ratio = 1000
		self.cell_amount = self._set_cell_amount()
		self.recorder = {}
		count = 0

		while count < self.pathnum:
			self.path_map.append([0]*self.cell_amount)
			count = count + 1

	def add_car(self,car,car_id):
		success = False
		add_place = 0
		lanes = random.randint(0,self.pathnum - 1)
		while(not success):
			if add_place >= self.cell_amount:
				# 车辆爆表了，不加了！
				break
			# 这个位置没有车
			if self.path_map[lanes][add_place] == 0:
				# 需要确定前面的车的长度
				forward_car = self.find_nearest_car(1,1,lanes,add_place)
				if len(forward_car)==1:
					forward_car = forward_car[0]
					tail = forward_car.get_place() - forward_car.length + 1
					if tail <= add_place:
						# 这里还是被占用了，不能开车
						add_place = add_place + 1
						continue
				back_car = self.find_nearest_car(1,-1,lanes,add_place)
				if len(back_car)==1:
					back_car = back_car[0]
					head = back_car.get_place()
					if head >= add_place - car.length:
						# 这里会把别人占用了，不能放车
						add_place = add_place + 1
						continue
				# 更新地图
				self.path_map[lanes][add_place] = car_id
				# 更新车子坐标
				car.set_location(lanes,add_place)
				# 将车子加入该路段
				self.car_dictory[car_id]= car
				success = True
			else:
				add_place = add_place + 1


	def _set_cell_amount(self):
		return int((self.endpost - self.startpost) * self.mile_ratio)

	def update(self):
		"""
		1. 遍历目前存在于该路段的所有汽车；
		2. 对每辆汽车做变换车道操作
		3. 对每辆汽车做更新操作
		"""
		count = 0
		temp_path_map=[]
		while count < self.pathnum:
			temp_path_map.append([0]*self.cell_amount)
			count = count + 1
		output_cars = {}
		for car_id,car in self.car_dictory.items():
			logging.info("car_id is %s"%car_id)
			lanes = car.get_lanes()
			place = car.get_place()
			forward_cars = self.find_nearest_car(2,1,lanes,place)
			# back_cars = self.find_nearest_car(1,-1,car.get_lanes(),car.get_place())
			new_location = car.update_status(forward_cars)
			# 清空历史状态
			temp_path_map[lanes][place] = 0 
			# 如果新的location过大，则说明已经离开这个地方了
			if new_location[1] < self.cell_amount:
				# 记录新状态
				temp_path_map[new_location[0]][new_location[1]] = car_id
			else:
				output_cars[car_id] = car
		self.path_map = temp_path_map
		for key,value in output_cars.items():
			del self.car_dictory[key]
		self.update_recorder()
		return output_cars

	def update_recorder(self):
		count = 0
		while count < self.pathnum:
			if self.recorder.has_key(count):
				self.recorder[count].append(self.path_map[count])
			else:
				self.recorder[count] = [self.path_map[count]]
			count = count + 1

	def find_nearest_car(self,amount,direction,lanes,place):
		"""
			direction: +1 代表向前找 -1 代表向后找
			amount: 要查找的车的数目
		"""
		end = False
		step = direction
		temp_place = place + step
		car_list = []
		count = 0
		while not end:
			if temp_place >= self.cell_amount or temp_place < 0:
				break
			car_num = self.path_map[lanes][temp_place]
			if car_num != 0:
				#print "length of car list is %s "%len(car_list)
				#print "number is %s"%car_num
				#print "car_dictory is %s "%self.car_dictory
				car_list.append(self.car_dictory[car_num])
				count = count + 1
				if count == amount:
					break
			else:
				temp_place = temp_place + step
		return car_list


	def plot(self,line_number,count_max):
		count =1
		while(count <= count_max):
			x = []
			y = []
			for index, path_list in enumerate(self.recorder[line_number]):
				appear = False
				try:
					place = path_list.index(count)
					appear = True
					x.append(place)
					y.append(index)
				except Exception as e:
					if appear:
						# 车消失了
						break
			plt.plot(x,y,'k-')
			count = count + 1
		plt.title("time-space",fontsize=15)
		plt.xlabel("space")
		plt.ylabel("time", fontsize=15)
		plt.show()
