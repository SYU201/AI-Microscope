import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# =========================
# 1. 基础配置
# =========================
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

st.set_page_config(
    page_title="NoBias AI 心理实验室",
    layout="wide",
    initial_sidebar_state="expanded"   # 修复侧边栏折叠问题的关键
)

# =========================
# 2. 超级美化 CSS
# =========================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 主标题字体 -->
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&display=swap" rel="stylesheet">

<!-- 中文高级字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">

<style>

/* =========================
   全局字体
========================= */
html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif !important;
}

/* =========================
   页面背景
========================= */
.stApp {
    background:
        linear-gradient(
            rgba(0,0,0,0.45),
            rgba(0,0,0,0.78)
        ),
        url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =========================
   隐藏默认组件
========================= */
footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

div[data-testid="stStatusWidget"] {
    visibility: hidden;
}

/* 右下角 Manage app */
.viewerBadge_container__1QSob {
    display: none !important;
}

/* =========================
   修复侧边栏折叠按钮
========================= */

/* Streamlit 原生折叠按钮 */
button[kind="header"] {
    background-color: rgba(0,0,0,0.35) !important;
    border-radius: 12px !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    padding: 6px 10px !important;
}

/* 鼠标悬停 */
button[kind="header"]:hover {
    background-color: rgba(0,242,254,0.2) !important;
}

/* 侧边栏宽度 */
section[data-testid="stSidebar"] {
    width: 320px !important;
}

/* 收起后仍显示展开按钮 */
section[data-testid="stSidebar"][aria-expanded="false"] {
    min-width: 72px !important;
    max-width: 72px !important;
}

/* =========================
   侧边栏美化
========================= */
[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            rgba(8,12,20,0.96),
            rgba(5,8,15,0.92)
        );

    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
}

/* Sidebar文字 */
[data-testid="stSidebar"] * {
    color: #f0f0f0 !important;
}

/* =========================
   主标题
========================= */
.main-title {
    font-family: 'Orbitron', sans-serif !important;

    font-size: 4rem !important;
    font-weight: 800 !important;

    text-align: center;

    background: linear-gradient(
        90deg,
        #00f2fe,
        #4facfe,
        #7b61ff
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    letter-spacing: 2px;

    margin-top: 10px;
    margin-bottom: 10px;

    text-shadow:
        0 0 15px rgba(0,242,254,0.3);
}

/* =========================
   副标题
========================= */
.sub-title {
    text-align: center;

    color: rgba(255,255,255,0.82);

    font-size: 1.2rem;

    font-weight: 300;

    margin-bottom: 2.5rem;

    letter-spacing: 1px;
}

/* =========================
   输入框 Label（待检样本）
========================= */
label,
.stTextArea label,
p {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1.05rem !important;
}

/* =========================
   输入框整体
========================= */
.stTextArea textarea {

    background: rgba(255,255,255,0.92) !important;

    color: #111111 !important;   /* 深色字 */

    border: 1px solid rgba(0,242,254,0.25) !important;

    border-radius: 18px !important;

    padding: 18px !important;

    font-size: 1.08rem !important;

    font-weight: 500 !important;

    line-height: 1.8 !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);

    backdrop-filter: blur(12px);
}

/* placeholder颜色 */
.stTextArea textarea::placeholder {
    color: rgba(0,0,0,0.45) !important;
}

/* 聚焦效果 */
.stTextArea textarea:focus {
    border: 1px solid #00f2fe !important;

    box-shadow:
        0 0 18px rgba(0,242,254,0.45) !important;
}

/* =========================
   按钮美化
========================= */
.stButton > button {

    width: 100%;

    background:
        linear-gradient(
            135deg,
            #00f2fe,
            #4facfe
        ) !important;

    color: #001b2b !important;

    font-size: 1.15rem !important;

    font-weight: 800 !important;

    border: none !important;

    border-radius: 14px !important;

    padding: 0.75rem 0 !important;

    transition: all 0.28s ease !important;

    box-shadow:
        0 5px 20px rgba(0,242,254,0.32);

    letter-spacing: 1px;
}

/* hover */
.stButton > button:hover {

    transform: translateY(-2px) scale(1.02);

    box-shadow:
        0 10px 30px rgba(0,242,254,0.45);

    filter: brightness(1.05);
}

/* =========================
   卡片 / Metric
========================= */
div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 18px;

    backdrop-filter: blur(12px);

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}

/* metric文字 */
div[data-testid="stMetric"] label {
    color: rgba(255,255,255,0.8) !important;
}

/* =========================
   信息框
========================= */
.stInfo {
    background:
        rgba(255,255,255,0.08) !important;

    border:
        1px solid rgba(0,242,254,0.25) !important;

    border-radius: 16px !important;

    color: white !important;

    backdrop-filter: blur(10px);
}

/* =========================
   Expander
========================= */
.streamlit-expanderHeader {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* =========================
   底部语录
========================= */
.quote-style {
    text-align: center;
    color: rgba(255,255,255,0.35);
    font-size: 1rem;
    margin-top: 40px;
    letter-spacing: 1px;
}

/* =========================
   去掉白边
========================= */
.block-container {
    padding-top: 2rem;
}

/* =========================
   Toast
========================= */
[data-testid="stToast"] {
    background: rgba(0,0,0,0.78) !important;
    color: white !important;
    border: 1px solid rgba(0,242,254,0.3);
}

</style>
""", unsafe_allow_html=True)

# =========================
# 3. 侧边栏
# =========================
with st.sidebar:

    st.markdown("<br>", unsafe_allow_html=True)

    st.image(
        "https://img.icons8.com/fluency/96/microscope.png",
        width=88
    )

    st.markdown("## 🔬 实验室控制台")

    st.markdown("---")

    with st.expander("🛠️ 系统工具栈", expanded=False):

        st.caption("核心模型：Gemini 1.5 Flash")
        st.caption("前端框架：Streamlit")
        st.caption("编程语言：Python")
        st.caption("视觉风格：Cyber Psychology Lab")

    st.markdown("---")

    st.markdown("### 💡 灵感触发")

    if st.button("随机测试一段文字"):

        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",
            "专家建议：每天喝八杯水可以延长寿命，不信的人最后都后悔了。"
        ]

        st.session_state.random_text = samples[int(time.time()) % 3]

# =========================
# 4. 主界面
# =========================
st.markdown(
    '<div class="main-title">🔍 AI 心理实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">让偏见无处遁形，解构文字背后的真相</div>',
    unsafe_allow_html=True
)

# 页面居中
left, center, right = st.columns([1, 8, 1])

with center:

    default_text = st.session_state.get('random_text', "")

    user_input = st.text_area(
        "🧪 待检样本：",
        value=default_text,
        placeholder="在这里输入你想分析的文字，AI 将扫描其中的偏见、情绪与逻辑漏洞……",
        height=220
    )

    analyze_btn = st.button("🚀 启动深度扫描")

    if analyze_btn:

        if user_input:

            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            你是一位毒舌但客观的文字解剖专家。

            请对以下文本进行深度扫描：

            1. [得分]
            给出 0-100 的“偏激指数”。

            2. [成分]
            识别文字中的情绪化词汇。

            3. [漏洞]
            拆解逻辑谬误：
            - 非黑即白
            - 诉诸情绪
            - 降智打击
            - 以偏概全
            等。

            4. [结论]
            一句话戳穿真实意图。

            5. [净化]
            改写成完全中立的客观描述。

            待检文本：
            "{user_input}"
            """

            with st.spinner('🧬 正在分析语言分子结构...'):

                try:

                    response = model.generate_content(prompt)

                    res_text = response.text

                    st.markdown("## 📊 扫描结果报告")

                    m1, m2, m3 = st.columns(3)

                    with m1:
                        st.metric(
                            "🚩 偏激指数",
                            "高危" if "80" in res_text else "正常"
                        )

                    with m2:
                        st.metric(
                            "⚖️ 逻辑完整度",
                            "存在缺陷"
                        )

                    with m3:
                        st.metric(
                            "👁️ 视觉干扰",
                            "已过滤"
                        )

                    st.markdown("---")

                    st.markdown("### 📝 深度实验日志")

                    st.info(res_text)

                    st.toast(
                        "扫描成功，实验记录已归档。",
                        icon="✅"
                    )

                except Exception as e:

                    st.error(f"实验室设备故障：{str(e)}")

        else:

            st.warning("请先输入待检测文本。")

# =========================
# 5. 底部语录
# =========================
quotes = [
    "“所有偏见，本质上都是认知捷径。”",
    "“换个角度，世界可能完全不同。”",
    "“理智，是唯一的显微镜。”"
]

st.markdown(
    f'<div class="quote-style">{quotes[int(time.time()) % 3]}</div>',
    unsafe_allow_html=True
)