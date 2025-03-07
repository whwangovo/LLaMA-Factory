# app.py
# 主要的应用逻辑

import gradio as gr
from openai import OpenAI
import time
import sys
import os

# 将前端配置模块添加到路径中
sys.path.append(os.path.join(os.path.dirname(__file__), "frontend"))
from frontend.config import (
    CSS, TITLE_HTML, FOOTER_HTML, DEFAULT_TEMPERATURE, DEFAULT_TOP_P,
    DEFAULT_MAX_TOKENS, DEFAULT_REPETITION_PENALTY, UI_TEXT,
    get_stats_html, SERVER_CONFIG
)

# 可用模型列表
AVAILABLE_MODELS = [
    "qwen_chat",
    "rw",
    "cs"
]

# OpenAI 客户端配置
openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8000/v1"
default_model = "qwen_chat"  # 默认模型
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

def query_model(user_input, model_choice, temperature, top_p, max_tokens, repetition_penalty):
    """
    使用 OpenAI API 查询模型并生成响应
    """
    start_time = time.time()
    token_count = 0
    try:
        chat_response = client.chat.completions.create(
            model=model_choice,  # 使用用户选择的模型
            messages=[
                {"role": "user", "content": user_input},
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            # frequency_penalty=repetition_penalty,  # 更新为使用重复惩罚参数
            stream=True
        )
        
        collected_messages = []
        for chunk in chat_response:
            if chunk.choices[0].delta.content is not None:
                token_count += 1  # 简化的令牌计数方法
                collected_messages.append(chunk.choices[0].delta.content)
                full_response = "".join(collected_messages)
                elapsed_time = time.time() - start_time
                chars_count = len(full_response)
                words_count = len(full_response.split())
                
                stats = get_stats_html(chars_count, words_count, elapsed_time, token_count)
                
                yield full_response, stats
                
    except Exception as e:
        error_message = f"Error: {e}"
        yield error_message, UI_TEXT["error_stats"]

def create_ui():
    """
    创建 Gradio 用户界面
    """
    with gr.Blocks(css=CSS) as demo:
        with gr.Column(elem_classes="main-container"):
            with gr.Column(elem_classes="title-container"):
                gr.HTML(TITLE_HTML)
            
            with gr.Row(elem_classes="two-column"):
                # 左列 - 输入和参数
                with gr.Column(elem_classes="left-column"):
                    with gr.Column(elem_classes="panel"):
                        gr.HTML(UI_TEXT["input_panel_title"])
                        user_input = gr.Textbox(
                            label=UI_TEXT["input_label"],
                            placeholder=UI_TEXT["input_placeholder"], 
                            lines=8
                        )
                        
                        # 添加模型选择下拉菜单
                        model_choice = gr.Dropdown(
                            choices=AVAILABLE_MODELS,
                            value=default_model,
                            label="选择模型",
                            info="选择要使用的大语言模型"
                        )
                        
                        gr.HTML(UI_TEXT["parameter_title"])
                        with gr.Row():
                            with gr.Column():
                                temperature = gr.Slider(
                                    minimum=0, maximum=1, value=DEFAULT_TEMPERATURE, step=0.01,
                                    label=UI_TEXT["temperature_label"], 
                                    info=UI_TEXT["temperature_info"]
                                )
                                repetition_penalty = gr.Slider(
                                    minimum=1.0, maximum=2.0, value=DEFAULT_REPETITION_PENALTY, step=0.01,
                                    label=UI_TEXT["repetition_penalty_label"], 
                                    info=UI_TEXT["repetition_penalty_info"]
                                )
                            with gr.Column():
                                top_p = gr.Slider(
                                    minimum=0, maximum=1, value=DEFAULT_TOP_P, step=0.01,
                                    label=UI_TEXT["top_p_label"], 
                                    info=UI_TEXT["top_p_info"]
                                )
                                max_tokens = gr.Slider(
                                    minimum=1024, maximum=8192, value=DEFAULT_MAX_TOKENS, step=512,
                                    label=UI_TEXT["max_tokens_label"], 
                                    info=UI_TEXT["max_tokens_info"]
                                )
                        
                        submit_btn = gr.Button(UI_TEXT["submit_button"], elem_classes="submit-button")
                
                # 右列 - 输出和统计
                with gr.Column(elem_classes="right-column"):
                    with gr.Column(elem_classes="panel"):
                        gr.HTML(UI_TEXT["output_panel_title"])
                        output = gr.Textbox(
                            label=UI_TEXT["output_label"],
                            placeholder=UI_TEXT["output_placeholder"], 
                            lines=15
                        )
                        stats_output = gr.HTML()
            
            gr.HTML(FOOTER_HTML)
            
            submit_btn.click(
                fn=query_model,
                inputs=[user_input, model_choice, temperature, top_p, max_tokens, repetition_penalty],
                outputs=[output, stats_output]
            )
    
    return demo

def main():
    """
    主函数，用于启动应用程序
    """
    demo = create_ui()
    demo.launch(
        server_name=SERVER_CONFIG["server_name"],
        server_port=SERVER_CONFIG["server_port"]
    )

if __name__ == "__main__":
    main()