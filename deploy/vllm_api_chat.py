import asyncio
import random
import aiohttp
import time
import json
from openai import AsyncOpenAI

# OpenAI API 配置
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

total_chars = 0  # 统计生成的汉字总数

async def fetch_chat_response(session, item, index):
    global total_chars
    question = item["question"]
    
    try:
        response = await client.chat.completions.create(
            model="qwen_chat",
            messages=[
                {"role": "user", "content": question},
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=8192,
            extra_body={"repetition_penalty": 1.05},
        )
        response_text = response.choices[0].message.content
        # total_chars += len(response_text)  # 统计汉字数量
        # print(f"Response {index}: {response_text[:100]}...")  # 仅打印前100字符
        
        # 添加预测结果到原始数据项
        item["predict"] = response_text
        return item
        
    except Exception as e:
        print(f"Error in request {index}: {e}")
        item["predict"] = f"Error: {str(e)}"
        return item

async def main(input_file, output_file):
    # 读取JSON文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} items from {input_file}")
    except Exception as e:
        print(f"Error loading input file: {e}")
        return
    
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chat_response(session, item, i) for i, item in enumerate(data)]
        results = await asyncio.gather(*tasks)
    
    # 保存结果到JSON文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")
    
    end_time = time.time()
    total_time = end_time - start_time

if __name__ == "__main__":
    input_file = "data/eval_data/keywords_data.json"  # 输入文件名
    output_file = "data/eval_data/keywords_data@predict@14b.json"  # 输出文件名
    asyncio.run(main(input_file, output_file))