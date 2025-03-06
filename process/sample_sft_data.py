import json
import random

def sample_json(input_file, output_file, sample_size=100):
    try:
        # 读取输入JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 检查数据是否是列表
        if not isinstance(data, list):
            raise ValueError("输入JSON必须是列表格式")
            
        # 确定采样大小
        actual_sample_size = min(sample_size, len(data))
        
        # 随机采样
        sampled_data = random.sample(data, actual_sample_size)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sampled_data, f, ensure_ascii=False, indent=2)
            
        print(f"成功从{len(data)}个样本中随机采样{actual_sample_size}个样本")
        print(f"采样结果已保存至: {output_file}")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


if __name__ == "__main__":
    input_file = "process_data/finetune_general_250112.json"
    output_file = "process_data/finetune_general_250112_sample_5000.json"
    sample_size = 5000
    
    # 执行采样
    sample_json(input_file, output_file, sample_size)
