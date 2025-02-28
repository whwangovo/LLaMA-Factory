import os
import json
from pathlib import Path

def process_json_files(input_dir, output_dir):
    # 确保输出目录存在
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # 遍历输入目录中的所有json文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"{filename}")
            
            try:
                # 读取输入文件
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 转换格式
                processed_data = [{"text": item["content"]} for item in data]
                
                # 写入输出文件
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=2)
                
                print(f"Successfully processed {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

def main():
    # 设置输入和输出目录
    input_dir = "/home/lt_08321/hdd/wangweihang/data/bidding_data/pretrain_data/WuDaoCorpus2.0_base_200G"
    output_dir = "/home/lt_08321/hdd/wangweihang/data/bidding_data/pretrain_data/wudao_clean"
    
    # 处理文件
    process_json_files(input_dir, output_dir)
    print("处理完成!")

if __name__ == "__main__":
    main()