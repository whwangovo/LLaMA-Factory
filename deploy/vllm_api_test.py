import asyncio
import random
import aiohttp
import time
from openai import AsyncOpenAI

# OpenAI API 配置
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8001/v1"

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
    user_prompt = f"""你是一名熟悉建筑领域投标书编写规范的工程专家，请根据以下项目信息，**严格按照技术标评审因素中给出的顺序与一级标题名称**，生成一份最多包含七级目录的技术标目录结构。

请注意以下要求：
1. 目录中每个一级标题必须严格使用技术标评审因素中给出的名称和顺序，不可更改；
2. 仅二级标题及以下可以根据内容自由扩展，最多支持到七级标题，使用层级标识符 `[L1]` ~ `[L7]`；
3. 二级及以下标题的生成应**充分依赖“建设规模”与“招标范围”**中提及的工程内容，体现项目重点；
4. 参考“项目分类”与“项目性质”对目录结构进行优化调整，合理规避无关章节；
5. 参考“项目地点”、“计划开始时间”和“计划竣工时间”判断施工工期是否包含雨季或冬季，并进一步在相关二级标题中添加目录内容。如果无法判断则默认不生成；
6. 不输出正文内容，仅输出目录结构，格式如下：
<format>
[L1] 一级标题名称
[L2] 二级标题名称
[L3] 三级标题名称
……
</format>

以下是项目信息：

- 项目地点：江苏省宿迁市
- 项目性质：市政/道路（如新建、改建等）
- 项目分类：改建（如房建、市政等）
- 建设规模：项目对宿豫大道（项王东路-燕山路）进行改造提升，道路全长约 2.3km， 本次改造内容包括：（1）双侧雨水管网改造约 4.6 km，管径 D600-D2200mm；（2）污水管 网改造约 2.3 km，管径 D400-D600mm；（3）道路断面优化及修复等；总投资约 8000 万元（描述建筑体量、层数、面积等）
- 招标范围：项目对宿豫大道（项王东路-燕山路）进行改造提升，道路全长约 2.3km， 本次改造内容包括：（1）双侧雨水管网改造约 4.6 km，管径 D600-D2200mm；（2）污水管 网改造约 2.3 km，管径 D400-D600mm；（3）道路断面优化及修复等；总投资约 8000 万元（施工内容或承包内容）
- 计划开工时间：
- 计划竣工时间：
- 技术标评审因素（按以下顺序和名称生成一级标题）：
  总体概述：施工组织总体设想、方案针对性及施工标段划分
  施工现场平面布置和临时设施、临时道路布置
  施工进度计划和各阶段进度的保证措施
  施工过程各阶段质量安全的保证措施
  劳动力、机械设备和材料投入计划
  关键施工技术、工艺及工程项目实施的重点、难点和解决方案
  新技术、新产品、新工艺、新材料应用

请根据上述信息生成格式规范的技术标目录（只输出 `[Lx] 标题名称`，不包含任何注释）:"""
    
    try:
        response = await client.chat.completions.create(
            model="qwen_chat",
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
