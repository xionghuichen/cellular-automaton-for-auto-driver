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
from Global import CARS_INFO, MAX_PATH, MAX_VELOCITY,CELL_RATIO,TIME_SLICE, TIMES
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

		change log:
		2017.2.3:
			1. 增加路段之间的地图信息交互
				if last_path != 0:
					last_path.update_next_path_info(path)
			2. 在这个路段的车辆
		2017.2.4：
			1. 把 last_path = 0 放到了 while times的循环体里面，
				使得每次迭代的初始状态的last_path都是空的，
				避免了最后一个里程的“下一个里程”信息被污染
		"""
		count = 0 
		# initial vehicles：
		last_path = 0
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
			# 初始化完成，将这个里程路段的前面的车辆信息传递给上一个车道
			if last_path != 0:
				last_path.update_next_path_info(path)
			last_path = path
		count = 0
		# 第一次迭代的时候没有上一辆车，所以用０
		reocord_volume = []
		reocord_velocity = []
		last_path = 0
		output_cars = 0
		while count < TIMES:
			for index, path in enumerate(self.route_list[route_id].path_list):
				car_dictory = self.to_next_path(path,last_path,output_cars)
				output_cars = self.update(path,car_dictory)
				if index != 0:
					# 将上个车道的output加入这个车道的input
					last_path.update_next_path_info(path)
				last_path = path

			# self.itertor(self.route_list[route_id])
			# 更新一遍之后，我们需要把最后一个路段结尾的ouput的车子加入第一个路段中，并且，我们需要更新他的car_id
			output_cars = self._update_cars(output_cars)
			reocord_volume.append(len(output_cars))
			if len(output_cars)>0:
				reocord_velocity.extend([x.velocity*1.0 for key,x in output_cars.items() if x.velocity > 0])
			# 加入这段代码，从头进入
			# car_dictory = self.to_next_path(path,last_path,output_cars)
			# for car_id,car in car_dictory.items():
			# 	# 重新初始化补充车辆
			# 	new_car_id = self.next_car_id()
			# 	self.route_list[route_id].path_list[0].add_init_car(car, new_car_id)
			# 	# 开始下一轮迭代之前，需要吧last_path 清空
			# 	last_path = 0
			# 	output_cars = 0
			count = count + 1
			print "driver count is :%s"%count
		# logging.info(self.route_list[route_id].path_list[0].inc_path.recorder)
		print reocord_volume
		avg_vol =sum(reocord_volume) * 3600 / TIMES
		avg_vel = sum(reocord_velocity)*1.0/len(reocord_velocity)*3.6
		print "volume is %s"%avg_vol
		print "velocity is %s , %s"%(avg_vel, reocord_velocity)
		return (avg_vol, avg_vel)
	def plot_single_path(self,route_id):
		self.route_list[route_id].plot(self.car_id_count)

	def plot_all_path(self,route_id):
		self.route_list[route_id].plot_for_multi_path(self.car_id_count)

	def plot_path_map(self,route_id,path_id):
		self.route_list[route_id].path_list[path_id].plot_map()
		
	def update(self,path, car_dictory):
		"""
			操作一个道路路段的更新
			1. 按照概率分布和上一个路段对本路段的影响创造汽车
			2. 对每辆汽车进行元胞迭代操作
				- 变道判断[自动车解决冲突]
				- 前进更新
			3. 将更新结果更新到地图中
			4. 返回更新结果
		change log
		2017.2.3:
			1. [todo]在进行add_car的操作之前，要做一个操作，使这辆车概率丢失
			2. 每次是先更新，再将上一个里程过来的车加进来，而不是相反
		"""
		logging.info("[handler.update]update car_dictory is :%s"%car_dictory)
		output_cars = path.update(self.next_car_id)
		for car_id,car in car_dictory.items():
			# car.change_lanes()
			success = path.add_car(car,car_id)
			if not success:
				# 添加失败，作为新生成的车子进行重新初始化
				new_car_id = self.next_car_id()
				logging.info("failed car %s"%car)
				init_lanes = path.random_path()
				init_place = random.randint(0,path.cell_amount)# new_car.velocity 
				car.location = [init_lanes, init_place]
				path.add_init_car(car, new_car_id)
		# logging.info("completed update:%s"%path.recorder[MAX_PATH - 1][-1])
		return output_cars

	def path_log_recorder(self,path):
		"""
			记录这个过程的每次状态信息，用于绘图
		"""

	def get_single_lines_cars(self,car):
		location = car.get_place()
		lanes = car.get_lanes()

