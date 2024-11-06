import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# 设置仿真参数
resolution = 20  # 每单位长度的网格点数量 (增加这个值可以提高精度，但计算时间也会增加)

# 定义头部尺寸 (球形模型) 和介质属性
head_radius = 0.2  # 头部半径 (m)
head_center = mp.Vector3(0, 0, 0)  # 头部中心位置

# 定义头部材料 (可以根据不同组织定义多个介质)
brain = mp.Medium(epsilon=50, sigma=0.001)  # 假设脑组织的介电常数和导电率

# 创建仿真空间和材料
cell = mp.Vector3(1, 1, 1)  # 仿真空间的大小 (m)
geometry = [mp.Sphere(center=head_center, radius=head_radius, material=brain)]

# 定义天线位置和波源 (假设工作频率为2.4 GHz)
frequency = 2.4e9  # Hz
wavelength = mp.c_0 / frequency
sources = [mp.Source(mp.ContinuousSource(frequency=frequency),
                     component=mp.Ez,  # 假设电场方向为z轴
                     center=mp.Vector3(0.3, 0.3, 0),  # 天线位置
                     size=mp.Vector3(0, 0, 0))]

# 设置仿真边界条件 (吸收边界，避免反射干扰)
pml_layers = [mp.PML(0.1)]

# 创建仿真对象
sim = mp.Simulation(cell_size=cell,
                    geometry=geometry,
                    sources=sources,
                    resolution=resolution,
                    boundary_layers=pml_layers)

# 运行仿真，记录电场数据
sim.run(until=200)

# 提取电场数据
eps_data = sim.get_array(center=head_center, size=mp.Vector3(0.4, 0.4, 0.4), component=mp.Ez)

# 可视化结果 (二维切片)
plt.imshow(np.abs(eps_data.T), interpolation='spline36', cmap='RdBu')
plt.colorbar()
plt.title("头部内部的电场分布")
plt.show()
