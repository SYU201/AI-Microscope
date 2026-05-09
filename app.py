import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# 尝试导入 pandas 确保图表功能正常
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
# 旗舰版 UI 样式（包含所有细节）
# =========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@500;700;900&display=swap');

/* 全局背景与磨砂玻璃 */
.stApp {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.85)), 
                url("https://raw.githubusercontent.com/SYU201/AI-Microscope/main/background.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* 侧边栏样式 */
[data-testid="stSidebar"] {
    background-color: rgba(15, 20, 35, 0.95) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(0, 242, 254, 0.2);
}

/* 强制显示收缩按钮 */
button[kind="header"] {
    color: #00f2fe !important;
    background: rgba(0,242,254,0.1) !important;
}

/* 主标题 */
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

/* 输入框样式 */
.stTextArea textarea {
    background: rgba(255, 255, 255, 0.98) !important;
    color: #1e293b !important;
    border-radius: 20px !important;
    font-size: 1.1rem !important;
    padding: 20px !important;
    border: 2px solid rgba(0, 242, 254, 0.3) !important;
    box-shadow: 0 15px 45px rgba(0,0,0,0.5) !important;
}

/* 深度扫描按钮 */
div.stButton > button {
    width: 100% !important;
    height: 4rem !important;
    background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
    color: #ffffff !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    letter-spacing: 6px !important;
    border-radius: 18px !important;
    white-space: nowrap !important;
    border: none !important;
    box-shadow: 0 5px 25px rgba(0, 210, 255, 0.4) !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 35px rgba(0, 210, 255, 0.6) !important;
}

/* 结果分析卡片 */
.result-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    backdrop-filter: blur(15px);
    line-height: 1.8;
    color: white;
}

/* 隐藏 Streamlit 默认装饰 */
footer {visibility: hidden;}
header {background: transparent !important;}
</style>
""", unsafe_allow_html=True)

# =========================================
# 侧边栏：档案、历史与信息
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=70)
    st.markdown("## 🔬 实验室档案")
    
    # 随机样本
    if st.button("✨ 获取随机样本"):
        samples = [
            "现在的年轻人真是越来越懒了，只想着躺平，根本不理解父母的辛苦。",
            "只要你足够努力，就一定能成功。那些失败的人，只是因为他们还不够拼命。",
            "这个设计简直是天才！虽然贵但物有所值。"
        ]
        st.session_state.random_text = samples[int(time.time()) % 3]

    st.markdown("---")
    
    # 历史记录展示部分
    st.markdown("📂 **历史实验记录**")
    if st.session_state.history:
        with st.expander("查看过往分析"):
            for i, record in enumerate(reversed(st.session_state.history)):
                st.markdown(f"**记录 {len(st.session_state.history)-i}:**")
                st.caption(record[:60] + "...")
        
        # 导出功能
        history_data = "\n\n".join(st.session_state.history)
        st.download_button("📥 导出实验存档", history_data, file_name="bias_lab_report.txt")
    else:
        st.caption("暂无实验记录")

    st.markdown("---")
    
    # 系统信息
    with st.expander("🛠️ 系统信息"):
        st.caption("内核版本: Gemini 1.5 Flash")
        st.caption("视觉架构: NoBias UI V4.3")
        st.caption("状态: 深度扫描仪已就绪")

# =========================================
# 主界面内容
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 还原真实</div>', unsafe_allow_html=True)

col_l, col_m, col_r = st.columns([1, 8, 1])

with col_m:
    # 输入区域
    current_txt = st.session_state.get("random_text", "")
    user_input = st.text_area("", value=current_txt, placeholder="在此放入待解剖的文字标本...", height=220)
    
    # 扫描执行
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # 使用 status 组件提供实时反馈，防止用户以为死机
            with st.status("正在启动解剖设备...", expanded=True) as status:
                try:
                    st.write("正在分析文字分子结构...")
                    prompt = f"你是一位毒舌但客观的文字解剖专家。请对文本进行深度扫描：偏激指数(0-100)、情绪化词汇识别、逻辑谬误拆解、一句话穿真实意图、中立版本改写。文本：{user_input}"
                    
                    response = model.generate_content(prompt)
                    res_text = response.text
                    
                    # 记录到历史
                    st.session_state.history.append(f"【样本】: {user_input}\n【报告】: \n{res_text}")
                    
                    # 渲染可视化图表
                    if pd is not None:
                        st.write("正在生成维度可视化数据...")
                        chart_data = pd.DataFrame({
                            '维度': ['偏激度', '情绪化', '偏见感', '逻辑性'],
                            '分值': [75, 85, 60, 40] # 模拟分值，可根据AI返回内容进一步解析
                        })
                        st.bar_chart(chart_data.set_index('维度'))
                    
                    status.update(label="扫描完成！报告已生成", state="complete", expanded=False)
                    
                    # 展示报告卡片
                    st.markdown(f'<div class="result-card">{res_text}</div>', unsafe_allow_html=True)
                    st.toast("报告已归档", icon="✅")
                    
                except Exception as e:
                    status.update(label="扫描发生故障", state="error")
                    st.error(f"连接失败: {e}")
        else:
            st.warning("⚠️ 样本盒为空。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)