import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c, pi, epsilon_0

# 假设手机的工作频率为 2.4 GHz
frequency = 2.4e9  # Hz
wavelength = c / frequency  # 波长 (m)
k = 2 * np.pi / wavelength  # 波数
E0 = 1.0  # 假设天线的初始电场强度

# 天线坐标（假设天线在手机的四角）
antenna_positions = np.array([[0.05, 0.05, 0], 
                              [-0.05, 0.05, 0],
                              [0.05, -0.05, 0], 
                              [-0.05, -0.05, 0]])

# 球形物体的半径 (模拟人体)
sphere_radius = 0.2  # 0.2米，约为人体头部的大小
sphere_center = np.array([0, 0, 0.3])  # 球的中心离手机0.3米

# 生成球体表面点
phi = np.linspace(0, np.pi, 100)
theta = np.linspace(0, 2 * np.pi, 100)
phi, theta = np.meshgrid(phi, theta)

x_sphere = sphere_center[0] + sphere_radius * np.sin(phi) * np.cos(theta)
y_sphere = sphere_center[1] + sphere_radius * np.sin(phi) * np.sin(theta)
z_sphere = sphere_center[2] + sphere_radius * np.cos(phi)

# 计算天线辐射在球体表面各点的电场强度 (偶极子模型)
def electric_field(antenna_pos, point, k, E0):
    r = np.linalg.norm(point - antenna_pos)  # 距离
    E_r = E0 * np.exp(-1j * k * r) / r  # 假设自由空间中的电场随距离衰减
    return np.abs(E_r)  # 返回电场的绝对值

# 在球体表面计算总电场（所有天线的叠加）
E_total = np.zeros_like(x_sphere, dtype=np.complex128)
for antenna_pos in antenna_positions:
    for i in range(x_sphere.shape[0]):
        for j in range(x_sphere.shape[1]):
            point = np.array([x_sphere[i, j], y_sphere[i, j], z_sphere[i, j]])
            E_total[i, j] += electric_field(antenna_pos, point, k, E0)

# 可视化结果
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x_sphere, y_sphere, z_sphere, facecolors=plt.cm.viridis(np.abs(E_total) / np.max(np.abs(E_total))))
ax.set_title("天线辐射在球形人体附近的电场分布")
plt.show()
