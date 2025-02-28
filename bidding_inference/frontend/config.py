# frontend/config.py
# 存储所有前端相关的样式、HTML 和 UI 配置

# CSS 样式定义
CSS = """
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

# HTML 内容
TITLE_HTML = """
<h1 class="title">CISL Lab: Tender Agent</h1>
<p class="subtitle">基于大模型的智能投标助手</p>
"""

FOOTER_HTML = """
<div class="footer">© 2025 CISL Laboratory. All rights reserved.</div>
"""

# 统计信息模板
def get_stats_html(chars_count, words_count, elapsed_time, token_count):
    return f"""<div class="stats-container">
        <div class="stat-box">
            <div class="stat-label">字数</div>
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

# 默认参数值
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.8
DEFAULT_MAX_TOKENS = 8192
DEFAULT_REPETITION_PENALTY = 1.05

# UI 文案
UI_TEXT = {
    "input_panel_title": '<div class="panel-title">提问区域</div>',
    "output_panel_title": '<div class="panel-title">回答结果</div>',
    "parameter_title": '<div class="parameter-title">参数设置</div>',
    "input_label": "请输入您的问题或需求",
    "input_placeholder": "请在此输入您的询问内容...",
    "output_label": "AI 回答",
    "output_placeholder": "模型回答将在这里显示...",
    "submit_button": "获取回答",
    "temperature_label": "Temperature (创造性)",
    "temperature_info": "调整回答的随机性，值越高创造性越强",
    "top_p_label": "Top P (多样性)",
    "top_p_info": "控制输出的词汇多样性",
    "max_tokens_label": "Max Tokens (最大长度)",
    "max_tokens_info": "设置回答的最大长度",
    "repetition_penalty_label": "Repetition Penalty (重复惩罚)",
    "repetition_penalty_info": "避免内容重复，值越高越不容易重复（注意，此参数暂时无效）",
    "error_stats": "<div class='stats-container'>统计信息不可用</div>"
}

# 服务器配置
SERVER_CONFIG = {
    "server_name": "0.0.0.0",
    "server_port": 7860
}