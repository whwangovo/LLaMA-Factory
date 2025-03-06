from openai import OpenAI
# Set OpenAI's API key and API base to use vLLM's API server.
model_path = "/home/lt_08321/hdd/wangweihang/checkpoints/Qwen/Qwen2.5-14B-Instruct"
# model_path = "/home/lt_08321/hdd/wangweihang/outputs/saves/qwen2.5-14b/full/sft"
# model_path = "/home/lt_08321/hdd/wangweihang/outputs/saves/qwen2.5-14b/full/sft_241203"
# model_path = "/home/lt_08321/hdd/wangweihang/outputs/saves/241216/qwen2.5-14b/full/pt"

openai_api_key = "EMPTY"
openai_api_base = "http://localhost:8000/v1"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# case_1 = {
#     "model": model_path,
#     "messages": [
#         {"role": "user", "content": "现在有一个《嘉善县蓉溪净水厂及配套道路（一期工程）》的工程项目，所属的分类是市政工程/污水处理/基础设施。\
#                                     你正在撰写该项目的投标书，现在写到了“第四章 工程质量保证措施/4.1 关键工序、复杂环节及预防主要质量通病技术措施”，\
#                                     请你撰写其中“4.1.1 桩基围护施工质量通病技术措施”这部分的内容,内容不少于2000字。"
#         },
#     ],
#     "max_tokens": 2048,
#     "seed": 1,
# }
# chat_response = client.chat.completions.create(**case_1)

prompt = """钢筋砼雨水管施工方案
1、施工工艺流程 
2、施工测量 
管线开工前期测定管线中线，检查井位置，建立临时水准点。测定管道中心时，在起点、终点、平面折点、纵向折点及直线段的控制点测设中心桩；在挖槽见底前、灌筑砼基础前，管道铺设或砌筑前，及时校测管道中心线及高程桩的高程。 """

case_1 = {
    "model": model_path,
    "messages": [
        {"role": "user", "content": f"有一个工程名称为“翠屏山片区路网建设乔家湖路北段工程”的项目，年度为2023年，项目分类：市政/道路，项目性质：新建,项目所在地：江苏省徐州市，建设规模：“道路北起和平路，南至郭庄路，长约 1375 米，红线宽 36 米，为城市次干路。配套建设交通、桥梁、排水、照明、绿化等工程设施”，方案分类：施工重难点/雨污水工程/钢筋砼雨水管。目前需要写钢筋砼雨水管施工方案，字数2800字左右，请你进行写作。{prompt}"},
    ],
    "max_tokens": 10000,
    "seed": 1,
}
chat_response = client.chat.completions.create(**case_1)

# case_2 = {
#     "model": model_path,
#     "messages": [
#         {"role": "user", "content": "现在有一个《嘉兴港独山港区B区21、22号多用途泊位工程房建标段》的工程项目，所属的分类是港口建筑/公用基础设施/码头。\
#             你正在撰写该项目的投标书，现在写到了“第二章难点、重点分析及实施方案/一、本工程的难点、重点/2、针对建筑结构工程的特点、难点分析和实施方案”，\
#             请你撰写其中“2、针对建筑结构工程的特点、难点分析和实施方案”这部分的内容,内不少容于2000字。"
#         },
#     ],
#     "max_tokens": 2048,
#     "seed": 3,
# }
# chat_response = client.chat.completions.create(**case_2)


print(chat_response.choices[0].message.content)
