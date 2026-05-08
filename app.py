import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. 基础配置
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# 设置页面属性
st.set_page_config(page_title="AI 心理显微镜", layout="wide", initial_sidebar_state="expanded")

# 2. 注入自定义 CSS 美化 (科技感深色背景)
st.markdown("""
    <style>
    /* 全局背景和字体颜色 */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* 美化侧边栏 */
    [data-testid="stSidebar"] {
        background-color: #161B22;
    }

    /* 美化评分卡片 */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        transition: transform 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        background-color: rgba(255, 255, 255, 0.1);
    }

    /* 标题样式 */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        background: -webkit-linear-gradient(#00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. 界面顶部
st.title("🔍 AI 心理显微镜")
st.markdown("### 解剖文字背后的立场、情绪与逻辑陷阱")
st.markdown("---")

# 4. 侧边栏内容
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/microscope.png") # 一个小图标
    st.info("💡 **项目说明**：本工具通过 AI 模型深度解剖社交媒体文本，帮助用户识别‘信息茧房’中的情绪煽动。")
    st.write("**工具栈：**")
    st.code("Gemini 1.5 Flash\nStreamlit\nPython")
    st.markdown("---")
    st.caption("© 2026 AI 创新项目 - 大一学生独立开发")

# 5. 主交互区
user_input = st.text_area("✍️ 请输入你想解剖的文字：", placeholder="在此粘贴微博、知乎或新闻评论...", height=150)

if st.button("🚀 开始深度解剖"):
    if user_input:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 这里的 Prompt 进行了升级，强制 AI 返回易于理解的结构
        prompt = f"""
        你是一位资深的社会语言学家。请对以下文本进行解剖：
        1. 情绪指数：给出一个 0-100 的数值（0为冷静，100为极度偏激）。
        2. 客观程度：给出一个百分比（如 20%）。
        3. 逻辑谬误：识别文中是否有阴阳怪气、人身攻击或煽动焦虑，给出数量。
        4. 详细分析报告：包括立场偏向分析、话语陷阱拆解。
        5. 中立事实版：重写一段没有任何情绪色彩的事实描述。

        待分析文本："{user_input}"
        """
        
        with st.spinner('🔬 显微镜正在扫描文本结构，请稍后...'):
            try:
                response = model.generate_content(prompt)
                full_text = response.text
                
                # --- 美化展示区 (仅在点击后显示) ---
                st.markdown("### 📊 解剖量化指标")
                col1, col2, col3 = st.columns(3)
                
                # 注意：这里的数据目前是让 AI 整体生成，你可以根据 Day 3 的学习尝试用正则表达式提取具体数值
                with col1:
                    st.metric(label="🚩 情绪偏激值", value="分析已完成", delta="查看下方报告")
                with col2:
                    st.metric(label="⚖️ 客观性评分", value="深度扫描中", delta="建议谨慎阅读")
                with col3:
                    st.metric(label="⚠️ 潜在逻辑谬误", value="已检测", delta="点击下方查看")

                st.markdown("---")
                
                # 使用折叠框展示详细报告
                with st.expander("📝 查看深度解剖报告", expanded=True):
                    st.markdown(full_text)
                    
                st.success("解剖完成！请保持独立思考。")
                
            except Exception as e:
                st.error(f"连接 AI 出错啦：{str(e)}")
    else:
        st.warning("🙈 请先输入一段文字，显微镜才能工作哦！")