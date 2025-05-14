import os
import json
import pandas as pd
from pathlib import Path

def json_to_csv(json_folder_path, output_csv_path):
    # 获取文件夹中的所有JSON文件
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]
    
    if not json_files:
        print(f"在 {json_folder_path} 中没有找到JSON文件")
        return None
    
    # 创建一个字典来存储所有数据，以input为键
    all_data = {}
    json_file_names = []
    
    # 遍历每个JSON文件
    for json_file in json_files:
        file_path = os.path.join(json_folder_path, json_file)
        json_name = Path(json_file).stem  # 获取不带扩展名的文件名
        json_file_names.append(json_name)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # 处理每条数据
                for item in data:
                    input_value = item.get('input', '')
                    output_value = item.get('output', '')
                    
                    # 如果这个input尚未在字典中，则创建一个新条目
                    if input_value not in all_data:
                        all_data[input_value] = {'input': input_value}
                    
                    # 添加当前JSON文件的output
                    all_data[input_value][json_name] = output_value
        
        except Exception as e:
            print(f"处理文件 {json_file} 时出错: {e}")
    
    # 将字典转换为DataFrame
    df = pd.DataFrame.from_dict(all_data.values())
    
    # 确保所有列都存在，对于缺失的值填充为空字符串
    for json_name in json_file_names:
        if json_name not in df.columns:
            df[json_name] = ''
    
    # 重新排列列，使input列在最前面
    columns = ['input'] + [col for col in df.columns if col != 'input']
    df = df[columns]
    
    # 保存为CSV
    df.to_excel(output_csv_path, index=False)
    print(f"数据已合并并保存至 {output_csv_path}")
    
    return output_csv_path

if __name__ == "__main__":    
    json_folder = "data/test/test_output/0425"
    output_path =  "data/test/test_output/0425/test_output.xlsx"
    
    json_to_csv(json_folder, output_path)