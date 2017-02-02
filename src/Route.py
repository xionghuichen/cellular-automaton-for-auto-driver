#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.2.1
# Version     :   1.0
# Route.py

"""
路线类，包含了一个公路的诸多段落
"""
import copy
import numpy as np
import random
import json
import logging
from matplotlib import pyplot as plt

from functions import binomial_creator, do_probability_test
from Global import MAX_PATH, CARS_INFO, TIME_SLICE, CELL_RATIO
from Car import NoAutoCar
class Route(object):
	def __init__(self,route_id,resource_item_list):
		"""
		构造道路路段
		"""
		self.route_id = route_id# 该路线的id
		self.route_amount = len(resource_item_list)# 改路线拥有的道路的个数 
		self.path_list =[]# 构造每一个道路路段的数据结构
		for value in resource_item_list:
			self.path_list.append(Path(value))

	def plot(self,count_max,direction='up'):
		if direction =='up':
			offset = MAX_PATH - 1
			line_number = offset
			while(line_number < MAX_PATH):
				# plt.subplot(3,1,line_number - offset + 1)
				# plt.subplot(5,1,1+line_number)
				count =2
				while(count <= count_max):
					x = []
					y = []
					last_cell_amount = 0
					appear = False
					disappear = False
					for path_num, path in enumerate(self.path_list):
						for index, path_list in enumerate(path.recorder[line_number]):
							if count == 3 and line_number == 1 and path_num == 1:
								logging.info("[route.plot] self.recorder[line_number]:%s"%path.recorder[line_number])
							try:
								place = path_list.index(count)
								appear = True
								x.append(place+last_cell_amount)
								y.append(index)
							except Exception as e:
								if appear:
									# 车消失了
									disappear = True
									plt.plot(x,y,'k-')
									x = []
									y = []
									break
						last_cell_amount = last_cell_amount +  path.cell_amount
						# print "last cell amount : %s"%last_cell_amount
					plt.plot(x,y,'k-')
					count = count + 1
					plt.title("time-space in path %s"%line_number,fontsize=15)
					plt.xlabel("space")
					plt.ylabel("time", fontsize=15)
					plt.axis([0,last_cell_amount,0,len(path.recorder[line_number])])
				line_number = line_number + 1
			plt.show()

		# if direction =='up':
		# 	
		# 	line_number = 0
		# 	while line_number < MAX_PATH:
		# 		print "line number is %s"%line_number
		# 		pltb.subplot(5,1,1+line_numer)
		# 		count =2
		# 		while(count <= count_max):
		# 			x = []
		# 			y = []
		# 			last_cell_amount = 0
		# 			for path_num, road in enumerate(self.path_list):
		# 				path = road.inc_path
		# 				for index, path_list in enumerate(path.recorder[4]):
		# 					# if count == 3:
		# 						# logging.info("[route.plot] self.recorder[line_number]:%s"%self.recorder[line_number])
		# 					appear = False
		# 					try:
		# 						place = path_list.index(count)
		# 						appear = True
		# 						x.append(place+last_cell_amount)
		# 						y.append(index)
		# 					except Exception as e:
		# 						if appear:
		# 							# 车消失了
		# 							break
		# 				last_cell_amount = last_cell_amount +  path.cell_amount
		# 				# print "last cell amount : %s"%last_cell_amount
		# 			plt.plot(x,y,'k-')
		# 			count = count + 1
		# 		line_number = line_number + 1
		# 	#plt.title("time-space in single path",fontsize=15)
		# 	#plt.xlabel("space")
		# 	#plt.ylabel("time", fontsize=15)
		# 	plt.show()

"""
公路段类，包含了两个方向的公路,对应excel的一调数据
"""
# class Road(object):
# 	def __init__(self,):
# 		"""
# 			构造一个路段
# 		"""
# 		self.startpost = resource_item['startpost']# A marker on the road that measures distance in miles from either the start of the route or a state boundary.
# 		self.endpost = resource_item['endpost']# The average number of cars per day driving on the road.
# 		self.traffic_amount = resource_item['density']# average daily traffic
# 		self.path_number = resource_item['path_number']
# 		self.peak_hours=2
# 		self.no_peak_hours = 18
# 		self.peak_ratio = 0.08
# 		self.no_peak_ratio = 0.8
# 		self.time_slice = TIME_SLICE
# 		# self.no_peak_amount_per_hours = self._no_peak_amount_per_hours()
# 		# 累加的二项分布概率
# 		self.acc_bi_peak = []

# 		# self.inc_path=Path(self.increase_dir, self.startpost, self.endpost)
# 		# self.dec_path=Path(self.decrease_dir, self.startpost, self.endpost)

# 	def get_Singleton_peak(self,last_amount,direction='up'):
# 		if self.acc_bi_peak== []:
# 			self.peak_amount_per_hours = self._peak_amount_per_hours(last_amount)
# 			probability_of_single_car = (self.peak_amount_per_hours/3600*self.time_slice)/(3600*self.time_slice)
# 			if direction == 'up':
# 				probability_of_single_car = probability_of_single_car * self.increase_dir
# 				amount_per_hours = self.peak_amount_per_hours* self.increase_dir
# 			else:
# 				probability_of_single_car = probability_of_single_car * self.decrease_dir
# 				amount_per_hours = self.peak_amount_per_hours* self.decrease_dir
# 			self.acc_bi_peak = binomial_creator(amount_per_hours,probability_of_single_car)
# 		return self.acc_bi_peak

# 	def get_Singleton_no_peak(self,last_amount,direction='up'):
# 		if self.acc_bi_no_peak== []:
# 			self.peak_amount_per_hours = self._peak_amount_per_hours()
# 			probability_of_single_car = (self.peak_amount_per_hours/3600*self.time_slice)/(3600*self.time_slice)
# 			if direction == 'up':
# 				probability_of_single_car = probability_of_single_car * self.increase_dir
# 				amount_per_hours = self.peak_amount_per_hours* self.increase_dir
# 			else:
# 				probability_of_single_car = probability_of_single_car * self.decrease_dir
# 				amount_per_hours = self.peak_amount_per_hours* self.decrease_dir
# 			self.acc_bi_no_peak = binomial_creator(amount_per_hours, probability_of_single_car)
# 		return self.acc_bi_no_peak
	
# 	def _peak_amount_per_hours(self, last_amount):
# 		return ( self.car_volume() - last_amount )* self.peak_ratio / self.peak_hours

# 	def _no_peak_amount_per_hours(self, last_amount):
# 		return (self.car_volume() - last_amount) * self.no_peak_ratio / self.no_peak_hours/(self.increase_dir + self.decrease_dir)

# 	def car_volume(self):
# 		return self.traffic_amount /(self.increase_dir + self.decrease_dir)


		
"""
	构造一个一个方向的路，这个是一个元胞自动机进行模拟的单元
"""
class Path(object):
	def __init__(self,resource_item):
		self.path_num = resource_item['path_number']
		self.startpost = resource_item['startpost']
		self.endpost = resource_item['endpost']
		self.density = resource_item['density'] 
		self.path_map = []# np.zeros(self.direction,self.endpost - self.startpost)
		self.car_dictory = {}
		self.cell_amount = self._set_cell_amount()
		self.recorder = {}
		self.volume = []
		self.car_initial_amount = int((self.endpost - self.startpost)*self.density * self.path_num)
		count = 0
		# 创建虚拟车辆，即障碍物
		self.car_dictory[1] = NoAutoCar(0, CARS_INFO[1])
		logging.info("[PATH] %s"%self.path_num)
		print "cell amount is %s"%self.cell_amount
		while count < MAX_PATH:
			if count >= MAX_PATH - self.path_num:
				self.path_map.append([0]*self.cell_amount)
			else:
				# 使用虚拟车辆1号车占位
				self.path_map.append([1]*self.cell_amount)
			#[todo]
			count = count + 1

	def random_path(self):
		"""随机产生一个对于当前路段合法的车道number

		"""
		return random.randint(MAX_PATH - self.path_num, MAX_PATH - 1)

	def add_init_car(self,car,car_id):
		"""将初始化的车辆加入道路
		"""
		success = False
		add_place = car.place
		lanes = MAX_PATH - 1
		start_place = add_place # MAX_VELOCITY + 1
		zero_flag = False
		while True:
			try:
				# 从最大速度+1 开始找第一个值为0的下标
				add_place = self.path_map[lanes][start_place:].index(0)
				# 上面那个步骤没有出错，说明查找0号成功了
				add_place = add_place +start_place
				if self.is_safe_place(lanes,add_place, car.length,car_id):
					# 这个位置前后是安全的
					logging.info("[add_init_Car] add id:%s, into lanes %s, place %s"%(car_id, lanes, add_place))
					car.location = [lanes,add_place]
					self.add_car_info(car_id,car)
					success = True
					break
			except Exception as e:
				# 前面的车道没有下标为0的点了，换车道
				lanes = lanes - 1
				start_place = 0
				logging.info("[add_init_car] change lanes to %s"%lanes)
				if lanes < MAX_PATH - self.path_num:
					logging.info("[add_init_car] invalid lanes")
					break
				else:
					logging.info("[add_init_car] valid lanes")
					continue
			# 循环走到这里还没结束，说明找到了下表为0的点，但是这个点不安全，我们需要继续往前找
			start_place = add_place + 1
			if start_place >= self.cell_amount:
				# 已经到达边界了
				if not zero_flag:
					# 这次循环不是从头开始的
					zero_flag =True
					start_place = 0
				else:
					lanes = lanes - 1
					start_place = 0
					logging.info("[add_init_car] arrived boundary, change lanes to %s"%lanes)

	def add_car_info(self,car_id,car):
		"""将车辆信息加入地图和车辆字典

		Args:
			car_id:车辆id
			car车辆对象
		"""
		self.path_map[car.lanes][car.place] = car_id
		self.car_dictory[car_id]= car

	def is_safe_place(self,lanes,add_place,length,self_car_id):
		# 需要确定前面的车的长度
		forward_car = self.find_nearest_car(1,1,lanes,add_place,self_car_id)
		if len(forward_car)==1:
			# 前面有一辆车
			forward_car = forward_car[0]
			tail = forward_car.place - forward_car.length + 1
			if tail <= add_place:
				# 这里还是被占用了，不能开车
				# add_place = add_place + 1
				# continue
				return False
		back_car = self.find_nearest_car(1,-1,lanes,add_place,self_car_id)
		if len(back_car)==1:
			# 后面有车
			back_car = back_car[0]
			head = back_car.place
			if head >= add_place - length:
				# 这里会把别人占用了，不能放车
				# add_place = add_place + 1
				# continue
				return False
		return True
		# 更新地图
		self.path_map[lanes][add_place] = car_id
		# 更新车子坐标
		car.location = [lanes,add_place]
		# 将车子加入该路段
		self.car_dictory[car_id]= car
		success = True

	def add_car(self,car,car_id):
		"""上一个里程的车子加入这个里程中
		"""
		success = False
		add_place = car.place
		lanes = car.lanes
		while True:
			# 从该车本来应该达到的位置为起始点递减查找车辆，要求坐标位置为空。并且坐标是安全坐标
			if self.path_map[lanes][add_place] == 0 and self.is_safe_place(lanes,add_place,car.length,car_id):
				# 这个位置前后是安全的
				logging.info("[add_Car] add id:%s, into lanes %s, place %s"%(car_id, lanes, add_place))
				car.location = [lanes,add_place]
				self.add_car_info(car_id,car)
				success = True
				# 查找完毕
				break
			else:
				# 非空或者虽然是空的，但是不安全，需要把place = place -1继续搜索
				add_place = add_place - 1
				if add_place <=0:
					# 已经低到头了
					# [todo] 应该在左右车道重新选择，这里直接舍弃这辆车
					logging.info("[add_car] add_place less than 0")

					break
		return success

	def _set_cell_amount(self):
		return int((self.endpost - self.startpost) * CELL_RATIO)

	def update(self):
		"""
		1. 遍历目前存在于该路段的所有汽车；
		2. 对每辆汽车做变换车道操作
		3. 对每辆汽车做更新操作
		---
		change log:
		2017.1.2
			1. 寻找自己之前的车道的方法，没有考虑到别的车道的自己的横向坐标位置的车子，修复这个bug
		"""
		count = 0
		clear_list = []
		change_map = []
		has_token = []
		output_cars = {}
		change_lance_list = []
		for car_id,car in self.car_dictory.items():	
			if car_id == 1:
				# 一号车不用更新
				continue
			logging.info("car_id is %s"%car_id)
			lanes = car.lanes
			place = car.place
			# [增加弃车规则]
			# if not do_probability_tes):
			# 	# 判定为该车在该过程中从其他道路离开了
			# 	# 清空该车在地图的状态
			# 	# print "==in do probability test"
			# 	# print "lanes: %s"%lanes
			# 	# print "id : %s"%car_id
			# 	# print "place: %s"%place
			# 	change_map.append([lanes,place,0])
			# 	clear_list.append(car_id) 
			# 	continue

			# back_cars = self.find_nearest_car(1,-1,car.lanes,car.place)

			around_cars = {'r':False,'l':False}
			# 获得左右两边的车子
			if lanes - 1 >= MAX_PATH - self.path_num:
				around_cars['r'] = True
				around_cars['r+']=self.find_nearest_car(1,1,lanes - 1,place,car_id)
				around_cars['r-']=self.find_nearest_car(1,-1,lanes - 1,place,car_id)
			if lanes + 1 < MAX_PATH:
				around_cars['l'] = True
				around_cars['l+'] = self.find_nearest_car(1,1,lanes + 1,place,car_id)
				around_cars['l-'] = self.find_nearest_car(1,-1,lanes + 1,place,car_id)
			around_cars['+'] = self.find_nearest_car(1,1,lanes,place,car_id)
			turn = car.change_lance(around_cars)
			if turn != 0 :
				logging.info("[update] start turning %s"%turn)
				logging.info("[update] has_token %s"%has_token)
				logging.info("[update] map:\n %s"%self.path_map)
				logging.info("[update.car] :id:%s, info: %s"%(car_id,car))

			forward_cars = self.find_nearest_car(2,1,lanes + turn,place,car_id)
			(vn, new_location) = car.update_status(forward_cars,turn)
			if not self.is_road_free(has_token, new_location):
				# 如果位置已经被占据，重新更新状态
				(vn, new_location) = car.update_status(forward_cars,-turn)
			else:
				if turn != 0:
					has_token.append(new_location)
					change_lance_list.append(car_id)
			# 清空历史状态
			change_map.append([copy.deepcopy(lanes),copy.deepcopy(place),0,vn])
			# 如果新的location过大，则说明已经离开这个地方了
			if new_location[1] < self.cell_amount:
				# 记录新状态
				change_map.append([new_location[0],new_location[1],car_id,vn])

			else:
				# 需要把新的location记录下来，以便做里程迁移的时候使用
				car.location = new_location
				output_cars[car_id] = car

		for key,value in output_cars.items():
			del self.car_dictory[key]
		for item in clear_list:
			# 清空本轮被随机清除的车辆
			del self.car_dictory[item]
		for item in change_map:

			self.path_map[item[0]][item[1]] = item[2]
			# 不用于清空，而是更新这个车子的信息
			if item[2] != 0:
				# print "[update.change_map], item[0] %s"%item[0]
				# print "[update.change_map], item[1] %s"%item[1]
				# print "[update.change_map], item[2] %s"%item[2]
				# print "[update.change_map], item[3] %s"%item[3]
				# print "[update.change_map], length path_map[item[0]]: %s"%len(self.path_map[item[0]])
				# print "[update.change_map],self.cell_amount: %s"%self.cell_amount
				car = self.car_dictory[item[2]]
				car.update_infomation(item[3])
		self.update_recorder(output_cars)
		return output_cars

	def is_road_free(self,has_token, location):
		road_is_free = False
		try:
			has_token.index(location)
		except Exception as e:
			road_is_free = True
		return road_is_free

	def update_recorder(self,output_cars):
		count = 0# int(MAX_PATH - self.path_num)
		# print "[update recorder] count : %s"%count 
		# if self.recorder.has_key(MAX_PATH-1):
		# 	logging.info("[update recorder] before self.recorder[MAX_PATH-1]: %s"%self.recorder[MAX_PATH-1])
		self.volume.append(len(output_cars))
		while count < MAX_PATH:
			if self.recorder.has_key(count):
				self.recorder[count].append(copy.deepcopy(self.path_map[count] ))
			else:
				# print "[update recorder] self.path_map[count] : %s"%self.path_map[count]
				self.recorder[count] = [copy.deepcopy(self.path_map[count] )]
			count = count + 1
		# logging.info("[update recorder]  self.recorder[MAX_PATH-1]: %s"%self.recorder[MAX_PATH-1])

	def find_nearest_car(self,amount,direction,lanes,place,self_car_id):
		"""
			direction: +1 代表向前找 -1 代表向后找
			amount: 要查找的车的数目

		change log:
		2017.1.2
			1. 寻找自己之前的车道的方法，没有考虑到别的车道的自己的横向坐标位置的车子，修复这个bug：
				增加self_car_id 参数，同时修改了 is_safe_place 的参数列表，也是增加了self_Car_id 参数
		"""
		end = False
		step = direction	
		temp_place = place
		car_list = []
		count = 0
		while not end:
			if temp_place >= self.cell_amount or temp_place < 0:
				# 坐标已经走到头了
				break
			car_num = self.path_map[lanes][temp_place]
			if car_num != 0:
				# 发现新的车辆
				#print "length of car list is %s "%len(car_list)
				#print "number is %s"%car_num
				#print "car_dictory is %s "%self.car_dictory
				if car_num == self_car_id:
					temp_place = temp_place + step
					continue
				car_list.append(self.car_dictory[car_num])
				count = count + 1
				if count == amount:
					break
			# 不管有没有新的发现，都需要让坐标加上step
			temp_place = temp_place + step
		return car_list


	def plot(self,line_number,count_max,path_num):
		count =2
		plt.figure(path_num)
		while(count <= count_max):
			x = []
			y = []
			for index, path_list in enumerate(self.recorder[line_number]):
				# if count == 3:
					# logging.info("[route.plot] self.recorder[line_number]:%s"%self.recorder[line_number])
				
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
		plt.title("time-space in single path",fontsize=15)
		plt.xlabel("space")
		plt.ylabel("time", fontsize=15)
		plt.show()
