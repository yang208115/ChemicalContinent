# coding=gbk
import os
import re


def extract_files_with_id(folder_path, target_id):
    a = 0
    id_pattern = re.compile(r'(\d+)_(\d+)\.png')  # 正则表达式用于匹配数字_数字.png的模式

    results = []  # 存储提取出来的文件路径的列表

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.png'):  # 假设你的图片文件是以.png结尾的
            # 使用正则表达式从文件名中提取两个数字
            match = id_pattern.search(filename)
            if match:
                extracted_id = int(match.group(2))  # 提取第一个数字部分
                if extracted_id == target_id:
                    results.append(file_path)  # 将提取出来的文件路径添加到结果列表中
                    a += 1

    return results, a


# 使用示例
folder_path = 'balloon/image'  # 替换为你的文件夹路径
target_id = 1
b = 0
files_with_id_1, b = extract_files_with_id(folder_path, target_id)
print(files_with_id_1, " ", b)
