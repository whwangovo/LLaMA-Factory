import json
import pandas as pd

# 读取JSON文件
with open('finetune_output_250125_async.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 准备数据列表
rows = []
for item in data:
    rows.extend([
        {'prompt': item['q'], 'content_1': item['a_1'], 'content_2': item['a_2'], 'content_3': item['a_3']},
    ])

# 创建DataFrame
df = pd.DataFrame(rows)

# 保存为Excel
df.to_excel('responses.xlsx', index=False, engine='openpyxl')