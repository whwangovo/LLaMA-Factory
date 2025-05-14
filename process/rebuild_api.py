import asyncio
import aiohttp
import json
import time
import os
from openai import AsyncOpenAI
from const import output_template, instruct_template, instruct_template_wocore

# OpenAI API 配置
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

async def fetch_chat_response(original_instruction, original_output, instruct_template, output_template):
    try:
        # 构建提示词
        instruction_prompt = instruct_template.format(text=original_instruction)
        output_prompt = output_template.format(text=original_output)
        
        # 应用聊天模板
        input_messages = [
            {"role": "user", "content": instruction_prompt}
        ]
        output_messages = [
            {"role": "user", "content": output_prompt}
        ]
        
        # 创建API请求
        input_response = await client.chat.completions.create(
            model="qwen_chat",  # 使用适当的模型名称
            messages=input_messages,
            temperature=0.7,
            max_tokens=8192
        )
        
        output_response = await client.chat.completions.create(
            model="qwen_chat",  # 使用适当的模型名称
            messages=output_messages,
            temperature=0.7,
            max_tokens=8192
        )
        
        input_generated_text = input_response.choices[0].message.content
        output_generated_text = output_response.choices[0].message.content

        # 返回带有结果的字典
        return {
            'original_instruction': original_instruction,
            'instruction': input_generated_text,
            'input': '',
            'original_output': original_output,
            'output': output_generated_text
        }
        
    except Exception as e:
        return {
            'original_instruction': original_instruction,
            'instruction': f"Error: {str(e)}",
            'input': '',
            'original_output': original_output,
            'output': f"Error: {str(e)}"
        }

async def process_batch(batch_items, batch_number, output_file, instruct_template, output_template):
    print(f"Processing batch {batch_number}, items {batch_number*20}-{batch_number*20+len(batch_items)-1}")
    start_time = time.time()
    
    async with aiohttp.ClientSession():
        tasks = [
            fetch_chat_response(
                item['original_instruction'], 
                item['original_output'], 
                instruct_template, 
                output_template
            ) for item in batch_items
        ]
        batch_results = await asyncio.gather(*tasks)
    
    # 检查是否已有结果文件
    all_results = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                all_results = json.load(f)
        except json.JSONDecodeError:
            # 如果文件存在但不是有效的JSON，创建新的
            all_results = []
    
    # 添加新批次的结果
    all_results.extend(batch_results)
    
    # 保存所有结果到JSON文件
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"Batch {batch_number} results saved to {output_file}")
    except Exception as e:
        print(f"Error saving batch {batch_number} to output file: {e}")
    
    end_time = time.time()
    batch_time = end_time - start_time
    print(f"Batch {batch_number} processing time: {batch_time:.2f} seconds")
    print(f"Average time per item in batch {batch_number}: {batch_time/len(batch_items):.2f} seconds")
    
    return batch_results

async def main(input_file, output_file, batch_size=20):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} items from {input_file}")
    except Exception as e:
        print(f"Error loading input file: {e}")
        return
    
    # 检查是否有已经处理过的结果
    processed_count = 0
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                existing_results = json.load(f)
                processed_count = len(existing_results)
                print(f"Found {processed_count} already processed items in {output_file}")
        except Exception as e:
            print(f"Error reading existing output file: {e}")
            processed_count = 0
    
    # 跳过已处理的项目
    remaining_data = data[processed_count:]
    print(f"{len(remaining_data)} items remaining to be processed")
    
    if not remaining_data:
        print("All items have been processed already!")
        return
    
    all_results = []
    start_time = time.time()
    
    # 将剩余的数据分批处理
    for i in range(0, len(remaining_data), batch_size):
        batch_number = (processed_count + i) // batch_size
        batch_items = remaining_data[i:i+batch_size]
        batch_results = await process_batch(batch_items, batch_number, output_file, instruct_template_wocore, output_template)
        all_results.extend(batch_results)
    
    end_time = time.time()
    total_time = end_time - start_time
    print(f"All batches completed!")
    print(f"Total processing time: {total_time:.2f} seconds")
    print(f"Average time per item: {total_time/len(remaining_data):.2f} seconds")
    print(f"Total processed items: {processed_count + len(remaining_data)}")

if __name__ == "__main__":
    input_file = "data/source/finetune_realworld_3.json"
    output_file = "data/finetune_realworld_part3.json"
    batch_size = 100
    
    asyncio.run(main(input_file, output_file, batch_size))