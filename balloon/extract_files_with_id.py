import os, re


def extract_files_with_id(folder_path, target_id):
    id_pattern = re.compile(r'(\d+)_(\d+)\.png')  # 正则表达式用于匹配数字_数字.png的模式
    a = 0

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
