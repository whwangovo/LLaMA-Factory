import asyncio
import random
import aiohttp
import time
import csv
from openai import AsyncOpenAI
from statistics import mean
from tqdm.asyncio import tqdm_asyncio

# OpenAI API 本地部署地址
openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8001/v1"

client = AsyncOpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# 要测试的目标字数
target_word_counts = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]
samples_per_target = 100

# 保存最终统计结果
results = []

def build_prompt(word_target):
    return f"""【项目基本信息】
- 项目名称：滨海新区沧海未来社区B区块施工
- 项目年份：2024年
- 项目分类：房建/住宅
- 项目性质：新建
- 项目所在地：浙江省绍兴市

【方案分类】
- 施工方案/机电安装/电梯

【包含要点】
- 安全管理方针
- 安全管理目标
- 管理机构
- 危险源辨识与控制
- 安全管理制度
- ESHS管措施

【任务要求】
- 编写"电梯工程质量控制措施"部分
- 字数要求{word_target}字左右。"""

async def fetch_response_length(session, word_target, index):
    try:
        response = await client.chat.completions.create(
            model="qwen_chat_14",
            messages=[
                {"role": "user", "content": build_prompt(word_target)},
            ],
            temperature=0.7,
            top_p=0.9,
            max_tokens=8192,
            extra_body={"repetition_penalty": 1.05},
        )
        content = response.choices[0].message.content
        return len(content)
    except Exception as e:
        print(f"⚠️ Error for target {word_target} at index {index}: {e}")
        return 0  # 如果出错，返回0避免中断统计

async def run_test_for_target(session, word_target):
    tasks = [
        fetch_response_length(session, word_target, i)
        for i in range(samples_per_target)
    ]
    return await tqdm_asyncio.gather(*tasks, desc=f"⏳ Generating {word_target}字", ncols=100)

async def main():
    async with aiohttp.ClientSession() as session:
        for word_target in target_word_counts:
            print(f"\n🧪 正在测试目标字数：{word_target} 字")
            char_counts = await run_test_for_target(session, word_target)

            valid_counts = [c for c in char_counts if c > 0]
            if not valid_counts:
                print(f"❌ 无有效响应")
                continue

            min_len = min(valid_counts)
            max_len = max(valid_counts)
            avg_len = round(mean(valid_counts), 2)
            lower_bound = int(word_target * 0.8)
            upper_bound = int(word_target * 1.2)
            in_range = [c for c in valid_counts if lower_bound <= c <= upper_bound]
            in_range_ratio = round(len(in_range) / len(valid_counts) * 100, 2)

            print(f"✅ 完成 {word_target} 字测试")
            print(f" - 最小字数：{min_len}")
            print(f" - 最大字数：{max_len}")
            print(f" - 平均字数：{avg_len}")
            print(f" - 落在 {lower_bound}-{upper_bound} 区间的占比：{in_range_ratio}%")

            results.append({
                "目标字数": word_target,
                "最小字数": min_len,
                "最大字数": max_len,
                "平均字数": avg_len,
                "±20%区间命中率(%)": in_range_ratio,
                "样本字数列表": valid_counts,
            })

        # 写入 CSV 文件
        with open("output_stats.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "目标字数", "最小字数", "最大字数", "平均字数", "±20%区间命中率(%)", "样本字数列表"
            ])
            writer.writeheader()
            for row in results:
                row["样本字数列表"] = str(row["样本字数列表"])
                writer.writerow(row)

        print("\n📁 所有统计结果已保存至 output_stats.csv")

if __name__ == "__main__":
    asyncio.run(main())
