import gradio as gr
from openai import OpenAI

openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8000/v1"

model = "bidding_outputs/finetune_outputs/bidding_pretrain_finetune_250118"

client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def query_model(user_input, temperature, top_p, max_tokens, repetition_penalty):
    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=[
                # {"role": "system", "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant."},
                {"role": "user", "content": user_input},
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
            stream=True  # 启用流式输出
        )
        
        # 处理流式响应
        collected_messages = []
        for chunk in chat_response:
            if chunk.choices[0].delta.content is not None:
                collected_messages.append(chunk.choices[0].delta.content)
                yield "".join(collected_messages)
                
    except Exception as e:
        yield f"Error: {e}"

default_temperature = 0.7
default_top_p = 0.8
default_max_tokens = 8192
default_repetition_penalty = 1.05

# 修改: 改用 Interface 而不是 Blocks
demo = gr.Interface(
    fn=query_model,
    inputs=[
        gr.Textbox(label="Input", placeholder="请输入", lines=4),
        gr.Slider(minimum=0, maximum=1, value=default_temperature, label="Temperature"),
        gr.Slider(minimum=0, maximum=1, value=default_top_p, label="Top P"),
        gr.Slider(minimum=8192, maximum=8192, value=default_max_tokens, step=1, label="Max Tokens"),
        gr.Slider(minimum=1.0, maximum=2.0, value=default_repetition_penalty, step=0.01, label="Repetition Penalty")
    ],
    outputs=gr.Textbox(label="Output", placeholder="模型回答...", lines=10),
    title="CISL Lab: Tender Agent",
    live=False,  # 不使用实时更新
)

# 启动服务
demo.launch(server_name="0.0.0.0", server_port=7860)