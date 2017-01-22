## 项目介绍
## 数据结构
"""
车的基类
"""
class BasicCar
	velocity:当前行驶速度
	length:长度
	location:[x,y]
	accelerate:加速度


	def update_status():
		"""
		"""

	def change_lanes(left_cars, right_cars):	
		"""
			根据左右最近车的位置情况做出车道变道决策
			1. 首先考虑右车道
				- 右车道的
		"""

	
"""
自动驾驶汽车类
"""
class AutoCar


"""
非自动驾驶汽车类
"""
class NoAutoCar
	type:类型


"""
路线类，包含了一个公路的诸多段落
"""
class Route

"""
公路段类，包含了两个方向的公路
"""
class Road
	road_length
	increase_dir
	decrease_dir


"""
每一个方向的路为一个path，一个path有若干的车道
"""
class Path


"""
每个车道的单元
"""
class PathUnit


"""
自动机驱动器
"""
class CellularHandler
	car_amount
	auto-car_rate

	def car_creator():
		"""
		车辆生产器，用来在道路的开头生产车辆
		需要使用numpy库模拟二项分布
		"""

	def itertor():
		"""
			迭代控制器
		"""
	def change_lanes_handler():
		"""
			处理每辆车的变道逻辑
		"""
	def update_status_handler():
		"""
			更新每辆车的速度
		"""
	
	def log_recorder():
		"""
			记录这个过程的每次状态信息，用于绘图
		"""




## 项目结构
## 主要函数的代码逻辑