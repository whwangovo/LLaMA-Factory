from transformers import AutoTokenizer
from tqdm import tqdm
import os
import json
def count_tokens_in_large_document(file_path, model_name='/home/lt_08321/hdd/wangweihang/checkpoints/Qwen/Qwen2.5-0.5B-Instruct', chunk_size=4000):
    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    total_token_count = 0
    
    # 获取文件的总大小（用于进度条）
    file_size = os.path.getsize(file_path)
    
    # 分块读取文件，并显示进度条
    with open(file_path, 'r', encoding='utf-8') as file, tqdm(total=file_size, desc="Processing file", unit="B", unit_scale=True) as pbar:
        while True:
            chunk = file.read(chunk_size)  # 读取指定大小的块
            if not chunk:  # 文件结束
                break
            
            # 对当前块进行编码并统计 token 数量
            tokens = tokenizer(chunk, return_tensors='pt', truncation=False)
            token_count = tokens.input_ids.size(1)
            total_token_count += token_count
            
            # 更新进度条
            pbar.update(len(chunk))
    
    print(f"Total tokens in document: {total_token_count}")
    return total_token_count

def count_tokens_in_jsonl(file_path, model_name='/home/lt_08321/hdd/wangweihang/checkpoints/Qwen/Qwen2.5-0.5B-Instruct'):
    # 加载 tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    total_token_count = 0

    # 获取文件的总大小（用于进度条）
    file_size = os.path.getsize(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # 假设整个文件是一个 JSON 数组
        with tqdm(total=len(data), desc="Processing items", unit="item") as pbar:
            for obj in data:
                text = obj.get("text", "")
                tokens = tokenizer.encode(text, add_special_tokens=False)
                total_token_count += len(tokens)
                pbar.update(1)

    print(f"所有 text 字段内容的总 token 数量为: {total_token_count}")
    return total_token_count

token_size_1 = count_tokens_in_jsonl("data/pretrain_main_250105.json")
token_size_2 = count_tokens_in_jsonl("data/pretrain_main_250312.json")
token_size_3 = count_tokens_in_jsonl("data/pretrain_rules_250105.json")
print(token_size_1 + token_size_2 + token_size_3)