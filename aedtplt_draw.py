import re
import numpy as np
import matplotlib.pyplot as plt

# 打开并读取 .aedtplt 文件
with open('data/Eface.aedtplt', 'r', encoding='utf-8') as file:
    content = file.read()

# 正则表达式匹配节点和场解数据
nodes_pattern = re.compile(r"Nodes\((.*?)\)", re.DOTALL)
elemsolution_pattern = re.compile(r"ElemSolution\((.*?)\)", re.DOTALL)
elements_pattern = re.compile(r"Elements\((.*?)\)", re.DOTALL)
minmaxlocation_pattern = re.compile(r"ElemSolutionMinMaxLocation\((.*?)\)", re.DOTALL)

nodes_match = nodes_pattern.search(content)
elemsolution_match = elemsolution_pattern.search(content)
elements_match = elements_pattern.search(content)
minmaxlocation_match = minmaxlocation_pattern.search(content)




if nodes_match and elemsolution_match:
    # 提取并处理节点数据
    nodes_data = nodes_match.group(1).split(',')
    print(len(nodes_data))
    nodes_data = np.array([float(node.strip()) for node in nodes_data]).reshape(-1, 3)  # 将节点坐标转换为 3D 数组
    
    elements_data = [int(item) for item in elements_match.group(1).split(',')]
    
    nodes_num = elements_data[0]
    elements_num = elements_data[1]
    element_size = (len(elements_data) - 2) / elements_num
    
    print("Elements Size", element_size)
    
    elements = np.array(elements_data[2:]).reshape(-1, int(element_size))
    
    print("Element Number", len(elements), elements[0])
    
    print("Max", max(elements_data))
    
    # 提取并处理场解数据
    elem_solution_data = elemsolution_match.group(1).split(',')
    elem_solution_data = np.array([float(solution.strip()) for solution in elem_solution_data])
    
    print("element", elem_solution_data[2], len(elem_solution_data), len(elem_solution_data) / elem_solution_data[2])
    
    element_solution = elem_solution_data[3:].reshape(-1, int(elem_solution_data[2]))
    
    print(len(element_solution), element_solution[0])
    
    x_data = []
    y_data = []
    field_values_list = [[] for i in range(19)]
    
    for element, element_result in zip(elements, element_solution):
        # print(element, element_result)
        polygon_points = [nodes_data[idx - 1] for idx in element[-6:]]
        
        # print(polygon_points)
        point_x = [point[0] for point in polygon_points]
        point_y = [point[1] for point in polygon_points]
        center_x = sum(point_x) / len(point_x)
        center_y = sum(point_y) / len(point_y)
        
        
        value = element_result[0]
        
        # print(center_x, center_y, value)
        
        x_data.append(center_x)
        y_data.append(center_y)
        
        for i in range(18): 
            field_values_list[i].append(element_result[i])

        field_values_list[18].append((element_result[0] **2 + element_result[1] **2 + element_result[2] **2) ** 0.5)

    

    # 检查 x, y 和 field_values 的长度
    print("Length of x_data:", len(x_data))
    print("Length of y_data:", len(y_data))
    # print("Length of field_values:", len(field_values))
    print("TOP 5 field value")
    print("element_number", len(elements_data))
    print("first")

    for i, field_values in enumerate(field_values_list):
        # 使用 Matplotlib 绘制场图
        plt.figure(figsize=(8, 6))
        plt.tricontourf(x_data, y_data, field_values, levels=14, cmap='RdYlBu_r')
        plt.colorbar(label='Field Strength')
        plt.title(f'Field Plot Visualization {i}')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True)
        plt.savefig(f"results/field_plot_{i}.png")


else:
    print("没有找到匹配的节点或场解数据")
