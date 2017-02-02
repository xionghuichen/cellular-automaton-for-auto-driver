#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.1.21
# Modified    :   2017.2.1
# Version     :   1.0
# structure.py
import logging
from functions import do_probability_test
from Global import MAX_PATH, CELL_RATIO, TIME_SLICE
"""
车的基类
"""
class BasicCar(object):
	
	def __init__(self, init_vel,car_info, lanes=MAX_PATH, place=0):
		self._velocity=init_vel # 当前行驶速度
		self.max_velocity=int(car_info['max_velocity']/3600*CELL_RATIO*TIME_SLICE)# 车辆的限制速度
		self.length=int(car_info['length']*CELL_RATIO)# 车辆长度
		self._location=[lanes,place]# 车辆当前的位置，在路段的多个车道内定义:[x,y]
		self.accelerate=1# 车辆的等效加速度
		self.slow_rate = car_info['slow_rate']
		self.slow_rate_low = 0.01
		self.slow_velocity = 1
		self.safe_distance = 0# car_info['safe_distance']
		self.slow_rate_high = 0.8
		self.turn_rate = 0.7


	@property
	def velocity(self):
		return self._velocity

	@velocity.setter
	def velocity(self,value):
		if value<0:
			raise Exception("velocity error velocity is %s"%value)
		self._velocity = value

	@property
	def location(self):
		return self._location

	@location.setter
	def location(self,value):
		"""
			设置车辆的位置
		"""
		if value[0] < 0 or value[1] < 0:
			raise Exception("location error lanes is %s, place is %s"%(value[0],value[1])) 
		self._location[0] = value[0]
		self._location[1] = value[1]

	@property
	def place(self):
		return self._location[1]

	@place.setter
	def place(self,place):
		if place<0:
			raise Exception("place error place is %s"%place)
		self._location[1] = place

	@property
	def lanes(self):
		"""
			返回该车辆现在所在的车道位置
		"""
		return self._location[0]

	@lanes.setter
	def lanes(self, value):
		if value<0:
			raise Exception("place error lanes is %s"%value)
		self._location[0] = value

	def __repr__(self):
		return self.car_info()

	def car_info(self):
		return "location is %s, velocity is %s, length is %s"%(self.location, self.velocity, self.length)

	def update_infomation(self, vn):
		"""
			设置新的坐标位置
		"""
		self.velocity = vn
		self.place = self.place + vn

	def calculate_distance(self, another_car):
		"""
			headway = 两辆车的坐标差- 前面的车的长度
		"""
		distance = abs(another_car.place - self.place)
		if self.place > another_car.place:
			length = self.length
		else:
			length = another_car.length
		if distance - length < 0:
			logging.info("[calculate distance], distance is %s, length is %s"%(distance,length))
			return 0
			# raise Exception("error in calculate distance, distance is %s, length is %s"%(distance,length))
		return distance - length

	def calculate_slow_rate(self,vn):
		"""
			获得随机慢化概率
		"""
		if vn == self.max_velocity :
			return self.slow_rate_low
		elif vn ==0:
			return self.slow_rate_high
		else:
			return self.slow_rate

	def do_slow(self,vn):
		return max(vn-self.slow_velocity,0)

	def change_lance(self, around_cars):	
		"""
			lance_amount:总的车道的数目
			has_token:已经被占据的格子
			around_cars: include 
				'l+':left_forward_car,
				'l-':left_back_car, 
				'r+':right_forward_car, 
				'r-':right_back_car
			根据左右最近车的位置情况做出车道变道决策
			b. 换车道思考过程：
				i. 三车道换道模型
					1) 如果右车道安全，且比当前车道车况好[车距更大]，就换右车道
					2) 右车道路况没有比当前路况好，那么
						a) 如果左车道安全
						b) 当前车道不满足行驶条件
						c) 左车道路况比当前路况好
						d) 满足以上所有条件，换左车道
					3) 做出最后的换道决策，前面只是做出思考，有Pignore的概率拒绝换道[模拟人的因素]
					4) 这部分私家车和自动驾驶汽车暂时没有思考出区别
				ii. 考虑鸣笛效应
					1) 当n号车后面的车满足以下条件的时候，对n号车鸣笛
						a) n号车无法正常速度行驶
						b) n号车无法换道
					2) 当n号车被鸣笛之后：
						a) 如果右车道安全，且比当前车道车况好，就换右车道
						b) 如果右车道不能换，那么
							i) 如果左车道安全
							ii) 左车道满足当前的行驶条件[速度满足当前的速度]
						c) 决定换左车道
					3) 上面只是做出思考，没有做出最终决策，有Pignore的概率拒绝换道[模拟人的因素]
					4) 换道环节结束之后进入单车道思考过程
		[change log]
		2017.2.2
		around_cars[‘r+’] 之前写成 r-，导致判断出错
		"""
		# 考虑右边车道
		logging.info("self: %s"%self)
		logging.info("around_cars: %s"%around_cars)
		if around_cars['+'] == []:
			logging.info("前面没有车")
			# 前面没有车，不需要转弯
			return 0
		turn = 0
		result1 = False
		result2 = False
		if around_cars['r']:
			result1 = False
			if around_cars['r-'] != []:
				if self.calculate_distance(around_cars['r-'][0]) > around_cars['r-'][0].max_velocity:
					result1 = True
				else:
					logging.info("right 右边的后面的车子距离自己太近了，%s"%self.calculate_distance(around_cars['r-'][0]))
			else:
				logging.info("右边没有车，result1 = true")
				result1 = True
			result2 = False
			if around_cars['r+'] != []:
				if self.calculate_distance(around_cars['r+'][0]) > self.calculate_distance(around_cars['+'][0]):
					result2 = True
				else:
					logging.info("right 右边的前面的车的距离太近了，车况不如当前车道，dr+ :%s, d+ : %s"%(self.calculate_distance(around_cars['r+'][0]),self.calculate_distance(around_cars['+'][0])))
			else:
				result2 = True
		else:
			logging.info("这辆车没有right右边车道")
		if result1 and result2:
			turn = -1

		# 考虑左边车道
		result1 = False
		result2 = False
		result3 = False
		if turn == 0 and around_cars['l']:
			result1 = False
			if around_cars['l-'] != []:
				if self.calculate_distance(around_cars['l-'][0]) > around_cars['l-'][0].max_velocity:
					result1 = True
				else:
					logging.info("left左边的后面的车子距离自己太近了，%s"%self.calculate_distance(around_cars['l-'][0]))
			else:
				logging.info("左边没有车，result1 = true")
				result1 = True
			result2 = False
			result3 = False
			if around_cars['l+'] != []:
				if self.calculate_distance(around_cars['+'][0]) < min(self.velocity+1,self.max_velocity) or self.velocity == 0:
					result2 =True
				else:
					logging.info("不满足前面车况不太好的条件，车子可以自由行驶，不需要转弯")
				if self.calculate_distance(around_cars['l+'][0]) > self.calculate_distance(around_cars['+'][0]):
					result3 = True
				else:
					logging.info("left 左边 前面的车况没有当前的车况好")
			else:
				result2 = True
		if result1 and result2 and result3:
			turn = 1

		if turn !=0:
			# 有几率满足条件也不转弯
			logging.info("决策 turn is: %s"%turn)
			if not do_probability_test(self.turn_rate):
				turn = 0
		return turn

	def update_status(self, around_cars,turn = 0):
		"""
			around_cars: include 
				forward_cars ：观察两辆
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
		# logging.info("velocity is %s"%self.velocity)
		# logging.info("forward car number is %s"%len(around_cars))
		# logging.info("location is :%s"%self.location)
		self.lanes = self.lanes+turn
		vn = min(self.velocity+self.accelerate, self.max_velocity)
		# 减速
		if len(around_cars) == 2:
			v_forward_imaginary = min(
				around_cars[0].max_velocity - self.safe_distance,
				max(around_cars[0].velocity - self.safe_distance,0),
				max(0,around_cars[0].calculate_distance(around_cars[1]) - self.safe_distance))
		elif len(around_cars) == 1:
			#这辆车前面只有一辆车，第三项消除
			v_forward_imaginary = min(
				max(around_cars[0].max_velocity - self.safe_distance,around_cars[0].length),
				max(around_cars[0].velocity - self.safe_distance,around_cars[0].length),
				999999)
			# logging.info("v forward imaginary is :%s"%v_forward_imaginary)
		if len(around_cars) != 0:
			# logging.info("distance is :%s"%self.calculate_distance(around_cars[0]))
			vn = min(vn,self.calculate_distance(around_cars[0])+v_forward_imaginary)
		# logging.info("vn before slow is %s"%vn)	
			# 这辆车前面没有车，不会受限制
		# 随机慢化
		# 计算当前随机漫画概率
		slow_rate = self.calculate_slow_rate(vn)
		if do_probability_test(slow_rate):
			# 进行随机慢化
			vn = self.do_slow(vn)
		# 更新速度
		# 返回更新后的坐标
		# logging.info("vn after slow is %s"%vn)	
		return (vn, [self.lanes, self.place + vn])


class NoAutoCar(BasicCar):
    def __init__(self, *argc, **argkw):
        super(NoAutoCar, self).__init__(*argc, **argkw)  

class AutoCar(BasicCar):
    def __init__(self, *argc, **argkw):
        super(AutoCar, self).__init__(*argc, **argkw)  
