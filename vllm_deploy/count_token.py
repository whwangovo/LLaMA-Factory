from transformers import AutoTokenizer
from tqdm import tqdm
import os
import json

if __name__ == "__main__":
    model_name = "checkpoints/Qwen/Qwen2.5-0.5B-Instruct"
    file_path =  "data/bidding_pretrain_241216.json"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    total_token_count = 0
    with open(file_path, 'r') as f:
        datas = json.load(f)
    
    for data in tqdm(datas):
        v = data['text']
        tokens = tokenizer(v, return_tensors='pt', truncation=False)
        token_count = tokens.input_ids.size(1)
        total_token_count += token_count
        
    print(total_token_count)