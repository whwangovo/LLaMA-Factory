import json
import argparse

def replace_templates(data, name, author):
    """
    递归地处理数据结构中的所有字符串，替换模板变量
    """
    if isinstance(data, dict):
        return {k: replace_templates(v, name, author) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_templates(item, name, author) for item in data]
    elif isinstance(data, str):
        return data.replace("{{name}}", name).replace("{{author}}", author)
    else:
        return data

def process_json_file(input_file, output_file, name, author):
    try:
        # 读取输入JSON文件
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 替换模板变量
        processed_data = replace_templates(data, name, author)
        
        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, ensure_ascii=False, indent=2)
            
        print(f"处理完成！结果已保存至: {output_file}")
        
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")


if __name__ == "__main__":
    input_file = "/home/lt_08321/ssd/wangweihang/LLaMA-Factory/data/archived/identity.json"
    output_file = "/home/lt_08321/ssd/wangweihang/LLaMA-Factory/data/archived/identity_cisl.json"
    sample_size = 100
    name = "Tender Agent"
    author = "CISL Lab"
    
    process_json_file(input_file, output_file, name, author)
