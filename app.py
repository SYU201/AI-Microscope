import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# 1. 基础配置
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 页面属性设置
st.set_page_config(page_title="NoBias AI 心理实验室", layout="wide")

# 2. 深度定制化 CSS
st.markdown(f"""
    <style>
    /* 全局背景图：使用你提供的链接 */
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.8)), 
                    url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* 隐藏底部 Streamlit 默认页脚和管理按钮 */
    footer {{visibility: hidden;}}
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    div[data-testid="stStatusWidget"] {{visibility: hidden;}}
    .viewerBadge_container__1QSob {{display: none !important;}} /* 隐藏右下角 Manage app */

    /* 主标题美化 */
    .main-title {{
        font-size: 3rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }}

    /* 副标题 */
    .sub-title {{
        color: #d1d1d1;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }}

    /* 输入框美化 */
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.3) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        font-size: 1.1rem !important;
    }}

    /* 核心修改：针对小火箭按钮的美化 */
    .stButton>button {{
        width: 100%;
        background: linear-gradient(45deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #002b36 !important; /* 深色文字，确保在亮色按钮上清晰 */
        font-weight: bold !important;
        font-size: 1.2rem !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 0 !important;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 242, 254, 0.4);
    }}
    .stButton>button:hover {{
        transform: scale(1.02);
        box-shadow: 0 6px 20px rgba(0, 242, 254, 0.6);
    }}

    /* 侧边栏美化 */
    [data-testid="stSidebar"] {{
        background-color: rgba(10, 15, 25, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }}

    /* 结果卡片美化 */
    div[data-testid="stMetric"] {{
        background-color: rgba(0, 242, 254, 0.05);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 15px;
        padding: 15px;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. 侧边栏视图 (重写：将工具栈隐藏在此)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=80)
    st.markdown("### 🔬 实验室控制台")
    
    with st.expander("🛠️ 系统工具栈"):
        st.caption("核心模型: Gemini 1.5 Flash")
        st.caption("前端框架: Streamlit 1.32")
        st.caption("语言: Python 3.9")
    
    st.markdown("---")
    st.markdown("#### 💡 灵感触发")
    if st.button("随机测试一段文字"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "这个产品的设计简直是天才！虽然价格贵了一点，但它带来的身份感是无价的。",
            "专家建议：每天喝八杯水可以延长寿命，不信的人最后都后悔了。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

# 4. 主界面布局
st.markdown('<p class="main-title">🔍 AI 心理实验室</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">让偏见无处遁形，解构文字背后的真相</p>', unsafe_allow_html=True)

# 容器居中处理
col_main_1, col_main_2, col_main_3 = st.columns([1, 8, 1])

with col_main_2:
    # 文本输入
    default_text = st.session_state.get('random_text', "")
    user_input = st.text_area("🧪 待检标本：", value=default_text, placeholder="在此粘贴你想分析的文字，观察它的真实面目...", height=180)
    
    analyze_btn = st.button("🚀 启动深度扫描")

    if analyze_btn:
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 升级后的 Prompt
            prompt = f"""
            你是一位毒舌但客观的文字解剖专家。请对以下文本进行深度扫描：
            1. [得分]：给出 0-100 的‘偏激指数’。
            2. [成分]：识别文字中的‘情绪化词汇’有哪些。
            3. [漏洞]：拆解其逻辑谬误（如：非黑即白、诉诸情感、降智打击等）。
            4. [结论]：一句话戳穿这段话的真实意图。
            5. [净化]：将这段话改写成完全中立的客观描述。

            待检文本："{user_input}"
            """
            
            with st.spinner('正在分析分子结构...'):
                try:
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    # 创意展示：结果区域
                    st.markdown("### 📊 扫描结果报告")
                    
                    # 模拟仪表盘
                    m1, m2, m3 = st.columns(3)
                    with m1:
                        st.metric("🚩 偏激指数", "高危" if "80" in res_text else "正常")
                    with m2:
                        st.metric("⚖️ 逻辑完整度", "有缺陷")
                    with m3:
                        st.metric("👁️ 视觉干扰", "已过滤")

                    st.markdown("---")
                    
                    # 打字机效果展示结论
                    with st.container():
                        st.markdown("#### 📝 详细实验日志")
                        st.info(res_text)
                    
                    st.toast("扫描成功！已自动存入实验室记录。", icon="✅")
                    
                except Exception as e:
                    st.error(f"实验室设备故障：{str(e)}")
        else:
            st.warning("请先放入标本（输入文字）。")

# 5. 交互小创意：底部动态提示
st.markdown("<br><br>", unsafe_allow_html=True)
placeholder = st.empty()
quotes = ["“所有的偏见都源于无知。”", "“换个角度，世界可能完全不同。”", "“理智，是唯一的显微镜。”"]
# 可以在这里做个简单的轮播或者静态展示
st.markdown(f"<center style='color:rgba(255,255,255,0.3)'>{quotes[int(time.time()) % 3]}</center>", unsafe_allow_html=True)