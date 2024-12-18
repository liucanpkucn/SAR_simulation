import pandas as pd
import matplotlib.pyplot as plt


slice_data = pd.read_csv('temp_data/slice_data.csv', header=None)

plt.imshow(slice_data, cmap='viridis')  # 选择颜色映射
plt.colorbar()  # 可选，添加颜色条

# 保存为图像文件
plt.savefig('slice_data_image.png', dpi=300)  # 调整 dpi 以提高分辨率
plt.close()