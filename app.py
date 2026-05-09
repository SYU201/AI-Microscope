import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# 尝试导入 pandas
try:
    import pandas as pd
except ImportError:
    pd = None

# =========================================
# 基础配置
# =========================================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="NoBias AI 心理实验室",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化历史记录
if 'history' not in st.session_state:
    st.session_state.history = []

# =========================================
# UI 样式 (保持 V4.1 风格不变)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

.stApp {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stSidebar"] {
    background-color: rgba(15, 20, 35, 0.95) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
    z-index: 100;
}

[data-testid="stSidebarNav"] {background-color: transparent !important;}
button[kind="header"] {
    color: #00f2fe !important;
    background: rgba(0,242,254,0.1) !important;
}

header {background: transparent !important;}
footer {visibility: hidden;}

.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: clamp(2rem, 5vw, 3.5rem) !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #a29bfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 10px rgba(0,242,254,0.3));
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    color: rgba(255,255,255,0.6);
    font-size: 1rem;
    letter-spacing: 6px;
    margin-bottom: 30px;
}

.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #0f172a !important;
    border-radius: 15px !important;
    padding: 20px !important;
    font-size: 1.1rem !important;
    border: 2px solid rgba(0, 242, 254, 0.4) !important;
}

div.stButton > button {
    width: 100% !important;
    height: 3.8rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 15px !important;
    white-space: nowrap !important;
    box-shadow: 0 4px 20px rgba(0, 210, 255, 0.3) !important;
}

div.stButton > button:hover {
    box-shadow: 0 8px 30px rgba(0, 210, 255, 0.5) !important;
    transform: translateY(-1px);
}

.result-card {
    background: rgba(255,255,255,0.07);
    border-left: 5px solid #00f2fe;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    color: white;
}

/* 历史记录文本样式 */
.history-item {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.7);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏内容 (补全历史记录部分)
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=60)
    st.markdown("### 🔬 实验室控制台")
    
    # 1. 随机标本按钮
    if st.button("✨ 获取随机标本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平。",
            "这个产品的设计简直是天才！虽然贵但物有所值。",
            "专家说多喝热水能治百病，我看那些不听的人身体都不行。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")

    # 2. 核心补全：历史实验记录展示
    st.markdown("📂 **历史实验记录**")
    if st.session_state.history:
        # 使用 expander 避免侧边栏太长
        with st.expander("点击展开/记录"):
            for i, record in enumerate(reversed(st.session_state.history)):
                # 只显示样本的前 20 个字作为标题
                st.markdown(f"<div class='history-item'><b>记录 {len(st.session_state.history)-i}:</b><br>{record[:50]}...</div>", unsafe_allow_html=True)
        
        # 3. 导出按钮
        history_text = "\n\n".join(st.session_state.history)
        st.download_button("📥 导出实验存档", history_text, file_name="bias_lab_report.txt")
    else:
        st.caption("暂无历史记录可供查看")

    st.markdown("---")
    
    # 4. 系统信息
    with st.expander("🛠️ 系统信息"):
        st.caption("内核: Gemini 1.5 Flash")
        st.caption("架构: NoBias V4.2 Stable")
        st.caption("环境: Streamlit Cloud")

# =========================================
# 主界面
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS</div>', unsafe_allow_html=True)

_, col_m, _ = st.columns([1, 8, 1])

with col_m:
    # 输入区
    txt = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=txt, placeholder="输入标本...", height=200)
    
    # 扫描按钮
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            with st.spinner('正在解剖文本...'):
                try:
                    response = model.generate_content(f"作为文字解剖专家，深度分析这段话的偏见、意图、逻辑谬误并提供中立改写：{user_input}")
                    res = response.text
                    
                    # 关键：将记录存入历史
                    st.session_state.history.append(f"【标本】：{user_input}\n【分析报告】：\n{res}")
                    
                    if pd:
                        st.markdown("#### 📊 维度扫描仪")
                        # 模拟图表
                        st.bar_chart(pd.DataFrame({'维度': ['偏激度', '情绪化', '偏见感'], '分值': [70, 85, 60]}).set_index('维度'))
                    
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                    st.toast("扫描完成，已自动归档", icon="✅")
                except Exception as e:
                    st.error(f"实验室设备故障: {e}")
        else:
            st.warning("⚠️ 标本盒为空，请输入内容。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)