import asyncio
import random
import aiohttp
import time
from openai import AsyncOpenAI

# OpenAI API 配置
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def get_random_word_count():
    """生成符合正态分布的字数要求（500-5000）。"""
    while True:
        word_count = int(random.gauss(2750, 750))  # 均值 2750，标准差 750
        if 500 <= word_count <= 5000:
            return word_count

total_chars = 0  # 统计生成的汉字总数

async def fetch_chat_response(session, index):
    global total_chars
    word_count = get_random_word_count()
    user_prompt = f"有一个工程名称为“01依江新能源汽车零部件产业基地B区建设项目”的项目，2024年的，项目分类：房建/库房，项目性质：新建,项目所在地：安徽省安庆市，建设规模：“本项目为安庆迎江经济开发区提质增效项目-依江新能源汽车零部件产业基地B区建设项目，项目主要内容包括建设厂房、宿舍及附属配套设施等，总建筑面积约4.20万平方米:详见施工图设计文件、工程量清单及最高投标限价等。”，招标范围：“招标文件、施工图设计文件中涉及《安庆迎江经济开发区提质增效项目-依江新能源汽车零部件产业基地B区》的建筑、装饰、安装、室外道排、景观、室外安装工程等内容,”，方案分类：施工方案/季节性/季节性。目前需要写季节性施工方案，字数7000字左右，请你进行写作"
    
    try:
        response = await client.chat.completions.create(
            model="cs",
            messages=[
                # {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            top_p=0.8,
            max_tokens=8192,
            extra_body={"repetition_penalty": 1.05},
        )
        response_text = response.choices[0].message.content
        total_chars += len(response_text)  # 统计汉字数量
        print(f"Response {index}: {response_text}...")  # 仅打印前100字符
    except Exception as e:
        print(f"Error in request {index}: {e}")

async def main(step):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chat_response(session, i) for i in range(step)]
        await asyncio.gather(*tasks)
        # for i in range(step):
        #     await fetch_chat_response(session, i)
        #     await asyncio.sleep(0.5)  # 每次请求间隔 0.5 秒
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Completed {step} requests in {total_time:.2f} seconds")
    print(f"Total generated characters: {total_chars}")
    print(f"Characters per second: {total_chars / total_time:.2f}")

if __name__ == "__main__":
    asyncio.run(main(1))
