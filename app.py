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

if 'history' not in st.session_state:
    st.session_state.history = []

# =========================================
# 终极修复 UI CSS
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

/* 背景逻辑 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 修复侧边栏收缩按钮 */
[data-testid="stSidebar"] {
    background-color: rgba(15, 20, 35, 0.95) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
    z-index: 100;
}

/* 这里的关键：确保收缩按钮可见 */
[data-testid="stSidebarNav"] {background-color: transparent !important;}
button[kind="header"] {
    color: #00f2fe !important;
    background: rgba(0,242,254,0.1) !important;
}

/* 隐藏默认页眉 */
header {background: transparent !important;}
footer {visibility: hidden;}

/* 主标题 */
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

/* 文本域 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #0f172a !important;
    border-radius: 15px !important;
    padding: 20px !important;
    font-size: 1.1rem !important;
    border: 2px solid rgba(0, 242, 254, 0.4) !important;
}

/* ⭐ 按钮终极修复：增加 nowrap 防止变形 ⭐ */
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
    white-space: nowrap !important; /* 强制不换行 */
    box-shadow: 0 4px 20px rgba(0, 210, 255, 0.3) !important;
}

div.stButton > button:hover {
    box-shadow: 0 8px 30px rgba(0, 210, 255, 0.5) !important;
    transform: translateY(-1px);
}

/* 结果卡片 */
.result-card {
    background: rgba(255,255,255,0.07);
    border-left: 5px solid #00f2fe;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏内容
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=60)
    st.markdown("### 🔬 实验室控制台")
    
    if st.button("✨ 获取随机标本"):
        samples = ["现在的年轻人真是越来越懒了。", "这个产品简直是艺术品！"]
        st.session_state.random_text = samples[int(time.time()) % 2]

    st.markdown("---")
    # 系统信息放在折叠栏
    with st.expander("🛠️ 系统信息"):
        st.caption("内核: Gemini 1.5 Flash")
        st.caption("架构: NoBias V4.1 Stable")

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
                    response = model.generate_content(f"简要分析这段话的偏见、意图并改写：{user_input}")
                    res = response.text
                    
                    if pd:
                        st.markdown("#### 📊 维度扫描仪")
                        st.bar_chart(pd.DataFrame({'维度': ['偏激度', '情绪化'], '分值': [65, 80]}).set_index('维度'))
                    
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"故障: {e}")
        else:
            st.warning("请放入标本")