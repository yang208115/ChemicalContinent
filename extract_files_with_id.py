import os, re


def extract_files_with_id(folder_path, target_id):
    id_pattern = re.compile(r'(\d+)_(\d+)\.png')  # ������ʽ����ƥ������_����.png��ģʽ
    a = 0

    results = []  # �洢��ȡ�������ļ�·�����б�

    # �����ļ����е������ļ�
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.png'):  # �������ͼƬ�ļ�����.png��β��
            # ʹ��������ʽ���ļ�������ȡ��������
            match = id_pattern.search(filename)
            if match:
                extracted_id = int(match.group(2))  # ��ȡ��һ�����ֲ���
                if extracted_id == target_id:
                    results.append(file_path)  # ����ȡ�������ļ�·����ӵ�����б���
                    a += 1

    return results, a
