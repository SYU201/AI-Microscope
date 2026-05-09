import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import pandas as pd

# =========================================
# 基础配置
# =========================================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="NoBias AI 心理实验室",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化历史记录（仅存在于当前用户的当前会话中）
if 'history' not in st.session_state:
    st.session_state.history = []

# =========================================
# UI 再次升级 (V3.1 稳定美化版)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

.stApp {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 侧边栏及按钮显形修复 */
[data-testid="stSidebar"] {
    background-color: rgba(8, 12, 20, 0.95) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 242, 254, 0.15);
}
button[kind="header"] {
    background-color: rgba(0, 242, 254, 0.3) !important;
    color: white !important;
    border: 1px solid #00f2fe !important;
}

/* 隐藏干扰元素 */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {background: transparent !important;}
.viewerBadge_container__1QSob {display: none !important;}

/* 标题样式 */
.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(135deg, #00f2fe, #4facfe, #a29bfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 5px;
    filter: drop-shadow(0 0 15px rgba(0,242,254,0.3));
}

.sub-title {
    text-align: center;
    color: #ffffff;
    font-size: 1.1rem;
    letter-spacing: 6px;
    margin-bottom: 35px;
    opacity: 0.7;
}

/* 输入框 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #0f172a !important;
    border-radius: 24px !important;
    font-size: 1.1rem !important;
    padding: 25px !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
}

/* 启动按钮：纯白艺术字 + 黄金间距 */
div.stButton > button {
    width: 100% !important;
    height: 4.5rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: #ffffff !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 900 !important;
    letter-spacing: 1px !important; 
    border: none !important;
    border-radius: 22px !important;
    box-shadow: 0 0 30px rgba(0, 210, 255, 0.4) !important;
    transition: all 0.4s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 15px 40px rgba(0, 210, 255, 0.7) !important;
}

/* 结果卡片 */
.result-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 25px;
    margin-top: 20px;
    backdrop-filter: blur(15px);
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=70)
    st.markdown("## 🔬 实验控制台")
    
    if st.button("✨ 随机获取待检样本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",
            "专家说多喝热水能治百病，我看那些不听的人身体都不太行。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")
    st.markdown("### 💾 导出实验报告")
    if st.session_state.history:
        history_text = "\n\n".join(st.session_state.history)
        st.download_button(
            label="📥 下载本次实验存档",
            data=history_text,
            file_name=f"bias_report_{int(time.time())}.txt",
            mime="text/plain"
        )
    else:
        st.caption("暂无历史记录可导出")

# =========================================
# 主界面
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 还原真实</div>', unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 7, 1])

with col_m:
    input_val = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=input_val, placeholder="在此放入待解剖的文字标本...", height=200)
    
    # 按钮字样：左右增加空格
    if st.button("    启 动 深 度 扫 描    "):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"你是一位毒舌但客观的文字解剖专家。请对文本进行深度扫描：偏激指数、情绪化词汇识别、逻辑谬误拆解、一句话穿真实意图、中立版本改写。文本：{user_input}"
            
            with st.spinner('实验室正在高速扫描标本中...'):
                try:
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    # 存入历史（仅限当前会话）
                    st.session_state.history.append(f"【样本】：{user_input}\n【结论】：\n{res_text}")
                    
                    # --- 只有在这里才会渲染结果，防止空值报错 ---
                    st.markdown("### 📊 深度分析报告")
                    
                    # 柱状图：展示维度分值
                    chart_data = pd.DataFrame({
                        '维度': ['偏激指数', '情感浓度', '逻辑漏洞', '语言客观性'],
                        '分值': [78, 92, 45, 20] # 这里你可以根据需求手动设定或随机
                    })
                    st.bar_chart(chart_data.set_index('维度'))
                    
                    # 详细文本结果
                    st.markdown(f'<div class="result-card">{res_text}</div>', unsafe_allow_html=True)
                    
                    st.toast("扫描成功", icon="✅")
                    
                except Exception as e:
                    st.error(f"实验室设备故障：{str(e)}")
        else:
            st.warning("⚠️ 实验舱为空，请放入文字标本。")

st.markdown(f"<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)