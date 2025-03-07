import gradio as gr
from openai import OpenAI
import time

openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8000/v1"
model = "qwen_chat"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)

css = """
.gradio-container {
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

.main-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.title-container {
    text-align: center;
    margin-bottom: 1.5rem;
}

.title {
    font-size: 2rem !important;
    color: #2563EB !important;
    margin-bottom: 0.5rem !important;
}

.subtitle {
    font-size: 1rem;
    color: #6B7280;
    margin-bottom: 1.5rem;
}

.two-column {
    display: flex;
    gap: 1.5rem;
}

.left-column, .right-column {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.panel {
    background-color: #F9FAFB;
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    height: 100%;
}

.panel-title {
    font-weight: bold;
    font-size: 1.1rem;
    color: #374151;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E5E7EB;
}

.parameter-section {
    background-color: #F3F4F6;
    border-radius: 8px;
    padding: 0.8rem;
    border: 1px solid #E5E7EB;
    margin-bottom: 1rem;
}

.parameter-title {
    font-weight: bold;
    font-size: 0.9rem;
    color: #374151;
    margin-bottom: 0.5rem;
}

.submit-button {
    background-color: #2563EB !important;
    color: white !important;
    padding: 0.5rem 1.5rem !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
    margin-top: 0.5rem !important;
}

.submit-button:hover {
    background-color: #1D4ED8 !important;
    transform: translateY(-1px) !important;
}

.stats-container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
    margin-top: 1rem;
    background-color: #EFF6FF;
    border-radius: 8px;
    padding: 0.8rem;
    border: 1px solid #DBEAFE;
}

.stat-box {
    text-align: center;
    padding: 0.5rem;
}

.stat-label {
    font-size: 0.8rem;
    color: #4B5563;
}

.stat-value {
    font-size: 1.1rem;
    font-weight: bold;
    color: #2563EB;
}

.footer {
    text-align: center;
    font-size: 0.8rem;
    color: #9CA3AF;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #E5E7EB;
}
"""

def query_model(user_input, temperature, top_p, max_tokens, repetition_penalty):
    start_time = time.time()
    token_count = 0
    try:
        chat_response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": user_input},
            ],
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            extra_body={
                "repetition_penalty": repetition_penalty,
            },
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
                # words_count = len(full_response.split())
                
                stats = f"""<div class="stats-container">
                    <div class="stat-box">
                        <div class="stat-label">汉字数</div>
                        <div class="stat-value">{chars_count}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Token数</div>
                        <div class="stat-value">{token_count}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">耗时</div>
                        <div class="stat-value">{elapsed_time:.2f}秒</div>
                    </div>
                </div>"""
                
                yield full_response, stats
                
    except Exception as e:
        error_message = f"Error: {e}"
        yield error_message, "<div class='stats-container'>统计信息不可用</div>"

with gr.Blocks(css=css) as demo:
    with gr.Column(elem_classes="main-container"):
        with gr.Column(elem_classes="title-container"):
            gr.HTML("""
                <h1 class="title">CISL Lab: Tender Agent</h1>
                <p class="subtitle">基于大模型的智能投标助手</p>
            """)
        
        with gr.Row(elem_classes="two-column"):
            # 左列 - 输入和参数
            with gr.Column(elem_classes="left-column"):
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<div class="panel-title">提问区域</div>')
                    user_input = gr.Textbox(
                        label="请输入您的问题或需求",
                        placeholder="请在此输入您的询问内容...", 
                        lines=8
                    )
                    
                    gr.HTML('<div class="parameter-title">参数设置</div>')
                    with gr.Row():
                        with gr.Column():
                            temperature = gr.Slider(
                                minimum=0, maximum=1, value=0.7, step=0.01,
                                label="Temperature (创造性)", 
                                info="调整回答的随机性，值越高创造性越强"
                            )
                            repetition_penalty = gr.Slider(
                                minimum=1.0, maximum=2.0, value=1.05, step=0.01,
                                label="Repetition Penalty (重复惩罚)", 
                                info="避免内容重复，值越高越不容易重复"
                            )
                        with gr.Column():
                            top_p = gr.Slider(
                                minimum=0, maximum=1, value=0.8, step=0.01,
                                label="Top P (多样性)", 
                                info="控制输出的词汇多样性"
                            )
                            max_tokens = gr.Slider(
                                minimum=1024, maximum=8192, value=8192, step=512,
                                label="Max Tokens (最大长度)", 
                                info="设置回答的最大长度"
                            )
                    
                    submit_btn = gr.Button("获取回答", elem_classes="submit-button")
            
            # 右列 - 输出和统计
            with gr.Column(elem_classes="right-column"):
                with gr.Column(elem_classes="panel"):
                    gr.HTML('<div class="panel-title">回答结果</div>')
                    output = gr.Textbox(
                        label="AI 回答",
                        placeholder="模型回答将在这里显示...", 
                        lines=15
                    )
                    stats_output = gr.HTML()
        
        gr.HTML('<div class="footer">© 2025 CISL Laboratory. All rights reserved.</div>')
        
        submit_btn.click(
            fn=query_model,
            inputs=[user_input, temperature, top_p, max_tokens, repetition_penalty],
            outputs=[output, stats_output]
        )

# 启动服务
demo.launch(server_name="0.0.0.0", server_port=7860)