import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt


from read3daedt import readaedt

with open('../data/E.aedtplt', 'r', encoding='utf-8') as file:
    content = file.read()
x_data, y_data, z_data, field_values_list, points = readaedt(content)

# 假设我们已有一些不规则分布的三维点和它们的数值
# 例如：
# 点的坐标
# points = np.array([
#     [1, 1, 2],
#     [3, 3, 1],
#     [5, 2, 3],
#     [2, 5, 4],
#     [6, 6, 2]
# ])

print(points[:5])

points = np.array(points)


x_min = np.min(points[:, 0])
x_max = np.max(points[:, 0])
y_min = np.min(points[:, 1])
y_max = np.max(points[:, 1])
z_min = np.min(points[:, 2])
z_max = np.max(points[:, 2])



print("Y, X, Z range:", y_max - y_min, x_max - x_min, z_max - z_min)

print("Y:", y_min, y_max)
print("X:", x_min, x_max)
print("Z:", z_min, z_max)


# 每个点对应的值
# values = np.array([10, 15, 20, 25, 30])

values = np.array(field_values_list[-1])


print("point number", len(points), "value number", len(values))


# 定义我们希望插值的规则网格范围
# 生成规则的网格坐标
# grid_x, grid_y, grid_z = np.mgrid[0:7:50j, 0:7:50j, 0:5:50j]


grid_x, grid_y, grid_z = np.mgrid[x_min:x_max:50j, y_min:y_max:50j, z_min:z_max:50j]

# 插值到规则网格
grid_values = griddata(points, values, (grid_x, grid_y, grid_z), method='linear')

print("grid_values shape", grid_values.shape)

# 可以选择可视化某个切片来查看插值结果
plt.imshow(grid_values[:, :, 25], extent=(x_min, x_max, y_min, y_max), origin='lower', cmap='viridis')
plt.colorbar(label='Interpolated values')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Interpolated slice at Z = midpoint')
plt.savefig('./3Dprocess/interpolation.png')
