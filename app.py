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
# 终极 UI 修复与艺术化 CSS
# =========================================
st.markdown("""
<style>
/* 导入高级科技字体 */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Noto+Sans+SC:wght@700;900&display=swap');

/* 全局背景控制 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* --- 侧边栏开关强制显形修复 --- */
button[kind="header"] {
    background-color: rgba(0, 242, 254, 0.2) !important;
    color: white !important;
    border: 1px solid #00f2fe !important;
    border-radius: 50% !important;
}
svg {
    fill: white !important; /* 强制图标变白 */
}

/* 侧边栏本身美化 */
[data-testid="stSidebar"] {
    background-color: rgba(5, 10, 20, 0.9) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(0, 242, 254, 0.3);
}

/* 隐藏不必要的元素 */
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
header {background: transparent !important;}
.viewerBadge_container__1QSob {display: none !important;}

/* 主标题：更强烈的科技感 */
.main-title {
    font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
    font-size: 3.8rem !important;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    text-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
}

.sub-title {
    text-align: center;
    color: #ffffff;
    font-size: 1.2rem;
    letter-spacing: 5px;
    margin-bottom: 30px;
    opacity: 0.8;
}

/* 输入框：磨砂感标本箱 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.95) !important;
    color: #111111 !important;
    border-radius: 20px !important;
    font-size: 1.15rem !important;
    padding: 20px !important;
    border: 2px solid #00f2fe !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
}

/* ⭐⭐⭐ 启动按钮：艺术字 + 极光渐变样式 ⭐⭐⭐ */
div.stButton > button {
    width: 100% !important;
    height: 4.5rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important; /* 极光蓝渐变 */
    color: #ffffff !important; /* 纯白艺术字 */
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 900 !important;
    text-transform: uppercase;
    letter-spacing: 10px !important; /* 极宽间距，非常有艺术感 */
    border: none !important;
    border-radius: 20px !important;
    box-shadow: 0 0 25px rgba(0, 210, 255, 0.6) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    margin-top: 20px !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3); /* 文字立体感 */
}

div.stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 15px 40px rgba(0, 210, 255, 0.8) !important;
    background: linear-gradient(90deg, #3a7bd5 0%, #00d2ff 100%) !important;
}

/* 结果卡片 */
div[data-testid="stMetric"] {
    background: rgba(0, 242, 254, 0.1) !important;
    border: 1px solid rgba(0, 242, 254, 0.4);
    border-radius: 20px;
    backdrop-filter: blur(5px);
}

.quote-style {
    text-align: center;
    color: rgba(255,255,255,0.5);
    margin-top: 60px;
    font-family: 'Noto Sans SC';
    letter-spacing: 2px;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏恢复
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
    st.markdown("## 🔬 实验室控制")
    
    st.markdown("---")
    if st.button("✨ 随机获取待检样本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",
            "只要你足够努力，就一定能成功。那些失败的人，只是因为他们还不够拼命。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]
    
    with st.expander("🛠️ 系统信息"):
        st.caption("引擎: Gemini 1.5 Flash")
        st.caption("版本: Lab 2.0 Custom")

# =========================================
# 主界面展示
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 解构偏见</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 7, 1])

with col2:
    default_text = st.session_state.get("random_text", "")
    user_input = st.text_area(
        "", # 标签留空，更简洁
        value=default_text,
        placeholder="在此放入你想解剖的文字标本...",
        height=220
    )
    
    if st.button("启动深度扫描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"你是一位毒舌但客观的文字解剖专家。请对文本进行深度扫描，包含偏激指数(0-100)、情绪化词汇识别、逻辑谬误拆解、一句话穿真实意图、中立版本改写。文本：{user_input}"
            
            with st.spinner('实验室正在高速扫描标本中...'):
                try:
                    response = model.generate_content(prompt)
                    st.markdown("### 📊 扫描结果报告")
                    m1, m2, m3 = st.columns(3)
                    m1.metric("🚩 偏激指数", "实时监测")
                    m2.metric("⚖️ 逻辑状态", "存在偏差")
                    m3.metric("👁️ 视觉干扰", "已净化")
                    
                    st.info(response.text)
                    st.toast("报告已生成", icon="🔬")
                except Exception as e:
                    st.error(f"设备运行异常: {e}")
        else:
            st.warning("⚠️ 实验舱为空，请放入文字标本。")

st.markdown('<div class="quote-style">“理智，是唯一的显微镜。”</div>', unsafe_allow_html=True)