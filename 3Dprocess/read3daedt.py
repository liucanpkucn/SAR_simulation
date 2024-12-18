import re
import numpy as np
import pandas as pd

def readaedt(content):
    # 正则表达式匹配节点和场解数据
    nodes_pattern = re.compile(r"Nodes\((.*?)\)", re.DOTALL)
    elemsolution_pattern = re.compile(r"ElemSolution\((.*?)\)", re.DOTALL)
    elements_pattern = re.compile(r"Elements\((.*?)\)", re.DOTALL)
    minmaxlocation_pattern = re.compile(r"ElemSolutionMinMaxLocation\((.*?)\)", re.DOTALL)

    nodes_match = nodes_pattern.search(content)
    elemsolution_match = elemsolution_pattern.search(content)
    elements_match = elements_pattern.search(content)
    
    nodes_data = nodes_match.group(1).split(',')
    # print(len(nodes_data))
    nodes_data = np.array([float(node.strip()) for node in nodes_data]).reshape(-1, 3)  # 将节点坐标转换为 3D 数组
    
    elements_data = [int(item) for item in elements_match.group(1).split(',')]
    
    nodes_num = elements_data[0]
    elements_num = elements_data[1]
    element_size = (len(elements_data) - 2) / elements_num
    
    # print("Elements Size", element_size)
    
    elements = np.array(elements_data[2:]).reshape(-1, int(element_size))

    
    # print("Element Number", len(elements), elements[0])
    
    # print("Max", max(elements_data))
    
    # 提取并处理场解数据
    elem_solution_data = elemsolution_match.group(1).split(',')
    elem_solution_data = np.array([float(solution.strip()) for solution in elem_solution_data])
    
    # print("element", elem_solution_data[2], len(elem_solution_data), len(elem_solution_data) / elem_solution_data[2])
    
    element_solution = elem_solution_data[3:].reshape(-1, int(elem_solution_data[2]))
    
    each_element_value_num = int(elem_solution_data[2])
    
    # print(f"Each Element has {each_element_value_num} value")
    
    
    # print(len(element_solution), element_solution[0])
    
    x_data = []
    y_data = []
    z_data = []
    field_values_list = [[] for i in range(each_element_value_num + 1)]
    
    points = []
    
    for element, element_result in zip(elements, element_solution):
        # print(element, element_result)
        
        element_num = int(element[4])
        # print("This element has ", element_num)
        polygon_points = [nodes_data[idx - 1] for idx in element[-element_num:]]
        
        # print(polygon_points)
        point_x = [point[0] for point in polygon_points]
        point_y = [point[1] for point in polygon_points]
        point_z = [point[2] for point in polygon_points]
        center_x = sum(point_x) / len(point_x)
        center_y = sum(point_y) / len(point_y)
        center_z = sum(point_z) / len(point_z)        
        
        # print(center_x, center_y, value)
        
        x_data.append(center_x)
        y_data.append(center_y)
        z_data.append(center_z)
        
        points.append([center_x, center_y, center_z])
        
        for i in range(each_element_value_num): 
            field_values_list[i].append(element_result[i])

        field_values_list[each_element_value_num].append((element_result[0] **2 + element_result[1] **2 + element_result[2] **2) ** 0.5)
        
    
    return x_data, y_data, z_data, field_values_list, points



if __name__ == '__main__':
    
    
    # 打开并读取 .aedtplt 文件
    with open('../data/E.aedtplt', 'r', encoding='utf-8') as file:
        content = file.read()

        
    x_data, y_data, z_data, field_values_list = readaedt(content)
    
    # 创建一个字典，将每个列表映射到各自的列名
    data = {
        'x': x_data,
        'y': y_data,
        'z': z_data
    }

    # 将 field_values_list 展开为多个字段列
    for i, field_values in enumerate(field_values_list):
        data[f'field_{i+1}'] = field_values

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 导出到 CSV 文件
    df.to_csv('output.csv', index=False)

    
    