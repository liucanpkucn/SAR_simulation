import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

import h5py

from read3daedt import readaedt
import pandas as pd

import time

with open('../data/loop/LOOP E MOVE FEED=4mm_my=32mm.aedtplt', 'r', encoding='utf-8') as file:
    content = file.read()
    
x_data, y_data, z_data, field_values_list, points = readaedt(content)

# 假设我们已有一些不规则分布的三维点和它们的数值

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


Y_grid = 512
X_grid = (x_max - x_min) * Y_grid / (y_max - y_min)
Z_grid = (z_max - z_min) * Y_grid / (y_max - y_min)


# 每个点对应的值
values = np.array([10, 15, 20, 25, 30])


values = np.array(field_values_list[-1])
print("point number", len(points), "value number", len(values))

# 定义我们希望插值的规则网格范围
# 生成规则的网格坐标
# grid_x, grid_y, grid_z = np.mgrid[0:7:50j, 0:7:50j, 0:5:50j]
grid_x, grid_y, grid_z = np.mgrid[x_min:x_max:X_grid * 1j, y_min:y_max:Y_grid * 1j, z_min:z_max:Z_grid * 1j]

import time
begin_time = time.time()
# 插值到规则网格
grid_values = griddata(points, values, (grid_x, grid_y, grid_z), method='linear')

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')

# # 将三维网格和插值数据展开
# x = grid_x.flatten()
# y = grid_y.flatten()
# z = grid_z.flatten()
# values = grid_values.flatten()

# # 绘制散点图
# sc = ax.scatter(x, y, z, c=values, cmap='viridis', marker='o', s=2)
# plt.colorbar(sc, ax=ax, label='Values')
# ax.set_title("3D Interpolated Data")
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_zlabel("Z")
# plt.show()
    




end_time = time.time()

print("Cost time", end_time - begin_time)
# import pyvista as pv

# import pyvista as pv

# # 创建数据网格
# grid = pv.StructuredGrid(grid_x, grid_y, grid_z)
# grid["Values"] = grid_values.flatten(order="F")  # 将值赋予网格

# # 创建体渲染
# plotter = pv.Plotter()
# plotter.add_volume(grid, scalars="Values", cmap="viridis", opacity="linear")
# plotter.show()



print("grid_values shape", grid_values.shape)

chosen_index = int((Z_grid - 1) // 2)
print("chosen_index", chosen_index)

slice_data = grid_values[:, :, chosen_index]
print("slice_data shape", slice_data.shape)

# 存储到 HDF5 文件
with h5py.File('grid_data.h5', 'w') as f:
    # 存储 grid_values
    f.create_dataset('grid_values', data=slice_data)

    # 如果需要，存储网格的坐标信息
    f.create_dataset('grid_x', data=grid_x)
    f.create_dataset('grid_y', data=grid_y)

print("数据已存储到 grid_data.h5 文件")

# 将 slice_data 转换为 DataFrame
df = pd.DataFrame(slice_data)

# 保存为 CSV 文件
df.to_csv('temp_data/slice_data.csv', index=False)

# 设置颜色映射的取值范围
vmin = np.min(slice_data)  # 或者你可以手动设置
vmax = np.max(slice_data)  # 或者你可以手动设置


for i in range(int(Z_grid)):
    slice_data = grid_values[:, :, i]
    
    # 过滤掉 NaN 再计算最大最小值
    slice_data = grid_values[:, :, i]

    # 过滤掉 NaN 值
    filtered_slice_data = slice_data[~np.isnan(slice_data)]
        
    image_file = f'./temp_data/interpolation2_{i}.png'
    # print(np.min(slice_data), np.max(slice_data), image_file)
    
    if filtered_slice_data.size > 0:
        min_value = np.min(filtered_slice_data)
        max_value = np.max(filtered_slice_data)
        print(min_value, max_value, image_file)
    else:
        print("当前切片数据全部为 NaN！", image_file)

    # 可以选择可视化某个切片来查看插值结果
    plt.imshow(slice_data, extent=(x_min, x_max, y_min, y_max), origin='lower', cmap='viridis')
    plt.colorbar(label='Interpolated values')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Interpolated slice at Z = {i}')
    plt.savefig(image_file)
    plt.close()
