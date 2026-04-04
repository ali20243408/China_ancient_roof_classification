import streamlit as st
from pathlib import Path

# 全局配置
st.set_page_config(
    page_title="古建筑屋顶可视化平台",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------- 路径 --------------------------
current_dir = Path(__file__).parent
bg_img_path = current_dir / "photos" / "images4" / "背景.jpg"
font_path = current_dir / "fonts" / "HongLeiBanShuJianTi-2.ttf"

img_paths = [
    current_dir / "photos" / "images4" / "官式.jpg",
    current_dir / "photos" / "images4" / "民居.jpg",
    current_dir / "photos" / "images4" / "园林.jpg",
    current_dir / "photos" / "images4" / "ai识别.jpg"
]

# -------------------------- 工具函数 --------------------------
def get_base64(file_path):
    import base64
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# -------------------------- 样式：增加云端通用中文字体后备，原有样式丝毫不改 --------------------------
st.markdown(
    f"""
    <style>
    /* 全局页面默认文字后备系统中文字体，云端不崩中文 */
    * {{
        font-family: WenQuanYi Zen Hei, WenQuanYi Micro Hei, SimHei, STKaiti, KaiTi, serif !important;
    }}

    /* 1. 背景样式（完全保留原样） */
    .stApp {{
        background-image: url("data:image/jpg;base64,{get_base64(bg_img_path)}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    .main .block-container {{
        background-color: rgba(253, 249, 242, 0.88) !important;
        border-radius: 12px !important;
        padding: 2rem 3rem 4rem 3rem !important;
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    h1 {{
        text-align: center !important;
        font-family: 'HongLeiBanShuJianTi-2', WenQuanYi Zen Hei, STKaiti, KaiTi, serif !important;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #5D4037 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1) !important;
    }}
    .spacer {{
        flex-grow: 1 !important;
        min-height: 235px !important;
    }}

    /* 2. 图片木质画框（原样保留） */
    .stImage {{
        border: 8px solid #8B5A2B !important;
        border-radius: 12px !important;
        padding: 8px !important;
        background-color: #f5f5dc !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        overflow: hidden !important;
        background-image: repeating-linear-gradient(
            45deg,
            rgba(139, 90, 43, 0.1),
            rgba139, 90, 43, 0.1) 10px,
            rgba160, 110, 60, 0.05) 10px,
            rgba160, 110, 60, 0.05) 20px
        !important;
    }}
    .stImage img {{
        border-radius: 4px !important;
        display: block !important;
        width: 100% !important;
    }}

    /* 3. 按钮样式不变，补字体后备 */
    .stButton>button {{
        width: 100% !important;
        background-color: rgba(180, 140, 100, 0.25) !important;
        border: 1.5px solid rgba(139, 119, 101, 0.4) !important;
        border-radius: 10px !important;
        font-family: WenQuanYi Zen Hei, Microsoft YaHei, sans-serif !important;
        font-size: 1.1rem !important;
        color: #5D4037 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }}
    .stButton>button:hover {{
        background-color: rgba(180, 140, 100, 0.4) !important;
        border-color: rgba139, 119, 101, 0.7) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }}

    /* 4. 侧边导航原样保留+字体兜底 */
    [data-testid="stSidebar"] {{
        background-color: rgba(253, 249, 242, 1) !important;
        border: none !important;
        background-image: none !important;
    }}
    [data-testid="stSidebar"] .stNav li span {{
        color: #5D4037 !important;
        font-family: WenQuanYi Zen Hei !important;
    }}
    [data-testid="stSidebar"] [data-testid="stNav"] a {{
        background-color: transparent !important;
    }}
    [data-testid="stSidebar"] [data-testid="stNav"] a[aria-current="page"] {{
        background-color: rgba(180, 140, 100, 0.2) !important;
        color: #5D4037 !important;
        font-weight: bold !important;
        font-family: WenQuanYi Zen Hei !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 本地手写字体加载完全保留，找不到就自动用系统WenQuanYi兜底
if font_path.exists():
    st.markdown(
        f"""
        <style>
        @font-face {{
            font-family: 'HongLeiBanShuJianTi-2';
            src: url('data:font/ttf;base64,{get_base64(font_path)}') format('truetype');
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------- 页面主体原样不动 --------------------------
st.title("中国古建筑屋顶多维度可视化综合平台")
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

cols = st.columns(4, gap="large")

page_file_paths = [
    "pages/01_官式屋顶.py",
    "pages/02_民居屋顶.py",
    "pages/03_园林屋顶.py",
    "pages/04_智能识别.py"
]

captions = [
    "官式屋顶",
    "民居屋顶",
    "园林屋顶",
    "智能识别"
]

for col, img_path, caption, page_path in zip(cols, img_paths, captions, page_file_paths):
    with col:
        st.image(str(img_path), use_container_width=True)
        if st.button(caption, key=caption, use_container_width=True):
            st.switch_page(page_path)