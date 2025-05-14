# app.py
# 主要的应用逻辑 - 多轮对话版本

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

# 添加全局停止生成标志
STOP_GENERATION = False

# 可用模型列表
AVAILABLE_MODELS = [
    "qwen_chat",
    "rw",
    "cs"
]

# OpenAI 客户端配置
openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8001/v1"
default_model = "qwen_chat"  # 默认模型

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

# ====================== 核心功能函数 ======================

def create_chat_completion(messages, model_choice, temperature, top_p, max_tokens, repetition_penalty):
    """
    创建聊天完成请求 - 将API调用逻辑分离出来便于测试和维护
    """
    return client.chat.completions.create(
        model=model_choice,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        frequency_penalty=repetition_penalty,
        stream=True
    )

def format_chat_history(chat_history):
    """
    将对话历史格式化为API请求格式
    """
    messages = []
    for human_msg, ai_msg in chat_history:
        messages.append({"role": "user", "content": human_msg})
        if ai_msg:  # 确保AI消息不为空
            messages.append({"role": "assistant", "content": ai_msg})
    return messages

def query_model(user_input, chat_history, model_choice, temperature, top_p, max_tokens, repetition_penalty, stop_generation_state):
    """
    使用 OpenAI API 查询模型并生成响应
    """
    # 输入验证
    if not user_input or not user_input.strip():
        return chat_history, "", UI_TEXT["error_stats"], False
    
    # 重置停止生成标志
    global STOP_GENERATION
    STOP_GENERATION = False
    
    # 准备历史消息列表
    messages = format_chat_history(chat_history)
    
    # 添加当前用户输入
    messages.append({"role": "user", "content": user_input})
    
    # 初始化计时和计数
    start_time = time.time()
    token_count = 0
    collected_messages = []
    
    try:
        # 创建聊天完成请求
        chat_response = create_chat_completion(
            messages=messages,
            model_choice=model_choice,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            repetition_penalty=repetition_penalty
        )
        
        # 处理流式响应
        for chunk in chat_response:
            # 检查是否应该停止生成 (使用全局变量)
            if STOP_GENERATION:
                break
                
            if chunk.choices[0].delta.content is not None:
                token_count += 1
                collected_messages.append(chunk.choices[0].delta.content)
                full_response = "".join(collected_messages)
                
                # 计算统计信息
                stats = calculate_stats(full_response, start_time, token_count)
                
                # 更新聊天历史（临时，用于显示）
                chat_history_with_response = chat_history + [(user_input, full_response)]
                
                yield chat_history_with_response, "", stats, False
        
        # 检查是否被停止
        if STOP_GENERATION:
            full_response = "".join(collected_messages) + " [已停止生成]"
            # 重置停止标志
            reset_stop_generation()
        else:
            full_response = "".join(collected_messages)
            
        # 计算最终统计信息
        stats = calculate_stats(full_response, start_time, token_count)
        
        # 将结果添加到聊天历史
        chat_history.append((user_input, full_response))
        return chat_history, "", stats, False
                
    except Exception as e:
        error_message = f"Error: {e}"
        chat_history.append((user_input, error_message))
        return chat_history, "", UI_TEXT["error_stats"], False

def calculate_stats(text, start_time, token_count):
    """
    计算响应统计信息（字符数、单词数、时间等）
    """
    elapsed_time = time.time() - start_time
    chars_count = len(text)
    words_count = len(text.split())
    return get_stats_html(chars_count, words_count, elapsed_time, token_count)

# ====================== 界面状态操作函数 ======================

def clear_chat():
    """
    清空聊天历史
    """
    return [], "", "", False

def stop_generating():
    """
    设置停止生成标志
    """
    global STOP_GENERATION
    STOP_GENERATION = True
    return True

def reset_stop_generation():
    """
    重置停止生成标志
    """
    global STOP_GENERATION
    STOP_GENERATION = False
    return False

def clear_input():
    """
    清空输入框
    """
    return ""

# ====================== UI 构建函数 ======================

def create_parameter_panel():
    """
    创建参数控制面板
    """
    model_choice = gr.Dropdown(
        choices=AVAILABLE_MODELS,
        value=default_model,
        label="选择模型",
        info="选择要使用的大语言模型"
    )
    
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
    
    return model_choice, temperature, top_p, max_tokens, repetition_penalty

def create_input_panel():
    """
    创建输入面板
    """
    user_input = gr.Textbox(
        label=UI_TEXT["input_label"],
        placeholder=UI_TEXT["input_placeholder"], 
        lines=3
    )
    
    with gr.Row():
        clear_btn = gr.Button("清空对话", variant="secondary")
        submit_btn = gr.Button(UI_TEXT["submit_button"], elem_classes="submit-button")
        stop_btn = gr.Button("停止生成", variant="stop", elem_classes="stop-button")
    
    return user_input, submit_btn, clear_btn, stop_btn

def create_output_panel():
    """
    创建输出面板
    """
    chatbot = gr.Chatbot(
        label="对话历史",
        elem_id="chatbot",
        height=400,
        show_label=True
    )
    
    output = gr.Textbox(
        label="调试输出",
        visible=False  # 隐藏，仅用于调试
    )
    
    stats_output = gr.HTML()
    
    return chatbot, output, stats_output

def create_ui():
    """
    创建完整的用户界面
    """
    with gr.Blocks(css=CSS) as demo:
        # 状态变量
        chat_history = gr.State([])
        stop_generation = gr.State(False)
        
        with gr.Column(elem_classes="main-container"):
            # 标题部分
            with gr.Column(elem_classes="title-container"):
                gr.HTML(TITLE_HTML)
            
            # 主体内容
            with gr.Row(elem_classes="two-column"):
                # 左列 - 输入和参数
                with gr.Column(elem_classes="left-column"):
                    with gr.Column(elem_classes="panel"):
                        gr.HTML(UI_TEXT["input_panel_title"])
                        
                        # 创建输入面板
                        user_input, submit_btn, clear_btn, stop_btn = create_input_panel()
                        
                        # 模型选择和参数控制
                        gr.HTML(UI_TEXT["parameter_title"])
                        model_choice, temperature, top_p, max_tokens, repetition_penalty = create_parameter_panel()
                
                # 右列 - 聊天历史和统计信息
                with gr.Column(elem_classes="right-column"):
                    with gr.Column(elem_classes="panel"):
                        gr.HTML(UI_TEXT["output_panel_title"])
                        
                        # 创建输出面板
                        chatbot, output, stats_output = create_output_panel()
            
            # 页脚
            gr.HTML(FOOTER_HTML)
            
            # ========== 事件处理 ==========
            
            # 提交按钮点击事件
            submit_btn.click(
                fn=query_model,
                inputs=[user_input, chat_history, model_choice, temperature, top_p, max_tokens, repetition_penalty, stop_generation],
                outputs=[chatbot, output, stats_output, stop_generation],
                queue=True
            ).then(
                fn=clear_input,
                inputs=None,
                outputs=[user_input]
            )
            
            # 停止生成按钮事件 - 使用全局变量处理
            stop_btn.click(
                fn=stop_generating,
                inputs=None,
                outputs=[stop_generation],
                queue=False
            )
            
            # 清空聊天按钮事件
            clear_btn.click(
                fn=clear_chat,
                inputs=None,
                outputs=[chatbot, output, stats_output, stop_generation]
            )
            
            # 回车键提交
            user_input.submit(
                fn=query_model,
                inputs=[user_input, chat_history, model_choice, temperature, top_p, max_tokens, repetition_penalty, stop_generation],
                outputs=[chatbot, output, stats_output, stop_generation],
                queue=True
            ).then(
                fn=clear_input,
                inputs=None,
                outputs=[user_input]
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