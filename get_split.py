import json

with open("data/zhulong@2@20250225_original.json", 'r') as f:
    data = json.load(f)

dpo_data = data[:1000]
other_data = data[1000:]

with open("data/dpo@zhulong@2@20250306.json", 'w', encoding='utf8') as f:
    json.dump(dpo_data, f, ensure_ascii=False)

with open("data/finetune@zhulong@2@20250306.json", 'w', encoding='utf8') as f:
    json.dump(other_data, f, ensure_ascii=False)