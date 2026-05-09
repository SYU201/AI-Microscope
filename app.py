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

# =========================================
# 实验室级 UI 美化 CSS
# =========================================
st.markdown("""
<style>
/* 导入字体 */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Noto+Sans+SC:wght@500;700&display=swap');

/* 全局背景 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.75)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 隐藏冗余 */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.viewerBadge_container__1QSob {display: none !important;}

/* 侧边栏样式修正 - 确保它可见且美观 */
[data-testid="stSidebar"] {
    background-color: rgba(10, 15, 25, 0.85) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
}

/* 主标题 */
.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.5rem !important;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #7b61ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.1rem;
    filter: drop-shadow(0 0 10px rgba(0,242,254,0.3));
}

/* 副标题 */
.sub-title {
    text-align: center;
    color: rgba(255,255,255,0.8);
    font-size: 1.3rem;
    margin-bottom: 2rem;
    letter-spacing: 2px;
}

/* 输入框区域 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    color: #1a1a1a !important;
    border-radius: 15px !important;
    font-size: 1.1rem !important;
    padding: 1.5rem !important;
    border: 2px solid rgba(0, 242, 254, 0.5) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
}

/* ⭐⭐⭐ 核心修改：按钮宽度与艺术感 ⭐⭐⭐ */
div.stButton > button {
    width: 100% !important; /* 强制占满中间栏的宽度 */
    height: 3.5rem !important;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
    color: #002b36 !important; /* 深色文字更清晰 */
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 4px !important; /* 文字间距，增加高级感 */
    border: none !important;
    border-radius: 15px !important;
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.5) !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important;
}

div.stButton > button:hover {
    transform: scale(1.01) !important;
    box-shadow: 0 0 35px rgba(0, 242, 254, 0.8) !important;
    filter: brightness(1.1);
}

/* Metric 卡片美化 */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.1) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 15px;
    padding: 15px;
}

/* 底部语录 */
.quote-style {
    text-align: center;
    color: rgba(255,255,255,0.4);
    font-size: 1rem;
    margin-top: 50px;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏（已恢复）
# =========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
    st.markdown("### 🔬 实验室控制台")
    st.markdown("---")
    
    with st.expander("🛠️ 系统工具栈", expanded=False):
        st.caption("核心模型: Gemini 1.5 Flash")
        st.caption("前端框架: Streamlit Pro")
        st.caption("底层语言: Python 3.9")
        st.caption("视觉设计: Cyber Psych")

    st.markdown("---")
    st.markdown("### 💡 实验样本生成")
    if st.button("🪄 随机获取一个标本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",
            "只要你足够努力，就一定能成功。那些失败的人，只是因为他们还不够拼命。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

# =========================================
# 主界面布局
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">让偏见无处遁形，解构文字背后的真相</div>', unsafe_allow_html=True)

# 使用 columns 居中内容，给按钮足够的展开空间
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    default_text = st.session_state.get("random_text", "")
    user_input = st.text_area(
        "🧪 待检样本：", 
        value=default_text,
        placeholder="在此放入你想解剖的文字...",
        height=200
    )
    
    # 按钮会占满 col2 的宽度
    analyze_btn = st.button("启动深度扫描")

    if analyze_btn:
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"""
            你是一位毒舌但客观的文字解剖专家。请对以下文本进行深度扫描：
            1. [得分]：给出 0-100 的‘偏激指数’。
            2. [成分]：识别其中的‘情绪化词汇’。
            3. [漏洞]：拆解逻辑谬误（如：非黑即白、诉诸情绪等）。
            4. [结论]：一句话戳穿其真实潜台词。
            5. [净化]：改写成完全客观的中立描述。
            
            待检文本："{user_input}"
            """
            
            with st.spinner('正在分析语言分子结构...'):
                try:
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    st.markdown("### 📊 扫描结果报告")
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("🚩 偏激指数", "分析中", delta="-12%")
                    with m2:
                        st.metric("⚖️ 逻辑状态", "有漏洞")
                    with m3:
                        st.metric("👁️ 视觉干扰", "已过滤")
                    
                    st.info(res_text)
                    st.toast("实验报告生成成功！", icon="✅")
                except Exception as e:
                    st.error(f"设备故障: {e}")
        else:
            st.warning("实验舱为空，请输入文字。")

# 底部语录
quotes = ["“所有偏见，本质上都是认知捷径。”", "“理智，是唯一的显微镜。”", "“换个角度，世界可能完全不同。”"]
st.markdown(f'<div class="quote-style">{quotes[int(time.time()) % 3]}</div>', unsafe_allow_html=True)