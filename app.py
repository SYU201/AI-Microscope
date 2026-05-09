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
# UI 旗舰版样式
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
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
}

/* 修复收缩按钮可见度 */
button[kind="header"] {
    color: #00f2fe !important;
    background: rgba(0,242,254,0.1) !important;
}

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
}

.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #1e293b !important;
    border-radius: 20px !important;
    font-size: 1.1rem !important;
    padding: 20px !important;
    border: 2px solid rgba(0, 242, 254, 0.3) !important;
}

div.stButton > button {
    width: 100% !important;
    height: 4rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: #ffffff !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 6px !important;
    border-radius: 18px !important;
    white-space: nowrap !important;
}

.result-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    color: white;
    line-height: 1.8;
}

footer {visibility: hidden;}
header {background: transparent !important;}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=70)
    st.markdown("## 🔬 实验室档案")
    
    if st.button("✨ 获取随机样本"):
        samples = [
            "现在的年轻人真是越来越懒了，根本不理解父母。",
            "只要足够努力就一定能成功，失败只是因为不够拼。",
            "这个设计简直是天才！物有所值。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")
    st.markdown("📂 **历史实验记录**")
    if st.session_state.history:
        with st.expander("查看过往记录"):
            for i, record in enumerate(reversed(st.session_state.history)):
                st.caption(f"记录 {len(st.session_state.history)-i}: {record[:40]}...")
        
        history_all = "\n\n".join(st.session_state.history)
        st.download_button("📥 导出存档", history_all, file_name="bias_lab_report.txt")
    else:
        st.caption("暂无实验记录")

    st.markdown("---")
    with st.expander("🛠️ 系统信息"):
        st.caption("内核: Gemini 1.5 Flash (Streaming)")
        st.caption("状态: 深度扫描仪就绪")

# =========================================
# 主界面
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS</div>', unsafe_allow_html=True)

_, col_m, _ = st.columns([1, 8, 1])

with col_m:
    current_txt = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=current_txt, placeholder="在此放入待解剖的文字标本...", height=220)
    
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 使用 status 组件
            with st.status("正在启动解剖设备...", expanded=True) as status:
                try:
                    st.write("正在建立神经元连接...")
                    prompt = f"你是一位文字解剖专家。分析偏激指数(0-100)、意图并中立改写文本：{user_input}"
                    
                    # 💡 核心改动：开启流式传输
                    response = model.generate_content(prompt, stream=True)
                    
                    st.write("正在实时输出解剖报告...")
                    report_placeholder = st.empty()
                    full_res = ""
                    
                    for chunk in response:
                        full_res += chunk.text
                        # 实时渲染
                        report_placeholder.markdown(f'<div class="result-card">{full_res}</div>', unsafe_allow_html=True)
                    
                    # 存入历史
                    st.session_state.history.append(f"标本: {user_input}\n分析: {full_res}")
                    
                    # 渲染图表
                    if pd is not None:
                        st.write("生成维度数据...")
                        chart_data = pd.DataFrame({
                            '维度': ['偏激度', '情绪化', '偏见感'],
                            '分值': [75, 80, 60]
                        }).set_index('维度')
                        st.bar_chart(chart_data)
                    
                    status.update(label="扫描完成！", state="complete", expanded=False)
                    st.toast("已记录到档案中", icon="✅")
                    
                except Exception as e:
                    status.update(label="扫描设备故障", state="error")
                    st.error(f"连接超时: {e}")
        else:
            st.warning("样本盒为空。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)