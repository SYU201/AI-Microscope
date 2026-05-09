import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

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
# UI 样式 (保持 V4.2 风格)
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
}

.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #a29bfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 0 10px rgba(0,242,254,0.3));
}

div.stButton > button {
    width: 100% !important;
    height: 3.8rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 4px !important;
    border-radius: 15px !important;
    white-space: nowrap !important;
}

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
# 侧边栏 (保留历史记录功能)
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=60)
    st.markdown("### 🔬 实验室控制台")
    
    if st.button("✨ 获取随机标本"):
        samples = ["现在的年轻人真是越来越懒了。", "这个设计简直是天才！"]
        st.session_state.random_text = samples[int(time.time()) % 2]

    st.markdown("---")
    st.markdown("📂 **历史实验记录**")
    if st.session_state.history:
        with st.expander("点击展开历史记录"):
            for record in reversed(st.session_state.history):
                st.markdown(f"内容: {record[:30]}...")
        
        if st.download_button("📥 导出存档", "\n\n".join(st.session_state.history), file_name="lab_report.txt"):
            st.success("导出成功！")
    else:
        st.caption("暂无实验记录")

    st.markdown("---")
    with st.expander("🛠️ 系统信息"):
        st.caption("内核: Gemini 1.5 Flash")
        st.caption("状态: 运行中")

# =========================================
# 主界面
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:gray;">DECONSTRUCTING BIAS</p>', unsafe_allow_html=True)

_, col_m, _ = st.columns([1, 8, 1])

with col_m:
    txt = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=txt, placeholder="输入标本...", height=200)
    
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # 💡 增加加载提示
            with st.status("正在启动解剖设备...", expanded=True) as status:
                try:
                    st.write("正在扫描文字分子结构...")
                    # 💡 注意：这里调用 API
                    response = model.generate_content(f"深度分析这段话的偏见、意图并改写：{user_input}")
                    res = response.text
                    
                    # 归档
                    st.session_state.history.append(f"标本: {user_input}\n分析: {res}")
                    
                    status.update(label="扫描完成！", state="complete", expanded=False)
                    st.markdown(f'<div class="result-card">{res}</div>', unsafe_allow_html=True)
                    st.toast("已自动存入历史记录", icon="✅")
                except Exception as e:
                    status.update(label="设备超时或故障", state="error")
                    st.error(f"连接 Google 实验室超时，请稍后再试或检查 API 密钥。错误信息: {e}")
        else:
            st.warning("请先输入标本。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)