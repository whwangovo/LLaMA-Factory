from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# model_path = "/home/lt_08321/hdd/wangweihang/checkpoints/Qwen/Qwen2.5-14B-Instruct"
# model_path = "/home/lt_08321/hdd/wangweihang/outputs/saves/qwen2.5-14b/full/sft/"
model_path = "/home/lt_08321/hdd/wangweihang/outputs/saves/qwen2.5-14b/full/sft_241203/"

# Initialize the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Pass the default decoding hyperparameters of Qwen2.5-7B-Instruct
# max_tokens is for the maximum length for generation.
sampling_params = SamplingParams(temperature=0.7, top_p=0.8, repetition_penalty=1.05, max_tokens=2048)

# Input the model name or path. Can be GPTQ or AWQ models.
llm = LLM(model=model_path)

# Prepare your prompts
prompt = "现在有一个《嘉善县蓉溪净水厂及配套道路（一期工程）》的工程项目，所属的分类是市政工程/污水处理/基础设施。\
    你正在撰写该项目的投标书，现在写到了“第四章 工程质量保证措施/4.1 关键工序、复杂环节及预防主要质量通病技术措施”，\
    请你撰写其中“4.1.1 桩基围护施工质量通病技术措施”这部分的内容,内容不少于2000字。"
    
messages = [
    {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
    {"role": "user", "content": prompt}
]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# generate outputs
outputs = llm.generate([text], sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Generated text: {generated_text!r}")