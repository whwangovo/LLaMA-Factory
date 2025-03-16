import json

def split_txt_to_json(input_file, output_file, chunk_size=4096):
    # 打开输入文件并读取内容
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # 根据指定长度进行划分
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    # 构造 JSON 结构
    json_data = [{"text": chunk} for chunk in chunks]

    # 将结果写入到 output.json 文件中
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=2)

# 示例调用
if __name__ == '__main__':
    input_file = "data/source/pretrain_rules.txt"
    output_file = "data/source/pretrain_rules.json"
    split_txt_to_json(input_file, output_file)