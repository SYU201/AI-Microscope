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
# 超级UI美化 CSS
# =========================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- 主标题科技字体 -->
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&display=swap" rel="stylesheet">

<!-- 中文高级字体 -->
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">

<style>

/* =====================================
   全局字体
===================================== */
html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif !important;
}

/* =====================================
   页面背景
===================================== */
.stApp {

    background:
        linear-gradient(
            rgba(0,0,0,0.45),
            rgba(0,0,0,0.80)
        ),
        url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* =====================================
   隐藏 Streamlit 默认元素
===================================== */
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

/* 右下角 manage app */
.viewerBadge_container__1QSob {
    display: none !important;
}

/* =====================================
   ⭐⭐⭐ 修复侧边栏显示 ⭐⭐⭐
===================================== */

/* 侧边栏整体 */
section[data-testid="stSidebar"] {

    display: block !important;

    visibility: visible !important;

    width: 320px !important;

    min-width: 320px !important;

    background:
        linear-gradient(
            180deg,
            rgba(8,12,20,0.96),
            rgba(5,8,15,0.94)
        );

    border-right:
        1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(20px);

    transition: all 0.3s ease;
}

/* 侧边栏文字 */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* 收起状态 */
section[data-testid="stSidebar"][aria-expanded="false"] {

    min-width: 78px !important;

    width: 78px !important;
}

/* 展开/收起按钮 */
button[kind="header"] {

    display: block !important;

    visibility: visible !important;

    background:
        rgba(0,0,0,0.35) !important;

    color: white !important;

    border-radius: 12px !important;

    border:
        1px solid rgba(255,255,255,0.12) !important;

    margin-left: 10px !important;

    margin-top: 10px !important;

    transition: 0.2s;
}

/* hover */
button[kind="header"]:hover {

    background:
        rgba(0,242,254,0.25) !important;
}

/* 防止按钮消失 */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
}

/* =====================================
   主标题
===================================== */
.main-title {

    font-family: 'Orbitron', sans-serif !important;

    font-size: 4.2rem !important;

    font-weight: 800 !important;

    text-align: center;

    background:
        linear-gradient(
            90deg,
            #00f2fe,
            #4facfe,
            #7b61ff
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    letter-spacing: 3px;

    margin-top: 5px;

    margin-bottom: 10px;

    text-shadow:
        0 0 18px rgba(0,242,254,0.25);
}

/* =====================================
   副标题
===================================== */
.sub-title {

    text-align: center;

    color: rgba(255,255,255,0.85);

    font-size: 1.25rem;

    font-weight: 400;

    margin-bottom: 2.8rem;

    letter-spacing: 1px;
}

/* =====================================
   Label
===================================== */
label,
.stTextArea label {

    color: white !important;

    font-size: 1.15rem !important;

    font-weight: 700 !important;
}

/* =====================================
   输入框
===================================== */
.stTextArea textarea {

    background:
        rgba(255,255,255,0.94) !important;

    color:
        #111111 !important;

    border:
        1px solid rgba(0,242,254,0.25) !important;

    border-radius:
        18px !important;

    padding:
        20px !important;

    font-size:
        1.08rem !important;

    font-weight:
        500 !important;

    line-height:
        1.8 !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);

    backdrop-filter:
        blur(10px);
}

/* placeholder */
.stTextArea textarea::placeholder {

    color:
        rgba(0,0,0,0.45) !important;
}

/* focus */
.stTextArea textarea:focus {

    border:
        1px solid #00f2fe !important;

    box-shadow:
        0 0 18px rgba(0,242,254,0.45) !important;
}

/* =====================================
   按钮（已去掉小火箭）
===================================== */
.stButton > button {

    width: 100%;

    background:
        linear-gradient(
            135deg,
            #00f2fe,
            #4facfe
        ) !important;

    color:
        #001b2b !important;

    font-size:
        1.12rem !important;

    font-weight:
        800 !important;

    border:
        none !important;

    border-radius:
        14px !important;

    padding:
        0.75rem 0 !important;

    transition:
        all 0.28s ease !important;

    box-shadow:
        0 5px 20px rgba(0,242,254,0.32);

    letter-spacing:
        1px;
}

/* hover */
.stButton > button:hover {

    transform:
        translateY(-2px) scale(1.02);

    box-shadow:
        0 10px 30px rgba(0,242,254,0.45);

    filter:
        brightness(1.05);
}

/* =====================================
   metric 卡片
===================================== */
div[data-testid="stMetric"] {

    background:
        rgba(255,255,255,0.06);

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius:
        18px;

    padding:
        18px;

    backdrop-filter:
        blur(12px);

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}

/* =====================================
   info 区域
===================================== */
.stInfo {

    background:
        rgba(255,255,255,0.08) !important;

    border:
        1px solid rgba(0,242,254,0.25) !important;

    border-radius:
        16px !important;

    color:
        white !important;

    backdrop-filter:
        blur(10px);
}

/* =====================================
   expander
===================================== */
.streamlit-expanderHeader {

    font-size:
        1rem !important;

    font-weight:
        700 !important;

    color:
        white !important;
}

/* =====================================
   底部语录
===================================== */
.quote-style {

    text-align:
        center;

    color:
        rgba(255,255,255,0.35);

    font-size:
        1rem;

    margin-top:
        40px;

    letter-spacing:
        1px;
}

/* =====================================
   页面边距
===================================== */
.block-container {

    padding-top:
        2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# 左侧工具栏（已修复）
# =========================================
with st.sidebar:

    st.markdown("<br>", unsafe_allow_html=True)

    st.image(
        "https://img.icons8.com/fluency/96/microscope.png",
        width=90
    )

    st.markdown("## 🔬 实验室控制台")

    st.markdown("---")

    with st.expander("🛠️ 系统工具栈", expanded=False):

        st.caption("核心模型：Gemini 1.5 Flash")
        st.caption("前端框架：Streamlit")
        st.caption("语言：Python")
        st.caption("视觉风格：Cyber Psychology")

    st.markdown("---")

    st.markdown("### 💡 灵感触发")

    if st.button("随机测试一段文字"):

        samples = [

            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",

            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",

            "专家建议：每天喝八杯水可以延长寿命，不信的人最后都后悔了。"
        ]

        st.session_state.random_text = samples[int(time.time()) % 3]

# =========================================
# 主界面
# =========================================
st.markdown(
    '<div class="main-title">🔍 AI 心理实验室</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">让偏见无处遁形，解构文字背后的真相</div>',
    unsafe_allow_html=True
)

# 居中布局
left, center, right = st.columns([1, 8, 1])

with center:

    default_text = st.session_state.get("random_text", "")

    user_input = st.text_area(
        "🧪 待检样本：",
        value=default_text,
        placeholder="在这里输入你想分析的文字，AI 将扫描其中的偏见、情绪与逻辑漏洞……",
        height=220
    )

    # 已去掉小火箭
    analyze_btn = st.button("启动深度扫描")

    if analyze_btn:

        if user_input:

            model = genai.GenerativeModel(
                "gemini-1.5-flash"
            )

            prompt = f"""
            你是一位毒舌但客观的文字解剖专家。

            请对以下文本进行深度扫描：

            1.【得分】
            给出 0-100 的偏激指数。

            2.【成分】
            识别情绪化词汇。

            3.【漏洞】
            拆解逻辑谬误：
            - 非黑即白
            - 诉诸情绪
            - 以偏概全
            - 降智打击
            等。

            4.【结论】
            一句话戳穿真实意图。

            5.【净化】
            改写成完全中立客观的版本。

            待检文本：
            "{user_input}"
            """

            with st.spinner("正在分析语言分子结构..."):

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

                    st.error(
                        f"实验室设备故障：{str(e)}"
                    )

        else:

            st.warning("请先输入待检测文本。")

# =========================================
# 底部语录
# =========================================
quotes = [

    "“所有偏见，本质上都是认知捷径。”",

    "“换个角度，世界可能完全不同。”",

    "“理智，是唯一的显微镜。”"
]

st.markdown(
    f'<div class="quote-style">{quotes[int(time.time()) % 3]}</div>',
    unsafe_allow_html=True
)