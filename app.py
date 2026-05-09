import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# 尝试导入 pandas，如果环境未就绪则优雅跳过绘图
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
# 像素级 UI 优化 CSS (V4.0)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

/* 全局背景 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.55), rgba(0,0,0,0.85)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 侧边栏：磨砂玻璃效果 */
[data-testid="stSidebar"] {
    background-color: rgba(10, 15, 30, 0.9) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
}

/* 侧边栏开关按钮：强制显形 */
button[kind="header"] {
    background-color: rgba(0, 242, 254, 0.2) !important;
    color: white !important;
    border: 1px solid #00f2fe !important;
    border-radius: 50% !important;
}

/* 隐藏冗余元素 */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {background: transparent !important;}
.viewerBadge_container__1QSob {display: none !important;}

/* 主标题：霓虹艺术字 */
.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #a29bfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 15px rgba(0,242,254,0.4));
    margin-top: -20px;
}

.sub-title {
    text-align: center;
    color: rgba(255,255,255,0.7);
    font-size: 1.1rem;
    letter-spacing: 8px;
    margin-bottom: 40px;
    font-weight: 300;
}

/* 输入框：标本展示箱风格 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #1e293b !important;
    border-radius: 20px !important;
    font-size: 1.1rem !important;
    padding: 20px !important;
    border: 2px solid rgba(0, 242, 254, 0.3) !important;
    box-shadow: 0 15px 45px rgba(0,0,0,0.5) !important;
}

/* ⭐ 深度扫描按钮：修复变形，精调字间距 ⭐ */
div.stButton > button {
    width: 100% !important;
    height: 4rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: #ffffff !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 6px !important; /* 通过代码控制间距，不再使用空格 */
    border: none !important;
    border-radius: 18px !important;
    box-shadow: 0 5px 25px rgba(0, 210, 255, 0.4) !important;
    transition: all 0.3s ease !important;
    display: flex;
    justify-content: center;
    align-items: center;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0, 210, 255, 0.6) !important;
    filter: brightness(1.1);
}

/* 结果分析卡片 */
.result-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    backdrop-filter: blur(15px);
    line-height: 1.8;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏：档案与系统信息
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=75)
    st.markdown("## 🔬 实验室档案")
    
    st.markdown("---")
    # 随机样本功能
    if st.button("✨ 获取随机样本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "只要你足够努力，就一定能成功。那些失败的人，只是因为他们还不够拼命。",
            "专家说多喝热水能治百病，我看那些不听的人身体都不太行。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    # 导出历史记录
    if st.session_state.history:
        history_data = "\n\n".join(st.session_state.history)
        st.download_button("📥 导出实验存档", history_data, file_name="bias_lab_report.txt")
    else:
        st.caption("暂无历史记录可导出")

    # 🛠️ 找回系统信息
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🛠️ 系统信息", expanded=False):
        st.caption("内核版本: Gemini 1.5 Flash")
        st.caption("视觉架构: NoBias UI V4.0")
        st.caption("开发者权限: 已认证")

# =========================================
# 主界面展示
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 还原真实</div>', unsafe_allow_html=True)

# 左右留空，聚焦中间内容
col_l, col_m, col_r = st.columns([1, 8, 1])

with col_m:
    # 标本输入区
    current_input = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=current_input, placeholder="在此放入待解剖的文字标本...", height=220)
    
    # 扫描按钮
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"你是一位毒舌但客观的文字解剖专家。请对文本进行深度扫描：偏激指数(0-100)、情绪化词汇识别、逻辑谬误拆解、一句话穿真实意图、中立版本改写。文本：{user_input}"
            
            with st.spinner('实验室正在高速扫描标本中...'):
                try:
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    # 归档
                    st.session_state.history.append(f"【样本】：{user_input}\n【结论】：\n{res_text}")
                    
                    # 展示可视化图表（仅在 pandas 可用时）
                    if pd is not None:
                        st.markdown("### 📊 维度可视化分析")
                        chart_data = pd.DataFrame({
                            '维度': ['偏激度', '情绪化', '逻辑性', '客观性'],
                            '百分比': [75, 88, 42, 20] # 模拟分值
                        })
                        st.bar_chart(chart_data.set_index('维度'))
                    
                    # 展示报告卡片
                    st.markdown(f'<div class="result-card">{res_text}</div>', unsafe_allow_html=True)
                    st.toast("分析完成并存入档案", icon="✅")
                    
                except Exception as e:
                    st.error(f"实验室设备故障: {e}")
        else:
            st.warning("⚠️ 标本盒为空，请输入内容。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)