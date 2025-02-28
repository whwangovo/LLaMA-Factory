from transformers import AutoTokenizer
from tqdm import tqdm
import os

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

token_size = count_tokens_in_large_document('/home/lt_08321/ssd/wangweihang/LLaMA-Factory/process_data/combine.txt')
print(token_size)