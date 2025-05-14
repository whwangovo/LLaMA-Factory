# frontend/ui.py
# 负责界面构建和交互

import gradio as gr
from frontend.config import (
    CSS, TITLE_HTML, FOOTER_HTML, DEFAULT_TEMPERATURE, DEFAULT_TOP_P,
    DEFAULT_MAX_TOKENS, DEFAULT_REPETITION_PENALTY, UI_TEXT,
    get_stats_html, SERVER_CONFIG
)

# 从后端导入功能函数
from backend.core import (
    query_model, clear_chat, stop_generating, clear_input,
    AVAILABLE_MODELS, default_model
)

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
    
    # 按钮行，使用container_class增加自定义样式类
    with gr.Row(elem_classes="button-row"):
        clear_btn = gr.Button("清空对话", variant="secondary", elem_classes="action-button")
        submit_btn = gr.Button(UI_TEXT["submit_button"], elem_classes="action-button submit-button")
        stop_btn = gr.Button("停止生成", variant="stop", elem_classes="action-button stop-button")
    
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
    # 扩展CSS样式，添加按钮对齐的样式
    extended_css = CSS + """
    /* 按钮行样式 */
    .button-row {
        display: flex !important;
        gap: 10px !important;
        margin-top: 10px !important;
        margin-bottom: 10px !important;
    }
    
    /* 统一按钮样式 */
    .action-button {
        flex: 1 !important;
        min-width: 0 !important;
        height: 40px !important;
    }
    
    /* 确保按钮文字居中 */
    .action-button > div {
        justify-content: center !important;
    }
    
    /* 停止按钮样式 */
    .stop-button {
        background-color: #e74c3c !important;
        color: white !important;
    }
    """
    
    with gr.Blocks(css=extended_css) as demo:
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
            
            # 停止生成按钮事件
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

def launch_ui():
    """
    启动用户界面
    """
    demo = create_ui()
    demo.launch(
        server_name=SERVER_CONFIG["server_name"],
        server_port=SERVER_CONFIG["server_port"]
    )