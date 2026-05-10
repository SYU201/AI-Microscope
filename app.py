import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import os
import time

# =========================================
# 1. API 核心初始化 (严格读取 Secrets)
# =========================================
# 优先从 st.secrets 获取，确保云端运行正常
G_KEY = st.secrets.get("GOOGLE_API_KEY", "")
K_KEY = st.secrets.get("KIMI_API_KEY", "")

# 初始化 Gemini
if G_KEY:
    genai.configure(api_key=G_KEY)

# 初始化 Kimi
k_client = None
if K_KEY:
    k_client = OpenAI(
        api_key=K_KEY,
        base_url="https://api.moonshot.cn/v1",
    )

# 页面基础配置
st.set_page_config(
    page_title="NoBias AI 心理实验室",
    page_icon="🔍",
    layout="wide"
)

# 初始化 Session State
if 'history' not in st.session_state:
    st.session_state.history = []
if 'random_text' not in st.session_state:
    st.session_state.random_text = ""

# =========================================
# 2. UI 界面样式 (V4.2 经典皮肤)
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
}

.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #a29bfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.result-card {
    background: rgba(255,255,255,0.08);
    border-left: 5px solid #00f2fe;
    border-radius: 15px;
    padding: 25px;
    margin-top: 20px;
    color: white;
}

div.stButton > button {
    width: 100% !important;
    height: 3.8rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    border-radius: 15px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 3. 侧边栏控制台
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=60)
    st.markdown("### 🔬 实验配置")
    
    # 模型选择
    engine = st.selectbox(
        "选择分析引擎",
        ["Gemini 1.5 Flash", "Kimi (备用)"]
    )
    
    st.markdown("---")
    if st.button("✨ 获取随机待检样本"):
        samples = [
            "现在的年轻人真是越来越懒了，根本不理解父母的辛苦。",
            "只要你足够努力，就一定能成功。失败的人只是不够拼。",
            "这个设计简直是天才！虽然贵但绝对物有所值。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")
    st.markdown("📂 **历史档案**")
    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history)):
            st.caption(f"记录 {len(st.session_state.history)-i}: {h[:30]}...")
    else:
        st.caption("暂无实验记录")

# =========================================
# 4. 主界面：解剖逻辑
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:gray;">DECONSTRUCTING BIAS</p>', unsafe_allow_html=True)

_, col_m, _ = st.columns([1, 8, 1])

with col_m:
    # 输入区域
    user_input = st.text_area("", value=st.session_state.random_text, placeholder="输入标本...", height=200)
    
    if st.button("启 动 深 度 扫 描"):
        if not user_input:
            st.warning("实验舱为空，请输入文字。")
        else:
            prompt = f"你是一位文字解剖专家。请对以下文本进行深度分析：偏激指数、意图拆解、中立改写。文本：{user_input}"
            
            with st.status(f"正在调用 {engine} 内核...", expanded=True) as status:
                full_response = ""
                placeholder = st.empty()
                
                try:
                    # --- 分支：Gemini ---
                    if engine == "Gemini 1.5 Flash":
                        if not G_KEY:
                            raise ValueError("Gemini Key 未配置")
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(prompt, stream=True)
                        for chunk in response:
                            full_response += chunk.text
                            placeholder.markdown(f'<div class="result-card">{full_response}</div>', unsafe_allow_html=True)
                    
                    # --- 分支：Kimi ---
                    else:
                        if not k_client:
                            raise ValueError("Kimi Key 未配置")
                        completion = k_client.chat.completions.create(
                            model="moonshot-v1-8k",
                            messages=[{"role": "user", "content": prompt}],
                            stream=True
                        )
                        for chunk in completion:
                            delta = chunk.choices[0].delta.content
                            if delta:
                                full_response += delta
                                placeholder.markdown(f'<div class="result-card">{full_response}</div>', unsafe_allow_html=True)

                    if full_response:
                        st.session_state.history.append(full_response)
                        status.update(label="扫描成功", state="complete", expanded=False)
                        
                except Exception as e:
                    status.update(label="设备故障", state="error")
                    st.error(f"分析失败。请确保 Secrets 中 Key 填写正确且无空格。错误提示: {e}")

st.markdown("<br><center style='color:rgba(255,255,255,0.2)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)