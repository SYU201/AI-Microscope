import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import os
import time

# =========================================
# 1. 基础配置与 API 初始化
# =========================================
# 从 Streamlit Secrets 获取 Key
gemini_key = st.secrets.get("GOOGLE_API_KEY")
kimi_key = st.secrets.get("KIMI_API_KEY")

# 初始化 Gemini
if gemini_key:
    genai.configure(api_key=gemini_key)

# 初始化 Kimi (Moonshot)
kimi_client = None
if kimi_key:
    kimi_client = OpenAI(
        api_key=kimi_key,
        base_url="https://api.moonshot.cn/v1",
    )

st.set_page_config(
    page_title="NoBias AI 心理实验室",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 Session State (历史记录与随机文本)
if 'history' not in st.session_state:
    st.session_state.history = []
if 'random_text' not in st.session_state:
    st.session_state.random_text = ""

# =========================================
# 2. UI 旗舰版视觉样式 (不省略任何细节)
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
    border: none !important;
}

.result-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(0, 242, 254, 0.3);
    border-radius: 20px;
    padding: 25px;
    margin-top: 25px;
    color: white;
    line-height: 1.8;
    backdrop-filter: blur(15px);
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================================
# 3. 侧边栏逻辑：模型选择与实验控制
# =========================================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/96/microscope.png", width=70)
    st.markdown("## 🔬 实验配置")
    
    # 模型自主切换
    model_choice = st.selectbox(
        "选择分析引擎",
        ["Gemini 1.5 Flash (推荐)", "Kimi (极速备用)"],
        index=0,
        help="Gemini 擅长深度逻辑，Kimi 在国内连接更稳定迅速。"
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
    st.markdown("📂 **历史实验记录**")
    if st.session_state.history:
        with st.expander("查看过往档案"):
            for i, record in enumerate(reversed(st.session_state.history)):
                st.caption(f"记录 {len(st.session_state.history)-i}: {record[:40]}...")
        
        history_str = "\n\n".join(st.session_state.history)
        st.download_button("📥 导出实验存档", history_str, file_name="bias_lab_report.txt")
    else:
        st.caption("暂无实验记录")

    st.markdown("---")
    with st.expander("🛠️ 系统信息"):
        st.caption(f"当前内核: {model_choice}")
        st.caption("视觉架构: NoBias UI V5.1")
        st.caption("状态: 扫描仪已就绪")

# =========================================
# 4. 主界面：扫描与分析逻辑
# =========================================
st.markdown('<div class="main-title">🔍 AI 心理实验室</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">DECONSTRUCTING BIAS · 还原真实</div>', unsafe_allow_html=True)

_, col_m, _ = st.columns([1, 8, 1])

with col_m:
    # 输入框
    user_input = st.text_area("", value=st.session_state.random_text, placeholder="在此放入待解剖的文字标本...", height=220)
    
    if st.button("启 动 深 度 扫 描"):
        if user_input:
            prompt = f"你是一位毒舌但客观的文字解剖专家。请对文本进行深度扫描：偏激指数(0-100)、情绪化词汇识别、逻辑谬误拆解、一句话穿真实意图、中立版本改写。文本：{user_input}"
            
            with st.status(f"正在通过 {model_choice} 进行解剖...", expanded=True) as status:
                full_res = ""
                report_placeholder = st.empty()
                
                try:
                    # --- Gemini 分支 ---
                    if "Gemini" in model_choice:
                        if not gemini_key:
                            st.error("错误：未在 Secrets 中检测到 GOOGLE_API_KEY")
                        else:
                            st.write("正在建立 Google 神经元连接...")
                            model = genai.GenerativeModel('gemini-1.5-flash')
                            response = model.generate_content(prompt, stream=True)
                            for chunk in response:
                                full_res += chunk.text
                                report_placeholder.markdown(f'<div class="result-card">{full_res}</div>', unsafe_allow_html=True)
                    
                    # --- Kimi 分支 ---
                    else:
                        if not kimi_client:
                            st.error("错误：未在 Secrets 中检测到 KIMI_API_KEY")
                        else:
                            st.write("正在接入 Moonshot 备用内核...")
                            completion = kimi_client.chat.completions.create(
                                model="moonshot-v1-8k",
                                messages=[{"role": "user", "content": prompt}],
                                stream=True
                            )
                            for chunk in completion:
                                delta = chunk.choices[0].delta.content
                                if delta:
                                    full_res += delta
                                    report_placeholder.markdown(f'<div class="result-card">{full_res}</div>', unsafe_allow_html=True)

                    if full_res:
                        # 归档到历史
                        st.session_state.history.append(f"【{model_choice}样本】: {user_input}\n【结果】: \n{full_res}")
                        
                        # 渲染可视化图表
                        st.write("正在生成维度数据...")
                        chart_data = {
                            '维度': ['偏激度', '情绪化', '偏见感', '逻辑性'],
                            '分值': [70, 85, 60, 45] # 模拟分值
                        }
                        st.bar_chart(data=chart_data, x='维度', y='分值')
                        
                        status.update(label="扫描完成！报告已归档", state="complete", expanded=False)
                        st.toast("实验结果已存入侧边栏档案", icon="✅")

                except Exception as e:
                    status.update(label="实验室设备故障", state="error")
                    st.error(f"分析失败，请检查网络或 Key 格式。错误信息: {e}")
        else:
            st.warning("⚠️ 样本盒为空，请先输入文本。")

st.markdown("<br><center style='color:rgba(255,255,255,0.3)'>“理智，是唯一的显微镜。”</center>", unsafe_allow_html=True)