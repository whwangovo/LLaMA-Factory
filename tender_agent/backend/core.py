# backend/core.py
# 后端核心功能实现

from openai import OpenAI
import time
import sys
import os

# 引入前端配置
sys.path.append(os.path.join(os.path.dirname(__file__), "../frontend"))
from config import UI_TEXT, get_stats_html

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
        print("messages:", messages)
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