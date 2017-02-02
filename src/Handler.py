#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.22
# Modified    :   2017.2.1
# Version     :   1.0
# Handler.py
import json
from Route import Route
import random
from functions import multi_probility_test, accumulator, do_probability_test
from Global import CARS_INFO, MAX_PATH, MAX_VELOCITY,CELL_RATIO,TIME_SLICE
from Car import NoAutoCar, AutoCar
import logging

class CellularHandler(object):

	def __init__(self,data, car_ratio):
		self.route_list = {}
		self.result_dict = {}
		self.car_acc_probility = accumulator(car_ratio)
		self._route_creator(data)
		self.car_id_count = 2
		# self.remain_rate = 1

	def _route_creator(self,data):
		"""
			构造线路列表
		"""
		for key,item in data.items():
			self.route_list[key] = Route(key,item)

	def _update_cars(self,output_cars):
		"""更新carlist的每个汽车的id
		"""
		new_car_dic = {}
		for key,item in output_cars.items():
			new_id = self.next_car_id()
			new_car_dic[new_id] = item
		return new_car_dic

	def next_car_id(self):
		"""
			新增的car的id
		"""

		new_id = self.car_id_count
		logging.info("new car id is :%s"%new_id)
		self.car_id_count = self.car_id_count+1
		return new_id

	def to_next_path(self,this_road,last_road,output_cars):
		"""
			车辆生产器，用来在道路的开头生产车辆
			需要使用numpy库模拟二项分布
				如果上一个道路段的 车辆个数比这个道路段的少，
					那么新增的车子数目按照二项分布进行生产车子，
					将上一个车道的数目按照留存的比例增加到目前的车道
					进行安排放置
				如果上一个车道的车辆个数比这个车道的多，
					那么这个车道本身不产生新的车子，
					上一个车道的车子按照缺少的比例流失

		"""
		car_dictory = {}
		# 把从上一个车道离开的车子挪到下一个车道
		# output_amount = len(output_cars)
		if last_road != 0:
			for key,value in output_cars.items():
				value.place = value.place - last_road.cell_amount
				car_dictory[key] = value
		# if last_road == 0:
		# 	# 第一个车道，不需要进行这个操作
		# 	bi_probality = this_road.get_Singleton_peak(0)
		# 	car_amount = multi_probility_test(bi_probality)
		# 	count = 0
		# 	# 本次随机实验计算得应该产生car_amount 量车子
		# 	# print "new car amount is :%s"%car_amount
		# 	while(count < car_amount):
		# 		# 产生对应类型的汽车
		# 		car_type = multi_probility_test(self.car_acc_probility)
		# 		single_car_info = CARS_INFO[car_type]
		# 		max_vel = single_car_info['max_velocity']
		# 		# [todo] 正太分布
		# 		init_vel = random.randint(2, max_vel/3)
		# 		# print "[car_creator]new car type is %s"%single_car_info['type']
		# 		if single_car_info['type']==0:
		# 			# 自动驾驶汽车
		# 			pass
		# 		else:
		# 			new_car = NoAutoCar(init_vel, single_car_info)
		# 			car_id = self.next_car_id()
		# 			car_dictory[car_id] = new_car

		# 			logging.info("new car id is :%s"%car_id)
		# 		count = count + 1
		# #[todo] 合并新老车
		# #[todo] 新车生成
		# elif last_road.car_volume() < this_road.car_volume():
		# 	# 将上一个路段的车子按照比例增加在该路段
		# 	output_amount = len(output_cars)
		# 	for key,value in output_cars.items():
		# 		value.place = value.place - last_road.cell_amount
		# 		car_dictory[key] = value
		# 	# 上一个道路段的车辆个数比这个道路段少，按比例产生新的车子
		# 	bi_probality = this_road.get_Singleton_peak(last_road.car_volume())
		# 	car_amount = multi_probility_test(bi_probality)
		# 	count = 0
		# 	while(count < car_amount):
		# 		# 产生对应类型的汽车

		# 		count =count + 1
		# else:
		# 	for key,value in output_cars.items():
		# 		value.set_place(value.get_place() - last_road.cell_amount)
		# 		car_dictory[key] = value
		return car_dictory



	def single_car_creator(self):
		"""用来产生一辆汽车
		
		"""
		car_type = multi_probility_test(self.car_acc_probility)
		single_car_info = CARS_INFO[car_type]
		# todo 这里的结构不是特别合理，因为在car的初始化的时候重新计算了一遍
		max_vel = int(single_car_info['max_velocity']/3600*CELL_RATIO*TIME_SLICE)
		init_vel = random.randint(0, max_vel/3)

		if single_car_info['type']==0:
			# 自动驾驶汽车
			new_car = AutoCar(init_vel, single_car_info)
			car_id = self.next_car_id()
		else:
			new_car = NoAutoCar(init_vel, single_car_info)
			car_id = self.next_car_id()
		return (car_id, new_car)

	def driver(self,route_id):
		"""
			元胞驱动器，用来启动所有程序流程
		"""
		count = 0 
		# initial vehicles：初始化的车子必须在一个最大速度以外，避免从上一轮出来的车子和他相撞
		for index, path in enumerate(self.route_list[route_id].path_list):
			amount = path.car_initial_amount
			count = 0 
			print "[driver] path index is %s, amount is %s"%(index,amount)
			while(count < amount):
				(car_id, new_car) = self.single_car_creator()
				init_lanes = path.random_path()
				init_place = random.randint(0,path.cell_amount)# new_car.velocity 
				new_car.location = [init_lanes, init_place]
				path.add_init_car(new_car, car_id)
				count = count + 1
		count = 0
		# 第一次迭代的时候没有上一辆车，所以用０
		last_path = 0
		output_cars = 0
		reocord_volume = []
		while count < 1800:
			#[todo] 将上个车道的output加入这个车道的input
			for index, path in enumerate(self.route_list[route_id].path_list):
				car_dictory = self.to_next_path(path,last_path,output_cars)
				output_cars = self.update(path,car_dictory)
				last_path = path
			# self.itertor(self.route_list[route_id])
			# 更新一遍之后，我们需要把最后一个路段结尾的ouput的车子加入第一个路段中，并且，我们需要更新他的car_id
			output_cars = self._update_cars(output_cars)
			# car_dictory = self.to_next_path(path,last_path,output_cars)
			# reocord_volume.append(len(output_cars))
			# for car_id,car in car_dictory.items():
			# 	# 重新初始化补充车辆
			# 	self.route_list[route_id].path_list[0].add_init_car(car, new_car_id)
			# 	# 开始下一轮迭代之前，需要吧last_path 清空
			# 	last_path = 0
			# 	output_cars = 0
			count = count + 1
			print "driver count is :%s"%count
		# logging.info(self.route_list[route_id].path_list[0].inc_path.recorder)
		print reocord_volume
		print "volume is %s"%sum(reocord_volume)
		self.route_list[route_id].plot(self.car_id_count)


	def itertor(self, route):
		"""
			迭代控制器,控制每次迭代进行的更新操作
			- 从头开始更新路段信息，
			- 将一个路段更新的结果传递给下一个路段
			- 进行道路车辆的道路选择
			- 记录本次更新的结果，用于最后绘图
			- 对下一个路段进行更新，
			- 一直到路段更新结束
		"""
		last_path = 0
		#[todo] 将上个车道的output加入这个车道的input
		output_cars = 0
		for index, path in enumerate(route.path_list):
			# [delete]
			# if index < len(route.path_list) - 1:
			# 	# 设置保留率，如果从不拥堵的路段过渡到拥堵的路段，则有保留率，否则，保留率为1
			# 	next_path = route.path_list[index+1]
			# 	rate = (path.car_volume()/next_path.car_volume())

			# 	if rate >1:
			# 		self.remain_rate =  (next_path.car_volume()/path.car_volume())
			# 	else:
			# 		self.remain_rate = rate
			# initial vehicles：初始化的车子必须在一个最大速度以外，避免从上一轮出来的车子和他相撞
			# add ouput vehicles.
			# update.
			
			# 将上个里程的车传递到下一个里程中
			#　[todo]如果没法增加到下一个里程中[被塞满了],则退回来上一个路段，目前是直接清除该辆车
			#　最后一个里程的车作为系统边界回到第一个里程中
			car_dictory = self.to_next_path(path,last_path,output_cars)
			output_cars = self.update(path,car_dictory)
			last_path = path
		# 更新一遍之后，我们需要把最后一个路段结尾的ouput的车子加入第一个路段中，并且，我们需要更新他的car_id
		output_cars = self._update_cars(output_cars)
		car_dictory = self.to_next_path(route.path_list[0],last_path,output_cars)
		output_cars = self.update(route.path_list[0],car_dictory)

	def update(self,path, car_dictory):
		"""
			操作一个道路路段的更新
			1. 按照概率分布和上一个路段对本路段的影响创造汽车
			2. 对每辆汽车进行元胞迭代操作
				- 变道判断[自动车解决冲突]
				- 前进更新
			3. 将更新结果更新到地图中
			4. 返回更新结果
		"""
		logging.info("[handler.update]update car_dictory is :%s"%car_dictory)
		for car_id,car in car_dictory.items():
			# car.change_lanes()
			success = path.add_car(car,car_id)
			if not success:
				# 添加失败，作为新生成的车子进行重新初始化
				new_car_id = self.next_car_id()
				path.add_init_car(car, new_car_id)

		output_cars = path.update()
		# logging.info("completed update:%s"%path.recorder[MAX_PATH - 1][-1])
		return output_cars

	def path_log_recorder(self,path):
		"""
			记录这个过程的每次状态信息，用于绘图
		"""

	def get_single_lines_cars(self,car):
		location = car.get_place()
		lanes = car.get_lanes()