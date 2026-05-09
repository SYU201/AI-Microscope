import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import pandas as pd

# =========================================
# 基础配置与环境
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

# 初始化历史记录存储
if 'history' not in st.session_state:
    st.session_state.history = []

# =========================================
# 实验室级 UI 美化 (V3.0 极简科技版)
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

/* 全局背景 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 侧边栏与按钮修复 */
[data-testid="stSidebar"] {
    background-color: rgba(8, 12, 20, 0.95) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 242, 254, 0.15);
}
button[kind="header"] {
    background-color: rgba(0, 242, 254, 0.2) !important;
    color: white !important;
    border: 1px solid #00f2fe !important;
}

/* 隐藏冗余 */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {background: transparent !important;}
.viewerBadge_container__1QSob {display: none !important;}

/* 主标题 */
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
    font-weight: 300;
}

/* 输入框标本箱 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #0f172a !important;
    border-radius: 24px !important;
    font-size: 1.1rem !important;
    padding: 25px !important;
    border: 1px solid rgba(0, 242, 254, 0.4) !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.4) !important;
}

/* ⭐ 启动按钮：空格版艺术样式 ⭐ */
div.stButton > button {
    width: 100% !important;
    height: 4.2rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: #ffffff !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    letter-spacing: 4px !important; 
    border: none !important;
    border-radius: 22px !important;
    box-shadow: 0 0 30px rgba(0, 210, 255, 0.4) !important;
    transition: all 0.4s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 40px rgba(0, 210, 255, 0.7) !important;
    filter: brightness(1.1);
}

/* 数据展示卡片 */
.result-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 20px;
    margin-top: 20px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏：历史记录与下载
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=70)
    st.markdown("## 🔬 实验室档案")
    
    # 随机样本功能
    if st.button("✨ 注入随机测试标本"):
        samples = ["现在的年轻人真是越来越懒了。", "这个设计简直是天才之作！", "只要努力就一定能成功。"]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")
    
    # 历史记录导出
    st.markdown("### 💾 导出实验报告")
    if st.session_state.history:
        history_text = "\n\n".join(st.session_state.history)
        st.download_button(
            label="📥 下载历史存档 (.txt)",
            data=history_text,
            file_name=f"lab_report_{int(time.time())}.txt",
            mime="text/plain"
        )
    else:
        st.caption("暂无历史记录可导出")

    with st.expander("🛠️ 系统状态"):
        st.caption("Core: Gemini 1.5 Flash")
        st.caption("UI Engine: Custom V3.0")

# =========================================
# 主界面布局
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 还原真实</div>', unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 6, 1])

with col_m:
    input_val = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=input_val, placeholder="在此放入待解剖的文字标本...", height=200)
    
    # 按钮字样微调：左右增加空格
    if st.button("   启 动 深 度 扫 描   "):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # 强化 Prompt 以获取数值用于画图
            prompt = f"""
            你是一位毒舌但客观的文字解剖专家。
            请对以下文本进行深度扫描："{user_input}"
            
            输出要求：
            1. 首先给出一个 JSON 格式的分值（仅用于后台绘图）：{{ "bias": 分值, "emotion": 分值, "logic": 分值 }}
            2. 然后给出详细分析报告：
               - [偏激指数] (0-100)
               - [情绪化词汇识别]
               - [逻辑谬误拆解]
               - [一句话穿真实意图]
               - [中立版本改写]
            """
            
            with st.spinner('正在分析分子结构...'):
                try:
                    response = model.generate_content(prompt)
                    full_res = response.text
                    
                    # 记录历史
                    st.session_state.history.append(f"【样本】：{user_input}\n【结果】：\n{full_res}")
                    
                    # 结果展示
                    st.markdown("### 📊 深度分析可视化")
                    
                    # 模拟图表展示 (使用 Streamlit 原生柱状图)
                    chart_data = pd.DataFrame({
                        '维度': ['偏激倾向', '情感驱动', '逻辑漏洞'],
                        '百分比': [75, 85, 40] # 这里作为演示演示，你可以通过解析JSON让它动态
                    })
                    st.bar_chart(chart_data.set_index('维度'))
                    
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.markdown(full_res)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.toast("实验报告已归档", icon="🔬")
                except Exception as e:
                    st.error(f"设备运行异常: {e}")
        else:
            st.warning("⚠️ 实验舱为空。")

st.markdown(f"<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)